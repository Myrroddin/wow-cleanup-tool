"""
Backend logic for the File Cleaner tab.

This module is deliberately UI-agnostic: it does filesystem work
and logging only. The Tkinter tree, buttons, dialogs, etc., stay
in wow_cleanup_tool.py.
"""

import os
import os.path
import itertools

try:
    from send2trash import send2trash
    HAS_TRASH = True
except Exception:  # pragma: no cover
    HAS_TRASH = False


def find_bak_old_files(versions, logger=None):
    """
    Scan WoW versions for .bak / .old files.

    Parameters:
        versions: iterable of (version_path, version_label)
        logger: object with .debug(...) and/or .info(...), optional

    Returns:
        dict mapping version_label -> list of absolute file paths
    """
    results = {}
    total = 0

    for vpath, vlabel in versions:
        vlabel_files = []
        for rootd, _dirs, files in os.walk(vpath):
            for fname in files:
                if fname.lower().endswith((".bak", ".old")):
                    fpath = os.path.join(rootd, fname)
                    vlabel_files.append(fpath)
                    total += 1
                    if logger:
                        logger.debug(f"[FileCleaner] Found file in {vlabel}: {fpath}")
        if vlabel_files:
            results[vlabel] = vlabel_files

    if logger:
        logger.info(f"[FileCleaner] Total .bak/.old files found: {total}")

    return results


def delete_files(paths, use_trash=False, logger=None):
    """
    Delete or move files to trash.

    Parameters:
        paths: iterable of absolute file paths
        use_trash: bool, if True and send2trash is available, move to trash
        logger: object with .info(...) / .error(...), optional

    Returns:
        (processed_count, permanently_deleted_flag, used_trash_flag)
    """
    processed = 0
    used_trash = False

    # If caller wants trash but module doesn't have it, we still delete,
    # but we report that it ended up permanent.
    real_use_trash = bool(use_trash and HAS_TRASH)

    for fp in paths:
        try:
            if real_use_trash:
                send2trash(fp)
                used_trash = True
                if logger:
                    logger.info(f"[FileCleaner] Moved to trash: {fp}")
            else:
                os.remove(fp)
                if logger:
                    logger.info(f"[FileCleaner] Deleted: {fp}")
            processed += 1
        except Exception as e:  # pragma: no cover
            if logger:
                logger.error(f"[FileCleaner] ERROR deleting {fp}: {e}")

    permanently_deleted = not real_use_trash
    return processed, permanently_deleted, used_trash
