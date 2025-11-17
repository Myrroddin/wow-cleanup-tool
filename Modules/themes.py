"""
Themes module for WoW Cleanup Tool.

Provides light and dark theme support:
- Light/Dark theme color dictionaries
- Treeview theming
- Recursive widget theming
- Unified apply_theme() entry point

The application can switch themes at runtime, and this module handles
applying the theme to all UI widgets. Checkboxes are generated dynamically
using PIL/Pillow (see ui_helpers.ImgAssets) rather than PNG files.
"""

import tkinter as tk
from tkinter import ttk

LIGHT = {
    # Light theme uses light backgrounds with dark text
    "bg": "#e6e6e6",                           # Background for frames
    "fg": "#000000",                           # Foreground/text color
    "button_bg": "#d0d0d0",                    # Button background
    "button_fg": "#000000",                    # Button text
    "entry_bg": "#ffffff",                     # Entry field background
    "entry_fg": "#000000",                     # Entry field text
    "tree_bg": "#f8f8f8",                      # Treeview background
    "tree_fg": "#000000",                      # Treeview text
}

DARK = {
    # Dark theme uses dark backgrounds with light text
    "bg": "#2e2e2e",                           # Background for frames
    "fg": "#ffffff",                           # Foreground/text color
    "button_bg": "#3c3c3c",                    # Button background
    "button_fg": "#ffffff",                    # Button text
    "entry_bg": "#444444",                     # Entry field background
    "entry_fg": "#ffffff",                     # Entry field text
    "tree_bg": "#383838",                      # Treeview background
    "tree_fg": "#ffffff",                      # Treeview text
}

THEMES = {
    "light": LIGHT,
    "dark": DARK,
}

