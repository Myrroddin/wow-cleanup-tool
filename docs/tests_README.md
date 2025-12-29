

# Unit Tests

This directory contains automated, isolated unit tests for the WoW Cleanup Tool.

**Note:** The UI is modular, with each main tab implemented as a separate class in `src/ui/tabs/`, and all log actions handled by the log controls utility (`src/ui/log_controls.py`). All file-based code is tested in isolation using mocks or temporary files.

## Running Tests

Run all tests:
```bash
python -m unittest discover tests/ -v
```

Run a specific test file:
```bash
python -m unittest tests.test_localization
python -m unittest tests.test_path_manager
python -m unittest tests.test_logger
```

## Test Coverage

### `test_localization.py`
- Translation loading and fallback
- Localization class initialization and translation lookup
- Translation completeness calculation
- Language display names
- Module constants

### `test_path_manager.py`
- PathManager initialization
- Class constants (COMMON_PATHS, WOW_FLAVORS)
- Path validation (valid/invalid/empty paths)
- WoW flavor detection (single/multiple flavors)
- Path getter methods (AddOns, WTF, Cache, etc.)
- Installation validation
- Directory population checking

### `test_logger.py`
- Logger initialization, log/verbose/debug/error/warning
- Log rotation and append mode
- UI widget handler (mocked)
- Error badge callback

### `test_settings.py`
- Settings load/save (mocked file I/O)
- User log file save/load

### `test_file_cleaner.py`
- FileCleaner initialization (max_workers, logger)
- Regex pattern matching for .bak/.old files (case-insensitive)
- Scanning empty directories
- Scanning directories with .bak files
- Nested directory traversal
- Permission error handling
- Integration with PathManager (mocked)

### `test_localization_en_us.py`, `test_error_handler.py`, `test_wow_cleanup_tool.py`, `test_main_window.py`, `test_log_tabs.py`
- Additional coverage for localization keys, error handling, main app startup, main window initialization, and log tab functionality

## Test Structure

- Uses Python's built-in `unittest` framework
- Each test file contains multiple `TestCase` classes
- `setUp()` and `tearDown()` methods handle test fixtures and mocks
- Tests create temporary directories or use mocking for file I/O

## Type Safety

All test files include type hints where applicable and are checked by Pylance/Pyright for type correctness.

## Future Tests

Potential areas for additional testing:
- `base_scanner.py` - Parallel scanning operations
- UI integration tests (lower priority)
