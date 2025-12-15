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
from wow.path_manager import PathManager
from wow.path_handler import WoWPathHandler
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


class WoWCleanupTool:
    MIN_W = 480
    MIN_H = 320

    def reset_window_geometry(self):
        """Reset window geometry to default (content-based) size on next launch."""
        # Remove geometry-related settings
        for key in [
            "window_width",
            "window_height",
            "window_x",
            "window_y",
            "is_maximized",
        ]:
            if key in self.settings:
                del self.settings[key]
        save_settings(self.settings)
        # Optionally, resize immediately (for current session)
        from ui.geometry import center_first_launch

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        center_first_launch(self, sw, sh)

    def __init__(self, root):
        self.root = root
        self.settings = load_settings()

        # Initialize localization
        self.loc = Localization(self.settings.get("language", "en_us"))

        # Set window title (before checking license)
        self.root.title(self.loc._("title_main_window"))

        # Hide main window until license is accepted
        self.root.withdraw()

        # Get theme for license dialog
        theme_name = self.settings.get("theme", "light")

        # Show license dialog
        license_accepted = show_license_dialog(
            self.root, self.loc, theme_name, self.settings
        )

        if not license_accepted:
            # User declined - exit application
            self.root.destroy()
            sys.exit(0)

        # User accepted - show main window and continue with normal initialization
        self.root.deiconify()

        # Initialize logger with verbose and append_log settings
        self.logger = Logger(
            verbose=self.settings.get("verbose_logging", True),
            append_mode=self.settings.get("append_log", False),
        )

        # Load previous logs if append mode is enabled
        if self.settings.get("append_log", False):
            self.logger.load_previous_log()

        # Initialize PathManager with localization and PathHandler
        self.path_manager = PathManager(self.loc)
        self.path_handler = WoWPathHandler(
            self.root, self.settings, self.logger, self.loc, self.path_manager
        )

        # Get font and theme settings (use defaults if missing)
        font_family = self.settings.get("font_family", "TkDefaultFont")
        font_size = self.settings.get("font_size", 9)
        theme_name = self.settings.get("theme", "light")

        # Apply theme and font to root before any widget creation
        apply_theme(self.root, theme_name, font_family, font_size)

        # Pass browse_wow_path as a callback for the builder's browse button
        self.settings["browse_callback"] = self.browse_wow_path
        builder = MainWindowBuilder(
            self.root, self.loc, self.settings, self.logger, font_utils
        )
        self.ui_widgets = builder.build(theme_toggle_callback=self.on_theme_toggle)

        # ...existing code...

        # Initialize application controller
        self.controller = ApplicationController(
            self.root, self.settings, self.ui_widgets, self.logger, builder
        )

        # Store builder reference for theme updates
        self.builder = builder

        # All wow path row widgets are now created only in build()
        # Save settings on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Center the main window on screen at launch (after all widgets are realized)
        from ui.geometry import setup_geometry

        setup_geometry(self)

        # Detect WoW path on first run (after UI is ready)
        self.root.after(100, self._detect_wow_on_first_run)

        # Show WoW close warning after detection (if not disabled)
        self.root.after(
            200,
            lambda: show_wow_close_warning(
                self.root, self.loc, self.settings.get("theme", "light"), self.settings
            ),
        )

    def on_theme_toggle(self):
        """Handle theme toggle with dev log color refresh."""
        self.controller.toggle_theme()
        # Refresh developer log colors
        if hasattr(self, "builder") and hasattr(self.builder, "refresh_dev_log_colors"):
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
        if self.settings.get("append_log", False):
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
        loc = Localization(settings.get("language", "en_us"))

        # Optionally log error here if needed
        import traceback

        traceback.print_exc()
        input(loc._("press_enter_to_exit"))


if __name__ == "__main__":
    main()
