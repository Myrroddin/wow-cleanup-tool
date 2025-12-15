# Operations Module

This module contains all file system operations for WoW cleanup functionality.

## Design Philosophy

- **Modular**: Each operation type has its own scanner
- **Optimized**: Uses `os.scandir()` for 2-3x faster directory traversal
- **Parallel**: ThreadPoolExecutor for concurrent scanning across WoW versions
- **Adaptive**: Disk type detection adjusts parallelism for HDD vs SSD
- **Safe**: Comprehensive error handling, permission checks, and trash support


## Structure

### Base Classes
- `base_scanner.py`: Common scanning functionality for all operations

### Utilities
- `disk_utils.py`: Disk type detection and performance optimization

### Current Infrastructure
- Logging and settings infrastructure supports chat timestamps (user and developer logs)
- Localization system with 98+ keys, tooltips, and robust English support

### Future Scanners (to be implemented)
- `file_scanner.py`: Scan for .bak and .old files
- `folder_scanner.py`: Scan for cleanable folders (Logs, Errors, etc.)
- `orphan_scanner.py`: Scan for orphaned SavedVariables

### Future Operations (to be implemented)
- `file_operations.py`: Delete/move files with trash support and batch operations

## Performance Optimizations

### 1. os.scandir() Instead of os.listdir()
```python
# Slow (loads entire directory into memory)
for name in os.listdir(path):
    full_path = os.path.join(path, name)
    if os.path.isfile(full_path):
        # ...

# Fast (iterator, minimal memory, single syscall per entry)
with os.scandir(path) as entries:
    for entry in entries:
        if entry.is_file():
            # entry.path already has full path
```

### 2. Parallel Scanning
```python
# Sequential (slow)
for version_path, label in versions:
    results[label] = scan_version(version_path)

# Parallel (fast for multiple versions)
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(scan_version, vpath): label 
               for vpath, label in versions}
```

### 3. Disk-Aware Threading
```python
# Auto-tune based on disk type
workers = get_optimal_workers(wow_path)
# SSD: 8 workers
# HDD: 2 workers (seeking kills parallelism benefit)
```

### 4. Compiled Regex Patterns
```python
# Module level - compiled once
BAK_OLD_PATTERN = re.compile(r'\.(bak|old)$', re.IGNORECASE)

# In scan loop - no recompilation overhead
if BAK_OLD_PATTERN.search(filename):
    # ...
```

## Usage Pattern (Future)

```python
from operations import FileScanner, get_optimal_workers

# Create scanner with disk-optimized threading and logger
wow_path = "C:\\World of Warcraft"
workers = get_optimal_workers(wow_path)
scanner = FileScanner(max_workers=workers, logger=logger, loc=loc)

# Scan with progress tracking
def on_progress(current, total, label):
    print(f"Scanning {label}: {current}/{total}")

versions = [
    ("C:\\World of Warcraft\\_retail_", "Retail"),
    ("C:\\World of Warcraft\\_classic_", "Classic"),
]

results = scanner.scan_versions(versions, progress_callback=on_progress)
# Returns: {'Retail': [list of .bak/.old files], 'Classic': [...]}

# Logger usage in scanners:
# - logger.log(): Essential user messages
# - logger.verbose(): Detailed operation messages (if verbose enabled)
# - logger.debug(): Technical details → Developer tab
# - logger.error(): Errors → Developer tab with error badge
```

## Thread Safety

All scanners are designed to be thread-safe:
- No shared mutable state during scanning
- Results collected via concurrent.futures
- UI updates scheduled via root.after() on main thread
- Exception handling prevents one version failure from affecting others

## Error Handling

Comprehensive error handling at multiple levels:
1. **File level**: Skip inaccessible files, continue scanning
2. **Directory level**: Skip permission-denied folders
3. **Version level**: Continue with other versions if one fails
4. **Executor level**: Fall back to single-threaded if parallel fails

from .file_scanner import FileScanner
from .folder_scanner import FolderScanner
from .orphan_scanner import OrphanScanner
from .file_operations import delete_files_batch
