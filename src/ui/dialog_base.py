"""Base dialog functionality for consistent dialog creation."""

import tkinter as tk
from tkinter import ttk
from core.themes import apply_theme
from .ui_constants import DialogDimensions, DialogFontSizes


class BaseDialog:
    # Track all open dialog instances
    _open_dialogs = set()
    """Base class for application dialogs with theme and localization support."""

    def __init__(self, parent, loc, theme_name, settings, title_key):
        """Initialize base dialog.

        Args:
            parent: Parent window
            loc: Localization instance
            theme_name: Current theme name ('light' or 'dark')
            settings: Application settings dictionary
            title_key: Localization key for dialog title
        """
        self.parent = parent
        self.loc = loc
        self.theme_name = theme_name
        self.settings = settings
        self.title_key = title_key
        self.font_family = settings.get("font_family", "TkDefaultFont")
        self.font_size = settings.get("font_size", 12)
        self.dialog = None

        # Register this dialog instance
        BaseDialog._open_dialogs.add(self)

    def create_dialog(
        self, resizable=False, modal=True, min_width=None, min_height=None
    ):
        """Create a themed dialog window.

        Args:
            resizable: Whether dialog should be resizable
            modal: Whether dialog should be modal (grab focus)
            min_width: Minimum width (optional)
            min_height: Minimum height (optional)

        Returns:
            tk.Toplevel: Created dialog window
        """
        dialog = tk.Toplevel(self.parent)
        dialog.title(self.loc._(self.title_key))

        # Handle transient behavior
        try:
            if self.parent.state() != "withdrawn":
                dialog.transient(self.parent)
        except (tk.TclError, AttributeError):
            pass

        if modal:
            dialog.grab_set()

        dialog.resizable(resizable, resizable)

        if min_width and min_height:
            dialog.minsize(min_width, min_height)

        # Apply theme to dialog
        apply_theme(dialog, self.theme_name, self.font_family, self.font_size)

        self.dialog = dialog

        # Remove from open dialogs when closed
        def _on_destroy(event=None):
            BaseDialog._open_dialogs.discard(self)

        dialog.bind("<Destroy>", _on_destroy)
        return dialog

    def refresh_theme_and_fonts(
        self, theme_name=None, font_family=None, font_size=None
    ):
        """Re-apply theme and font to this dialog."""
        if not self.dialog:
            return
        if theme_name is not None:
            self.theme_name = theme_name
        if font_family is not None:
            self.font_family = font_family
        if font_size is not None:
            self.font_size = font_size
        apply_theme(self.dialog, self.theme_name, self.font_family, self.font_size)

        # Optionally, force style re-application for all children
        def refresh_ttk_styles(widget):
            try:
                style = widget.cget("style")
                if style:
                    widget.configure(style=style)
            except Exception:
                pass
            for child in widget.winfo_children():
                refresh_ttk_styles(child)

        refresh_ttk_styles(self.dialog)

    @classmethod
    def refresh_all_open_dialogs(cls, theme_name, font_family, font_size):
        for dlg in list(cls._open_dialogs):
            dlg.refresh_theme_and_fonts(theme_name, font_family, font_size)

    def create_content_frame(self, dialog, padding=None):
        """Create main content frame for dialog.

        Args:
            dialog: Dialog window
            padding: Padding amount (default: DialogDimensions.CONTENT_PADDING)

        Returns:
            ttk.Frame: Content frame
        """
        if padding is None:
            padding = DialogDimensions.CONTENT_PADDING

        content = ttk.Frame(dialog, padding=padding)
        content.pack(fill="both", expand=True)
        return content

    def create_title_label(self, parent, text_key, wraplength=None):
        """Create a styled title label.

        Args:
            parent: Parent widget
            text_key: Localization key for title text
            wraplength: Optional wrap length

        Returns:
            ttk.Label: Title label
        """
        style_name = f"DialogTitle.TLabel.{id(self)}"
        self._configure_title_style(style_name)

        label = ttk.Label(parent, text=self.loc._(text_key), style=style_name)
        if wraplength:
            label.configure(wraplength=wraplength)
        return label

    def create_subtitle_label(self, parent, text_key, wraplength=None):
        """Create a styled subtitle label.

        Args:
            parent: Parent widget
            text_key: Localization key for subtitle text
            wraplength: Optional wrap length

        Returns:
            ttk.Label: Subtitle label
        """
        style_name = f"DialogSubtitle.TLabel.{id(self)}"
        self._configure_subtitle_style(style_name)

        label = ttk.Label(parent, text=self.loc._(text_key), style=style_name)
        if wraplength:
            label.configure(wraplength=wraplength)
        return label

    def create_warning_icon(self, parent, icon_symbol=None):
        """Create a warning icon label.

        Args:
            parent: Parent widget
            icon_symbol: Symbol to display (default from localization)

        Returns:
            ttk.Label: Warning icon label
        """
        if icon_symbol is None:
            icon_symbol = self.loc._("warning_icon")

        style_name = f"WarningIcon.TLabel.{id(self)}"
        self._configure_icon_style(style_name)

        label = ttk.Label(parent, text=icon_symbol, style=style_name)
        return label

    def create_message_label(self, parent, text_key, wraplength=None, justify=None):
        """Create a message label.

        Args:
            parent: Parent widget
            text_key: Localization key for message text
            wraplength: Wrap length (default: DialogDimensions.WRAP_MEDIUM)
            justify: Text justification ('left', 'center', 'right')

        Returns:
            ttk.Label: Message label
        """
        if wraplength is None:
            wraplength = DialogDimensions.WRAP_MEDIUM

        if justify is None:
            justify = "left"

        label = ttk.Label(
            parent, text=self.loc._(text_key), wraplength=wraplength, justify=justify
        )
        return label

    def create_button(self, parent, text_key, command, width=None):
        """Create a themed button.

        Args:
            parent: Parent widget
            text_key: Localization key for button text
            command: Button command callback
            width: Button width (default: DialogDimensions.BUTTON_WIDTH_STANDARD)

        Returns:
            ttk.Button: Button widget
        """
        if width is None:
            width = DialogDimensions.BUTTON_WIDTH_STANDARD

        button = ttk.Button(
            parent, text=self.loc._(text_key), command=command, width=width
        )
        return button

    def create_checkbox(self, parent, text_key, variable=None):
        """Create a themed checkbox.

        Args:
            parent: Parent widget
            text_key: Localization key for checkbox text
            variable: BooleanVar to associate with checkbox

        Returns:
            ttk.Checkbutton: Checkbox widget
        """
        if variable is None:
            variable = tk.BooleanVar(value=False)

        checkbox = ttk.Checkbutton(parent, text=self.loc._(text_key), variable=variable)
        return checkbox, variable

    def center_on_parent(self):
        """Center dialog on parent window."""
        if not self.dialog:
            return

        self.dialog.update_idletasks()

        # Get dialog dimensions
        dialog_w = self.dialog.winfo_width()
        dialog_h = self.dialog.winfo_height()

        try:
            # Get parent dimensions and position
            parent_x = self.parent.winfo_x()
            parent_y = self.parent.winfo_y()
            parent_w = self.parent.winfo_width()
            parent_h = self.parent.winfo_height()

            # Calculate centered position
            x = parent_x + (parent_w - dialog_w) // 2
            y = parent_y + (parent_h - dialog_h) // 2
        except (tk.TclError, AttributeError):
            # Fall back to screen center if parent position unavailable
            screen_w = self.dialog.winfo_screenwidth()
            screen_h = self.dialog.winfo_screenheight()
            x = (screen_w - dialog_w) // 2
            y = (screen_h - dialog_h) // 2

        self.dialog.geometry(f"+{x}+{y}")

    def center_on_screen(self):
        """Center dialog on screen."""
        if not self.dialog:
            return

        self.dialog.update_idletasks()

        # Get dialog dimensions
        dialog_w = self.dialog.winfo_width()
        dialog_h = self.dialog.winfo_height()

        # Get screen dimensions
        screen_w = self.dialog.winfo_screenwidth()
        screen_h = self.dialog.winfo_screenheight()

        # Calculate center position
        x = (screen_w - dialog_w) // 2
        y = (screen_h - dialog_h) // 2

        self.dialog.geometry(f"+{x}+{y}")

    def _configure_title_style(self, style_name):
        """Configure title label style.

        Args:
            style_name: Unique style name for this instance
        """
        if not self.dialog:
            return

        style = ttk.Style(self.dialog)
        from core.themes import THEMES

        theme = THEMES.get(self.theme_name, THEMES["light"])

        title_size = DialogFontSizes.get_title_size(self.font_size)
        # Use TLabel as the base layout
        style.layout(style_name, style.layout("TLabel"))
        style.configure(
            style_name,
            background=theme["frame_bg"],
            foreground=theme["fg"],
            font=(self.font_family, title_size, "bold"),
        )

    def _configure_subtitle_style(self, style_name):
        """Configure subtitle label style.

        Args:
            style_name: Unique style name for this instance
        """
        if not self.dialog:
            return

        style = ttk.Style(self.dialog)
        from core.themes import THEMES

        theme = THEMES.get(self.theme_name, THEMES["light"])

        subtitle_size = DialogFontSizes.get_subtitle_size(self.font_size)
        # Use TLabel as the base layout
        style.layout(style_name, style.layout("TLabel"))
        style.configure(
            style_name,
            background=theme["frame_bg"],
            foreground=theme["fg"],
            font=(self.font_family, subtitle_size, "bold"),
        )

    def _configure_icon_style(self, style_name):
        """Configure icon label style.

        Args:
            style_name: Unique style name for this instance
        """
        if not self.dialog:
            return

        style = ttk.Style(self.dialog)
        from core.themes import THEMES

        theme = THEMES.get(self.theme_name, THEMES["light"])

        icon_size = DialogFontSizes.get_icon_size(self.font_size)
        # Use TLabel as the base layout
        style.layout(style_name, style.layout("TLabel"))
        style.configure(
            style_name,
            background=theme["frame_bg"],
            foreground=theme["fg"],
            font=(self.font_family, icon_size),
        )
