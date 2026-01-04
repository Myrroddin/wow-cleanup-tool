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

**194 tests collected** | 192 passed | 2 skipped | 0 failed

## Coverage by Module

**Highlights:**
- `test_dependencies.py` (20): Parallel installation (3 workers), queue comms, 30s timeout
- `test_folder_cleaner_tab.py`: Screenshot caching, debounce, wraplength, selection/removal flows
- `test_main_window.py`: Screenshot remove handler (trash vs permanent), early-return safety
- `test_tooltip.py` (9): TkFixedFont 10pt, theme colors, boundary detection, lifecycle

**Other Coverage:**
- Localization (fallback, key validation), path_manager (8 flavors), logger (rotation, append), file_cleaner/file_operations (trash vs permanent, AddOns.txt), log controls/tabs, orphan scanner, settings, themes, tooltip, screenshot viewer, entrypoint smoke tests.

## Framework

- **pytest** with unittest TestCase classes
- Mocking for file I/O and external dependencies
- setUp/tearDown for fixtures and cleanup
- Type hints validated by Pylance/Pyright

See [TYPE_HINTS_AND_TESTS_SUMMARY.md](TYPE_HINTS_AND_TESTS_SUMMARY.md) for implementation details.