def apply_ttk_theme(root, theme_data):
    """
    Apply theme colors to all ttk widgets via ttk.Style.
    
    TTK widgets don't support direct bg/fg configuration - they use
    ttk.Style instead. This function configures all common ttk widget
    styles for the current theme.
    
    Args:
        root: The root Tk window (for accessing the style)
        theme_data: Dictionary with color definitions
    """
    style = ttk.Style(root)
    
    # Use 'clam' theme as base for better color control
    # (native themes like 'vista' or 'winnative' often ignore custom colors)
    try:
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
        elif 'default' in available_themes:
            style.theme_use('default')
    except Exception:
        pass
    
    # TFrame - main background
    style.configure(
        "TFrame",
        background=theme_data["bg"]
    )
    style.map(
        "TFrame",
        background=[("!disabled", theme_data["bg"])]
    )
    
    # TLabel - text labels
    style.configure(
        "TLabel",
        background=theme_data["bg"],
        foreground=theme_data["fg"]
    )
    style.map(
        "TLabel",
        background=[("!disabled", theme_data["bg"])],
        foreground=[("!disabled", theme_data["fg"])]
    )
    
    # TButton - buttons
    style.configure(
        "TButton",
        background=theme_data["button_bg"],
        foreground=theme_data["button_fg"],
        bordercolor=theme_data["fg"],
        lightcolor=theme_data["button_bg"],
        darkcolor=theme_data["button_bg"]
    )
    style.map(
        "TButton",
        background=[("active", theme_data["bg"]), ("!disabled", theme_data["button_bg"])],
        foreground=[("active", theme_data["fg"]), ("!disabled", theme_data["button_fg"])],
        bordercolor=[("!disabled", theme_data["fg"])]
    )
    
    # TCheckbutton - checkbuttons
    style.configure(
        "TCheckbutton",
        background=theme_data["bg"],
        foreground=theme_data["fg"]
    )
    style.map(
        "TCheckbutton",
        background=[("!disabled", theme_data["bg"])],
        foreground=[("!disabled", theme_data["fg"])]
    )
    
    # TRadiobutton - radio buttons
    style.configure(
        "TRadiobutton",
        background=theme_data["bg"],
        foreground=theme_data["fg"]
    )
    style.map(
        "TRadiobutton",
        background=[("!disabled", theme_data["bg"])],
        foreground=[("!disabled", theme_data["fg"])]
    )
    
    # TEntry - entry fields
    style.configure(
        "TEntry",
        fieldbackground=theme_data["entry_bg"],
        foreground=theme_data["entry_fg"],
        insertcolor=theme_data["fg"],
        bordercolor=theme_data["fg"]
    )
    style.map(
        "TEntry",
        fieldbackground=[("!disabled", theme_data["entry_bg"])],
        foreground=[("!disabled", theme_data["entry_fg"])]
    )
    
    # TSpinbox - spinbox fields (number input)
    style.configure(
        "TSpinbox",
        fieldbackground=theme_data["entry_bg"],
        foreground=theme_data["entry_fg"],
        insertcolor=theme_data["fg"],
        arrowcolor=theme_data["fg"],
        bordercolor=theme_data["fg"]
    )
    style.map(
        "TSpinbox",
        fieldbackground=[("!disabled", theme_data["entry_bg"])],
        foreground=[("!disabled", theme_data["entry_fg"])],
        arrowcolor=[("!disabled", theme_data["fg"])]
    )
    
    # TCombobox - dropdown menus
    style.configure(
        "TCombobox",
        fieldbackground=theme_data["entry_bg"],
        background=theme_data["button_bg"],
        foreground=theme_data["entry_fg"],
        arrowcolor=theme_data["fg"],
        bordercolor=theme_data["fg"]
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", theme_data["entry_bg"]), ("!disabled", theme_data["entry_bg"])],
        foreground=[("readonly", theme_data["entry_fg"]), ("!disabled", theme_data["entry_fg"])],
        background=[("readonly", theme_data["button_bg"]), ("!disabled", theme_data["button_bg"])],
        arrowcolor=[("!disabled", theme_data["fg"])]
    )
    
    # TNotebook - tab container
    style.configure(
        "TNotebook",
        background=theme_data["bg"],
        borderwidth=0,
        tabmargins=[2, 5, 2, 0]
    )
    style.map(
        "TNotebook",
        background=[("!disabled", theme_data["bg"])]
    )
    
    # TNotebook.Tab - individual tabs (critical for visibility)
    style.configure(
        "TNotebook.Tab",
        background=theme_data["button_bg"],
        foreground=theme_data["fg"],
        padding=[12, 6],
        bordercolor=theme_data["fg"]
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", theme_data["bg"]), ("!selected", theme_data["button_bg"]), ("active", theme_data["button_bg"])],
        foreground=[("selected", theme_data["fg"]), ("!selected", theme_data["fg"]), ("active", theme_data["fg"])],
        expand=[("selected", [1, 1, 1, 0])]
    )
    
    # TLabelframe - labeled frame containers
    style.configure(
        "TLabelframe",
        background=theme_data["bg"],
        foreground=theme_data["fg"],
        bordercolor=theme_data["fg"]
    )
    style.configure(
        "TLabelframe.Label",
        background=theme_data["bg"],
        foreground=theme_data["fg"]
    )
    style.map(
        "TLabelframe",
        background=[("!disabled", theme_data["bg"])],
        foreground=[("!disabled", theme_data["fg"])]
    )
    style.map(
        "TLabelframe.Label",
        background=[("!disabled", theme_data["bg"])],
        foreground=[("!disabled", theme_data["fg"])]
    )
    
    # TMenubutton - menu buttons
    style.configure(
        "TMenubutton",
        background=theme_data["button_bg"],
        foreground=theme_data["button_fg"],
        bordercolor=theme_data["fg"]
    )
    style.map(
        "TMenubutton",
        background=[("active", theme_data["bg"]), ("!disabled", theme_data["button_bg"])],
        foreground=[("active", theme_data["fg"]), ("!disabled", theme_data["button_fg"])]
    )
    
    # Vertical.TScrollbar - vertical scrollbars
    style.configure(
        "Vertical.TScrollbar",
        background=theme_data["button_bg"],
        troughcolor=theme_data["bg"],
        bordercolor=theme_data["fg"],
        arrowcolor=theme_data["fg"]
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("active", theme_data["bg"]), ("!disabled", theme_data["button_bg"])],
        arrowcolor=[("!disabled", theme_data["fg"])]
    )
    
    # Horizontal.TScrollbar - horizontal scrollbars
    style.configure(
        "Horizontal.TScrollbar",
        background=theme_data["button_bg"],
        troughcolor=theme_data["bg"],
        bordercolor=theme_data["fg"],
        arrowcolor=theme_data["fg"]
    )
    style.map(
        "Horizontal.TScrollbar",
        background=[("active", theme_data["bg"]), ("!disabled", theme_data["button_bg"])],
        arrowcolor=[("!disabled", theme_data["fg"])]
    )
    
    # Treeview - tree/list widgets
    style.configure(
        "Treeview",
        background=theme_data["tree_bg"],
        fieldbackground=theme_data["tree_bg"],
        foreground=theme_data["tree_fg"],
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        background=theme_data["button_bg"],
        foreground=theme_data["fg"],
        borderwidth=1,
        relief="raised"
    )
    style.map(
        "Treeview",
        background=[("selected", theme_data["button_bg"])],
        foreground=[("selected", theme_data["fg"])]
    )
    style.map(
        "Treeview.Heading",
        background=[("active", theme_data["button_bg"]), ("!disabled", theme_data["button_bg"])],
        foreground=[("active", theme_data["fg"]), ("!disabled", theme_data["fg"])]
    )

