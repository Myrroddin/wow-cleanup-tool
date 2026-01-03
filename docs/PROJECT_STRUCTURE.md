# Project Structure

## Directory Organization

```
wow-cleanup-tool/
├── .github/                    # GitHub configuration
│   ├── workflows/
│   │   └── build-release.yml  # CI/CD for building executables
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   └── FUNDING.yml            # Sponsorship info
│
├── src/                      # Main application source code
│   ├── core/                 # Core application infrastructure
│   │   ├── background_task.py# Threaded background task runner with error handling
│   │   ├── bootstrap.py      # Application bootstrap and dependency checks
│   │   ├── dependencies.py   # Parallel dependency installation (ThreadPoolExecutor, queue-based)
│   │   ├── error_handler.py  # Global error handling and reporting
│   │   ├── instance_utils.py # Single instance enforcement utilities
│   │   ├── logger.py         # Dual-channel logging (user + developer)
│   │   ├── settings.py       # Settings persistence (per-user + cache)
│   │   ├── single_instance.py# Prevent multiple app instances
│   │   └── themes.py         # Theme system (light/dark mode)
│   ├── localization/         # Multi-language support
│   │   ├── __init__.py       # Localization class
│   │   └── en_us.py          # English translations (140+ keys, organized by prefix)
│   ├── operations/           # File system operations
│   │   ├── base_scanner.py   # Base class for all scanners (parallel processing, progress callbacks)
│   │   ├── file_cleaner.py   # Scanner for .bak/.old backup files
│   │   ├── file_operations.py# Batch delete/trash + AddOns.txt cleaning
│   │   ├── orphan_scanner.py # Scanner for orphaned SavedVariables
│   │   └── README.md         # Operations module documentation
│   ├── ui/                   # User interface components
│   │   ├── dialogs/          # Dialog windows
│   │   │   ├── __init__.py   # Dialog exports
│   │   │   ├── license_dialog.py       # GPL-3.0 license dialog
│   │   │   ├── multiple_installations.py # Multiple WoW installs warning
│   │   │   ├── screenshot_viewer.py    # Screenshot preview with caching
│   │   │   └── wow_close_warning.py    # WoW running warning
│   │   ├── tabs/             # Tab implementations
│   │   │   ├── developer_tab.py     # Developer log tab
│   │   │   ├── file_cleaner_tab.py  # File cleaner tab
│   │   │   ├── folder_cleaner_tab.py# Folder cleaner tab with screenshot caching
│   │   │   ├── game_optimizer_tab.py# Game optimizer tab
│   │   │   └── log_tab.py           # User log tab
│   │   ├── widgets/          # Custom widgets
│   │   │   ├── __init__.py   # Widgets package
│   │   │   └── tooltip.py    # Fixed 10pt TkFixedFont tooltips with boundary detection
│   │   ├── __init__.py       # UI module exports
│   │   ├── app_controller.py # Event handlers and UI state management
│   │   ├── custom_tabbar.py  # Custom tab bar with tooltips and debouncing
│   │   ├── dialog_base.py    # Base class for theme-aware dialogs
│   │   ├── font_utils.py     # System font detection
│   │   ├── geometry.py       # Window geometry calculations
│   │   ├── log_controls.py   # Centralized log control buttons
│   │   ├── main_window.py    # Main window builder (6 tabs)
│   │   ├── text_widget_handler.py # Text widget log output handler
│   │   └── ui_constants.py   # UI dimensions and styling constants
│   ├── wow/                  # WoW-specific functionality
│   │   ├── __init__.py       # WoW module exports
│   │   ├── path_handler.py   # WoW path detection and user browsing
│   │   ├── path_manager.py   # Installation management and validation
│   │   └── version_manager.py# Game version detection and management
│   ├── wow_cleanup_tool.py   # Main application entry point
│   └── wow_cleanup_tool.spec # PyInstaller build configuration
│
├── assets/
│   └── icons/                # Application icons
│       ├── wow_cleanup_icon.ico   # Windows icon
│       └── wow_cleanup_icon.icns  # macOS icon
│
├── docs/                    # Documentation files
│   ├── BACKGROUND_TASK_GUIDE.md    # BackgroundTask usage guide
│   ├── CODE_DOCUMENTATION.md       # Code documentation standards
│   ├── IMPLEMENTATION_ROADMAP.md   # Development roadmap
│   ├── LOGGING_GUIDE.md            # Logging system guide
│   ├── PROJECT_STRUCTURE.md        # This file
│   ├── README.md                   # Main documentation
│   ├── tests_README.md             # Test suite documentation
│   └── TYPE_HINTS_AND_TESTS_SUMMARY.md # Type hints and testing overview
│
├── tests/                  # Unit tests (189 tests: 188 passed, 1 skipped)
│   ├── test_dependencies.py        # DependencyManager tests (20 tests)
│   ├── test_error_handler.py       # ErrorHandler tests
│   ├── test_file_cleaner.py        # FileCleaner tests
│   ├── test_file_operations.py     # File operations tests
│   ├── test_folder_cleaner_tab.py  # FolderCleanerTab tests (28 tests)
│   ├── test_localization.py        # Localization tests
│   ├── test_localization_en_us.py  # English translation tests
│   ├── test_log_controls.py        # Log controls tests
│   ├── test_log_tabs.py            # Log/Developer tab tests
│   ├── test_logger.py              # Logger tests
│   ├── test_main_window.py         # Main window tests
│   ├── test_orphan_scanner.py      # OrphanScanner tests
│   ├── test_path_manager.py        # PathManager tests
│   ├── test_screenshot_viewer.py   # Screenshot viewer tests
│   ├── test_settings.py            # Settings tests
│   ├── test_themes.py              # Theme system tests
│   ├── test_tooltip.py             # Tooltip widget tests (9 tests)
│   └── test_wow_cleanup_tool.py    # Main application tests
│
├── tools/                  # Development utilities
│   └── audit_i18n_keys.py  # Localization key audit tool
│
├── LICENSE                 # GPL-3.0 license
├── README.md               # Project readme
├── requirements.txt        # Python dependencies
└── test_results.txt        # Latest test execution results
```

