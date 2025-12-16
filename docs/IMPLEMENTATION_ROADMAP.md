

# Implementation Roadmap for Cleanup Features

This roadmap tracks the development of the WoW Cleanup Tool, with a focus on modularity, maintainability, and user experience. The codebase now uses a modular UI architecture:
- **Tabs**: Each main tab (File Cleaner, Folder Cleaner, Game Optimizer, Log, Developer) is a separate class in `src/ui/tabs/`.
- **Log Controls Utility**: All log actions (copy, save, clear, delete) are handled by `src/ui/log_controls.py` for both user and developer logs.
- **Custom Widgets**: Standalone widgets (e.g., Tooltip) are in `src/ui/widgets/`.
- **Main Window**: `main_window.py` delegates tab UI and log actions to dedicated modules.

---

## Current Status ✅
- Modular UI refactor: All main tabs are now separate classes in `src/ui/tabs/` ⭐ NEW
- Log controls utility: Centralized log actions in `src/ui/log_controls.py` ⭐ NEW
- Custom widgets: Tooltip and future widgets in `src/ui/widgets/` ⭐ NEW
- Main window delegates to modular tabs and log controls ⭐ NEW
- All main window rows use unique grid rows for clear, non-overlapping layout ⭐
- Language dropdown in WoW path row is now correctly placed, fully visible, and does not overlap other widgets ⭐
- Main window dynamically resizes to fit all widgets in the WoW path row, ensuring no controls are hidden ⭐
- Browse button tooltip is concise and user-friendly ⭐
- Debug prints for widget geometry include the language dropdown and aid in diagnosing layout issues ⭐
- Further UI polish and layout bugfixes for robust, user-friendly experience ⭐
- Debug prints removed, codebase formatted with Black, and trailing spaces/blank lines normalized ⭐
- Centralized theme/font refresh logic for all UI elements ⭐
- Settings changes now provide immediate UI feedback ⭐
- Robust settings persistence and reliable UI updates for all user preference changes
- Logger class refactored (60 lines reduced, helper methods extracted, constant caching)
- Font utilities caching (eliminates repeated system calls)
- All dialogs and tooltips now live-update their theme and font when user settings change
- Chat Timestamps checkbox added (affects both User Log and Developer Log)
- All translation keys alphabetically sorted for easy maintenance
- Localization tooltips and new keys added for all new features
- Fixed all indentation errors in UI and dialog code for reliable imports and execution
- Test framework: Python unittest, with tests for initialization, validation, detection, and helper functions
- Mock objects for testing without filesystem dependencies
- Removed unused imports (11 files cleaned up)
- All sapling-related code and files (CustomTabBar, SaplingCanvas, TreeNode, sapling_box_style_checklist.md) have been removed for a clean slate. A new custom tree widget will be implemented in a future phase.

---

## Next Steps (When Ready)

### Phase 1: File Scanner (.bak/.old files)
**File**: `src/operations/file_scanner.py`

```python
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
```

**Integration**:
1. Add to `src/operations/__init__.py`: `from .file_scanner import FileScanner`
2. Create UI tab in `src/ui/tabs/file_cleaner_tab.py`
3. Pass logger to scanner: `scanner = FileScanner(max_workers=workers, logger=self.logger, loc=loc)`
4. Add scan button that calls `FileScanner.scan_versions()`
5. Display results in a new custom tree widget (to be implemented)
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
- [x] FileScanner: .bak/.old file scan
- [x] FolderScanner: cleanable folder scan
- [x] OrphanScanner: orphaned SavedVariables scan (stub)
- [x] Batch file/folder delete operations
- [x] Alphabetically sorted localization keys
- [x] Updated .spec and GitHub workflow for new modules
