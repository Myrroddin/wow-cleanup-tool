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
│   │   ├── dependencies.py   # External dependency management
│   │   ├── geometry.py       # Window sizing and positioning utilities
│   │   ├── global_settings.py# Global constants and configuration
│   │   ├── logger.py         # Dual-channel logging (user + developer)
│   │   ├── settings.py       # Settings persistence (per-user + cache)
│   │   ├── single_instance.py# Prevent multiple app instances
│   │   └── themes.py         # Theme system (light/dark mode)
│   ├── localization/         # Multi-language support
│   │   ├── __init__.py       # Localization class
│   │   └── en_us.py          # English translations (100+ keys, organized by prefix)
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
│   │   │   └── wow_close_warning.py    # WoW running warning
│   │   ├── widgets/          # Custom widgets (future use)
│   │   │   └── __init__.py   # Widgets package
│   │   ├── __init__.py       # UI module exports
│   │   ├── app_controller.py # Event handlers and UI state management
│   │   ├── dialog_base.py    # Base class for theme-aware dialogs
│   │   ├── font_utils.py     # System font detection
│   │   ├── geometry.py       # Window geometry calculations
│   │   ├── main_window.py    # Main window builder (6 tabs)
│   │   └── ui_constants.py   # UI dimensions and styling constants
│   └── wow/                  # WoW-specific functionality
│       ├── __init__.py       # WoW module exports
│       ├── game_optimizer.py # Game configuration optimization (future)
│       ├── game_validation.py# Installation validation utilities
│       ├── path_handler.py   # WoW path detection and user browsing
│       └── path_manager.py   # Installation management and validation
│   └── wow_cleanup_tool.py   # Main application entry point
│   └── wow_cleanup_tool.spec # PyInstaller build configuration (v1.0 feature-complete)
│
├── assets/
│   └── icons/                # Application icons
│       ├── wow_cleanup_icon.ico   # Windows icon
│       ├── wow_cleanup_icon.icns  # macOS icon
│       └── *.png                  # PNG icons
│
├── docs/                    # Documentation files
│   ├── README.md
│   ├── LOGGING_GUIDE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── TYPE_HINTS_AND_TESTS_SUMMARY.md
│   ├── IMPLEMENTATION_ROADMAP.md
│   ├── tests_README.md
│   └── BACKGROUND_TASK_GUIDE.md
│
├── tests/                  # Unit tests (129 tests: 127 passed, 2 skipped)
│
├── LICENSE                 # GPL-3.0 license
└── requirements.txt        # Python dependencies
```

## Design Principles

### 1. Separation of Concerns
- **Backend** (operations): Pure logic, no UI, returns data
- **Frontend** (ui): Displays data, handles user interaction
- **Core**: System-level infrastructure used by both

### 2. Modularity
- Each module has single responsibility
- Clear import hierarchy: core → localization/operations/wow → ui → main
- No circular dependencies

### 3. Performance
- `os.scandir()` for fast file/folder listing
- Parallel processing with ThreadPoolExecutor (BaseScanner)
- Compiled regex patterns at module level (FileCleaner)

### 4. User Experience
- All user-facing text localized (sorted keys, robust fallback)
- Theme-aware UI components
- Settings persistence across sessions (per-user JSON)
- Error handling with graceful degradation

### 5. Extensibility
- `BaseScanner` class for new cleanup features (FileCleaner, OrphanScanner, future FolderScanner)
- File operations module with batch delete and AddOns.txt integration
- Plugin-ready localization system
- `BaseDialog` for new dialogs
- Modular tab system for new UI features

## Build Configuration

### PyInstaller (`wow_cleanup_tool.spec`)
Defines how to build standalone executables:
- Includes all module paths
- Platform-specific icon selection
- Hidden imports for dynamic modules
- Single-file executable output

### GitHub Actions (`.github/workflows/build-release.yml`)
Automated builds for Windows, macOS, and Linux:
- Triggers on version tags (v*.*.*)
- Builds platform-specific executables
- Creates release artifacts
- Automatic version updates in code

## Data Files

### Settings
- **User settings**: `~/.wow_cleanup_tool/settings.json`
  - Theme, font, language, window geometry
  - Delete mode ('trash' or 'permanent')
  - Verbose logging (True/False)
  - Append log (True/False, enables log persistence)
  - Per-user, cross-platform

- **WoW path cache**: `<WoW_Install>/.wow_cleanup_cache.json`
  - Cached detected WoW installation path
  - Avoids requiring admin rights for global settings

- **User log**: `~/.wow_cleanup_tool/user_log.txt`
  - Persistent log file (when append mode enabled)
  - Newest sessions at top with separators
  - Each session timestamped

### Logs
- **Tabbed interface** in main window:
  - **Feature tabs**: File Cleaner, Folder Cleaner, Game Optimizer, Optimization Suggestions (future)
  - **Log tab**: User operations with Copy/Save/Delete (log_controls.py)
    - `.log()`: Essential messages
    - `.verbose()`: Detailed operations (if verbose enabled)
    - Delete button visible only when append mode enabled
    - Respects delete mode setting (trash vs permanent)
  - **Developer tab**: Technical diagnostics (always verbose)
    - `.debug()`: Blue-colored debug messages
    - `.error()`: Red-colored errors with 🔴 badge counter
    - Copy/Save buttons for bug reports
- **Session management**: When append mode enabled, logs persist with newest-first ordering
- No external log files required (user preference)

## Import Patterns

### Main Application
```python
from core.logger import Logger
from core.settings import load_settings, save_settings
from localization import Localization
from ui.main_window import MainWindow
from wow.path_manager import PathManager
```

### UI Components
```python
from ..core.themes import apply_theme
from ..localization import Localization
from .ui_constants import DialogDimensions
from .dialog_base import BaseDialog
```

### Operations
```python
from operations.base_scanner import BaseScanner
from operations.file_cleaner import FileCleaner
from operations.file_operations import delete_files_batch
```

## Testing Checklist

When modifying structure:
- [ ] Run application to verify imports
- [ ] Check for linting errors
- [ ] Update `wow_cleanup_tool.spec` if modules added/moved
- [ ] Update this document
- [ ] Update `IMPLEMENTATION_ROADMAP.md` if relevant
- [ ] Test PyInstaller build: `pyinstaller wow_cleanup_tool.spec`
- [ ] Verify no __pycache__ committed to git
- [ ] Ensure all user-facing strings are localized and sorted
- [ ] Ensure all new/changed code is covered by isolated unit tests
