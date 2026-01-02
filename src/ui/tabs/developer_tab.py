"""Developer Log Tab UI for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk


class DeveloperTab:
    def __init__(self, parent, loc, log_controls, font_size=12):
        self.frame = ttk.Frame(parent, padding=5)
        self.font_size = font_size
        self._create_content(loc, log_controls)

    def _create_content(self, loc, log_controls):
        # Description label
        desc_label = ttk.Label(
            self.frame,
            text=loc._("desc_developer_log"),
            justify="left",
            wraplength=600,
        )
        desc_label.grid(row=0, column=0, sticky="ew", pady=(0, 6))

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
