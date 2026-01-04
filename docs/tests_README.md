# Unit Tests

Automated unit tests for WoW Cleanup Tool using pytest. UI is modular (tabs in `src/ui/tabs/`, log controls in `src/ui/log_controls.py`). All file operations tested with mocks/temporary files.

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

**With verbose output:**
```bash
pytest -v
```

**With coverage report:**
```bash
pytest --cov=src --cov-report=html
```

## Test Coverage

Tests cover all major functionality including:
- Dependencies (parallel installation, queue comms, timeouts)
- UI components (folder cleaner tab, main window, screenshot viewer, tooltips)
- File operations (trash vs permanent delete, AddOns.txt cleaning)
- Localization (fallback, key validation)
- Path management (flavor detection, path validation)
- Logger (thread-safe logging, rotation, append mode)
- Core utilities (settings, themes, error handling)

## Framework

- **pytest** with unittest TestCase classes
- Mocking for file I/O and external dependencies
- setUp/tearDown for fixtures and cleanup
- Type hints validated by Pylance/Pyright

See [TYPE_HINTS_AND_TESTS_SUMMARY.md](TYPE_HINTS_AND_TESTS_SUMMARY.md) for implementation details.
