"""User Log Tab UI for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk


class LogTab:
    def __init__(self, parent, loc, log_controls):
        self.frame = ttk.Frame(parent, padding=5)
        self._create_content(loc, log_controls)

    def _create_content(self, loc, log_controls):
        controls = ttk.Frame(self.frame)
        controls.pack(side="top", fill="x", pady=(0, 5))
        # Buttons will be added by main window using log_controls
