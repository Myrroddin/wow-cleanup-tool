"""Main window UI creation for WoW Cleanup Tool."""
import tkinter as tk
from tkinter import ttk


class MainWindowBuilder:
    """Builder class for constructing the main application window UI."""
    
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
        
        # Widget references to be populated
        self.wow_path_var = None
        self.path_entry = None
        self.font_family_var = None
        self.font_combo = None
        self.font_size_var = None
        self.log_text = None
        self.dev_text = None
        self.notebook = None
        self.dev_tab_index = None
        self.dev_badge_label = None
        
        # Track feature tab indices for enable/disable
        self.feature_tab_indices = []
    
    def build(self):
        """Build and return the main window UI components.
        
        Returns:
            dict: Dictionary containing references to key UI components
        """
        # Initialize font StringVars early
        system_default_label = self.loc._("system_default_font")
        current_font = self.settings.get('font_family', 'TkDefaultFont')
        display_value = system_default_label if current_font == 'TkDefaultFont' else current_font
        self.font_family_var = tk.StringVar(value=display_value)
        self.font_size_var = tk.StringVar(value=str(self.settings.get('font_size', 9)))
        
        # Initialize delete mode StringVar
        self.delete_mode_var = tk.StringVar(value=self.settings.get('delete_mode', 'trash'))
        
        # Initialize verbose logging BooleanVar
        self.verbose_var = tk.BooleanVar(value=self.settings.get('verbose_logging', True))
        
        # Initialize append log BooleanVar
        self.append_log_var = tk.BooleanVar(value=self.settings.get('append_log', False))
        
        # Initialize language StringVar with display name
        self.language_var = tk.StringVar(value=self.loc._("option_language_english"))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # Log area expands vertically
        
        # Build UI sections
        self._create_title(main_frame)
        path_frame = self._create_toolbar(main_frame)
        self._create_tabbed_log_area(main_frame)
        
        # Log initial message
        self.logger.log(self.loc._("status_app_started"))
        
        # Return references to important widgets
        return {
            'path_frame': path_frame,
            'wow_path_var': self.wow_path_var,
            'path_entry': self.path_entry,
            'font_family_var': self.font_family_var,
            'font_combo': self.font_combo,
            'font_size_var': self.font_size_var,
            'delete_mode_var': self.delete_mode_var,
            'verbose_var': self.verbose_var,
            'append_log_var': self.append_log_var,
            'language_var': self.language_var,
            'language_combo': self.language_combo,
            'reset_button': self.reset_button,
            'log_text': self.log_text,
            'dev_text': self.dev_text,
            'notebook': self.notebook,
        }
    
    def _create_title(self, parent):
        """Create the title label.
        
        Args:
            parent: Parent widget
        """
        title = ttk.Label(parent, text=self.loc._("title_main_window"), style='Title.TLabel')
        title.grid(row=0, column=0, pady=(0, 10))
    
    def _create_toolbar(self, parent):
        """Create the toolbar with WoW path, theme toggle, and font controls.
        
        Args:
            parent: Parent widget
            
        Returns:
            ttk.Frame: The toolbar frame
        """
        toolbar_container = ttk.Frame(parent)
        toolbar_container.grid(row=1, column=0, pady=(0, 10))
        
        # First row - WoW path, browse, theme, and font controls (left-aligned)
        path_frame = ttk.Frame(toolbar_container)
        path_frame.grid(row=0, column=0, sticky='w')
        
        # WoW path label
        path_label = ttk.Label(path_frame, text=self.loc._("label_wow_installation_path"))
        path_label.grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        # WoW path entry (read-only) - dynamically sized based on path length
        self.wow_path_var = tk.StringVar(value=self.settings.get('wow_path', ''))
        wow_path = self.settings.get('wow_path', '')
        # Set width based on path length, minimum is the shortest possible WoW path
        min_wow_path = len(r'C:\World of Warcraft')  # 20 characters
        entry_width = min(max(len(wow_path) if wow_path else min_wow_path, min_wow_path), 60)
        self.path_entry = ttk.Entry(path_frame, textvariable=self.wow_path_var, 
                                     state='readonly', width=entry_width)
        self.path_entry.grid(row=0, column=1, padx=(0, 5))
        
        # Second row - Delete mode and logging options (left-aligned)
        options_frame = ttk.Frame(toolbar_container)
        options_frame.grid(row=1, column=0, sticky='w', pady=(5, 0))
        self._create_delete_mode_toggle(options_frame)
        
        return path_frame
    
    def add_browse_button(self, path_frame, command):
        """Add browse button to toolbar.
        
        Args:
            path_frame: Toolbar frame
            command: Command callback for browse button
        """
        browse_button = ttk.Button(path_frame, text=self.loc._("btn_browse"), command=command)
        browse_button.grid(row=0, column=2, padx=(0, 5))
    
    def add_theme_toggle(self, path_frame, command):
        """Add theme toggle button to toolbar.
        
        Args:
            path_frame: Toolbar frame
            command: Command callback for theme toggle
        """
        theme_button = ttk.Button(path_frame, text=self.loc._("btn_toggle_theme"), command=command)
        theme_button.grid(row=0, column=3, padx=(0, 5))
    
    def add_font_controls(self, path_frame, font_family_callback, font_size_callback):
        """Add font selection controls to toolbar.
        
        Args:
            path_frame: Toolbar frame
            font_family_callback: Callback for font family changes
            font_size_callback: Callback for font size changes
        """
        # Font label
        font_label = ttk.Label(path_frame, text=self.loc._("label_font"))
        font_label.grid(row=0, column=4, sticky='w', padx=(0, 5))
        
        # Font family combobox (StringVar already created in build())
        system_default_label = self.loc._("system_default_font")
        font_families = self.font_utils.get_available_fonts(default_label=system_default_label)
        
        self.font_combo = ttk.Combobox(path_frame, textvariable=self.font_family_var,
                                       values=font_families, width=20, state='readonly')
        self.font_combo.grid(row=0, column=5, padx=(0, 5))
        self.font_combo.bind('<<ComboboxSelected>>', font_family_callback)
        
        # Font size label
        font_size_label = ttk.Label(path_frame, text=self.loc._("label_font_size"))
        font_size_label.grid(row=0, column=6, sticky='w', padx=(0, 5))
        
        # Font size combobox (StringVar already created in build())
        font_size_combo = ttk.Combobox(path_frame, textvariable=self.font_size_var, 
                                       values=self.font_utils.get_font_sizes(), width=5, state='readonly')
        font_size_combo.grid(row=0, column=7)
        font_size_combo.bind('<<ComboboxSelected>>', font_size_callback)
    
    def _create_delete_mode_toggle(self, parent):
        """Create delete mode radio buttons.
        
        Args:
            parent: Parent widget
        """
        # Delete mode label
        mode_label = ttk.Label(parent, text=self.loc._("label_delete_mode"))
        mode_label.grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        # Trash radio button (default)
        trash_radio = ttk.Radiobutton(
            parent,
            text=self.loc._("option_delete_mode_trash"),
            variable=self.delete_mode_var,
            value='trash'
        )
        trash_radio.grid(row=0, column=1, sticky='w', padx=(0, 10))
        
        # Permanent delete radio button
        permanent_radio = ttk.Radiobutton(
            parent,
            text=self.loc._("option_delete_mode_permanent"),
            variable=self.delete_mode_var,
            value='permanent'
        )
        permanent_radio.grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        # Verbose logging checkbox (for detailed operation messages)
        verbose_check = ttk.Checkbutton(
            parent,
            text=self.loc._("label_verbose_logging"),
            variable=self.verbose_var
        )
        verbose_check.grid(row=0, column=3, sticky='w', padx=(20, 10))
        
        # Append log checkbox (preserve log across sessions)
        append_check = ttk.Checkbutton(
            parent,
            text=self.loc._("label_append_log"),
            variable=self.append_log_var
        )
        append_check.grid(row=0, column=4, sticky='w', padx=(10, 10))
        
        # Language selector
        language_label = ttk.Label(parent, text=self.loc._("label_language"))
        language_label.grid(row=0, column=5, sticky='w', padx=(20, 5))
        
        self.language_combo = ttk.Combobox(
            parent,
            textvariable=self.language_var,
            values=[self.loc._("option_language_english")],
            width=12,
            state='readonly'
        )
        self.language_combo.grid(row=0, column=6, sticky='w', padx=(0, 10))
        # Language change will be implemented when more languages are added
        
        # Reset settings button
        self.reset_button = ttk.Button(
            parent,
            text=self.loc._("btn_reset_settings")
        )
        self.reset_button.grid(row=0, column=7, sticky='w', padx=(20, 0))
    
    def _create_tabbed_log_area(self, parent):
        """Create the tabbed area with feature tabs and log tabs.
        
        Args:
            parent: Parent widget
        """
        # Create notebook (tabbed container)
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, sticky='nsew', pady=5)
        
        # File Cleaner Tab
        file_cleaner_frame = ttk.Frame(self.notebook, padding=5)
        file_cleaner_idx = self.notebook.index('end')
        self.notebook.add(file_cleaner_frame, text=self.loc._("tab_file_cleaner"))
        self.feature_tab_indices.append(file_cleaner_idx)
        
        # Folder Cleaner Tab
        folder_cleaner_frame = ttk.Frame(self.notebook, padding=5)
        folder_cleaner_idx = self.notebook.index('end')
        self.notebook.add(folder_cleaner_frame, text=self.loc._("tab_folder_cleaner"))
        self.feature_tab_indices.append(folder_cleaner_idx)
        
        # Game Optimizer Tab
        game_optimizer_frame = ttk.Frame(self.notebook, padding=5)
        game_optimizer_idx = self.notebook.index('end')
        self.notebook.add(game_optimizer_frame, text=self.loc._("tab_game_optimizer"))
        self.feature_tab_indices.append(game_optimizer_idx)
        
        # Optimization Suggestions Tab
        optimization_suggestions_frame = ttk.Frame(self.notebook, padding=5)
        optimization_suggestions_idx = self.notebook.index('end')
        self.notebook.add(optimization_suggestions_frame, text=self.loc._("tab_optimization_suggestions"))
        self.feature_tab_indices.append(optimization_suggestions_idx)
        
        # Main Log Tab
        log_frame = ttk.Frame(self.notebook, padding=5)
        self.notebook.add(log_frame, text=self.loc._("tab_log"))
        
        # User log controls frame
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(side='top', fill='x', pady=(0, 5))
        
        # Copy button
        copy_log_btn = ttk.Button(
            log_controls,
            text=self.loc._("log_copy"),
            command=self._copy_user_log
        )
        copy_log_btn.pack(side='left', padx=(0, 5))
        
        # Save button
        save_log_btn = ttk.Button(
            log_controls,
            text=self.loc._("log_save"),
            command=self._save_user_log
        )
        save_log_btn.pack(side='left', padx=(0, 5))
        
        # Delete button (only visible when append mode is enabled)
        self.delete_log_btn = ttk.Button(
            log_controls,
            text=self.loc._("log_delete"),
            command=self._delete_user_log
        )
        # Show/hide based on append_log setting
        if self.settings.get('append_log', False):
            self.delete_log_btn.pack(side='left', padx=(0, 10))
        
        # Create text widget with scrollbar for main log
        text_scroll = ttk.Scrollbar(log_frame)
        text_scroll.pack(side='right', fill='y')
        
        font_family = self.settings.get('font_family', 'TkDefaultFont')
        font_size = self.settings.get('font_size', 9)
        self.log_text = tk.Text(log_frame, height=15, width=60, 
                                yscrollcommand=text_scroll.set, 
                                wrap='word', font=(font_family, font_size))
        self.log_text.pack(side='left', fill='both', expand=True)
        text_scroll.config(command=self.log_text.yview)
        
        # Attach main logger to text widget
        self.logger.attach_text_widget(self.log_text)
        
        # Developer Tab
        dev_frame = ttk.Frame(self.notebook, padding=5)
        self.dev_tab_index = self.notebook.index('end')
        self.notebook.add(dev_frame, text=self.loc._("tab_developer"))
        
        # Developer tab controls frame
        dev_controls = ttk.Frame(dev_frame)
        dev_controls.pack(side='top', fill='x', pady=(0, 5))
        
        # Copy button
        copy_btn = ttk.Button(
            dev_controls,
            text=self.loc._("log_copy"),
            command=self._copy_dev_log
        )
        copy_btn.pack(side='left', padx=(0, 5))
        
        # Save button
        save_btn = ttk.Button(
            dev_controls,
            text=self.loc._("log_save"),
            command=self._save_dev_log
        )
        save_btn.pack(side='left', padx=(0, 10))
        
        # Error badge label
        self.dev_badge_label = ttk.Label(dev_controls, text="")
        self.dev_badge_label.pack(side='right', padx=(10, 0))
        
        # Create text widget with scrollbar for developer log
        dev_scroll = ttk.Scrollbar(dev_frame)
        dev_scroll.pack(side='right', fill='y')
        
        self.dev_text = tk.Text(dev_frame, height=15, width=60,
                               yscrollcommand=dev_scroll.set,
                               wrap='word', font=(font_family, font_size))
        self.dev_text.pack(side='left', fill='both', expand=True)
        dev_scroll.config(command=self.dev_text.yview)
        
        # Configure color tags for developer log
        self._configure_dev_log_colors()
        
        # Attach developer logger to text widget
        self.logger.attach_dev_text_widget(self.dev_text)
        
        # Set error callback for badge updates
        self.logger.set_error_callback(self._update_error_badge)
    
    def _configure_dev_log_colors(self):
        """Configure color tags for developer log based on theme."""
        # Get current theme colors
        from modules.core.themes import get_theme_colors
        theme_name = self.settings.get('theme', 'light')
        colors = get_theme_colors(theme_name)
        
        # Configure debug tag (blue/cyan)
        if theme_name == 'dark':
            self.dev_text.tag_config("debug", foreground="#6eb4f7")  # Light blue
        else:
            self.dev_text.tag_config("debug", foreground="#0066cc")  # Dark blue
        
        # Configure error tag (red/orange)
        if theme_name == 'dark':
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
            messagebox.showinfo(
                self.loc._("log_copy"),
                self.loc._("log_copied")
            )
    
    def _save_user_log(self):
        """Save user log to file."""
        from tkinter import filedialog
        from datetime import datetime
        
        # Default filename with timestamp
        default_name = f"wow_cleanup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[(self.loc._("file_text_files"), "*.txt"), 
                      (self.loc._("file_all_files"), "*.*")],
            initialfile=default_name
        )
        
        if file_path:
            try:
                user_log = self.log_text.get("1.0", "end-1c")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(user_log)
                
                import tkinter.messagebox as messagebox
                messagebox.showinfo(
                    self.loc._("log_save"),
                    self.loc._("log_saved").format(file_path)
                )
            except Exception as e:
                import tkinter.messagebox as messagebox
                messagebox.showerror(
                    self.loc._("error_prefix"),
                    str(e)
                )
    
    def _delete_user_log(self):
        """Delete the persistent user log file."""
        from modules.core.settings import get_user_log_file
        import tkinter.messagebox as messagebox
        from pathlib import Path
        
        log_file = get_user_log_file()
        
        if not log_file.exists():
            return
        
        try:
            # Respect the delete mode setting
            delete_mode = self.settings.get('delete_mode', 'trash')
            
            if delete_mode == 'trash':
                # Move to trash/recycle bin
                from send2trash import send2trash
                send2trash(str(log_file))
            else:
                # Permanent deletion
                log_file.unlink()
            
            messagebox.showinfo(
                self.loc._("log_delete"),
                self.loc._("status_log_deleted")
            )
        except Exception as e:
            messagebox.showerror(
                self.loc._("error_prefix"),
                self.loc._("log_delete_error").format(str(e))
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
                self.loc._("log_copy"),
                self.loc._("status_log_copied")
            )
    
    def _save_dev_log(self):
        """Save developer log to file."""
        from tkinter import filedialog
        from datetime import datetime
        
        # Default filename with timestamp
        default_name = f"wow_cleanup_dev_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[(self.loc._("file_text_files"), "*.txt"), 
                      (self.loc._("file_all_files"), "*.*")],
            initialfile=default_name
        )
        
        if file_path:
            try:
                dev_log = self.logger.get_dev_log()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(dev_log)
                
                import tkinter.messagebox as messagebox
                messagebox.showinfo(
                    self.loc._("log_save"),
                    self.loc._("log_saved").format(file_path)
                )
            except Exception as e:
                import tkinter.messagebox as messagebox
                messagebox.showerror(
                    self.loc._("error_prefix"),
                    str(e)
                )
    
    def _update_error_badge(self, count):
        """Update error badge on developer tab.
        
        Args:
            count: Number of errors
        """
        if count > 0:
            self.dev_badge_label.config(text=f"🔴 {count}")
            # Update tab text to include badge
            self.notebook.tab(self.dev_tab_index, 
                            text=f"{self.loc._('tab_developer')} 🔴 {count}")
        else:
            self.dev_badge_label.config(text="")
            self.notebook.tab(self.dev_tab_index, 
                            text=self.loc._('tab_developer'))
    
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
            if not hasattr(self, '_tab_tooltip_bindings') or not self._tab_tooltip_bindings:
                return
            
            # Identify which tab is under the cursor
            try:
                elem = self.notebook.identify(event.x, event.y)
                if elem and hasattr(self.notebook, 'index'):
                    # elem format: "tab@x,y" or similar - try to extract tab index
                    tab_idx = self.notebook.index(f"@{event.x},{event.y}")
                    
                    # Only show tooltip if tab is in bindings (disabled tabs only)
                    if tab_idx in self._tab_tooltip_bindings:
                        # Don't recreate if already showing for this tab
                        if self._current_tooltip_tab == tab_idx and self._tooltip_window:
                            return
                        
                        tooltip_text = self._tab_tooltip_bindings[tab_idx]
                        
                        # Destroy existing tooltip
                        if self._tooltip_window:
                            self._tooltip_window.destroy()
                        
                        # Get current theme colors
                        from modules.core.themes import THEMES
                        current_theme = self.settings.get('theme', 'dark')
                        theme_colors = THEMES.get(current_theme, THEMES['dark'])
                        
                        # Create tooltip window
                        self._tooltip_window = tk.Toplevel(self.notebook)
                        self._tooltip_window.wm_overrideredirect(True)
                        self._tooltip_window.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
                        
                        # Create label with word wrapping (max width ~300px)
                        label = tk.Label(
                            self._tooltip_window,
                            text=tooltip_text,
                            background=theme_colors.get('tooltip_bg', '#ffffe0'),
                            foreground=theme_colors.get('tooltip_fg', '#000000'),
                            relief="solid",
                            borderwidth=1,
                            font=("TkDefaultFont", 9),
                            padx=8,
                            pady=5,
                            wraplength=300,
                            justify='left'
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
        self.notebook.bind('<Motion>', show_tooltip)
        self.notebook.bind('<Leave>', hide_tooltip)
    
    def set_feature_tabs_enabled(self, enabled):
        """Enable or disable feature tabs based on WoW path validity.
        
        Args:
            enabled: True to enable tabs, False to disable
        """
        state = 'normal' if enabled else 'disabled'
        
        # Initialize tooltip bindings dict if needed
        if not hasattr(self, '_tab_tooltip_bindings'):
            self._tab_tooltip_bindings = {}
        
        # Update tab states and tooltip bindings
        for tab_idx in self.feature_tab_indices:
            self.notebook.tab(tab_idx, state=state)
            
            if enabled:
                # Remove tooltip binding when tab is enabled
                if tab_idx in self._tab_tooltip_bindings:
                    del self._tab_tooltip_bindings[tab_idx]
            else:
                # Add tooltip binding when tab is disabled
                self._tab_tooltip_bindings[tab_idx] = self.loc._("tab_disabled_tooltip")
        
        # Clear any visible tooltip when state changes
        if hasattr(self, '_tooltip_window') and self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None
            self._current_tooltip_tab = None
        
        # Set up hover event handling for tooltips (only once)
        if not hasattr(self, '_tooltip_bound'):
            self._setup_tab_tooltip_handler()
            self._tooltip_bound = True
