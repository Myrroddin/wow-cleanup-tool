"""
Geometry management module for WoW Cleanup Tool.

Handles window sizing, positioning, centering, and persistence.
Keeps the main app class clean by delegating all geometry-related logic here.
"""

import tkinter as tk

def setup_geometry(app):
    """Set up window geometry from saved settings or center on launch.
    
    Args:
        app: The WoWCleanupTool instance
    """
    sw = app.root.winfo_screenwidth()
    sh = app.root.winfo_screenheight()
    w = app.settings.get("window_width")
    h = app.settings.get("window_height")
    x = app.settings.get("window_x")
    y = app.settings.get("window_y")
    is_max = app.settings.get("is_maximized", False)
    if all(val is not None for val in (w, h, x, y)):
        try:
            w = max(int(w), app.MIN_W); h = max(int(h), app.MIN_H)
            x = int(x); y = int(y)
            x, y = keep_on_screen(x, y, w, h, sw, sh)
            app.root.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            center_first_launch(app, sw, sh)
    else:
        center_first_launch(app, sw, sh)
    app.root.minsize(app.MIN_W, app.MIN_H)
    if is_max:
        try: app.root.state("zoomed")
        except Exception: pass

def center_first_launch(app, sw, sh):
    """Center window on first launch based on screen size.
    
    Args:
        app: The WoWCleanupTool instance
        sw: Screen width
        sh: Screen height
    """
    if sw >= 3840:
        w = max(int(sw * 0.25), app.MIN_W)
        h = max(int(sh * 0.25), app.MIN_H)
    else:
        w = max(int(sw * 0.58), app.MIN_W)
        h = max(int(sh * 0.6), app.MIN_H)
    x = (sw // 2) - (w // 2); y = (sh // 2) - (h // 2)
    app.root.geometry(f"{w}x{h}+{x}+{y}")

def parse_geometry(geometry):
    """Parse a geometry string into (width, height, x, y).
    
    Args:
        geometry: Geometry string from root.geometry()
    
    Returns:
        Tuple of (w, h, x, y) or None if parsing fails
    """
    try:
        size, pos = geometry.split("+", 1)
        w_str, h_str = size.split("x")
        x_str, y_str = pos.split("+")
        return int(w_str), int(h_str), int(x_str), int(y_str)
    except Exception:
        return None

def keep_on_screen(x, y, w, h, sw, sh):
    """Adjust window position to keep at least 20% visible on screen.
    
    Allows the window to move to other monitors in multi-monitor setups,
    but ensures at least 20% of the window remains visible (80% can be off-screen).
    
    Args:
        x, y: Window position
        w, h: Window dimensions
        sw, sh: Screen dimensions (primary screen or virtual desktop)
    
    Returns:
        Tuple of (adjusted_x, adjusted_y)
    """
    # Minimum visible portion: 20% of window dimensions
    min_visible_w = int(w * 0.2)
    min_visible_h = int(h * 0.2)
    
    # Allow window to extend beyond screen bounds for multi-monitor support
    # but ensure at least 20% remains visible on the primary screen area
    
    # Right edge: ensure at least min_visible_w pixels are visible from the left
    if x > sw - min_visible_w:
        x = sw - min_visible_w
    
    # Left edge: ensure at least min_visible_w pixels are visible from the right
    if x + w < min_visible_w:
        x = min_visible_w - w
    
    # Bottom edge: ensure at least min_visible_h pixels are visible from the top
    if y > sh - min_visible_h:
        y = sh - min_visible_h
    
    # Top edge: ensure at least min_visible_h pixels are visible from the bottom
    if y + h < min_visible_h:
        y = min_visible_h - h
    
    return x, y

def on_configure(app):
    """Handle window resize/move events to keep window on screen.
    
    Args:
        app: The WoWCleanupTool instance
    """
    try:
        if app.root.state() == "zoomed":
            return
    except Exception:
        pass
    parsed = parse_geometry(app.root.geometry())
    if not parsed: return
    w, h, x, y = parsed
    sw = app.root.winfo_screenwidth(); sh = app.root.winfo_screenheight()
    nx, ny = keep_on_screen(x, y, w, h, sw, sh)
    if (nx, ny) != (x, y):
        app.root.geometry(f"{w}x{h}+{nx}+{ny}")

def save_geometry(app):
    """Save current window geometry to settings.
    
    Args:
        app: The WoWCleanupTool instance
    """
    is_max = False
    try: is_max = (app.root.state() == "zoomed")
    except Exception: pass
    if not is_max:
        parsed = parse_geometry(app.root.geometry())
        if parsed:
            w, h, x, y = parsed
            app.settings["window_width"] = max(w, app.MIN_W)
            app.settings["window_height"] = max(h, app.MIN_H)
            app.settings["window_x"] = x
            app.settings["window_y"] = y
    app.settings["is_maximized"] = is_max
