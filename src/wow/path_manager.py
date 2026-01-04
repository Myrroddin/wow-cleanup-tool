"""WoW installation path detection and management.

This module provides the PathManager class which handles:
- Automatic detection of World of Warcraft installation paths
- Registry lookups on Windows
- Multi-flavor support (Retail, Classic, PTR, Beta, Classic Era)
- Path validation and installation verification

The PathManager uses a combination of:
1. Windows Registry lookups (if on Windows)
2. Common installation paths (C:, D:, E:, F: drives)
3. Flavor directory detection (_retail_, _classic_, etc.)
4. Installation validation (checking for valid game files/folders)
"""

from functools import lru_cache
import os
import sys
import winreg
from typing import Optional, List, Tuple, Dict, Any

from wow.version_manager import GameVersion


class PathManager:
    """Manages WoW installation paths and detection.

    Responsibilities:
    - Detect WoW installation path from registry or common locations
    - Validate that a path contains a valid WoW installation
    - Detect and manage multiple game flavors (versions)
    - Provide localized display names for flavors

    Added: Initial implementation
    Updated: December 28, 2025 - Enhanced documentation
    """

    # Common WoW installation locations across different drive letters
    # These are checked in order if registry lookup fails
    COMMON_PATHS: List[str] = [
        r"C:\World of Warcraft",  # Most common location
        r"C:\Program Files (x86)\World of Warcraft",  # Battle.net default
        r"C:\Program Files\World of Warcraft",  # Alternative default
        r"D:\World of Warcraft",  # Secondary drive installs
        r"E:\World of Warcraft",
        r"F:\World of Warcraft",
    ]

    # WoW flavor directories mapped to localization keys
    # Each flavor represents a different game version that can coexist
    # December 30, 2025: Updated to use game_version_ keys with base + modifier pattern
    WOW_FLAVORS: Dict[str, str] = {
        "_retail_": "game_version_retail",
        "_ptr_": "game_version_retail+ptr",  # Retail PTR
        "_beta_": "game_version_retail+beta",  # Retail Beta
        "_classic_": "game_version_classic",
        "_classic_ptr_": "game_version_classic+ptr",  # Classic PTR
        "_classic_beta_": "game_version_classic+beta",  # Classic Beta
        "_classic_era_": "game_version_classic_era",
        "_classic_era_ptr_": "game_version_classic_era+ptr",  # Classic Era PTR
    }

    def __init__(self, loc: Optional[Any] = None) -> None:
        """Initialize PathManager with optional localization support.

        Args:
            loc: Optional Localization instance for translated flavor names.
                 If None, English fallback names will be used.

        Returns:
            None

        Attributes Created:
            wow_path: Currently selected WoW installation path (None until detected)
            detected_flavors: Dict mapping flavor dirs to their full paths
            loc: Localization instance for translating flavor names
        """
        self.wow_path: Optional[str] = None
        self.detected_flavors: Dict[str, str] = {}
        self.loc = loc

    @lru_cache(maxsize=128)
    def get_flavor_display_name(self, flavor_dir: str) -> str:
        """Get user-friendly display name for a WoW flavor directory.

        December 30, 2025: Updated to support base + modifier pattern for
        localized display (e.g., "Classic Era PTR", "Retail Beta").

        Converts internal flavor directory names (e.g., "_retail_") to
        localized display names (e.g., "Retail" in English).

        Args:
            flavor_dir: Internal flavor directory name like "_retail_", "_classic_ptr_"

        Returns:
            str: Localized display name if available, otherwise the flavor_dir itself

        Example:
            >>> pm = PathManager(loc)
            >>> pm.get_flavor_display_name("_classic_era_ptr_")
            "Classic Era PTR"  # or translated equivalent
        """
        loc_key = self.WOW_FLAVORS.get(flavor_dir)
        if not loc_key:
            return flavor_dir

        # December 30, 2025: Handle base + modifier pattern (e.g., "game_version_retail+ptr")
        if "+" in loc_key:
            base_key, modifier_key = loc_key.split("+", 1)
            modifier_key = f"game_version_modifier_{modifier_key}"

            if self.loc:
                base = self.loc._(base_key)
                modifier = self.loc._(modifier_key)
                return f"{base} {modifier}"

            # Fallback to English
            base_fallbacks = {
                "game_version_retail": "Retail",
                "game_version_classic": "Classic",
                "game_version_classic_era": "Classic Era",
            }
            modifier_fallbacks = {
                "game_version_modifier_ptr": "PTR",
                "game_version_modifier_beta": "Beta",
            }
            base = base_fallbacks.get(base_key, base_key)
            modifier = modifier_fallbacks.get(modifier_key, modifier_key)
            return f"{base} {modifier}"

        # Simple key without modifier
        if self.loc:
            return self.loc._(loc_key)

        # Fallback to English
        fallbacks = {
            "game_version_retail": "Retail",
            "game_version_classic": "Classic",
            "game_version_classic_era": "Classic Era",
        }
        return fallbacks.get(loc_key, flavor_dir)

    def detect_wow_path(self) -> Optional[str]:
        """Detect WoW installation path automatically.

        Detection Strategy:
        1. On Windows: Check Windows Registry for official install path
        2. Fallback: Check common installation locations in order
        3. Validate each found path to ensure it's a valid WoW installation

        This method updates self.wow_path if a valid installation is found.

        Args:
            None

        Returns:
            str: Valid WoW installation path, or None if not found

        Side Effects:
            Sets self.wow_path to the detected path if successful
        """
        # Try registry on Windows (most reliable method)
        if sys.platform == "win32":
            registry_path = self._get_path_from_registry()
            if registry_path and self._validate_wow_path(registry_path):
                self.wow_path = registry_path
                return registry_path

        # Try common locations as fallback
        for path in self.COMMON_PATHS:
            if self._validate_wow_path(path):
                self.wow_path = path
                return path

        return None

    def detect_all_wow_installations(self) -> List[str]:
        """Detect all WoW installations on the system.

        Unlike detect_wow_path() which returns the first valid installation,
        this method finds ALL valid WoW installations across all drives and
        registry entries. Useful for systems with multiple WoW installs
        (e.g., on different drives, or separate retail/classic installs).

        Args:
            None

        Returns:
            list: List of all valid WoW installation paths (may be empty)
                  Duplicates are automatically removed.
        """
        found_installations: List[str] = []

        # Check registry on Windows
        if sys.platform == "win32":
            registry_path = self._get_path_from_registry()
            if registry_path and self._validate_wow_path(registry_path):
                if registry_path not in found_installations:
                    found_installations.append(registry_path)

        # Check all common locations
        for path in self.COMMON_PATHS:
            if self._validate_wow_path(path):
                if path not in found_installations:
                    found_installations.append(path)

        return found_installations

    def _get_path_from_registry(self) -> Optional[str]:
        """Get WoW installation path from Windows Registry.

        Blizzard's Battle.net installer registers the WoW installation path
        in the Windows Registry. This is the most reliable detection method
        on Windows systems.

        Registry Locations Checked (in order):
        1. HKLM\\SOFTWARE\\WOW6432Node\\Blizzard Entertainment\\World of Warcraft
           (64-bit Windows, 32-bit application)
        2. HKLM\\SOFTWARE\\Blizzard Entertainment\\World of Warcraft
           (32-bit Windows or native 64-bit app)

        Args:
            None

        Returns:
            str: InstallPath value from registry, or None if not found/accessible

        Note:
            Registry access may fail due to:
            - WoW not installed via Battle.net
            - Manual installation without registry entries
            - Permission issues
            All failures are silently handled (returns None).
        """
        registry_keys: List[Tuple[int, str]] = [
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\Blizzard Entertainment\World of Warcraft",
            ),
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Blizzard Entertainment\World of Warcraft",
            ),
        ]

        for hkey, subkey in registry_keys:
            try:
                key = winreg.OpenKey(hkey, subkey)
                path, _ = winreg.QueryValueEx(key, "InstallPath")
                winreg.CloseKey(key)
                if path:
                    return path
            except (FileNotFoundError, OSError):
                continue

        return None

    def _validate_wow_path(self, path: str) -> bool:
        """Validate if path is a valid WoW installation.

        Args:
            path: Path to validate

        Returns:
            bool: True if valid WoW installation (has at least one game version that's been run)
        """
        if not path or not os.path.exists(path):
            return False

        # Must have at least one flavor directory with WTF/Account folder (indicating it's been run)
        for flavor in self.WOW_FLAVORS.keys():
            flavor_path = os.path.join(path, flavor)
            wtf_path = os.path.join(flavor_path, "WTF")
            account_path = os.path.join(wtf_path, "Account")
            if (
                os.path.exists(flavor_path)
                and os.path.exists(wtf_path)
                and os.path.exists(account_path)
            ):
                # Check if Account folder is populated (optimized with scandir)
                try:
                    if self._has_populated_directory(account_path):
                        return True
                except (OSError, PermissionError):
                    continue

        return False

    def validate_wow_path(self, path: str) -> bool:
        """Public method to validate if path is a valid WoW installation.

        Args:
            path: Path to validate

        Returns:
            bool: True if valid WoW installation
        """
        return self._validate_wow_path(path)

    def validate_installation(self, path: str) -> Tuple[bool, List[GameVersion]]:
        """Validate WoW installation and detect all game versions that have been run.

        Args:
            path: Path to WoW installation

        Returns:
            tuple: (is_valid, list_of_versions) where each version is a GameVersion object
        """
        if not path or not os.path.exists(path):
            return False, []

        # Detect all flavors that have been run at least once (have WTF/Account folder)
        found_versions: List[GameVersion] = []
        for flavor_dir in self.WOW_FLAVORS.keys():
            flavor_path = os.path.join(path, flavor_dir)
            wtf_path = os.path.join(flavor_path, "WTF")
            account_path = os.path.join(wtf_path, "Account")
            if (
                os.path.exists(flavor_path)
                and os.path.exists(wtf_path)
                and os.path.exists(account_path)
            ):
                # Check if Account folder is populated (optimized with scandir)
                try:
                    if self._has_populated_directory(account_path):
                        display_name = self.get_flavor_display_name(flavor_dir)
                        version = GameVersion(flavor_dir, display_name, flavor_path)
                        found_versions.append(version)
                except (OSError, PermissionError):
                    continue

        # Valid if at least one flavor has been run
        return len(found_versions) > 0, found_versions

    def detect_flavors(self, wow_path: Optional[str] = None) -> Dict[str, str]:
        """Detect installed WoW flavors that have been run at least once.

        Args:
            wow_path: WoW installation path (uses self.wow_path if None)

        Returns:
            dict: Dictionary of {flavor_dir: display_name}
        """
        path = wow_path or self.wow_path
        if not path or not os.path.exists(path):
            return {}

        self.detected_flavors = {}
        for flavor_dir in self.WOW_FLAVORS.keys():
            flavor_path = os.path.join(path, flavor_dir)
            wtf_path = os.path.join(flavor_path, "WTF")
            account_path = os.path.join(wtf_path, "Account")
            if (
                os.path.exists(flavor_path)
                and os.path.exists(wtf_path)
                and os.path.exists(account_path)
            ):
                # Check if Account folder is populated (optimized with scandir)
                try:
                    if self._has_populated_directory(account_path):
                        display_name = self.get_flavor_display_name(flavor_dir)
                        self.detected_flavors[flavor_dir] = display_name
                except (OSError, PermissionError):
                    continue

        return self.detected_flavors

    def get_flavor_path(self, flavor_dir: str) -> Optional[str]:
        """Get full path to a WoW flavor directory.

        Args:
            flavor_dir: Flavor directory name (e.g., "_retail_")

        Returns:
            str: Full path to flavor directory or None
        """
        if not self.wow_path:
            return None

        flavor_path = os.path.join(self.wow_path, flavor_dir)
        return flavor_path if os.path.exists(flavor_path) else None

    def get_addons_path(self, flavor_dir: str) -> Optional[str]:
        """Get path to AddOns folder for a flavor.

        Args:
            flavor_dir: Flavor directory name

        Returns:
            str: Path to AddOns folder or None
        """
        flavor_path = self.get_flavor_path(flavor_dir)
        if not flavor_path:
            return None

        addons_path = os.path.join(flavor_path, "Interface", "AddOns")
        return addons_path if os.path.exists(addons_path) else None

    def get_wtf_path(self, flavor_dir: str) -> Optional[str]:
        """Get path to WTF folder for a flavor.

        Args:
            flavor_dir: Flavor directory name

        Returns:
            str: Path to WTF folder or None
        """
        flavor_path = self.get_flavor_path(flavor_dir)
        if not flavor_path:
            return None

        wtf_path = os.path.join(flavor_path, "WTF")
        return wtf_path if os.path.exists(wtf_path) else None

    def get_cache_path(self, flavor_dir: str) -> Optional[str]:
        """Get path to Cache folder for a flavor.

        Args:
            flavor_dir: Flavor directory name

        Returns:
            str: Path to Cache folder or None
        """
        flavor_path = self.get_flavor_path(flavor_dir)
        if not flavor_path:
            return None

        cache_path = os.path.join(flavor_path, "Cache")
        return cache_path if os.path.exists(cache_path) else None

    def get_screenshots_path(self) -> Optional[str]:
        """Get path to Screenshots folder.

        Returns:
            str: Path to Screenshots folder or None
        """
        if not self.wow_path:
            return None

        screenshots_path = os.path.join(self.wow_path, "Screenshots")
        return screenshots_path if os.path.exists(screenshots_path) else None

    def get_logs_path(self) -> Optional[str]:
        """Get path to Logs folder.

        Returns:
            str: Path to Logs folder or None
        """
        if not self.wow_path:
            return None

        logs_path = os.path.join(self.wow_path, "Logs")
        return logs_path if os.path.exists(logs_path) else None

    def _has_populated_directory(self, dir_path: str) -> bool:
        """Check if directory has any entries without loading all names.

        Uses os.scandir for efficiency - returns immediately upon finding
        first entry instead of loading entire directory listing into memory.

        Args:
            dir_path: Path to directory to check

        Returns:
            bool: True if directory has at least one entry
        """
        try:
            with os.scandir(dir_path) as it:
                return next(it, None) is not None
        except (OSError, PermissionError):
            return False
