"""
Update checker module for WoW Cleanup Tool.

Handles checking for new releases on GitHub and downloading updates.
"""

import urllib.request
import urllib.error
import json
import os
import tempfile
import threading
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from Modules import localization

GITHUB_REPO = "Myrroddin/wow-cleanup-tool"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

def get_latest_release_info():
    """Fetch the latest release information from GitHub.
    
    Returns:
        dict: Release data including tag_name, assets, etc., or None on error
    """
    try:
        with urllib.request.urlopen(GITHUB_API_URL, timeout=5) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None

def download_update(download_url, app=None):
    """Download the update file with a progress dialog.
    
    Args:
        download_url: URL to download the update from
        app: Parent application instance for theming
        
    Returns:
        str: Path to downloaded file, or None if cancelled/failed
    """
    _ = localization.get_text
    
    # Create themed download dialog
    dialog = tk.Toplevel()
    dialog.title(_("downloading_update"))
    dialog.resizable(False, False)
    dialog.transient(app.root if app else None)
    dialog.grab_set()
    
    # Apply theme if available
    if app and hasattr(app, 'theme_data'):
        bg = app.theme_data.get("bg", "#f0f0f0")
        fg = app.theme_data.get("fg", "#000000")
        dialog.configure(bg=bg)
    else:
        bg = "#f0f0f0"
        fg = "#000000"
    
    # Center the dialog
    dialog.update_idletasks()
    width = 400
    height = 150
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    # Content frame
    frame = ttk.Frame(dialog, padding=20)
    frame.pack(fill="both", expand=True)
    
    # Status label
    status_label = ttk.Label(frame, text=_("downloading_update_file"))
    status_label.pack(pady=(0, 10))
    
    # Progress bar
    progress = ttk.Progressbar(frame, mode='determinate', length=350)
    progress.pack(pady=(0, 10))
    
    # Size label
    size_label = ttk.Label(frame, text="0 MB / 0 MB")
    size_label.pack()
    
    # Cancel button
    cancelled = {"value": False}
    
    def cancel_download():
        cancelled["value"] = True
        dialog.destroy()
    
    cancel_btn = ttk.Button(frame, text=_("cancel"), command=cancel_download)
    cancel_btn.pack(pady=(10, 0))
    
    # Download in thread
    download_path = {"path": None}
    
    def download_thread():
        try:
            # Get filename from URL
            filename = download_url.split("/")[-1]
            if not filename.endswith(('.exe', '.zip')):
                filename = "wow_cleanup_tool_update.exe"
            
            # Download to temp directory
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, filename)
            
            def reporthook(block_num, block_size, total_size):
                if cancelled["value"]:
                    raise Exception("Download cancelled")
                    
                downloaded = block_num * block_size
                if total_size > 0:
                    percent = min(100, (downloaded / total_size) * 100)
                    progress['value'] = percent
                    
                    # Update size label
                    downloaded_mb = downloaded / (1024 * 1024)
                    total_mb = total_size / (1024 * 1024)
                    size_label.config(text=f"{downloaded_mb:.1f} MB / {total_mb:.1f} MB")
            
            urllib.request.urlretrieve(download_url, file_path, reporthook)
            download_path["path"] = file_path
            dialog.after(100, dialog.destroy)
            
        except Exception as e:
            if not cancelled["value"]:
                dialog.after(100, lambda: show_download_error(str(e), app))
            dialog.after(100, dialog.destroy)
    
    # Start download
    thread = threading.Thread(target=download_thread, daemon=True)
    thread.start()
    
    dialog.wait_window()
    return download_path["path"]

def show_download_error(error_msg, app=None):
    """Show download error message."""
    _ = localization.get_text
    messagebox.showerror(
        _("download_failed"),
        _("download_failed_message").format(error_msg),
        parent=app.root if app else None
    )

