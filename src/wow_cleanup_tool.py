"""WoW Cleanup Tool - Main Application"""
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

 # Single instance check - silently exit if another instance is running
from core.single_instance import SingleInstance

instance_lock = SingleInstance()
if not instance_lock.acquire():
    sys.exit(0)

 # Check and install dependencies silently before importing modules that need them
from core.dependencies import check_and_install_dependencies

if not check_and_install_dependencies():
    sys.exit(1)

from core.settings import load_settings, save_settings
from core.logger import Logger
from core.themes import apply_theme
from localization import Localization
from ui import (
    show_wow_close_warning, 
    show_license_dialog, 
    font_utils,
    MainWindowBuilder,
    ApplicationController,
    setup_geometry,
    on_configure,
)
from wow import PathManager, WoWPathHandler

class WoWCleanupTool:
    def __init__(self, root):
        self.root = root
        self.settings = load_settings()
        
        # Initialize localization
        self.loc = Localization(self.settings.get('language', 'en_us'))
        
        # Set window title (before checking license)
        self.root.title(self.loc._("title_main_window"))
        
        # Hide main window until license is accepted
        self.root.withdraw()
        
        # Get theme for license dialog
        theme_name = self.settings.get('theme', 'light')
        
        # Show license dialog
        license_accepted = show_license_dialog(self.root, self.loc, theme_name, self.settings)
        
        if not license_accepted:
            # User declined - exit application
            self.root.destroy()
            sys.exit(0)
        
        # User accepted - show main window and continue with normal initialization
        self.root.deiconify()
        
        # Initialize logger with verbose and append_log settings
        self.logger = Logger(
            verbose=self.settings.get('verbose_logging', True),
            append_mode=self.settings.get('append_log', False)
        )
        
        # Load previous logs if append mode is enabled
        if self.settings.get('append_log', False):
            self.logger.load_previous_log()
        
        # Initialize PathManager with localization and PathHandler
        self.path_manager = PathManager(self.loc)
        self.path_handler = WoWPathHandler(
            self.root, self.settings, self.logger, self.loc, self.path_manager
        )
        
        # Get font settings
        font_family = self.settings.get('font_family', 'TkDefaultFont')
        font_size = self.settings.get('font_size', 9)
        
        # Apply theme with font
        apply_theme(self.root, self.settings.get('theme', 'light'), font_family, font_size)
        
        # Create UI using MainWindowBuilder
        builder = MainWindowBuilder(self.root, self.loc, self.settings, self.logger, font_utils)
        self.ui_widgets = builder.build()
        
        # Initialize application controller
        self.controller = ApplicationController(
            self.root, self.settings, self.ui_widgets, self.logger, builder
        )
        
        # Store builder reference for theme updates
        self.builder = builder
        
        # Add toolbar controls with callbacks
        path_frame = self.ui_widgets['path_frame']
        builder.add_browse_button(path_frame, self.browse_wow_path)
        builder.add_theme_toggle(path_frame, self.on_theme_toggle)
        builder.add_font_controls(
            path_frame,
            self.controller.on_font_family_changed,
            self.controller.on_font_size_changed
        )
        
        # Update ui_widgets with font_combo reference (set in add_font_controls)
        self.ui_widgets['font_combo'] = builder.font_combo
        
        # Set up delete mode change handler
        self.ui_widgets['delete_mode_var'].trace_add('write', self.controller.on_delete_mode_changed)
        
        # Set up verbose logging change handler
        self.ui_widgets['verbose_var'].trace_add('write', self.controller.on_verbose_changed)
        
        # Set up append log change handler
        self.ui_widgets['append_log_var'].trace_add('write', self.controller.on_append_log_changed)
        
        # Set up reset button handler
        if self.ui_widgets.get('reset_button') is not None:
            self.ui_widgets['reset_button'].config(command=self.controller.reset_settings)
        
        # Set up scan files button handler
        if 'scan_files_btn' in self.ui_widgets:
            self.ui_widgets['scan_files_btn'].config(command=self.controller.scan_bak_old_files)
        
        # Set up select all/unselect all toggle handler
        if 'select_all_btn' in self.ui_widgets:
            self.ui_widgets['select_all_btn'].config(command=self.controller.toggle_select_all_bak_old)
        
        # Set up delete selected button handler
        if 'delete_selected_btn' in self.ui_widgets:
            self.ui_widgets['delete_selected_btn'].config(command=self.controller.delete_selected_files)
        
        # Calculate minimum dimensions based on content
        self.MIN_W, self.MIN_H = self.controller.update_minimum_size()
        
        # Set initial state of feature tabs based on WoW path
        current_wow_path = self.settings.get('wow_path', '')
        builder.set_feature_tabs_enabled(bool(current_wow_path))
        
        # Setup geometry (must be after UI creation for content-based sizing)
        setup_geometry(self)
        
        # Bind configure event for saving geometry
        self.root.bind('<Configure>', lambda e: on_configure(self))
        
        # Save settings on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Detect WoW path on first run (after UI is ready)
        self.root.after(100, self._detect_wow_on_first_run)
        
        # Show WoW close warning after detection (if not disabled)
        self.root.after(200, lambda: show_wow_close_warning(self.root, self.loc, self.settings.get('theme', 'light'), self.settings))
    
    def on_theme_toggle(self):
        """Handle theme toggle with dev log color refresh."""
        self.controller.toggle_theme()
        # Refresh developer log colors
        if hasattr(self, 'builder') and hasattr(self.builder, 'refresh_dev_log_colors'):
            self.builder.refresh_dev_log_colors()
    
    def browse_wow_path(self):
        """Handle WoW path browsing."""
        new_path = self.path_handler.browse_for_path()
        if new_path:
            self.controller.update_wow_path(new_path)
            self.controller.update_minimum_size()
    
    def _detect_wow_on_first_run(self):
        """Detect WoW installation on first run."""
        detected_path = self.path_handler.detect_wow_on_first_run()
        if detected_path:
            self.controller.update_wow_path(detected_path)
            self.controller.update_minimum_size()
    
    def on_close(self):
        """Handle window close event"""
        save_settings(self.settings)
        
        # Save user log to disk if append mode is enabled
        if self.settings.get('append_log', False):
            self.logger.save_log_to_disk()
        
        self.logger.log(self.loc._("status_settings_saved"))
        instance_lock.release()
        self.root.destroy()

def main():
    try:
        root = tk.Tk()
        app = WoWCleanupTool(root)
        root.mainloop()
    except Exception as e:
        # Use basic localization for error display
        from localization import Localization
        from core.settings import load_settings
        settings = load_settings()
        loc = Localization(settings.get('language', 'en_us'))
        
        print(f"{loc._('error_prefix')} {e}")
        import traceback
        traceback.print_exc()
        input(loc._('press_enter_to_exit'))

if __name__ == "__main__":
    main()
