"""FileCleaner: Scans for backup and old files in WoW directories.

Identifies .bak and .old files that can be safely removed to free up disk space.
Uses BaseScanner for optimized parallel scanning with os.scandir, providing
2-3x faster performance than traditional os.walk approaches.

Features:
- Parallel scanning across multiple WoW game versions
- Efficient directory filtering to skip irrelevant folders
- Thread-safe operation for UI responsiveness

Note:
- FileCleaner handles DETECTION only, not deletion
- File deletion is performed by operations.file_operations.delete_files_batch()
- This separation allows delete_files_batch() to support send2trash integration
  and respect user delete mode preferences (trash vs permanent)
"""

import os
from typing import List, Optional, Set
from operations.base_scanner import BaseScanner


DEFAULT_SKIP_DIRS: Set[str] = {
    "cache",
    "screenshots",
    "data",
    "fonts",
    "logs",
    ".battle.net",
    "utils",
}


class FileCleaner(BaseScanner):
    """Scans for .bak and .old files recursively across WoW installations.

    Inherits from BaseScanner to leverage optimized parallel scanning
    infrastructure with os.scandir for better performance.
    """

    def __init__(
        self,
        max_workers: int = 8,
        logger: Optional[any] = None,
        loc: Optional[any] = None,
        skip_dirs: Optional[Set[str]] = None,
    ):
        """Initialize FileCleaner with optional skip directory set.

        Args:
            max_workers: Number of parallel workers for BaseScanner
            logger: Optional logger instance for operation logging
            loc: Optional localization instance for translated messages
            skip_dirs: Optional set of directory names (case-insensitive) to skip
                      during scanning. Defaults to common irrelevant directories.
        """
        super().__init__(max_workers=max_workers, logger=logger, loc=loc)
        # Allow customization; default covers known irrelevant directories
        self.skip_dirs: Set[str] = {d.lower() for d in (skip_dirs or DEFAULT_SKIP_DIRS)}

    def _scan_version(self, version_path: str) -> List[str]:
        """Scan a WoW version directory for .bak/.old files recursively.

        Args:
            version_path: Path to WoW version (e.g., C:\\WoW\\_retail_)

        Returns:
            List of .bak/.old file paths found in the version directory
        """

        # Define filter for backup/old files
        # This inline function is passed to BaseScanner's recursive scanner
        def is_backup_file(entry: os.DirEntry) -> bool:
            """Filter for .bak and .old files (case-insensitive)."""
            name_lower = entry.name.lower()
            return name_lower.endswith(".bak") or name_lower.endswith(".old")

        # Use BaseScanner's optimized os.scandir traversal
        # Avoids creating unnecessary file lists in memory and skips irrelevant directories
        results = self._scan_directory_recursive(
            version_path, is_backup_file, skip_dirs=self.skip_dirs
        )

        return results

    # NOTE: File deletion is handled by operations.file_operations.delete_files_batch()
    # which supports send2trash integration and respects user delete mode preferences.
    # FileCleaner is responsible only for scanning/detection, not deletion.