## Design Principles

**Separation of Concerns**: Backend (operations) = pure logic; Frontend (ui) = user interaction; Core = shared infrastructure

**Modularity**: Single responsibility per module; clear import hierarchy (core → localization/operations/wow → ui → main); no circular dependencies

**Performance**: os.scandir() for fast I/O; ThreadPoolExecutor parallel processing (BaseScanner, dependencies); compiled regex patterns; Configure debouncing (50ms); screenshot caching (PIL LANCZOS); tab tooltip debouncing (200ms); emoji auto-scaling; thread-safe queue communication; minimal update_idletasks

**User Experience**: Localized text with fallback; theme-aware UI; persistent settings (per-user JSON); graceful error degradation

**Extensibility**: BaseScanner for new cleanup features; batch file operations; plugin-ready localization; BaseDialog for themed dialogs; modular tab system

## Build & Configuration

**PyInstaller** (`wow_cleanup_tool.spec`): Defines standalone executable builds with module paths, platform icons, hidden imports, single-file output

**GitHub Actions** (`.github/workflows/build-release.yml`): Automated CI/CD for Windows/macOS/Linux on version tags (v*.*.*), creates release artifacts

## Data Files

**Settings** (`~/.wow_cleanup_tool/settings.json`): Theme, font, language, window geometry, delete mode (trash/permanent), verbose/append logging  
**WoW Cache** (`<WoW_Install>/.wow_cleanup_cache.json`): Cached WoW path, avoids admin rights for global settings  
**User Log** (`~/.wow_cleanup_tool/user_log.txt`): Persistent log when append mode enabled, newest-first with session separators

**Tabbed Logging**:
- Feature tabs: File Cleaner, Folder Cleaner, Game Optimizer, Optimization Suggestions
- Log tab: User operations with `.log()` (essential) and `.verbose()` (detailed); Copy/Save/Delete buttons (log_controls.py); delete button dimmed when append OFF; respects delete mode
- Developer tab: Technical diagnostics with `.debug()` (blue), `.error()` (red + 🔴 badge counter); Copy/Save for bug reports; always verbose
- Session management: Append mode persists logs newest-first

## Import Patterns

**Main**: `from core.logger import Logger; from core.settings import load_settings; from localization import Localization; from ui.main_window import MainWindow; from wow.path_manager import PathManager`

**UI**: `from ..core.themes import apply_theme; from ..localization import Localization; from .ui_constants import DialogDimensions; from .dialog_base import BaseDialog`

**Operations**: `from operations.base_scanner import BaseScanner; from operations.file_cleaner import FileCleaner; from operations.file_operations import delete_files_batch`

## Testing Checklist
- [ ] Run application to verify imports
- [ ] Check linting errors
- [ ] Update `wow_cleanup_tool.spec` if modules added/moved
- [ ] Update this document and `IMPLEMENTATION_ROADMAP.md`
- [ ] Test PyInstaller build: `pyinstaller wow_cleanup_tool.spec`
- [ ] Verify no __pycache__ committed
- [ ] Ensure user-facing strings localized and sorted
- [ ] Ensure new/changed code covered by isolated unit tests

---

**Related Documentation**:
- [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) - Detailed module descriptions
- [LOGGING_GUIDE.md](LOGGING_GUIDE.md) - Logging system usage
- [BACKGROUND_TASK_GUIDE.md](BACKGROUND_TASK_GUIDE.md) - Background task patterns
- [tests_README.md](tests_README.md) - Test suite and coverage
- [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) - Development roadmap
