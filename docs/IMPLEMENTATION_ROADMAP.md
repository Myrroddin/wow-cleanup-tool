# Implementation Roadmap

Tracks WoW Cleanup Tool development with modular architecture: tabs in `src/ui/tabs/`, log controls in `src/ui/log_controls.py`, widgets in `src/ui/widgets/`.

**See also**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for directory organization | [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) for module details

## Architecture
- **Tabs**: Separate classes (File Cleaner, Folder Cleaner, Optimizer, Logs) with grid layouts
- **Log Controls**: Centralized in `log_controls.py` (copy, save, clear, delete)
- **Widgets**: Standalone components (Tooltip, etc.)
- **Main Window**: Delegates to modular tabs and utilities

## Completed Features ✅

### Core Application
- WoW path detection (registry + common paths), manual selection, validation
- Multi-flavor support (Retail, Classic, PTR, Beta, combinations)
- Settings persistence (theme, font, delete mode, logging), auto-save
- Cross-platform (Windows, macOS, Linux)

### UI & Theming
- Light/dark themes with live updates, centralized refresh logic
- Custom fonts (8–16pt, default 12), dynamic scaling
- Grid-based layout, responsive controls, theme-aware dialogs/tooltips

### Performance Optimizations
- Configure event debouncing (50ms tabs, 200ms tooltips) prevents layout thrashing
- Screenshot caching (PIL Image.thumbnail, LANCZOS resampling)
- Emoji icons (auto-scale, no image loading overhead)
- Parallel dependency installation (ThreadPoolExecutor, 3 workers, 30s timeout)
- Thread-safe queue-based UI updates (queue.Queue + root.after)
- Fixed TkFixedFont 10pt tooltips with boundary detection

### File Cleaner Tab
- Dual-panel: Backup files (.bak/.old) + Orphaned SavedVariables
- Background scanning, progress callbacks, hierarchical tree display
- Batch deletion (trash/permanent), FileCleaner/OrphanScanner integration
- AddOns.txt cleaning: Auto-removes orphaned addon entries from WTF structure
- Test coverage: 15 file ops + 6 AddOns.txt + 12 orphan scanner tests

### Log Tabs
- User: 4 buttons (Clear Session, Delete File, Open Folder, Copy)
- Developer: 3 buttons (Clear Session, Open Folder, Copy)
- Font-aware dimensions (18 rows × font_size ÷ 12), dynamic wraplength
- Append-mode aware, button state management, theme adaptation

### Code Quality
- Modular UI, centralized utilities, removed dead code/unused imports
- BaseScanner (parallel scanning, callbacks), defensive programming
- Type guards, universal logging pattern (if/else, not both)
- 189 tests (188 passed, 1 skipped), mock objects, ~7s execution

## Upcoming Features
- [ ] Folder Cleaner tab (Cache, Logs, Errors, Screenshots)
- [ ] FolderScanner implementation
- [ ] Game Optimizer tab with smart suggestions
- [ ] Tree widget enhancements (filtering, sorting)

## Localization
- **Default/Fallback**: English (US)
- **Pending**: 11 additional languages
- **Keys**: Alphabetically sorted with prefix convention (btn_, status_, label_)

## Development Guidelines

### BaseScanner Usage
```python
scanner = FileCleaner(max_workers=8, logger=logger, loc=loc)
results = scanner.scan_versions(versions, progress_callback=on_progress)
```

### UI Thread Safety
```python
def scan_worker():
    results = scanner.scan_versions(versions)
    root.after(0, lambda: update_tree_with_results(results))

threading.Thread(target=scan_worker, daemon=True).start()
```

### Testing Checklist
- [ ] Unit tests with mocks (no real WoW installation)
- [ ] Error handling (permissions, missing dirs)
- [ ] Logger integration, alphabetically sorted keys
- [ ] Update `wow_cleanup_tool.spec`, run test suite
- [ ] Verify build: `pyinstaller src/wow_cleanup_tool.spec`

**See also**: [tests_README.md](tests_README.md) for running tests and coverage details.
