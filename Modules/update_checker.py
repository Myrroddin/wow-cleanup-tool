"""
Update checker module for WoW Cleanup Tool.

Handles checking for new releases on GitHub.
"""

import urllib.request
import urllib.error
import json
from tkinter import messagebox

GITHUB_REPO = "Myrroddin/wow-cleanup-tool"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

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
                _show_update_dialog(has_update, current_version, latest_tag)

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
                    "No Updates Available",
                    f"You are running {current_version}.\n\nNo releases have been published yet.",
                )
        else:
            result = {
                "has_update": False,
                "latest_version": None,
                "error": f"HTTP error {e.code}: {e.reason}",
            }
            if parent_window:
                messagebox.showwarning(
                    "Update Check Failed",
                    f"Could not check for updates:\n\nHTTP {e.code}: {e.reason}",
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
                "Update Check Failed",
                f"Could not check for updates:\n\n{e}",
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
                "Update Check Error",
                f"An error occurred while checking for updates:\n\n{e}",
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

def _show_update_dialog(has_update: bool, current: str, latest: str):
    """Show appropriate messagebox based on update availability.

    Args:
        has_update: Whether an update is available
        current: Current version string
        latest: Latest version string
    """
    if has_update:
        messagebox.showinfo(
            "Update Available",
            f"A new version is available!\n\n"
            f"Current: {current}\n"
            f"Latest: {latest}\n\n"
            f"Visit the GitHub page to download the latest version.",
        )
    else:
        messagebox.showinfo(
            "Up to Date",
            f"You are running the latest version ({current}).",
        )

def open_github_page():
    """Open the project's GitHub page in the default browser."""
    import webbrowser
    url = f"https://github.com/{GITHUB_REPO}"
    try:
        webbrowser.open(url)
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not open browser:\n\n{e}",
        )
