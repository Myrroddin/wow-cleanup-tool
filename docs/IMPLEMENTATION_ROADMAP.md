# Implementation Roadmap for Cleanup Features

This roadmap tracks the development of the WoW Cleanup Tool, with a focus on modularity, maintainability, and user experience. The codebase uses a modular UI architecture:
- **Tabs**: Each main tab (File Cleaner, Folder Cleaner, Game Optimizer, Log, Developer) is a separate class in `src/ui/tabs/`. Log and Developer tabs now include a visible text area and log control buttons, using a grid-based layout.
- **Log Controls Utility**: All log actions (copy, save, clear, delete) are handled by `src/ui/log_controls.py` for both user and developer logs.
- **Custom Widgets**: Standalone widgets (e.g., Tooltip) are in `src/ui/widgets/`.
- **Main Window**: `main_window.py` delegates tab UI and log actions to dedicated modules.

---

## Current Status
- Modular UI refactor: All main tabs are now separate classes in `src/ui/tabs/`
- Log and Developer tabs now include a visible text area and log control buttons, using a grid-based layout
- Log controls utility: Centralized log actions in `src/ui/log_controls.py`
- Custom widgets: Tooltip and future widgets in `src/ui/widgets/`
- Main window delegates to modular tabs and log controls
- All main window rows use unique grid rows for clear, non-overlapping layout
- Language dropdown in WoW path row is now correctly placed, fully visible, and does not overlap other widgets
- Main window dynamically resizes to fit all widgets in the WoW path row, ensuring no controls are hidden
- Browse button tooltip is concise and user-friendly
- Debug prints removed, codebase formatted with Black, and trailing spaces/blank lines normalized
- Centralized theme/font refresh logic for all UI elements
- Settings changes now provide immediate UI feedback
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
- **BaseScanner** implemented with parallel version scanning, progress callbacks, and error isolation
- **FileCleaner** implemented and tested (.bak/.old file scanner)
- **file_operations.py**: batch delete/trash with logging
- Codebase cleanup: Removed unused operation stubs (file_scanner, folder_scanner, orphan_scanner, disk_utils)
- Removed dead UI methods and placeholder comments
- Single-instance lock reusable within process for test suite compatibility
- All tests passing: 77 passed, 2 skipped

---

## Next Steps (When Ready)
* [ ] Integrate FileCleaner into UI tab with scan/delete functionality
* [ ] Implement FolderScanner for cleanable folders (Logs, Errors, Cache, Screenshots)
* [ ] Implement OrphanScanner for orphaned SavedVariables
* [ ] Add custom tree widget for displaying scan results

### Phase 1: File Scanner Integration
**Current**: `src/operations/file_cleaner.py` exists and is tested

**Integration Tasks**:
1. Wire up `FileCleanerTab` in main window to use `FileCleaner`
2. Add scan button that calls `FileCleaner.scan_all_flavors()`
3. Display results in a tree/list view
4. Add delete button using `file_operations.delete_files_batch()`
5. Use logger methods:
    - `logger.log()`: Essential messages ("Scan complete")
    - `logger.verbose()`: Detailed operations ("Deleted file: addon.bak")
    - `logger.debug()`: Technical details → Developer tab
    - `logger.error()`: Errors → Developer tab with 🔴 badge

### Phase 2: Folder Scanner
**File**: `src/operations/folder_scanner.py` (to be recreated)

```python
from typing import List, Set
import os
from operations.base_scanner import BaseScanner

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
```

### Phase 3: Orphan Scanner
**File**: `src/operations/orphan_scanner.py` (to be recreated)

More complex - needs to:
1. Scan `Interface/AddOns` for installed addons
2. Scan `WTF/Account/**` for SavedVariables files
3. Find .lua files for uninstalled addons
4. Ignore Blizzard_* core files

### Phase 4: UI Integration
- Custom tree widget for displaying scan results
- Progress bars for scan operations
- Checkboxes for selective deletion
- Summary dialogs after operations

## Performance Guidelines

### Using BaseScanner
```python
from operations.base_scanner import BaseScanner
from operations.file_cleaner import FileCleaner

# Initialize scanner with optimal workers
scanner = FileCleaner(max_workers=8, logger=self.logger, loc=loc)

# Scan with progress callback
def on_progress(current, total, label):
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

**Note**: All new keys should follow the prefix naming convention and be alphabetically sorted.

## Testing Checklist

When adding each feature:
- [ ] Write unit tests for new scanner classes
- [ ] Test with temporary directories (no real WoW installation needed)
- [ ] Mock PathManager for flavor detection
- [ ] Verify logger integration
- [ ] Test error handling (permissions, missing directories)
- [ ] Ensure alphabetically sorted localization keys
- [ ] Update `wow_cleanup_tool.spec` for new modules
- [ ] Run full test suite: `python -m unittest discover tests/ -v`
- [ ] Verify application builds: `pyinstaller src/wow_cleanup_tool.spec`
