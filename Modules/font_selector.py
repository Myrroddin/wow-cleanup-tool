"""
Font selector module for WoW Cleanup Tool.

Provides an incremental-loading, searchable font selector dialog.
The selector displays fonts in their own style, with confirmation
before applying changes.
"""

import tkinter as tk
from tkinter import ttk, messagebox

def open_font_selector(app):
    """Open a searchable Toplevel that lists font families styled in their own font.

    Selecting a font previews it immediately. The user must Apply to persist
    the change, or Cancel to revert to the previous font.
    
    Uses incremental loading: displays fonts in batches as the user scrolls,
    improving performance on systems with large font catalogs.
    
    Args:
        app: The WoWCleanupTool instance with font_families, font_family_var, etc.
    """
    # If already open, bring to front
    if app._font_selector:
        try:
            app._font_selector.deiconify(); app._font_selector.lift()
        except Exception:
            pass
        return

    prev_family = app.font_family_var.get()
    app._prev_font_family = prev_family

    sel = tk.Toplevel(app.root)
    sel.title("Select Font")
    sel.transient(app.root)
    sel.grab_set()
    sel.geometry("+%d+%d" % (app.root.winfo_rootx() + 60, app.root.winfo_rooty() + 60))
    app._font_selector = sel

    filter_var = tk.StringVar()

    entry = ttk.Entry(sel, textvariable=filter_var)
    entry.pack(fill="x", padx=8, pady=(8,4))
    entry.focus_set()

    # Scrollable canvas to host styled Labels (each label can have its own font)
    canvas_frame = ttk.Frame(sel)
    canvas_frame.pack(fill="both", expand=True, padx=8, pady=(0,8))
    canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
    scroll_y = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    inner = ttk.Frame(canvas)
    inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)
    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    def _on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner.bind("<Configure>", _on_configure)

    # Incremental loading state
    app._font_label_widgets = []
    _load_state = {
        "filtered_fonts": [],
        "loaded_count": 0,
        "batch_size": 30,
        "after_id": None,
    }

    def get_filtered_fonts(filter_text=""):
        """Return list of fonts matching the filter."""
        pattern = filter_text.lower()
        result = []
        for fam in app.font_families:
            if pattern and pattern not in fam.lower():
                continue
            result.append(fam)
        return result

    def load_batch():
        """Load the next batch of fonts into the list."""
        state = _load_state
        if state["loaded_count"] >= len(state["filtered_fonts"]):
            return  # All loaded
        
        size = max(8, min(28, int(app.font_size_var.get())))
        batch_end = min(state["loaded_count"] + state["batch_size"], len(state["filtered_fonts"]))
        
        for i in range(state["loaded_count"], batch_end):
            fam = state["filtered_fonts"][i]
            try:
                lbl = tk.Label(inner, text=fam, anchor="w", font=(fam, size))
                lbl.pack(fill="x", anchor="w", padx=2, pady=1)
                lbl._family = fam
                def _on_click(event, f=fam):
                    try:
                        apply_font_preview(app, f)
                    except Exception:
                        pass
                lbl.bind("<Button-1>", _on_click)
                # Hover feedback
                lbl.bind("<Enter>", lambda e, l=lbl: l.configure(bg="#e6f2ff"))
                lbl.bind("<Leave>", lambda e, l=lbl: l.configure(bg=sel.cget("bg")))
                app._font_label_widgets.append(lbl)
            except Exception:
                # Skip fonts that raise errors when applied
                pass
        
        state["loaded_count"] = batch_end

    def on_scroll(*args):
        """Detect when user scrolls near the bottom and load more fonts."""
        state = _load_state
        if state["loaded_count"] >= len(state["filtered_fonts"]):
            return  # All already loaded
        
        # Cancel any pending load to avoid spamming
        if state["after_id"]:
            try:
                app.root.after_cancel(state["after_id"])
            except Exception:
                pass
        
        # Schedule load on next idle (debounce)
        state["after_id"] = app.root.after(100, load_batch)

    def populate(filter_text=""):
        """Clear list and prepare filtered fonts for incremental loading."""
        state = _load_state
        # Cancel any pending load
        if state["after_id"]:
            try:
                app.root.after_cancel(state["after_id"])
            except Exception:
                pass
        
        # Clear display
        for w in inner.winfo_children():
            w.destroy()
        app._font_label_widgets.clear()
        
        # Prepare filtered list
        state["filtered_fonts"] = get_filtered_fonts(filter_text)
        state["loaded_count"] = 0
        
        # Load first batch immediately
        load_batch()

    populate()

    def on_filter_change(*_):
        populate(filter_var.get())

    filter_var.trace_add("write", on_filter_change)
    
    # Detect scroll to load more fonts incrementally
    canvas.bind("<MouseWheel>", on_scroll)
    canvas.bind("<Button-4>", on_scroll)
    canvas.bind("<Button-5>", on_scroll)

    # Buttons
    btn_frame = ttk.Frame(sel)
    btn_frame.pack(fill="x", padx=8, pady=(0,8))
    apply_btn = ttk.Button(btn_frame, text="Apply", command=lambda: finalize_font_change(app))
    apply_btn.pack(side="right", padx=(4,0))
    cancel_btn = ttk.Button(btn_frame, text="Cancel", command=lambda: cancel_font_change(app))
    cancel_btn.pack(side="right")

    def on_close_sel():
        cancel_font_change(app)

    sel.protocol("WM_DELETE_WINDOW", on_close_sel)

