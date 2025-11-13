"""
Backend logic for Orphan Cleaner.

This module performs:
- Scanning for orphaned SavedVariables (.lua files in wrong locations)
- Detecting installed addons
- Rebuilding AddOns.txt files to match installed addons
- Deleting/moving orphan SavedVariables files

It contains zero Tkinter/UI logic.
Your main wow_cleanup_tool.py should use this module to populate the UI.

Context: World of Warcraft stores addon preferences (SavedVariables) in .lua files
that exist at Account, Realm, and Character levels. When addons are uninstalled,
their .lua files remain, creating clutter. This module finds and removes them.

Functions:
    savedvar_basename: Normalize SavedVariables filenames
    collect_addon_names: Get set of installed addon names
    iter_savedvariables_dirs: Yield all SavedVariables directories
    scan_orphans: Find orphaned SavedVariables files
    delete_orphans: Delete or move orphaned files
    rebuild_addons_txt: Rebuild AddOns.txt files to match installed addons
"""
import os

# Try to import send2trash for safe deletion to recycle bin/trash
# If unavailable, files will be permanently deleted instead
try:
    from send2trash import send2trash
    HAS_TRASH = True
except ImportError:
    HAS_TRASH = False

def savedvar_basename(filename):
    """
    Normalize SavedVariables filenames to plain addon names.
    
    SavedVariables files can have different extensions (.lua, .lua.bak, .bak),
    but they all represent an addon's saved settings. This function removes
    the extensions to get the canonical addon name.
    
    Examples:
        Foo.lua       -> Foo
        Foo.lua.bak   -> Foo
        Foo.bak       -> Foo
        Foo           -> Foo (unchanged)
    
    Args:
        filename: The SavedVariables filename
    
    Returns:
        str: The addon name without extensions
    """
    lf = filename.lower()
    if lf.endswith(".lua.bak"):
        return filename[:-8]
    if lf.endswith(".lua"):
        return filename[:-4]
    if lf.endswith(".bak"):
        return filename[:-4]
    return filename


def collect_addon_names(addons_dir):
    """
    Return a set of installed addon names (casefolded), excluding Blizzard_*.
    
    Scans the Interface/AddOns directory to find all installed addons.
    Blizzard_* folders are core game data and are excluded.
    Addon names are casefolded (lowercased) for comparison purposes.
    
    Args:
        addons_dir: Path to Interface/AddOns directory
    
    Returns:
        set: Set of installed addon names (lowercased), or empty set if directory doesn't exist
    """
    if not os.path.isdir(addons_dir):
        return set()

    return {
        entry.casefold()
        for entry in os.listdir(addons_dir)
        if os.path.isdir(os.path.join(addons_dir, entry))
        and not entry.lower().startswith("blizzard_")
    }


def iter_savedvariables_dirs(account_root):
    """
    Yield every SavedVariables directory within an account.
    
    SavedVariables can exist at multiple levels:
    - Account level: WTF/Account/SavedVariables
    - Realm level: WTF/Account/REALM/SavedVariables
    - Character level: WTF/Account/REALM/CHARACTER/SavedVariables
    
    This function yields all of them so we can scan for orphans at all levels.
    
    Args:
        account_root: Path to WTF/Account directory
    
    Yields:
        str: Absolute paths to SavedVariables directories
    """
    if not os.path.isdir(account_root):
        return

    # Account root-level SavedVariables
    root_sv = os.path.join(account_root, "SavedVariables")
    if os.path.isdir(root_sv):
        yield root_sv

    # Realms and characters nested under account
    for realm_name in os.listdir(account_root):
        realm_path = os.path.join(account_root, realm_name)
        # Skip if not a directory or if it's a SavedVariables folder (not a realm)
        if not os.path.isdir(realm_path) or realm_name.upper() == "SAVEDVARIABLES":
            continue

        # Realm-level SavedVariables
        realm_sv = os.path.join(realm_path, "SavedVariables")
        if os.path.isdir(realm_sv):
            yield realm_sv

        # Character-level SavedVariables (one per character on this realm)
        for char_name in os.listdir(realm_path):
            char_path = os.path.join(realm_path, char_name)
            # Skip if not a directory or if it's a SavedVariables folder (not a character)
            if not os.path.isdir(char_path) or char_name.upper() == "SAVEDVARIABLES":
                continue

            char_sv = os.path.join(char_path, "SavedVariables")
            if os.path.isdir(char_sv):
                yield char_sv

