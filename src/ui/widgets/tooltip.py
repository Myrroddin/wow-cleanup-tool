"""Reusable Tooltip widget for Tkinter."""

import tkinter as tk
from tkinter import font as tkfont


class Tooltip:
    _visible_tooltips = set()

    def __init__(self, widget, text, theme, wraplength=280):
        self.widget = widget
        self.text = text
        self.theme = theme
        self.wraplength = wraplength
        self.tipwindow = None
        self._label = None

    def show(self):
        if self.tipwindow:
            self.hide()

        # Get screen dimensions for boundary detection
        screen_width = self.widget.winfo_screenwidth()
        screen_height = self.widget.winfo_screenheight()

        # Initial position: below and to the right of widget
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        # Create tooltip window temporarily to measure its size
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(True)
        bg = self.theme.get("tooltip_bg", "#ffffe0")
        fg = self.theme.get("tooltip_fg", "#000000")
        self.tipwindow.configure(bg=bg)

        # Use TkFixedFont at fixed 10pt for consistent, readable tooltips
        tooltip_font = tkfont.nametofont("TkFixedFont").copy()
        tooltip_font.config(size=10)
        label = tk.Label(
            self.tipwindow,
            text=self.text,
            background=bg,
            foreground=fg,
            relief="solid",
            borderwidth=1,
            font=tooltip_font,
            wraplength=self.wraplength,
            justify="left",
        )
        label.pack(ipadx=6, ipady=2)

        # Update window to get accurate size
        self.tipwindow.update_idletasks()
        tooltip_width = self.tipwindow.winfo_reqwidth()
        tooltip_height = self.tipwindow.winfo_reqheight()

        # Check horizontal boundary and adjust if needed
        if x + tooltip_width > screen_width - 10:  # 10px margin
            # Position to the left of the widget instead
            x = self.widget.winfo_rootx() - tooltip_width - 5

        # Check vertical boundary and adjust if needed
        if y + tooltip_height > screen_height - 10:  # 10px margin
            # Position above the widget instead
            y = self.widget.winfo_rooty() - tooltip_height - 5

        # Ensure tooltip doesn't go off-screen on left/top edges
        x = max(10, x)
        y = max(10, y)

        # Position the tooltip
        self.tipwindow.wm_geometry(f"+{x}+{y}")

        Tooltip._visible_tooltips.add(self)
        self._label = label

    def hide(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
        Tooltip._visible_tooltips.discard(self)
        self._label = None

    def refresh_theme(self, theme):
        """Refresh tooltip with new theme colors (font is always fixed)."""
        self.theme = theme
        if self.tipwindow and self._label:
            bg = self.theme.get("tooltip_bg", "#ffffe0")
            fg = self.theme.get("tooltip_fg", "#000000")
            self.tipwindow.configure(bg=bg)
            self._label.configure(background=bg, foreground=fg)

    @classmethod
    def refresh_all_visible_tooltips(cls, theme):
        """Refresh all visible tooltips with new theme (font remains fixed)."""
        for tip in list(cls._visible_tooltips):
            tip.refresh_theme(theme)
