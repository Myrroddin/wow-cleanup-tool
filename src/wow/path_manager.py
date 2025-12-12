"""WoW installation path detection and management."""

import os
import sys
import winreg
from typing import Optional, List, Tuple, Dict, Any


class PathManager:
    """Manages WoW installation paths and detection."""

    # Common WoW installation locations
    COMMON_PATHS: List[str] = [
        r"C:\World of Warcraft",
        r"C:\Program Files (x86)\World of Warcraft",
        r"C:\Program Files\World of Warcraft",
        r"D:\World of Warcraft",
        r"E:\World of Warcraft",
        r"F:\World of Warcraft",
    ]

    # WoW flavor directories mapped to localization keys
    WOW_FLAVORS: Dict[str, str] = {
        "_retail_": "flavor_retail",
        "_ptr_": "flavor_ptr",
        "_beta_": "flavor_beta",
        "_classic_": "flavor_classic",
        "_classic_era_": "flavor_classic_era",
    }

    def __init__(self, loc: Optional[Any] = None) -> None:
        """Initialize PathManager.

        Args:
            loc: Optional Localization instance for translated flavor names
        """
        self.wow_path: Optional[str] = None
        self.detected_flavors: Dict[str, str] = {}
        self.loc = loc

    def get_flavor_display_name(self, flavor_dir: str) -> str:
        """Get display name for a WoW flavor.

        Args:
            flavor_dir: Flavor directory name (e.g., "_retail_")

        Returns:
            str: Localized display name or fallback English name
        """
        loc_key = self.WOW_FLAVORS.get(flavor_dir)
        if not loc_key:
            return flavor_dir

        # If localization is available, use it
        if self.loc:
            return self.loc._(loc_key)

        # Fallback to English
        fallbacks = {
            "flavor_retail": "Retail (Live)",
            "flavor_ptr": "Public Test Realm",
            "flavor_beta": "Beta",
            "flavor_classic": "Classic",
            "flavor_classic_era": "Classic Era",
        }
        return fallbacks.get(loc_key, flavor_dir)

    def detect_wow_path(self) -> Optional[str]:
        """Detect WoW installation path.

        Returns:
            str: WoW installation path or None if not found
        """
        # Try registry on Windows
        if sys.platform == "win32":
            registry_path = self._get_path_from_registry()
            if registry_path and self._validate_wow_path(registry_path):
                self.wow_path = registry_path
                return registry_path

        # Try common locations
        for path in self.COMMON_PATHS:
            if self._validate_wow_path(path):
                self.wow_path = path
                return path

        return None

    def detect_all_wow_installations(self) -> List[str]:
        """Detect all WoW installations on the system.

        Returns:
            list: List of all valid WoW installation paths
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
        """Get WoW path from Windows registry.

        Returns:
            str: Path from registry or None
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

    def validate_installation(self, path: str) -> Tuple[bool, List[Tuple[str, str]]]:
        """Validate WoW installation and detect all game versions that have been run.

        Args:
            path: Path to WoW installation

        Returns:
            tuple: (is_valid, list_of_flavors) where each flavor is (flavor_dir, display_name)
        """
        if not path or not os.path.exists(path):
            return False, []

        # Detect all flavors that have been run at least once (have WTF/Account folder)
        found_flavors: List[Tuple[str, str]] = []
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
                        found_flavors.append((flavor_dir, display_name))
                except (OSError, PermissionError):
                    continue

        # Valid if at least one flavor has been run
        return len(found_flavors) > 0, found_flavors

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
