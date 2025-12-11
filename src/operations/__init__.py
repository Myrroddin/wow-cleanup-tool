"""
WoW Cleanup Tool - Operations Module

This module contains all file/folder cleanup operations.
Current modules:
- base_scanner.py: Base class for all scanners with parallel processing
- disk_utils.py: Disk type detection and optimization

Future modules (see IMPLEMENTATION_ROADMAP.md):
- file_scanner.py: Scan for .bak/.old files
- folder_scanner.py: Scan for cleanable folders (Logs, Errors, etc.)
- orphan_scanner.py: Scan for orphaned SavedVariables
- file_operations.py: Delete/move operations with trash support

All modules use os.scandir() for performance and support
multithreading for parallel operations across WoW versions.
"""

from .base_scanner import BaseScanner
from .disk_utils import detect_disk_type, get_optimal_workers, is_nvme_drive
from .file_scanner import FileScanner
from .folder_scanner import FolderScanner
from .orphan_scanner import OrphanScanner
from .file_operations import delete_files_batch

__all__ = [
    'BaseScanner',
    'detect_disk_type',
    'get_optimal_workers',
    'is_nvme_drive',
    'FileScanner',
    'FolderScanner',
    'OrphanScanner',
    'delete_files_batch',
]
