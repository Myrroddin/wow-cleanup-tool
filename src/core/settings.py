"""
Settings management for WoW Cleanup Tool.

Handles loading, saving, and managing user preferences and application state.
- User settings (theme, font, geometry, etc.) are stored per-user in home directory
- WoW path is cached machine-wide in a shared location that doesn't require admin rights
"""

import json
import locale
import os
from pathlib import Path
import sys
from typing import Optional, Dict, Any


def get_system_language() -> str:
    """Get the system's default language code.
    
    Returns:
        str: Two-letter language code (e.g., 'en', 'de', 'fr'), defaults to 'en'
    """
    try:
        # Get system locale (newer method for Python 3.11+)
        if hasattr(locale, 'getlocale'):
            lang, encoding = locale.getlocale()
            if lang:
                # Extract language code (e.g., 'en_US' -> 'en')
                return lang.split('_')[0].lower()
    except:
        pass
    
    # Fallback to English
    return 'en'


def get_settings_file() -> Path:
    """Get the path to the user settings file.
    
    Returns:
        Path: Path to settings.json in user's home directory
    """
    return Path.home() / ".wow_cleanup_tool" / "settings.json"


def get_user_log_file() -> Path:
    """Get the path to the persistent user log file.
    
    Returns:
        Path: Path to user_log.txt in user's home directory
    """
    return Path.home() / ".wow_cleanup_tool" / "user_log.txt"


def get_wow_path_cache_file() -> Optional[Path]:
    """Get the path to the cached WoW installation path file.
    
    The WoW path is the same for all users on the system, so we cache it
    in a shared location. On Windows, we use a subdirectory under the WoW
    installation itself (since users have read access there). This avoids
    needing admin rights to ProgramData.
    
    Returns:
        Path or None: Path to cache file, or None if not yet determined
    """
    if sys.platform == 'win32':
        # Try common WoW locations for cache file
        cache_locations = [
            Path(r"C:\Program Files (x86)\World of Warcraft"),
            Path(r"C:\Program Files\World of Warcraft"),
            Path(r"D:\World of Warcraft"),
            Path(r"E:\World of Warcraft"),
        ]
        
        for location in cache_locations:
            if location.exists():
                cache_file = location / ".wow_cleanup_cache.json"
                # Check if we can write to this location
                try:
                    if cache_file.exists() or os.access(location, os.W_OK):
                        return cache_file
                except (OSError, PermissionError):
                    continue
    
    # Fallback: use user directory (per-user cache)
    return Path.home() / ".wow_cleanup_tool" / "wow_path_cache.json"


def load_wow_path_cache() -> Optional[str]:
    """Load cached WoW installation path.
    
    Returns:
        str or None: Cached WoW path, or None if not cached
    """
    cache_file = get_wow_path_cache_file()
    if not cache_file or not cache_file.exists():
        return None
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('wow_path')
    except Exception:
        return None


def save_wow_path_cache(wow_path: str) -> bool:
    """Save WoW installation path to cache.
    
    Args:
        wow_path: WoW installation path to cache
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    # Determine cache file location based on the WoW path
    if wow_path:
        wow_path_obj = Path(wow_path)
        cache_file = wow_path_obj / ".wow_cleanup_cache.json"
        
        # Check if we can write to the WoW directory
        try:
            if not cache_file.exists() and not os.access(wow_path_obj, os.W_OK):
                # Can't write to WoW directory, use fallback
                cache_file = Path.home() / ".wow_cleanup_tool" / "wow_path_cache.json"
        except (OSError, PermissionError):
            # Use fallback
            cache_file = Path.home() / ".wow_cleanup_tool" / "wow_path_cache.json"
    else:
        return False
    
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({'wow_path': wow_path}, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False



def load_settings() -> Dict[str, Any]:
    """Load user settings from disk and merge with cached WoW path.
    
    Returns:
        dict: Combined settings dictionary (user + cached WoW path)
    """
    settings_file = get_settings_file()
    defaults: Dict[str, Any] = {
        "language": get_system_language(),  # Default to OS language, fallback to 'en'
        "theme": "light",
        "font_family": "TkDefaultFont",
        "font_size": 9,
        "delete_mode": "trash",  # 'trash' or 'permanent'
        "verbose_logging": True,  # Show detailed operation messages (file deletions, config edits, etc.)
        "append_log": False,  # Append to user log across sessions instead of clearing
    }
    
    # Load user settings
    user_settings: Dict[str, Any] = defaults.copy()
    if settings_file.exists():
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                user_settings = {**defaults, **loaded}
        except Exception:
            pass
    
    # Load cached WoW path
    cached_wow_path = load_wow_path_cache()
    if cached_wow_path:
        user_settings['wow_path'] = cached_wow_path
    
    return user_settings


def save_settings(settings: Dict[str, Any]) -> bool:
    """Save settings to disk, separating user settings from WoW path cache.
    
    Args:
        settings: Dictionary of all settings to save
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    # Split settings: WoW path goes to cache, everything else to user settings
    wow_path = settings.get('wow_path')
    user_settings = {k: v for k, v in settings.items() if k != 'wow_path'}
    
    # Save user settings
    settings_file = get_settings_file()
    user_success = False
    try:
        settings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(user_settings, f, indent=2, ensure_ascii=False)
        user_success = True
    except Exception:
        pass
    
    # Save WoW path to cache if present
    cache_success = True
    if wow_path:
        cache_success = save_wow_path_cache(wow_path)
    
    return user_success and cache_success


def save_user_log(log_content: str) -> bool:
    """Save user log to disk.
    
    Args:
        log_content: String content of the user log
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    log_file = get_user_log_file()
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(log_content)
        return True
    except Exception:
        return False


def load_user_log() -> Optional[str]:
    """Load user log from disk.
    
    Returns:
        str or None: Log content, or None if not found or error
    """
    log_file = get_user_log_file()
    if not log_file.exists():
        return None
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None
