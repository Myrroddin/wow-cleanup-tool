"""
Backend logic for Orphan Cleaner.

This module performs:
- Scanning for orphaned SavedVariables
- Detecting installed addons
- Rebuilding AddOns.txt files properly
- Deleting/moving orphan files

It contains zero Tkinter/UI logic.
Your main wow_cleanup_tool.py should use this module to populate the UI.
"""

import os
import shutil

try:
    from send2trash import send2trash
    HAS_TRASH = True
except Exception:
    HAS_TRASH = False


# ------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------

def savedvar_basename(filename):
    """
    Normalize SavedVariables filenames to plain addon names.

    Examples:
        Foo.lua       -> Foo
        Foo.lua.bak   -> Foo
        Foo.bak       -> Foo
    """
    fn = filename
    lf = fn.lower()
    if lf.endswith(".lua.bak"):
        return fn[:-8]
    if lf.endswith(".lua"):
        return fn[:-4]
    if lf.endswith(".bak"):
        return fn[:-4]
    return fn


def collect_addon_names(addons_dir):
    """
    Return a set of installed addon names (casefolded), excluding Blizzard_*.
    """
    names = set()
    if not os.path.isdir(addons_dir):
        return names

    for entry in os.listdir(addons_dir):
        p = os.path.join(addons_dir, entry)
        if os.path.isdir(p) and not entry.lower().startswith("blizzard_"):
            names.add(entry.casefold())

    return names


def iter_savedvariables_dirs(account_root):
    """
    Yield every SavedVariables folder within:
    - Account
    - Realm
    - Character
    """
    if not os.path.isdir(account_root):
        return

    # Account root-level SavedVariables
    root_sv = os.path.join(account_root, "SavedVariables")
    if os.path.isdir(root_sv):
        yield root_sv

    # Realms and characters
    for realm_name in os.listdir(account_root):
        realm_path = os.path.join(account_root, realm_name)
        if not os.path.isdir(realm_path) or realm_name.upper() == "SAVEDVARIABLES":
            continue

        # Realm SV
        realm_sv = os.path.join(realm_path, "SavedVariables")
        if os.path.isdir(realm_sv):
            yield realm_sv

        # Characters
        for char_name in os.listdir(realm_path):
            char_path = os.path.join(realm_path, char_name)
            if not os.path.isdir(char_path) or char_name.upper() == "SAVEDVARIABLES":
                continue

            char_sv = os.path.join(char_path, "SavedVariables")
            if os.path.isdir(char_sv):
                yield char_sv


# ------------------------------------------------------------
# Scanning logic
# ------------------------------------------------------------

def scan_orphans(versions, logger=None):
    """
    Scan for orphaned SavedVariables across many versions.

    Parameters:
        versions: iterable of (version_path, version_label)
        logger: optional logger with .debug() / .info()

    Returns:
        dict mapping version_label -> list of orphan absolute paths
    """
    results = {}
    total = 0

    for vpath, vlabel in versions:
        addons_dir = os.path.join(vpath, "Interface", "AddOns")
        installed = collect_addon_names(addons_dir)

        account_root = os.path.join(vpath, "WTF", "Account")
        if not os.path.isdir(account_root):
            continue

        version_orphans = []

        for sv_dir in iter_savedvariables_dirs(account_root):
            try:
                for fname in os.listdir(sv_dir):
                    lf = fname.lower()

                    # Ignore Blizzard_*.lua (but keep Blizzard backups)
                    if lf.startswith("blizzard_") and lf.endswith(".lua") and not lf.endswith(".lua.bak"):
                        continue

                    if not (lf.endswith(".lua") or lf.endswith(".lua.bak")):
                        continue

                    base = savedvar_basename(fname).casefold()
                    if base not in installed:
                        fpath = os.path.join(sv_dir, fname)
                        version_orphans.append(fpath)
                        total += 1
                        if logger:
                            logger.debug(f"[OrphanCleaner] Found orphan in {vlabel}: {fpath}")

            except Exception:
                # Silent fallback; continue scanning other dirs
                pass

        if version_orphans:
            results[vlabel] = version_orphans

    if logger:
        logger.info(f"[OrphanCleaner] Total orphaned SavedVariables: {total}")

    return results


