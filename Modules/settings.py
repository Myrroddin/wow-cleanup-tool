import os
import json
from Modules import global_settings

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
    """Load and return settings dict, merging global + user settings.

    Global settings (wow_path, check_for_updates, verbose_logging, delete_mode) take precedence over user settings.
    Returns empty dict on error.
    """
    user_settings = {}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                user_settings = json.load(f)
        except Exception:
            pass

    # Load global settings and merge
    # Global settings override user settings for shared keys
    global_opts = global_settings.load_global_settings()
    if "wow_path" in global_opts:
        # wow_path is global; don't let user override it
        user_settings["wow_path"] = global_opts["wow_path"]
    if "check_for_updates" in global_opts:
        # check_for_updates is global; don't let user override it
        user_settings["check_for_updates"] = global_opts["check_for_updates"]
    if "verbose_logging" in global_opts:
        # verbose_logging is global; don't let user override it
        user_settings["verbose_logging"] = global_opts["verbose_logging"]
    if "delete_mode" in global_opts:
        # delete_mode is global; don't let user override it
        user_settings["delete_mode"] = global_opts["delete_mode"]

    return user_settings

def save_settings(settings):
    """Save settings dict to disk; silently ignore write errors.

    Special handling: wow_path, check_for_updates, verbose_logging, and delete_mode are saved to global settings.
    """
    try:
        # Extract global settings if present and save them globally
        global_to_save = {}
        if "wow_path" in settings:
            global_to_save["wow_path"] = settings.pop("wow_path")
        if "check_for_updates" in settings:
            global_to_save["check_for_updates"] = settings.pop("check_for_updates")
        if "verbose_logging" in settings:
            global_to_save["verbose_logging"] = settings.pop("verbose_logging")
        if "delete_mode" in settings:
            global_to_save["delete_mode"] = settings.pop("delete_mode")

        # Save global settings
        if global_to_save:
            current_global = global_settings.load_global_settings()
            current_global.update(global_to_save)
            global_settings.save_global_settings(current_global)

        # Save remaining user settings
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
    except Exception:
        pass
