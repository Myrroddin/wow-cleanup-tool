"""
OrphanScanner: Scans for orphaned SavedVariables files in WoW installation folders.
"""
from typing import List
from src.operations.base_scanner import BaseScanner
import os

class OrphanScanner(BaseScanner):
    """Scan for orphaned SavedVariables files."""
    def _scan_version(self, version_path: str) -> List[str]:
        # Placeholder for orphan scan logic
        # 1. Scan Interface/AddOns for installed addons
        # 2. Scan WTF/Account/** for SavedVariables files
        # 3. Find .lua files for uninstalled addons
        # 4. Ignore Blizzard_* core files
        return []
