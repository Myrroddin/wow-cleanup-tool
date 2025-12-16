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
│   │   └── en_us.py          # English translations (92 keys, organized by prefix)
│   ├── operations/           # File system operations (future cleanup features)
│   │   ├── base_scanner.py   # Base class for all scanners
│   │   ├── disk_utils.py     # HDD/SSD detection and optimization
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
│   └── wow_cleanup_tool.spec # PyInstaller build configuration
│
├── assets/
│   └── icons/                # Application icons
│       ├── wow_cleanup_icon.ico   # Windows icon
│       ├── wow_cleanup_icon.icns  # macOS icon
│       └── *.png                  # PNG icons
│
├── docs/                    # Documentation files
│   ├── README.md

# Project Structure

## Directory Organization

```
wow-cleanup-tool/
├── .github/                # GitHub configuration
│   ├── workflows/          # CI/CD workflows
│   │   └── build-release.yml
│   ├── ISSUE_TEMPLATE/     # Issue templates
│   └── FUNDING.yml         # Sponsorship info
│
├── src/                    # Main application source code
│   ├── core/               # Core infrastructure (settings, logging, themes)
│   ├── localization/       # Multi-language support (98+ keys)
│   ├── operations/         # File/folder cleanup, optimizer (future)
│   ├── ui/                 # User interface components
│   │   ├── dialogs/        # Dialog windows (license, warnings)
│   │   ├── tabs/           # Modular tab classes (FileCleanerTab, LogTab, etc.)
│   │   ├── widgets/        # Custom widgets (Tooltip, etc.)
│   │   ├── log_controls.py # Log controls utility (copy, save, clear, delete)
│   │   └── main_window.py  # Main window builder (delegates to tabs/utilities)
│   ├── wow/                # WoW-specific logic (path detection, validation)
│   └── wow_cleanup_tool.py # Main application entry point
│   └── wow_cleanup_tool.spec # PyInstaller build config
│
├── assets/
│   └── icons/              # Application icons
│
├── docs/                   # Documentation files
│   ├── README.md
│   ├── LOGGING_GUIDE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── TYPE_HINTS_AND_TESTS_SUMMARY.md
│   ├── IMPLEMENTATION_ROADMAP.md
│   └── tests_README.md
│
├── LICENSE                 # GPL-3.0 license
├── requirements.txt        # Python dependencies
└── tests/                  # Unit tests
```
- All dialogs are theme-aware and localized
- Use `BaseDialog` class for consistency
- **license_dialog.py**: GPL-3.0 license acceptance (first-run)
- **multiple_installations.py**: Warns about multiple WoW installations
- **wow_close_warning.py**: Warns if WoW is running (can be disabled)

### WoW (`src/wow/`)
World of Warcraft specific functionality:
- **game_optimizer.py**: Game configuration optimization features (future)
- **game_validation.py**: Installation structure validation utilities
- **path_handler.py**: WoW installation detection and user browsing
- **path_manager.py**: Installation validation, flavor detection, path utilities

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
- `os.scandir()` instead of `os.listdir()` (2-3x faster)
- Parallel processing with ThreadPoolExecutor
- Disk-aware threading (8 workers for SSD, 2 for HDD)
- Compiled regex patterns at module level

### 4. User Experience
- All user-facing text localized
- Theme-aware UI components
- Settings persistence across sessions
- Error handling with graceful degradation

### 5. Extensibility
- `BaseScanner` class for new cleanup features
- Plugin-ready localization system
- `BaseDialog` for new dialogs
- Operations module ready for future scanners

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
- **6-tab interface** in main window:
  - **Feature tabs** (File Cleaner, Folder Cleaner, Game Optimizer, Optimization Suggestions)
  - **Log tab**: User operations with Copy/Save/Delete buttons
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
from modules.core import Logger, load_settings, apply_theme
from modules.localization import Localization
from modules.ui import MainWindowBuilder, ApplicationController, setup_geometry
from modules.wow import PathManager, WoWPathHandler
```

### UI Components
```python
from ..core.themes import apply_theme
from ..localization import Localization
from .ui_constants import DialogDimensions
from .dialog_base import BaseDialog
```

### Future Operations
```python
from modules.operations import BaseScanner, get_optimal_workers
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
