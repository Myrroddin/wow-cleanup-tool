"""Main window UI creation for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk


# --- Tooltip Factory ---
class Tooltip:
    # Track all visible tooltips globally
    _visible_tooltips = set()

    def __init__(self, widget, text, theme, font_family, font_size, wraplength=320):
        self.widget = widget
        self.text = text
        self.theme = theme
        self.font_family = font_family
        self.font_size = font_size
        self.wraplength = wraplength
        self.tipwindow = None

    def show(self):
        if self.tipwindow:
            self.hide()
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(True)
        self.tipwindow.wm_geometry(f"+{x}+{y}")
        # Theme-aware colors
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
        # Register this tooltip as visible
        Tooltip._visible_tooltips.add(self)
        self._label = label

    def hide(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
        # Remove from visible tooltips
        Tooltip._visible_tooltips.discard(self)
        self._label = None

    def refresh_theme_and_fonts(self, theme, font_family, font_size):
        """Update the theme and font of the tooltip if visible."""
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

        # Only font/style update logic should be here. All widget creation and layout must be in build().
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

        # Track feature tab indices for enable/disable
        self.feature_tab_indices = []

    def build(self):
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
        self.language_var = tk.StringVar(value=self.loc._("option_language_english"))

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
        wow_path_frame.columnconfigure(0, weight=0)
        wow_path_frame.columnconfigure(1, weight=0)
        wow_path_frame.columnconfigure(2, weight=0)
        wow_path_frame.columnconfigure(3, weight=0)

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

        # Language dropdown (English always first, others sorted alphabetically)
        language_options = [
            (self.loc._("option_language_english"), "en_us"),
            # Add more languages here as (display_name, code)
            # Example: (self.loc._("option_language_french"), "fr_fr"),
        ]
        # If more languages are added, sort them alphabetically by display name, except English first
        if len(language_options) > 1:
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
            width=14,
        )
        language_combo.grid(row=0, column=3, sticky="w", padx=(0, 0))
        language_combo_ttp = (
            self.loc._("tooltip_language_menu")
            if hasattr(self.loc, "_") and "tooltip_language_menu" in self.loc.__dict__
            else "Select application language"
        )
        language_combo.bind(
            "<Enter>", lambda e: self._show_tooltip(language_combo, language_combo_ttp)
        )
        language_combo.bind("<Leave>", lambda e: self._hide_tooltip())

        # Debug prints for wow path row widgets (after all widgets are created)
        print("[DEBUG] WoW Path Row Widget Info:")
        try:
            widgets = [wow_path_label, self.path_entry, browse_btn, language_combo]
            widget_names = [
                "wow_path_label",
                "path_entry",
                "browse_btn",
                "language_combo",
            ]
            for name, widget in zip(widget_names, widgets):
                widget.update_idletasks()
                print(
                    f"  {name}: x={widget.winfo_x()}, y={widget.winfo_y()}, width={widget.winfo_width()}, req_width={widget.winfo_reqwidth()}, grid_info={widget.grid_info()}"
                )
        except Exception as e:
            print(f"[DEBUG] Error printing widget info: {e}")

        # Dynamically set minimum window width to fit all widgets in the WoW path row (including paddings)
        try:
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
        except Exception as e:
            print(f"[DEBUG] Error setting minsize: {e}")

        # Browse button
        def on_browse():
            import tkinter.filedialog as filedialog

            folder = filedialog.askdirectory(title=self.loc._("select_wow_folder"))
            if folder:
                self.wow_path_var.set(folder)

        browse_btn = ttk.Button(
            wow_path_frame, text=self.loc._("btn_browse"), command=on_browse
        )
        browse_btn.grid(row=0, column=2, padx=(8, 0))
        browse_btn_ttp = self.loc._("tooltip_browse_wow_folder")
        browse_btn.bind(
            "<Enter>", lambda e: self._show_tooltip(browse_btn, browse_btn_ttp)
        )
        browse_btn.bind("<Leave>", lambda e: self._hide_tooltip())

        # Language dropdown (English always first, others sorted alphabetically)
        language_options = [
            (self.loc._("option_language_english"), "en_us"),
            # Add more languages here as (display_name, code)
            # Example: (self.loc._("option_language_french"), "fr_fr"),
        ]
        # If more languages are added, sort them alphabetically by display name, except English first
        if len(language_options) > 1:
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
            width=14,
        )
        language_combo.grid(row=0, column=3, padx=(16, 0))
        language_combo_ttp = (
            self.loc._("tooltip_language_menu")
            if hasattr(self.loc, "_") and "tooltip_language_menu" in self.loc.__dict__
            else "Select application language"
        )
        language_combo.bind(
            "<Enter>", lambda e: self._show_tooltip(language_combo, language_combo_ttp)
        )
        language_combo.bind("<Leave>", lambda e: self._hide_tooltip())

        # --- UI Layout ---
        # Add row for delete mode selection (Move to Trash / Delete Permanently)
        delete_mode_frame = ttk.Frame(main_frame)
        delete_mode_frame.grid(row=2, column=0, sticky="w", pady=(0, 6), padx=(0, 0))
        delete_mode_label = ttk.Label(
            delete_mode_frame, text=self.loc._("label_delete_mode")
        )
        delete_mode_label.grid(row=0, column=0, padx=(0, 8), sticky="w")
        trash_rb = ttk.Radiobutton(
            delete_mode_frame,
            text=self.loc._("option_delete_mode_trash"),
            value="trash",
            variable=self.delete_mode_var,
        )
        trash_rb.grid(row=0, column=1, padx=(0, 8), sticky="w")
        permanent_rb = ttk.Radiobutton(
            delete_mode_frame,
            text=self.loc._("option_delete_mode_permanent"),
            value="permanent",
            variable=self.delete_mode_var,
        )
        permanent_rb.grid(row=0, column=2, sticky="w")

        # Add verbose logging checkbox to delete mode row (default on)
        verbose_cb = ttk.Checkbutton(
            delete_mode_frame,
            text=self.loc._("label_verbose_logging"),
            variable=self.verbose_var,
        )
        verbose_cb.grid(row=0, column=3, padx=(16, 0), sticky="w")

        # Add append log checkbox to delete mode row (default off)
        self.append_log_var = tk.BooleanVar(
            value=self.settings.get("append_log", False)
        )
        append_log_cb = ttk.Checkbutton(
            delete_mode_frame,
            text=self.loc._("label_append_log"),
            variable=self.append_log_var,
        )
        append_log_cb.grid(row=0, column=4, padx=(16, 0), sticky="w")
        self.root.update_idletasks()

        # Build UI sections
        path_frame = wow_path_frame

        # --- Create the tabbed log area (feature tabs) ---
        self._create_tabbed_log_area(main_frame, row=3)

        # Log initial message
        self.logger.log(self.loc._("status_app_started"))
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

        # Define tab ids and labels, add log tab
        tabs = [
            ("file_cleaner", self.loc._("tab_file_cleaner")),
            ("folder_cleaner", self.loc._("tab_folder_cleaner")),
            ("game_optimizer", self.loc._("tab_game_optimizer")),
            ("log", self.loc._("tab_log")),
            ("developer", self.loc._("tab_developer")),
        ]
        self.tab_frames = {}
        from core.themes import THEMES

        current_theme = self.settings.get("theme", "dark")
        theme_colors = THEMES.get(current_theme, THEMES["dark"])
        font_family = self.settings.get("font_family", "TkDefaultFont")
        font_size = int(self.settings.get("font_size", 9))

        # --- Use ttk.Notebook for main tabs ---
        self.notebook = ttk.Notebook(parent)
        self.tab_frames = {}
        self.dev_tab_index = None
        for idx, (tab_id, tab_label) in enumerate(tabs):
            frame = ttk.Frame(self.notebook, padding=5)
            self.notebook.add(frame, text=tab_label)
            self.tab_frames[tab_id] = frame
            if tab_id == "developer":
                self.dev_tab_index = idx
        self.notebook.grid(row=row, column=0, sticky="nsew", pady=6)

        # --- Use ttk.Notebook for child tabs in File Cleaner ---
        file_cleaner_frame = self.tab_frames["file_cleaner"]
        child_tabs = [
            ("backup_old_cleaner", self.loc._("tab_backup_old_cleaner")),
            # Add more child tabs here as needed
        ]
        self.child_notebook = ttk.Notebook(file_cleaner_frame)
        self.child_tab_frames = {}
        for tab_id, tab_label in child_tabs:
            frame = ttk.Frame(self.child_notebook, padding=5)
            self.child_notebook.add(frame, text=tab_label)
            self.child_tab_frames[tab_id] = frame
        self.child_notebook.pack(side="top", fill="x", pady=(0, 10))

        # Populate File Cleaner tab (create description and buttons only once)
        file_cleaner_frame = self.child_tab_frames["backup_old_cleaner"]
        if not hasattr(self, "_file_cleaner_content_created"):
            file_cleaner_desc_label = ttk.Label(
                file_cleaner_frame, text=self.loc._("desc_file_cleaner"), justify="left"
            )
            file_cleaner_desc_label.pack(side="top", fill="x", pady=(0, 10))
            button_frame = ttk.Frame(file_cleaner_frame)
            button_frame.pack(side="top", fill="x", pady=(0, 10))
            scan_btn = ttk.Button(
                button_frame,
                text=self.loc._("btn_scan_files"),
                command=self._on_scan_files,
            )
            scan_btn.pack(side="left", padx=(0, 10))
            select_all_btn = ttk.Button(
                button_frame,
                text=self.loc._("btn_select_all_toggle"),
                command=lambda: self._on_select_all_toggle(
                    self.get_selectable_items("file_cleaner")
                ),
            )
            select_all_btn.pack(side="left", padx=(0, 10))
            remove_btn = ttk.Button(
                button_frame,
                text=self.loc._("btn_remove_selected"),
                command=lambda: self._on_remove_selected(
                    self.get_selected_items("file_cleaner")
                ),
            )
            remove_btn.pack(side="left")
            self._file_cleaner_content_created = True

        # --- Populate Developer tab ---
        dev_frame = self.tab_frames["developer"]
        dev_controls = ttk.Frame(dev_frame)
        dev_controls.pack(side="top", fill="x", pady=(0, 5))

        copy_dev_btn = ttk.Button(
            dev_controls, text=self.loc._("btn_copy_log"), command=self._copy_dev_log
        )
        copy_dev_btn.pack(side="left", padx=(0, 5))

        save_dev_btn = ttk.Button(
            dev_controls, text=self.loc._("btn_save_log"), command=self._save_dev_log
        )
        save_dev_btn.pack(side="left", padx=(0, 5))

        self.dev_badge_label = ttk.Label(dev_controls, text="", style="TLabel")
        self.dev_badge_label.pack(side="left", padx=(10, 0))

        dev_text_scroll = ttk.Scrollbar(dev_frame)
        dev_text_scroll.pack(side="right", fill="y")
        self.dev_text = tk.Text(
            dev_frame,
            height=15,
            width=60,
            yscrollcommand=dev_text_scroll.set,
            wrap="word",
            font=(font_family, font_size),
            state="disabled",
        )
        self.dev_text.pack(side="left", fill="both", expand=True)
        dev_text_scroll.config(command=self.dev_text.yview)

        self._configure_dev_log_colors()
        # Attach developer logger to text widget for live updates
        if hasattr(self.logger, "attach_dev_text_widget"):
            self.logger.attach_dev_text_widget(self.dev_text)
        # Ensure color tags are refreshed on theme change
        if hasattr(self, "refresh_dev_log_colors"):
            self.refresh_dev_log_colors()

        # Populate Folder Cleaner tab
        folder_cleaner_frame = self.tab_frames["folder_cleaner"]
        folder_label = ttk.Label(
            folder_cleaner_frame, text="[DEBUG] Folder Cleaner Content"
        )
        folder_label.pack(side="top", fill="x", pady=(0, 10))

        # Populate Game Optimizer tab
        game_optimizer_frame = self.tab_frames["game_optimizer"]
        optimizer_label = ttk.Label(
            game_optimizer_frame, text="[DEBUG] Game Optimizer Content"
        )
        optimizer_label.pack(side="top", fill="x", pady=(0, 10))

        # Populate Log tab
        log_frame = self.tab_frames["log"]
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(side="top", fill="x", pady=(0, 5))

        copy_log_btn = ttk.Button(
            log_controls, text=self.loc._("btn_copy_log"), command=self._copy_user_log
        )
        copy_log_btn.pack(side="left", padx=(0, 5))

        save_log_btn = ttk.Button(
            log_controls, text=self.loc._("btn_save_log"), command=self._save_user_log
        )
        save_log_btn.pack(side="left", padx=(0, 5))

        self.delete_log_btn = ttk.Button(
            log_controls, text=self.loc._("log_delete"), command=self._delete_user_log
        )
        if self.settings.get("append_log", False):
            self.delete_log_btn.pack(side="left", padx=(0, 10))

        text_scroll = ttk.Scrollbar(log_frame)
        text_scroll.pack(side="right", fill="y")
        font_family = self.settings.get("font_family", "TkDefaultFont")
        font_size = self.settings.get("font_size", 9)
        self.log_text = tk.Text(
            log_frame,
            height=15,
            width=60,
            yscrollcommand=text_scroll.set,
            wrap="word",
            font=(font_family, font_size),
            state="disabled",
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        text_scroll.config(command=self.log_text.yview)

        # Attach main logger to text widget using custom handler
        handler = TextWidgetHandler(self.log_text)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(handler)

    def _on_tab_selected(self, tab_id):
        self._show_tab(tab_id)

    def _show_tab(self, tab_id):
        for tid, frame in self.tab_frames.items():
            if tid == tab_id:
                frame.tkraise()

        # Developer Tab
        # Developer tab migration to CustomTabBar is pending. Legacy ttk.Notebook code removed.

    def _configure_dev_log_colors(self):
        """Configure color tags for developer log based on theme."""
        # Get current theme colors
        from core.themes import get_theme_colors

        theme_name = self.settings.get("theme", "light")
        colors = get_theme_colors(theme_name)

        # Configure debug tag (blue/cyan)
        if theme_name == "dark":
            self.dev_text.tag_config("debug", foreground="#6eb4f7")  # Light blue
        else:
            self.dev_text.tag_config("debug", foreground="#0066cc")  # Dark blue

        # Configure error tag (red/orange)
        if theme_name == "dark":
            self.dev_text.tag_config("error", foreground="#ff6b6b")  # Light red
        else:
            self.dev_text.tag_config("error", foreground="#cc0000")  # Dark red

    def _copy_user_log(self):
        """Copy user log to clipboard."""
        user_log = self.log_text.get("1.0", "end-1c")
        if user_log:
            self.root.clipboard_clear()
            self.root.clipboard_append(user_log)
            # Temporary feedback
            import tkinter.messagebox as messagebox

            messagebox.showinfo(self.loc._("btn_copy_log"), self.loc._("log_copied"))

    def _save_user_log(self):
        """Save user log to file."""
        from tkinter import filedialog
        from datetime import datetime

        # Default filename with timestamp
        default_name = f"wow_cleanup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                (self.loc._("file_text_files"), "*.txt"),
                (self.loc._("file_all_files"), "*.*"),
            ],
            initialfile=default_name,
        )

        if file_path:
            try:
                user_log = self.log_text.get("1.0", "end-1c")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(user_log)

                import tkinter.messagebox as messagebox

                messagebox.showinfo(
                    self.loc._("btn_save_log"),
                    self.loc._("btn_log_saved").format(file_path),
                )
            except Exception as e:
                import tkinter.messagebox as messagebox

                messagebox.showerror(self.loc._("error_prefix"), str(e))

    def _delete_user_log(self):
        """Delete the persistent user log file."""
        from core.settings import get_user_log_file
        import tkinter.messagebox as messagebox
        from pathlib import Path

        log_file = get_user_log_file()

        if not log_file.exists():
            return

        try:
            # Respect the delete mode setting
            delete_mode = self.settings.get("delete_mode", "trash")

            if delete_mode == "trash":
                # Move to trash/recycle bin
                from send2trash import send2trash

                send2trash(str(log_file))
            else:
                # Permanent deletion
                log_file.unlink()

            messagebox.showinfo(
                self.loc._("log_delete"), self.loc._("status_log_deleted")
            )
        except Exception as e:
            messagebox.showerror(
                self.loc._("error_prefix"),
                self.loc._("log_delete_error").format(str(e)),
            )

    def _copy_dev_log(self):
        """Copy developer log to clipboard."""
        dev_log = self.logger.get_dev_log()
        if dev_log:
            self.root.clipboard_clear()
            self.root.clipboard_append(dev_log)
            # Temporary feedback
            import tkinter.messagebox as messagebox

            messagebox.showinfo(
                self.loc._("btn_copy_log"), self.loc._("status_log_copied")
            )

    def _save_dev_log(self):
        """Save developer log to file."""
        from tkinter import filedialog
        from datetime import datetime

        # Default filename with timestamp
        default_name = (
            f"wow_cleanup_dev_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                (self.loc._("file_text_files"), "*.txt"),
                (self.loc._("file_all_files"), "*.*"),
            ],
            initialfile=default_name,
        )

        if file_path:
            try:
                dev_log = self.logger.get_dev_log()
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(dev_log)

                import tkinter.messagebox as messagebox

                messagebox.showinfo(
                    self.loc._("btn_save_log"),
                    self.loc._("btn_log_saved").format(file_path),
                )
            except Exception as e:
                import tkinter.messagebox as messagebox

                messagebox.showerror(self.loc._("error_prefix"), str(e))

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
        if self.dev_text:
            self._configure_dev_log_colors()

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
