"""Core application infrastructure modules."""

from .caching import timed_cache, SettingsCache
from .dependencies import DependencyManager, check_and_install_dependencies
from .logger import Logger
from .settings import (
    load_settings,
    save_settings,
    get_settings_file,
    invalidate_settings_cache,
)
from .single_instance import SingleInstance
from .themes import apply_theme, THEMES

__all__ = [
    "caching",
    "timed_cache",
    "SettingsCache",
    "DependencyManager",
    "check_and_install_dependencies",
    "Logger",
    "load_settings",
    "save_settings",
    "get_settings_file",
    "invalidate_settings_cache",
    "SingleInstance",
    "apply_theme",
    "THEMES",
]
