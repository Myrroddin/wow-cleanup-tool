"""
WoW Cleanup Tool - Operations Module

This module contains all file/folder cleanup operations.

December 30, 2025: Updated with implemented scanners.

Current modules:
- base_scanner.py: Base class for all scanners with parallel processing
- file_cleaner.py: Scan for .bak/.old files (implemented)
- orphan_scanner.py: Scan for orphaned SavedVariables (implemented)
- file_operations.py: Delete/move operations with trash support

Future modules (see IMPLEMENTATION_ROADMAP.md):
- folder_scanner.py: Scan for cleanable folders (Logs, Errors, etc.)

All modules use os.scandir() for performance and support
multithreading for parallel operations across WoW versions.
"""

from .base_scanner import BaseScanner
from .file_cleaner import FileCleaner
from .file_operations import delete_files_batch
from .orphan_scanner import OrphanScanner

__all__ = [
    "BaseScanner",
    "FileCleaner",
    "OrphanScanner",
    "delete_files_batch",
]