def apply_font_preview(app, family: str):
    """Temporarily apply a font family to the UI for previewing.
    
    Args:
        app: The WoWCleanupTool instance
        family: Font family name to preview
    """
    try:
        if not family:
            return
        app.font_family_var.set(family)
        try:
            app.default_font.configure(family=family)
        except Exception:
            pass
        try:
            app.root.option_add("*Font", app.default_font)
        except Exception:
            pass
        # Update the font button to show preview
        try:
            app.font_button.configure(font=(family, app.font_size_var.get()))
        except Exception:
            pass
        # Track currently previewed family
        app._previewed_family = family
    except Exception:
        pass

def finalize_font_change(app):
    """Ask user to confirm the previewed font; save or revert accordingly.
    
    Args:
        app: The WoWCleanupTool instance
    """
    try:
        new = getattr(app, "_previewed_family", app.font_family_var.get())
        old = getattr(app, "_prev_font_family", None)
        if new == old:
            # Nothing changed
            try:
                if app._font_selector:
                    app._font_selector.grab_release(); app._font_selector.destroy()
            except Exception:
                pass
            app._font_selector = None
            return

        ok = messagebox.askyesno("Confirm Font", f"Apply font '{new}' to the application?")
        if ok:
            try:
                app.settings["font_family"] = new
                from Modules.settings import save_settings
                save_settings(app.settings)
            except Exception:
                pass
            try:
                if app._font_selector:
                    app._font_selector.grab_release(); app._font_selector.destroy()
            except Exception:
                pass
            app._font_selector = None
            app._prev_font_family = new
        else:
            # Revert
            try:
                if old:
                    app.default_font.configure(family=old)
                    app.root.option_add("*Font", app.default_font)
                    app.font_family_var.set(old)
                    try:
                        app.font_button.configure(font=(old, app.font_size_var.get()))
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                if app._font_selector:
                    app._font_selector.grab_release(); app._font_selector.destroy()
            except Exception:
                pass
            app._font_selector = None
    except Exception:
        pass

def cancel_font_change(app):
    """Cancel selector and revert any previewed font back to previous.
    
    Args:
        app: The WoWCleanupTool instance
    """
    try:
        prev = getattr(app, "_prev_font_family", None)
        if prev:
            try:
                app.default_font.configure(family=prev)
                app.root.option_add("*Font", app.default_font)
                app.font_family_var.set(prev)
                try:
                    app.font_button.configure(font=(prev, app.font_size_var.get()))
                except Exception:
                    pass
            except Exception:
                pass
    except Exception:
        pass
    try:
        if app._font_selector:
            app._font_selector.grab_release(); app._font_selector.destroy()
    except Exception:
        pass
    app._font_selector = None
