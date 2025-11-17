"""Common utilities for WoW version handling.

Provides caching and shared utilities for version enumeration and path handling.
"""
import os
import time
from pathlib import Path
from Modules import localization

# Cache for version enumeration
_VERSION_CACHE = {}
_CACHE_TTL = 60  # seconds

def enumerate_versions_cached(base_path, ttl_seconds=60):
    """Enumerate WoW versions with caching.
    
    Args:
        base_path: Base WoW installation directory
        ttl_seconds: Cache time-to-live in seconds
        
    Returns:
        list: List of (version_path, version_label) tuples
    """
    global _VERSION_CACHE, _CACHE_TTL
    
    cache_key = base_path
    current_time = time.time()
    
    # Check cache
    if cache_key in _VERSION_CACHE:
        cached_time, cached_data = _VERSION_CACHE[cache_key]
        if current_time - cached_time < ttl_seconds:
            return cached_data
    
    # Enumerate versions
    versions = []
    version_folders = [
        ("_classic_era_", "version_classic_era"),
        ("_classic_", "version_classic"),
        ("_retail_", "version_retail"),
    ]
    variant_suffixes = [
        ("_ptr_", "version_ptr"),
        ("_beta_", "version_beta"),
    ]
    
    try:
        with os.scandir(base_path) as entries:
            existing_dirs = {entry.name for entry in entries if entry.is_dir(follow_symlinks=False)}
        
        for folder, label_key in version_folders:
            if folder in existing_dirs:
                vpath = os.path.join(base_path, folder)
                versions.append((vpath, localization._(label_key)))
            for suf, suffix_key in variant_suffixes:
                variant_folder = folder[:-1] + suf[1:]
                if variant_folder in existing_dirs:
                    v2 = os.path.join(base_path, variant_folder)
                    versions.append((v2, localization._(label_key) + " " + localization._(suffix_key)))
    except (OSError, PermissionError):
        pass
    
    # Update cache
    _VERSION_CACHE[cache_key] = (current_time, versions)
    
    return versions

def clear_version_cache():
    """Clear the version enumeration cache."""
    global _VERSION_CACHE
    _VERSION_CACHE.clear()

def get_version_config_path(version_path):
    """Get Config.wtf path for a version.
    
    Args:
        version_path: Path to WoW version folder
        
    Returns:
        str: Path to Config.wtf
    """
    return os.path.join(version_path, "WTF", "Config.wtf")

def get_version_wtf_path(version_path):
    """Get WTF directory path for a version.
    
    Args:
        version_path: Path to WoW version folder
        
    Returns:
        str: Path to WTF directory
    """
    return os.path.join(version_path, "WTF")

def get_version_interface_path(version_path):
    """Get Interface directory path for a version.
    
    Args:
        version_path: Path to WoW version folder
        
    Returns:
        str: Path to Interface directory
    """
    return os.path.join(version_path, "Interface")

def get_version_addons_path(version_path):
    """Get AddOns directory path for a version.
    
    Args:
        version_path: Path to WoW version folder
        
    Returns:
        str: Path to AddOns directory
    """
    return os.path.join(version_path, "Interface", "AddOns")

def verify_version_structure(version_path):
    """Verify a version has required directories.
    
    Args:
        version_path: Path to WoW version folder
        
    Returns:
        bool: True if WTF and Interface/AddOns exist
    """
    wtf_dir = get_version_wtf_path(version_path)
    interface_dir = get_version_interface_path(version_path)
    addons_dir = get_version_addons_path(version_path)
    
    return (os.path.exists(wtf_dir) and 
            os.path.exists(interface_dir) and 
            os.path.exists(addons_dir))

def get_folder_size(folder_path):
    """Calculate total size of a folder in bytes.
    
    Args:
        folder_path: Path to folder
        
    Returns:
        int: Total size in bytes
    """
    total_size = 0
    try:
        with os.scandir(folder_path) as entries:
            for entry in entries:
                try:
                    if entry.is_file(follow_symlinks=False):
                        total_size += entry.stat().st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total_size += get_folder_size(entry.path)
                except (OSError, PermissionError):
                    continue
    except (OSError, PermissionError):
        pass
    
    return total_size

def get_folder_sizes_parallel(folder_paths):
    """Calculate sizes of multiple folders in parallel.
    
    Args:
        folder_paths: Iterable of folder paths
        
    Returns:
        dict: Mapping of folder_path -> size_in_bytes
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(get_folder_size, path): path for path in folder_paths}
        
        for future in as_completed(futures):
            path = futures[future]
            try:
                size = future.result()
                results[path] = size
            except Exception:
                results[path] = 0
    
    return results
