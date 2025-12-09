"""WoW close warning dialog."""
from tkinter import ttk
from ..dialog_base import BaseDialog
from ..ui_constants import DialogDimensions


class WoWCloseWarning(BaseDialog):
    """Display warning to close WoW before using the tool."""
    
    def __init__(self, parent, loc, theme_name, settings):
        """Initialize and show the WoW close warning dialog.
        
        Args:
            parent: Parent window
            loc: Localization instance
            theme_name: Current theme name ('light' or 'dark')
            settings: Application settings dictionary
        """
        super().__init__(parent, loc, theme_name, settings, 'warning')
        
    def show(self):
        """Show the warning dialog centered on parent."""
        # Create dialog window using base class
        dialog = self.create_dialog(
            resizable=False,
            modal=True,
            min_width=DialogDimensions.MIN_SIMPLE_WARNING_WIDTH,
            min_height=DialogDimensions.MIN_SIMPLE_WARNING_HEIGHT
        )
        
        # Make dialog unmovable
        dialog.protocol("WM_DELETE_WINDOW", lambda: self._on_ok(dialog))
        
        # Content frame with padding
        content = self.create_content_frame(dialog)
        
        # Warning icon and title frame
        title_frame = ttk.Frame(content)
        title_frame.pack(fill='x', pady=(0, DialogDimensions.SPACING_LARGE))
        
        # Warning symbol
        warning_icon = self.create_warning_icon(title_frame)
        warning_icon.pack(side='left', padx=(0, DialogDimensions.SPACING_MEDIUM))
        
        # Title text
        title = self.create_subtitle_label(title_frame, 'warning')
        title.pack(side='left')
        
        # Warning message
        message = self.create_message_label(
            content, 'msg_wow_close_warning',
            wraplength=DialogDimensions.WRAP_SHORT
        )
        message.pack(pady=(0, DialogDimensions.SPACING_XLARGE))
        
        # Don't show again checkbox
        dont_show, dont_show_var = self.create_checkbox(content, 'option_dont_show_again')
        dont_show.pack(pady=(0, DialogDimensions.SPACING_XLARGE))
        
        # OK button centered
        button_frame = ttk.Frame(content)
        button_frame.pack()
        
        ok_button = self.create_button(
            button_frame, 'ok',
            command=lambda: self._on_ok(dialog, dont_show_var)
        )
        ok_button.pack()
        
        # Bind Escape key to close
        dialog.bind('<Escape>', lambda e: self._on_ok(dialog, dont_show_var))
        
        # Set focus to OK button
        ok_button.focus_set()
        
        # Center on parent window
        self.center_on_parent()
        
        # Wait for dialog to close
        dialog.wait_window()
    
    def _on_ok(self, dialog, dont_show_var=None):
        """Handle OK button or Escape key.
        
        Args:
            dialog: Dialog window to close
            dont_show_var: BooleanVar for don't show again checkbox (optional)
        """
        if dont_show_var and dont_show_var.get():
            self.settings['disable_wow_close_warning'] = True
            # Save settings immediately to persist the preference
            from ...core.settings import save_settings
            save_settings(self.settings)
        dialog.destroy()


def show_wow_close_warning(parent, loc, theme_name, settings):
    """Show WoW close warning dialog.
    
    Args:
        parent: Parent window
        loc: Localization instance
        theme_name: Current theme name
        settings: Application settings dictionary
    """
    # Check if user has disabled this warning
    if settings.get('disable_wow_close_warning', False):
        return
    
    warning = WoWCloseWarning(parent, loc, theme_name, settings)
    warning.show()
