"""
Disk utilities for optimization.
Provides disk type detection and performance tuning based on
whether the WoW installation is on HDD or SSD.
"""

import os
import sys


def detect_disk_type(path: str) -> str:
    """Detect if path is on HDD or SSD.

    Args:
        path: File system path to check

    Returns:
        'ssd', 'hdd', or 'unknown'
    """
    if sys.platform != "win32":
        return "unknown"

    try:
        import ctypes
        from ctypes import wintypes

        # Get the drive letter
        drive = os.path.splitdrive(os.path.abspath(path))[0]
        if not drive:
            return "unknown"

        # Ensure it ends with backslash
        if not drive.endswith("\\"):
            drive += "\\"

        # IOCTL_STORAGE_QUERY_PROPERTY definitions
        IOCTL_STORAGE_QUERY_PROPERTY = 0x002D1400
        PropertyStandardQuery = 0
        StorageDeviceSeekPenaltyProperty = 7

        # class STORAGE_PROPERTY_QUERY(ctypes.Structure):
        #     pass  # Define fields if needed
        # ...additional logic would go here...
        return "unknown"  # Placeholder until implemented
    except Exception:
        return "unknown"
