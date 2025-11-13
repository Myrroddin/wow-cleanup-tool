#!/usr/bin/env python3
"""
World of Warcraft Maintenance Tool v1.0.0
"""

import os
import sys
import json
import shutil
import site
import importlib
import subprocess
import platform
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
from Modules.file_cleaner import find_bak_old_files, delete_files
from Modules.themes import apply_theme
from Modules.orphan_cleaner import (
    scan_orphans,
    delete_orphans,
    rebuild_addons_txt,
    collect_addon_names,
    HAS_TRASH
)
from Modules.folder_cleaner import (
    scan_all_versions,
    clean_folders,
    HAS_TRASH as FOLDER_HAS_TRASH
)

VERSION = "v1.0.0"

# -------------------- Silent package ensure --------------------
def ensure_package(module_name: str, pip_name: str):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        try:
            with open(os.devnull, "w") as devnull:
                subprocess.call(
                    [sys.executable, "-m", "pip", "install", "--user", "--quiet", "--no-warn-script-location", pip_name],
                    stdout=devnull, stderr=devnull
                )
            importlib.reload(site)
            return importlib.import_module(module_name)
        except Exception:
            return None

_send2trash_mod = ensure_package("send2trash", "send2trash")
if _send2trash_mod:
    from send2trash import send2trash
    HAS_TRASH = True
else:
    HAS_TRASH = False

_pil = ensure_package("PIL", "Pillow")
if _pil:
    from PIL import Image, ImageTk, ImageDraw
else:
    Image = ImageTk = ImageDraw = None

# -------------------- Settings helpers --------------------
def get_settings_path():
    home = os.path.expanduser("~")
    cfg = os.path.join(home, ".wow_cleanup_tool")
    os.makedirs(cfg, exist_ok=True)
    return os.path.join(cfg, "settings.json")

SETTINGS_FILE = get_settings_path()

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
    except Exception:
        pass

# -------------------- Tooltip --------------------
class Tooltip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip = None
        self.after_id = None
        widget.bind("<Enter>", self.on_enter, add="+")
        widget.bind("<Leave>", self.on_leave, add="+")
        widget.bind("<ButtonPress>", self.on_leave, add="+")
    def on_enter(self, _=None):
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
        lbl = tk.Label(tw, text=self.text, bg="#ffffe0", fg="black", relief="solid", bd=1, padx=6, pady=3, justify="left", wraplength=300)
        lbl.pack()
        self.tip = tw
    def hide(self):
        if self.tip:
            try: self.tip.destroy()
            except Exception: pass
            self.tip = None

# -------------------- Custom OS-aware checkbox / radio widgets --------------------
class ImgAssets:
    def __init__(self, osname: str, dark: bool):
        self.osname = osname
        self.dark = dark
        self.has_pil = bool(Image and ImageDraw and ImageTk)
        self.cache = {}

    def _colors(self):
        if self.dark:
            return {"border":"#b0b0b0","fill":"#3a3a3a","check":"#f5f5f5","dot":"#f5f5f5"}
        else:
            return {"border":"#707070","fill":"#ffffff","check":"#111111","dot":"#111111"}

    def checkbox(self, checked: bool):
        key = ("cb", checked, self.osname, self.dark)
        if key in self.cache: return self.cache[key]
        if not self.has_pil:
            self.cache[key] = None
            return None
        size = 16; pad = 1
        use_circle = (self.osname == "Darwin")
        img = Image.new("RGBA", (size, size), (0,0,0,0))
        d = ImageDraw.Draw(img)
        c = self._colors()
        if use_circle:
            d.ellipse([pad, pad, size-pad, size-pad], fill=c["fill"], outline=c["border"], width=1)
        else:
            d.rectangle([pad, pad, size-pad, size-pad], fill=c["fill"], outline=c["border"], width=1)
        if checked:
            d.line([4, 9, 7, 12, 12, 4], fill=c["check"], width=2)
        self.cache[key] = ImageTk.PhotoImage(img)
        return self.cache[key]

    def radio(self, selected: bool):
        key = ("rb", selected, self.osname, self.dark)
        if key in self.cache: return self.cache[key]
        if not self.has_pil:
            self.cache[key] = None
            return None
        size = 16; pad = 1
        img = Image.new("RGBA", (size, size), (0,0,0,0))
        d = ImageDraw.Draw(img)
        c = self._colors()
        d.ellipse([pad, pad, size-pad, size-pad], fill=c["fill"], outline=c["border"], width=1)
        if selected:
            d.ellipse([5,5, size-5, size-5], fill=c["dot"])
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
        self.text_label.pack(side="left", padx=(6,0))
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
            base = self.text_label.cget('text')
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
        self.img_label = tk.Label(self, bd=0, highlightthickness=0)
        self.text_label = ttk.Label(self, text=text)
        self.img_label.pack(side="left")
        self.text_label.pack(side="left", padx=(6,0))
        self._sync_image()
        self.img_label.bind("<Button-1>", self._select)
        self.text_label.bind("<Button-1>", self._select)
        self.bind("<Button-1>", self._select)
        self.variable.trace_add("write", lambda *_: self._sync_image())

    def _select(self, *_):
        self.variable.set(self.value)
        self._sync_image()

    def _sync_image(self):
        selected = (self.variable.get() == self.value)
        img = self.assets.radio(selected)
        if img is not None:
            self.img_label.configure(image=img)
            self.img_label.image = img

