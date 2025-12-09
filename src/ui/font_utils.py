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
    global _cached_fonts, _cached_common_fonts
    
    if _cached_fonts is None:
        # Common/useful fonts to prioritize
        common_fonts = [
            'Arial', 'Calibri', 'Consolas', 'Courier New', 'Georgia', 
            'Segoe UI', 'Tahoma', 'Times New Roman', 'Trebuchet MS', 'Verdana'
        ]
        
        available_fonts = sorted(set(tkfont.families()))
        
        # Build cached lists
        _cached_common_fonts = [f for f in common_fonts if f in available_fonts]
        _cached_fonts = [f for f in available_fonts if f not in common_fonts and not f.startswith('@')]
    
    # Build final list with localized default label
    font_list = [default_label]
    font_list += _cached_common_fonts
    font_list += _cached_fonts
    
    return font_list


def get_font_sizes():
    """Get standard font sizes for UI.
    
    Returns:
        list: List of font size strings
    """
    return ['8', '9', '10', '11', '12', '14', '16']
