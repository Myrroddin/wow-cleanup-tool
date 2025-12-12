"""Multiple WoW installations error dialog."""

from tkinter import ttk
from ..dialog_base import BaseDialog
from ..ui_constants import DialogDimensions


class MultipleInstallationsDialog(BaseDialog):
    """Dialog warning about multiple WoW installations."""

    def __init__(self, parent, loc, theme_name, settings, installations):
        """Initialize the dialog.

        Args:
            parent: Parent window
            loc: Localization instance
            theme_name: Theme name ('light' or 'dark')
            settings: Application settings dictionary
            installations: List of detected installation paths
        """
        super().__init__(
            parent, loc, theme_name, settings, "title_multiple_installations"
        )
        self.installations = installations

    def show(self):
        """Show the dialog.

        Returns:
            None: User must acknowledge and application will exit
        """
        # Create dialog window
        dialog = self.create_dialog(
            resizable=False,
            modal=True,
            min_width=DialogDimensions.WRAP_LONG,
            min_height=300,
        )

        # Content frame
        content = self.create_content_frame(dialog)

        # Warning icon and title
        title_frame = ttk.Frame(content)
        title_frame.pack(fill="x", pady=(0, DialogDimensions.SPACING_MEDIUM))

        icon = self.create_warning_icon(title_frame)
        icon.pack()

        title = self.create_subtitle_label(title_frame, "title_multiple_installations")
        title.pack()

        # Main message
        message = self.create_message_label(
            content, "msg_multiple_installations", wraplength=DialogDimensions.WRAP_LONG
        )
        message.pack(pady=DialogDimensions.SPACING_MEDIUM)

        # List of detected installations
        installations_frame = ttk.LabelFrame(
            content, text=self.loc._("label_detected_installations"), padding=10
        )
        installations_frame.pack(pady=DialogDimensions.SPACING_MEDIUM, fill="x")

        for install_path in self.installations:
            path_label = ttk.Label(installations_frame, text=f"• {install_path}")
            path_label.pack(pady=2, anchor="w")

        # Instructions
        instructions = self.create_message_label(
            content,
            "msg_multiple_installations_instructions",
            wraplength=DialogDimensions.WRAP_LONG - 100,
        )
        instructions.pack(pady=DialogDimensions.SPACING_MEDIUM)

        # OK button (will close dialog)
        button_frame = ttk.Frame(content)
        button_frame.pack(side="bottom", pady=(DialogDimensions.SPACING_MEDIUM, 0))

        ok_button = self.create_button(
            button_frame, "ok", command=lambda: dialog.destroy()
        )
        ok_button.pack(side="right", padx=DialogDimensions.BUTTON_PADDING)

        # Center on parent
        self.center_on_parent()

        # Wait for dialog to close
        dialog.wait_window()


def show_multiple_installations_dialog(
    parent, loc, theme_name, settings, installations
):
    """Show dialog about multiple WoW installations.

    Args:
        parent: Parent window
        loc: Localization instance
        theme_name: Theme name ('light' or 'dark')
        settings: Application settings dictionary
        installations: List of detected installation paths
    """
    dialog = MultipleInstallationsDialog(
        parent, loc, theme_name, settings, installations
    )
    dialog.show()
