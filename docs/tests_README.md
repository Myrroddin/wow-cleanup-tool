# Unit Tests

Automated unit tests for WoW Cleanup Tool. UI is modular (tabs in `src/ui/tabs/`, log controls in `src/ui/log_controls.py`). All file operations tested with mocks/temporary files.

## Running Tests

**All tests:**
```bash
pytest --maxfail=1 --disable-warnings
```

**Specific file:**
```bash
pytest tests/test_localization.py
pytest tests/test_dependencies.py
```

## Results

**189 tests** | 188 passed | 1 skipped | 0 failed

## Coverage by Module

**New Tests:**
- `test_dependencies.py` (20): Parallel installation (ThreadPoolExecutor 3 workers), queue communication, stable releases only, 30s timeout
- `test_tooltip.py` (9): TkFixedFont 10pt, theme colors, boundary detection, show/hide lifecycle
- `test_folder_cleaner_tab.py` (+12): Screenshot caching, Configure debouncing (50ms), wraplength updates

**Existing Tests:**
- `test_localization.py` (15): Translation loading, fallback, key validation
- `test_path_manager.py` (30): Flavor detection (8 flavors), path validation, installation checks
- `test_logger.py` (12): Thread-safe logging, rotation, append mode, widget handlers
- `test_file_cleaner.py` (9): .bak/.old detection, nested scanning, permissions
- `test_file_operations.py` (15): Batch delete (4-tuple return), trash/permanent modes, AddOns.txt cleaning
- `test_log_controls.py` (10): Copy, save, clear, delete operations
- `test_log_tabs.py` (5): Tab initialization, timestamps, layout
- `test_main_window.py` (4): Window init, tab management, background tasks
- `test_orphan_scanner.py` (12): Addon detection, orphan identification
- `test_settings.py` (5): Settings load/save
- Others: error_handler (1), themes (1), wow_cleanup_tool (2), screenshot_viewer (2), localization_en_us (7)

## Framework

- **pytest** with unittest TestCase classes
- Mocking for file I/O and external dependencies
- setUp/tearDown for fixtures and cleanup
- Type hints validated by Pylance/Pyright

See [TYPE_HINTS_AND_TESTS_SUMMARY.md](TYPE_HINTS_AND_TESTS_SUMMARY.md) for implementation details.
