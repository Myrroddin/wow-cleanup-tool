import os
import tkinter as tk
from tkinter import ttk
from Modules.ui_helpers import ImgCheckbox

def build_file_cleaner_tree(app, parent):
    """Build the File Cleaner tab UI onto `parent` using `app` for state.

    This reuses helper methods on the `app` instance (such as
    `_build_checkbox_images` and `_on_tree_click`) so we keep logic
    centralized on the main application while extracting the UI setup.
    """
    bar = ttk.Frame(parent, padding=10)
    bar.pack(fill="x")
    ttk.Button(bar, text="Scan for .bak / .old Files", command=app.scan_files_tree).pack(side="left")
    ttk.Button(bar, text="Expand All", command=app._tree_expand_all).pack(side="left", padx=(8,0))
    ttk.Button(bar, text="Collapse All", command=app._tree_collapse_all).pack(side="left", padx=(8,0))
    app.tree_select_all_var = tk.BooleanVar(value=False)
    app.tree_selall_frame = ImgCheckbox(bar, "Select / Deselect All", app.tree_select_all_var, app.assets)
    app.tree_selall_frame.pack(side="left", padx=(12,0))
    app.tree_select_all_var.trace_add("write", lambda *_: app._tree_toggle_all())
    ttk.Button(bar, text="Process Selected Files", command=app.process_selected_files_tree)\
        .pack(side="left", padx=(8, 0))
    # Use tk.Label instead of ttk.Label so we can color it based on theme
    app.file_scan_status = tk.Label(bar, text="", bg=app.root["bg"], fg="#000000")
    app.file_scan_status.pack(side="left", padx=(10, 0))

    tree_frame = ttk.Frame(parent, padding=(10, 10))
    tree_frame.pack(fill="both", expand=True)
    app.file_tree = ttk.Treeview(tree_frame, columns=("path",), show="tree", selectmode="none")
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=app.file_tree.yview)
    app.file_tree.configure(yscrollcommand=vsb.set)
    app.file_tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    app._build_checkbox_images()
    app.tree_checks = {}
    app.tree_paths = {}
    app.file_tree.bind("<Button-1>", app._on_tree_click)

    return app
