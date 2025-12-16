"""Game Optimizer Tab UI for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk


class GameOptimizerTab:
    def __init__(self, parent, loc):
        self.frame = ttk.Frame(parent, padding=5)
        self._create_content(loc)

    def _create_content(self, loc):
        label = ttk.Label(self.frame, text="[DEBUG] Game Optimizer Content")
        label.pack(side="top", fill="x", pady=(0, 10))
