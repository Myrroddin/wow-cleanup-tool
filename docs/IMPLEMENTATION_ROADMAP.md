# Implementation Roadmap


Tracks WoW Cleanup Tool development with modular architecture: tabs in `src/ui/tabs/`, log controls in `src/ui/log_controls.py`, widgets in `src/ui/widgets/`.

**See also**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for directory organization | [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) for module details

## Architecture
- **Tabs**: Separate classes (File Cleaner, Folder Cleaner, Optimizer, Logs) with grid layouts
- **Log Controls**: Centralized in `log_controls.py` (copy, save, clear, delete)
- **Widgets**: Standalone components (Tooltip, etc.)
- **Main Window**: Delegates to modular tabs and utilities

## Completed Features ✅

### Core & Platform
- WoW path detection (registry + common paths) with manual override and validation
- Multi-flavor support (Retail, Classic, Era, PTR, Beta)
- Settings persistence (theme, font, delete mode, logging) with auto-save
- Cross-platform startup (Windows/macOS/Linux)

### UI & Theming
- Light/dark themes with instant refresh; custom fonts (8–16pt, emoji support)
- Debounced layout (50ms tabs, 200ms tooltips) and theme-aware dialogs/tooltips
- Minimized `update_idletasks` usage

### Performance & Infrastructure
- `@lru_cache(maxsize=128)` on flavor display names; `@timed_cache` decorator for custom functions
- In-memory settings cache (10-100x speedup on repeated access)
- Font list cache with 1-hour TTL (100-500ms → <1ms)
- Hardware cache with 30-day TTL (parallel detection 60-70% faster)
- WoW path cache with 7-day TTL + path validation
- orjson settings I/O (2-3x faster JSON); queue-based UI updates; parallel dependency installs
- LANCZOS thumbnail caching for screenshots

### Folder & File Cleaning
- File Cleaner: .bak/.old cleanup, AddOns.txt repair, batch delete (trash/permanent)
- Folder Cleaner: cache/log/error toggles plus screenshot viewer (preview, expand, select/unselect/remove)
- Delete mode honored across tabs; background scans via `BackgroundTask`

### Logging & Quality
- Dual-channel logging with rotation, append mode, and centralized log controls
- Type hints across core modules; ruff/black clean
- Comprehensive test coverage across all major functionality

## Upcoming Features
- [ ] Game Optimizer tab with actionable suggestions
- [ ] Tree widget enhancements (filtering, sorting)
- [ ] Additional language packs (beyond en_us)
- [ ] PyInstaller hardening and release notes for first tagged build

## Localization
- **Default/Fallback**: English (US) - `src/localization/en_us.py`
- **Pending**: 11 additional languages ready for translation

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
