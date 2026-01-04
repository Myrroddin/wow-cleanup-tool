"""License acceptance dialog."""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
from ..dialog_base import BaseDialog
from ..ui_constants import DialogDimensions


class LicenseDialog(BaseDialog):
    """Display license agreement and get user acceptance."""

    def __init__(self, parent, loc, theme_name, settings):
        """Initialize license dialog.

        Args:
            parent: Parent window
            loc: Localization instance
            theme_name: Current theme name ('light' or 'dark')
            settings: Application settings dictionary
        """
        super().__init__(parent, loc, theme_name, settings, "title_license")
        self.accepted = False

    def show(self):
        """Show the license dialog and return acceptance status.

        Returns:
            bool: True if user accepted, False if declined
        """
        # Create dialog window using base class
        dialog = self.create_dialog(
            resizable=True,
            modal=True,
            min_width=DialogDimensions.MIN_LICENSE_WIDTH,
            min_height=DialogDimensions.MIN_LICENSE_HEIGHT,
        )

        # Get theme data for styling elements that don't use BaseDialog helpers
        from core.themes import THEMES

        theme = THEMES.get(self.theme_name, THEMES["light"])

        # Main content frame
        content = self.create_content_frame(dialog)

        # Title (uses built-in styling)
        title = self.create_title_label(content, "title_license")
        title.pack(pady=(0, DialogDimensions.SPACING_MEDIUM))

        # Instructions (using message label which doesn't have explicit styling)
        instructions = self.create_message_label(
            content, "msg_license_instructions", wraplength=DialogDimensions.WRAP_LONG
        )
        instructions.pack(pady=(0, DialogDimensions.SPACING_MEDIUM))

        # License text frame with scrollbar (styled to match theme)
        text_frame = ttk.Frame(content, style="TFrame")
        text_frame.pack(
            fill="both", expand=True, pady=(0, DialogDimensions.SPACING_LARGE)
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, style="TScrollbar")
        scrollbar.pack(side="right", fill="y")

        # Load license text first to determine width
        license_content = self._load_license()

        # Calculate optimal width based on longest line in license text
        lines = license_content.split("\n")
        max_line_length = max(len(line) for line in lines) if lines else 80
        # Use the actual max length without extra buffer to minimize whitespace
        optimal_width = max_line_length

        # Calculate height based on font size (25 rows at 12pt → 2.08x scaling)
        text_height = int(25 * (self.font_size / 12))

        # Text widget for license - with proper theme colors
        license_text = tk.Text(
            text_frame,
            wrap="none",
            yscrollcommand=scrollbar.set,
            width=optimal_width,
            height=text_height,
            bg=theme["entry_bg"],
            fg=theme["entry_fg"],
            insertbackground=theme["fg"],
            selectbackground=theme["select_bg"],
            selectforeground=theme["select_fg"],
            font=(self.font_family, self.font_size),
            relief="flat",
            borderwidth=0,
        )
        license_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=license_text.yview)

        # Display license text
        license_text.insert("1.0", license_content)
        license_text.config(state="disabled")  # Make read-only

        # Don't show again checkbox
        dont_show, dont_show_var = self.create_checkbox(
            content, "option_dont_show_again"
        )
        dont_show.pack(pady=(0, DialogDimensions.SPACING_LARGE))

        # Button frame
        button_frame = ttk.Frame(content, style="TFrame")
        button_frame.pack()

        # Accept button
        accept_button = self.create_button(
            button_frame,
            "license_accept",
            command=lambda: self._on_accept(dialog, dont_show_var),
        )
        accept_button.pack(side="left", padx=DialogDimensions.BUTTON_PADDING)

        # Decline button
        decline_button = self.create_button(
            button_frame, "license_decline", command=lambda: self._on_decline(dialog)
        )
        decline_button.pack(side="left", padx=DialogDimensions.BUTTON_PADDING)

        # Bind Escape to decline
        dialog.bind("<Escape>", lambda e: self._on_decline(dialog))

        # Set focus to accept button
        accept_button.focus_set()

        # Center on screen
        self.center_on_screen()

        # Wait for dialog to close
        dialog.wait_window()

        return self.accepted

    def _load_license(self):
        """Load license text from LICENSE file.

        Returns:
            str: License text content, or error message if not found
        """
        try:
            # Get path to LICENSE file (in root of project)
            license_path = Path(__file__).parent.parent.parent.parent / "LICENSE"
            with open(license_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            # Log error to dev log (unlocalized)
            from core.logger import log_dev_error

            log_dev_error(
                f"[LicenseDialog] LICENSE file not found at {license_path}: {e}"
            )
            return "License file could not be loaded. Please contact support."

    def _on_accept(self, dialog, dont_show_var):
        """Handle Accept button.

        Args:
            dialog: Dialog window to close
            dont_show_var: BooleanVar for don't show again checkbox
        """
        self.accepted = True
        self.settings["license_accepted"] = True
        if dont_show_var.get():
            self.settings["disable_license_dialog"] = True

        # Save settings immediately to persist the preferences
        from core.settings import save_settings

        save_settings(self.settings)

        dialog.destroy()

    def _on_decline(self, dialog):
        """Handle Decline button or Escape key.

        Args:
            dialog: Dialog window to close
        """
        self.accepted = False
        # Don't save anything - user should see license again next time
        dialog.destroy()


def show_license_dialog(parent, loc, theme_name, settings):
    """Show license acceptance dialog.

    Args:
        parent: Parent window
        loc: Localization instance
        theme_name: Current theme name
        settings: Application settings dictionary

    Returns:
        bool: True if user accepted, False if declined
    """
    # Check if user has already accepted and opted to not show again
    if settings.get("license_accepted", False) and settings.get(
        "disable_license_dialog", False
    ):
        return True

    # Show the dialog
    license_dialog = LicenseDialog(parent, loc, theme_name, settings)
    return license_dialog.show()
