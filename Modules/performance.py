"""
Performance optimization utilities for WoW Cleanup Tool.

Provides caching, memoization, and other performance enhancements.
"""

import functools
import os
import time
from typing import Any, Callable
from Modules import localization

# Try to import send2trash for safe deletion
try:
    from send2trash import send2trash
    HAS_TRASH = True
except ImportError:
    HAS_TRASH = False

def memoized_property(func: Callable) -> property:
    """Decorator to cache property results for the lifetime of the object.
    
    Useful for expensive computed properties that don't change during the app session.
    
    Args:
        func: The property getter function
        
    Returns:
        property: A memoized property that caches its value after first access
    """
    cache_attr = f'_cache_{func.__name__}'
    @property
    @functools.wraps(func)
    def wrapper(self):
        if not hasattr(self, cache_attr):
            setattr(self, cache_attr, func(self))
        return getattr(self, cache_attr)
    return wrapper

def cache_result(maxsize: int = 128) -> Callable:
    """LRU cache decorator for function results.
    
    Args:
        maxsize: Maximum number of cached results to keep
        
    Returns:
        Decorator that caches function results
    """
    return functools.lru_cache(maxsize=maxsize)

def profile_execution(logger=None):
    """Decorator to profile function execution time.
    
    Logs execution time for performance monitoring and optimization.
    
    Args:
        logger: Optional logger instance with .debug() method
        
    Returns:
        Decorator that logs execution time
        
    Example:
        @profile_execution(logger)
        def expensive_operation():
            # ... complex code
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            msg = localization._("performance_execution_time").format(func.__name__, elapsed)
            if logger and hasattr(logger, 'debug'):
                logger.debug(msg)
            else:
                print(msg)
            
            return result
        return wrapper
    return decorator

def delete_files_batch(paths, use_trash=False, logger=None, module_name="FileOps"):
    """Shared utility for deleting or trashing files/folders.
    
    Consolidates duplicate deletion logic from file_cleaner, folder_cleaner, 
    and orphan_cleaner modules for better code reuse and maintenance.
    
    Args:
        paths: Iterable of absolute file/folder paths to delete
        use_trash: If True, attempt to move to trash instead of permanent deletion
        logger: Optional object with .info() and .error() methods for logging
        module_name: Name for log messages (e.g., "FileCleaner", "OrphanCleaner")
    
    Returns:
        Tuple of (processed_count, permanently_deleted_flag, used_trash_flag):
        - processed_count: Number of items successfully deleted/moved
        - permanently_deleted_flag: True if items were permanently deleted
        - used_trash_flag: True if items were moved to trash
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
                    logger.info(localization._("perf_moved_trash").format(module_name, fp))
            else:
                # Permanently delete file or folder
                if os.path.isfile(fp):
                    os.remove(fp)
                elif os.path.isdir(fp):
                    import shutil
                    shutil.rmtree(fp)
                if logger:
                    logger.info(localization._("perf_deleted").format(module_name, fp))
            processed += 1
        except (OSError, IOError) as e:
            # Log error but continue with next item
            if logger:
                logger.error(localization._("perf_error_deleting").format(module_name, fp, e))
    
    permanently_deleted = not real_use_trash
    return processed, permanently_deleted, used_trash
