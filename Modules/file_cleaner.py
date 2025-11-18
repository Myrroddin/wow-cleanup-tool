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
import re
from Modules import localization
from send2trash import send2trash

# Compiled pattern for .bak/.old (performance)
_BAK_OLD_PATTERN = re.compile(r"\.(bak|old)$", re.IGNORECASE)

def scan_bak_old_in_version(version_path, logger=None):
    """Scan a single WoW version path for .bak/.old files.

    Args:
        version_path: Absolute path to a WoW version (e.g., _retail_)
        logger: Optional object with .debug() method

    Returns:
        list[str]: Absolute file paths found under this version
    """
    _ = localization.get_text
    matches = []
    for rootd, _dirs, files in os.walk(version_path):
        for fname in files:
            lf = fname.lower()
            if lf.endswith((".bak", ".old")):
                fpath = os.path.join(rootd, fname)
                matches.append(fpath)
                if logger:
                    logger.debug(_("file_cleaner_found_file").format(fpath))
    return matches

def find_bak_old_files(versions, logger=None):
    """Scan versions for .bak/.old files using os.scandir for speed."""
    _ = localization.get_text
    results = {}
    total = 0

    def _scan_dir(start_dir, out_list):
        try:
            with os.scandir(start_dir) as entries:
                for entry in entries:
                    try:
                        if entry.is_file(follow_symlinks=False):
                            if _BAK_OLD_PATTERN.search(entry.name):
                                out_list.append(entry.path)
                                if logger:
                                    logger.debug(_("file_cleaner_found").format(entry.path))
                        elif entry.is_dir(follow_symlinks=False):
                            _scan_dir(entry.path, out_list)
                    except (OSError, PermissionError):
                        # Skip problematic entries
                        continue
        except (OSError, PermissionError):
            # Skip directories we cannot access
            pass

    for vpath, vlabel in versions:
        vlabel_files = []
        _scan_dir(vpath, vlabel_files)
        if vlabel_files:
            results[vlabel] = vlabel_files
            total += len(vlabel_files)

    if logger:
        logger.info(_("file_cleaner_total_found").format(total))
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
    _ = localization.get_text
    processed = 0
    used_trash = False
    for fp in paths:
        try:
            if use_trash:
                send2trash(fp)
                used_trash = True
                if logger:
                    logger.info(_("file_cleaner_moved_trash").format(fp))
            else:
                os.remove(fp)
                if logger:
                    logger.info(_("file_cleaner_deleted").format(fp))
            processed += 1
        except (OSError, IOError) as e:
            if logger:
                logger.error(_("file_cleaner_error_deleting").format(fp, e))
    permanently_deleted = not use_trash
    return processed, permanently_deleted, used_trash