# -------------------- Main App --------------------
class WoWMaintenanceTool:
    MIN_W = 760
    MIN_H = 540

    VERSION_FOLDERS = [
        ("_classic_era_", "Classic Era"),
        ("_classic_", "Classic"),
        ("_retail_", "Retail"),
    ]
    VARIANT_SUFFIXES = [
        ("_ptr_", " PTR"),
        ("_beta_", " Beta"),
    ]

    def __init__(self, root):
        self.root = root
        self.settings = load_settings()
        self.log_lines = []

        # Base path for theme assets
        self.app_path = os.path.dirname(os.path.abspath(__file__))

        # OS theme baseline
        self.style = ttk.Style()
        self._apply_os_base_theme()

        # Fonts
        self.default_font = tkfont.nametofont("TkDefaultFont")
        start_size = int(self.settings.get("font_size", self.default_font.cget("size")))
        start_size = min(max(start_size, 6), 16)
        self.font_size_var = tk.IntVar(value=start_size)
        self.default_font.configure(size=self.font_size_var.get())
        self.root.option_add("*Font", self.default_font)

        # State
        self.wow_path_var = tk.StringVar(value=self.settings.get("wow_path", ""))
        self.delete_mode = tk.StringVar(value=self.settings.get("delete_mode", "delete"))
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "light"))
        self.verbose_var = tk.BooleanVar(value=bool(self.settings.get("verbose_logging", False)))

        self.root.title(f"World of Warcraft Maintenance Tool {VERSION}")
        self.setup_geometry()
        self._rebuild_assets()
        self.build_ui()
        self._apply_theme()   # ← apply after widgets exist

        self.root.bind("<Configure>", self._on_configure, add="+")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(200, self.show_startup_warning)
        self.log(f"Session started — {VERSION} (Harmony)")

    # -------- Verbose logging helper --------
    def vlog(self, text):
        if self.verbose_var.get():
            self.log(text)

    # ------------- OS base theme -------------
    def _apply_os_base_theme(self):
        osname = platform.system()
        try:
            if osname == "Windows" and "vista" in self.style.theme_names():
                self.style.theme_use("vista")
            elif osname == "Darwin" and "aqua" in self.style.theme_names():
                self.style.theme_use("aqua")
            else:
                self.style.theme_use("clam")
        except Exception:
            self.style.theme_use("clam")

    # ------------- Geometry -------------
    def setup_geometry(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w = self.settings.get("window_width")
        h = self.settings.get("window_height")
        x = self.settings.get("window_x")
        y = self.settings.get("window_y")
        is_max = self.settings.get("is_maximized", False)
        if all(val is not None for val in (w, h, x, y)):
            try:
                w = max(int(w), self.MIN_W); h = max(int(h), self.MIN_H)
                x = int(x); y = int(y)
                x, y = self._keep_on_screen(x, y, w, h, sw, sh)
                self.root.geometry(f"{w}x{h}+{x}+{y}")
            except Exception:
                self._center_first_launch(sw, sh)
        else:
            self._center_first_launch(sw, sh)
        self.root.minsize(self.MIN_W, self.MIN_H)
        if is_max:
            try: self.root.state("zoomed")
            except Exception: pass

    def _center_first_launch(self, sw, sh):
        if sw >= 3840:
            w = max(int(sw * 0.25), self.MIN_W)
            h = max(int(sh * 0.25), self.MIN_H)
        else:
            w = max(int(sw * 0.58), self.MIN_W)
            h = max(int(sh * 0.6), self.MIN_H)
        x = (sw // 2) - (w // 2); y = (sh // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _parse_geometry(self, geometry):
        try:
            size, pos = geometry.split("+", 1)
            w_str, h_str = size.split("x")
            x_str, y_str = pos.split("+")
            return int(w_str), int(h_str), int(x_str), int(y_str)
        except Exception:
            return None

    def _keep_on_screen(self, x, y, w, h, sw, sh):
        margin = 40
        if x + w < margin: x = margin
        if x > sw - margin: x = max(0, sw - w - margin)
        if y + h < margin: y = margin
        if y > sh - margin: y = max(0, sh - h - margin)
        x = max(0, min(x, max(0, sw - 50)))
        y = max(0, min(y, max(0, sh - 50)))
        return x, y

    def _on_configure(self, event):
        try:
            if self.root.state() == "zoomed":
                return
        except Exception:
            pass
        parsed = self._parse_geometry(self.root.geometry())
        if not parsed: return
        w, h, x, y = parsed
        sw = self.root.winfo_screenwidth(); sh = self.root.winfo_screenheight()
        nx, ny = self._keep_on_screen(x, y, w, h, sw, sh)
        if (nx, ny) != (x, y):
            self.root.geometry(f"{w}x{h}+{nx}+{ny}")

    # ------------- Theme -------------
    def _apply_theme(self):
        theme = self.theme_var.get().lower()

        checkbox_on, checkbox_off = apply_theme(
            root=self.root,
            treeviews=[self.file_tree, self.orphan_tree],
            theme_name=theme,
            base_path=self.app_path,
        )

        # Save icons for custom checkboxes
        self.checkbox_on_img = checkbox_on
        self.checkbox_off_img = checkbox_off

        # Update all custom checkboxes (you already have mapping dicts)
        self._reload_all_custom_checkboxes()

        # Recolor status bars if you have them
        if hasattr(self, "file_scan_status"):
            self.file_scan_status.configure(bg=self.root["bg"], fg=self.theme_fg)
        if hasattr(self, "orphan_scan_status"):
            self.orphan_scan_status.configure(bg=self.root["bg"], fg=self.theme_fg)

    def _rebuild_assets(self):
        osname = platform.system()
        dark = (self.theme_var.get() == "dark")
        self.assets = ImgAssets(osname=osname, dark=dark)

    def _set_options_border(self, show_dark_border: bool):
        if hasattr(self, "options_border"):
            try:
                self.options_border.configure(bg="#b0b0b0" if show_dark_border else self.root.cget("bg"))
            except Exception:
                pass

    def update_font_size(self):
        size = min(max(int(self.font_size_var.get()), 6), 16)
        self.font_size_var.set(size)
        self.default_font.configure(size=size)
        self.settings["font_size"] = size
        save_settings(self.settings)

    # ------------- UI Build -------------
    def build_ui(self):
        # Options with subtle border
        self.options_border = tk.Frame(self.root, bg=self.root.cget("bg"))
        self.options_border.pack(fill="x", padx=10, pady=(10, 8))
        options = ttk.LabelFrame(self.options_border, text="Options", padding=8)
        options.pack(fill="x", padx=1, pady=1)

        # Row 0: Label | Entry (half) | Browse | Font size | Theme
        ttk.Label(options, text="World of Warcraft Folder:").grid(row=0, column=0, sticky="w", padx=(0,6), pady=4)

        self.folder_entry = ttk.Entry(options, textvariable=self.wow_path_var, width=42)
        self.folder_entry.grid(row=0, column=1, sticky="we", padx=(0,6), pady=4)

        folder_btn = ttk.Button(options, text="Browse...", command=self.select_wow_folder)
        folder_btn.grid(row=0, column=2, sticky="w", padx=(0,10), pady=4)
        Tooltip(folder_btn, "Browse for your World of Warcraft folder.")

        ttk.Label(options, text="Font Size:").grid(row=0, column=3, sticky="e", padx=(0,6), pady=4)
        font_spin = ttk.Spinbox(options, from_=6, to=16, textvariable=self.font_size_var, width=5, command=self.update_font_size)
        font_spin.grid(row=0, column=4, sticky="w", padx=(0,10), pady=4)

        ttk.Label(options, text="Theme:").grid(row=0, column=5, sticky="e", padx=(0,6), pady=4)
        theme_combo = ttk.Combobox(options, textvariable=self.theme_var, values=["light", "dark"], state="readonly", width=10)
        theme_combo.grid(row=0, column=6, sticky="w", padx=(0,0), pady=4)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_theme())

        options.columnconfigure(1, weight=1)   # Entry stretches

        # Row 1: File Action label | Delete | Trash | Verbose | Restore
        mode_frame = ttk.Frame(options)
        mode_frame.grid(row=1, column=0, columnspan=7, sticky="we", pady=(2, 2))
        mode_frame.columnconfigure(10, weight=1)

        ttk.Label(mode_frame, text="File Action:").grid(row=0, column=0, sticky="w", padx=(0,8))

        self.radio_container = ttk.Frame(mode_frame)
        self.radio_container.grid(row=0, column=1, sticky="w")

        self.rb_delete = ImgRadio(self.radio_container, "Delete Permanently", self.delete_mode, "delete", self.assets)
        self.rb_trash  = ImgRadio(self.radio_container, "Move to Recycle Bin", self.delete_mode, "trash", self.assets)
        self.rb_delete.pack(side="left", padx=(0,14))
        self.rb_trash.pack(side="left", padx=(0,14))

        self.verbose_cb = ImgCheckbox(mode_frame, "Enable verbose logging", self.verbose_var, self.assets)
        self.verbose_cb.grid(row=0, column=2, sticky="w", padx=(10,0))
        Tooltip(self.verbose_cb, "When enabled, Log captures every processed file/folder/AddOns.txt line.")

        restore_btn = ttk.Button(mode_frame, text="Restore Defaults", command=self.restore_defaults)
        restore_btn.grid(row=0, column=9, sticky="e", padx=(10,0))

        # Main notebook
        self.main_notebook = ttk.Notebook(self.root)
        self.main_notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.main_notebook.configure(padding=(4, 0))

        # File Cleaner
        self.cleaner_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.cleaner_tab, text="File Cleaner")
        self.build_file_cleaner_tree(self.cleaner_tab)

        # Folder Cleaner
        self.folder_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.folder_tab, text="Folder Cleaner")
        self.build_folder_cleaner_tab(self.folder_tab)

        # Orphan Remover
        self.orphan_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.orphan_tab, text="Orphan Remover")
        self.build_orphan_remover_tab(self.orphan_tab)

        # Log
        self.log_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.log_tab, text="Log")
        self.build_log_tab(self.log_tab)

        # Help
        self.help_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.help_tab, text="Help / About")
        self.build_help_tab(self.help_tab)

        self._set_options_border(self.theme_var.get() == "dark")

    # track styled widgets for refresh (theme switch)
    def _refresh_styled_checkables(self):
        if hasattr(self, "rb_delete"):
            self.rb_delete.assets = self.assets; self.rb_delete._sync_image()
        if hasattr(self, "rb_trash"):
            self.rb_trash.assets = self.assets; self.rb_trash._sync_image()
        if hasattr(self, "styled_folder_boxes"):
            for cb in self.styled_folder_boxes:
                cb.assets = self.assets; cb._sync_image()
        if hasattr(self, "styled_shot_boxes"):
            for cb in self.styled_shot_boxes:
                cb.assets = self.assets; cb._sync_image()
        if hasattr(self, "_build_checkbox_images"):
            self._build_checkbox_images()
            if hasattr(self, "file_tree"):
                for iid in list(getattr(self, "tree_checks", {}).keys()):
                    self._tree_set_icon(iid)
            if hasattr(self, "orphan_tree"):
                for iid in list(getattr(self, "orphan_checks", {}).keys()):
                    self._orphan_tree_set_icon(iid)

    def _reload_all_custom_checkboxes(self):
        """
        Called after theme changes.
        Replaces checkbox images in file/orphan/folder cleaners.
        """

        # File Cleaner
        for iid, var in self.tree_checks.items():
            img = self.checkbox_on_img if var.get() else self.checkbox_off_img
            self.file_tree.item(iid, image=img)

        # Orphan Cleaner
        for iid, var in self.orphan_checks.items():
            img = self.checkbox_on_img if var.get() else self.checkbox_off_img
            self.orphan_tree.item(iid, image=img)

        # Folder cleaner uses per-version custom widgets,
        # so we only recolor frames/buttons normally.
        # No TreeView here.

    # ----------------- Common helpers -----------------
    def _enumerate_versions(self, base):
        versions = []
        for folder, label in self.VERSION_FOLDERS:
            vpath = os.path.join(base, folder)
            if os.path.isdir(vpath):
                versions.append((vpath, label))
            for suf, suffix_label in self.VARIANT_SUFFIXES:
                variant_folder = folder[:-1] + suf[1:]
                v2 = os.path.join(base, variant_folder)
                if os.path.isdir(v2):
                    versions.append((v2, label + suffix_label))
        return versions

    def _collect_addon_names(self, addons_dir):
        names = set()
        if os.path.isdir(addons_dir):
            try:
                for name in os.listdir(addons_dir):
                    p = os.path.join(addons_dir, name)
                    if os.path.isdir(p) and not name.lower().startswith("blizzard_"):
                        names.add(name.casefold())
            except Exception:
                pass
        return names

    def _iter_savedvariables_dirs(self, account_root):
        if not os.path.isdir(account_root):
            return
        acc_sv = os.path.join(account_root, "SavedVariables")
        if os.path.isdir(acc_sv):
            yield acc_sv
        try:
            for realm in os.listdir(account_root):
                realm_path = os.path.join(account_root, realm)
                if not os.path.isdir(realm_path) or realm.upper() == "SAVEDVARIABLES":
                    continue
                realm_sv = os.path.join(realm_path, "SavedVariables")
                if os.path.isdir(realm_sv):
                    yield realm_sv
                try:
                    for char in os.listdir(realm_path):
                        char_path = os.path.join(realm_path, char)
                        if not os.path.isdir(char_path) or char.upper() == "SAVEDVARIABLES":
                            continue
                        char_sv = os.path.join(char_path, "SavedVariables")
                        if os.path.isdir(char_sv):
                            yield char_sv
                except Exception:
                    pass
        except Exception:
            pass

    def _savedvar_basename(self, filename):
        fn = filename
        if fn.lower().endswith(".lua.bak"):
            fn = fn[:-8]
        elif fn.lower().endswith(".lua"):
            fn = fn[:-4]
        if fn.lower().endswith(".bak"):
            fn = fn[:-4]
        return fn

    # ------------- File Cleaner (Tree) -------------
    def _build_checkbox_images(self):
        self.chk_unchecked = self.assets.checkbox(False)
        self.chk_checked = self.assets.checkbox(True)

    def build_file_cleaner_tree(self, parent):
        bar = ttk.Frame(parent, padding=10)
        bar.pack(fill="x")
        ttk.Button(bar, text="Scan for .bak / .old Files", command=self.scan_files_tree).pack(side="left")
        ttk.Button(bar, text="Expand All", command=self._tree_expand_all).pack(side="left", padx=(8,0))
        ttk.Button(bar, text="Collapse All", command=self._tree_collapse_all).pack(side="left", padx=(8,0))
        self.tree_select_all_var = tk.BooleanVar(value=False)
        self.tree_selall_frame = ImgCheckbox(bar, "Select / Deselect All", self.tree_select_all_var, self.assets)
        self.tree_selall_frame.pack(side="left", padx=(12,0))
        self.tree_select_all_var.trace_add("write", lambda *_: self._tree_toggle_all())
        ttk.Button(bar, text="Process Selected Files", command=self.process_selected_files_tree)\
            .pack(side="left", padx=(8, 0))
        self.file_scan_status = ttk.Label(bar, text="")
        self.file_scan_status.pack(side="left", padx=(10, 0))

        tree_frame = ttk.Frame(parent, padding=(10, 10))
        tree_frame.pack(fill="both", expand=True)
        self.file_tree = ttk.Treeview(tree_frame, columns=("path",), show="tree", selectmode="none")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=vsb.set)
        self.file_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._build_checkbox_images()
        self.tree_checks = {}
        self.tree_paths = {}
        self.file_tree.bind("<Button-1>", self._on_tree_click)

    def _tree_add_parent(self, label):
        pid = self.file_tree.insert("", "end", text=f"  {label}", open=False)
        self.tree_checks[pid] = False
        self._tree_set_icon(pid)
        return pid

    def _tree_add_child_file(self, parent_id, path):
        basename = os.path.basename(path)
        iid = self.file_tree.insert(parent_id, "end", text=f"  {basename}", open=False)
        self.tree_checks[iid] = False
        self.tree_paths[iid] = path
        self._tree_set_icon(iid)
        return iid

    def _tree_set_icon(self, iid):
        if self.chk_unchecked:
            img = self.chk_checked if self.tree_checks.get(iid, False) else self.chk_unchecked
            self.file_tree.item(iid, image=img)
        else:
            checked = self.tree_checks.get(iid, False)
            text = self.file_tree.item(iid, "text")
            prefix = "[x]" if checked else "[ ]"
            if not text.strip().startswith("["):
                self.file_tree.item(iid, text=f"{prefix} {text.strip()}")
            else:
                self.file_tree.item(iid, text=f"{prefix} {text.strip()[3:].strip()}")

    def _on_tree_click(self, event):
        elem = self.file_tree.identify("element", event.x, event.y)
        if elem in ("Treeitem.indicator", "treeitem.indicator", "indicator"):
            # only expand/collapse
            return
        iid = self.file_tree.identify_row(event.y)
        if not iid:
            return
        # toggling selection
        if iid not in self.tree_paths:
            new_state = not self.tree_checks.get(iid, False)
            self.tree_checks[iid] = new_state
            for child in self.file_tree.get_children(iid):
                self.tree_checks[child] = new_state
                self._tree_set_icon(child)
            self._tree_set_icon(iid)
        else:
            self.tree_checks[iid] = not self.tree_checks.get(iid, False)
            self._tree_set_icon(iid)
        return "break"

    def _tree_toggle_all(self):
        new_state = self.tree_select_all_var.get()
        for iid in self.file_tree.get_children(""):
            self.tree_checks[iid] = new_state
            self._tree_set_icon(iid)
            for child in self.file_tree.get_children(iid):
                self.tree_checks[child] = new_state
                self._tree_set_icon(child)

    def _tree_expand_all(self):
        for iid in self.file_tree.get_children(""):
            self.file_tree.item(iid, open=True)

    def _tree_collapse_all(self):
        for iid in self.file_tree.get_children(""):
            self.file_tree.item(iid, open=False)

    def scan_files_tree(self):
        # Clear old tree
        for n in self.file_tree.get_children(""):
            self.file_tree.delete(n)
        self.tree_checks.clear()
        self.tree_paths.clear()
        self.tree_select_all_var.set(False)

        base = self.wow_path_var.get().strip()
        if not base or not os.path.isdir(base):
            messagebox.showerror("Invalid Folder", "Please select a valid WoW folder first.")
            return

        # Back-end: compute which files exist per version
        versions = self._enumerate_versions(base)
        files_by_version = find_bak_old_files(
            versions,
            logger=self if self.verbose_var.get() else None,
        )

        total = 0
        # Rebuild treeview using the backend results
        for vpath, vlabel in versions:
            # Only create a parent if we have files for this version
            v_files = files_by_version.get(vlabel, [])
            if not v_files:
                continue
            pid = self._tree_add_parent(vlabel)
            for fpath in v_files:
                self._tree_add_child_file(pid, fpath)
                total += 1
            self.file_tree.item(pid, open=False)

        if total:
            self.file_scan_status.configure(text=f"Found {total} file(s) across versions.")
        else:
            self.file_scan_status.configure(text="No .bak or .old files found.")

        self.log(f"File Cleaner scan: {total} match(es).")

    def process_selected_files_tree(self):
        selected = [
            path
            for iid, path in self.tree_paths.items()
            if self.tree_checks.get(iid, False)
        ]
        if not selected:
            messagebox.showinfo("No Selection", "No files selected for processing.")
            return

        use_trash_requested = (self.delete_mode.get() == "trash")
        action = (
            "move to Recycle Bin/Trash"
            if use_trash_requested and HAS_TRASH
            else "delete permanently"
        )

        if not messagebox.askyesno(
            "Confirm",
            f"Are you sure you want to {action} {len(selected)} file(s)?"
        ):
            return

        # Back-end deletion
        processed, permanently_deleted, used_trash = delete_files(
            selected,
            use_trash=use_trash_requested and HAS_TRASH,
            logger=self if self.verbose_var.get() else None,
        )

        # Handle the case where trash was requested but isn't available
        if use_trash_requested and not HAS_TRASH:
            messagebox.showwarning(
                "send2trash missing",
                "The 'send2trash' module is unavailable. Files were deleted permanently."
            )
            self.log("Warning: send2trash not installed; deletions were permanent.")

        self.log(f"File Cleaner: processed {processed} file(s).")
        messagebox.showinfo("Completed", f"Processed {processed} file(s).")

        # Refresh the tree to reflect deletions
        self.scan_files_tree()

    # ------------- Folder Cleaner -------------
    def build_folder_cleaner_tab(self, parent):
        self.version_notebook = ttk.Notebook(parent)
        self.version_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        base = self.wow_path_var.get().strip()
        self.version_tabs = []
        if base and os.path.isdir(base):
            versions = self._enumerate_versions(base)
            for vpath, vlabel in versions:
                tab = ttk.Frame(self.version_notebook)
                self.version_notebook.add(tab, text=vlabel)
                widgets = self._build_single_version_tab(tab, vpath, vlabel)
                self.version_tabs.append((vlabel, vpath, widgets))
        else:
            info = ttk.Frame(parent, padding=12)
            info.pack(fill="both", expand=True)
            ttk.Label(info, text="Select a valid World of Warcraft folder in Options to enable Folder Cleaner.").pack()

    def _build_single_version_tab(self, tab, version_path, version_label):
        outer = ttk.Frame(tab, padding=10)
        outer.pack(fill="both", expand=True)

        # Controls row: toggles side-by-side + Process button at end
        controls = ttk.Frame(outer)
        controls.pack(fill="x")

        folder_vars = {}
        toggle_container = ttk.Frame(controls)
        toggle_container.pack(side="left", fill="x", expand=True)

        targets = {
            "Screenshots": os.path.join(version_path, "Screenshots"),
            "Logs": os.path.join(version_path, "Logs"),
            "Errors": os.path.join(version_path, "Errors"),
            "Cache": os.path.join(version_path, "Cache"),
        }

        # Master "Select/Deselect All"
        master_var = tk.BooleanVar(value=False)
        master = ImgCheckbox(toggle_container, "Select / Deselect All Folders", master_var, self.assets)
        master.pack(side="left", padx=(0,10), pady=4)
        master_var.trace_add("write", lambda *_: self._toggle_all_folders(folder_vars))

        # Place folder toggles side-by-side (except Screenshots handled below)
        self.styled_folder_boxes = getattr(self, "styled_folder_boxes", [])
        for name, path in targets.items():
            if name == "Screenshots":
                continue
            if os.path.isdir(path):
                var = tk.BooleanVar(value=False)
                cb = ImgCheckbox(toggle_container, f"{name}", var, self.assets)
                cb.pack(side="left", padx=(0,10), pady=4)
                folder_vars[name] = (var, path, cb)
                self.styled_folder_boxes.append(cb)

        # Process button aligned right on same line
        ttk.Button(controls, text="Process Selected Folders",
                   command=lambda: self._process_selected_folders(version_label, folder_vars)).pack(side="right", padx=(10,0), pady=4)

        # Screenshots panel (unchanged)
        shot_panel = ttk.LabelFrame(outer, text="Screenshots (per-file actions)", padding=8)
        shot_panel.pack(fill="both", expand=True, pady=(8, 0))

        shots_left = ttk.Frame(shot_panel); shots_left.pack(side="left", fill="both", expand=True)
        shots_right = ttk.Frame(shot_panel); shots_right.pack(side="left", fill="both", expand=True, padx=(10, 0))

        shots_canvas = tk.Canvas(shots_left)
        shots_scroll = ttk.Scrollbar(shots_left, orient="vertical", command=shots_canvas.yview)
        shots_frame = ttk.Frame(shots_canvas)
        shots_frame.bind("<Configure>", lambda e: shots_canvas.configure(scrollregion=shots_canvas.bbox("all")))
        shots_canvas.create_window((0, 0), window=shots_frame, anchor="nw")
        shots_canvas.configure(yscrollcommand=shots_scroll.set)
        shots_canvas.pack(side="left", fill="both", expand=True)
        shots_scroll.pack(side="right", fill="y")

        shots_controls = ttk.Frame(outer); shots_controls.pack(fill="x", pady=(6, 0))
        shots_select_all_var = tk.BooleanVar(value=False)
        shots_selall = ImgCheckbox(shots_controls, "Select / Deselect All Screenshot Files", shots_select_all_var, self.assets)
        shots_selall.pack(side="left")
        shots_vars = {}
        shots_select_all_var.trace_add("write", lambda *_: self._toggle_all_screenshot_files(shots_vars))

        preview_label = ttk.Label(shots_right, text="Preview", anchor="center"); preview_label.pack(anchor="n")
        preview_canvas = tk.Canvas(shots_right, width=220, height=220, highlightthickness=1)
        preview_canvas.pack(fill="both", expand=False, pady=(6, 0))
        preview_canvas._img_ref = None

        self.styled_shot_boxes = getattr(self, "styled_shot_boxes", [])
        shot_folder = targets.get("Screenshots")
        if shot_folder and os.path.isdir(shot_folder):
            files = []
            try:
                for fname in os.listdir(shot_folder):
                    fp = os.path.join(shot_folder, fname)
                    if os.path.isfile(fp) and fname.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tga", ".gif")):
                        files.append(fp)
            except Exception:
                files = []
            files.sort(key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0, reverse=True)
            for fp in files:
                var = tk.BooleanVar(value=False)
                cb = ImgCheckbox(shots_frame, fp, var, self.assets)
                cb.pack(anchor="w", fill="x", padx=4, pady=1)
                cb.bind("<ButtonRelease-1>", lambda e, p=fp: self._show_preview(preview_canvas, p))
                self.styled_shot_boxes.append(cb)
                shots_vars[fp] = var
        else:
            ttk.Label(shots_frame, text="Screenshots folder not found for this version.").pack(anchor="w")

        return {"folder_vars": folder_vars, "shots_vars": shots_vars, "preview_canvas": preview_canvas}

    def _show_preview(self, canvas: tk.Canvas, path: str):
        if not Image or not ImageTk or not path or not os.path.exists(path):
            canvas.delete("all"); canvas._img_ref = None; return
        try:
            img = Image.open(path)
            canvas.update_idletasks()
            cw = max(200, int(canvas.winfo_width()))
            ch = max(200, int(canvas.winfo_height()))
            img.thumbnail((cw, ch))
            tkimg = ImageTk.PhotoImage(img)
            canvas.delete("all")
            cx, cy = cw // 2, ch // 2
            canvas.create_image(cx, cy, image=tkimg)
            canvas._img_ref = tkimg
        except Exception:
            canvas.delete("all"); canvas._img_ref = None

    def _toggle_all_folders(self, folder_vars):
        any_unchecked = any(not v.get() for v, _, _ in folder_vars.values())
        for var, _, _ in folder_vars.values():
            var.set(any_unchecked)
        for _, _, cb in folder_vars.values():
            cb._sync_image()

    def _process_selected_folders(self, version_label, folder_vars):
        """
        Called by the Folder Cleaner tab's per-version process button.

        version_label: e.g. "Retail", "Classic", etc.
        folder_vars: dict mapping rel_folder_name -> tk.BooleanVar
        """
        # Determine which folders are selected
        selected = [
            abs_path
            for (rel_name, abs_path) in self.folder_paths.get(version_label, {}).items()
            if folder_vars.get(rel_name, False).get()
        ]

        if not selected:
            messagebox.showinfo("No Selection", "No folders were selected for cleanup.")
            return

        use_trash_requested = (self.folder_delete_mode.get() == "trash")
        action = (
            "move to Recycle Bin/Trash"
            if use_trash_requested and FOLDER_HAS_TRASH
            else "delete permanently"
        )

        if not messagebox.askyesno(
            "Confirm",
            f"Are you sure you want to {action} {len(selected)} folder(s)?"
        ):
            return

        processed, permanently_deleted, used_trash = clean_folders(
            selected,
            use_trash=use_trash_requested and FOLDER_HAS_TRASH,
            logger=self if self.verbose_var.get() else None
        )

        if use_trash_requested and not FOLDER_HAS_TRASH:
            messagebox.showwarning(
                "send2trash missing",
                "The 'send2trash' module is unavailable. "
                "Folders were deleted permanently."
            )
            self.log("Warning: send2trash not installed; deletions were permanent.")

        self.log(f"Folder Cleaner: processed {processed} folder(s).")
        messagebox.showinfo("Completed", f"Processed {processed} folder(s).")

        # Rebuild UI for this version tab
        # This calls _build_single_version_tab again to refresh the toggles
        self.refresh_folder_cleaner_version(version_label)

    def refresh_folder_cleaner_version(self, version_label):
        """
        Rebuilds a single Folder Cleaner version tab after cleanup.
        """
        # Find the correct tab frame
        for tab_label, tab_path, widgets in self.version_tabs:
            if tab_label == version_label:
                frame = self.version_notebook.nametowidget(
                    self.version_notebook.select()
                )
                break
        else:
            return  # Version not found (safe fallback)

        # Clear widgets on the tab
        for widget in frame.winfo_children():
            widget.destroy()

        # Rebuild the version tab UI
        for vlabel, vpath, _widgets in self.version_tabs:
            if vlabel == version_label:
                # rebuild the exact tab
                self._build_single_version_tab(frame, vpath, vlabel)
                break

    def _toggle_all_screenshot_files(self, shots_vars):
        any_unchecked = any(not v.get() for v in shots_vars.values())
        for v in shots_vars.values():
            v.set(any_unchecked)

    # ------------- Orphan Remover -------------
    def build_orphan_remover_tab(self, parent):
        desc = ttk.Label(parent, padding=(10, 10),
            text=("Searches all detected WoW versions for addon SavedVariables (.lua / .lua.bak) "
                  "that do not have a corresponding installed addon (Interface/AddOns). "
                  "Scans Account, Realm, and Character SavedVariables folders. "
                  "Processing also rebuilds AddOns.txt to match installed addons (preserving enabled/disabled where possible).\n\n"
                  "Note: Blizzard_*.lua files are core game data and are automatically ignored "
                  "for safety (but their .lua.bak backups may be removed)."),
            wraplength=800, justify="left")
        desc.pack(fill="x")

        bar = ttk.Frame(parent, padding=(10, 0)); bar.pack(fill="x")
        ttk.Button(bar, text="Scan for Orphaned SavedVariables", command=self.scan_orphan_savedvars).pack(side="left")
        ttk.Button(bar, text="Expand All", command=self._orphan_tree_expand_all).pack(side="left", padx=(8,0))
        ttk.Button(bar, text="Collapse All", command=self._orphan_tree_collapse_all).pack(side="left", padx=(8,0))

        self.orphan_select_all_var = tk.BooleanVar(value=False)
        self.orphan_selall_frame = ImgCheckbox(bar, "Select / Deselect All", self.orphan_select_all_var, self.assets)
        self.orphan_selall_frame.pack(side="left", padx=(12,0))
        self.orphan_select_all_var.trace_add("write", lambda *_: self._orphan_tree_toggle_all())

        ttk.Button(bar, text="Process Selected Files", command=self.process_selected_orphans)\
            .pack(side="left", padx=(8, 0))
        self.orphan_scan_status = ttk.Label(bar, text="")
        self.orphan_scan_status.pack(side="left", padx=(10, 0))

        tree_frame = ttk.Frame(parent, padding=(10, 10)); tree_frame.pack(fill="both", expand=True)
        self.orphan_tree = ttk.Treeview(tree_frame, columns=("path",), show="tree", selectmode="none")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.orphan_tree.yview)
        self.orphan_tree.configure(yscrollcommand=vsb.set)
        self.orphan_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._build_checkbox_images()
        self.orphan_checks = {}
        self.orphan_paths = {}
        self.orphan_tree.bind("<Button-1>", self._on_orphan_tree_click)

    def _orphan_tree_add_parent(self, label):
        pid = self.orphan_tree.insert("", "end", text=f"  {label}", open=False)
        self.orphan_checks[pid] = False
        self._orphan_tree_set_icon(pid)
        return pid

    def _orphan_tree_add_child_file(self, parent_id, path):
        basename = os.path.basename(path)
        iid = self.orphan_tree.insert(parent_id, "end", text=f"  {basename}", open=False)
        self.orphan_checks[iid] = False
        self.orphan_paths[iid] = path
        self._orphan_tree_set_icon(iid)
        return iid

    def _orphan_tree_set_icon(self, iid):
        if self.chk_unchecked:
            img = self.chk_checked if self.orphan_checks.get(iid, False) else self.chk_unchecked
            self.orphan_tree.item(iid, image=img)
        else:
            checked = self.orphan_checks.get(iid, False)
            text = self.orphan_tree.item(iid, "text")
            prefix = "[x]" if checked else "[ ]"
            if not text.strip().startswith("["):
                self.orphan_tree.item(iid, text=f"{prefix} {text.strip()}")
            else:
                self.orphan_tree.item(iid, text=f"{prefix} {text.strip()[3:].strip()}")

    def _on_orphan_tree_click(self, event):
        elem = self.orphan_tree.identify("element", event.x, event.y)
        if elem in ("Treeitem.indicator", "treeitem.indicator", "indicator"):
            # only expand/collapse
            return
        iid = self.orphan_tree.identify_row(event.y)
        if not iid:
            return
        if iid not in self.orphan_paths:
            new_state = not self.orphan_checks.get(iid, False)
            self.orphan_checks[iid] = new_state
            for child in self.orphan_tree.get_children(iid):
                self.orphan_checks[child] = new_state
                self._orphan_tree_set_icon(child)
            self._orphan_tree_set_icon(iid)
        else:
            self.orphan_checks[iid] = not self.orphan_checks.get(iid, False)
            self._orphan_tree_set_icon(iid)
        return "break"

    def _orphan_tree_toggle_all(self):
        new_state = self.orphan_select_all_var.get()
        for iid in self.orphan_tree.get_children(""):
            self.orphan_checks[iid] = new_state
            self._orphan_tree_set_icon(iid)
            for child in self.orphan_tree.get_children(iid):
                self.orphan_checks[child] = new_state
                self._orphan_tree_set_icon(child)

    def _orphan_tree_expand_all(self):
        if hasattr(self, "orphan_tree"):
            for iid in self.orphan_tree.get_children(""):
                self.orphan_tree.item(iid, open=True)

    def _orphan_tree_collapse_all(self):
        if hasattr(self, "orphan_tree"):
            for iid in self.orphan_tree.get_children(""):
                self.orphan_tree.item(iid, open=False)

    def scan_orphan_savedvars(self):
        # Clear UI state
        for n in self.orphan_tree.get_children(""):
            self.orphan_tree.delete(n)
        self.orphan_checks.clear()
        self.orphan_paths.clear()
        self.orphan_select_all_var.set(False)

        base = self.wow_path_var.get().strip()
        if not base or not os.path.isdir(base):
            messagebox.showerror("Invalid Folder", "Please select a valid WoW folder first.")
            return

        versions = self._enumerate_versions(base)

        # Backend call (pure logic)
        orphan_data = scan_orphans(
            versions,
            logger=self if self.verbose_var.get() else None,
        )

        total = 0

        # Rebuild UI tree using backend results
        for vpath, vlabel in versions:
            v_orphans = orphan_data.get(vlabel)
            if not v_orphans:
                continue

            pid = self._orphan_tree_add_parent(vlabel)
            for fpath in v_orphans:
                self._orphan_tree_add_child_file(pid, fpath)
                total += 1

            self.orphan_tree.item(pid, open=False)

        if total:
            self.orphan_scan_status.configure(
                text=f"Found {total} orphan SavedVariable(s)."
            )
        else:
            self.orphan_scan_status.configure(
                text="No orphaned SavedVariables found."
            )

        self.log(f"Orphan Cleaner scan: {total} orphan(s).")

    def process_selected_orphans(self):
        selected = [
            path
            for iid, path in self.orphan_paths.items()
            if self.orphan_checks.get(iid, False)
        ]

        if not selected:
            messagebox.showinfo("No Selection", "No orphaned files selected.")
            return

        use_trash_requested = (self.delete_mode.get() == "trash")
        action = (
            "move to Recycle Bin/Trash"
            if use_trash_requested and HAS_TRASH
            else "delete permanently"
        )

        if not messagebox.askyesno(
            "Confirm",
            f"Are you sure you want to {action} {len(selected)} orphaned SavedVariables?"
        ):
            return

        processed, permanently_deleted, used_trash = delete_orphans(
            selected,
            use_trash=use_trash_requested and HAS_TRASH,
            logger=self if self.verbose_var.get() else None,
        )

        if use_trash_requested and not HAS_TRASH:
            messagebox.showwarning(
                "send2trash missing",
                "The 'send2trash' module is unavailable. Files were deleted permanently."
            )
            self.log("Warning: send2trash not installed; deletions were permanent.")

        self.log(f"Orphan Cleaner: processed {processed} orphan(s).")
        messagebox.showinfo("Completed", f"Processed {processed} orphan(s).")

        # Refresh
        self.scan_orphan_savedvars()

    def rebuild_addons_txt_gui(self):
        base = self.wow_path_var.get().strip()
        if not base or not os.path.isdir(base):
            messagebox.showerror(
                "Invalid Folder", "Please select a valid WoW folder first."
            )
            return

        versions = self._enumerate_versions(base)

        total_written = 0
        total_removed = 0

        for vpath, vlabel in versions:
            addons_dir = os.path.join(vpath, "Interface", "AddOns")
            installed = collect_addon_names(addons_dir)

            rebuilt, removed = rebuild_addons_txt(
                vpath,
                installed,
                logger=self if self.verbose_var.get() else None,
            )

            written_count = sum(len(v) for v in rebuilt.values())
            removed_count = sum(len(v) for v in removed.values())

            total_written += written_count
            total_removed += removed_count

            self.log(
                f"[AddOns.txt] {vlabel}: wrote {written_count} entries, removed {removed_count}"
            )

        messagebox.showinfo(
            "Completed",
            f"Rebuilt AddOns.txt entries.\n"
            f"Total written: {total_written}\n"
            f"Total removed: {total_removed}",
        )

    # ------------- Help & Log -------------
    def build_log_tab(self, parent):
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill="both", expand=True)
        self.log_text = tk.Text(frame, height=15, wrap="none", state="disabled")
        self.log_text.pack(fill="both", expand=True, side="left")
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        ttk.Button(parent, text="Clear Log", command=self.clear_log).pack(anchor="w", padx=10, pady=6)

    def build_help_tab(self, parent):
        outer = ttk.Frame(parent, padding=12)
        outer.pack(fill="both", expand=True)
        card = ttk.Frame(outer, padding=14, relief="groove")
        card.pack(padx=20, pady=20, fill="both", expand=False)
        ttk.Label(card, text=f"World of Warcraft Maintenance Tool {VERSION}",
                  font=(None, 14, "bold")).pack(anchor="center", pady=(0, 8))
        ttk.Label(
            card,
            text=("A utility to find and safely remove .bak and .old files, clean common folders, "
                  "remove orphaned SavedVariables and rebuild AddOns.txt entries.\n\n"
                  "Always close World of Warcraft before running this tool."),
            wraplength=520, justify="center"
        ).pack(anchor="center", pady=(0, 8))
        ttk.Label(card, text="Copyright © 2025 Paul Vandersypen. All rights reserved.",
                  font=(None, 10, "italic")).pack(anchor="center", pady=(0, 6))
        ttk.Button(card, text="Check for Updates", command=self.check_for_updates).pack(anchor="center", pady=(8, 0))

    # ------------- Path selection + detection -------------
    def select_wow_folder(self):
        folder = filedialog.askdirectory(title="Select World of Warcraft Folder")
        if not folder: return
        corrected = self._find_wow_root(folder)
        if not self._is_valid_wow_install(corrected):
            if not messagebox.askyesno("Unrecognized Installation", "The selected folder doesn't appear valid.\n\nContinue anyway?"):
                return
        self.wow_path_var.set(corrected)
        self.settings["wow_path"] = corrected
        save_settings(self.settings)
        self.log(f"WoW folder set: {corrected}")
        self._refresh_folder_cleaner_tabs()

    def _refresh_folder_cleaner_tabs(self):
        # Rebuild Folder Cleaner tabs to reflect new path
        try:
            self.version_notebook.destroy()
        except Exception:
            pass
        container = self.folder_tab
        for w in container.winfo_children():
            try: w.destroy()
            except Exception: pass
        self.build_folder_cleaner_tab(container)

    def _find_wow_root(self, path):
        path = os.path.abspath(path)
        markers = ["_retail_", "_classic_", "_classic_era_",
                   "_retail_ptr_", "_retail_beta_",
                   "_classic_ptr_", "_classic_beta_",
                   "_classic_era_ptr_", "_classic_era_beta_"]
        for _ in range(6):
            if any(os.path.isdir(os.path.join(path, m)) for m in markers):
                return path
            parent = os.path.dirname(path)
            if parent == path: break
            path = parent
        return path

    def _is_valid_wow_install(self, path):
        if not os.path.isdir(path): return False
        indicators = ["_retail_", "_classic_", "_classic_era_",
                      "_retail_ptr_", "_retail_beta_",
                      "_classic_ptr_", "_classic_beta_",
                      "_classic_era_ptr_", "_classic_era_beta_",
                      "Wow.exe", "Launcher.app"]
        return any(os.path.exists(os.path.join(path, it)) for it in indicators)

    # ------------- Logging helpers -------------
    def clear_log(self):
        self.log_lines = []
        try:
            self.log_text.configure(state="normal")
            self.log_text.delete("1.0", "end")
            self.log_text.configure(state="disabled")
        except Exception:
            pass

    def log(self, text):
        from datetime import datetime
        line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}"
        self.log_lines.append(line)
        try:
            self.log_text.configure(state="normal")
            self.log_text.insert("end", line + "\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        except Exception:
            pass

    # ------------- Defaults, Updates, Startup -------------
    def restore_defaults(self):
        if not messagebox.askyesno("Confirm", "Restore all settings to defaults?"):
            return
        try:
            if os.path.exists(SETTINGS_FILE):
                os.remove(SETTINGS_FILE)
            self.settings = {}
            messagebox.showinfo("Restored", "Settings restored to defaults. Please restart the application.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore defaults: {e}")

    def check_for_updates(self):
        messagebox.showinfo("Check for Updates", "Update checking will be added in a future release.")

    def show_startup_warning(self):
        if self.settings.get("hide_warning", False):
            return
        popup = tk.Toplevel(self.root)
        popup.title("Important Notice")
        popup.resizable(False, False)
        pw, ph = 460, 210
        self.root.update_idletasks()
        try:
            mw = self.root.winfo_width(); mh = self.root.winfo_height()
            mx = self.root.winfo_x(); my = self.root.winfo_y()
            px = mx + (mw // 2) - (pw // 2); py = my + (mh // 2) - (ph // 2)
        except Exception:
            sw = self.root.winfo_screenwidth(); sh = self.root.winfo_screenheight()
            px = (sw // 2) - (pw // 2); py = (sh // 2) - (ph // 2)
        popup.geometry(f"{pw}x{ph}+{px}+{py}")
        popup.transient(self.root); popup.grab_set()

        frm = ttk.Frame(popup, padding=12); frm.pack(fill="both", expand=True)
        ttk.Label(
            frm,
            text=("⚠️ Please ensure World of Warcraft is completely closed before using this tool.\n\n"
                  "Running the tool while WoW is open could interfere with the game's files."),
            wraplength=pw - 24, justify="left"
        ).pack(pady=(0, 12))
        self.never_show_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frm, text="Do not show this warning again", variable=self.never_show_var).pack(anchor="w")
        ttk.Button(frm, text="OK", command=lambda: self._dismiss_warning(popup)).pack(pady=(12, 0))

    def _dismiss_warning(self, popup):
        if getattr(self, "never_show_var", None) and self.never_show_var.get():
            self.settings["hide_warning"] = True
            save_settings(self.settings)
            self.log("User disabled startup warning.")
        popup.destroy()

    def on_close(self):
        is_max = False
        try: is_max = (self.root.state() == "zoomed")
        except Exception: pass
        if not is_max:
            parsed = self._parse_geometry(self.root.geometry())
            if parsed:
                w, h, x, y = parsed
                self.settings["window_width"] = max(w, self.MIN_W)
                self.settings["window_height"] = max(h, self.MIN_H)
                self.settings["window_x"] = x
                self.settings["window_y"] = y
        self.settings["is_maximized"] = is_max
        self.settings["wow_path"] = self.wow_path_var.get()
        self.settings["delete_mode"] = self.delete_mode.get()
        self.settings["theme"] = self.theme_var.get()
        self.settings["verbose_logging"] = bool(self.verbose_var.get())
        try:
            self.settings["font_size"] = int(self.font_size_var.get())
        except Exception:
            pass
        save_settings(self.settings)
        self.root.destroy()

# -------------------- Run --------------------
def main():
    root = tk.Tk()
    app = WoWMaintenanceTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
