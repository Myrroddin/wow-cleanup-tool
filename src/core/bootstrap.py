"""Dependency bootstrapper for WoW Cleanup Tool."""

from core.dependencies import check_and_install_dependencies
import sys


def ensure_dependencies():
    if not check_and_install_dependencies():
        sys.exit(1)
