"""UI helper widgets extracted from the main app.

Contains Tooltip, ImgAssets, ImgCheckbox and ImgRadio. These rely on Tk and
Pillow (if available) to render images; they gracefully degrade when Pillow
is not installed.
"""
import platform
import tkinter as tk
from tkinter import ttk

# Try to import PIL (optional)
try:
    from PIL import Image, ImageTk, ImageDraw
except Exception:
    Image = ImageTk = ImageDraw = None

class Tooltip:
    """Simple tooltip for widgets.

    Usage: Tooltip(widget, "Some text", delay=500)
    """
    
    # Class-level tracking of all active tooltips
    _all_tooltips = []

    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip = None
        self.after_id = None
        widget.bind("<Enter>", self.on_enter, add="+")
        widget.bind("<Leave>", self.on_leave, add="+")
        widget.bind("<ButtonPress>", self.on_leave, add="+")
        
        # Register this tooltip
        Tooltip._all_tooltips.append(self)

    def on_enter(self, _=None):
        # Hide all other tooltips before showing this one
        for tooltip in Tooltip._all_tooltips:
            if tooltip is not self:
                tooltip.hide()
        
        self.after_id = self.widget.after(self.delay, self.show)

    def on_leave(self, _=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self.hide()

    def show(self):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(
            tw,
            text=self.text,
            bg="#ffffe0",
            fg="black",
            relief="solid",
            bd=1,
            padx=6,
            pady=3,
            justify="left",
            wraplength=280,
        )
        lbl.pack()
        self.tip = tw

    def hide(self):
        if self.tip:
            try:
                self.tip.destroy()
            except tk.TclError:
                pass
            self.tip = None

class ImgAssets:
    """Generator for small checkbox/radio images using PIL when available."""

    def __init__(self, osname: str = None, dark: bool = False):
        self.osname = osname or platform.system()
        self.dark = dark
        self.has_pil = bool(Image and ImageDraw and ImageTk)
        self.cache = {}

    def _colors(self):
        if self.dark:
            return {
                "border": "#b0b0b0",
                "fill": "#3a3a3a",
                "check": "#f5f5f5",
                "dot": "#f5f5f5",
            }
        else:
            return {
                "border": "#707070",
                "fill": "#ffffff",
                "check": "#111111",
                "dot": "#111111",
            }

    def checkbox(self, checked: bool):
        key = ("cb", checked, self.osname, self.dark)
        if key in self.cache:
            return self.cache[key]
        if not self.has_pil:
            self.cache[key] = None
            return None
        size = 16
        pad = 1
        use_circle = self.osname == "Darwin"
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        c = self._colors()
        if use_circle:
            d.ellipse([pad, pad, size - pad, size - pad], fill=c["fill"], outline=c["border"], width=1)
        else:
            d.rectangle([pad, pad, size - pad, size - pad], fill=c["fill"], outline=c["border"], width=1)
        if checked:
            d.line([4, 9, 7, 12, 12, 4], fill=c["check"], width=2)
        self.cache[key] = ImageTk.PhotoImage(img)
        return self.cache[key]

    def radio(self, selected: bool):
        key = ("rb", selected, self.osname, self.dark)
        if key in self.cache:
            return self.cache[key]
        if not self.has_pil:
            self.cache[key] = None
            return None
        size = 16
        pad = 1
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        c = self._colors()
        d.ellipse([pad, pad, size - pad, size - pad], fill=c["fill"], outline=c["border"], width=1)
        if selected:
            d.ellipse([5, 5, size - 5, size - 5], fill=c["dot"])
        self.cache[key] = ImageTk.PhotoImage(img)
        return self.cache[key]

class ImgCheckbox(ttk.Frame):
    def __init__(self, master, text, variable: tk.BooleanVar, assets: ImgAssets, **kwargs):
        super().__init__(master, **kwargs)
        self.assets = assets
        self.variable = variable
        self.variable.set(bool(self.variable.get()))
        self.img_label = tk.Label(self, bd=0, highlightthickness=0)
        self.text_label = ttk.Label(self, text=text)
        self.img_label.pack(side="left")
        self.text_label.pack(side="left", padx=(6, 0))
        self._sync_image()
        self.img_label.bind("<Button-1>", self._toggle)
        self.text_label.bind("<Button-1>", self._toggle)
        self.bind("<Button-1>", self._toggle)

    def _toggle(self, *_):
        self.variable.set(not self.variable.get())
        self._sync_image()

    def _sync_image(self):
        checked = bool(self.variable.get())
        img = self.assets.checkbox(checked)
        if img is not None:
            self.img_label.configure(image=img)
            self.img_label.image = img
        else:
            prefix = "[x]" if checked else "[ ]"
            base = self.text_label.cget("text")
            if not base.startswith("["):
                self.text_label.configure(text=f"{prefix} {base}")
            else:
                self.text_label.configure(text=f"{prefix} {base[4:]}")

    def set_text(self, text):
        self.text_label.configure(text=text)

class ImgRadio(ttk.Frame):
    def __init__(self, master, text, variable: tk.StringVar, value: str, assets: ImgAssets, **kwargs):
        super().__init__(master, **kwargs)
        self.assets = assets
        self.variable = variable
        self.value = value
        self._disabled = False
        self.img_label = tk.Label(self, bd=0, highlightthickness=0)
        self.text_label = ttk.Label(self, text=text)
        self.img_label.pack(side="left")
        self.text_label.pack(side="left", padx=(6, 0))
        self._sync_image()
        self.img_label.bind("<Button-1>", self._select)
        self.text_label.bind("<Button-1>", self._select)
        self.bind("<Button-1>", self._select)
        self.variable.trace_add("write", lambda *_: self._sync_image())

    def configure(self, **kwargs):
        """Configure widget, including support for state='disabled'."""
        if "state" in kwargs:
            self._disabled = (kwargs["state"] == "disabled")
            self._apply_disabled_style()
            del kwargs["state"]
        super().configure(**kwargs)

    def _apply_disabled_style(self):
        """Apply visual styling for disabled state."""
        if self._disabled:
            self.text_label.configure(foreground="gray")
            self.img_label.configure(cursor="arrow")
            self.text_label.configure(cursor="arrow")
            self.configure(cursor="arrow")
        else:
            self.text_label.configure(foreground="")
            self.img_label.configure(cursor="hand2")
            self.text_label.configure(cursor="hand2")
            self.configure(cursor="hand2")

    def _select(self, *_):
        if self._disabled:
            return
        self.variable.set(self.value)
        self._sync_image()

    def _sync_image(self):
        selected = self.variable.get() == self.value
        img = self.assets.radio(selected)
        if img is not None:
            self.img_label.configure(image=img)
            self.img_label.image = img
            # Apply opacity effect for disabled state if needed
            if self._disabled:
                self.img_label.configure(state="disabled")
