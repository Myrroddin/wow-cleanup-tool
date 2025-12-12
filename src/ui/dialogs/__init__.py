"""Dialog modules for WoW Cleanup Tool."""

from .wow_close_warning import show_wow_close_warning
from .license_dialog import show_license_dialog
from .multiple_installations import show_multiple_installations_dialog

__all__ = [
    "show_wow_close_warning",
    "show_license_dialog",
    "show_multiple_installations_dialog",
]
