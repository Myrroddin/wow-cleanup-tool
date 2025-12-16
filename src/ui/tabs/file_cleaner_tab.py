"""File Cleaner Tab UI for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk


class FileCleanerTab:
    def __init__(
        self,
        parent,
        loc,
        on_scan_files,
        on_select_all_toggle,
        on_remove_selected,
        get_selectable_items,
        get_selected_items,
    ):
        self.frame = ttk.Frame(parent, padding=5)
        self._create_content(
            loc,
            on_scan_files,
            on_select_all_toggle,
            on_remove_selected,
            get_selectable_items,
            get_selected_items,
        )

    def _create_content(
        self,
        loc,
        on_scan_files,
        on_select_all_toggle,
        on_remove_selected,
        get_selectable_items,
        get_selected_items,
    ):
        desc_label = ttk.Label(
            self.frame, text=loc._("desc_file_cleaner"), justify="left"
        )
        desc_label.pack(side="top", fill="x", pady=(0, 10))
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(side="top", fill="x", pady=(0, 10))
        scan_btn = ttk.Button(
            button_frame, text=loc._("btn_scan_files"), command=on_scan_files
        )
        scan_btn.pack(side="left", padx=(0, 10))
        select_all_btn = ttk.Button(
            button_frame,
            text=loc._("btn_select_all_toggle"),
            command=lambda: on_select_all_toggle(get_selectable_items("file_cleaner")),
        )
        select_all_btn.pack(side="left", padx=(0, 10))
        remove_btn = ttk.Button(
            button_frame,
            text=loc._("btn_remove_selected"),
            command=lambda: on_remove_selected(get_selected_items("file_cleaner")),
        )
        remove_btn.pack(side="left")
