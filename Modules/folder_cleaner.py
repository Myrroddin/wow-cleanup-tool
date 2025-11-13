"""
Backend logic for Folder Cleaner.

This module performs:
- Scanning for folders that can be cleaned safely (Cache, Logs, etc.)
- Deleting folder contents, either permanently or to Trash
- Returning structured results to the UI layer

The UI (Tkinter) remains in wow_cleanup_tool.py.
"""

import os
import shutil

try:
    from send2trash import send2trash
    HAS_TRASH = True
except Exception:
    HAS_TRASH = False


# ------------------------------------------------------------
# SCANNING LOGIC
# ------------------------------------------------------------

DEFAULT_CLEANABLE_FOLDERS = [
    "Cache",
    "Logs",
    "Errors",
    "Crash",
    "AddOns.txt.bak",   # if someone stores it incorrectly
]


def scan_cleanable_folders(version_path, logger=None):
    """
    Scan a single WoW version for folders that can be cleaned.

    Parameters:
        version_path: absolute path to a WoW version root
        logger: optional object with .debug()

    Returns:
        list of (label, absolute_path)
    """
    found = []

    for rel in DEFAULT_CLEANABLE_FOLDERS:
        abs_path = os.path.join(version_path, rel)
        if os.path.exists(abs_path):
            found.append((rel, abs_path))
            if logger:
                logger.debug(f"[FolderCleaner] Found: {abs_path}")

    return found


def scan_all_versions(versions, logger=None):
    """
    Scan all versions for cleanable folders.

    Parameters:
        versions: iterable of (version_path, version_label)
        logger: optional

    Returns:
        dict mapping version_label -> list of (label, abs_path)
    """
    results = {}
    total = 0

    for vpath, vlabel in versions:
        lst = scan_cleanable_folders(vpath, logger=logger)
        if lst:
            results[vlabel] = lst
            total += len(lst)

    if logger:
        logger.info(f"[FolderCleaner] Total cleanable folders: {total}")

    return results


# ------------------------------------------------------------
# CLEANUP LOGIC
# ------------------------------------------------------------

def clean_folders(paths, use_trash=False, logger=None):
    """
    Delete contents of selected folders, or move entire folders to trash.

    Parameters:
        paths: iterable of folder paths
        use_trash: whether to trash instead of delete
        logger: optional

    Returns:
        (processed_count, permanently_deleted_flag, used_trash_flag)
    """
    processed = 0
    used_trash = False
    real_use_trash = bool(use_trash and HAS_TRASH)

    for folder in paths:
        try:
            if real_use_trash:
                send2trash(folder)
                used_trash = True
                if logger:
                    logger.info(f"[FolderCleaner] Moved to trash: {folder}")
            else:
                # Remove entire directory tree
                shutil.rmtree(folder, ignore_errors=False)
                if logger:
                    logger.info(f"[FolderCleaner] Deleted: {folder}")

            processed += 1

        except Exception as e:
            if logger:
                logger.error(f"[FolderCleaner] ERROR removing {folder}: {e}")

    permanently_deleted = not real_use_trash
    return processed, permanently_deleted, used_trash
