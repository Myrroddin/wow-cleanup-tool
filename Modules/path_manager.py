"""
Path management module for WoW Cleanup Tool.

Handles WoW installation detection, validation, and path selection.
Keeps file selection and path validation logic separate from the main UI.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Modules import localization

def find_wow_root(path):
    """Find the WoW installation root by walking up from a selected path.
    
    Looks for version folders (_retail_, _classic_, etc.) to identify
    the WoW root directory.
    
    Args:
        path: Starting path (may be a version folder or the root itself)
    
    Returns:
        str: The detected WoW root path, or the original path if not found
    """
    path = os.path.abspath(path)
    markers = ["_retail_", "_classic_", "_classic_era_",
               "_retail_ptr_", "_retail_beta_",
               "_classic_ptr_", "_classic_beta_",
               "_classic_era_ptr_", "_classic_era_beta_"]
    for _ in range(6):
        if any(os.path.isdir(os.path.join(path, m)) for m in markers):
            return path
        parent = os.path.dirname(path)
        if parent == path: break
        path = parent
    return path

def is_valid_wow_install(path):
    """Check if a path is a valid WoW installation.
    
    A valid installation has version folders or WoW executables/launchers.
    
    Args:
        path: Path to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not os.path.isdir(path): return False
    indicators = ["_retail_", "_classic_", "_classic_era_",
                  "_retail_ptr_", "_retail_beta_",
                  "_classic_ptr_", "_classic_beta_",
                  "_classic_era_ptr_", "_classic_era_beta_",
                  "Wow.exe", "Launcher.app"]
    return any(os.path.exists(os.path.join(path, it)) for it in indicators)

def select_wow_folder(app):
    """Open a file dialog to select WoW folder and save the selection.
    
    Args:
        app: The WoWCleanupTool instance
    """
    folder = filedialog.askdirectory(title=localization._("select_wow_folder_title"))
    if not folder: return
    corrected = find_wow_root(folder)
    if not is_valid_wow_install(corrected):
        if not messagebox.askyesno(localization._("unrecognized_installation"), localization._("folder_not_valid_continue")):
            return
    app.wow_path_var.set(corrected)
    app.settings["wow_path"] = corrected
    from Modules.settings import save_settings
    save_settings(app.settings)
    app.log(localization._("wow_folder_set").format(corrected))
    refresh_folder_cleaner_tabs(app)

def refresh_folder_cleaner_tabs(app):
    """Rebuild Folder Cleaner tabs to reflect a new WoW path.
    
    Args:
        app: The WoWCleanupTool instance
    """
    try:
        app.version_notebook.destroy()
    except Exception:
        pass
    container = app.folder_tab
    for w in container.winfo_children():
        try: w.destroy()
        except Exception: pass
    app.build_folder_cleaner_tab(container)
