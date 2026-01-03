"""Screenshot viewer dialog for displaying enlarged screenshots."""

import tkinter as tk
from ..dialog_base import BaseDialog


class ScreenshotViewer(BaseDialog):
    """Display a screenshot at 50% of screen size in a popup window."""

    def __init__(self, parent, loc, theme_name, settings, image_path):
        """Initialize screenshot viewer dialog.

        Args:
            parent: Parent window
            loc: Localization instance
            theme_name: Current theme name ('light' or 'dark')
            settings: Application settings dictionary
            image_path: Path to the screenshot file
        """
        super().__init__(parent, loc, theme_name, settings, "title_main_window")
        self.image_path = image_path
        self.photo_image = None

    def show(self):
        """Display the screenshot viewer dialog.

        Returns:
            None
        """
        try:
            from PIL import Image, ImageTk
        except ImportError:
            return

        # Load image
        try:
            img = Image.open(self.image_path)
        except Exception:
            return

        # Get screen dimensions
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        # Calculate 50% of screen size
        target_width = int(screen_width * 0.50)
        target_height = int(screen_height * 0.50)

        # Scale image to fit within target size while preserving aspect ratio
        original_width, original_height = img.size
        aspect_ratio = original_width / original_height

        if aspect_ratio > (target_width / target_height):
            # Width is the limiting factor
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            # Height is the limiting factor
            new_height = target_height
            new_width = int(target_height * aspect_ratio)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(img)

        # Create dialog window
        dialog = self.create_dialog(
            resizable=False,
            modal=True,
            min_width=None,
            min_height=None,
        )

        # Get theme data for canvas background
        from core.themes import THEMES

        theme = THEMES.get(self.theme_name, THEMES["light"])

        # Create canvas to display image
        canvas = tk.Canvas(
            dialog,
            width=new_width,
            height=new_height,
            bg=theme["bg"],
            highlightthickness=0,
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        # Display image
        canvas.create_image(new_width // 2, new_height // 2, image=self.photo_image)

        # Set window size to match image
        dialog.geometry(f"{new_width}x{new_height}")

        # Center the dialog on screen
        x = (screen_width - new_width) // 2
        y = (screen_height - new_height) // 2
        dialog.geometry(f"{new_width}x{new_height}+{x}+{y}")

        # Bind close events
        def close_dialog(event=None):
            dialog.destroy()

        canvas.bind("<Button-1>", close_dialog)
        dialog.bind("<Escape>", close_dialog)
        dialog.protocol("WM_DELETE_WINDOW", close_dialog)

        # Wait for dialog to close
        dialog.wait_window()
