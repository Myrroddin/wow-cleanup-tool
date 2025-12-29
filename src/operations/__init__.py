"""
WoW Cleanup Tool - Operations Module

This module contains all file/folder cleanup operations.
Current modules:
- base_scanner.py: Base class for all scanners with parallel processing

Future modules (see IMPLEMENTATION_ROADMAP.md):
- folder_scanner.py: Scan for cleanable folders (Logs, Errors, etc.)
- orphan_scanner.py: Scan for orphaned SavedVariables
- file_scanner.py: Scan for .bak/.old files
- file_operations.py: Delete/move operations with trash support

All modules use os.scandir() for performance and support
multithreading for parallel operations across WoW versions.
"""

from .base_scanner import BaseScanner
from .file_operations import delete_files_batch

__all__ = [
    "BaseScanner",
    "delete_files_batch",
]
