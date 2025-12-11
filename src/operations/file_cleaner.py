"""
FileCleaner: Scans for .bak and .old files in WoW directories.
Template implementation for testing and integration.
"""
import os
import re
from typing import List

class FileCleaner:
    BAK_OLD_PATTERN = re.compile(r'\.(bak|old)$', re.IGNORECASE)

    def __init__(self, max_workers: int = 2, logger=None):
        self.max_workers = max_workers
        self.logger = logger

    def _scan_version(self, version_path: str):
        """Scan a version directory for .bak/.old files recursively."""
        results = self.scan_directory(version_path)
        return results

    def scan_all_flavors(self, root_path: str, path_manager=None):
        """Scan all detected flavor directories for .bak/.old files."""
        results = {}
        if path_manager is not None:
            flavors = path_manager.detect_flavors(root_path)
            for flavor_dir in flavors:
                flavor_path = os.path.join(root_path, flavor_dir)
                files = self._scan_version(flavor_path)
                results[flavor_dir] = files
        else:
        return results

    def scan_directory(self, root_path: str) -> List[str]:
        """Recursively scan for .bak/.old files."""
        results = []
        for dirpath, _, filenames in os.walk(root_path):
            for filename in filenames:
                if self.BAK_OLD_PATTERN.search(filename):
                    full_path = os.path.join(dirpath, filename)
                    results.append(full_path)
                    if self.logger:
                        self.logger.verbose(f"Found: {full_path}")
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
