#!/usr/bin/env python3
"""
World of Warcraft Maintenance Tool v1.0.0

This is the main UI application file. It uses Tkinter to provide a graphical interface for:
- Finding and removing .bak and .old files
- Cleaning folder contents (Cache, Logs, Errors, etc.)
- Detecting and removing orphaned addon SavedVariables
- Rebuilding AddOns.txt files to match installed addons

The application uses backend modules (file_cleaner, folder_cleaner, orphan_cleaner) for
all filesystem operations, keeping the UI layer cleanly separated from business logic.
"""

import os
import sys
import json
import shutil
import site
import importlib
import subprocess
import platform
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont

# Import backend modules for file scanning and deletion operations
from Modules.file_cleaner import find_bak_old_files, delete_files
from Modules.themes import apply_theme
from Modules.orphan_cleaner import (
    scan_orphans,
    delete_orphans,
    rebuild_addons_txt,
    collect_addon_names,
    HAS_TRASH,
)
from Modules.folder_cleaner import (
    scan_all_versions,
    clean_folders,
    HAS_TRASH as FOLDER_HAS_TRASH,
)
# Pull smaller helpers into dedicated modules to slim the main file
from Modules.settings import load_settings, save_settings, SETTINGS_FILE
from Modules.ui_helpers import Tooltip, ImgAssets, ImgCheckbox, ImgRadio
from Modules.logger import Logger
from Modules.tabs.file_cleaner_tab import build_file_cleaner_tree as _build_file_cleaner_tab
from Modules.tabs.folder_cleaner_tab import build_folder_cleaner_tab as _build_folder_cleaner_tab
from Modules.tabs.orphan_cleaner_tab import build_orphan_cleaner_tab as _build_orphan_cleaner_tab
import Modules.tree_helpers as tree_helpers
from Modules.game_validation import is_game_version_valid, show_game_validation_warning

VERSION = "v1.0.0"

def ensure_package(module_name: str, pip_name: str):
    """
    Ensure a package is installed or install it silently.

    This function attempts to import a module. If the import fails, it tries
    to install the package via pip in the user directory, then reimports it.
    If installation fails, None is returned and the app gracefully degrades.

    Args:
        module_name: The Python module name (e.g., 'PIL')
        pip_name: The pip package name (e.g., 'Pillow')

    Returns:
        The imported module object, or None if import/install failed
    """
    try:
        return importlib.import_module(module_name)
    except ImportError:
        try:
            # Silently install package to user's Python directory
            with open(os.devnull, "w") as devnull:
                subprocess.call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--user",
                        "--quiet",
                        "--no-warn-script-location",
                        pip_name,
                    ],
                    stdout=devnull,
                    stderr=devnull,
                )
            importlib.reload(site)
            return importlib.import_module(module_name)
        except (OSError, subprocess.CalledProcessError):
            return None


