"""WoW path browser and detection utilities."""
import os
import sys
from tkinter import filedialog
from modules.ui.dialogs import wow_close_warning, show_multiple_installations_dialog


class WoWPathHandler:
    """Handler for WoW installation path selection and detection."""
    
    def __init__(self, root, settings, logger, loc, path_manager):
        """Initialize the WoW path handler.
        
        Args:
            root: Tkinter root window
            settings: Settings dictionary
            logger: Logger instance
            loc: Localization instance
            path_manager: PathManager instance
        """
        self.root = root
        self.settings = settings
        self.logger = logger
        self.loc = loc
        self.path_manager = path_manager
    
    def browse_for_path(self):
        """Open directory browser for WoW installation path.
        
        Returns:
            str or None: Selected path, or None if cancelled
        """
        # Show warning dialog if not disabled
        if not self.settings.get('disable_wow_close_warning', False):
            theme = self.settings.get('theme', 'light')
            result = wow_close_warning.show_wow_close_warning(
                self.root, self.loc, theme, self.settings
            )
            if not result:
                return None  # User cancelled
        
        # Open directory browser
        initial_dir = self.settings.get('wow_path', '')
        selected_path = filedialog.askdirectory(
            parent=self.root,
            title=self.loc._("select_wow_folder"),
            initialdir=initial_dir
        )
        
        if selected_path:
            # Validate the selected path
            if self.path_manager.validate_wow_path(selected_path):
                self.logger.log(self.loc._('wow_detected').format(selected_path))
                return selected_path
            else:
                self.logger.log(self.loc._("invalid_wow_path"))
                return None
        
        return None
    
    def detect_wow_on_first_run(self):
        """Detect WoW installation automatically on first run.
        
        Returns:
            str or None: Detected path, None if not found, or exits app if multiple found
        """
        current_path = self.settings.get('wow_path', '')
        if current_path:
            return None  # Already configured
        
        self.logger.log(self.loc._("status_detecting_wow"))
        
        # Check for multiple installations first
        all_installations = self.path_manager.detect_all_wow_installations()
        
        if len(all_installations) > 1:
            # Multiple installations found - show error dialog and exit
            self.logger.log(self.loc._("multiple_wow_detected").format(len(all_installations)))
            theme = self.settings.get('theme', 'light')
            show_multiple_installations_dialog(
                self.root, self.loc, theme, self.settings, all_installations
            )
            # Exit application after dialog is closed
            sys.exit(0)
        elif len(all_installations) == 1:
            # Single installation found
            detected_path = all_installations[0]
            self.logger.log(self.loc._('wow_detected').format(detected_path))
            return detected_path
        else:
            # No installation found
            self.logger.log(self.loc._("wow_not_detected"))
            return None
