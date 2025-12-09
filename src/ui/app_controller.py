"""Event handlers and UI controllers for the main application."""
import tkinter as tk
from tkinter import ttk
from core import themes


class ApplicationController:
    """Controller for handling main application events and UI updates."""
    
    def __init__(self, root, settings, ui_widgets, logger, builder=None):
        """Initialize the application controller.
        
        Args:
            root: Tkinter root window
            settings: Settings dictionary
            ui_widgets: Dictionary of UI widget references
            logger: Logger instance
            builder: MainWindowBuilder instance (optional, for dynamic UI updates)
        """
        self.root = root
        self.settings = settings
        self.ui_widgets = ui_widgets
        self.logger = logger
        self.builder = builder
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        current_theme = self.settings.get('theme', 'light')
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.settings['theme'] = new_theme
        
        # Apply theme with current font settings
        font_family = self.settings.get('font_family', 'TkDefaultFont')
        font_size = self.settings.get('font_size', 9)
        themes.apply_theme(self.root, new_theme, font_family, font_size)
    
    def on_font_size_changed(self, event=None):
        """Handle font size changes.
        
        Args:
            event: Tkinter event (optional)
        """
        try:
            font_size_var = self.ui_widgets.get('font_size_var')
            if not font_size_var:
                return
            
            new_size = int(font_size_var.get())
            self.settings['font_size'] = new_size
            
            # Apply font globally through theme system
            font_family = self.settings.get('font_family', 'TkDefaultFont')
            current_theme = self.settings.get('theme', 'light')
            themes.apply_theme(self.root, current_theme, font_family, new_size)
            
            # Force window to resize to fit new font
            self.root.update_idletasks()
            self.resize_to_fit_content()
        except ValueError:
            pass  # Invalid font size, ignore
    
    def on_font_family_changed(self, event=None):
        """Handle font family changes.
        
        Args:
            event: Tkinter event (optional)
        """
        from ui import font_utils
        
        font_family_var = self.ui_widgets.get('font_family_var')
        if not font_family_var:
            return
        
        selected = font_family_var.get()
        font_combo = self.ui_widgets.get('font_combo')
        
        # Get the actual font value from the combobox state
        # System default is stored as 'TkDefaultFont' internally
        if font_combo and hasattr(font_combo, 'current'):
            idx = font_combo.current()
            if idx == 0:  # First item is always system default
                actual_font = 'TkDefaultFont'
            else:
                actual_font = selected
        else:
            # Fallback: if selected matches display of system default, use TkDefaultFont
            actual_font = 'TkDefaultFont' if '(' in selected and ')' in selected else selected
        
        self.settings['font_family'] = actual_font
        
        # Apply font globally through theme system
        current_theme = self.settings.get('theme', 'light')
        font_size = self.settings.get('font_size', 9)
        themes.apply_theme(self.root, current_theme, actual_font, font_size)
        
        # Force window to resize to fit new font
        self.root.update_idletasks()
        self.resize_to_fit_content()
    
    def on_delete_mode_changed(self, *args):
        """Handle delete mode changes.
        
        Args:
            *args: Variable trace arguments
        """
        delete_mode_var = self.ui_widgets.get('delete_mode_var')
        if not delete_mode_var:
            return
        
        new_mode = delete_mode_var.get()
        self.settings['delete_mode'] = new_mode
    
    def on_verbose_changed(self, *args):
        """Handle verbose logging changes.
        
        Args:
            *args: Variable trace arguments
        """
        verbose_var = self.ui_widgets.get('verbose_var')
        if not verbose_var:
            return
        
        new_value = verbose_var.get()
        self.settings['verbose_logging'] = new_value
        
        # Update logger verbose mode
        self.logger.set_verbose(new_value)
    
    def on_append_log_changed(self, *args):
        """Handle append log changes.
        
        Args:
            *args: Variable trace arguments
        """
        append_log_var = self.ui_widgets.get('append_log_var')
        if not append_log_var:
            return
        
        new_value = append_log_var.get()
        self.settings['append_log'] = new_value
        
        # Update logger append mode
        self.logger.set_append_mode(new_value)
        
        # Show/hide delete log button based on append mode
        if self.builder and hasattr(self.builder, 'delete_log_btn'):
            if new_value:
                self.builder.delete_log_btn.pack(side='left', padx=(0, 10))
            else:
                self.builder.delete_log_btn.pack_forget()
    
    def update_wow_path(self, new_path):
        """Update the WoW path in UI and settings.
        
        Args:
            new_path: New WoW installation path
        """
        wow_path_var = self.ui_widgets.get('wow_path_var')
        path_entry = self.ui_widgets.get('path_entry')
        
        if wow_path_var:
            wow_path_var.set(new_path)
        
        # Update entry width to fit new path
        if path_entry:
            entry_width = max(len(new_path) if new_path else 20, 20)
            path_entry.config(width=entry_width)
        
        self.settings['wow_path'] = new_path
        
        # Enable/disable feature tabs based on whether we have a valid WoW path
        if self.builder and hasattr(self.builder, 'set_feature_tabs_enabled'):
            self.builder.set_feature_tabs_enabled(bool(new_path))
    
    def update_minimum_size(self):
        """Calculate and update the minimum window size based on content."""
        self.root.update_idletasks()
        
        path_entry = self.ui_widgets.get('path_entry')
        font_combo = self.ui_widgets.get('font_combo')
        
        if not path_entry or not font_combo:
            # Use default minimums if widgets not ready
            min_width = 480
            min_height = 320
        else:
            path_entry_width = path_entry.winfo_reqwidth()
            font_combo_width = font_combo.winfo_reqwidth()
            required_width = max(path_entry_width, font_combo_width) + 200
            
            min_width = max(required_width, 480)
            min_height = 320
        
        self.root.minsize(min_width, min_height)
        
        # Return the values so they can be used by the app
        return min_width, min_height
    
    def resize_to_fit_content(self):
        """Resize window to fit current content."""
        # Get screen dimensions
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        
        # Update all pending geometry calculations
        self.root.update_idletasks()
        
        # Get required size from widgets
        requested_w = self.root.winfo_reqwidth()
        requested_h = self.root.winfo_reqheight()
        
        # Get current position
        current_geo = self.root.geometry()
        if '+' in current_geo:
            parts = current_geo.split('+')
            try:
                x = int(parts[1])
                y = int(parts[2])
            except (IndexError, ValueError):
                x = self.root.winfo_x()
                y = self.root.winfo_y()
        else:
            x = self.root.winfo_x()
            y = self.root.winfo_y()
        
        # Calculate new size with constraints
        new_w = max(requested_w + 20, 480)  # Add padding for safety
        new_h = max(requested_h + 20, 320)
        
        # Don't exceed 90% of screen
        new_w = min(new_w, int(sw * 0.9))
        new_h = min(new_h, int(sh * 0.9))
        
        # Apply new size while keeping position
        self.root.geometry(f"{new_w}x{new_h}+{x}+{y}")
        self.root.minsize(new_w, new_h)
    
    def reset_settings(self):
        """Reset all settings to defaults (preserves cached data like wow_path)."""
        from tkinter import messagebox
        from localization.en_us import TRANSLATIONS
        
        # Get localization (fallback to English if localization not available)
        try:
            confirm_msg = self.builder.loc._("msg_reset_settings_confirm")
            confirm_title = self.builder.loc._("title_reset_settings")
            reset_msg = self.builder.loc._("status_settings_reset")
        except:
            confirm_msg = TRANSLATIONS["msg_reset_settings_confirm"]
            confirm_title = TRANSLATIONS["title_reset_settings"]
            reset_msg = TRANSLATIONS["status_settings_reset"]
        
        # Create custom themed dialog for better presentation
        dialog = tk.Toplevel(self.root)
        dialog.title(confirm_title)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Get current theme colors
        from core.themes import THEMES
        current_theme = self.settings.get('theme', 'dark')
        theme_colors = THEMES.get(current_theme, THEMES['dark'])
        
        # Configure dialog colors
        dialog.configure(bg=theme_colors['bg'])
        
        # Main frame with padding
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Message label with left alignment for bullet points
        message_label = ttk.Label(
            main_frame,
            text=confirm_msg,
            justify='left',
            wraplength=400
        )
        message_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()
        
        # Track user choice
        user_choice = {'confirmed': False}
        
        def on_yes():
            user_choice['confirmed'] = True
            dialog.destroy()
        
        def on_no():
            dialog.destroy()
        
        # Yes button
        yes_btn = ttk.Button(
            button_frame,
            text=self.builder.loc._("btn_yes") if hasattr(self.builder, 'loc') else "Yes",
            command=on_yes,
            width=10
        )
        yes_btn.pack(side='left', padx=(0, 10))
        
        # No button
        no_btn = ttk.Button(
            button_frame,
            text=self.builder.loc._("btn_no") if hasattr(self.builder, 'loc') else "No",
            command=on_no,
            width=10
        )
        no_btn.pack(side='left')
        
        # Center dialog on parent
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Wait for dialog to close
        dialog.wait_window()
        
        # Check if user confirmed
        if not user_choice['confirmed']:
            return
        
        # Store cached data before reset
        wow_path = self.settings.get('wow_path', '')
        geometry = self.settings.get('geometry', '')
        
        # Clear ALL settings
        self.settings.clear()
        
        # Reset to defaults (only settings, not cached data)
        self.settings['theme'] = 'light'
        self.settings['font_family'] = 'TkDefaultFont'
        self.settings['font_size'] = 9
        self.settings['delete_mode'] = 'trash'
        self.settings['verbose_logging'] = True
        self.settings['append_log'] = False
        self.settings['language'] = 'en'
        
        # Reset dialog preferences (re-enable all "don't show again" dialogs)
        self.settings['license_accepted'] = False
        self.settings['disable_license_dialog'] = False
        self.settings['disable_wow_close_warning'] = False
        
        # Restore cached data
        if wow_path:
            self.settings['wow_path'] = wow_path
        if geometry:
            self.settings['geometry'] = geometry
        
        # Save settings immediately
        from core.settings import save_settings
        save_settings(self.settings)
        
        # Update UI widgets to reflect reset values
        if self.ui_widgets.get('font_family_var'):
            self.ui_widgets['font_family_var'].set(self.builder.loc._("system_default_font") if hasattr(self.builder, 'loc') else "System Default")
        
        if self.ui_widgets.get('font_size_var'):
            self.ui_widgets['font_size_var'].set('9')
        
        if self.ui_widgets.get('delete_mode_var'):
            self.ui_widgets['delete_mode_var'].set('trash')
        
        if self.ui_widgets.get('verbose_var'):
            self.ui_widgets['verbose_var'].set(True)
        
        if self.ui_widgets.get('append_log_var'):
            self.ui_widgets['append_log_var'].set(False)
        
        if self.ui_widgets.get('language_var'):
            self.ui_widgets['language_var'].set(self.builder.loc._("option_language_english") if hasattr(self.builder, 'loc') else "English")
        
        # Apply default theme (light)
        themes.apply_theme(self.root, 'light', 'TkDefaultFont', 9)
        
        # Refresh developer log colors to match new theme
        if self.builder and hasattr(self.builder, 'refresh_dev_log_colors'):
            self.builder.refresh_dev_log_colors()
        
        # Update logger settings
        self.logger.set_verbose(True)
        self.logger.set_append_mode(False)
        
        # Hide delete log button (append mode disabled)
        if self.builder and hasattr(self.builder, 'delete_log_btn'):
            self.builder.delete_log_btn.pack_forget()
        
        # Log the reset
        self.logger.log(reset_msg)
        
        # Resize window
        self.root.update_idletasks()
        self.resize_to_fit_content()
