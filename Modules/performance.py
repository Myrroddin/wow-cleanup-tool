"""
Performance optimization utilities for WoW Cleanup Tool.

Provides caching, memoization, and other performance enhancements.
"""

import functools
from typing import Any, Callable

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
