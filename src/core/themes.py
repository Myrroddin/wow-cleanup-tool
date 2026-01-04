"""
Theme system for WoW Cleanup Tool.

Provides light and dark themes using sv-ttk with fallback to custom themes.
"""

from tkinter import ttk

try:
    import sv_ttk

    SV_TTK_AVAILABLE = True
except ImportError:
    SV_TTK_AVAILABLE = False


def resolve_system_theme() -> str:
    """Resolve 'system' theme to actual light or dark based on OS.

    Returns:
        str: "light" or "dark" depending on current OS theme setting
    """
    try:
        import darkdetect

        os_theme = darkdetect.theme()
        return "dark" if os_theme and os_theme.lower() == "dark" else "light"
    except Exception:
        return "light"  # Fallback to light if detection fails


THEMES = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "button_bg": "#e1e1e1",
        "button_fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000",
        "select_bg": "#0078d7",
        "select_fg": "#ffffff",
        "frame_bg": "#f0f0f0",
        "labelframe_bg": "#f0f0f0",
        "arrow_color": "#000000",
        "tooltip_bg": "#ffffe0",
        "tooltip_fg": "#000000",
    },
    "dark": {
        "bg": "#2b2b2b",
        "fg": "#e0e0e0",
        "button_bg": "#3c3c3c",
        "button_fg": "#e0e0e0",
        "entry_bg": "#1e1e1e",
        "entry_fg": "#e0e0e0",
        "select_bg": "#0078d7",
        "select_fg": "#ffffff",
        "frame_bg": "#2b2b2b",
        "labelframe_bg": "#353535",
        "arrow_color": "#e0e0e0",
        "tooltip_bg": "#4a4a4a",
        "tooltip_fg": "#e0e0e0",
    },
}


