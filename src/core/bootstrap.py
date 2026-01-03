"""Dependency bootstrapper for WoW Cleanup Tool.

Ensures required Python packages are installed before the application starts.
If dependencies are missing, attempts to install them automatically.
"""

from core.dependencies import check_and_install_dependencies
import sys


def ensure_dependencies():
    """Check for required dependencies and install if missing.

    Returns:
        bool: True if dependencies are satisfied, False otherwise

    The application will exit with code 1 if dependencies cannot be installed.
    This prevents crashes from missing imports later in the application.
    """
    if not check_and_install_dependencies():
        sys.exit(1)
