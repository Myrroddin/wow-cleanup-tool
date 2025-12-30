def reset_window_geometry(app):
    """Reset window geometry to default (content-based) size on next launch."""
    # Remove geometry-related settings
    for key in [
        "window_width",
        "window_height",
        "window_x",
        "window_y",
        "is_maximized",
    ]:
        if key in app.settings:
            del app.settings[key]
    from core.settings import save_settings

    save_settings(app.settings)
    # Optionally, resize immediately (for current session)
    if hasattr(app, "root"):
        sw = app.root.winfo_screenwidth()
        sh = app.root.winfo_screenheight()
        if hasattr(app, "center_first_launch"):
            app.center_first_launch(app, sw, sh)
        else:
            from ui.geometry import center_first_launch

            center_first_launch(app, sw, sh)


"""Geometry management for WoW Cleanup Tool.

Handles window sizing, positioning, and persistence across sessions.
"""

__all__ = [
    "setup_geometry",
]


def setup_geometry(app):
    """Set up window geometry from saved settings or use content-based sizing.

    Args:
        app: The application instance
    """
    sw = app.root.winfo_screenwidth()
    sh = app.root.winfo_screenheight()

    # Try to load saved geometry
    w = app.settings.get("window_width")
    h = app.settings.get("window_height")
    x = app.settings.get("window_x")
    y = app.settings.get("window_y")
    is_max = app.settings.get("is_maximized", False)

    if all(val is not None for val in (w, h, x, y)):
        try:

            y = int(y)
            x, y = keep_on_screen(x, y, w, h, sw, sh)
            app.root.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            center_first_launch(app, sw, sh)
    else:
        center_first_launch(app, sw, sh)

    app.root.minsize(app.MIN_W, app.MIN_H)

    if is_max:
        try:
            app.root.state("zoomed")
        except Exception:
            pass


def center_first_launch(app, sw, sh):
    """Center window on first launch based on content size and font.

    The window size automatically scales based on font size to ensure
    all UI elements are visible according to their defined layout.

    Args:
        app: The application instance
        sw: Screen width
        sh: Screen height
    """
    # Update geometry to ensure widgets are sized
    app.root.update_idletasks()

    # Get the requested size from the window manager
    requested_w = app.root.winfo_reqwidth()
    requested_h = app.root.winfo_reqheight()

    # Use requested size, but enforce minimums and screen limits
    w = max(requested_w, app.MIN_W)
    h = max(requested_h, app.MIN_H)

    # Don't exceed 90% of screen size
    max_w = int(sw * 0.9)
    max_h = int(sh * 0.9)
    w = min(w, max_w)
    h = min(h, max_h)

    # Center on screen
    x = (sw // 2) - (w // 2)
    y = (sh // 2) - (h // 2)
    app.root.geometry(f"{w}x{h}+{x}+{y}")


def keep_on_screen(x, y, w, h, sw, sh):
    """Adjust window position to keep at least 20% visible on screen.

    Args:
        x, y: Window position
        w, h: Window dimensions
        sw, sh: Screen dimensions

    Returns:
        Tuple of (adjusted_x, adjusted_y)
    """
    min_visible_w = int(w * 0.2)
    min_visible_h = int(h * 0.2)

    if x > sw - min_visible_w:
        x = sw - min_visible_w
    if x + w < min_visible_w:
        x = min_visible_w - w
    if y > sh - min_visible_h:
        y = sh - min_visible_h
    if y + h < min_visible_h:
        y = min_visible_h - h

    return x, y


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


def resize_to_content(root, min_w=480, min_h=320):
    """Resize window to fit requested content size while enforcing minimums.

    Args:
        root: Tk root window
        min_w: Minimum width
        min_h: Minimum height
    """
    # 2025-12-30: Shared helper to avoid duplicating geometry resize logic across UI events
    try:
        root.update_idletasks()
        req_w = root.winfo_reqwidth()
        req_h = root.winfo_reqheight()
        w = max(req_w, min_w)
        h = max(req_h, min_h)
        geo = root.geometry()
        parts = geo.split("+")
        if len(parts) >= 3:
            x_str, y_str = parts[1], parts[2]
            root.geometry(f"{w}x{h}+{x_str}+{y_str}")
        else:
            root.geometry(f"{w}x{h}")
    except Exception:
        pass


def on_configure(app):
    """Handle window resize/move events to keep window on screen.

    Args:
        app: The application instance
    """
    try:
        if app.root.state() == "zoomed":
            return
    except Exception:
        pass

    parsed = parse_geometry(app.root.geometry())
    if not parsed:
        return

    w, h, x, y = parsed
    sw = app.root.winfo_screenwidth()
    sh = app.root.winfo_screenheight()
    nx, ny = keep_on_screen(x, y, w, h, sw, sh)

    if (nx, ny) != (x, y):
        app.root.geometry(f"{w}x{h}+{nx}+{ny}")


def save_geometry(app):
    """Save current window geometry to settings.

    Args:
        app: The application instance
    """
    is_max = False
    try:
        is_max = app.root.state() == "zoomed"
    except Exception:
        pass

    if not is_max:
        parsed = parse_geometry(app.root.geometry())
        if parsed:
            w, h, x, y = parsed
            app.settings["window_width"] = max(w, app.MIN_W)
            app.settings["window_height"] = max(h, app.MIN_H)
            app.settings["window_x"] = x
            app.settings["window_y"] = y

    app.settings["is_maximized"] = is_max
