

# Unit Tests

This directory contains automated, isolated unit tests for the WoW Cleanup Tool.

**Note:** The UI is modular, with each main tab implemented as a separate class in `src/ui/tabs/`, and all log actions handled by the log controls utility (`src/ui/log_controls.py`). All file-based code is tested in isolation using mocks or temporary files.

## Running Tests

Run all tests with pytest:
```bash
pytest --maxfail=1 --disable-warnings
```

Run a specific test file:
```bash
pytest tests/test_localization.py
pytest tests/test_path_manager.py
pytest tests/test_logger.py
```

## Test Summary

**Total**: 189 tests | **Passed**: 188 | **Skipped**: 1 | **Failed**: 0

## Test Coverage

### `test_dependencies.py` (20 tests) - NEW
- DependencyManager parallel installation with ThreadPoolExecutor (3 workers max)
- Queue-based communication for progress updates (update_queue parameter)
- Package installation with stable/beta/alpha fallback strategies
- 30-second timeout handling for slow installations
- Installation result tracking and caching
- Error handling and graceful fallbacks

### `test_tooltip.py` (9 tests) - NEW
- Tooltip widget initialization with theme colors
- Fixed TkFixedFont 10pt rendering
- Toplevel window creation and lifecycle (show/hide)
- Smart boundary detection (280px wraplength default)
- Screen edge detection to prevent off-screen tooltips
- Multiple show/hide cycles
- Long text wrapping with custom wraplength

### `test_localization.py` (15 tests)
- Translation loading and fallback
- Localization class initialization and translation lookup
- Missing key handling

### `test_path_manager.py` (30 tests)
- PathManager initialization
- WoW flavor detection (all 8 flavors: Retail, Classic, PTR, Beta, and combinations)
- Path getter methods (AddOns, WTF, Cache, etc.)
- Installation validation
- Directory population checking
- Display name generation for game versions

### `test_logger.py` (12 tests)
- Logger initialization, log/verbose/debug/error/warning methods
- Log rotation and append mode
- UI widget handler with thread safety (mocked)
- Error badge callback
- RuntimeError handling in test environment (no event loop)

### `test_settings.py` (5 tests)
- Settings load/save (mocked file I/O)
- User log file save/load

### `test_file_cleaner.py` (9 tests)
- FileCleaner initialization (max_workers, logger)
- Regex pattern matching for .bak/.old files (case-insensitive)
- Scanning empty directories
- Scanning directories with .bak files
- Nested directory traversal
- Permission error handling
- Integration with PathManager (mocked)

### `test_file_operations.py` (9 tests) - NEW
- delete_files_batch 4-tuple return signature (processed_count, permanently_deleted, used_trash, processed_paths)
- Single file and multiple file deletion
- Directory deletion
- Mixed file/directory operations
- Trash vs permanent deletion modes
- Logging behavior (file_operations.py does NOT log successful deletions to prevent duplication; calling code handles logging)

### `test_log_controls.py` (10 tests)
- Log control button operations (copy, save, clear, delete)
- Logging integration
- File I/O operations
- UI state management

### `test_log_tabs.py` (5 tests)
- User Log tab initialization and functionality
- Developer Log tab initialization and functionality
- Chat timestamp toggle
- Append mode handling
- UI layout verification

### `test_main_window.py` (4 tests)
- Main window initialization
- Tab creation and management
- Background deletion task execution
- Empty item list handling
- Path deduplication

### `test_localization_en_us.py` (6 tests)
- All required localization keys present
- User log and removal operation keys
- Verbose logging message format
- Unknown version fallback
- Alphabetically sorted keys

### `test_folder_cleaner_tab.py` - Updated Tests (+12 new)
Added comprehensive tests for new features:
- **Screenshot Caching**: Cache initialization, storage/retrieval, clearing on rescan
- **Configure Debouncing**: Event debouncing with 50ms timer, timer cancellation
- **Wraplength Updates**: Font size changes trigger instruction label wraplength refresh
- **Stale Data Clearing**: Old data cleared between scan operations
- **Previous Tests Retained**: All original folder display, selection, and preview tests

### Other Tests
- `test_error_handler.py` (1 test) - Error handling utilities
- `test_themes.py` (1 test) - Theme system
- `test_wow_cleanup_tool.py` (2 tests) - Main app startup and initialization

## Test Structure

- Uses `pytest` testing framework
- Each test file contains multiple test functions or `TestCase` classes
- `setUp()` and `tearDown()` methods handle test fixtures and mocks
- Tests create temporary directories or use mocking for file I/O
- Run with `pytest --maxfail=1 --disable-warnings` for fast feedback

## Type Safety

All test files include type hints where applicable and are checked by Pylance/Pyright for type correctness.

## Future Tests

Potential areas for additional testing:
- `base_scanner.py` - Parallel scanning operations with progress callbacks
- Advanced UI integration tests (lower priority)
- Performance benchmarks for large directory trees
