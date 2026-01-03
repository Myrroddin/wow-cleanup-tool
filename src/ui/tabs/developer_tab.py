"""Developer Log Tab UI for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk


class DeveloperTab:
    def __init__(self, parent, loc, log_controls, font_size=12):
        self.frame = ttk.Frame(parent, padding=5)
        self.font_size = font_size
        self._configure_timer = None  # Debounce timer for configure events
        self._create_content(loc, log_controls)

    def _create_content(self, loc, log_controls):
        # Description label with dynamic wraplength based on widget width
        self.desc_label = ttk.Label(
            self.frame,
            text=loc._("desc_developer_log"),
            justify="left",
        )
        self.desc_label.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        # Bind to configure event with debouncing to reduce flicker
        self.desc_label.bind("<Configure>", self._debounced_update_wraplength)

        # Controls row - buttons in container frame
        controls = ttk.Frame(self.frame)
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        clear_btn = ttk.Button(
            controls, text=loc._("btn_clear_log"), command=log_controls["clear"]
        )
        clear_btn.grid(row=0, column=0, padx=(0, 8))

        open_folder_btn = ttk.Button(
            controls,
            text=loc._("btn_open_log_folder"),
            command=log_controls["open_folder"],
        )
        open_folder_btn.grid(row=0, column=1, padx=(0, 8))

        copy_btn = ttk.Button(
            controls, text=loc._("btn_copy_log"), command=log_controls["copy"]
        )
        copy_btn.grid(row=0, column=2)

        # Log display area
        # Calculate height based on font size (18 rows at 12pt → 1.5x scaling)
        text_height = int(18 * (self.font_size / 12))
        self.log_text = tk.Text(
            self.frame, wrap="word", height=text_height, width=80, state="disabled"
        )
        self.log_text.grid(row=2, column=0, sticky="nsew")

        # Configure expansion
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def _update_wraplength(self, event=None):
        """Update wraplength based on actual widget width."""
        if hasattr(self, "desc_label"):
            # Get actual widget width, subtract padding for margins
            width = self.desc_label.winfo_width()
            if width > 1:  # Ensure widget is actually rendered
                self.desc_label.configure(wraplength=max(width - 20, 100))

    def _debounced_update_wraplength(self, event=None):
        """Debounce wraplength updates to reduce flicker during resize."""
        # Cancel existing timer if any
        if self._configure_timer:
            self.frame.after_cancel(self._configure_timer)
        # Schedule update after 50ms of no resize events
        self._configure_timer = self.frame.after(50, self._update_wraplength)

    def refresh_wraplength(self, font_size):
        """Update description label wraplength when font size changes."""
        self.font_size = font_size
        # Trigger a wraplength update based on current width
        self._update_wraplength()
