"""WoW Cleanup Tool - Main Application"""

import sys
import tkinter as tk

from core.instance_utils import acquire_single_instance, release_single_instance
from core.bootstrap import ensure_dependencies
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
)


# Check and install dependencies silently before continuing
ensure_dependencies()


class WoWCleanupTool:
    MIN_W = 480
    MIN_H = 320

    def reset_window_geometry(self):
        from ui.geometry import reset_window_geometry

        reset_window_geometry(self)

    def __init__(self, root):
        self.root = root
        self.instance_lock = acquire_single_instance()

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
        font_size = self.settings.get("font_size", 12)
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
        # Wire font controls to controller handlers so changes apply immediately
        font_combo = self.ui_widgets.get("font_combo")
        if font_combo:
            font_combo.bind(
                "<<ComboboxSelected>>", self.controller.on_font_family_changed
            )
        font_size_combo = self.ui_widgets.get("font_size_combo")
        if font_size_combo:
            font_size_combo.bind(
                "<<ComboboxSelected>>", self.controller.on_font_size_changed
            )
        language_combo = self.ui_widgets.get("language_combo")
        if language_combo and hasattr(language_combo, "bind"):
            language_combo.bind(
                "<<ComboboxSelected>>", self.controller.on_language_changed
            )
        # Store builder reference for theme updates
        self.builder = builder
        # Save settings on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        from ui.geometry import setup_geometry

        setup_geometry(self)
        # Log: startup success for user, or error if exception occurs
        try:
            self.logger.log(self.loc._("user_log_normal_app_started"))
        except Exception as e:
            self.logger.log(self.loc._("user_log_normal_app_failure"))
            import traceback

            detailed_error = (
                "[Startup Failure] WoW Cleanup Tool failed to start.\n"
                f"Reason: {e}\n"
                f"Traceback:\n{traceback.format_exc()}\n"
                "Possible actions: Check your Python environment, dependencies, and configuration files. "
                "See the documentation or report this issue on GitHub with the above details."
            )
            if hasattr(self, "logger"):
                self.logger.error(detailed_error)

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

        save_settings(self.settings)

        # Save user log to disk if append mode is enabled
        if self.settings.get("append_log", False):
            self.logger.save_log_to_disk()
        release_single_instance(getattr(self, "instance_lock", None))
        self.root.destroy()


def main():
    try:
        root = tk.Tk()
        WoWCleanupTool(root)
        root.mainloop()
    except Exception as e:
        from core.error_handler import handle_top_level_exception

        handle_top_level_exception(e)


if __name__ == "__main__":
    main()