# Try to load optional dependencies
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
        self.logger = Logger()
        self.version_tabs = []
        self.folder_paths = {}

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
        self.log(f"Session started — {VERSION}")

    # -------- Verbose logging helper --------
    def vlog(self, text):
        if self.verbose_var.get():
            self.logger.log(text)

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
        # Determine theme
        theme = self.theme_var.get().lower()

        # Load theme colors at class level
        from Modules.themes import THEMES
        self.theme_data = THEMES.get(theme, THEMES["light"])

        # Apply theme via the theme module
        checkbox_on, checkbox_off = apply_theme(
            root=self.root,
            treeviews=[self.file_tree, self.orphan_tree],
            theme_name=theme,
            base_path=self.app_path,
        )

        # Save themed checkbox icons for use inside TreeViews
        self.checkbox_on_img = checkbox_on
        self.checkbox_off_img = checkbox_off

        # Refresh TreeView checkbox images
        self._reload_all_custom_checkboxes()

        # Refresh custom PIL-based checkboxes, radios, screenshot toggles, etc.
        self._refresh_styled_checkables()

        # Recolor status bars
        if hasattr(self, "file_scan_status"):
            self.file_scan_status.configure(
                bg=self.root["bg"],
                fg=self.theme_data["fg"]
            )
        if hasattr(self, "orphan_scan_status"):
            self.orphan_scan_status.configure(
                bg=self.root["bg"],
                fg=self.theme_data["fg"]
            )

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

        # Orphan Cleaner
        self.orphan_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.orphan_tab, text="Orphan Cleaner")
        self.build_orphan_cleaner_tab(self.orphan_tab)

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

    # ------------- File Cleaner (Tree) -------------
    def _build_checkbox_images(self):
        return tree_helpers.build_checkbox_images(self)

    def build_file_cleaner_tree(self, parent):
        return _build_file_cleaner_tab(self, parent)

    def _tree_add_parent(self, label):
        return tree_helpers.file_tree_add_parent(self, label)

    def _tree_add_child_file(self, parent_id, path):
        return tree_helpers.file_tree_add_child_file(self, parent_id, path)

    def _tree_set_icon(self, iid):
        return tree_helpers.file_tree_set_icon(self, iid)

    def _on_tree_click(self, event):
        return tree_helpers.on_file_tree_click(self, event)

    def _tree_toggle_all(self):
        return tree_helpers.tree_toggle_all(self)

    def _tree_expand_all(self):
        return tree_helpers.tree_expand_all(self)

    def _tree_collapse_all(self):
        return tree_helpers.tree_collapse_all(self)

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

        # Verify game installation is valid before proceeding
        base = self.wow_path_var.get().strip()
        versions = self._enumerate_versions(base)
        for vpath, vlabel in versions:
            if not is_game_version_valid(vpath):
                show_game_validation_warning(self.root)
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
        return _build_folder_cleaner_tab(self, parent)

    def _build_single_version_tab(self, tab, version_path, version_label):
        from Modules.tabs.folder_helpers import build_single_version_tab as _bsv
        return _bsv(self, tab, version_path, version_label)

    def _show_preview(self, canvas: tk.Canvas, path: str):
        try:
            from Modules.tabs.folder_helpers import show_preview as _show_preview
            _show_preview(self, canvas, path)
        except Exception:
            try:
                canvas.delete("all"); canvas._img_ref = None
            except Exception:
                pass

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
        folder_vars: dict mapping rel_folder_name -> (tk.BooleanVar, path, widget)
        """
        # Determine which folders are selected
        selected = [
            abs_path
            for (rel_name, (var, abs_path, _)) in folder_vars.items()
            if var.get()
        ]

        if not selected:
            messagebox.showinfo("No Selection", "No folders were selected for cleanup.")
            return

        # Verify game installation is valid before proceeding
        base = self.wow_path_var.get().strip()
        for vpath, vlabel in self._enumerate_versions(base):
            if vlabel == version_label:
                if not is_game_version_valid(vpath):
                    show_game_validation_warning(self.root)
                    return
                break

        use_trash_requested = self.delete_mode.get() == "trash"
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

    # ------------- Orphan Cleaner -------------
    def build_orphan_cleaner_tab(self, parent):
        return _build_orphan_cleaner_tab(self, parent)

    def _orphan_tree_add_parent(self, label):
        return tree_helpers.orphan_tree_add_parent(self, label)

    def _orphan_tree_add_child_file(self, parent_id, path):
        return tree_helpers.orphan_tree_add_child_file(self, parent_id, path)

    def _orphan_tree_set_icon(self, iid):
        return tree_helpers.orphan_tree_set_icon(self, iid)

    def _on_orphan_tree_click(self, event):
        return tree_helpers.on_orphan_tree_click(self, event)

    def _orphan_tree_toggle_all(self):
        return tree_helpers.orphan_tree_toggle_all(self)

    def _orphan_tree_expand_all(self):
        return tree_helpers.orphan_tree_expand_all(self)

    def _orphan_tree_collapse_all(self):
        return tree_helpers.orphan_tree_collapse_all(self)

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

        # Verify game installation is valid before proceeding with orphan deletion
        base = self.wow_path_var.get().strip()
        versions = self._enumerate_versions(base)
        for vpath, vlabel in versions:
            if not is_game_version_valid(vpath):
                show_game_validation_warning(self.root)
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
        # Attach the UI text widget to the logger so it mirrors stored lines
        try:
            self.logger.attach_text_widget(self.log_text)
        except Exception:
            pass
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
        try:
            self.logger.clear()
        except Exception:
            # Fallback if logger not ready
            try:
                self.log_text.configure(state="normal")
                self.log_text.delete("1.0", "end")
                self.log_text.configure(state="disabled")
            except Exception:
                pass

    def log(self, text):
        # Delegate to the external logger module
        try:
            self.logger.log(text)
        except Exception:
            # Fallback: directly append to UI text widget
            try:
                line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}"
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
            # Inform user and attempt an automatic restart.
            # Prefer spawning a fresh process then exiting this one; if that fails,
            # fall back to closing the UI and letting the user relaunch manually.
            try:
                messagebox.showinfo("Restored", "Settings restored to defaults. The application will now restart.")
            except Exception:
                # If message box fails for any reason, continue with restart.
                pass

            try:
                # Try to spawn a fresh Python process running the same command-line
                python = sys.executable
                args = [python] + sys.argv
                # Start detached process and exit this one
                subprocess.Popen(args, close_fds=True)
                try:
                    self.root.destroy()
                except Exception:
                    pass
                try:
                    sys.exit(0)
                except SystemExit:
                    # Ensure process ends
                    return
            except Exception:
                # If spawning a new process fails, gracefully close the UI.
                try:
                    messagebox.showinfo("Restored", "Settings restored to defaults. Please restart the application manually.")
                except Exception:
                    pass
                try:
                    self.root.destroy()
                except Exception:
                    pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore defaults: {e}")

    def check_for_updates(self):
        messagebox.showinfo("Check for Updates", "Update checking will be added in a future release.")

    def show_startup_warning(self):
        try:
            from Modules.startup_warning import show_startup_warning as _sw
            _sw(self.root, self.settings, save_settings, logger=getattr(self, "logger", None))
        except Exception:
            # If the module can't be loaded for any reason, silently continue
            pass

    def _dismiss_warning(self, popup):
        # Deprecated: logic moved to Modules.startup_warning
        try:
            popup.destroy()
        except Exception:
            pass

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
