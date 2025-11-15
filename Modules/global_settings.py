"""
Global settings module for WoW Cleanup Tool.

Handles system-wide settings stored in a shared location accessible to all users.
On Windows: C:\\ProgramData\\WoWCleanupTool\\
On Unix-like: /etc/wow-cleanup-tool/ or /opt/wow-cleanup-tool/
"""

import os
import json
import platform

def get_global_settings_path():
    """Return path to global settings directory, creating it if needed.

    Uses platform-specific locations:
    - Windows: C:\\ProgramData\\WoWCleanupTool\\
    - Unix/Linux: /etc/wow-cleanup-tool/ (requires permissions)

    Returns:
        str: Path to global settings directory
    """
    osname = platform.system()

    if osname == "Windows":
        # Use ProgramData on Windows
        base = os.environ.get("ProgramData", "C:\\ProgramData")
        config_dir = os.path.join(base, "WoWCleanupTool")
    else:
        # Use /etc on Unix-like systems
        config_dir = "/etc/wow-cleanup-tool"

    # Try to create directory with appropriate permissions
    try:
        os.makedirs(config_dir, exist_ok=True)
    except PermissionError:
        # If we can't create in system location, fall back to user home
        home = os.path.expanduser("~")
        config_dir = os.path.join(home, ".wow_cleanup_tool_global")
        os.makedirs(config_dir, exist_ok=True)

    return config_dir

def get_global_settings_file():
    """Return full path to global settings JSON file."""
    config_dir = get_global_settings_path()
    return os.path.join(config_dir, "global_settings.json")

def load_global_settings():
    """Load global settings from disk.

    Returns:
        dict: Global settings dict, or empty dict if file doesn't exist or on error
    """
    settings_file = get_global_settings_file()
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_global_settings(settings):
    """Save global settings to disk.

    Args:
        settings: dict of global settings to save

    Returns:
        bool: True if successful, False on error
    """
    try:
        settings_file = get_global_settings_file()
        # Ensure directory exists
        os.makedirs(os.path.dirname(settings_file), exist_ok=True)
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception:
        return False

def get_global_setting(key, default=None):
    """Get a single global setting value.

    Args:
        key: Setting key to retrieve
        default: Default value if key doesn't exist

    Returns:
        Setting value or default
    """
    settings = load_global_settings()
    return settings.get(key, default)

def set_global_setting(key, value):
    """Set a single global setting value and persist to disk.

    Args:
        key: Setting key to set
        value: Value to set

    Returns:
        bool: True if successful, False on error
    """
    settings = load_global_settings()
    settings[key] = value
    return save_global_settings(settings)
