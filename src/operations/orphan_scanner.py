"""OrphanScanner: Detects orphaned SavedVariables files.

Identifies .lua and .bak files in WTF\\Account\\*\\SavedVariables that don't
correspond to currently installed AddOns. These files are leftover from
uninstalled addons and can be safely removed to free up disk space.

Critical Protection:
- Excludes Blizzard_.lua files (required by the game engine)
- Blizzard_.bak files can be safely removed
- Only targets files from truly uninstalled AddOns
"""

import os
from typing import List, Set
from operations.base_scanner import BaseScanner


class OrphanScanner(BaseScanner):
    """Scans for orphaned SavedVariables files from uninstalled AddOns.

    December 30, 2025: Implemented to detect SavedVariables from AddOns
    that have been uninstalled, comparing files in WTF directories to
    AddOn folder names in Interface\\AddOns.
    """

    def _scan_version(self, version_path: str) -> List[str]:
        """Scan a WoW version for orphaned SavedVariables.

        Args:
            version_path: Path to WoW version (e.g., C:\\WoW\\_retail_)

        Returns:
            List of orphaned SavedVariables file paths
        """
        orphans = []

        # December 30, 2025: Get installed AddOn names for comparison
        # This creates the baseline of what SHOULD exist
        addons_path = os.path.join(version_path, "Interface", "AddOns")
        installed_addons = self._get_installed_addons(addons_path)

        # December 30, 2025: Navigate WoW's SavedVariables directory structure
        # Structure: WTF\Account\<account_name>\SavedVariables
        #            WTF\Account\<account_name>\<realm>\SavedVariables
        wtf_path = os.path.join(version_path, "WTF")
        if not os.path.isdir(wtf_path):
            return orphans

        account_path = os.path.join(wtf_path, "Account")
        if not os.path.isdir(account_path):
            return orphans

        # Scan each account (players can have multiple WoW accounts)
        try:
            with os.scandir(account_path) as accounts:
                for account_entry in accounts:
                    if not account_entry.is_dir(follow_symlinks=False):
                        continue

                    # December 30, 2025: Scan account-level SavedVariables
                    # These apply to all characters on all realms
                    sv_path = os.path.join(account_entry.path, "SavedVariables")
                    if os.path.isdir(sv_path):
                        orphans.extend(
                            self._scan_savedvariables(sv_path, installed_addons)
                        )

                    # December 30, 2025: Scan realm-level SavedVariables
                    # Each realm has its own subfolder with per-realm settings
                    try:
                        with os.scandir(account_entry.path) as realms:
                            for realm_entry in realms:
                                if not realm_entry.is_dir(follow_symlinks=False):
                                    continue
                                if realm_entry.name == "SavedVariables":
                                    continue

                                realm_sv = os.path.join(
                                    realm_entry.path, "SavedVariables"
                                )
                                if os.path.isdir(realm_sv):
                                    orphans.extend(
                                        self._scan_savedvariables(
                                            realm_sv, installed_addons
                                        )
                                    )
                    except (OSError, PermissionError):
                        continue

        except (OSError, PermissionError):
            pass

        return orphans

    def _get_installed_addons(self, addons_path: str) -> Set[str]:
        """Get set of installed AddOn folder names.

        Args:
            addons_path: Path to Interface\\AddOns

        Returns:
            Set of AddOn folder names (case-insensitive)
        """
        addons = set()
        if not os.path.isdir(addons_path):
            return addons

        try:
            with os.scandir(addons_path) as entries:
                for entry in entries:
                    if entry.is_dir(follow_symlinks=False):
                        addons.add(entry.name.lower())
        except (OSError, PermissionError):
            pass

        return addons

    def _scan_savedvariables(
        self, sv_path: str, installed_addons: Set[str]
    ) -> List[str]:
        """Scan SavedVariables folder for orphaned files.

        Args:
            sv_path: Path to SavedVariables folder
            installed_addons: Set of installed AddOn names (lowercase)

        Returns:
            List of orphaned file paths
        """
        orphans = []

        try:
            with os.scandir(sv_path) as entries:
                for entry in entries:
                    if not entry.is_file(follow_symlinks=False):
                        continue

                    name = entry.name
                    name_lower = name.lower()

                    # December 30, 2025: Only check SavedVariables file types
                    # .lua = settings data, .bak = backup of settings
                    if not (name_lower.endswith(".lua") or name_lower.endswith(".bak")):
                        continue

                    # Extract AddOn name by removing extension
                    if name_lower.endswith(".lua"):
                        base_name = name[:-4]
                    else:  # .bak
                        base_name = name[:-4]

                    # December 30, 2025: CRITICAL PROTECTION
                    # Blizzard_ .lua files are core game files, not AddOn settings
                    # Removing them would break the game UI
                    # However, Blizzard_ .bak files are safe to remove
                    if name_lower.endswith(".lua") and name.startswith("Blizzard_"):
                        continue

                    # December 30, 2025: Check if this AddOn is still installed
                    # If not found in Interface\AddOns, it's an orphan
                    if base_name.lower() not in installed_addons:
                        orphans.append(entry.path)

        except (OSError, PermissionError):
            pass

        return orphans