def show_install_prompt(file_path, app=None):
    """Show install prompt dialog with themed styling.
    
    Args:
        file_path: Path to the downloaded update file
        app: Parent application instance
        
    Returns:
        bool: True if user chose to install now
    """
    _ = localization.get_text
    
    # Create custom themed dialog
    dialog = tk.Toplevel()
    dialog.title(_("update_ready"))
    dialog.resizable(False, False)
    dialog.transient(app.root if app else None)
    dialog.grab_set()
    
    # Apply theme
    if app and hasattr(app, 'theme_data'):
        bg = app.theme_data.get("bg", "#f0f0f0")
        fg = app.theme_data.get("fg", "#000000")
        dialog.configure(bg=bg)
    else:
        bg = "#f0f0f0"
        fg = "#000000"
    
    # Center dialog
    dialog.update_idletasks()
    width = 450
    height = 200
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    # Content frame
    frame = ttk.Frame(dialog, padding=20)
    frame.pack(fill="both", expand=True)
    
    # Message
    msg_text = _("update_downloaded_message").format(os.path.basename(file_path))
    msg_label = ttk.Label(frame, text=msg_text, wraplength=400, justify="center")
    msg_label.pack(pady=(0, 20))
    
    # Buttons
    result = {"install": False}
    
    def install_now():
        result["install"] = True
        dialog.destroy()
    
    def install_later():
        result["install"] = False
        dialog.destroy()
    
    btn_frame = ttk.Frame(frame)
    btn_frame.pack()
    
    install_btn = ttk.Button(btn_frame, text=_("install_now"), command=install_now)
    install_btn.pack(side="left", padx=(0, 10))
    
    later_btn = ttk.Button(btn_frame, text=_("install_later"), command=install_later)
    later_btn.pack(side="left", padx=(10, 0))
    
    # File location info
    location_label = ttk.Label(frame, text=_("update_location").format(file_path), 
                               wraplength=400, font=(None, 8, "italic"))
    location_label.pack(pady=(20, 0))
    
    dialog.wait_window()
    return result["install"]

def check_for_updates(current_version: str, parent_window=None):
    """Check GitHub for the latest release version.

    Compares the current version against the latest GitHub release.
    Shows a messagebox with results if parent_window is provided.

    Args:
        current_version: The current app version string (e.g., "v1.0.0")
        parent_window: Optional Tkinter window for messagebox parent

    Returns:
        dict: {'has_update': bool, 'latest_version': str or None, 'error': str or None}
    """
    _ = localization.get_text
    try:
        with urllib.request.urlopen(GITHUB_API_URL, timeout=5) as response:
            data = json.loads(response.read().decode())
            latest_tag = data.get("tag_name", "")
            latest_version = latest_tag.lstrip("v")
            current = current_version.lstrip("v")

            has_update = _compare_versions(current, latest_version) < 0

            result = {
                "has_update": has_update,
                "latest_version": latest_tag,
                "current_version": current_version,
                "error": None,
            }

            if parent_window:
                if has_update:
                    _show_update_dialog(current_version, latest_tag, parent_window)
                else:
                    messagebox.showinfo(
                        _("up_to_date"),
                        _("up_to_date_message").format(current_version),
                        parent=parent_window.root if parent_window else None
                    )

            return result

    except urllib.error.HTTPError as e:
        if e.code == 404:
            # No releases published yet
            result = {
                "has_update": False,
                "latest_version": None,
                "error": "No releases published yet",
            }
            if parent_window:
                messagebox.showinfo(
                    _("no_updates_available"),
                    _("no_releases_published").format(current_version),
                )
        else:
            result = {
                "has_update": False,
                "latest_version": None,
                "error": f"HTTP error {e.code}: {e.reason}",
            }
            if parent_window:
                messagebox.showwarning(
                    _("update_check_failed"),
                    _("update_check_http_error").format(e.code, e.reason),
                )
        return result
    except urllib.error.URLError as e:
        result = {
            "has_update": False,
            "latest_version": None,
            "error": f"Network error: {e}",
        }
        if parent_window:
            messagebox.showwarning(
                _("update_check_failed"),
                _("update_check_network_error").format(e),
            )
        return result
    except Exception as e:
        result = {
            "has_update": False,
            "latest_version": None,
            "error": str(e),
        }
        if parent_window:
            messagebox.showerror(
                _("update_check_error"),
                _("update_check_exception").format(e),
            )
        return result

