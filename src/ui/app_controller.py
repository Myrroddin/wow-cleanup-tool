"""Event handlers and UI controllers for the main application."""

import tkinter as tk
from tkinter import ttk
from core import themes


class ApplicationController:
    """Controller for handling main application events and UI updates."""

    def update_wow_path(self, new_path):
        """Update the WoW installation path in settings and refresh UI as needed."""
        if not new_path:
            return
        self.settings["wow_path"] = new_path
        # Save settings immediately
        from core.settings import save_settings

        save_settings(self.settings)
        # Update any UI widgets that display the path
        if self.ui_widgets.get("wow_path_var"):
            self.ui_widgets["wow_path_var"].set(new_path)
        # Optionally, refresh any dependent UI or state here
        if self.logger:
            # Use localized message for WoW validation
            from localization import en_us
            if self.logger.verbose:
                # Detect flavors using PathManager
                try:
                    from wow.path_manager import PathManager
                    pm = PathManager()
                    is_valid, flavors = pm.validate_installation(new_path)
                    if is_valid and flavors:
                        # List of localized flavor names
                        flavor_names = ", ".join([name for _, name in flavors])
                        msg = en_us.TRANSLATIONS["user_log_verbose_wow_validated"].replace("{}", flavor_names)
                    else:
                        msg = en_us.TRANSLATIONS["user_log_verbose_wow_validated"].replace("{}", "")
                except Exception:
                    msg = en_us.TRANSLATIONS["user_log_verbose_wow_validated"].replace("{}", "")
            else:
                msg = en_us.TRANSLATIONS["user_log_normal_wow_validated"]
            self.logger.log(msg)

    def handle_new_wow_path(self, new_path):
        """Alias for update_wow_path for backward compatibility."""
        return self.update_wow_path(new_path)

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
        current_theme = self.settings.get("theme", "light")
        new_theme = "dark" if current_theme == "light" else "light"
        self.settings["theme"] = new_theme
        # Apply theme with current font settings
        font_family = self.settings.get("font_family", "TkDefaultFont")
        font_size = self.settings.get("font_size", 9)
        themes.apply_theme(self.root, new_theme, font_family, font_size)
        # Force refresh all widget fonts/styles
        if self.builder and hasattr(self.builder, "refresh_all_widget_fonts"):
            self.builder.refresh_all_widget_fonts()
            # Also refresh all open dialogs
            try:
                from ui.dialog_base import BaseDialog

                BaseDialog.refresh_all_open_dialogs(new_theme, font_family, font_size)
            except Exception:
                pass
        from core.settings import save_settings

        save_settings(self.settings)

    def on_font_size_changed(self, event=None):
        """Handle font size changes and ensure settings and StringVar are updated."""
        import sys

        try:
            font_size_var = self.ui_widgets.get("font_size_var")
            if not font_size_var:
                return
            new_size = int(font_size_var.get())
            self.settings["font_size"] = new_size
            font_size_var.set(str(new_size))
            font_family = self.settings.get("font_family", "TkDefaultFont")
            current_theme = self.settings.get("theme", "light")
            themes.apply_theme(self.root, current_theme, font_family, new_size)
            self._refresh_all_fonts(font_family, new_size)
            self.root.update_idletasks()
            self.resize_to_fit_content()
            # Also refresh all open dialogs
            try:
                from ui.dialog_base import BaseDialog

                BaseDialog.refresh_all_open_dialogs(
                    current_theme, font_family, new_size
                )
            except Exception:
                pass
            from core.settings import save_settings

            save_settings(self.settings)
        except ValueError:
            pass  # Invalid font size, ignore

    def on_font_family_changed(self, event=None):
        """Handle font family changes and ensure settings and StringVar are updated."""
        import sys

        font_family_var = self.ui_widgets.get("font_family_var")
        if not font_family_var:
            return
        selected = font_family_var.get()
        # Map UI label to settings value
        system_default_label = (
            self.builder.loc._("system_default_font")
            if hasattr(self.builder, "loc")
            else "System Default"
        )
        if selected == system_default_label:
            actual_font = "TkDefaultFont"
        else:
            actual_font = selected
        self.settings["font_family"] = actual_font
        font_family_var.set(selected)
        current_theme = self.settings.get("theme", "light")
        font_size = self.settings.get("font_size", 9)
        themes.apply_theme(self.root, current_theme, actual_font, font_size)
        self._refresh_all_fonts(actual_font, font_size)
        self.root.update_idletasks()
        self.resize_to_fit_content()
        # Also refresh all open dialogs
        try:
            from ui.dialog_base import BaseDialog

            BaseDialog.refresh_all_open_dialogs(current_theme, actual_font, font_size)
        except Exception:
            pass
        from core.settings import save_settings

        save_settings(self.settings)

    def on_delete_mode_changed(self, *args):
        """Handle delete mode changes.

        Args:
            *args: Variable trace arguments
        """

        def reset_settings(self):
            """Immediately reset all settings to defaults (preserves cached data like wow_path)."""
            # Store cached data before reset
            wow_path = self.settings.get("wow_path", "")
            geometry = self.settings.get("geometry", "")

            # Clear ALL settings
            self.settings.clear()

            # Reset to defaults (only settings, not cached data)
            self.settings["theme"] = "light"
            self.settings["font_family"] = "TkDefaultFont"
            self.settings["font_size"] = 9
            self.settings["delete_mode"] = "trash"
            self.settings["verbose_logging"] = True
            self.settings["append_log"] = False
            self.settings["language"] = "en"

            # Reset dialog preferences (re-enable all "don't show again" dialogs)
            self.settings["license_accepted"] = False
            self.settings["disable_license_dialog"] = False
            self.settings["disable_wow_close_warning"] = False

            # Restore cached data
            if wow_path:
                self.settings["wow_path"] = wow_path
            if geometry:
                self.settings["geometry"] = geometry

            # Save settings
            from core.settings import save_settings

            save_settings(self.settings)

            # Show reset message
            from tkinter import messagebox

            messagebox.showinfo(
                self.builder.loc._("btn_reset_settings"),
                self.builder.loc._("status_settings_reset") + " applied.",
            )

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
        # No confirmation dialog; reset settings immediately

        # Store cached data before reset
        wow_path = self.settings.get("wow_path", "")
        geometry = self.settings.get("geometry", "")

        # Clear ALL settings
        self.settings.clear()

        # Reset to hardcoded app defaults (not user file contents)
        from core.settings import get_system_language

        self.settings["language"] = get_system_language()
        self.settings["theme"] = "light"
        self.settings["font_family"] = "TkDefaultFont"
        self.settings["font_size"] = 9
        self.settings["delete_mode"] = "trash"
        self.settings["verbose_logging"] = True
        self.settings["append_log"] = False
        self.settings["license_accepted"] = False
        self.settings["disable_license_dialog"] = False
        self.settings["disable_wow_close_warning"] = False

        # Restore cached data
        if wow_path:
            self.settings["wow_path"] = wow_path
        if geometry:
            self.settings["geometry"] = geometry

        # Save settings immediately
        from core.settings import save_settings

        save_settings(self.settings)

        # Update UI widgets to reflect reset values
        if self.ui_widgets.get("font_family_var"):
            self.ui_widgets["font_family_var"].set(
                self.builder.loc._("system_default_font")
                if hasattr(self.builder, "loc")
                else "System Default"
            )

        if self.ui_widgets.get("font_size_var"):
            self.ui_widgets["font_size_var"].set("9")

        if self.ui_widgets.get("delete_mode_var"):
            self.ui_widgets["delete_mode_var"].set("trash")

        if self.ui_widgets.get("verbose_var"):
            self.ui_widgets["verbose_var"].set(True)

        if self.ui_widgets.get("append_log_var"):
            self.ui_widgets["append_log_var"].set(False)

        if self.ui_widgets.get("language_var"):
            self.ui_widgets["language_var"].set("English (US)")

        # Apply default theme (light) and refresh all widget fonts/styles
        themes.apply_theme(self.root, "light", "TkDefaultFont", 9)
        # Force all UI widgets to update theme and font
        if self.builder and hasattr(self.builder, "refresh_all_widget_fonts"):
            self.builder.refresh_all_widget_fonts()
        # Also force refresh of all fonts for classic widgets
        self._refresh_all_fonts("TkDefaultFont", 9)
        # Refresh all open dialogs to new theme
        try:
            from ui.dialog_base import BaseDialog

            BaseDialog.refresh_all_open_dialogs("light", "TkDefaultFont", 9)
        except Exception:
            pass
        # If there are any theme toggle callbacks, trigger them
        if hasattr(self, "on_theme_changed") and callable(self.on_theme_changed):
            self.on_theme_changed()
        # Refresh developer log colors to match new theme
        if self.builder and hasattr(self.builder, "refresh_dev_log_colors"):
            self.builder.refresh_dev_log_colors()

        # Update logger settings
        self.logger.set_verbose(True)
        self.logger.set_append_mode(False)

        # Hide delete log button (append mode disabled)
        if self.builder and hasattr(self.builder, "delete_log_btn"):
            self.builder.delete_log_btn.pack_forget()

        # Resize window
        self.root.update_idletasks()
        self.resize_to_fit_content()

    def _refresh_all_fonts(self, font_family, font_size):
        """Force refresh of all main window widgets to apply new font settings everywhere."""
        import sys
        from core import themes

        # Debug print removed
        # Re-apply theme to root (updates ttk styles)
        current_theme = self.settings.get("theme", "light")
        themes.apply_theme(self.root, current_theme, font_family, font_size)
        # Recursively update all classic widgets in the main frame
        main_frame = self.ui_widgets.get("main_frame")
        if main_frame:
            themes._apply_widget_theme(
                main_frame,
                themes.THEMES.get(current_theme, themes.THEMES["light"]),
                font_family,
                font_size,
            )
        # Refresh classic Tk widgets (Text, etc.)
        for key in ["log_text", "dev_text"]:
            widget = self.ui_widgets.get(key)
            if widget:
                try:
                    widget.configure(font=(font_family, font_size))
                except Exception:
                    pass
