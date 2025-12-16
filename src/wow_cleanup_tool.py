"""WoW Cleanup Tool - Main Application"""

import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.instance_utils import acquire_single_instance, release_single_instance

instance_lock = acquire_single_instance()


# Check and install dependencies silently before importing modules that need them
from core.bootstrap import ensure_dependencies

ensure_dependencies()

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
        from ui.geometry import reset_window_geometry

        reset_window_geometry(self)

    def __init__(self, root):
        import platform
        import time

        self.root = root
        t0 = time.perf_counter()

        # Minimal startup: load settings, localization, logger
        self.settings = load_settings()
        lang = self.settings.get("language", "en_us")
        self.loc = Localization(lang)
        self.logger = Logger(
            verbose=self.settings.get("verbose_logging", True),
            append_mode=self.settings.get("append_log", False),
        )
        self.root.title(self.loc._("title_main_window"))

        # Hide main window until license is accepted
        self.root.withdraw()
        import time

        t1 = time.perf_counter()
        # Show license dialog
        theme_name = self.settings.get("theme", "light")
        license_accepted = show_license_dialog(
            self.root, self.loc, theme_name, self.settings
        )
        if not license_accepted:
            self.root.destroy()
            sys.exit(0)

        # User accepted - show main window and continue with normal initialization
        self.root.deiconify()
        # Load previous logs if append mode is enabled
        if self.settings.get("append_log", False):
            self.logger.load_previous_log()
        # Initialize PathManager and PathHandler
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
        # Initialize application controller
        self.controller = ApplicationController(
            self.root, self.settings, self.ui_widgets, self.logger, builder
        )
        # Store builder reference for theme updates
        self.builder = builder
        # Save settings on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        from ui.geometry import setup_geometry

        setup_geometry(self)
        # Log: startup success for user, or error if exception occurs
        try:
            self.logger.log(self.loc._("startup_success"))
        except Exception as e:
            self.logger.error(self.loc._("startup_error_see_devlog"))

        # Detect WoW path on first run (after UI is ready)
        def detect_and_log():
            self._detect_wow_on_first_run()

        self.root.after(100, detect_and_log)

        # Show WoW close warning after detection (if not disabled)
        def show_warning_and_log():
            show_wow_close_warning(
                self.root, self.loc, self.settings.get("theme", "light"), self.settings
            )

        self.root.after(200, show_warning_and_log)

    def on_theme_toggle(self):
        """Handle theme toggle with dev log color refresh."""
        self.controller.toggle_theme()
        # Refresh developer log colors
        if hasattr(self, "builder") and hasattr(self.builder, "refresh_dev_log_colors"):
            self.builder.refresh_dev_log_colors()

    def browse_wow_path(self):
        """Delegate WoW path browsing to path handler/controller."""
        new_path = self.path_handler.browse_for_path()
        if new_path:
            self.controller.handle_new_wow_path(new_path)

    def _detect_wow_on_first_run(self):
        """Delegate WoW path detection to path handler/controller."""
        detected_path = self.path_handler.detect_wow_on_first_run()
        if detected_path:
            self.controller.handle_new_wow_path(detected_path)

    def on_close(self):
        """Handle window close event, abstracted for future profiles."""
        from core.settings import save_settings

        save_settings(self.settings)

        # Save user log to disk if append mode is enabled
        if self.settings.get("append_log", False):
            self.logger.save_log_to_disk()

        self.logger.log(self.loc._("status_settings_saved"))
        release_single_instance(instance_lock)
        self.root.destroy()


def main():
    try:
        root = tk.Tk()
        app = WoWCleanupTool(root)
        root.mainloop()
    except Exception as e:
        from core.error_handler import handle_top_level_exception

        handle_top_level_exception(e)


if __name__ == "__main__":
    main()