def _compare_versions(v1: str, v2: str) -> int:
    """Compare two semantic version strings.

    Args:
        v1: First version (e.g., "1.0.0")
        v2: Second version (e.g., "1.0.1")

    Returns:
        -1 if v1 < v2, 0 if equal, 1 if v1 > v2
    """
    parts1 = [int(x) for x in v1.split(".")[:3]]
    parts2 = [int(x) for x in v2.split(".")[:3]]

    # Pad with zeros if needed
    while len(parts1) < 3:
        parts1.append(0)
    while len(parts2) < 3:
        parts2.append(0)

    if parts1 < parts2:
        return -1
    elif parts1 > parts2:
        return 1
    else:
        return 0

def _show_update_dialog(current_version, latest_version, app=None):
    """Show dialog informing user about available update with download option.
    
    Args:
        current_version: The current version of the application
        latest_version: The latest version available
        app: Optional parent application instance for theming
    """
    _ = localization.get_text
    
    # Create themed dialog
    dialog = tk.Toplevel()
    dialog.title(_("update_available"))
    dialog.resizable(False, False)
    dialog.transient(app.root if app else None)
    dialog.grab_set()
    
    # Apply theme
    if app and hasattr(app, 'theme_data'):
        bg = app.theme_data.get("bg", "#f0f0f0")
        fg = app.theme_data.get("fg", "#000000")
        dialog.configure(bg=bg)
    else:
        bg = "#f0f0f0"
        fg = "#000000"
    
    # Center dialog
    dialog.update_idletasks()
    width = 450
    height = 220
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    # Content frame
    frame = ttk.Frame(dialog, padding=20)
    frame.pack(fill="both", expand=True)
    
    # Update message
    update_msg = _("update_message").format(current_version, latest_version)
    msg_label = ttk.Label(frame, text=update_msg, wraplength=400, justify="center")
    msg_label.pack(pady=(0, 20))
    
    # Button handlers
    def download_update_handler():
        dialog.destroy()
        
        # Get release info
        release_data = get_latest_release_info()
        if not release_data:
            messagebox.showerror(
                _("error"),
                _("failed_to_fetch_release"),
                parent=app.root if app else None
            )
            return
        
        # Find downloadable asset
        assets = release_data.get("assets", [])
        download_url = None
        
        # Prefer .exe for Windows
        for asset in assets:
            name = asset.get("name", "").lower()
            if name.endswith(".exe"):
                download_url = asset.get("browser_download_url")
                break
        
        # Fallback to first asset
        if not download_url and assets:
            download_url = assets[0].get("browser_download_url")
        
        if not download_url:
            messagebox.showerror(
                _("error"),
                _("no_download_available"),
                parent=app.root if app else None
            )
            return
        
        # Download the update
        file_path = download_update(download_url, app)
        
        if file_path:
            # Show install prompt
            if show_install_prompt(file_path, app):
                # User chose to install now - open file location
                os.startfile(os.path.dirname(file_path))
                messagebox.showinfo(
                    _("install_update"),
                    _("please_run_installer"),
                    parent=app.root if app else None
                )
            else:
                # User chose to install later
                messagebox.showinfo(
                    _("install_later"),
                    _("update_saved_message").format(file_path),
                    parent=app.root if app else None
                )
    
    def view_release_handler():
        dialog.destroy()
        open_github_page()
    
    def later_handler():
        dialog.destroy()
    
    # Buttons
    btn_frame = ttk.Frame(frame)
    btn_frame.pack()
    
    download_btn = ttk.Button(btn_frame, text=_("download_update"), 
                             command=download_update_handler)
    download_btn.pack(side="left", padx=(0, 10))
    
    view_btn = ttk.Button(btn_frame, text=_("view_release"), 
                         command=view_release_handler)
    view_btn.pack(side="left", padx=(10, 10))
    
    later_btn = ttk.Button(btn_frame, text=_("later"), 
                          command=later_handler)
    later_btn.pack(side="left", padx=(10, 0))
    
    dialog.wait_window()

def open_github_page():
    """Open the project's GitHub page in the default browser."""
    _ = localization.get_text
    import webbrowser
    url = f"https://github.com/{GITHUB_REPO}"
    try:
        webbrowser.open(url)
    except Exception as e:
        messagebox.showerror(
            _("error_title"),
            _("browser_open_error").format(e),
        )
