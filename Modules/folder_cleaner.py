"""
Backend logic for Folder Cleaner.

This module performs:
- Scanning for folders that can be cleaned safely (Logs, Errors, Screenshots, etc.)
- Deleting folder contents, either permanently or to Trash
- Returning structured results to the UI layer

The UI (Tkinter) remains in wow_cleanup_tool.py. This module only handles
filesystem operations and optional logging.

Functions:
    scan_cleanable_folders: Scan a single version for cleanable folders
    scan_all_versions: Scan all WoW versions for cleanable folders
    clean_folders: Delete or trash entire folders
"""
import os
import shutil

# Try to import send2trash for safe deletion to recycle bin/trash
# If unavailable, folders will be permanently deleted instead
try:
    from send2trash import send2trash
    HAS_TRASH = True
except ImportError:
    HAS_TRASH = False

DEFAULT_CLEANABLE_FOLDERS = [
    "Logs",                 # Debug and error logs
    "Errors",               # Error report files
    "AddOns.txt.bak",       # Backup of AddOns.txt (if stored incorrectly)
]

def scan_cleanable_folders(version_path, logger=None):
    """
    Scan a single WoW version for folders that can be cleaned.
    
    Checks for the existence of known safe-to-delete folders within
    a WoW version directory.
    
    Parameters:
        version_path: Absolute path to a WoW version root (e.g., _retail_, _classic_)
        logger: Optional object with .debug() method for logging
    
    Returns:
        list: List of (folder_name, absolute_path) tuples for existing cleanable folders
    """
    found = [
        (rel, os.path.join(version_path, rel))
        for rel in DEFAULT_CLEANABLE_FOLDERS
        if os.path.exists(os.path.join(version_path, rel))
    ]
    if logger:
        for rel, abs_path in found:
            logger.debug(f"[FolderCleaner] Found: {abs_path}")

    return found


def scan_all_versions(versions, logger=None):
    """
    Scan all WoW versions for cleanable folders.
    
    Iterates through all provided WoW versions and finds cleanable folders
    in each one.
    
    Parameters:
        versions: Iterable of (version_path, version_label) tuples
                  Each tuple represents a WoW installation
        logger: Optional object with .info() and .debug() methods
    
    Returns:
        dict: Mapping of version_label -> list of (folder_name, abs_path) tuples
              Only includes versions that have cleanable folders
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


def clean_folders(paths, use_trash=False, logger=None):
    """
    Delete or move folders to trash.
    
    For each folder in the paths list, either:
    - Move the entire folder to the system Recycle Bin/Trash (if use_trash=True and available)
    - Permanently delete the entire folder (if use_trash=False or send2trash not available)
    
    If a folder fails to delete, the operation continues with remaining folders.
    
    Parameters:
        paths: Iterable of absolute folder paths to delete
        use_trash: Boolean - if True, attempt to move to trash instead of permanent deletion
        logger: Optional object with .info() and .error() methods for logging
    
    Returns:
        Tuple of (processed_count, permanently_deleted_flag, used_trash_flag):
        - processed_count: Number of folders successfully deleted/moved
        - permanently_deleted_flag: True if folders were permanently deleted
        - used_trash_flag: True if any folders were moved to trash
    """
    processed = 0
    used_trash = False
    real_use_trash = use_trash and HAS_TRASH
    for folder in paths:
        try:
            if real_use_trash:
                send2trash(folder)
                used_trash = True
                if logger:
                    logger.info(f"[FolderCleaner] Moved to trash: {folder}")
            else:
                shutil.rmtree(folder, ignore_errors=False)
                if logger:
                    logger.info(f"[FolderCleaner] Deleted: {folder}")
            processed += 1
        except (OSError, IOError) as e:
            if logger:
                logger.error(f"[FolderCleaner] ERROR removing {folder}: {e}")
    permanently_deleted = not real_use_trash
    return processed, permanently_deleted, used_trash
