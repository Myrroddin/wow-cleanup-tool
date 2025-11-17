import os
import tkinter as tk
from tkinter import ttk
from Modules.ui_helpers import ImgCheckbox
from Modules import localization

def build_folder_cleaner_tab(app, parent):
    """Build a per-version Folder Cleaner notebook into `parent` using `app` for state."""
    app.version_notebook = ttk.Notebook(parent)
    app.version_notebook.pack(fill="both", expand=True, padx=10, pady=10)
    base = app.wow_path_var.get().strip()
    app.version_tabs.clear()
    app.folder_paths.clear()
    # Clear styled checkboxes lists for theme refresh
    app.styled_folder_boxes = []
    app.styled_shot_boxes = []
    if base and os.path.isdir(base):
        versions = app._enumerate_versions(base)
        for vpath, vlabel in versions:
            tab = ttk.Frame(app.version_notebook)
            app.version_notebook.add(tab, text=vlabel)
            widgets = app._build_single_version_tab(tab, vpath, vlabel)
            app.version_tabs.append((vlabel, vpath, widgets))
    else:
        info = ttk.Frame(parent, padding=12)
        info.pack(fill="both", expand=True)
        ttk.Label(info, text=localization._("select_valid_wow_folder_cleaner")).pack()

    return app