def scan_orphans(versions, logger=None):
    """
    Scan for orphaned SavedVariables across many WoW versions.
    
    For each version, this function:
    1. Gets the list of installed addons from Interface/AddOns
    2. Scans all SavedVariables directories at Account/Realm/Character levels
    3. Identifies any SavedVariables files for addons that are no longer installed
    4. Collects these orphaned files for potential deletion
    
    Blizzard_* core game files are automatically ignored for safety.
    
    Parameters:
        versions: Iterable of (version_path, version_label) tuples
                  Each represents a WoW installation (Retail, Classic, etc.)
        logger: Optional object with .debug() and .info() methods for logging
    
    Returns:
        dict: Mapping of version_label -> list of absolute paths to orphaned SavedVariables files
              Only includes versions that have orphaned files
    """
    results = {}
    total = 0

    for vpath, vlabel in versions:
        # Get list of currently installed addons
        addons_dir = os.path.join(vpath, "Interface", "AddOns")
        installed = collect_addon_names(addons_dir)

        # Find the WTF account directory for this version
        account_root = os.path.join(vpath, "WTF", "Account")
        if not os.path.isdir(account_root):
            # This version doesn't have an account setup yet
            continue

        version_orphans = []

        # Scan every SavedVariables directory at all levels
        for sv_dir in iter_savedvariables_dirs(account_root):
            try:
                for fname in os.listdir(sv_dir):
                    lf = fname.lower()

                    # Ignore Blizzard_*.lua core files (but keep Blizzard backups)
                    # These are game-critical and should never be deleted
                    if (
                        lf.startswith("blizzard_")
                        and lf.endswith(".lua")
                        and not lf.endswith(".lua.bak")
                    ):
                        continue

                    # Only process .lua and .lua.bak files (SavedVariables format)
                    if not (lf.endswith(".lua") or lf.endswith(".lua.bak")):
                        continue

                    # Normalize filename to addon name for comparison
                    base = savedvar_basename(fname).casefold()
                    # If this addon is not installed, it's orphaned
                    if base not in installed:
                        fpath = os.path.join(sv_dir, fname)
                        version_orphans.append(fpath)
                        total += 1
                        if logger:
                            logger.debug(
                                f"[OrphanCleaner] Found orphan in {vlabel}: {fpath}"
                            )

            except (OSError, IOError):
                # If we can't read a SavedVariables directory, just skip it
                # and continue scanning others
                pass

        if version_orphans:
            results[vlabel] = version_orphans

    if logger:
        logger.info(f"[OrphanCleaner] Total orphaned SavedVariables: {total}")

    return results



def delete_orphans(paths, use_trash=False, logger=None):
    """
    Delete or move orphaned SavedVariables to trash.
    
    For each orphaned SavedVariables file, either:
    - Move it to the system Recycle Bin/Trash (if use_trash=True and available)
    - Permanently delete it (if use_trash=False or send2trash not available)
    
    If a file fails to delete, the operation continues with remaining files.
    
    Parameters:
        paths: Iterable of absolute paths to orphaned SavedVariables files
        use_trash: Boolean - if True, attempt to move to trash
        logger: Optional object with .info() and .error() methods
    
    Returns:
        Tuple of (processed_count, permanently_deleted_flag, used_trash_flag):
        - processed_count: Number of files successfully deleted/moved
        - permanently_deleted_flag: True if files were permanently deleted
        - used_trash_flag: True if files were moved to trash
    """
    processed = 0
    used_trash = False
    real_use_trash = use_trash and HAS_TRASH

    for fp in paths:
        try:
            if real_use_trash:
                # Move to system trash/recycle bin
                send2trash(fp)
                used_trash = True
                if logger:
                    logger.info(f"[OrphanCleaner] Moved to trash: {fp}")
            else:
                # Permanently delete file
                os.remove(fp)
                if logger:
                    logger.info(f"[OrphanCleaner] Deleted: {fp}")
            processed += 1

        except (OSError, IOError) as e:
            # Log error but continue with next file
            if logger:
                logger.error(f"[OrphanCleaner] ERROR deleting {fp}: {e}")

    permanently_deleted = not real_use_trash
    return processed, permanently_deleted, used_trash


# ============================================================
# ADDONS.TXT REBUILD LOGIC
# ============================================================
# Functions for rebuilding AddOns.txt files to match installed addons