def apply_theme(root, theme_name, font_family="TkDefaultFont", font_size=9):
    """Apply theme and font to the application.

    Attempts to use sv-ttk for modern Windows 11-style theming first.
    Falls back to custom theme implementation if sv-ttk is unavailable or fails.

    Args:
        root: Tkinter root window
        theme_name: Name of theme ("light", "dark", or "system")
        font_family: Font family to use
        font_size: Font size to use

    Returns:
        dict: Theme data dictionary
    """
    # Resolve "system" theme to actual light or dark
    if theme_name == "system":
        theme_name = resolve_system_theme()

    # Use sv-ttk if available for modern Windows 11-style UI
    if SV_TTK_AVAILABLE:
        try:
            if theme_name == "dark":
                sv_ttk.set_theme("dark")
            else:
                sv_ttk.set_theme("light")

            # Apply font customization
            style = ttk.Style(root)
            style.configure(".", font=(font_family, font_size))
            style.configure("TButton", font=(font_family, font_size))
            style.configure("TLabel", font=(font_family, font_size))
            style.configure("Title.TLabel", font=(font_family, font_size + 3, "bold"))
            style.configure("TLabelFrame.Label", font=(font_family, font_size, "bold"))

            # Return theme data for compatibility
            return THEMES.get(theme_name, THEMES["light"])
        except Exception:
            # Fall back to custom themes if sv-ttk fails
            pass

    # ============================================================================
    # FALLBACK THEME IMPLEMENTATION
    # The code below is used only when sv-ttk is unavailable or fails to load.
    # This ensures graceful degradation on systems without sv-ttk installed.
    # ============================================================================
    theme_data = THEMES.get(theme_name, THEMES["light"])

    # Configure ttk styles
    style = ttk.Style(root)

    # Configure ttk theme
    style.theme_use("clam")  # Use clam theme as base (supports more customization)

    # Configure ttk widget styles with font
    style.configure("TFrame", background=theme_data["frame_bg"])
    style.configure(
        "TLabelFrame",
        background=theme_data["labelframe_bg"],
        foreground=theme_data["fg"],
        bordercolor=theme_data["fg"],
        relief="solid",
        borderwidth=1,
    )
    style.configure(
        "TLabelFrame.Label",
        background=theme_data["labelframe_bg"],
        foreground=theme_data["fg"],
        font=(font_family, font_size, "bold"),
    )
    style.configure(
        "TLabel",
        background=theme_data["frame_bg"],
        foreground=theme_data["fg"],
        font=(font_family, font_size),
    )
    style.configure(
        "Title.TLabel",
        background=theme_data["frame_bg"],
        foreground=theme_data["fg"],
        font=(font_family, font_size + 3, "bold"),
    )
    # 2025-12-30: Scale button padding with font to avoid oversized borders on small fonts
    pad_x = max(6, int(font_size * 0.7))
    pad_y = max(3, int(font_size * 0.45))
    style.configure(
        "TButton",
        background=theme_data["button_bg"],
        foreground=theme_data["button_fg"],
        font=(font_family, font_size),
        padding=(pad_x, pad_y),
    )
    style.map(
        "TButton",
        background=[
            ("active", theme_data["select_bg"]),
            ("!active", theme_data["button_bg"]),
        ],
        foreground=[
            ("active", theme_data["select_fg"]),
            ("!active", theme_data["button_fg"]),
        ],
    )
    style.configure(
        "TEntry",
        fieldbackground=theme_data["entry_bg"],
        foreground=theme_data["entry_fg"],
        font=(font_family, font_size),
    )
    style.configure(
        "TCombobox",
        fieldbackground=theme_data["entry_bg"],
        foreground=theme_data["entry_fg"],
        background=theme_data["button_bg"],
        arrowcolor=theme_data["arrow_color"],
        font=(font_family, font_size),
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", theme_data["entry_bg"])],
        foreground=[("readonly", theme_data["entry_fg"])],
        selectbackground=[("readonly", theme_data["entry_bg"])],
        selectforeground=[("readonly", theme_data["entry_fg"])],
        arrowcolor=[
            ("disabled", theme_data["fg"]),
            ("pressed", theme_data["select_bg"]),
            ("active", theme_data["arrow_color"]),
            ("!active", theme_data["arrow_color"]),
        ],
    )
    style.configure(
        "TCheckbutton",
        background=theme_data["frame_bg"],
        foreground=theme_data["fg"],
        font=(font_family, font_size),
    )
    style.configure(
        "TRadiobutton",
        background=theme_data["frame_bg"],
        foreground=theme_data["fg"],
        font=(font_family, font_size),
    )
    style.configure(
        "TScrollbar", background=theme_data["button_bg"], troughcolor=theme_data["bg"]
    )
    style.configure(
        "TNotebook",
        background=theme_data["frame_bg"],
        borderwidth=0,
        tabmargins=[2, 5, 2, 0],
    )
    style.configure(
        "TNotebook.Tab",
        background=theme_data["button_bg"],
        foreground=theme_data["fg"],
        padding=[10, 5],
        font=(font_family, font_size),
    )
    style.map(
        "TNotebook.Tab",
        background=[
            ("selected", theme_data["select_bg"]),
            ("!selected", theme_data["button_bg"]),
        ],
        foreground=[
            ("selected", theme_data["select_fg"]),
            ("!selected", theme_data["fg"]),
        ],
    )
    style.configure(
        "Treeview",
        background=theme_data["entry_bg"],
        foreground=theme_data["fg"],
        fieldbackground=theme_data["entry_bg"],
        font=(font_family, font_size),
        rowheight=int(font_size * 2.2),  # Scale row height with font
    )
    style.configure(
        "Treeview.Heading",
        background=theme_data["button_bg"],
        foreground=theme_data["fg"],
        font=(font_family, font_size, "bold"),
    )
    style.map(
        "Treeview",
        background=[("selected", theme_data["select_bg"])],
        foreground=[("selected", theme_data["select_fg"])],
    )

    # Apply to root window
    try:
        root.configure(bg=theme_data["bg"])
    except Exception:
        pass

    # Recursively apply to all widgets (for classic tk widgets like Text)
    _apply_widget_theme(root, theme_data, font_family, font_size)

    return theme_data


def _apply_widget_theme(widget, theme_data, font_family="TkDefaultFont", font_size=9):
    """Recursively apply colors and font to a widget and all its children.

    Args:
        widget: The Tkinter widget to theme
        theme_data: Dictionary with color definitions
        font_family: Font family to use
        font_size: Font size to use
    """
    wclass = widget.winfo_class()

    # Only apply to classic tk widgets (ttk widgets use ttk.Style)
    # Handle Text widget specifically (it's classic tk, not ttk)
    if wclass == "Text":
        try:
            widget.configure(
                bg=theme_data["entry_bg"],
                fg=theme_data["entry_fg"],
                insertbackground=theme_data["fg"],
                selectbackground=theme_data["select_bg"],
                selectforeground=theme_data["select_fg"],
                font=(font_family, font_size),
            )
        except Exception:
            pass
    elif wclass == "Canvas":
        try:
            widget.configure(bg=theme_data["bg"])
        except Exception:
            pass

    # Recurse into all children
    for child in widget.winfo_children():
        _apply_widget_theme(child, theme_data, font_family, font_size)


def get_theme_colors(theme_name):
    """Get color dictionary for a theme.

    Args:
        theme_name: Name of theme ("light", "dark", or "system")

    Returns:
        dict: Theme color data
    """
    # Resolve "system" theme to actual light or dark
    if theme_name == "system":
        theme_name = resolve_system_theme()

    return THEMES.get(theme_name, THEMES["light"])
