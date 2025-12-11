import tkinter as tk
from tkinter import ttk

class CustomTabBar(tk.Frame):
    def __init__(self, parent, tabs, on_tab_selected, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.tabs = tabs  # List of (tab_id, label)
        self.on_tab_selected = on_tab_selected
        self.buttons = {}
        self.selected_tab = None
        self._build()

    def _build(self):
        for idx, (tab_id, label) in enumerate(self.tabs):
            btn = ttk.Button(self, text=label, command=lambda tid=tab_id: self.select_tab(tid))
            btn.grid(row=0, column=idx, sticky='nsew', padx=(0, 2))
            self.buttons[tab_id] = btn
            self.grid_columnconfigure(idx, weight=1)
        if self.tabs:
            self.select_tab(self.tabs[0][0])

    def select_tab(self, tab_id):
        if self.selected_tab == tab_id:
            return
        # Update button styles
        for tid, btn in self.buttons.items():
            if tid == tab_id:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])
        self.selected_tab = tab_id
        if self.on_tab_selected:
            self.on_tab_selected(tab_id)

    def get_selected_tab(self):
        return self.selected_tab
