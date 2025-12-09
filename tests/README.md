# Unit Tests

This directory contains automated unit tests for the WoW Cleanup Tool.

## Running Tests

Run all tests:
```bash
python -m unittest discover tests/
```

Run specific test file:
```bash
python -m unittest tests.test_localization
python -m unittest tests.test_path_manager
```

Run with verbose output:
```bash
python -m unittest discover tests/ -v
```

## Test Coverage

### `test_localization.py` (15 tests)
Tests for the localization system:
- Translation loading and fallback
- Localization class initialization and translation lookup
- Translation completeness calculation
- Language display names
- Module constants

### `test_path_manager.py` (28 tests)
Tests for WoW path management:
- PathManager initialization
- Class constants (COMMON_PATHS, WOW_FLAVORS)
- Path validation (valid/invalid/empty paths)
- WoW flavor detection (single/multiple flavors)
- Path getter methods (AddOns, WTF, Cache, etc.)
- Installation validation
- Directory population checking

## Test Structure

Tests use Python's built-in `unittest` framework:
- Each test file contains multiple `TestCase` classes
- Each `TestCase` groups related tests
- `setUp()` and `tearDown()` methods handle test fixtures
- Tests create temporary directories when needed

## Type Safety

All test files include type hints where applicable and are checked by Pylance/Pyright for type correctness.

## Future Tests

Potential areas for additional testing:
- `base_scanner.py` - Parallel scanning operations
- `settings.py` - Settings load/save operations (needs mocking)
- UI components (lower priority - integration tests more suitable)
