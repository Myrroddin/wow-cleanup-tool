"""File operations for deleting or trashing files/folders in WoW Cleanup Tool.

This module provides the centralized file deletion functionality for the application,
replacing direct os.remove() calls with safer alternatives:

- delete_files_batch(): Handles both trash and permanent deletion modes
  - Respects user preferences (send2trash vs os.remove/shutil.rmtree)
  - Provides consistent logging and error handling
  - Returns detailed operation results for UI feedback

- clean_addons_txt_for_orphans(): Automatically removes orphaned addon entries
  - Cleans AddOns.txt files when SavedVariables are deleted
  - Traverses account/realm/character directory structures
  - Preserves file formatting and handles edge cases

Note: All file deletion in the application should use delete_files_batch() instead
of direct os.remove() or shutil.rmtree() calls to ensure send2trash integration
and user preference support.
"""

from typing import List, Tuple, Dict, Set
import os
from send2trash import send2trash


def clean_addons_txt_for_orphans(
    orphan_paths: List[str], version_path: str, logger=None, loc=None
) -> Dict[str, int]:
    """Clean AddOns.txt files after removing orphaned addon .lua files.

    When orphaned addon .lua files are removed (excluding Blizzard_ and .bak files),
    this function removes the corresponding addon entries from all AddOns.txt files
    in the WTF directory structure.

    Args:
        orphan_paths: List of orphaned file paths that were removed
        version_path: Path to WoW version (e.g., C:\\WoW\\_retail_)
        logger: Logger instance for verbose output
        loc: Localization instance

    Returns:
        Dict mapping AddOns.txt file paths to number of lines removed
    """
    # Extract addon names from orphaned .lua files (excluding Blizzard_ and .bak)
    addon_names: Set[str] = set()
    for path in orphan_paths:
        # Only process .lua files (not .bak)
        if not path.lower().endswith(".lua"):
            continue

        # Skip Blizzard_ files
        filename = os.path.basename(path)
        if filename.startswith("Blizzard_"):
            continue

        # Extract addon name (remove .lua extension)
        addon_name = filename[:-4]
        addon_names.add(addon_name)

    if not addon_names:
        return {}

    # Find and clean all AddOns.txt files in WTF directory
    wtf_path = os.path.join(version_path, "WTF")
    if not os.path.isdir(wtf_path):
        return {}

    cleaned_files: Dict[str, int] = {}
    account_path = os.path.join(wtf_path, "Account")
    if not os.path.isdir(account_path):
        return cleaned_files

    # Walk through WTF\Account\<account>\<realm>\<character>\AddOns.txt
    try:
        for account_name in os.listdir(account_path):
            account_dir = os.path.join(account_path, account_name)
            if not os.path.isdir(account_dir):
                continue

            # Check each realm directory
            for realm_name in os.listdir(account_dir):
                realm_dir = os.path.join(account_dir, realm_name)
                if not os.path.isdir(realm_dir):
                    continue

                # Skip SavedVariables directory
                if realm_name == "SavedVariables":
                    continue

                # Check each character directory
                for char_name in os.listdir(realm_dir):
                    char_dir = os.path.join(realm_dir, char_name)
                    if not os.path.isdir(char_dir):
                        continue

                    addons_txt = os.path.join(char_dir, "AddOns.txt")
                    if not os.path.isfile(addons_txt):
                        continue

                    # Read and clean the AddOns.txt file
                    removed_count = _clean_single_addons_txt(
                        addons_txt, addon_names, logger
                    )
                    if removed_count > 0:
                        cleaned_files[addons_txt] = removed_count

    except (OSError, PermissionError) as e:
        if logger:
            logger.error(f"Error scanning WTF directory: {e}")

    return cleaned_files


def _clean_single_addons_txt(
    addons_txt_path: str, addon_names: Set[str], logger=None
) -> int:
    """Clean a single AddOns.txt file by removing orphaned addon entries.

    Args:
        addons_txt_path: Path to AddOns.txt file
        addon_names: Set of addon names to remove
        logger: Logger instance for verbose output

    Returns:
        Number of lines removed from the file
    """
    try:
        # Read all lines from the file
        with open(addons_txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Filter out orphaned addon entries
        original_count = len(lines)
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            # Keep line if it's not an orphaned addon name
            if stripped not in addon_names:
                cleaned_lines.append(line)

        removed_count = original_count - len(cleaned_lines)

        # Only write back if we actually removed something
        if removed_count > 0:
            with open(addons_txt_path, "w", encoding="utf-8") as f:
                f.writelines(cleaned_lines)

        return removed_count

    except (OSError, IOError, UnicodeDecodeError) as e:
        if logger:
            logger.error(f"Failed to clean {addons_txt_path}: {e}")
        return 0


def delete_files_batch(
    paths: List[str], delete_mode: str = "trash", logger=None, loc=None
) -> Tuple[int, bool, bool, List[str]]:
    """Delete or trash files/folders.
    Args:
        paths: List of file/folder paths to delete
        delete_mode: 'trash' or 'permanent'
        logger: Logger instance for verbose output
        loc: Localization instance
    Returns:
        (processed_count, permanently_deleted, used_trash, processed_paths)
    """
    # Defensive: ensure paths is actually a list
    if isinstance(paths, str):
        if logger:
            logger.error(
                f"Bug: delete_files_batch received string instead of list: {paths}"
            )
        return 0, False, False, []

    processed = 0
    used_trash = False
    processed_paths: List[str] = []
    for path in paths:
        try:
            if delete_mode == "trash":
                send2trash(path)
                used_trash = True
            else:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    import shutil

                    shutil.rmtree(path)
            processed += 1
            processed_paths.append(path)
        except (OSError, IOError) as e:
            if logger:
                logger.error(f"Failed to delete {path}: {e}")
            continue
    return processed, not used_trash, used_trash, processed_paths
