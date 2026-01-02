# Implementation Roadmap for Cleanup Features

This roadmap tracks the development of the WoW Cleanup Tool, with a focus on modularity, maintainability, and user experience. The codebase uses a modular UI architecture:
- **Tabs**: Each main tab (File Cleaner, Folder Cleaner, Game Optimizer, Log, Developer) is a separate class in `src/ui/tabs/`. Log and Developer tabs now include a visible text area and log control buttons, using a grid-based layout.
- **Log Controls Utility**: All log actions (copy, save, clear, delete) are handled by `src/ui/log_controls.py` for both user and developer logs.
- **Custom Widgets**: Standalone widgets (e.g., Tooltip) are in `src/ui/widgets/`.
- **Main Window**: `main_window.py` delegates tab UI and log actions to dedicated modules.

---

## Current Status
- Modular UI refactor: All main tabs are now separate classes in `src/ui/tabs/`
- **✅ Core Application Features: FEATURE-COMPLETE**
  - Automatic WoW path detection (registry scan + common paths)
  - Manual path selection with validation
  - Multi-flavor support (Retail, Classic, PTR, Beta, and combinations)
  - Installation validation (flavor detection, directory structure)
  - Settings persistence (theme, font, delete mode, logging preferences)
  - Auto-save on all preference changes
  - Cross-platform support (Windows, macOS, Linux)
- **✅ UI Layout & Theming: FEATURE-COMPLETE**
  - Light/dark theme support with live updates
  - Custom font selection (8–16pt, default 12)
  - Grid-based layout system with proper widget placement
  - Dynamic resizing and responsive controls
  - All dialogs and tooltips theme-aware
  - Centralized theme/font refresh logic
- **✅ File Cleaner Tab: FEATURE-COMPLETE**
  - Dual-panel UI: Backup files (.bak/.old) and Orphaned SavedVariables
  - Background scanning with progress callbacks
  - Multi-select tree widgets with hierarchical display (version → files)
  - Batch deletion with logging (move to trash or permanent delete)
  - Integration with FileCleaner and OrphanScanner
  - AddOns.txt cleaning: Automatically removes orphaned addon names from AddOns.txt files when orphaned SavedVariables are deleted
    - Scans entire WTF directory structure (account-level and realm-level SavedVariables)
    - Extracts addon names from deleted .lua files
    - Removes entries from AddOns.txt while preserving file integrity
    - Supports multi-version WoW installations
  - Comprehensive error handling and threading safety
  - Full test coverage: 15 file operation tests + 6 AddOns.txt-specific tests + 12 orphan scanner tests
  - Optimized size column: 100px fixed width (was 150px), more space for file paths
- **✅ Log and Developer tabs: FEATURE-COMPLETE**
  - User Log Tab: 4 buttons (Clear Session Log, Delete Log File, Open Log Folder, Copy to Clipboard)
  - Developer Log Tab: 3 buttons (Clear Session Log, Open Log Folder, Copy to Clipboard)
  - Text widget dimensions dynamically scale with font size (log tabs: 18 rows, license: 25 rows × font_size ÷ 12)
  - All tk.Text widgets now font-aware across entire application
  - Append-mode-aware "Clear Session Log": clears display + deletes file when append OFF; clears display only when append ON
  - "Delete Log File" button dynamically dims/disables when append mode OFF (using overlay technique)
  - Descriptions added to both tabs with proper word-wrapping
  - Grid-based layout with matching aesthetics between tabs
  - "Open Log Folder" replaces redundant save buttons (auto-save on every log entry)
  - Button state adapts to theme changes without geometry issues
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
- **OrphanScanner** implemented and integrated (scans SavedVariables for orphaned AddOn settings)
- **file_operations.py**: batch delete/trash (logging handled by caller to prevent duplication)
- Codebase cleanup: Removed unused operation stubs (file_scanner, folder_scanner, disk_utils)
- Removed dead UI methods and placeholder comments
- Single-instance lock reusable within process for test suite compatibility
- **Defensive programming**: Type guards in file deletion to prevent string-iteration bugs with clear error logging
- **Universal logging pattern**: logger.log() vs logger.verbose() use if/else (never both for same action)
- **Comprehensive test coverage**:
    - 129 total tests: 127 passed, 2 skipped (platform-specific)
    - New: 12 OrphanScanner tests (addon detection, orphan identification, multi-version scanning)
    - New: 6 AddOns.txt cleaning tests (removal, Blizzard_ protection, .bak skipping, multi-character handling)
    - Updated: Localization tests include AddOns.txt key validation
    - Updated: Tkinter compatibility handling for CI/CD environments
    - Tests cover: initialization, validation, detection, UI widgets, log controls, file operations, orphan scanning, AddOns.txt cleaning
    - Mock objects for testing without filesystem dependencies
    - Execution time: ~7-21 seconds (varies by system)

---

## Next Steps (When Ready)
* [ ] Integrate FolderCleaner into UI tab for cache/logs/screenshots/errors cleanup
* [ ] Implement FolderScanner for cleanable folders (Logs, Errors, Cache, Screenshots)
* [ ] Add Game Optimizer tab with smart suggestions
* [ ] Add custom tree widget enhancements (filtering, sorting)

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

### Phase 3: Game Optimizer & Advanced Features
- Custom tree widget enhancements (filtering, sorting)
- Progress bars for scan operations
- Performance metrics and suggestions
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

## Localization Status

**Completed Keys** (File Cleaner - already implemented):
- ✅ `btn_scan_files` - "Scan Files"
- ✅ `btn_remove_selected` - "Remove Selected"
- ✅ `btn_select_all_toggle` - "Select All / Unselect All"
- ✅ `option_delete_mode_trash` - "Move to Trash"
- ✅ `option_delete_mode_permanent` - "Delete Permanently"
- ✅ All tab labels (file_cleaner, folder_cleaner, game_optimizer, log, developer)
- ✅ All WoW flavor display names (retail, classic, ptr, beta, etc.)

**Keys Needed for Future Features** (Folder Scanner - when implemented):
```python
"btn_scan_folders": "Scan Cleanable Folders"
"status_scanning_folders": "Scanning folders..."
"status_folders_found": "Found {} cleanable folders"
```

**Note**: All new keys follow the prefix naming convention (btn_, status_, label_, etc.) and are alphabetically sorted in `en_us.py`.

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
