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
    if sys.platform != 'win32':
        return 'unknown'
    
    try:
        import ctypes
        from ctypes import wintypes
        
        # Get the drive letter
        drive = os.path.splitdrive(os.path.abspath(path))[0]
        if not drive:
            return 'unknown'
        
        # Ensure it ends with backslash
        if not drive.endswith('\\'):
            drive += '\\'
        
        # IOCTL_STORAGE_QUERY_PROPERTY definitions
        IOCTL_STORAGE_QUERY_PROPERTY = 0x002D1400
        PropertyStandardQuery = 0
        StorageDeviceSeekPenaltyProperty = 7
        
        class STORAGE_PROPERTY_QUERY(ctypes.Structure):
            _fields_ = [
                ('PropertyId', ctypes.c_int),
                ('QueryType', ctypes.c_int),
                ('AdditionalParameters', ctypes.c_byte * 1)
            ]
        
        class DEVICE_SEEK_PENALTY_DESCRIPTOR(ctypes.Structure):
            _fields_ = [
                ('Version', wintypes.DWORD),
                ('Size', wintypes.DWORD),
                ('IncursSeekPenalty', wintypes.BOOLEAN)
            ]
        
        # Open the drive
        drive_handle = ctypes.windll.kernel32.CreateFileW(
            f"\\\\.\\{drive[0]}:",
            0,  # No access to drive
            3,  # FILE_SHARE_READ | FILE_SHARE_WRITE
            None,
            3,  # OPEN_EXISTING
            0,
            None
        )
        
        if drive_handle == -1:
            return 'unknown'
        
        try:
            # Query seek penalty
            query = STORAGE_PROPERTY_QUERY()
            query.PropertyId = StorageDeviceSeekPenaltyProperty
            query.QueryType = PropertyStandardQuery
            
            result = DEVICE_SEEK_PENALTY_DESCRIPTOR()
            bytes_returned = wintypes.DWORD()
            
            success = ctypes.windll.kernel32.DeviceIoControl(
                drive_handle,
                IOCTL_STORAGE_QUERY_PROPERTY,
                ctypes.byref(query),
                ctypes.sizeof(query),
                ctypes.byref(result),
                ctypes.sizeof(result),
                ctypes.byref(bytes_returned),
                None
            )
            
            if success:
                # IncursSeekPenalty: True = HDD, False = SSD
                return 'hdd' if result.IncursSeekPenalty else 'ssd'
        finally:
            ctypes.windll.kernel32.CloseHandle(drive_handle)
            
    except Exception:
        pass
    
    return 'unknown'


def get_optimal_workers(path: str, default: int = 8) -> int:
    """Get optimal number of worker threads based on disk type.
    
    Args:
        path: Path to scan (used for disk type detection)
        default: Default workers if disk type unknown
        
    Returns:
        Optimal number of worker threads
    """
    disk_type = detect_disk_type(path)
    
    if disk_type == 'ssd':
        # SSDs handle parallelism well
        return 8
    elif disk_type == 'hdd':
        # HDDs benefit less from parallelism due to seek time
        return 2
    else:
        # Unknown - use conservative default
        return default


def is_nvme_drive(path: str) -> bool:
    """Check if path is on NVMe drive (even faster than SATA SSD).
    
    Args:
        path: File system path to check
        
    Returns:
        True if likely NVMe (very fast), False otherwise
    """
    # This is a simplified heuristic
    # NVMe drives typically show as SSD with very high performance
    # For now, just return False - can be enhanced with WMI queries
    return False
