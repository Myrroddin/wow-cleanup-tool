import os
import json

def get_settings_path():
    """Return path to settings.json in user's config directory.
    
    Creates the directory if it doesn't exist.
    """
    home = os.path.expanduser("~")
    cfg = os.path.join(home, ".wow_cleanup_tool")
    os.makedirs(cfg, exist_ok=True)
    return os.path.join(cfg, "settings.json")

SETTINGS_FILE = get_settings_path()

def load_settings():
    """Load and return settings dict, or empty dict on error."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings):
    """Save settings dict to disk; silently ignore write errors."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
    except Exception:
        pass
