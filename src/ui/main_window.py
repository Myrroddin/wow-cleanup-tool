
"""Main window UI creation for WoW Cleanup Tool."""
import tkinter as tk
from tkinter import ttk


class MainWindowBuilder:
    """Builder class for constructing the main application window UI."""

    def add_theme_toggle(self, parent, command):
        """Stub for add_theme_toggle. To be implemented."""
        pass

    def add_font_controls(self, *args, **kwargs):
        """Stub for add_font_controls. To be implemented."""
        pass

    def add_browse_button(self, parent, command):
        """Stub for add_browse_button. To be implemented."""
        pass

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
        self.notebook = None
        self.dev_tab_index = None
        self.dev_badge_label = None
        self.wow_path_var = None
        self.path_entry = None
        
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
        # Toolbar removed in custom tab system refactor
        self._create_tabbed_log_area(main_frame)
        path_frame = None
        
        # Log initial message
        self.logger.log(self.loc._("status_app_started"))
        # Return references to important widgets
        return {
            'path_frame': path_frame,
            'wow_path_var': self.wow_path_var,
            'path_entry': self.path_entry,
            'font_family_var': self.font_family_var,
            'append_log_var': self.append_log_var,
            'language_var': self.language_var,
            'delete_mode_var': self.delete_mode_var,
            'verbose_var': self.verbose_var,
            'reset_button': None,  # Stub for legacy reset_button
            # Legacy widgets removed from return dict
        }
    
    def _create_title(self, parent):
        """Create the title label.
        
        Args:
            parent: Parent widget
        """
        title = ttk.Label(parent, text=self.loc._("title_main_window"), style='Title.TLabel')
        def _create_tabbed_log_area(self, parent):
            import sys
            # Debug print removed
            from ui.custom_tabbar import CustomTabBar
            # Define tab ids and labels
            tabs = [
                ("file_cleaner", self.loc._("tab_file_cleaner")),
                ("folder_cleaner", self.loc._("tab_folder_cleaner")),
                ("game_optimizer", self.loc._("tab_game_optimizer")),
                ("optimization_suggestions", self.loc._("tab_optimization_suggestions")),
                ("log", self.loc._("tab_log")),
            ]
            # Tab bar
            self.tabbar = CustomTabBar(parent, tabs, self._on_tab_selected)
            self.tabbar.grid(row=2, column=0, sticky='ew', pady=(5, 0))
            # Debug print removed
            # Content frames for each tab
            self.tab_frames = {}
            for tab_id, _ in tabs:
                frame = ttk.Frame(parent, padding=5)
                frame.grid(row=3, column=0, sticky='nsew')
                self.tab_frames[tab_id] = frame
                # Debug print removed
            parent.rowconfigure(3, weight=1)
            # Build content for File Cleaner tab (template)
            self._build_file_cleaner_tab(self.tab_frames["file_cleaner"])
            # Build content for Folder Cleaner tab (template)
            self._build_folder_cleaner_tab(self.tab_frames["folder_cleaner"])
            # TODO: Build other tabs as needed
            # Show the first tab by default
            self._show_tab("file_cleaner")
        def _on_tab_selected(self, tab_id):
            import sys
            # Debug print removed
            self._show_tab(tab_id)
        def _show_tab(self, tab_id):
            for tid, frame in self.tab_frames.items():
                if tid == tab_id:
                    frame.tkraise()
                    frame.lift()
                    frame.grid()
                    # Debug print removed
                else:
                    frame.lower()
                    frame.grid_remove()
                    # Debug print removed
        def _build_file_cleaner_tab(self, parent):
            import sys
            # Debug print removed
            file_cleaner_desc_label = ttk.Label(
                parent,
                text=self.loc._("desc_file_cleaner"),
                justify='left'
            )
            file_cleaner_desc_label.pack(side='top', fill='x', pady=(0, 10))
            button_frame = ttk.Frame(parent)
            button_frame.pack(side='top', fill='x', pady=(0, 10))
            scan_btn = ttk.Button(
                button_frame,
                text=self.loc._("btn_scan_files"),
                command=self._on_scan_files
            )
            scan_btn.pack(side='left', padx=(0, 10))
            select_all_btn = ttk.Button(
                button_frame,
                text=self.loc._("btn_select_all_toggle"),
                command=lambda: self._on_select_all_toggle(self.get_selectable_items('file_cleaner'))
            )
            select_all_btn.pack(side='left', padx=(0, 10))
            remove_btn = ttk.Button(
                button_frame,
                text=self.loc._("btn_remove_selected"),
                command=lambda: self._on_remove_selected(self.get_selected_items('file_cleaner'))
            )
            remove_btn.pack(side='left')
            # Sub-tabs (template, not functional yet)
            sub_label = ttk.Label(parent, text='Sub-tabs would go here')
            sub_label.pack(side='top', fill='x', pady=(10, 0))
        def _build_folder_cleaner_tab(self, parent):
            import sys
            # Debug print removed
            label = ttk.Label(parent, text='Folder Cleaner Content')
            label.pack(side='top', fill='x', pady=(0, 10))
    
    def _create_tabbed_log_area(self, parent):
        import sys
        # Debug print removed
        """Create the tabbed area with feature tabs and log tabs.
        
        Args:
            parent: Parent widget
        """
        # Create notebook (tabbed container)
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, sticky='nsew', pady=5)
        # Debug print removed
        def on_tab_changed(event):
            try:
                tab_id = event.widget.select()
                if not tab_id:
                    # Debug print removed
                    return
                idx = event.widget.index(tab_id)
                # Debug print removed
            except Exception as e:
                pass
        self.notebook.bind('<<NotebookTabChanged>>', on_tab_changed)

        # File Cleaner Tab
        from ui.widgets.sapling_canvas import SaplingCanvas, TreeNode
        file_cleaner_frame = ttk.Frame(self.notebook, padding=5)
        # Debug print removed
        file_cleaner_idx = self.notebook.index('end')
        # Debug print removed
        self.notebook.add(file_cleaner_frame, text=self.loc._("tab_file_cleaner"))
        # Debug print removed
        self.feature_tab_indices.append(file_cleaner_idx)
        # Debug print removed
        # Add description label to File Cleaner tab
        file_cleaner_desc_label = ttk.Label(
            file_cleaner_frame,
            text=self.loc._("desc_file_cleaner"),
            justify='left'
        )
        # Debug print removed
        file_cleaner_desc_label.pack(side='top', fill='x', pady=(0, 10))
        # Debug print removed

        # Add Scan Files and Remove Files buttons
        button_frame = ttk.Frame(file_cleaner_frame)
        # Debug print removed
        button_frame.pack(side='top', fill='x', pady=(0, 10))
        # Debug print removed

        scan_btn = ttk.Button(
            button_frame,
            text=self.loc._("btn_scan_files"),
            command=self._on_scan_files
        )
        # Debug print removed
        scan_btn.pack(side='left', padx=(0, 10))
        # Debug print removed


        select_all_btn = ttk.Button(
            button_frame,
            text=self.loc._("btn_select_all_toggle"),
            command=lambda: self._on_select_all_toggle(self.get_selectable_items('file_cleaner'))
        )
        # Debug print removed
        select_all_btn.pack(side='left', padx=(0, 10))
        # Debug print removed

        remove_btn = ttk.Button(
            button_frame,
            text=self.loc._("btn_remove_selected"),
            command=lambda: self._on_remove_selected(self.get_selected_items('file_cleaner'))
        )
        # Debug print removed
        remove_btn.pack(side='left')
        # Debug print removed

        # Add sub-tabs for file cleaning features
        sub_notebook = ttk.Notebook(file_cleaner_frame)
        # Debug print removed
        sub_notebook.pack(side='top', fill='both', expand=True, pady=(0, 10))
        # Debug print removed

        backup_old_tab = ttk.Frame(sub_notebook)
        orphan_tab = ttk.Frame(sub_notebook)
        # Debug print removed
        sub_notebook.add(backup_old_tab, text=self.loc._("tab_backup_old_cleaner"))
        sub_notebook.add(orphan_tab, text=self.loc._("tab_orphan_cleaner"))
        # Debug print removed

        def update_wraplength(event=None):
            width = file_cleaner_frame.winfo_width() - 32
            if width > 100:
                file_cleaner_desc_label.config(wraplength=width)
        file_cleaner_frame.bind('<Configure>', update_wraplength)
        update_wraplength()
        # Debug print removed
    def _on_select_all_toggle(self, items):
        # TODO: Implement select all/unselect all logic for files/folders
        print(f"Select All/Unselect All button clicked. Items: {items}")

    def get_selectable_items(self, context):
        # Placeholder: Return all selectable items for the given context (e.g., 'file_cleaner', 'folder_cleaner')
        # Replace with actual logic
        return []

        # Placeholder for file/folder tree removed. Area will be populated later.

        # Folder Cleaner Tab
        folder_cleaner_frame = ttk.Frame(self.notebook, padding=5)
        # Debug print removed
        folder_cleaner_idx = self.notebook.index('end')
        # Debug print removed
        self.notebook.add(folder_cleaner_frame, text=self.loc._("tab_folder_cleaner"))
        # Debug print removed
        # Add a label to make sure content is visible
        folder_label = ttk.Label(folder_cleaner_frame, text='[DEBUG] Folder Cleaner Content')
        folder_label.pack(side='top', fill='x', pady=(0, 10))
        # Debug print removed
        self.feature_tab_indices.append(folder_cleaner_idx)
        # Debug print removed

        # Game Optimizer Tab
        game_optimizer_frame = ttk.Frame(self.notebook, padding=5)
        # Debug print removed
        game_optimizer_idx = self.notebook.index('end')
        # Debug print removed
        self.notebook.add(game_optimizer_frame, text=self.loc._("tab_game_optimizer"))
        # Debug print removed
        # Add a label to make sure content is visible
        optimizer_label = ttk.Label(game_optimizer_frame, text='[DEBUG] Game Optimizer Content')
        optimizer_label.pack(side='top', fill='x', pady=(0, 10))
        # Debug print removed
        self.feature_tab_indices.append(game_optimizer_idx)
        # Debug print removed

        # Optimization Suggestions Tab
        optimization_suggestions_frame = ttk.Frame(self.notebook, padding=5)
        # Debug print removed
        optimization_suggestions_idx = self.notebook.index('end')
        # Debug print removed
        self.notebook.add(optimization_suggestions_frame, text=self.loc._("tab_optimization_suggestions"))
        # Debug print removed
        # Add a label to make sure content is visible
        suggestions_label = ttk.Label(optimization_suggestions_frame, text='[DEBUG] Optimization Suggestions Content')
        suggestions_label.pack(side='top', fill='x', pady=(0, 10))
        # Debug print removed
        self.feature_tab_indices.append(optimization_suggestions_idx)
        # Debug print removed

        # Main Log Tab
        log_frame = ttk.Frame(self.notebook, padding=5)
        # Debug print removed
        # Debug print removed
        self.notebook.add(log_frame, text=self.loc._("tab_log"))
        # Debug print removed
        # Add a label to make sure content is visible
        log_label = ttk.Label(log_frame, text='[DEBUG] Log Content')
        log_label.pack(side='top', fill='x', pady=(0, 10))
        # Debug print removed
        print('[DEBUG] Log tab added', file=sys.stderr)

        # Improved: Force each tab to be selected and update, then return to the first tab
        try:
            tab_count = self.notebook.index('end')
            print(f'[DEBUG] Forcing realization of {tab_count} tabs', file=sys.stderr)
            for i in range(tab_count):
                self.notebook.select(i)
                self.root.update()
                print(f'[DEBUG] Selected tab {i} ({self.notebook.tab(i, "text")}) for realization', file=sys.stderr)
                frame = self.notebook.nametowidget(self.notebook.tabs()[i])
                print(f'[DEBUG] Tab {i} children after select: {frame.winfo_children()}', file=sys.stderr)
            self.notebook.select(0)
            self.root.update()
            print('[DEBUG] Returned to first tab after realization', file=sys.stderr)
        except Exception as e:
            print(f'[DEBUG] Exception during tab realization: {e}', file=sys.stderr)

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
        save_btn.pack(side='left', padx=(0, 5))
        
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
        from core.themes import get_theme_colors
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
        from core.settings import get_user_log_file
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
                        from core.themes import THEMES
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