def rebuild_addons_txt(version_root, installed_addons, logger=None):
    """
    Rebuild every AddOns.txt file under WTF/Account/... for the given version.
    
    AddOns.txt files store which addons are enabled/disabled for each character.
    When addons are deleted, their entries remain in these files. This function
    rebuilds them to only include currently installed addons, while preserving
    the enabled/disabled state where possible.
    
    WoW looks for these files at: WTF/Account/REALM/CHARACTER/AddOns.txt
    
    The function:
    1. Finds all AddOns.txt files for all characters
    2. Loads the previous enabled/disabled state
    3. Recreates the file with only installed addons
    4. Preserves Blizzard_* entries for core game addons
    
    Parameters:
        version_root: Path to the WoW version (e.g., _retail_)
        installed_addons: Set of currently installed addon names (casefolded)
        logger: Optional object with .info() and .error() methods
    
    Returns:
        Tuple of (rebuilt_map, removed_map):
        - rebuilt_map: Dict mapping AddOns.txt path -> list of lines written
        - removed_map: Dict mapping AddOns.txt path -> list of addon names removed
    """
    rebuilt_map = {}
    removed_map = {}

    account_root = os.path.join(version_root, "WTF", "Account")
    if not os.path.isdir(account_root):
        # No account setup for this version
        return rebuilt_map, removed_map

    addons_dir = os.path.join(version_root, "Interface", "AddOns")

    # Get list of currently installed addon folder names
    try:
        dir_listing = [
            d
            for d in os.listdir(addons_dir)
            if os.path.isdir(os.path.join(addons_dir, d))
        ]
    except (OSError, IOError):
        dir_listing = []

    # Map casefolded addon names to real folder names for display
    # (preserves the original case from folder names)
    dir_by_cf = {d.casefold(): d for d in dir_listing if not d.lower().startswith("blizzard_")}

    def parse_line(line):
        """Parse an AddOns.txt line into (name, state)."""
        parts = line.split(":", 1)
        if len(parts) != 2:
            return line.strip(), "enabled"
        name = parts[0].strip()
        state = parts[1].strip().lower()
        return name, ("enabled" if state in ("enabled", "disabled") else "enabled")

    try:
        for account in os.listdir(account_root):
            account_path = os.path.join(account_root, account)
            if not os.path.isdir(account_path):
                continue

            for realm in os.listdir(account_path):
                realm_path = os.path.join(account_path, realm)
                if not os.path.isdir(realm_path) or realm.upper() == "SAVEDVARIABLES":
                    continue

                for char in os.listdir(realm_path):
                    char_path = os.path.join(realm_path, char)
                    if (
                        not os.path.isdir(char_path)
                        or char.upper() == "SAVEDVARIABLES"
                    ):
                        continue

                    addons_txt = os.path.join(char_path, "AddOns.txt")

                    prev_states = {}
                    prev_blizzard = {}

                    # Load existing AddOns.txt
                    if os.path.isfile(addons_txt):
                        try:
                            with open(
                                addons_txt, "r", encoding="utf-8", errors="ignore"
                            ) as f:
                                for raw in f.read().splitlines():
                                    if not raw.strip():
                                        continue
                                    name, state = parse_line(raw)
                                    cf = name.casefold()
                                    if name.lower().startswith("blizzard_"):
                                        prev_blizzard[cf] = (name, state)
                                    else:
                                        prev_states[cf] = (name, state)

                        except (OSError, IOError):
                            prev_states = {}
                            prev_blizzard = {}

                    # Build new entries
                    entries = {}

                    # Installed addons
                    for addon_cf in installed_addons:
                        display_name = dir_by_cf.get(addon_cf, addon_cf)
                        state = prev_states.get(addon_cf, (display_name, "enabled"))[1]
                        entries[addon_cf] = (display_name, state)

                    # Blizzard addons preserved
                    entries.update(prev_blizzard)

                    # Removed addons
                    removed = [
                        cf for cf in prev_states.keys() if cf not in installed_addons
                    ]

                    # Alphabetize for output
                    sorted_items = sorted(
                        entries.items(), key=lambda kv: kv[1][0].casefold()
                    )

                    written = [
                        f"{disp}: {state}" for _, (disp, state) in sorted_items
                    ]

                    # Write file
                    try:
                        with open(addons_txt, "w", encoding="utf-8") as f:
                            f.write("\n".join(written))

                        rebuilt_map[addons_txt] = written
                        removed_map[addons_txt] = removed

                        if logger:
                            logger.info(f"[OrphanCleaner] Rebuilt: {addons_txt}")

                    except (OSError, IOError) as e:
                        if logger:
                            logger.error(
                                f"[OrphanCleaner] ERROR writing AddOns.txt {addons_txt}: {e}"
                            )

    except (OSError, IOError) as e:
        if logger:
            logger.error(f"[OrphanCleaner] ERROR during AddOns.txt rebuild: {e}")

    return rebuilt_map, removed_map
