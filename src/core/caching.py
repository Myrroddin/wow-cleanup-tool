"""Caching improvements for UI operations like theme detection and settings access."""

import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)


def timed_cache(seconds: int = 300):
    """Decorator for caching function results with TTL (time-to-live).

    Useful for expensive operations that can be cached for a short time.
    Examples: theme detection, system info, calculated layouts.

    Args:
        seconds: How long to cache result (default: 5 minutes)

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        cache: Dict[str, Any] = {"value": None, "expires": None}

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = datetime.now()

            # Check if cache exists and hasn't expired
            if cache["value"] is not None and cache["expires"]:
                if now < cache["expires"]:
                    logger.debug(
                        f"Using cached result for {func.__name__} "
                        f"(expires in {(cache['expires'] - now).total_seconds():.0f}s)"
                    )
                    return cache["value"]

            # Cache miss or expired - call function
            result = func(*args, **kwargs)
            cache["value"] = result
            cache["expires"] = now + timedelta(seconds=seconds)
            logger.debug(f"Cached {func.__name__} for {seconds} seconds")
            return result

        # Allow manual cache invalidation
        wrapper.invalidate_cache = lambda: cache.update(
            {"value": None, "expires": None}
        )

        return wrapper

    return decorator


class SettingsCache:
    """Fast in-memory cache for frequently accessed settings.

    Reduces disk I/O by caching loaded settings in memory. Automatically
    invalidates when settings are saved.
    """

    def __init__(self):
        """Initialize settings cache."""
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting from cache.

        Args:
            key: Setting key
            default: Default value if not found

        Returns:
            Cached value or default
        """
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set setting in cache.

        Args:
            key: Setting key
            value: Value to cache
        """
        self._cache[key] = value
        self._timestamps[key] = datetime.now().timestamp()

    def set_all(self, settings_dict: Dict[str, Any]) -> None:
        """Cache entire settings dictionary.

        Args:
            settings_dict: Dictionary of all settings
        """
        self._cache = settings_dict.copy()
        now = datetime.now().timestamp()
        self._timestamps = {key: now for key in settings_dict.keys()}
        logger.debug(f"Cached {len(settings_dict)} settings")

    def invalidate(self, key: str = None) -> None:
        """Invalidate cache entry.

        Args:
            key: Specific key to invalidate. If None, clears entire cache.
        """
        if key is None:
            self._cache.clear()
            self._timestamps.clear()
            logger.debug("Cleared settings cache")
        elif key in self._cache:
            del self._cache[key]
            del self._timestamps[key]
            logger.debug(f"Invalidated cache for '{key}'")

    def is_empty(self) -> bool:
        """Check if cache is empty."""
        return len(self._cache) == 0
