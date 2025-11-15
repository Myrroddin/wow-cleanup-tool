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
from Modules.performance import delete_files_batch, HAS_TRASH

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
    """Delete or move folders using shared utility.
    
    Parameters:
        paths: Iterable of absolute folder paths to delete
        use_trash: Boolean - if True, attempt to move to trash
        logger: Optional object with .info() and .error() methods
    
    Returns:
        Tuple of (processed_count, permanently_deleted_flag, used_trash_flag)
    """
    return delete_files_batch(paths, use_trash, logger, "FolderCleaner")
