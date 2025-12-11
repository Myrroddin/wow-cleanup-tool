"""
FileScanner: Scans for .bak and .old files in WoW installation folders.
"""
import re
from typing import List
from src.operations.base_scanner import BaseScanner

class FileScanner(BaseScanner):
    """Scan for .bak and .old files."""
    BAK_OLD_PATTERN = re.compile(r'\.(bak|old)$', re.IGNORECASE)

    def _scan_version(self, version_path: str) -> List[str]:
        """Scan single WoW version for .bak/.old files."""
        return self._scan_directory_recursive(
            version_path,
            lambda entry: self.BAK_OLD_PATTERN.search(entry.name)
        )
