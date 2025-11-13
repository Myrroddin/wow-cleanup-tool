"""
Themes module for WoW Cleanup Tool.

Provides:
- Light/Dark theme color dictionaries
- Checkbox icon loading
- Treeview theming
- Recursive widget theming
- Unified apply_theme() entry point
"""

import os
import tkinter as tk
from tkinter import ttk


# ---------------------------------------
# THEME DEFINITIONS
# ---------------------------------------

LIGHT = {
    "bg": "#e6e6e6",
    "fg": "#000000",
    "button_bg": "#d0d0d0",
    "button_fg": "#000000",
    "entry_bg": "#ffffff",
    "entry_fg": "#000000",
    "tree_bg": "#f8f8f8",
    "tree_fg": "#000000",
    "checkbox_on": "images/light/checkbox_on.png",
    "checkbox_off": "images/light/checkbox_off.png",
}

DARK = {
    "bg": "#2e2e2e",
    "fg": "#ffffff",
    "button_bg": "#3c3c3c",
    "button_fg": "#ffffff",
    "entry_bg": "#444444",
    "entry_fg": "#ffffff",
    "tree_bg": "#383838",
    "tree_fg": "#ffffff",
    "checkbox_on": "images/dark/checkbox_on.png",
    "checkbox_off": "images/dark/checkbox_off.png",
}

THEMES = {
    "light": LIGHT,
    "dark": DARK,
}


# ---------------------------------------
# CHECKBOX ICON LOADING
# ---------------------------------------

def load_checkbox_icons(theme_data, base_path):
    """Load themed checkbox images."""
    on_path = os.path.join(base_path, theme_data["checkbox_on"])
    off_path = os.path.join(base_path, theme_data["checkbox_off"])
    return (
        tk.PhotoImage(file=on_path),
        tk.PhotoImage(file=off_path),
    )


# ---------------------------------------
# TREEVIEW STYLE
# ---------------------------------------

def apply_treeview_theme(treeview, theme_data):
    style = ttk.Style(treeview)

    style.configure(
        "Treeview",
        background=theme_data["tree_bg"],
        fieldbackground=theme_data["tree_bg"],
        foreground=theme_data["tree_fg"],
        borderwidth=0,
    )
    style.configure("Treeview.Item", foreground=theme_data["tree_fg"])


# ---------------------------------------
# RECURSIVE WIDGET THEMING
# ---------------------------------------

def _apply_widget_theme(widget, theme_data):
    """
    Safely apply colors only to widgets that support bg/fg.
    Ttk widgets use styles instead and must be skipped.
    """

    wclass = widget.winfo_class()

    # ----- Tk Widgets (support bg/fg) -----
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

    # ----- TTK widgets (skip direct coloring) -----
    elif wclass.startswith("T"):
        # TFrame, TLabel, TButton, TCombobox, Treeview, etc.
        # These must be styled via ttk.Style ONLY.
        pass

    # ----- Recurse into children -----
    for child in widget.winfo_children():
        _apply_widget_theme(child, theme_data)

# ---------------------------------------
# MAIN APPLY FUNCTION
# ---------------------------------------

def apply_theme(root, treeviews, theme_name, base_path):
    """
    Apply the selected theme to:
    - root + all widgets
    - provided treeviews
    - returns checkbox icon pair
    """
    theme_data = THEMES.get(theme_name, THEMES["light"])

    # Apply widget color theme recursively
    _apply_widget_theme(root, theme_data)

    # Treeviews
    for tv in treeviews:
        apply_treeview_theme(tv, theme_data)

    # Checkbox image set
    return load_checkbox_icons(theme_data, base_path)
