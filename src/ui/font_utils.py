"""Font utilities for UI."""

import tkinter.font as tkfont


# Cache font families to avoid repeated system calls
_cached_fonts = None
_cached_common_fonts = None


def get_available_fonts(default_label="System Default"):
    """Get list of available system fonts, with common fonts prioritized.

    Caches results to avoid repeated system font queries.

    Args:
        default_label: Localized label for system default font

    Returns:
        list: Sorted list of font family names, common fonts first.
    """
    global _cached_fonts

    if _cached_fonts is None:
        # Get all available fonts, remove those starting with '@', sort alphabetically (case-insensitive)
        available_fonts = [f for f in set(tkfont.families()) if not f.startswith("@")]
        available_fonts = sorted(available_fonts, key=lambda s: s.lower())
        _cached_fonts = available_fonts

    # Remove the default label if present in the font list (case-insensitive match)
    font_list = [f for f in _cached_fonts if f.lower() != default_label.lower()]
    # Insert the localized default label at the top
    font_list.insert(0, default_label)
    return font_list


def get_font_sizes():
    """Get standard font sizes for UI.

    Returns:
        list: List of font size strings
    """
    return ["8", "9", "10", "11", "12", "14", "16"]
