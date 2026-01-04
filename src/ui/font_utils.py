"""Font utilities for UI with optimized caching."""

import logging
import tkinter.font as tkfont
from datetime import datetime

logger = logging.getLogger(__name__)

# Module-level cache with TTL support
_font_cache = {
    "fonts": None,
    "timestamp": None,
    "ttl_seconds": 3600,  # Re-check system fonts every hour
}


def _font_cache_expired() -> bool:
    """Check if font cache has expired."""
    if _font_cache["timestamp"] is None:
        return True

    age_seconds = (datetime.now() - _font_cache["timestamp"]).total_seconds()
    return age_seconds > _font_cache["ttl_seconds"]


def get_available_fonts(default_label="System Default"):
    """Get list of available system fonts, with common fonts prioritized.

    Caches results to avoid repeated expensive system font queries.
    Cache automatically expires after 1 hour, or can be manually invalidated
    if fonts are installed at runtime.

    Args:
        default_label: Localized label for system default font

    Returns:
        list: Sorted list of font family names, common fonts first.
    """
    global _font_cache

    # Return cached result if valid
    if _font_cache["fonts"] is not None and not _font_cache_expired():
        logger.debug(
            f"Using cached fonts list ({len(_font_cache['fonts'])} fonts, "
            f"cached {(datetime.now() - _font_cache['timestamp']).total_seconds():.0f}s ago)"
        )
        # Remove the default label if present in the font list (case-insensitive match)
        font_list = [
            f for f in _font_cache["fonts"] if f.lower() != default_label.lower()
        ]
        # Insert the localized default label at the top
        font_list.insert(0, default_label)
        return font_list

    # Cache miss or expired - query system fonts
    logger.debug("Refreshing system fonts list...")
    try:
        # Get all available fonts, remove those starting with '@' (internal fonts)
        # Case-insensitive sorting for better UX
        available_fonts = [f for f in set(tkfont.families()) if not f.startswith("@")]
        available_fonts = sorted(available_fonts, key=lambda s: s.lower())

        # Update cache
        _font_cache["fonts"] = available_fonts
        _font_cache["timestamp"] = datetime.now()

        logger.debug(f"Cached {len(available_fonts)} system fonts")

        # Remove the default label if present in the font list (case-insensitive match)
        font_list = [f for f in available_fonts if f.lower() != default_label.lower()]
        # Insert the localized default label at the top
        font_list.insert(0, default_label)
        return font_list

    except Exception as e:
        logger.warning(f"Failed to get system fonts: {e}")
        # Fallback to minimal list
        return [default_label, "Arial", "Courier New"]


def get_font_sizes():
    """Get standard font sizes for UI.

    Returns:
        list: List of font size strings (8-16pt)
    """
    return ["8", "9", "10", "11", "12", "14", "16"]


def invalidate_font_cache() -> None:
    """Manually invalidate the font cache.

    Call this if fonts are installed at runtime and you need to refresh
    the available fonts list.
    """
    global _font_cache
    _font_cache["fonts"] = None
    _font_cache["timestamp"] = None
    logger.debug("Font cache invalidated")
