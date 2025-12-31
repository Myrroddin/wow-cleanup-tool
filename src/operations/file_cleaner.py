"""
FileCleaner: Scans for .bak and .old files in WoW directories.
Uses BaseScanner for optimized parallel scanning with os.scandir.

Last Updated: December 30, 2025
- Refactored to inherit from BaseScanner for parallel processing
- Replaced os.walk with os.scandir for 2-3x performance improvement
- Supports multi-threaded scanning across WoW versions
- Uses efficient directory filtering during traversal
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
    """Scans for .bak and .old files recursively.

    December 30, 2025: Refactored to use BaseScanner's optimized
    parallel scanning infrastructure with os.scandir.
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
            max_workers: Parallel workers for BaseScanner
            logger: Optional logger
            loc: Optional localization instance
            skip_dirs: Optional set of directory names (case-insensitive) to skip
        """
        super().__init__(max_workers=max_workers, logger=logger, loc=loc)
        # December 30, 2025: Allow customization; default covers known irrelevant dirs
        self.skip_dirs: Set[str] = {d.lower() for d in (skip_dirs or DEFAULT_SKIP_DIRS)}

    def _scan_version(self, version_path: str) -> List[str]:
        """Scan a WoW version directory for .bak/.old files recursively.

        Args:
            version_path: Path to WoW version (e.g., C:\\WoW\\_retail_)

        Returns:
            List of .bak/.old file paths
        """

        # December 30, 2025: Define filter for backup/old files
        # This inline function is passed to BaseScanner's recursive scanner
        def is_backup_file(entry: os.DirEntry) -> bool:
            """Filter for .bak and .old files (case-insensitive)."""
            name_lower = entry.name.lower()
            return name_lower.endswith(".bak") or name_lower.endswith(".old")

        # December 30, 2025: Use BaseScanner's optimized os.scandir traversal
        # Avoids creating unnecessary file lists in memory and skips irrelevant dirs
        results = self._scan_directory_recursive(
            version_path, is_backup_file, skip_dirs=self.skip_dirs
        )

        return results

    def delete_files(self, file_paths: List[str]) -> int:
        """Delete files in the provided list."""
        deleted = 0
        for path in file_paths:
            try:
                os.remove(path)
                deleted += 1
                if self.logger:
                    self.logger.verbose(f"Deleted: {path}")
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Failed to delete {path}: {e}")
        return deleted
