

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

**Total**: 109 tests | **Passed**: 109 | **Skipped**: 1 | **Failed**: 0

## Test Coverage

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
- Logging and error handling

### `test_log_controls.py` (9 tests, 1 skipped)
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

### Other Tests
- `test_error_handler.py` (1 test) - Error handling utilities
- `test_themes.py` (1 test) - Theme system
- `test_wow_cleanup_tool.py` (2 tests) - Main app startup and initialization

## Test Structure

- Uses Python's built-in `unittest` framework
- Each test file contains multiple `TestCase` classes
- `setUp()` and `tearDown()` methods handle test fixtures and mocks
- Tests create temporary directories or use mocking for file I/O

## Type Safety

All test files include type hints where applicable and are checked by Pylance/Pyright for type correctness.

## Future Tests

Potential areas for additional testing:
- `base_scanner.py` - Parallel scanning operations with progress callbacks
- Advanced UI integration tests (lower priority)
- Performance benchmarks for large directory trees
