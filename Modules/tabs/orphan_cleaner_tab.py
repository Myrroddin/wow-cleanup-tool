import os
import tkinter as tk
from tkinter import ttk
from Modules.ui_helpers import ImgCheckbox

def build_orphan_cleaner_tab(app, parent):
    """Build the Orphan Cleaner tab UI onto `parent` using `app` for state."""
    description_text = (
        "Searches all detected WoW versions for addon SavedVariables (.lua / .lua.bak) that do not have a corresponding installed addon (Interface/AddOns). Scans Account, Realm, and Character SavedVariables folders. Processing also rebuilds AddOns." + "\u200B" + "txt to match installed addons (preserving enabled/disabled where possible).\n\n"
        "Note: Blizzard_*.lua files are core game data and are automatically ignored for safety (but their .lua.bak backups may be removed)."
    )
    desc = ttk.Label(parent, padding=(10, 10),
        text=description_text,
        wraplength=max(200, parent.winfo_width() - 40), justify="left")
    desc.pack(fill="x")

    def update_wraplength(event):
        # Subtract padding margin to prevent text cutoff
        desc.configure(wraplength=max(200, parent.winfo_width() - 40))

    parent.bind("<Configure>", update_wraplength)

    bar = ttk.Frame(parent, padding=(10, 0)); bar.pack(fill="x")
    ttk.Button(bar, text="Scan for Orphaned SavedVariables", command=app.scan_orphan_savedvars).pack(side="left")
    ttk.Button(bar, text="Expand All", command=app._orphan_tree_expand_all).pack(side="left", padx=(8,0))
    ttk.Button(bar, text="Collapse All", command=app._orphan_tree_collapse_all).pack(side="left", padx=(8,0))

    app.orphan_select_all_var = tk.BooleanVar(value=False)
    app.orphan_selall_frame = ImgCheckbox(bar, "Select / Deselect All", app.orphan_select_all_var, app.assets)
    app.orphan_selall_frame.pack(side="left", padx=(12,0))
    app.orphan_select_all_var.trace_add("write", lambda *_: app._orphan_tree_toggle_all())

    ttk.Button(bar, text="Process Selected Files", command=app.process_selected_orphans)\
        .pack(side="left", padx=(8, 0))
    # Use tk.Label instead of ttk.Label so we can color it based on theme
    app.orphan_scan_status = tk.Label(bar, text="", bg=app.root["bg"], fg="#000000")
    app.orphan_scan_status.pack(side="left", padx=(10, 0))

    tree_frame = ttk.Frame(parent, padding=(10, 10)); tree_frame.pack(fill="both", expand=True)
    app.orphan_tree = ttk.Treeview(tree_frame, columns=("path",), show="tree", selectmode="none")
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=app.orphan_tree.yview)
    app.orphan_tree.configure(yscrollcommand=vsb.set)
    app.orphan_tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    app._build_checkbox_images()
    app.orphan_checks = {}
    app.orphan_paths = {}
    app.orphan_tree.bind("<Button-1>", app._on_orphan_tree_click)

    return app
