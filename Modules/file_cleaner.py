"""
Backend logic for the File Cleaner tab.

This module is deliberately UI-agnostic: it does filesystem work and logging only.
The Tkinter tree, buttons, dialogs, etc., stay in wow_cleanup_tool.py.

Functions:
    find_bak_old_files: Scan versions for .bak and .old files
    delete_files: Delete or move files to trash
"""
import os
import os.path

# Try to import send2trash for safe deletion to recycle bin/trash
# If unavailable, files will be permanently deleted instead
try:
    from send2trash import send2trash
    HAS_TRASH = True
except ImportError:
    HAS_TRASH = False

def find_bak_old_files(versions, logger=None):
    """
    Scan WoW versions for .bak / .old files.
    
    Recursively walks through each version directory looking for files
    ending in .bak or .old. These are typically backup files created
    by WoW, text editors, or other tools that can safely be removed.
    
    Parameters:
        versions: Iterable of (version_path, version_label) tuples.
                  Each tuple represents a WoW installation (Retail, Classic, etc.)
        logger: Optional object with .debug() and .info() methods for logging
    
    Returns:
        dict: Mapping of version_label -> list of absolute file paths
              Only includes versions that have files to clean
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
    
    For each file in the paths list, either:
    - Move it to the system Recycle Bin/Trash (if use_trash=True and send2trash available)
    - Permanently delete it (if use_trash=False or send2trash not available)
    
    If a file fails to delete, the operation continues with remaining files.
    
    Parameters:
        paths: Iterable of absolute file paths to delete
        use_trash: Boolean - if True, attempt to move to trash instead of permanent deletion
        logger: Optional object with .info() and .error() methods for logging
    
    Returns:
        Tuple of (processed_count, permanently_deleted_flag, used_trash_flag):
        - processed_count: Number of files successfully deleted/moved
        - permanently_deleted_flag: True if files were permanently deleted (not in trash)
        - used_trash_flag: True if files were moved to trash (even if only some)
    """
    processed = 0
    used_trash = False
    real_use_trash = use_trash and HAS_TRASH
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
        except (OSError, IOError) as e:
            if logger:
                logger.error(f"[FileCleaner] ERROR deleting {fp}: {e}")
    permanently_deleted = not real_use_trash
    return processed, permanently_deleted, used_trash

