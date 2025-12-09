# Implementation Roadmap for Cleanup Features

## Current Status ✅
  - User log: 1MB rotation, 1 backup (wow_cleanup_user.log)
  - Developer log: 5MB rotation, 2 backups (wow_cleanup_dev.log)
  - Custom TextWidgetHandler for Tkinter integration
  - SessionSeparatorHandler for append mode
  - Thread-safe logging with automatic rotation
  - Test framework: Python unittest
  - Tests for initialization, validation, detection, and helper functions
  - Mock objects for testing without filesystem dependencies
  - `btn_` prefix: Button labels (6 keys)
  - `label_` prefix: UI labels (8 keys)
  - `status_` prefix: Status messages (8 keys)
  - `msg_` prefix: Dialog messages (6 keys)
  - `version_` prefix: Version types (3 keys)
  - `option_` prefix: Checkbox/radio options (5 keys)
  - `title_` prefix: Window/dialog titles (7 keys)
  - `tab_` prefix: Tab names (6 keys)
  - `flavor_` prefix: WoW flavor display names (5 keys) ⭐ NEW
  - Additional prefixes: `dep_`, `error_`, `file_`, `log_`, `wow_`
  - All keys alphabetically sorted for easy maintenance
  - Logger class refactored (60 lines reduced, helper methods extracted, constant caching)
  - Font utilities caching (eliminates repeated system calls)
  - Removed unused imports (11 files cleaned up) ⭐ NEW

## Next Steps (When Ready)

### Phase 1: File Scanner (.bak/.old files)
**File**: `src/operations/file_scanner.py`

```python
import re
from typing import List
from modules.operations.base_scanner import BaseScanner

class FileScanner(BaseScanner):
    """Scan for .bak and .old files."""
    
    BAK_OLD_PATTERN = re.compile(r'\.(bak|old)$', re.IGNORECASE)
    
    def _scan_version(self, version_path: str) -> List[str]:
        """Scan single WoW version for .bak/.old files."""
        return self._scan_directory_recursive(
            version_path,
            lambda entry: self.BAK_OLD_PATTERN.search(entry.name)
        )
```

**Integration**:
1. Add to `src/operations/__init__.py`: `from .file_scanner import FileScanner`
2. Create UI tab in `src/ui/tabs/file_cleaner_tab.py`
3. Pass logger to scanner: `scanner = FileScanner(max_workers=workers, logger=self.logger, loc=loc)`
4. Add scan button that calls `FileScanner.scan_versions()`
5. Display results in SaplingCanvas widget (`src/ui/widgets/sapling_canvas.py`)
6. Use logger methods:
   - `logger.log()`: Essential messages ("Scan complete")
   - `logger.verbose()`: Detailed operations ("Deleted file: addon.bak")
   - `logger.debug()`: Technical details → Developer tab
   - `logger.error()`: Errors → Developer tab with 🔴 badge

### Phase 2: Folder Scanner (Logs, Errors, etc.)
**File**: `src/operations/folder_scanner.py`

```python
from typing import List, Set
from src.operations.base_scanner import BaseScanner

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
                        # Check if folder has content
                        if self._has_populated_directory(entry.path):
                            results.append(entry.path)
        except (OSError, PermissionError):
            pass
        return results
```

### Phase 3: Orphan Scanner (SavedVariables)
**File**: `src/operations/orphan_scanner.py`

More complex - needs to:
1. Scan `Interface/AddOns` for installed addons
2. Scan `WTF/Account/**` for SavedVariables files
3. Find .lua files for uninstalled addons
4. Ignore Blizzard_* core files

### Phase 4: File Operations
**File**: `src/operations/file_operations.py`

```python
from typing import List, Tuple
import os
from send2trash import send2trash

def delete_files_batch(
    paths: List[str], 
    delete_mode: str = 'trash',
    logger = None,
    loc = None
) -> Tuple[int, bool, bool]:
    """Delete or trash files/folders.
    
    Args:
        paths: List of file/folder paths to delete
        delete_mode: 'trash' or 'permanent'
        logger: Logger instance for verbose output
        loc: Localization instance
    
    Returns:
        (processed_count, permanently_deleted, used_trash)
    """
    processed = 0
    used_trash = False
    
    for path in paths:
        try:
            if delete_mode == 'trash':
                send2trash(path)
                used_trash = True
                if logger:
                    logger.verbose(f"Moved to trash: {path}")
            else:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                if logger:
                    logger.verbose(f"Deleted permanently: {path}")
            processed += 1
        except (OSError, IOError) as e:
            if logger:
                logger.error(f"Failed to delete {path}: {e}")
            continue
    
    return processed, not used_trash, used_trash
```

## Performance Guidelines

### Disk Type Optimization
```python
from src.operations.disk_utils import get_optimal_workers

# In scanner initialization
wow_path = "C:\World of Warcraft"
workers = get_optimal_workers(wow_path)
scanner = FileScanner(max_workers=workers, logger=self.logger)
# Auto: 8 for SSD, 2 for HDD
```

### Progress Reporting
```python
def on_progress(current, total, label):
    # Update UI progress bar or status label
    status_label.config(text=f"Scanning {label}: {current}/{total}")
    root.update_idletasks()

results = scanner.scan_versions(versions, progress_callback=on_progress)
```

### UI Thread Safety
```python
# In worker thread
def scan_worker():
    results = scanner.scan_versions(versions)
    
    # Schedule UI update on main thread
    root.after(0, lambda: update_tree_with_results(results))

# Start background thread
threading.Thread(target=scan_worker, daemon=True).start()
```

## Localization Keys to Add

When implementing cleanup features, add these keys to `en_us.py` following the established prefix conventions:

```python
# File Scanner (follow btn_, label_, status_ prefixes)
"btn_scan_files": "Scan for .bak/.old Files",
"status_scanning_files": "Scanning files...",
"status_files_found": "Found {} .bak/.old files",
"btn_delete_files": "Delete Selected Files",

# Folder Scanner  
"btn_scan_folders": "Scan Cleanable Folders",
"status_scanning_folders": "Scanning folders...",
"status_folders_found": "Found {} cleanable folders",
"btn_clean_folders": "Clean Selected Folders",

# Orphan Scanner
"btn_scan_orphans": "Scan for Orphaned SavedVariables",
"status_scanning_orphans": "Scanning for orphans...",
"status_orphans_found": "Found {} orphaned files",
"btn_delete_orphans": "Delete Selected Orphans",

# Operations
"title_confirm_delete": "Confirm Deletion",
"msg_confirm_delete": "Are you sure you want to {} {} items?",
"title_delete_complete": "Deletion Complete",
"status_deleted_items": "Successfully processed {} items",
"option_move_to_trash": "Move to Recycle Bin",
"option_delete_permanently": "Delete Permanently",
```

**Note**: All new keys should follow the prefix naming convention:

## Testing Checklist

When adding each feature:
- [ ] Verify application builds: `pyinstaller src/wow_cleanup_tool.spec`
