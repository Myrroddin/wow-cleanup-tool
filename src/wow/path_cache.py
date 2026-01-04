"""WoW installation path detection and caching with TTL support."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List

logger = logging.getLogger(__name__)


class PathCache:
    """Manages caching of detected WoW installation paths with time-to-live (TTL).

    Benefits:
    - Reduces repeated filesystem scans
    - Detects if installation has moved (TTL expiration)
    - Fast lookup of previously detected paths
    - Automatic cleanup of stale cache
    """

    CACHE_FILE = Path.home() / ".wow_cleanup_tool" / "path_cache.json"
    DEFAULT_TTL_DAYS = 7  # Paths are cached for 7 days before re-detection needed

    def __init__(self, ttl_days: int = DEFAULT_TTL_DAYS):
        """Initialize the path cache.

        Args:
            ttl_days: Days to keep cache valid before forcing re-detection
        """
        self.ttl_days = ttl_days
        self._cache: dict = {}
        self._load_cache()

    def _load_cache(self) -> None:
        """Load cache from disk if it exists and is valid."""
        if not self.CACHE_FILE.exists():
            return

        try:
            with open(self.CACHE_FILE, "r") as f:
                data = json.load(f)
                self._cache = data
                logger.debug("Loaded WoW path cache from disk")
        except Exception as e:
            logger.warning(f"Failed to load path cache: {e}")
            self._cache = {}

    def _save_cache(self) -> None:
        """Save cache to disk."""
        try:
            self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(self.CACHE_FILE, "w") as f:
                json.dump(self._cache, f, indent=2)
            logger.debug("Saved WoW path cache to disk")
        except Exception as e:
            logger.warning(f"Failed to save path cache: {e}")

    def get(self, key: str) -> Optional[str]:
        """Get cached path if it exists and is valid (not expired).

        Args:
            key: Cache key (usually "wow_path" or "wow_path_<flavor>")

        Returns:
            Cached path if valid, None if expired or not found
        """
        if key not in self._cache:
            return None

        entry = self._cache[key]
        cached_path = entry.get("path")
        timestamp = entry.get("timestamp", 0)

        # Check if cache has expired
        age_seconds = datetime.now().timestamp() - timestamp
        age_days = age_seconds / (24 * 60 * 60)

        if age_days > self.ttl_days:
            logger.debug(f"Path cache '{key}' expired ({age_days:.1f} days old)")
            return None

        # Verify path still exists
        if cached_path and Path(cached_path).exists():
            logger.debug(f"Using cached path for '{key}': {cached_path}")
            return cached_path

        # Path no longer exists, invalidate cache
        logger.debug(f"Cached path for '{key}' no longer exists: {cached_path}")
        del self._cache[key]
        self._save_cache()
        return None

    def set(self, key: str, path: str) -> None:
        """Cache a WoW installation path with current timestamp.

        Args:
            key: Cache key (usually "wow_path" or "wow_path_<flavor>")
            path: Full filesystem path to WoW installation
        """
        self._cache[key] = {
            "path": path,
            "timestamp": datetime.now().timestamp(),
        }
        self._save_cache()
        logger.debug(f"Cached path for '{key}': {path}")

    def invalidate(self, key: str = None) -> None:
        """Invalidate cache entries.

        Args:
            key: Specific key to invalidate. If None, clears all cache.
        """
        if key is None:
            self._cache.clear()
            logger.debug("Cleared entire path cache")
        elif key in self._cache:
            del self._cache[key]
            logger.debug(f"Invalidated cache key: {key}")

        self._save_cache()

    def get_all_cached_paths(self) -> List[str]:
        """Get list of all currently cached valid paths.

        Returns:
            List of valid cached paths (expired entries filtered out)
        """
        valid_paths = []
        expired_keys = []

        for key, entry in self._cache.items():
            cached_path = entry.get("path")
            timestamp = entry.get("timestamp", 0)

            age_seconds = datetime.now().timestamp() - timestamp
            age_days = age_seconds / (24 * 60 * 60)

            if age_days <= self.ttl_days and cached_path:
                if Path(cached_path).exists():
                    valid_paths.append(cached_path)
                else:
                    expired_keys.append(key)
            else:
                expired_keys.append(key)

        # Clean up expired entries
        if expired_keys:
            for key in expired_keys:
                del self._cache[key]
            self._save_cache()

        return valid_paths
