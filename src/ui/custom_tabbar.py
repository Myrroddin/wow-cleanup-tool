import tkinter as tk
from tkinter import ttk

class CustomTabBar(tk.Frame):
    def __init__(self, parent, tabs, on_tab_selected, theme_colors=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.tabs = tabs  # List of (tab_id, label)
        self.on_tab_selected = on_tab_selected
        self.buttons = {}
        self.selected_tab = None
        self.theme_colors = theme_colors or {
            'button_bg': '#e1e1e1',
            'button_fg': '#000000',
            'select_bg': '#0078d7',
            'select_fg': '#ffffff',
            'frame_bg': '#f0f0f0',
            'fg': '#000000',
        }

        # Add a background frame to fill the row with the theme's frame_bg color
        self.bg_frame = tk.Frame(self, bg=self.theme_colors['frame_bg'])
        self.bg_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        style = ttk.Style(self)
        style.layout('Tab.TButton', [
            ('Button.focus', {'children': [
                ('Button.padding', {'children': [
                    ('Button.label', {'side': 'left', 'expand': 1})
                ]})
            ]})
        ])
        style.configure('Tab.TButton',
                        padding=(12, 4, 12, 2),
                        relief='flat',
                        borderwidth=1,
                        background=self.theme_colors['button_bg'],
                        foreground=self.theme_colors['button_fg'])
        style.map('Tab.TButton',
                  background=[('pressed', self.theme_colors['select_bg']),
                              ('active', self.theme_colors['frame_bg']),
                              ('!active', self.theme_colors['button_bg'])],
                  foreground=[('pressed', self.theme_colors['select_fg']),
                              ('active', self.theme_colors['fg']),
                              ('!active', self.theme_colors['button_fg'])],
                  relief=[('pressed', 'raised'), ('!pressed', 'flat')])

        style.configure('SelectedTab.TButton',
                        padding=(12, 4, 12, 2),
                        relief='raised',
                        borderwidth=2,
                        background=self.theme_colors['select_bg'],
                        foreground=self.theme_colors['select_fg'])
        self._build()

    def _build(self):
        # Place tab buttons above the background frame
        for idx, (tab_id, label) in enumerate(self.tabs):
            btn = ttk.Button(self, text=label, style='Tab.TButton', command=lambda tid=tab_id: self.select_tab(tid))
            btn.place(in_=self, relx=0, rely=0, x=idx*160, y=0)  # Use place to keep above bg_frame
            self.buttons[tab_id] = btn
        # Make the tab bar expand horizontally and fill the row
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.config(bg=self.theme_colors['frame_bg'])
        if self.tabs:
            self.select_tab(self.tabs[0][0])

    def select_tab(self, tab_id):
        if self.selected_tab == tab_id:
            return
        # Update button styles to look like tabs
        for tid, btn in self.buttons.items():
            if tid == tab_id:
                btn.configure(style='SelectedTab.TButton')
            else:
                btn.configure(style='Tab.TButton')
        self.selected_tab = tab_id
        if self.on_tab_selected:
            self.on_tab_selected(tab_id)

    def get_selected_tab(self):
        return self.selected_tab