def apply_treeview_theme(treeview, theme_data):
    """
    Apply theme colors to a treeview widget.
    
    Treeview widgets use ttk.Style instead of direct color configuration,
    so we need to configure the style for the Treeview widget class.
    
    Args:
        treeview: The ttk.Treeview widget to theme
        theme_data: Dictionary with color definitions
    """
    style = ttk.Style(treeview)

    # Configure the Treeview style
    style.configure(
        "Treeview",
        background=theme_data["tree_bg"],
        fieldbackground=theme_data["tree_bg"],
        foreground=theme_data["tree_fg"],
        borderwidth=0,
    )
    # Configure individual items in the treeview
    style.configure("Treeview.Item", foreground=theme_data["tree_fg"])

def _apply_widget_theme(widget, theme_data):
    """
    Recursively apply colors to a widget and all its children.
    
    This function handles Tk widgets (which support bg/fg options directly)
    separately from ttk widgets (which use styles instead). It recursively
    processes all child widgets.
    
    Tk widgets directly configured: Tk (root), Frame, LabelFrame, Canvas, Label, 
    Button, Entry, Checkbutton, Text. TTK widgets are skipped (they use ttk.Style).
    
    Args:
        widget: The Tkinter widget to theme
        theme_data: Dictionary with color definitions
    """
    wclass = widget.winfo_class()
    
    # Handle root Tk window
    if wclass == "Tk":
        try:
            widget.configure(bg=theme_data["bg"])
        except tk.TclError:
            pass
    elif wclass in ("Frame", "LabelFrame", "Canvas"):
        try:
            widget.configure(bg=theme_data["bg"])
        except tk.TclError:
            pass
    elif wclass == "Label":
        try:
            widget.configure(bg=theme_data["bg"], fg=theme_data["fg"])
        except tk.TclError:
            pass
    elif wclass == "Button":
        try:
            widget.configure(
                bg=theme_data["button_bg"],
                fg=theme_data["button_fg"],
                activebackground=theme_data["button_bg"],
                activeforeground=theme_data["fg"],
            )
        except tk.TclError:
            pass
    elif wclass == "Entry":
        try:
            widget.configure(
                bg=theme_data["entry_bg"],
                fg=theme_data["entry_fg"],
                insertbackground=theme_data["fg"],
            )
        except tk.TclError:
            pass
    elif wclass == "Text":
        try:
            widget.configure(
                bg=theme_data["entry_bg"],
                fg=theme_data["entry_fg"],
                insertbackground=theme_data["fg"],
            )
        except tk.TclError:
            pass
    elif wclass == "Checkbutton":
        try:
            widget.configure(bg=theme_data["bg"], fg=theme_data["fg"])
        except tk.TclError:
            pass
    elif not wclass.startswith("T"):
        # For non-TTK widgets that aren't in our list above,
        # only recurse into children (this likely won't match anything)
        for child in widget.winfo_children():
            _apply_widget_theme(child, theme_data)
        return
    
    # Recurse into all children
    for child in widget.winfo_children():
        _apply_widget_theme(child, theme_data)

def apply_theme(root, treeviews, theme_name, base_path):
    """
    Apply the selected theme to the entire application.
    
    This is the main entry point for theme switching. It:
    1. Gets the theme data for the selected theme name
    2. Applies ttk.Style configuration for all ttk widgets
    3. Recursively applies colors to root widget and all children
    4. Applies special styling to treeview widgets
    
    Args:
        root: The root Tk window
        treeviews: List of ttk.Treeview widgets to theme
        theme_name: Name of theme to apply ("light" or "dark")
        base_path: Base directory path (not used, kept for compatibility)
    """
    theme_data = THEMES.get(theme_name, THEMES["light"])
    
    # Apply ttk.Style configuration (for ttk widgets)
    apply_ttk_theme(root, theme_data)
    
    # Apply direct widget configuration (for tk widgets)
    _apply_widget_theme(root, theme_data)
    
    # Apply treeview-specific theming
    for tv in treeviews:
        apply_treeview_theme(tv, theme_data)