# ------------------------------------------------------------
# Deletion logic
# ------------------------------------------------------------

def delete_orphans(paths, use_trash=False, logger=None):
    """
    Delete or move orphaned SavedVariables to trash.

    Returns:
        processed_count, permanently_deleted_flag, used_trash_flag
    """
    processed = 0
    used_trash = False
    real_use_trash = bool(use_trash and HAS_TRASH)

    for fp in paths:
        try:
            if real_use_trash:
                send2trash(fp)
                used_trash = True
                if logger:
                    logger.info(f"[OrphanCleaner] Moved to trash: {fp}")
            else:
                os.remove(fp)
                if logger:
                    logger.info(f"[OrphanCleaner] Deleted: {fp}")
            processed += 1

        except Exception as e:
            if logger:
                logger.error(f"[OrphanCleaner] ERROR deleting {fp}: {e}")

    permanently_deleted = not real_use_trash
    return processed, permanently_deleted, used_trash


# ------------------------------------------------------------
# AddOns.txt rebuild logic
# ------------------------------------------------------------

def rebuild_addons_txt(version_root, installed_addons, logger=None):
    """
    Rebuild every AddOns.txt file under WTF/Account/... for the given version.

    Returns:
        rebuilt_map: {addons_txt_path: written_lines}
        removed_map: {addons_txt_path: removed_addons}
    """
    rebuilt_map = {}
    removed_map = {}

    account_root = os.path.join(version_root, "WTF", "Account")
    if not os.path.isdir(account_root):
        return rebuilt_map, removed_map

    addons_dir = os.path.join(version_root, "Interface", "AddOns")

    try:
        dir_listing = [
            d for d in os.listdir(addons_dir)
            if os.path.isdir(os.path.join(addons_dir, d))
        ]
    except Exception:
        dir_listing = []

    # Map casefolded names to real folder names
    dir_by_cf = {
        d.casefold(): d
        for d in dir_listing
        if not d.lower().startswith("blizzard_")
    }

    def parse_line(line):
        parts = line.split(":", 1)
        if len(parts) != 2:
            return line.strip(), "enabled"
        name = parts[0].strip()
        state = parts[1].strip().lower()
        if state not in ("enabled", "disabled"):
            state = "enabled"
        return name, state

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
                    if not os.path.isdir(char_path) or char.upper() == "SAVEDVARIABLES":
                        continue

                    addons_txt = os.path.join(char_path, "AddOns.txt")

                    prev_states = {}
                    prev_blizzard = {}

                    # Load existing AddOns.txt
                    if os.path.isfile(addons_txt):
                        try:
                            with open(addons_txt, "r", encoding="utf-8", errors="ignore") as f:
                                for raw in f.read().splitlines():
                                    if not raw.strip():
                                        continue
                                    name, state = parse_line(raw)
                                    cf = name.casefold()
                                    if name.lower().startswith("blizzard_"):
                                        prev_blizzard[cf] = (name, state)
                                    else:
                                        prev_states[cf] = (name, state)

                        except Exception:
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
                    for blizz_cf, (blizz_name, blizz_state) in prev_blizzard.items():
                        entries[blizz_cf] = (blizz_name, blizz_state)

                    # Removed addons
                    removed = [
                        cf for cf in prev_states.keys()
                        if cf not in installed_addons
                    ]

                    # Alphabetize for output
                    sorted_items = sorted(
                        entries.items(),
                        key=lambda kv: kv[1][0].casefold()
                    )

                    written = [
                        f"{disp}: {state}"
                        for _, (disp, state) in sorted_items
                    ]

                    # Write file
                    try:
                        with open(addons_txt, "w", encoding="utf-8") as f:
                            f.write("\n".join(written))

                        rebuilt_map[addons_txt] = written
                        removed_map[addons_txt] = removed

                        if logger:
                            logger.info(f"[OrphanCleaner] Rebuilt: {addons_txt}")

                    except Exception as e:
                        if logger:
                            logger.error(f"[OrphanCleaner] ERROR writing AddOns.txt {addons_txt}: {e}")

    except Exception as e:
        if logger:
            logger.error(f"[OrphanCleaner] ERROR during AddOns.txt rebuild: {e}")

    return rebuilt_map, removed_map
