"""Developer Log Tab UI for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk


class DeveloperTab:
    def __init__(self, parent, loc, log_controls):
        self.frame = ttk.Frame(parent, padding=5)
        self._create_content(loc, log_controls)

    def _create_content(self, loc, log_controls):
        # Controls row
        controls = ttk.Frame(self.frame)
        controls.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        controls.columnconfigure(0, weight=1)
        clear_btn = ttk.Button(controls, text=loc._("btn_clear_log"))
        clear_btn.grid(row=0, column=0, padx=(0, 8))
        save_btn = ttk.Button(controls, text=loc._("btn_save_log"))
        save_btn.grid(row=0, column=1, padx=(0, 8))
        copy_btn = ttk.Button(controls, text=loc._("btn_copy_log"))
        copy_btn.grid(row=0, column=2, padx=(0, 8))

        # Log display area
        self.log_text = tk.Text(
            self.frame, wrap="word", height=18, width=80, state="disabled"
        )
        self.log_text.grid(row=1, column=0, sticky="nsew")
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
