"""
Themes module for WoW Cleanup Tool.

Provides light and dark theme support:
- Light/Dark theme color dictionaries
- Checkbox icon loading
- Treeview theming
- Recursive widget theming
- Unified apply_theme() entry point

The application can switch themes at runtime, and this module handles
applying the theme to all UI widgets.
"""

import os
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
    "checkbox_on": "images/light/checkbox_on.png",    # Checked checkbox image
    "checkbox_off": "images/light/checkbox_off.png",  # Unchecked checkbox image
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
    "checkbox_on": "images/dark/checkbox_on.png",     # Checked checkbox image
    "checkbox_off": "images/dark/checkbox_off.png",   # Unchecked checkbox image
}

THEMES = {
    "light": LIGHT,
    "dark": DARK,
}

def load_checkbox_icons(theme_data, base_path):
    """
    Load themed checkbox images.
    
    Loads the "on" (checked) and "off" (unchecked) checkbox images
    for the current theme. These are used by custom checkbox widgets
    to display proper themed checkboxes.
    
    Args:
        theme_data: Dictionary with "checkbox_on" and "checkbox_off" keys
        base_path: Base directory path for resolving image paths
    
    Returns:
        Tuple of (on_image, off_image) as tk.PhotoImage objects
    """
    on_path = os.path.join(base_path, theme_data["checkbox_on"])
    off_path = os.path.join(base_path, theme_data["checkbox_off"])
    return (
        tk.PhotoImage(file=on_path),
        tk.PhotoImage(file=off_path),
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
    
    Tk widgets directly configured: Frame, LabelFrame, Canvas, Label, Button,
    Entry, Checkbutton. TTK widgets are skipped (they use ttk.Style).
    
    Args:
        widget: The Tkinter widget to theme
        theme_data: Dictionary with color definitions
    """
    wclass = widget.winfo_class()
    if wclass in ("Frame", "LabelFrame", "Canvas"):
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
    for child in widget.winfo_children():
        _apply_widget_theme(child, theme_data)

def apply_theme(root, treeviews, theme_name, base_path):
    """
    Apply the selected theme to the entire application.
    
    This is the main entry point for theme switching. It:
    1. Gets the theme data for the selected theme name
    2. Recursively applies colors to root widget and all children
    3. Applies special styling to treeview widgets
    4. Loads and returns checkbox icon images for use in custom widgets
    
    Args:
        root: The root Tk window
        treeviews: List of ttk.Treeview widgets to theme
        theme_name: Name of theme to apply ("light" or "dark")
        base_path: Base directory path for resolving image paths
    
    Returns:
        Tuple of (checkbox_on_image, checkbox_off_image) as tk.PhotoImage objects
    """
    theme_data = THEMES.get(theme_name, THEMES["light"])
    _apply_widget_theme(root, theme_data)
    for tv in treeviews:
        apply_treeview_theme(tv, theme_data)
    return load_checkbox_icons(theme_data, base_path)
