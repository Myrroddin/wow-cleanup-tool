"""
FolderScanner: Scans for cleanable folders (Logs, Errors, Cache, Screenshots) in WoW installation folders.
"""
from typing import List, Set
from src.operations.base_scanner import BaseScanner
import os

class FolderScanner(BaseScanner):
    """Scan for cleanable folders."""
    CLEANABLE_FOLDERS: Set[str] = {
        "Logs", "Errors", "Cache", "Screenshots"
    }

    def _scan_version(self, version_path: str) -> List[str]:
        """Scan for cleanable folders in version."""
        results = []
        try:
            with os.scandir(version_path) as entries:
                for entry in entries:
                    if entry.is_dir() and entry.name in self.CLEANABLE_FOLDERS:
                        if self._has_populated_directory(entry.path):
                            results.append(entry.path)
        except (OSError, PermissionError):
            pass
        return results
