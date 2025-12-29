"""Main window UI creation for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk
from ui.widgets.tooltip import Tooltip
from ui.log_controls import (
    clear_user_log,
    copy_user_log,
    save_user_log,
    delete_user_log,
    clear_dev_log,
    copy_dev_log,
    save_dev_log,
)
from ui.tabs.file_cleaner_tab import FileCleanerTab
from ui.tabs.folder_cleaner_tab import FolderCleanerTab
from ui.tabs.game_optimizer_tab import GameOptimizerTab
from ui.tabs.log_tab import LogTab
from ui.tabs.developer_tab import DeveloperTab


class MainWindowBuilder:
    def _show_tooltip(self, widget, text):
        # Simple tooltip implementation
        if hasattr(self, "_tooltip_window") and self._tooltip_window:
            return
        x = widget.winfo_rootx() + 20
        y = widget.winfo_rooty() + widget.winfo_height() + 10
        self._tooltip_window = tw = tk.Toplevel(widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("TkDefaultFont", 9),
        )
        label.pack(ipadx=6, ipady=2)

    def _hide_tooltip(self):
        if hasattr(self, "_tooltip_window") and self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None

    def refresh_all_widget_fonts(self):
        """Force refresh of all widget fonts and styles after a font or font size change, including tooltips."""
        import sys
        from core.themes import THEMES

        font_family = self.settings.get("font_family", "TkDefaultFont")
        font_size = int(self.settings.get("font_size", 9))
        theme_name = self.settings.get("theme", "light")
        theme_colors = THEMES.get(theme_name, THEMES["light"])
        # ...removed debug print...
        # Re-apply theme to root (updates ttk styles)
        from core.themes import apply_theme

        apply_theme(self.root, theme_name, font_family, font_size)
        # ...removed debug print...
        # Update ttk styles for all major widget types
        style = ttk.Style()
        widget_types = [
            "TLabel",
            "TButton",
            "TEntry",
            "TCombobox",
            "TCheckbutton",
            "TRadiobutton",
            "Treeview",
            "TNotebook",
            "TFrame",
            "Labelframe",
            "TMenubutton",
            "TScrollbar",
        ]

        # Refresh bug icon if it exists
        self._refresh_bug_icon(font_size)

        # Only font/style update logic should be here. All widget creation and layout must be in build().
        pass

    def _refresh_bug_icon(self, font_size):
        """Refresh the bug icon to match current font size."""
        try:
            from PIL import Image, ImageTk
            from pathlib import Path

            # Determine icon size based on font size
            icon_size = max(16, font_size + 6)

            # Load and resize the bug icon
            icon_path = (
                Path(__file__).parent.parent.parent / "assets" / "icons" / "bug_16.png"
            )
            if icon_path.exists():
                bug_icon = Image.open(icon_path)
                bug_icon = bug_icon.resize(
                    (icon_size, icon_size), Image.Resampling.LANCZOS
                )
                self.bug_icon_photo = ImageTk.PhotoImage(bug_icon)
        except Exception:
            # Silently fail if icon refresh is not possible
            pass

    def add_font_controls(self, parent, on_font_family_changed, on_font_size_changed):
        """Add font family and size controls to the given parent widget."""
        # Font Label
        font_label = ttk.Label(parent, text=self.loc._("label_font"), style="TLabel")
        font_label.grid(row=0, column=4, padx=(8, 0))
        # Font Family Combobox
        system_default_label = self.loc._("system_default_font")
        font_list = self.font_utils.get_available_fonts(system_default_label)
        # Map settings value to UI label
        saved_font = self.settings.get("font_family", "TkDefaultFont")
        if saved_font == "TkDefaultFont":
            initial_font_label = system_default_label
        else:
            initial_font_label = saved_font
        self.font_family_var = tk.StringVar(value=initial_font_label)
        font_combo = ttk.Combobox(
            parent,
            textvariable=self.font_family_var,
            values=font_list,
            state="readonly",
            width=18,
        )
        font_combo.grid(row=0, column=5, padx=(8, 0))
        font_combo.bind("<<ComboboxSelected>>", on_font_family_changed)
        self.font_combo = font_combo
        # Font Size Label
        font_size_label = ttk.Label(
            parent, text=self.loc._("label_font_size"), style="TLabel"
        )
        font_size_label.grid(row=0, column=6, padx=(4, 0))
        # Font Size Combobox
        font_sizes = self.font_utils.get_font_sizes()
        saved_size = str(self.settings.get("font_size", 9))
        self.font_size_var = tk.StringVar(value=saved_size)
        font_size_combo = ttk.Combobox(
            parent,
            textvariable=self.font_size_var,
            values=font_sizes,
            state="readonly",
            width=4,
        )
        font_size_combo.grid(row=0, column=7, padx=(4, 0))
        font_size_combo.bind("<<ComboboxSelected>>", on_font_size_changed)
        self.font_size_combo = font_size_combo
        return font_combo, font_size_combo

    def add_theme_toggle(self, parent, command):
        """Add a toggle theme button to the given parent widget."""
        btn = ttk.Button(
            parent,
            text=self.loc._("btn_toggle_theme"),
            command=command,
            style="TButton",
        )
        btn.grid(row=0, column=3, padx=(8, 0))
        # No tooltip for theme toggle button
        return btn

    def __init__(self, *args, **kwargs):
        def show_tooltip(event):
            """Show tooltip when hovering over a disabled tab."""
            if (
                not hasattr(self, "_tab_tooltip_bindings")
                or not self._tab_tooltip_bindings
            ):
                return
            try:
                elem = self.tabbar.identify(event.x, event.y)
                if elem and hasattr(self.tabbar, "index"):
                    tab_idx = self.tabbar.index(f"@{event.x},{event.y}")
                    if tab_idx in self._tab_tooltip_bindings:
                        if (
                            self._current_tooltip_tab == tab_idx
                            and self._tooltip_window
                        ):
                            return
                        tooltip_text = self._tab_tooltip_bindings[tab_idx]
                        if self._tooltip_window:
                            self._tooltip_window.destroy()
                        from core.themes import THEMES

                        current_theme = self.settings.get("theme", "dark")
                        theme_colors = THEMES.get(current_theme, THEMES["dark"])
                        self._tooltip_window = tk.Toplevel(self.tabbar)
                        self._tooltip_window.wm_overrideredirect(True)
                        self._tooltip_window.wm_geometry(
                            f"+{event.x_root + 10}+{event.y_root + 10}"
                        )
                        label = tk.Label(
                            self._tooltip_window,
                            text=tooltip_text,
                            background=theme_colors.get("tooltip_bg", "#ffffe0"),
                            foreground=theme_colors.get("tooltip_fg", "#000000"),
                            relief="solid",
                            borderwidth=1,
                            font=("TkDefaultFont", 9),
                            padx=8,
                            pady=5,
                            wraplength=300,
                            justify="left",
                        )
                        label.pack()
                        self._current_tooltip_tab = tab_idx
                    else:
                        hide_tooltip(None)
            except Exception:
                pass

        def hide_tooltip(event):
            if self._tooltip_window:
                self._tooltip_window.destroy()
                self._tooltip_window = None
                self._current_tooltip_tab = None

        self.tabbar.bind("<Motion>", show_tooltip)
        self.tabbar.bind("<Leave>", hide_tooltip)
        font_size_label.grid(row=0, column=6, padx=(4, 0))
        # Font Size Combobox
        font_sizes = self.font_utils.get_font_sizes()
        self.font_size_var = tk.StringVar(value=str(self.settings.get("font_size", 9)))
        font_size_combo = ttk.Combobox(
            parent,
            textvariable=self.font_size_var,
            values=font_sizes,
            state="readonly",
            width=4,
        )
        font_size_combo.grid(row=0, column=7, padx=(4, 0))
        font_size_combo.bind("<<ComboboxSelected>>", on_font_size_changed)
        # Store references for controller
        self.font_size_combo = font_size_combo
        return font_combo, font_size_combo

    # add_browse_button is now implemented in build(); stub removed.

    def _on_scan_files(self):
        # TODO: Implement scan files logic
        pass

    def _on_remove_selected(self, selected_items):
        # TODO: Implement remove selected logic for files/folders
        pass

    def get_selected_items(self, context):
        # Placeholder: Return selected items for the given context (e.g., 'file_cleaner', 'folder_cleaner')
        # Replace with actual selection logic
        return []

    def __init__(self, root, loc, settings, logger, font_utils):
        """Initialize the main window builder.
        Args:
            root: Tkinter root window
            loc: Localization instance
            settings: Settings dictionary
            logger: Logger instance
            font_utils: Font utilities module
        """
        self.root = root
        self.loc = loc
        self.settings = settings
        self.logger = logger
        self.font_utils = font_utils
        # self.log_text = None
        # self.dev_text = None
        # self.notebook = None
        # self.feature_tab_indices = []
        self.font_family_var = None
        self.font_combo = None
        self.font_size_var = None
        self.log_text = None
        self.dev_text = None
        self.dev_tab_index = None
        self.dev_badge_label = None
        self.wow_path_var = None
        self.path_entry = None
        self.bug_icon_photo = None  # Store reference to bug icon PhotoImage

        # Track feature tab indices for enable/disable
        self.feature_tab_indices = []

    def build(self, theme_toggle_callback=None):
        # from ui.custom_tabbar import CustomTabBar  # Already imported at top

        """Build and return the main window UI components.
        Returns:
            dict: Dictionary containing references to key UI components
        """
        import sys

        # Initialize font StringVars early
        system_default_label = self.loc._("system_default_font")
        current_font = self.settings.get("font_family", "TkDefaultFont")
        if current_font == "TkDefaultFont":
            self.font_family_var = tk.StringVar(value=system_default_label)
        else:
            self.font_family_var = tk.StringVar(value=current_font)
        self.font_size_var = tk.StringVar(value=str(self.settings.get("font_size", 9)))

        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.rowconfigure(0, weight=0)  # Title
        main_frame.rowconfigure(1, weight=0)  # WoW path
        main_frame.rowconfigure(2, weight=0)  # Delete mode row does not expand
        main_frame.rowconfigure(3, weight=0)  # Tab bar does not expand
        main_frame.rowconfigure(4, weight=1)  # Tab content expands vertically
        main_frame.columnconfigure(0, weight=1)  # Ensure tab bar expands horizontally

        # Initialize delete mode StringVar
        self.delete_mode_var = tk.StringVar(
            value=self.settings.get("delete_mode", "trash")
        )

        # Initialize verbose logging BooleanVar
        self.verbose_var = tk.BooleanVar(
            value=self.settings.get("verbose_logging", True)
        )

        # (Debug prints for wow_path_label must only appear after assignment)
        self._create_tabbed_log_area(main_frame, row=3)
        self.append_log_var = tk.BooleanVar(
            value=self.settings.get("append_log", False)
        )

        # Initialize language StringVar with display name
        self.language_var = tk.StringVar(value="English (US)")

        # (Debug prints for detected_path and valid must only appear after assignment)
        # Main frame already created above
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # --- Main Title ---
        title_label = ttk.Label(
            main_frame,
            text=self.loc._("title_main_window"),
            anchor="center",
            style="Title.TLabel",
        )
        title_label.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)
        # --- End Main Title ---

        # WoW path field will be row=1

        # --- WoW Path Field, Browse Button, and Language Dropdown ---
        from wow.path_manager import PathManager

        wow_path_frame = ttk.Frame(main_frame)
        wow_path_frame.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        # Ensure wow_path_frame expands horizontally
        main_frame.columnconfigure(0, weight=1)
        for i in range(8):
            wow_path_frame.columnconfigure(i, weight=0)

        wow_path_label = ttk.Label(
            wow_path_frame, text=self.loc._("label_wow_installation_path")
        )
        wow_path_label.grid(row=0, column=0, sticky="w", padx=(0, 12))

        # Auto-detect WoW path
        path_manager = PathManager(self.loc)
        detected_path = path_manager.detect_wow_path()
        valid = (
            path_manager.validate_wow_path(detected_path) if detected_path else False
        )
        wow_path_value = detected_path if valid else ""

        self.wow_path_var = tk.StringVar(value=wow_path_value)
        self.path_entry = ttk.Entry(
            wow_path_frame, textvariable=self.wow_path_var, width=24
        )
        self.path_entry.grid(row=0, column=1, sticky="w", padx=(0, 12))
        self.root.update_idletasks()

        # Browse button
        def on_browse():
            import tkinter.filedialog as filedialog

            folder = filedialog.askdirectory(title=self.loc._("select_wow_folder"))
            if folder:
                self.wow_path_var.set(folder)

        browse_btn = ttk.Button(
            wow_path_frame, text=self.loc._("btn_browse"), command=on_browse
        )
        browse_btn.grid(row=0, column=2, sticky="w", padx=(0, 12))
        browse_btn_ttp = self.loc._("tooltip_browse_wow_folder")
        browse_btn.bind(
            "<Enter>", lambda e: self._show_tooltip(browse_btn, browse_btn_ttp)
        )
        browse_btn.bind("<Leave>", lambda e: self._hide_tooltip())

        # Language dropdown (English always first, others sorted alphabetically, native names)
        language_options = [
            ("English (US)", "en_us"),
            ("Deutsch", "de_de"),
            ("Français", "fr_fr"),
            ("Italiano", "it_it"),
            ("Русский", "ru_ru"),
            ("繁體中文", "zh_tw"),
            ("简体中文", "zh_cn"),
            ("Português (Brasil)", "pt_br"),
            ("Español (EU)", "es_es"),
            ("Español (Latinoamérica)", "es_mx"),
            ("Українська", "uk_ua"),
            ("한국어", "ko_kr"),
        ]
        # Sort all except English alphabetically by display name
        english = language_options[0]
        other_langs = sorted(language_options[1:], key=lambda x: x[0].lower())
        language_options = [english] + other_langs
        language_names = [name for name, code in language_options]
        self.language_var = tk.StringVar(value=language_names[0])
        language_combo = ttk.Combobox(
            wow_path_frame,
            textvariable=self.language_var,
            values=language_names,
            state="readonly",
            width=20,
        )
        language_combo.grid(row=0, column=3, sticky="w", padx=(0, 12))

        # Theme toggle button (column 4)
        theme_btn = ttk.Button(
            wow_path_frame,
            text=self.loc._("btn_toggle_theme"),
            command=theme_toggle_callback,
            style="TButton",
        )
        theme_btn.grid(row=0, column=4, padx=(0, 12))

        # Font label (column 5)
        font_label = ttk.Label(
            wow_path_frame, text=self.loc._("label_font"), style="TLabel"
        )
        font_label.grid(row=0, column=5, padx=(0, 12))

        # Font family combobox (column 6)
        system_default_label = self.loc._("system_default_font")
        font_list = self.font_utils.get_available_fonts(system_default_label)
        saved_font = self.settings.get("font_family", "TkDefaultFont")
        initial_font_label = (
            system_default_label if saved_font == "TkDefaultFont" else saved_font
        )
        self.font_family_var = tk.StringVar(value=initial_font_label)
        font_combo = ttk.Combobox(
            wow_path_frame,
            textvariable=self.font_family_var,
            values=font_list,
            state="readonly",
            width=18,
        )
        font_combo.grid(row=0, column=6, padx=(0, 12))
        self.font_combo = font_combo

        # Font size label (column 7)
        font_size_label = ttk.Label(
            wow_path_frame, text=self.loc._("label_font_size"), style="TLabel"
        )
        font_size_label.grid(row=0, column=7, padx=(0, 12))

        # Font size combobox (column 8)
        font_sizes = self.font_utils.get_font_sizes()
        saved_size = str(self.settings.get("font_size", 9))
        self.font_size_var = tk.StringVar(value=saved_size)
        font_size_combo = ttk.Combobox(
            wow_path_frame,
            textvariable=self.font_size_var,
            values=font_sizes,
            state="readonly",
            width=4,
        )
        font_size_combo.grid(
            row=0, column=8, padx=(0, 0)
        )  # Last widget: no right padding
        self.font_size_combo = font_size_combo
        language_combo_ttp = self.loc._("tooltip_language_menu")
        language_combo.bind(
            "<Enter>", lambda e: self._show_tooltip(language_combo, language_combo_ttp)
        )
        language_combo.bind("<Leave>", lambda e: self._hide_tooltip())

        # Debug prints for wow path row widgets (after all widgets are created)
        # ...debug prints removed...

        # Dynamically set minimum window width to fit all widgets in the WoW path row (including paddings)
        total_width = 0
        paddings = [(0, 12), (0, 12), (0, 12), (0, 0)]
        for widget, pad in zip(
            [wow_path_label, self.path_entry, browse_btn, language_combo], paddings
        ):
            widget.update_idletasks()
            total_width += widget.winfo_reqwidth() + sum(pad)
        # Add a little extra for spacing
        min_width = total_width + 20
        self.root.minsize(min_width, self.root.winfo_height())
        # ...debug prints removed...

        # --- UI Layout ---
        # Add row for delete mode selection (Move to Trash / Delete Permanently)
        delete_mode_frame = ttk.Frame(main_frame)
        delete_mode_frame.grid(row=2, column=0, sticky="w", pady=(0, 6), padx=(0, 0))
        for i in range(5):
            delete_mode_frame.columnconfigure(i, weight=0)
        delete_mode_label = ttk.Label(
            delete_mode_frame, text=self.loc._("label_delete_mode")
        )
        delete_mode_label.grid(row=0, column=0, padx=(0, 12), sticky="w")
        trash_rb = ttk.Radiobutton(
            delete_mode_frame,
            text=self.loc._("option_delete_mode_trash"),
            value="trash",
            variable=self.delete_mode_var,
        )
        trash_rb.grid(row=0, column=1, padx=(0, 12), sticky="w")
        permanent_rb = ttk.Radiobutton(
            delete_mode_frame,
            text=self.loc._("option_delete_mode_permanent"),
            value="permanent",
            variable=self.delete_mode_var,
        )
        permanent_rb.grid(row=0, column=2, padx=(0, 12), sticky="w")

        # Add verbose logging checkbox to delete mode row (default on)
        verbose_cb = ttk.Checkbutton(
            delete_mode_frame,
            text=self.loc._("label_verbose_logging"),
            variable=self.verbose_var,
        )
        verbose_cb.grid(row=0, column=3, padx=(0, 12), sticky="w")
        # Add tooltip to verbose logging checkbox
        verbose_cb_ttp = self.loc._("tooltip_user_log_only")
        verbose_cb.bind(
            "<Enter>", lambda e: self._show_tooltip(verbose_cb, verbose_cb_ttp)
        )
        verbose_cb.bind("<Leave>", lambda e: self._hide_tooltip())

        # Add chat timestamps checkbox to delete mode row (default on)
        self.chat_timestamps_var = tk.BooleanVar(
            value=self.settings.get("chat_timestamps", True)
        )

        def on_chat_timestamps_toggle():
            # Update log formatter dynamically
            if hasattr(self.logger, "set_timestamps_enabled"):
                self.logger.set_timestamps_enabled(self.chat_timestamps_var.get())

        chat_timestamps_cb = ttk.Checkbutton(
            delete_mode_frame,
            text=self.loc._("label_log_timestamps"),
            variable=self.chat_timestamps_var,
            command=on_chat_timestamps_toggle,
        )
        chat_timestamps_cb.grid(row=0, column=5, padx=(0, 12), sticky="w")
        chat_timestamps_cb_ttp = self.loc._("tooltip_log_timestamps")
        chat_timestamps_cb.bind(
            "<Enter>",
            lambda e: self._show_tooltip(chat_timestamps_cb, chat_timestamps_cb_ttp),
        )
        chat_timestamps_cb.bind("<Leave>", lambda e: self._hide_tooltip())

        # Add append log checkbox to delete mode row (default off)
        self.append_log_var = tk.BooleanVar(
            value=self.settings.get("append_log", False)
        )
        append_log_cb = ttk.Checkbutton(
            delete_mode_frame,
            text=self.loc._("label_append_log"),
            variable=self.append_log_var,
        )
        append_log_cb.grid(row=0, column=4, padx=(0, 12), sticky="w")
        # Add tooltip to append log checkbox
        append_log_cb_ttp = self.loc._("tooltip_user_log_only")
        append_log_cb.bind(
            "<Enter>", lambda e: self._show_tooltip(append_log_cb, append_log_cb_ttp)
        )
        append_log_cb.bind("<Leave>", lambda e: self._hide_tooltip())

        # Add reset settings button (now column 6, no right padding)
        def on_reset_settings():
            from core.settings import load_settings, save_settings

            # Reload defaults
            defaults = load_settings.__globals__["load_settings"]()
            # Remove wow_path from reset (preserve current path if set)
            wow_path = self.wow_path_var.get() if self.wow_path_var else None
            if wow_path:
                defaults["wow_path"] = wow_path
            save_settings(defaults)
            # Update all UI elements to reflect defaults
            self.settings.clear()
            self.settings.update(defaults)
            # Language
            self.language_var.set("English (US)")
            # Theme
            from core.themes import apply_theme

            theme_name = self.settings.get("theme", "light")
            font_family = self.settings.get("font_family", "TkDefaultFont")
            font_size = int(self.settings.get("font_size", 9))
            apply_theme(self.root, theme_name, font_family, font_size)
            # Font family and size
            system_default_label = self.loc._("system_default_font")
            if font_family == "TkDefaultFont":
                self.font_family_var.set(system_default_label)
            else:
                self.font_family_var.set(font_family)
            self.font_size_var.set(str(font_size))
            # Delete mode
            self.delete_mode_var.set(self.settings.get("delete_mode", "trash"))
            # Verbose logging
            self.verbose_var.set(self.settings.get("verbose_logging", True))
            # Append log
            self.append_log_var.set(self.settings.get("append_log", False))
            # Chat timestamps
            self.chat_timestamps_var.set(self.settings.get("chat_timestamps", True))
            # Refresh all widget fonts and theme
            self.refresh_all_widget_fonts()
            # Optionally, show a message to the user
            import tkinter.messagebox as messagebox

            messagebox.showinfo(
                self.loc._("btn_reset_settings"),
                self.loc._("btn_reset_settings") + " applied.",
            )

        # Add reset settings button (column 6, with consistent padding)
        reset_btn = ttk.Button(
            delete_mode_frame,
            text=self.loc._("btn_reset_settings"),
            command=on_reset_settings,
            style="TButton",
        )
        reset_btn.grid(row=0, column=6, padx=(0, 12), sticky="w")

        # Add bug report button (column 7, with bug icon and consistent padding)
        def on_bug_report():
            import webbrowser

            webbrowser.open_new("https://github.com/Myrroddin/wow-cleanup-tool/issues")

        # Use ttk.Button with emoji icon (simple and reliable)
        # The emoji will scale with the font size automatically
        bug_btn = ttk.Button(
            delete_mode_frame,
            text="🐞 " + self.loc._("btn_bug_report"),
            command=on_bug_report,
            style="TButton",
        )

        bug_btn.grid(row=0, column=7, padx=(0, 0), sticky="w")
        self.root.update_idletasks()

        # Build UI sections
        path_frame = wow_path_frame

        # --- Create the tabbed log area (feature tabs) ---
        self._create_tabbed_log_area(main_frame, row=3)

        # After building, force font/theme refresh to apply persisted settings
        self.refresh_all_widget_fonts()
        # Return references to important widgets
        return {
            "path_frame": wow_path_frame,
            "wow_path_var": self.wow_path_var,
            "path_entry": self.path_entry,
            "font_family_var": self.font_family_var,
            "font_size_var": self.font_size_var,
            "font_combo": getattr(self, "font_combo", None),
            "font_size_combo": getattr(self, "font_size_combo", None),
            "append_log_var": self.append_log_var,
            "language_var": self.language_var,
            "delete_mode_var": self.delete_mode_var,
            "verbose_var": self.verbose_var,
            "reset_button": None,  # Stub for legacy reset_button
        }

    # _create_title is now implemented in build(); stub removed.

    def _create_tabbed_log_area(self, parent, row=2):
        from ui.text_widget_handler import TextWidgetHandler
        import logging
        from core.themes import THEMES

        # Tab definitions
        tabs = [
            ("file_cleaner", self.loc._("tab_file_cleaner")),
            ("folder_cleaner", self.loc._("tab_folder_cleaner")),
            ("game_optimizer", self.loc._("tab_game_optimizer")),
            ("log", self.loc._("tab_log")),
            ("developer", self.loc._("tab_developer")),
        ]
        self.tab_frames = {}
        self.notebook = ttk.Notebook(parent)
        self.dev_tab_index = None
        for idx, (tab_id, tab_label) in enumerate(tabs):
            frame = ttk.Frame(self.notebook, padding=5)
            tab_pad = (0, 12) if idx < len(tabs) - 1 else (0, 0)
            self.notebook.add(frame, text=tab_label, padding=tab_pad)
            self.tab_frames[tab_id] = frame
            if tab_id == "developer":
                self.dev_tab_index = idx
        self.notebook.grid(row=row, column=0, sticky="nsew", pady=6)

        # File Cleaner Tab (with child notebook)
        file_cleaner_tab = FileCleanerTab(
            self.tab_frames["file_cleaner"],
            self.loc,
            self._on_scan_files,
            getattr(self, "_on_select_all_toggle", lambda items: None),
            self._on_remove_selected,
            getattr(self, "get_selectable_items", lambda ctx: []),
            self.get_selected_items,
        )
        file_cleaner_tab.frame.pack(fill="both", expand=True)

        # Folder Cleaner Tab
        folder_cleaner_tab = FolderCleanerTab(
            self.tab_frames["folder_cleaner"], self.loc
        )
        folder_cleaner_tab.frame.pack(fill="both", expand=True)

        # Game Optimizer Tab
        game_optimizer_tab = GameOptimizerTab(
            self.tab_frames["game_optimizer"], self.loc
        )
        game_optimizer_tab.frame.pack(fill="both", expand=True)

        # Log Tab
        log_tab = LogTab(
            self.tab_frames["log"],
            self.loc,
            log_controls={
                "clear": lambda: clear_user_log(self.log_text),
                "copy": lambda: copy_user_log(self.root, self.log_text, self.loc),
                "save": lambda: save_user_log(self.log_text, self.loc),
                "delete": lambda: delete_user_log(self.settings, self.loc),
            },
        )
        log_tab.frame.pack(fill="both", expand=True)
        # Store reference to log text widget
        self.log_text = log_tab.log_text
        # Attach logger to user log text widget
        self.logger.attach_text_widget(self.log_text)

        # Load previous user log if append mode is enabled
        if self.settings.get("append_log", False):
            from core.settings import load_user_log

            previous_log = load_user_log()
            if previous_log:
                # Find the log_text widget in the log tab
                for child in self.tab_frames["log"].winfo_children():
                    if isinstance(child, tk.Text):
                        child.configure(state="normal")
                        child.insert("1.0", previous_log + "\n")
                        child.configure(state="disabled")
                        break

        # Developer Tab
        developer_tab = DeveloperTab(
            self.tab_frames["developer"],
            self.loc,
            log_controls={
                "clear": lambda: clear_dev_log(self.dev_text),
                "copy": lambda: copy_dev_log(self.root, self.logger, self.loc),
                "save": lambda: save_dev_log(self.logger, self.loc),
            },
        )
        developer_tab.frame.pack(fill="both", expand=True)
        # Store reference to developer log text widget
        self.dev_text = developer_tab.log_text
        # Attach logger to developer log text widget
        self.logger.attach_dev_text_widget(self.dev_text)

    # Log control methods are now imported from ui.log_controls

    # Tab UI creation is now handled by separate tab classes in ui.tabs

    def _update_error_badge(self, count):
        """Update error badge on developer tab.

        Args:
            count: Number of errors
        """
        if count > 0:
            self.dev_badge_label.config(text=f"🔴 {count}")
            # Update tab text to include badge
            self.notebook.tab(
                self.dev_tab_index, text=f"{self.loc._('tab_developer')} 🔴 {count}"
            )
        else:
            self.dev_badge_label.config(text="")
            self.notebook.tab(self.dev_tab_index, text=self.loc._("tab_developer"))

    def refresh_dev_log_colors(self):
        """Refresh developer log color tags when theme changes."""
        # Dev log colors are handled by the logger; no special widget-level configuration needed
        pass

    def _setup_tab_tooltip_handler(self):
        """Set up tooltip display for disabled tabs."""
        self._tooltip_window = None
        self._current_tooltip_tab = None

        def show_tooltip(event):
            """Show tooltip when hovering over a disabled tab."""
            if (
                not hasattr(self, "_tab_tooltip_bindings")
                or not self._tab_tooltip_bindings
            ):
                return

            # Identify which tab is under the cursor
            try:
                elem = self.notebook.identify(event.x, event.y)
                if elem and hasattr(self.notebook, "index"):
                    # elem format: "tab@x,y" or similar - try to extract tab index
                    tab_idx = self.notebook.index(f"@{event.x},{event.y}")

                    # Only show tooltip if tab is in bindings (disabled tabs only)
                    if tab_idx in self._tab_tooltip_bindings:
                        # Don't recreate if already showing for this tab
                        if (
                            self._current_tooltip_tab == tab_idx
                            and self._tooltip_window
                        ):
                            return

                        tooltip_text = self._tab_tooltip_bindings[tab_idx]

                        # Destroy existing tooltip
                        if self._tooltip_window:
                            self._tooltip_window.destroy()

                        # Get current theme colors
                        from core.themes import THEMES

                        current_theme = self.settings.get("theme", "dark")
                        theme_colors = THEMES.get(current_theme, THEMES["dark"])

                        # Create tooltip window
                        self._tooltip_window = tk.Toplevel(self.notebook)
                        self._tooltip_window.wm_overrideredirect(True)
                        self._tooltip_window.wm_geometry(
                            f"+{event.x_root + 10}+{event.y_root + 10}"
                        )

                        # Create label with word wrapping (max width ~300px)
                        self._tooltip_window.configure(
                            bg=theme_colors.get("tooltip_bg", "#ffffe0")
                        )
                        label = tk.Label(
                            self._tooltip_window,
                            text=tooltip_text,
                            background=theme_colors.get("tooltip_bg", "#ffffe0"),
                            foreground=theme_colors.get("tooltip_fg", "#000000"),
                            relief="solid",
                            borderwidth=1,
                            font=("TkDefaultFont", 9),
                            padx=8,
                            pady=5,
                            wraplength=300,
                            justify="left",
                        )
                        label.pack()
                        self._current_tooltip_tab = tab_idx
                    else:
                        # Not hovering over a disabled tab, hide tooltip
                        hide_tooltip(None)
            except Exception:
                pass

        def hide_tooltip(event):
            """Hide tooltip when cursor leaves."""
            if self._tooltip_window:
                self._tooltip_window.destroy()
                self._tooltip_window = None
                self._current_tooltip_tab = None

        # Bind hover events to notebook
        self.notebook.bind("<Motion>", show_tooltip)
        self.notebook.bind("<Leave>", hide_tooltip)

    def set_feature_tabs_enabled(self, enabled):
        """Enable or disable feature tabs based on WoW path validity.

        Args:
            enabled: True to enable tabs, False to disable
        """
        state = "normal" if enabled else "disabled"
        if not hasattr(self, "_tab_tooltip_bindings"):
            self._tab_tooltip_bindings = {}
        for tab_idx in self.feature_tab_indices:
            self.tabbar.tab(tab_idx, state=state)
            if enabled:
                if tab_idx in self._tab_tooltip_bindings:
                    del self._tab_tooltip_bindings[tab_idx]
            else:
                self._tab_tooltip_bindings[tab_idx] = self.loc._("tab_disabled_tooltip")
        if hasattr(self, "_tooltip_window") and self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None
            self._current_tooltip_tab = None
