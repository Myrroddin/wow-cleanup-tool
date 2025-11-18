#!/usr/bin/env python3
"""
WoW Cleanup Tool v1.0.0

This is the main UI application file. It uses Tkinter to provide a graphical interface for:
- Finding and removing .bak and .old files
- Cleaning folder contents (Logs, Errors, etc.)
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
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import platform
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
from Modules.file_cleaner import find_bak_old_files, delete_files, scan_bak_old_in_version
from Modules.themes import apply_theme
from Modules.orphan_cleaner import scan_orphans, delete_orphans, rebuild_addons_txt, collect_addon_names
from Modules.folder_cleaner import scan_all_versions, clean_folders
from Modules.settings import load_settings, save_settings, SETTINGS_FILE
from Modules.ui_helpers import Tooltip, ImgAssets, ImgCheckbox, ImgRadio
from Modules.logger import Logger
from Modules.Tabs.file_cleaner_tab import build_file_cleaner_tree as _build_file_cleaner_tab
from Modules.Tabs.folder_cleaner_tab import build_folder_cleaner_tab as _build_folder_cleaner_tab
from Modules.Tabs.orphan_cleaner_tab import build_orphan_cleaner_tab as _build_orphan_cleaner_tab
import Modules.tree_helpers as tree_helpers
from Modules.game_validation import is_game_version_valid, show_game_validation_warning
from Modules import font_selector, geometry, path_manager, ui_refresh, game_optimizer, update_checker, global_settings
from Modules.global_settings import get_global_setting, set_global_setting
from Modules import localization

VERSION = "v1.0.0"

def ensure_package(module_name: str, pip_name: str):
    """
    Ensure a package is installed or install it automatically.

    This function attempts to import a module. If the import fails, it
    installs the package via pip in the user directory, then imports it.
    All dependencies are required for full functionality.

    Args:
        module_name: The Python module name (e.g., 'PIL')
        pip_name: The pip package name (e.g., 'Pillow')

    Returns:
        The imported module object
        
    Raises:
        SystemExit: If package installation fails
    """
    try:
        return importlib.import_module(module_name)
    except ImportError:
        print(f"Installing required package: {pip_name}...")
        try:
            # Install package to user's Python directory
            subprocess.check_call(
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
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            importlib.reload(site)
            return importlib.import_module(module_name)
        except (OSError, subprocess.CalledProcessError) as e:
            print(f"ERROR: Failed to install required package '{pip_name}'.")
            print(f"Please install manually: pip install {pip_name}")
            sys.exit(1)

# Ensure all required dependencies are installed
ensure_package("psutil", "psutil")
ensure_package("send2trash", "send2trash")
ensure_package("PIL", "Pillow")

# Import required dependencies
from send2trash import send2trash
from PIL import Image, ImageTk, ImageDraw

class WoWCleanupTool:
    # Minimum window size: 25% of 1080p (1920x1080) = 480x270
    MIN_W = 480
    MIN_H = 270

    VERSION_FOLDERS = [
        ("_classic_era_", "version_classic_era"),
        ("_classic_", "version_classic"),
        ("_retail_", "version_retail"),
    ]
    VARIANT_SUFFIXES = [
        ("_ptr_", "version_ptr"),
        ("_beta_", "version_beta"),
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
        # Choose an OS-native font family when available for better fidelity
        osname = platform.system()
        try:
            avail = set(tkfont.families())
        except Exception:
            avail = set()

        if osname == "Darwin":
            preferred_families = [".SF NS Text", "Helvetica Neue", "Helvetica", "Arial"]
        elif osname == "Windows":
            preferred_families = ["Segoe UI", "Tahoma", "Arial"]
        else:
            preferred_families = ["Ubuntu", "Cantarell", "DejaVu Sans", "Arial", "Sans"]

        for fam in preferred_families:
            if fam in avail:
                try:
                    self.default_font.configure(family=fam)
                except Exception:
                    pass
                break

        # Build a sorted list of all available font families for the Font dropdown
        # and allow user settings to override the detected default family.
        self.font_families = sorted(avail)
        self.font_family_var = tk.StringVar(value=self.settings.get("font_family", self.default_font.cget("family")))
        
        # Create a separate display variable with cleaned font name
        def clean_font_name_for_display(font_name):
            """Clean font name for display by removing leading non-letter characters and trimming spaces."""
            import re
            if not font_name:
                return ""
            cleaned = font_name.strip()
            # Remove leading non-letter characters
            while cleaned and not cleaned[0].isalpha():
                cleaned = cleaned[1:]
            # Remove trailing non-alphanumeric characters except spaces between words
            while cleaned and not cleaned[-1].isalpha() and not cleaned[-1].isdigit():
                cleaned = cleaned[:-1]
            # Replace multiple spaces with single space and strip
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            return cleaned
        
        self.font_family_display_var = tk.StringVar(value=clean_font_name_for_display(self.font_family_var.get()))
        
        # Trace changes to keep display var in sync
        def update_font_display(*args):
            self.font_family_display_var.set(clean_font_name_for_display(self.font_family_var.get()))
        self.font_family_var.trace_add("write", update_font_display)
        
        try:
            # If the user had a saved font, apply it now.
            self.default_font.configure(family=self.font_family_var.get())
        except Exception:
            pass

        # Determine base size (allow user override via settings)
        base_size = self.default_font.cget("size")
        try:
            start_size = int(self.settings.get("font_size", base_size))
        except Exception:
            start_size = int(base_size)

        # Apply small OS-specific size nudges for native look
        if osname == "Darwin":
            # macOS UI typically uses slightly larger default text
            start_size = max(start_size, int(base_size) + 1)
        else:
            start_size = max(start_size, int(base_size))

        start_size = min(max(start_size, 6), 16)
        self.font_size_var = tk.IntVar(value=start_size)
        try:
            self.default_font.configure(size=self.font_size_var.get())
        except Exception:
            pass
        self.root.option_add("*Font", self.default_font)

        # Micro-adjustments to ttk widget styling per OS for closer native fidelity
        try:
            if osname == "Darwin":
                # Slightly larger button padding on macOS
                self.style.configure("TButton", padding=(8, 4))
                self.style.configure("TMenubutton", padding=(8, 4))
            elif osname == "Windows":
                # Use Windows-like tighter padding
                self.style.configure("TButton", padding=(6, 3))
            else:
                # Linux: conservative padding
                self.style.configure("TButton", padding=(6, 4))
        except Exception:
            pass

        # Initialize localization
        saved_language = self.settings.get("language", None)
        if saved_language and saved_language in localization.AVAILABLE_LANGUAGES:
            localization.set_language(saved_language)
        else:
            # Auto-detect system language
            detected_lang = localization.detect_system_language()
            localization.set_language(detected_lang)
            self.settings["language"] = detected_lang

        # State
        self.wow_path_var = tk.StringVar(value=self.settings.get("wow_path", ""))
        self.delete_mode = tk.StringVar(value=self.settings.get("delete_mode", "delete"))
        # Theme: translate stored English value to current language for display
        stored_theme = self.settings.get("theme", "light")
        self.theme_var = tk.StringVar(value=localization._(stored_theme))
        self.language_var = tk.StringVar(value=localization.get_language())
        self.verbose_var = tk.BooleanVar(value=bool(self.settings.get("verbose_logging", False)))
        self.check_for_updates_var = tk.BooleanVar(value=bool(self.settings.get("check_for_updates", True)))
        # External log mode: "fresh" creates new file, "append" appends to existing (max 20 sessions)
        self.external_log_mode_var = tk.StringVar(value=self.settings.get("external_log_mode", "fresh"))

        self.root.title(localization._("window_title") + f" {VERSION}")
        geometry.setup_geometry(self)
        ui_refresh.rebuild_assets(self)
        self.build_ui()
        self._apply_theme()   # ← apply after widgets exist

        self.root.bind("<Configure>", lambda e: geometry.on_configure(self), add="+")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(200, self.show_startup_warning)
        self.root.after(500, self._apply_smart_defaults)  # Apply smart defaults after UI is ready
        self.log(localization._("session_started", VERSION))

    # -------- Verbose logging helper --------
    def vlog(self, text):
        if self.verbose_var.get():
            self.logger.log(text)

    # ------------- OS base theme -------------
    def _apply_os_base_theme(self):
        osname = platform.system()
        # Prefer OS-native themes when available, falling back to a sensible default.
        available = list(self.style.theme_names())
        if osname == "Darwin":
            preferred = ["aqua", "clam", "default"]
        elif osname == "Windows":
            preferred = ["vista", "winnative", "xpnative", "clam", "default"]
        else:
            # Linux / other X11 systems
            preferred = ["clam", "alt", "default"]

        for theme in preferred:
            if theme in available:
                try:
                    self.style.theme_use(theme)
                    return
                except Exception:
                    continue

        # As a last resort, use whatever theme is currently set (or the first available)
        try:
            current = self.style.theme_use()
            self.style.theme_use(current)
        except Exception:
            try:
                if available:
                    self.style.theme_use(available[0])
            except Exception:
                pass

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
        # Determine theme - convert from translated display value to English
        theme_display = self.theme_var.get()
        if theme_display == localization._("dark"):
            theme = "dark"
        elif theme_display == localization._("light"):
            theme = "light"
        else:
            theme = theme_display.lower()  # fallback

        # Load theme colors at class level
        from Modules.themes import THEMES
        self.theme_data = THEMES.get(theme, THEMES["light"])

        # Apply theme via the theme module
        apply_theme(
            root=self.root,
            treeviews=[self.file_tree, self.orphan_tree],
            theme_name=theme,
            base_path=self.app_path,
        )

        # Refresh TreeView checkbox images (PIL-generated)
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
        
        # Recolor optimization suggestions disclaimer
        if hasattr(self, "opt_sug_disclaimer"):
            is_dark = theme == "dark"
            warning_color = "#ff9933" if is_dark else "#cc0000"  # Orange for dark, dark red for light
            self.opt_sug_disclaimer.configure(
                bg=self.theme_data["bg"],
                fg=warning_color
            )
        
        # Recolor game optimizer bullet point labels
        if hasattr(self, "optimizer_bullet_labels"):
            is_dark = theme == "dark"
            for item in self.optimizer_bullet_labels:
                # Handle both simple labels and (label, is_new) tuples
                if isinstance(item, tuple):
                    lbl, is_new = item
                    if is_new:
                        # New settings: use green (lighter green for dark theme)
                        text_color = "#00ff00" if is_dark else "#008000"
                    else:
                        # Existing settings: use theme text color
                        text_color = "#ffffff" if is_dark else "#000000"
                else:
                    lbl = item
                    # Regular bullet labels use theme text color
                    text_color = "#ffffff" if is_dark else "#000000"
                
                lbl.configure(
                    bg=self.theme_data["bg"],
                    fg=text_color
                )
        
        # Recolor game optimizer theme-aware labels
        if hasattr(self, "optimizer_theme_labels"):
            is_dark = theme == "dark"
            for item in self.optimizer_theme_labels:
                label_type = item[0]
                label = item[1]
                
                if label_type == 'info':
                    # Gray info label
                    gray_color = "#a0a0a0" if is_dark else "#808080"
                    label.configure(bg=self.theme_data["bg"], fg=gray_color)
                elif label_type == 'gpu_switch':
                    # Blue GPU switch label
                    blue_color = "#6699ff" if is_dark else "#0000ff"
                    label.configure(bg=self.theme_data["bg"], fg=blue_color)
                elif label_type == 'instruction':
                    # Red instruction label
                    red_color = "#ff6666" if is_dark else "#cc0000"
                    label.configure(bg=self.theme_data["bg"], fg=red_color)
                elif label_type == 'system_match':
                    # Blue system match label
                    blue_color = "#6699ff" if is_dark else "#0000ff"
                    label.configure(bg=self.theme_data["bg"], fg=blue_color)
                elif label_type == 'optimization_status':
                    # Green/orange optimization status label (has StringVar)
                    if len(item) > 2:
                        status_var = item[2]
                        # Check current text to determine color
                        current_text = status_var.get()
                        # If status contains "applied", use green; otherwise orange
                        if "applied" in current_text.lower():
                            fg_color = "#00ff00" if is_dark else "#008000"
                        else:
                            fg_color = "#ff9933" if is_dark else "#ff8800"
                        label.configure(bg=self.theme_data["bg"], fg=fg_color)
                elif label_type == 'status':
                    # Green status label
                    green_color = "#00ff00" if is_dark else "#008000"
                    label.configure(bg=self.theme_data["bg"], fg=green_color)
        
        # Update options border for theme
        self._set_options_border(theme == "dark")

    # Asset rebuild now delegated to Modules.ui_refresh
    def _rebuild_assets(self):
        ui_refresh.rebuild_assets(self)

    def _set_options_border(self, show_dark_border: bool):
        ui_refresh.set_options_border(self, show_dark_border)

    def _apply_smart_defaults(self):
        """Apply smart defaults on first launch: auto-detect WoW path and run hardware scan."""
        try:
            # Only apply smart defaults if this appears to be first launch
            is_first_launch = not self.settings.get("wow_path") or not get_global_setting("hardware_cache")
            
            if not is_first_launch:
                return
            
            # Try to auto-detect WoW installation path
            wow_path = self._auto_detect_wow_path()
            if wow_path:
                self.wow_path_var.set(wow_path)
                self.settings["wow_path"] = wow_path
                save_settings(self.settings)
                self.log(localization._("auto_detected_wow").format(wow_path), always_log=True)
            
            # Run hardware scan automatically if WoW path is set
            if self.wow_path_var.get() and hasattr(self, 'optimizer_tab'):
                self.log(localization._("running_initial_hardware_scan"), always_log=True)
                # Switch to Game Optimizer tab
                try:
                    self.main_notebook.select(self.optimizer_tab)
                except Exception:
                    pass
        except Exception as e:
            self.log(localization._("smart_defaults_error").format(str(e)))

    def _auto_detect_wow_path(self):
        """Attempt to auto-detect World of Warcraft installation path.
        
        Returns:
            str: Path to WoW folder, or empty string if not found
        """
        import platform
        
        common_paths = []
        system = platform.system()
        
        if system == "Windows":
            # Common Windows installation paths
            drives = ["C:", "D:", "E:"]
            for drive in drives:
                common_paths.extend([
                    f"{drive}\\Program Files (x86)\\World of Warcraft",
                    f"{drive}\\Program Files\\World of Warcraft",
                    f"{drive}\\Games\\World of Warcraft",
                    f"{drive}\\Blizzard Games\\World of Warcraft",
                ])
        elif system == "Darwin":  # macOS
            home = os.path.expanduser("~")
            common_paths.extend([
                "/Applications/World of Warcraft",
                f"{home}/Applications/World of Warcraft",
                "/Applications/Games/World of Warcraft",
            ])
        else:  # Linux
            home = os.path.expanduser("~")
            common_paths.extend([
                f"{home}/.wine/drive_c/Program Files (x86)/World of Warcraft",
                f"{home}/Games/World of Warcraft",
                f"{home}/.local/share/lutris/runners/wine/*/World of Warcraft",
            ])
        
        # Check each path
        for path in common_paths:
            if os.path.isdir(path):
                # Verify it's actually a WoW folder by checking for key files
                if self._verify_wow_folder(path):
                    return path
        
        return ""

    def _verify_wow_folder(self, path):
        """Verify that a folder is a valid World of Warcraft installation.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path contains valid WoW installation
        """
        if not os.path.isdir(path):
            return False
        
        # Check for at least one version folder
        version_folders = ["_retail_", "_classic_era_", "_classic_", "_ptr_", "_beta_"]
        has_version = any(os.path.isdir(os.path.join(path, vf)) for vf in version_folders)
        
        return has_version

    def _add_tab_help_icon(self, tab_frame, tab_key):
        """Add a help icon to a tab that shows contextual information.
        
        Args:
            tab_frame: The tab's frame widget
            tab_key: Key for help text lookup
        """
        help_texts = {
            "file_cleaner": (
                "File Cleaner Help\n\n"
                "Scans for .bak and .old backup files in your WoW folders.\n\n"
                "• Click 'Scan' to find backup files\n"
                "• Select files to remove using checkboxes\n"
                "• Click 'Process Selected' to delete or move to recycle bin\n\n"
                "Safe to use: These are backup files that can be removed."
            ),
            "folder_cleaner": (
                "Folder Cleaner Help\n\n"
                "Removes specific game folders like Cache, Logs, and Screenshots.\n\n"
                "• Select version (Retail, Classic, etc.)\n"
                "• Check folders you want to clean\n"
                "• Click 'Preview' to see what will be removed\n"
                "• Click 'Process Selected Folders' to clean\n\n"
                "Note: Cache and logs regenerate automatically."
            ),
            "orphan_cleaner": (
                "Orphan Cleaner Help\n\n"
                "Finds SavedVariables files for uninstalled addons.\n\n"
                "• Scans AddOns.txt to find installed addons\n"
                "• Compares with SavedVariables folder\n"
                "• Lists orphaned files for removal\n\n"
                "Helps keep your SavedVariables folder clean."
            ),
            "game_optimizer": (
                "Game Optimizer Help\n\n"
                "Automatically configures WoW graphics settings based on your hardware.\n\n"
                "• Click 'Scan Hardware' to detect your system\n"
                "• Review recommended preset (Low/Medium/High/Ultra)\n"
                "• Select desired preset from dropdown\n"
                "• Click 'Apply' to update Config.wtf\n\n"
                "A backup is created automatically before changes."
            ),
            "optimization_suggestions": (
                "Optimization Suggestions Help\n\n"
                "Manual optimizations you can perform to improve game performance.\n\n"
                "• These are NOT performed automatically\n"
                "• Hover over each suggestion title for detailed information\n"
                "• Follow instructions carefully\n"
                "• Some require BIOS changes\n\n"
                "Risk levels indicated in tooltips."
            ),
            "log": (
                "Log Help\n\n"
                "View all actions performed by the application.\n\n"
                "• Real-time log of all operations\n"
                "• Click 'Export Log' to save to file\n"
                "• Click 'Clear Log' to reset display\n\n"
                "Useful for troubleshooting issues."
            )
        }
        
        help_text = help_texts.get(tab_key, "No help available for this tab.")
        
        # Create help button in top-right corner
        help_btn = ttk.Label(tab_frame, text="❓", font=(None, 12), foreground="blue", cursor="hand2")
        help_btn.place(relx=1.0, rely=0.0, x=-10, y=5, anchor="ne")
        
        # Add tooltip with detailed help
        from Modules.ui_helpers import Tooltip
        Tooltip(help_btn, help_text, app=self)
        
        # Add click handler for detailed help dialog
        def show_detailed_help(event=None):
            from tkinter import messagebox
            messagebox.showinfo(f"{tab_key.replace('_', ' ').title()} Help", help_text)
        
        help_btn.bind("<Button-1>", show_detailed_help)

    def update_font_size(self):
        size = min(max(int(self.font_size_var.get()), 6), 16)
        self.font_size_var.set(size)
        self.default_font.configure(size=size)
        self.settings["font_size"] = size
        save_settings(self.settings)
        # If we have a font OptionMenu, update its display font and menu entries
        try:
            if hasattr(self, "font_optionmenu"):
                try:
                    self.font_optionmenu.configure(font=(self.font_family_var.get(), size))
                except Exception:
                    pass
                try:
                    menu = self.font_optionmenu["menu"]
                    for i, fam in enumerate(self.font_families):
                        try:
                            menu.entryconfig(i, font=(fam, size))
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            pass
        # If the font selector is open, update label widget fonts to the new size
        try:
            if self._font_selector and self._font_label_widgets:
                for lbl in self._font_label_widgets:
                    try:
                        # lbl is a tk.Label
                        fam = getattr(lbl, "_family", None)
                        if fam:
                            lbl.configure(font=(fam, size))
                    except Exception:
                        pass
        except Exception:
            pass

    def open_font_selector(self):
        """Open a searchable Toplevel that lists font families styled in their own font.

        Selecting a font previews it immediately. The user must Apply to persist
        the change, or Cancel to revert to the previous font.
        
        Uses incremental loading: displays fonts in batches as the user scrolls,
        improving performance on systems with large font catalogs.
        """
        # If already open, bring to front
        if self._font_selector:
            try:
                self._font_selector.deiconify(); self._font_selector.lift()
            except Exception:
                pass
            return

        prev_family = self.font_family_var.get()
        self._prev_font_family = prev_family

        sel = tk.Toplevel(self.root)
        sel.title("Select Font")
        sel.transient(self.root)
        sel.grab_set()
        sel.geometry("+%d+%d" % (self.root.winfo_rootx() + 60, self.root.winfo_rooty() + 60))
        self._font_selector = sel

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
        self._font_label_widgets = []
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
            for fam in self.font_families:
                if pattern and pattern not in fam.lower():
                    continue
                result.append(fam)
            return result

        def load_batch():
            """Load the next batch of fonts into the list."""
            state = _load_state
            if state["loaded_count"] >= len(state["filtered_fonts"]):
                return  # All loaded
            
            size = max(8, min(28, int(self.font_size_var.get())))
            batch_end = min(state["loaded_count"] + state["batch_size"], len(state["filtered_fonts"]))
            
            for i in range(state["loaded_count"], batch_end):
                fam = state["filtered_fonts"][i]
                try:
                    lbl = tk.Label(inner, text=fam, anchor="w", font=(fam, size))
                    lbl.pack(fill="x", anchor="w", padx=2, pady=1)
                    lbl._family = fam
                    def _on_click(event, f=fam):
                        try:
                            self.apply_font_preview(f)
                        except Exception:
                            pass
                    lbl.bind("<Button-1>", _on_click)
                    # Hover feedback
                    lbl.bind("<Enter>", lambda e, l=lbl: l.configure(bg="#e6f2ff"))
                    lbl.bind("<Leave>", lambda e, l=lbl: l.configure(bg=sel.cget("bg")))
                    self._font_label_widgets.append(lbl)
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
                    self.root.after_cancel(state["after_id"])
                except Exception:
                    pass
            
            # Schedule load on next idle (debounce)
            state["after_id"] = self.root.after(100, load_batch)

        def populate(filter_text=""):
            """Clear list and prepare filtered fonts for incremental loading."""
            state = _load_state
            # Cancel any pending load
            if state["after_id"]:
                try:
                    self.root.after_cancel(state["after_id"])
                except Exception:
                    pass
            
            # Clear display
            for w in inner.winfo_children():
                w.destroy()
            self._font_label_widgets.clear()
            
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
        apply_btn = ttk.Button(btn_frame, text=localization._("apply"), command=lambda: self._finalize_font_change())
        apply_btn.pack(side="right", padx=(4,0))
        cancel_btn = ttk.Button(btn_frame, text=localization._("cancel"), command=lambda: self._cancel_font_change())
        cancel_btn.pack(side="right")

        def on_close_sel():
            self._cancel_font_change()

        sel.protocol("WM_DELETE_WINDOW", on_close_sel)

    def apply_font_preview(self, family: str):
        """Temporarily apply a font family to the UI for previewing."""
        try:
            if not family:
                return
            self.font_family_var.set(family)
            try:
                self.default_font.configure(family=family)
            except Exception:
                pass
            try:
                self.root.option_add("*Font", self.default_font)
            except Exception:
                pass
            # Update the font button to show preview
            try:
                self.font_button.configure(font=(family, self.font_size_var.get()))
            except Exception:
                pass
            # Track currently previewed family
            self._previewed_family = family
        except Exception:
            pass

    def _finalize_font_change(self):
        """Ask user to confirm the previewed font; save or revert accordingly."""
        try:
            new = getattr(self, "_previewed_family", self.font_family_var.get())
            old = getattr(self, "_prev_font_family", None)
            if new == old:
                # Nothing changed
                try:
                    if self._font_selector:
                        self._font_selector.grab_release(); self._font_selector.destroy()
                except Exception:
                    pass
                self._font_selector = None
                return

            ok = messagebox.askyesno(localization._("confirm_font"), localization._("apply_font_question").format(new))
            if ok:
                try:
                    self.settings["font_family"] = new
                    save_settings(self.settings)
                except Exception:
                    pass
                try:
                    if self._font_selector:
                        self._font_selector.grab_release(); self._font_selector.destroy()
                except Exception:
                    pass
                self._font_selector = None
                self._prev_font_family = new
            else:
                # Revert
                try:
                    if old:
                        self.default_font.configure(family=old)
                        self.root.option_add("*Font", self.default_font)
                        self.font_family_var.set(old)
                        try:
                            self.font_button.configure(font=(old, self.font_size_var.get()))
                        except Exception:
                            pass
                except Exception:
                    pass
                try:
                    if self._font_selector:
                        self._font_selector.grab_release(); self._font_selector.destroy()
                except Exception:
                    pass
                self._font_selector = None
        except Exception:
            pass

    def _cancel_font_change(self):
        """Cancel selector and revert any previewed font back to previous."""
        try:
            prev = getattr(self, "_prev_font_family", None)
            if prev:
                try:
                    self.default_font.configure(family=prev)
                    self.root.option_add("*Font", self.default_font)
                    self.font_family_var.set(prev)
                    try:
                        self.font_button.configure(font=(prev, self.font_size_var.get()))
                    except Exception:
                        pass
                except Exception:
                    pass
        except Exception:
            pass
        try:
            if self._font_selector:
                self._font_selector.grab_release(); self._font_selector.destroy()
        except Exception:
            pass
        self._font_selector = None

    def update_font_family(self):
        """Apply a newly selected font family and persist it per-user."""
        try:
            fam = self.font_family_var.get()
            if fam:
                try:
                    self.default_font.configure(family=fam)
                except Exception:
                    pass
                # Update OptionMenu button font
                try:
                    if hasattr(self, "font_optionmenu"):
                        self.font_optionmenu.configure(font=(fam, self.font_size_var.get()))
                except Exception:
                    pass
                # Persist
                self.settings["font_family"] = fam
                save_settings(self.settings)
        except Exception:
            pass

    def change_language(self, *args):
        """Handle language change with confirmation and automatic application."""
        from tkinter import messagebox
        import sys
        import subprocess
        
        new_lang = self.language_var.get()
        current_lang = localization.get_language()
        
        if new_lang != current_lang:
            # Get the display names for confirmation
            new_lang_name = localization.AVAILABLE_LANGUAGES.get(new_lang, new_lang)
            current_lang_name = localization.AVAILABLE_LANGUAGES.get(current_lang, current_lang)
            
            # Show confirmation dialog
            confirm = messagebox.askyesno(
                localization._("change_language"),
                localization._("change_language_question").format(current_lang_name, new_lang_name),
                icon='question'
            )
            
            if confirm:
                # Save all current settings before restart (same as on_close)
                geometry.save_geometry(self)
                self.settings["wow_path"] = self.wow_path_var.get()
                self.settings["delete_mode"] = self.delete_mode.get()
                
                # Convert displayed translated values back to English for storage
                theme_display = self.theme_var.get()
                theme = "light"  # default
                if theme_display == localization._("dark"):
                    theme = "dark"
                elif theme_display == localization._("light"):
                    theme = "light"
                else:
                    theme = theme_display.lower()  # fallback
                self.settings["theme"] = theme
                
                # Save the new language preference
                localization.set_language(new_lang)
                self.settings["language"] = new_lang
                
                self.settings["verbose_logging"] = bool(self.verbose_var.get())
                self.settings["check_for_updates"] = bool(self.check_for_updates_var.get())
                self.settings["external_log_mode"] = self.external_log_mode_var.get()
                try:
                    self.settings["font_size"] = int(self.font_size_var.get())
                except Exception:
                    pass
                try:
                    self.settings["font_family"] = self.font_family_var.get()
                except Exception:
                    pass
                
                save_settings(self.settings)
                
                # Show brief confirmation
                messagebox.showinfo(
                    localization._("language_changed"),
                    localization._("language_changed_restart").format(new_lang_name)
                )
                
                # Restart the application using subprocess to handle paths with spaces
                python = sys.executable
                script = sys.argv[0]
                
                # Close current window
                self.root.destroy()
                
                # Start new instance
                if platform.system() == "Windows":
                    # Windows: use subprocess.Popen with properly quoted arguments
                    subprocess.Popen([python, script] + sys.argv[1:], 
                                   creationflags=subprocess.CREATE_NEW_CONSOLE if sys.stdout is None else 0)
                else:
                    # macOS/Linux: use os.execv which handles spaces correctly
                    os.execv(python, [python, script] + sys.argv[1:])
            else:
                # User cancelled - revert to previous language in the dropdown
                old_lang_name = localization.AVAILABLE_LANGUAGES.get(current_lang, current_lang_name)
                self.language_display_var.set(old_lang_name)
                self.language_var.set(current_lang)

    # ------------- UI Build -------------
    def build_ui(self):
        _ = localization._  # Convenience alias
        
        # Options with subtle border
        self.options_border = tk.Frame(self.root, bg=self.root.cget("bg"))
        self.options_border.pack(fill="x", padx=10, pady=(10, 8))
        options = ttk.LabelFrame(self.options_border, text=_("options"), padding=8)
        options.pack(fill="x", padx=1, pady=1)

        # Row 0: Label | Entry (half) | Browse | Font size | Theme | Language
        ttk.Label(options, text=_("wow_folder")).grid(row=0, column=0, sticky="w", padx=(0,6), pady=4)

        self.folder_entry = ttk.Entry(options, textvariable=self.wow_path_var, width=42)
        self.folder_entry.grid(row=0, column=1, sticky="we", padx=(0,6), pady=4)

        folder_btn = ttk.Button(options, text=_("browse"), command=self.select_wow_folder)
        folder_btn.grid(row=0, column=2, sticky="w", padx=(0,10), pady=4)
        Tooltip(folder_btn, _("browse_tooltip"), app=self)

        ttk.Label(options, text=_("font_size")).grid(row=0, column=3, sticky="e", padx=(0,6), pady=4)
        font_spin = ttk.Spinbox(options, from_=6, to=16, textvariable=self.font_size_var, width=5, command=self.update_font_size)
        font_spin.grid(row=0, column=4, sticky="w", padx=(0,10), pady=4)

        # Font selection: a searchable selector opened from a button showing current font
        ttk.Label(options, text=_("font")).grid(row=0, column=5, sticky="e", padx=(0,6), pady=4)
        # Button shows the currently selected font; clicking opens a searchable selector.
        self.font_button = ttk.Button(options, textvariable=self.font_family_display_var, command=lambda: font_selector.open_font_selector(self))
        self.font_button.grid(row=0, column=6, sticky="w", padx=(0,10), pady=4)
        try:
            # Apply the selected font to the button itself for a live preview.
            self.font_button.configure(style="TButton")
            self.font_button.configure(font=(self.font_family_var.get(), self.font_size_var.get()))
        except Exception:
            pass
        # Prepare holder for selector widgets when opened
        self._font_selector = None
        self._font_label_widgets = []

        ttk.Label(options, text=_("theme")).grid(row=0, column=7, sticky="e", padx=(0,6), pady=4)
        theme_combo = ttk.Combobox(options, textvariable=self.theme_var, values=[_("light"), _("dark")], state="readonly", width=10)
        theme_combo.grid(row=0, column=8, sticky="w", padx=(0,10), pady=4)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_theme())

        ttk.Label(options, text=_("language")).grid(row=0, column=9, sticky="e", padx=(0,6), pady=4)
        # Create language dropdown with native language names
        lang_codes = sorted(localization.AVAILABLE_LANGUAGES.keys())
        lang_display_names = [localization.AVAILABLE_LANGUAGES[code] for code in lang_codes]
        self._lang_code_map = dict(zip(lang_display_names, lang_codes))
        self._lang_name_map = {code: localization.AVAILABLE_LANGUAGES[code] for code in lang_codes}
        current_lang_name = self._lang_name_map[self.language_var.get()]
        self.language_display_var = tk.StringVar(value=current_lang_name)
        language_combo = ttk.Combobox(options, textvariable=self.language_display_var, values=lang_display_names, state="readonly", width=18)
        language_combo.grid(row=0, column=10, sticky="w", padx=(0,0), pady=4)
        
        def on_language_change(e):
            selected_name = self.language_display_var.get()
            selected_code = self._lang_code_map.get(selected_name)
            if selected_code:
                self.language_var.set(selected_code)
                self.change_language()
        
        language_combo.bind("<<ComboboxSelected>>", on_language_change)

        options.columnconfigure(1, weight=1)   # Entry stretches

        # Row 1: File Action label | Delete | Trash | Verbose | Check Updates | Restore
        mode_frame = ttk.Frame(options)
        mode_frame.grid(row=1, column=0, columnspan=11, sticky="we", pady=(2, 2))
        mode_frame.columnconfigure(10, weight=1)

        ttk.Label(mode_frame, text=_("file_action")).grid(row=0, column=0, sticky="w", padx=(0,8))

        self.radio_container = ttk.Frame(mode_frame)
        self.radio_container.grid(row=0, column=1, sticky="w")

        self.rb_delete = ImgRadio(self.radio_container, _("delete_permanently"), self.delete_mode, "delete", self.assets)
        self.rb_trash  = ImgRadio(self.radio_container, _("move_to_recycle"), self.delete_mode, "trash", self.assets)
        self.rb_delete.pack(side="left", padx=(0,14))
        self.rb_trash.pack(side="left", padx=(0,14))

        self.verbose_cb = ImgCheckbox(mode_frame, _("enable_verbose"), self.verbose_var, self.assets)
        self.verbose_cb.grid(row=0, column=2, sticky="w", padx=(10,0))
        Tooltip(self.verbose_cb, _("verbose_tooltip"), app=self)

        # External log mode
        ttk.Label(mode_frame, text=_("external_log")).grid(row=0, column=3, sticky="e", padx=(10,6))
        self.external_log_fresh_rb = ImgRadio(mode_frame, _("fresh"), self.external_log_mode_var, "fresh", self.assets)
        self.external_log_fresh_rb.grid(row=0, column=4, sticky="w")
        Tooltip(self.external_log_fresh_rb, _("fresh_tooltip"), app=self)
        self.external_log_append_rb = ImgRadio(mode_frame, _("append"), self.external_log_mode_var, "append", self.assets)
        self.external_log_append_rb.grid(row=0, column=5, sticky="w", padx=(5,0))
        Tooltip(self.external_log_append_rb, _("append_tooltip"), app=self)

        self.check_updates_cb = ImgCheckbox(mode_frame, _("check_updates"), self.check_for_updates_var, self.assets)
        self.check_updates_cb.grid(row=0, column=6, sticky="w", padx=(10,0))
        Tooltip(self.check_updates_cb, _("check_updates_tooltip"), app=self)

        restore_btn = ttk.Button(mode_frame, text=_("restore_defaults"), command=self.restore_defaults)
        restore_btn.grid(row=0, column=9, sticky="e", padx=(10,0))

        # Main notebook
        self.main_notebook = ttk.Notebook(self.root)
        self.main_notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.main_notebook.configure(padding=(4, 0))

        # File Cleaner
        self.cleaner_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.cleaner_tab, text=f"🗂️  {_('file_cleaner')}")
        self._add_tab_help_icon(self.cleaner_tab, "file_cleaner")
        self.build_file_cleaner_tree(self.cleaner_tab)

        # Folder Cleaner
        self.folder_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.folder_tab, text=f"📁  {_('folder_cleaner')}")
        self._add_tab_help_icon(self.folder_tab, "folder_cleaner")
        self.build_folder_cleaner_tab(self.folder_tab)

        # Orphan Cleaner
        self.orphan_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.orphan_tab, text=f"🔍  {_('orphan_cleaner')}")
        self._add_tab_help_icon(self.orphan_tab, "orphan_cleaner")
        self.build_orphan_cleaner_tab(self.orphan_tab)

        # Game Optimizer
        self.optimizer_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.optimizer_tab, text=f"⚙️  {_('game_optimizer')}")
        self._add_tab_help_icon(self.optimizer_tab, "game_optimizer")
        # Initialize lists for theme-aware labels
        self.optimizer_bullet_labels = []
        self.optimizer_theme_labels = []
        game_optimizer.build_game_optimizer_tab(self, self.optimizer_tab)

        # Optimization Suggestions
        self.suggestions_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.suggestions_tab, text=f"💡  {_('optimization_suggestions')}")
        self._add_tab_help_icon(self.suggestions_tab, "optimization_suggestions")
        self.build_optimization_suggestions_tab(self.suggestions_tab)

        # Log
        self.log_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.log_tab, text=f"📋  {_('log')}")
        self._add_tab_help_icon(self.log_tab, "log")
        self.build_log_tab(self.log_tab)

        # Help
        self.help_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.help_tab, text=f"❓  {localization._('help_about')}")
        self.build_help_tab(self.help_tab)

        self._set_options_border(self.theme_var.get() == localization._("dark"))

    # track styled widgets for refresh (theme switch)
    def _refresh_styled_checkables(self):
        if hasattr(self, "rb_delete"):
            self.rb_delete.assets = self.assets; self.rb_delete._sync_image()
        if hasattr(self, "rb_trash"):
            self.rb_trash.assets = self.assets; self.rb_trash._sync_image()
        if hasattr(self, "verbose_cb"):
            self.verbose_cb.assets = self.assets; self.verbose_cb._sync_image()
        if hasattr(self, "external_log_fresh_rb"):
            self.external_log_fresh_rb.assets = self.assets; self.external_log_fresh_rb._sync_image()
        if hasattr(self, "external_log_append_rb"):
            self.external_log_append_rb.assets = self.assets; self.external_log_append_rb._sync_image()
        if hasattr(self, "tree_selall_frame"):
            self.tree_selall_frame.assets = self.assets; self.tree_selall_frame._sync_image()
        if hasattr(self, "orphan_selall_frame"):
            self.orphan_selall_frame.assets = self.assets; self.orphan_selall_frame._sync_image()
        if hasattr(self, "styled_folder_boxes"):
            for cb in self.styled_folder_boxes:
                cb.assets = self.assets; cb._sync_image()
        if hasattr(self, "styled_shot_boxes"):
            for cb in self.styled_shot_boxes:
                cb.assets = self.assets; cb._sync_image()
        if hasattr(self, "_build_checkbox_images"):
            self._build_checkbox_images()
            if hasattr(self, "file_tree"):
                for iid in getattr(self, "tree_checks", {}):
                    self._tree_set_icon(iid)
            if hasattr(self, "orphan_tree"):
                for iid in getattr(self, "orphan_checks", {}):
                    self._orphan_tree_set_icon(iid)

    def _reload_all_custom_checkboxes(self):
        """
        Called after theme changes.
        Replaces checkbox images in file/orphan/folder cleaners.
        """

        # File Cleaner
        for iid, var in self.tree_checks.items():
            # var is a boolean, not a BooleanVar
            img = self.chk_checked if var else self.chk_unchecked
            self.file_tree.item(iid, image=img)

        # Orphan Cleaner
        for iid, var in self.orphan_checks.items():
            # var is a boolean, not a BooleanVar
            img = self.chk_checked if var else self.chk_unchecked
            self.orphan_tree.item(iid, image=img)

        # Folder cleaner uses per-version custom widgets,
        # so we only recolor frames/buttons normally.
        # No TreeView here.

    # ----------------- Common helpers -----------------
    def _enumerate_versions(self, base):
        from Modules.version_utils import enumerate_versions_cached
        return enumerate_versions_cached(base)

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
        """Scan WoW versions for .bak and .old files in a background thread.
        
        Clears existing tree data, validates WoW path, then spawns a worker thread
        to scan all versions using ThreadPoolExecutor. Results are applied to the
        UI tree incrementally to maintain responsiveness.
        
        Thread Safety:
            - Uses root.after() to schedule UI updates on the main thread
            - Prevents concurrent scans with _file_scan_in_progress flag
            - All UI modifications happen on main thread via callbacks
        
        Side Effects:
            - Clears file_tree widget contents
            - Resets tree_checks and tree_paths dictionaries
            - Updates file_scan_status label during scan
            - Sets _file_scan_in_progress flag during operation
        """
        # Prevent concurrent scans
        if getattr(self, "_file_scan_in_progress", False):
            return
        self._file_scan_in_progress = True
        
        # Clear old tree visually and show scanning status
        for n in self.file_tree.get_children(""):
            self.file_tree.delete(n)
        self.tree_checks.clear()
        self.tree_paths.clear()
        self.tree_select_all_var.set(False)
        try:
            self.file_scan_status.configure(text=localization._("scanning"))
        except Exception:
            pass

        base = self.wow_path_var.get().strip()
        if not base or not os.path.isdir(base):
            self._file_scan_in_progress = False
            messagebox.showerror(localization._("invalid_folder"), localization._("select_valid_wow_first"))
            return

        versions = self._enumerate_versions(base)
        verbose_logger = self if self.verbose_var.get() else None

        def worker():
            results = {}
            # Limit workers to number of versions, cap reasonable upper bound
            max_workers = min(len(versions) or 1, 8)
            try:
                with ThreadPoolExecutor(max_workers=max_workers) as ex:
                    future_map = {
                        ex.submit(scan_bak_old_in_version, vpath, verbose_logger): vlabel
                        for vpath, vlabel in versions
                    }
                    for fut in as_completed(future_map):
                        vlabel = future_map[fut]
                        try:
                            lst = fut.result() or []
                        except Exception:
                            lst = []
                        if lst:
                            results[vlabel] = lst
            except Exception:
                # Fallback to single-threaded on any executor issue
                try:
                    files_by_version = find_bak_old_files(versions, logger=verbose_logger)
                    results.update(files_by_version or {})
                except Exception:
                    pass

            def apply_results():
                # Create parents first
                version_parents = {}
                total_count = 0
                for _vpath, vlabel in versions:
                    v_files = results.get(vlabel, [])
                    if v_files:
                        pid = self._tree_add_parent(vlabel)
                        version_parents[vlabel] = (pid, v_files)
                        total_count += len(v_files)

                # Insert children in chunks to keep UI smooth
                items = []
                for vlabel, (pid, v_files) in version_parents.items():
                    for f in v_files:
                        items.append((pid, f))

                chunk_size = 200
                state = {"idx": 0, "n": len(items)}

                def insert_chunk():
                    end = min(state["idx"] + chunk_size, state["n"])
                    for i in range(state["idx"], end):
                        pid, fpath = items[i]
                        self._tree_add_child_file(pid, fpath)
                    state["idx"] = end
                    if state["idx"] < state["n"]:
                        self.root.after(0, insert_chunk)
                    else:
                        # Close parents and finalize status
                        for pid, _ in version_parents.values():
                            try:
                                self.file_tree.item(pid, open=False)
                            except Exception:
                                pass
                        try:
                            if total_count:
                                self.file_scan_status.configure(text=localization._("found_files_count").format(total_count))
                            else:
                                self.file_scan_status.configure(text=localization._("no_bak_old_found"))
                        except Exception:
                            pass
                        self.log(localization._("file_scan").format(total_count))
                        self._file_scan_in_progress = False

                # Kick off chunked insertion (or finalize immediately)
                if items:
                    self.root.after(0, insert_chunk)
                else:
                    try:
                        self.file_scan_status.configure(text=localization._("no_bak_old_found"))
                    except Exception:
                        pass
                    self.log(localization._("file_scan").format(0))
                    self._file_scan_in_progress = False

            # Schedule UI updates on main thread
            try:
                self.root.after(0, apply_results)
            except Exception:
                # As a last resort, clear the in-progress flag
                self._file_scan_in_progress = False

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def process_selected_files_tree(self):
        """
        Process (delete/trash) selected .bak/.old files from the File Cleaner tab.
        
        Validates game installation integrity before deletion, confirms with user,
        then delegates to backend delete_files(). Refreshes tree on completion.
        
        Side Effects:
            - Shows warning if no files selected
            - Blocks deletion if game installation invalid
            - Prompts user for confirmation dialog
            - Updates tree after deletion
        """
        selected = [
            path
            for iid, path in self.tree_paths.items()
            if self.tree_checks.get(iid, False)
        ]
        if not selected:
            messagebox.showinfo(localization._("no_selection"), localization._("no_files_selected"))
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
            localization._("move_to_trash")
            if use_trash_requested
            else localization._("delete_permanently_action")
        )

        if not messagebox.askyesno(
            localization._("confirm"),
            localization._("confirm_action_files").format(action, len(selected))
        ):
            return

        # Back-end deletion
        processed, permanently_deleted, used_trash = delete_files(
            selected,
            use_trash=use_trash_requested,
            logger=self if self.verbose_var.get() else None,
        )

        self.log(localization._("file_processed").format(processed))
        messagebox.showinfo(localization._("completed"), localization._("processed_files_count").format(processed))

        # Refresh the tree to reflect deletions
        self.scan_files_tree()

    # ------------- Folder Cleaner -------------
    def build_folder_cleaner_tab(self, parent):
        return _build_folder_cleaner_tab(self, parent)

    def _build_single_version_tab(self, tab, version_path, version_label):
        from Modules.Tabs.folder_helpers import build_single_version_tab as _bsv
        return _bsv(self, tab, version_path, version_label)

    def _show_preview(self, canvas: tk.Canvas, path: str):
        try:
            from Modules.Tabs.folder_helpers import show_preview as _show_preview
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
            messagebox.showinfo(localization._("no_selection"), localization._("no_folders_selected"))
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
            localization._("move_to_trash")
            if use_trash_requested
            else localization._("delete_permanently_action")
        )

        if not messagebox.askyesno(
            localization._("confirm"),
            localization._("confirm_action_folders").format(action, len(selected))
        ):
            return

        processed, permanently_deleted, used_trash = clean_folders(
            selected,
            use_trash=use_trash_requested,
            logger=self if self.verbose_var.get() else None
        )

        self.log(localization._("folder_processed").format(processed))
        messagebox.showinfo(localization._("completed"), localization._("processed_folders_count").format(processed))

        # Rebuild UI for this version tab
        # This calls _build_single_version_tab again to refresh the toggles
        self.refresh_folder_cleaner_version(version_label)

    def refresh_folder_cleaner_version(self, version_label):
        """
        Rebuilds a single Folder Cleaner version tab after cleanup.
        """
        # Find the correct tab and frame for the version
        target_frame = None
        target_path = None
        
        for i, (tab_label, tab_path, widgets) in enumerate(self.version_tabs):
            if tab_label == version_label:
                # Get the actual frame widget for this tab
                tab_id = self.version_notebook.tabs()[i]
                target_frame = self.version_notebook.nametowidget(tab_id)
                target_path = tab_path
                break
        
        if not target_frame:
            return  # Version not found (safe fallback)

        # Clear widgets on the tab
        for widget in target_frame.winfo_children():
            widget.destroy()

        # Rebuild the version tab UI
        self._build_single_version_tab(target_frame, target_path, version_label)

    def _toggle_all_screenshot_files(self, shots_vars):
        any_unchecked = any(not v.get() for v in shots_vars.values())
        for v in shots_vars.values():
            v.set(any_unchecked)
        # Update visual appearance for all screenshot checkboxes
        if hasattr(self, 'styled_shot_boxes'):
            for cb in self.styled_shot_boxes:
                cb._sync_image()

    def _reset_screenshot_select_all(self, version_label):
        """Reset the select/deselect all screenshots toggle for a version tab."""
        if hasattr(self, 'version_tabs'):
            for vlabel, vpath, widgets in self.version_tabs:
                if vlabel == version_label and widgets:
                    shots_select_all_var = widgets.get("shots_select_all_var")
                    if shots_select_all_var:
                        shots_select_all_var.set(False)
                    break

    def _process_selected_screenshots(self, version_label, shots_vars):
        """
        Process (delete/trash) selected screenshot files from the Folder Cleaner tab.
        
        Args:
            version_label: Version label (e.g., 'Retail', 'Classic')
            shots_vars: Dictionary mapping file paths to BooleanVar checkboxes
        """
        from tkinter import messagebox
        from Modules.file_cleaner import delete_files
        
        # Get selected screenshot files
        selected = [path for path, var in shots_vars.items() if var.get()]
        
        if not selected:
            messagebox.showinfo(localization._("no_selection"), localization._("no_screenshots_selected"))
            return
        
        # Confirm deletion
        action = localization._("move_to_trash") if self.delete_mode.get() == "trash" else localization._("delete_permanently_action")
        confirm_msg = localization._("confirm_action_screenshots").format(action, len(selected))
        
        if not messagebox.askyesno(localization._("confirm"), confirm_msg):
            return
        
        # Delete files
        use_trash = (self.delete_mode.get() == "trash")
        processed, permanently_deleted, used_trash = delete_files(
            selected,
            use_trash=use_trash,
            logger=self if self.verbose_var.get() else None
        )
        
        self.log(localization._("folder_processed_screenshots").format(version_label, processed))
        
        # Check if Screenshots folder is now empty of image files and delete if so
        if processed > 0:
            # Get the Screenshots folder path for this version
            screenshots_folder = None
            if hasattr(self, 'folder_paths') and version_label in self.folder_paths:
                screenshots_folder = self.folder_paths[version_label].get("Screenshots")
            
            if screenshots_folder and os.path.isdir(screenshots_folder):
                # Check if there are any remaining image files
                try:
                    remaining_images = []
                    for fname in os.listdir(screenshots_folder):
                        fp = os.path.join(screenshots_folder, fname)
                        if os.path.isfile(fp) and fname.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tga", ".gif")):
                            remaining_images.append(fp)
                    
                    # If no image files remain, delete the Screenshots folder
                    if not remaining_images:
                        try:
                            import shutil
                            shutil.rmtree(screenshots_folder)
                            self.log(localization._("folder_deleted_screenshots_folder").format(version_label))
                        except Exception as e:
                            self.log(localization._("folder_delete_screenshots_failed").format(version_label, e))
                except Exception:
                    pass
        
        messagebox.showinfo(localization._("completed"), localization._("processed_screenshots_count").format(processed))
        
        # Reset the select/deselect all toggle
        self._reset_screenshot_select_all(version_label)
        
        # Refresh the tab to reflect deletions
        self.refresh_folder_cleaner_version(version_label)

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
            messagebox.showerror(localization._("invalid_folder"), localization._("select_valid_wow_first"))
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
                text=localization._("found_orphans_count").format(total)
            )
        else:
            self.orphan_scan_status.configure(
                text=localization._("no_orphans_found")
            )

        self.log(localization._("orphan_scan").format(total))

    def process_selected_orphans(self):
        selected = [
            path
            for iid, path in self.orphan_paths.items()
            if self.orphan_checks.get(iid, False)
        ]

        if not selected:
            messagebox.showinfo(localization._("no_selection"), localization._("no_orphans_selected"))
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
            localization._("move_to_trash")
            if use_trash_requested
            else localization._("delete_permanently_action")
        )

        if not messagebox.askyesno(
            localization._("confirm"),
            localization._("confirm_action_orphans").format(action, len(selected))
        ):
            return

        processed, permanently_deleted, used_trash = delete_orphans(
            selected,
            use_trash=use_trash_requested,
            logger=self if self.verbose_var.get() else None,
        )

        self.log(localization._("orphan_processed").format(processed))
        messagebox.showinfo(localization._("completed"), localization._("processed_orphans_count").format(processed))

        # Refresh
        self.scan_orphan_savedvars()

    def rebuild_addons_txt_gui(self):
        base = self.wow_path_var.get().strip()
        if not base or not os.path.isdir(base):
            messagebox.showerror(
                localization._("invalid_folder"), localization._("select_valid_wow_first")
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
            localization._("completed"),
            localization._("rebuilt_addons_summary").format(total_written, total_removed)
        )

    # ------------- Help & Log -------------
    def build_optimization_suggestions_tab(self, parent):
        """Build the Optimization Suggestions tab with manual recommendations."""
        frame = ttk.Frame(parent, padding=10)
        frame.pack(fill="both", expand=True)
        
        # Header with disclaimer
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill="x", pady=(0, 12))
        
        ttk.Label(
            header_frame,
            text=localization._("opt_sug_header"),
            font=(None, 12, "bold")
        ).pack(anchor="w")
        
        # Use tk.Label for disclaimer so we can set theme-aware colors
        # Dark theme uses orange/yellow for warnings, light theme uses red
        is_dark = self.settings.get("theme", "light") == "dark"
        warning_color = "#ff9933" if is_dark else "#cc0000"  # Orange for dark, dark red for light
        bg_color = "#2e2e2e" if is_dark else "#e6e6e6"
        
        self.opt_sug_disclaimer = tk.Label(
            header_frame,
            text=localization._("opt_sug_disclaimer"),
            fg=warning_color,
            bg=bg_color,
            font=(None, 9, "italic"),
            wraplength=max(200, (header_frame.winfo_width() - 40) if header_frame.winfo_width() > 1 else 560),
            justify="left"
        )
        self.opt_sug_disclaimer.pack(anchor="w", pady=(4, 0))
        
        # Update wraplength on resize with margin to prevent text cutoff
        def update_disclaimer_wrap(event):
            self.opt_sug_disclaimer.configure(wraplength=max(200, header_frame.winfo_width() - 40))
        header_frame.bind("<Configure>", update_disclaimer_wrap)
        
        # Create scrollable content area
        canvas = tk.Canvas(frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        content_frame = ttk.Frame(canvas)
        
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Suggestions list
        suggestions = [
            {
                "title": localization._("opt_sug_clean_data_title"),
                "text": localization._("opt_sug_clean_data_text"),
                "tooltip": localization._("opt_sug_clean_data_tooltip")
            },
            {
                "title": localization._("opt_sug_reinstall_title"),
                "text": localization._("opt_sug_reinstall_text"),
                "tooltip": localization._("opt_sug_reinstall_tooltip")
            },
            {
                "title": localization._("opt_sug_hdr_title"),
                "text": localization._("opt_sug_hdr_text"),
                "tooltip": localization._("opt_sug_hdr_tooltip")
            },
            {
                "title": localization._("opt_sug_refresh_title"),
                "text": localization._("opt_sug_refresh_text"),
                "tooltip": localization._("opt_sug_refresh_tooltip")
            },
            {
                "title": localization._("opt_sug_sam_title"),
                "text": localization._("opt_sug_sam_text"),
                "tooltip": localization._("opt_sug_sam_tooltip")
            },
            {
                "title": localization._("opt_sug_xmp_title"),
                "text": localization._("opt_sug_xmp_text"),
                "tooltip": localization._("opt_sug_xmp_tooltip")
            }
        ]
        
        # Create grid with one column per suggestion - spread across full width
        # Use 3 columns per row with padding to avoid scrollbar overlap
        grid_frame = ttk.Frame(content_frame)
        grid_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Don't use uniform sizing - let columns be independent
        # Configure columns with weight but no uniform constraint
        for col in range(3):
            grid_frame.columnconfigure(col, weight=1)
        
        for idx, suggestion in enumerate(suggestions):
            # Calculate row and column for 3-column layout
            row = idx // 3  # Integer division for row
            col = idx % 3   # Modulo for column
            
            # Create column for each suggestion with increased padding
            # Use a container frame to limit width
            container = ttk.Frame(grid_frame)
            container.grid(row=row, column=col, sticky="w", padx=8, pady=10)
            
            column_frame = ttk.Frame(container, relief="ridge", borderwidth=1, padding=15, width=350, height=150)
            column_frame.pack(fill="both", expand=True)
            # Don't use pack_propagate(False) - let height adjust to content
            
            # Title with bullet
            title_label = ttk.Label(
                column_frame,
                text=f"•  {suggestion['title']}",
                font=(None, 10, "bold")
            )
            title_label.pack(anchor="w", fill="x")
            
            # Add tooltip to title with detailed information
            from Modules.ui_helpers import Tooltip
            Tooltip(title_label, suggestion.get('tooltip', 'Click for more information'), app=self)
            
            # Description with dynamic word wrap - set to fixed width minus padding
            desc_label = ttk.Label(
                column_frame,
                text=suggestion['text'],
                wraplength=320,  # Fixed width (350 - 30 for padding)
                justify="left"
            )
            desc_label.pack(anchor="w", padx=(15, 0), pady=(6, 0), fill="both", expand=True)

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
        
        # Button frame for Export and Clear
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(anchor="w", padx=10, pady=6)
        ttk.Button(btn_frame, text=localization._("export_log"), command=self.export_log).pack(side="left")
        ttk.Button(btn_frame, text=localization._("clear_log"), command=self.clear_log).pack(side="left", padx=(8,0))

    def build_help_tab(self, parent):
        outer = ttk.Frame(parent, padding=12)
        outer.pack(fill="both", expand=True)
        card = ttk.Frame(outer, padding=14, relief="groove")
        card.pack(padx=20, pady=20, fill="both", expand=False)
        ttk.Label(card, text=localization._("help_version_label").format(VERSION),
                  font=(None, 14, "bold")).pack(anchor="center", pady=(0, 8))
        ttk.Label(
            card,
            text=localization._("help_about_description"),
            wraplength=500, justify="center"
        ).pack(anchor="center", pady=(0, 8))
        ttk.Label(
            card,
            text=localization._("help_copyright"),
            font=(None, 10, "italic"),
        ).pack(anchor="center", pady=(0, 6))
        
        # GitHub links frame
        github_frame = ttk.Frame(card)
        github_frame.pack(anchor="center", pady=(8, 8))
        
        # GitHub Repository button
        github_repo_btn = ttk.Button(
            github_frame,
            text=f"🔗 {localization._('github_repository')}",
            command=lambda: self._open_url("https://github.com/Myrroddin/wow-cleanup-tool")
        )
        github_repo_btn.pack(side="left", padx=(0, 10))
        
        # GitHub Issues button
        github_issues_btn = ttk.Button(
            github_frame,
            text=f"🐛 {localization._('github_issues')}",
            command=lambda: self._open_url("https://github.com/Myrroddin/wow-cleanup-tool/issues")
        )
        github_issues_btn.pack(side="left", padx=(10, 0))
        
        ttk.Button(card, text=localization._("check_for_updates"), command=self.check_for_updates).pack(anchor="center", pady=(8, 8))
        
        # Donation buttons frame
        donation_frame = ttk.Frame(card)
        donation_frame.pack(anchor="center", pady=(0, 8))
        
        # Patreon button
        patreon_btn = ttk.Button(
            donation_frame,
            text=f"🎨 {localization._('support_patreon')}",
            command=lambda: self._open_url("https://www.patreon.com/c/Myrroddin")
        )
        patreon_btn.pack(side="left", padx=(0, 10))
        
        # PayPal button
        paypal_btn = ttk.Button(
            donation_frame,
            text=f"💳 {localization._('donate_paypal')}",
            command=lambda: self._open_url("https://www.paypal.com/paypalme/PVandersypen")
        )
        paypal_btn.pack(side="left", padx=(10, 0))
    
    def _open_url(self, url):
        """Open a URL in the default web browser."""
        import webbrowser
        try:
            webbrowser.open(url)
        except Exception as e:
            self.log(localization._("failed_to_open_url").format(e), always_log=True)

    # ------------- Path selection + detection -------------
    # Path management methods now delegated to Modules.path_manager
    def select_wow_folder(self):
        path_manager.select_wow_folder(self)

    def _refresh_folder_cleaner_tabs(self):
        path_manager.refresh_folder_cleaner_tabs(self)

    def _find_wow_root(self, path):
        return path_manager.find_wow_root(path)

    def _is_valid_wow_install(self, path):
        return path_manager.is_valid_wow_install(path)

    # ------------- Logging helpers -------------
    def export_log(self):
        """Export the current log to an external text file."""
        try:
            from tkinter import filedialog
            import platform
            
            # Determine default directory (Documents folder)
            default_dir = os.path.expanduser("~")
            if platform.system() == "Windows":
                # Try to get Documents folder on Windows
                try:
                    import ctypes.wintypes
                    CSIDL_PERSONAL = 5
                    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, 0, buf)
                    default_dir = buf.value
                except Exception:
                    default_dir = os.path.join(os.path.expanduser("~"), "Documents")
            elif platform.system() == "Darwin":
                default_dir = os.path.join(os.path.expanduser("~"), "Documents")
            else:
                # Linux/Unix - try common locations
                docs = os.path.join(os.path.expanduser("~"), "Documents")
                if os.path.exists(docs):
                    default_dir = docs
            
            # Get timestamp for default filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"wow_cleanup_log_{timestamp}.txt"
            
            # Ask user where to save
            filepath = filedialog.asksaveasfilename(
                title="Export Log",
                initialdir=default_dir,
                initialfile=default_filename,
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            
            if not filepath:
                return  # User cancelled
            
            # Get log content
            log_lines = self.logger.get_lines()
            if not log_lines:
                messagebox.showinfo(localization._("export_log"), localization._("log_empty_nothing_export"))
                return
            
            # Determine mode
            mode = self.external_log_mode_var.get()
            # Max sessions: 10 for verbose logging (more output), 20 for normal logging
            max_sessions = 10 if self.verbose_var.get() else 20
            
            if mode == "fresh":
                # Fresh mode: overwrite file
                with open(filepath, "w", encoding="utf-8") as f:
                    for line in log_lines:
                        f.write(line + "\n")
            else:
                # Append mode: add to existing file with session limit
                existing_content = ""
                if os.path.exists(filepath):
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            existing_content = f.read()
                    except Exception:
                        existing_content = ""
                
                # Parse existing sessions if file exists
                if existing_content:
                    # Split by session markers
                    session_marker = "=" * 80
                    sessions = []
                    current_session = []
                    
                    for line in existing_content.split("\n"):
                        if line.strip() == session_marker:
                            if current_session:
                                sessions.append("\n".join(current_session))
                                current_session = []
                        current_session.append(line)
                    
                    # Add last session if exists
                    if current_session:
                        sessions.append("\n".join(current_session))
                    
                    # Keep only the most recent (max_sessions - 1) to make room for new session
                    if len(sessions) >= max_sessions:
                        sessions = sessions[-(max_sessions - 1):]
                    
                    # Write back existing sessions
                    with open(filepath, "w", encoding="utf-8") as f:
                        for session in sessions:
                            f.write(session)
                            if not session.endswith("\n"):
                                f.write("\n")
                
                # Append new session with separator
                with open(filepath, "a", encoding="utf-8") as f:
                    f.write("\n" + "="*80 + "\n")
                    f.write(f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*80 + "\n")
                    for line in log_lines:
                        f.write(line + "\n")
            
            messagebox.showinfo(localization._("export_log_title"), localization._("log_exported").format(filepath))
            
        except Exception as e:
            messagebox.showerror(localization._("export_error"), localization._("export_failed").format(str(e)))
    
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

    def log(self, text, always_log=False):
        # If always_log is True, bypass verbose check and log regardless
        if always_log:
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
        else:
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
        if not messagebox.askyesno(localization._("confirm"), localization._("restore_defaults_confirm")):
            return
        try:
            # 1) Reset per-user settings by deleting user settings file
            if os.path.exists(SETTINGS_FILE):
                os.remove(SETTINGS_FILE)
            self.settings = {}

            # 2) Reset global settings to app defaults, while preserving wow_path and hardware_cache
            try:
                current_global = global_settings.load_global_settings()
            except Exception:
                current_global = {}

            preserved_wow_path = current_global.get("wow_path")
            preserved_hw_cache = current_global.get("hardware_cache")

            default_globals = {
                # Defaults for global options
                "check_for_updates": True,
                "verbose_logging": False,
                "delete_mode": "delete",
            }
            # Rebuild globals with preserved keys
            new_globals = dict(default_globals)
            if preserved_wow_path is not None:
                new_globals["wow_path"] = preserved_wow_path
            if preserved_hw_cache is not None:
                new_globals["hardware_cache"] = preserved_hw_cache

            try:
                global_settings.save_global_settings(new_globals)
            except Exception:
                pass
            # Inform user and attempt an automatic restart.
            # Prefer spawning a fresh process then exiting this one; if that fails,
            # fall back to closing the UI and letting the user relaunch manually.
            try:
                messagebox.showinfo(localization._("restored"), localization._("settings_restored_restart"))
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
                    messagebox.showinfo(localization._("restored"), localization._("settings_restored_manual"))
                except Exception:
                    pass
                try:
                    self.root.destroy()
                except Exception:
                    pass
        except Exception as e:
            messagebox.showerror(localization._("error"), localization._("failed_restore_defaults").format(e))

    def check_for_updates(self):
        update_checker.check_for_updates(VERSION, parent_window=self.root)

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
        geometry.save_geometry(self)
        self.settings["wow_path"] = self.wow_path_var.get()
        self.settings["delete_mode"] = self.delete_mode.get()
        # Convert displayed translated values back to English for storage
        theme_display = self.theme_var.get()
        theme = "light"  # default
        if theme_display == localization._("dark"):
            theme = "dark"
        elif theme_display == localization._("light"):
            theme = "light"
        else:
            theme = theme_display.lower()  # fallback
        self.settings["theme"] = theme
        self.settings["language"] = self.language_var.get()
        self.settings["verbose_logging"] = bool(self.verbose_var.get())
        self.settings["check_for_updates"] = bool(self.check_for_updates_var.get())
        self.settings["external_log_mode"] = self.external_log_mode_var.get()
        try:
            self.settings["font_size"] = int(self.font_size_var.get())
        except Exception:
            pass
        try:
            self.settings["font_family"] = self.font_family_var.get()
        except Exception:
            pass
        save_settings(self.settings)
        self.root.destroy()

# -------------------- Run --------------------
def main():
    import tempfile
    
    # Create lock file to prevent multiple instances
    lock_file_path = os.path.join(tempfile.gettempdir(), "wow_cleanup_tool.lock")
    lock_file = None
    
    try:
        # Try to open and lock the file
        lock_file = open(lock_file_path, 'w')
        
        # Platform-specific locking
        if platform.system() == "Windows":
            # On Windows, use msvcrt for file locking
            import msvcrt
            try:
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
            except (IOError, OSError):
                # Lock failed - another instance is running
                # Silently exit without showing any dialog
                lock_file.close()
                sys.exit(0)
        else:
            # On Unix-like systems, use fcntl
            import fcntl
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except (IOError, OSError):
                # Lock failed - another instance is running
                # Silently exit without showing any dialog
                lock_file.close()
                sys.exit(0)
        
        # Lock acquired successfully - start the application
        root = tk.Tk()
        app = WoWCleanupTool(root)
        root.mainloop()
        
    finally:
        # Clean up lock file when application exits
        if lock_file:
            try:
                # Release the lock
                if platform.system() == "Windows":
                    import msvcrt
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                lock_file.close()
                # Remove the lock file
                if os.path.exists(lock_file_path):
                    os.remove(lock_file_path)
            except Exception:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    main()
