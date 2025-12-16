"""Reusable Tooltip widget for Tkinter."""

import tkinter as tk


class Tooltip:
    _visible_tooltips = set()

    def __init__(self, widget, text, theme, font_family, font_size, wraplength=320):
        self.widget = widget
        self.text = text
        self.theme = theme
        self.font_family = font_family
        self.font_size = font_size
        self.wraplength = wraplength
        self.tipwindow = None
        self._label = None

    def show(self):
        if self.tipwindow:
            self.hide()
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(True)
        self.tipwindow.wm_geometry(f"+{x}+{y}")
        bg = self.theme.get("tooltip_bg", "#ffffe0")
        fg = self.theme.get("tooltip_fg", "#000000")
        self.tipwindow.configure(bg=bg)
        label = tk.Label(
            self.tipwindow,
            text=self.text,
            background=bg,
            foreground=fg,
            relief="solid",
            borderwidth=1,
            font=(self.font_family, self.font_size),
            wraplength=self.wraplength,
            justify="left",
        )
        label.pack(ipadx=6, ipady=2)
        Tooltip._visible_tooltips.add(self)
        self._label = label

    def hide(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
        Tooltip._visible_tooltips.discard(self)
        self._label = None

    def refresh_theme_and_fonts(self, theme, font_family, font_size):
        self.theme = theme
        self.font_family = font_family
        self.font_size = font_size
        if self.tipwindow and self._label:
            bg = self.theme.get("tooltip_bg", "#ffffe0")
            fg = self.theme.get("tooltip_fg", "#000000")
            self.tipwindow.configure(bg=bg)
            self._label.configure(
                background=bg, foreground=fg, font=(self.font_family, self.font_size)
            )

    @classmethod
    def refresh_all_visible_tooltips(cls, theme, font_family, font_size):
        for tip in list(cls._visible_tooltips):
            tip.refresh_theme_and_fonts(theme, font_family, font_size)
