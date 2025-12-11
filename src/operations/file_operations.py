"""
File operations for deleting or trashing files/folders in WoW Cleanup Tool.
"""
from typing import List, Tuple
import os
from send2trash import send2trash

def delete_files_batch(
    paths: List[str], 
    delete_mode: str = 'trash',
    logger = None,
    loc = None
) -> Tuple[int, bool, bool]:
    """Delete or trash files/folders.
    Args:
        paths: List of file/folder paths to delete
        delete_mode: 'trash' or 'permanent'
        logger: Logger instance for verbose output
        loc: Localization instance
    Returns:
        (processed_count, permanently_deleted, used_trash)
    """
    processed = 0
    used_trash = False
    for path in paths:
        try:
            if delete_mode == 'trash':
                send2trash(path)
                used_trash = True
                if logger:
                    logger.verbose(f"Moved to trash: {path}")
            else:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                if logger:
                    logger.verbose(f"Deleted permanently: {path}")
            processed += 1
        except (OSError, IOError) as e:
            if logger:
                logger.error(f"Failed to delete {path}: {e}")
            continue
    return processed, not used_trash, used_trash
