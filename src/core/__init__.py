"""Core application infrastructure modules."""

from .dependencies import DependencyManager, check_and_install_dependencies
from .logger import Logger
from .settings import (
    load_settings,
    save_settings,
    get_settings_file,
    load_wow_path_cache,
    save_wow_path_cache,
    get_wow_path_cache_file,
)
from .single_instance import SingleInstance
from .themes import apply_theme, THEMES

__all__ = [
    "DependencyManager",
    "check_and_install_dependencies",
    "Logger",
    "load_settings",
    "save_settings",
    "get_settings_file",
    "load_wow_path_cache",
    "save_wow_path_cache",
    "get_wow_path_cache_file",
    "SingleInstance",
    "apply_theme",
    "THEMES",
]
