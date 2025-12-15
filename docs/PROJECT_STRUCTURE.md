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
│   ├── LOGGING_GUIDE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── TYPE_HINTS_AND_TESTS_SUMMARY.md
│   ├── IMPLEMENTATION_ROADMAP.md
│   └── tests_README.md
│
├── LICENSE                  # GPL-3.0 license
├── requirements.txt         # Python dependencies
└── tests/                   # Unit tests
```

## Module Responsibilities

### Core (`src/core/`)
System-level infrastructure and configuration:
- **dependencies.py**: Checks and installs required Python packages
- **geometry.py**: Window sizing, positioning, and screen calculations
- **global_settings.py**: Application-wide constants and default values
- **logger.py**: Dual-channel logging system with session persistence
  - `.log()`: Essential user messages → Log tab
  - `.verbose()`: Detailed operations (if verbose enabled) → Log tab
  - `.debug()`: Technical details → Developer tab (blue)
  - `.error()`: Errors and exceptions → Developer tab (red, badge)
  - Session separators in append mode (newest-first ordering)
  - Persistent log storage: `~/.wow_cleanup_tool/user_log.txt`
- **settings.py**: Per-user settings + WoW path caching + log persistence
  - Includes: theme, font, delete_mode, verbose_logging, append_log, geometry
- **single_instance.py**: Prevents multiple app instances
- **themes.py**: Light/dark theme management with tab spacing

### Localization (`src/localization/`)
Multi-language support system with organized key naming:
- **__init__.py**: `Localization` class with translation lookup
- **en_us.py**: English (US) translations dictionary (92 keys, organized by prefix):
  - `btn_*`: Button labels (6 keys)
  - `label_*`: UI field labels (8 keys)
  - `status_*`: Status messages (8 keys)
  - `msg_*`: Dialog messages (6 keys)
  - `title_*`: Window/dialog titles (7 keys)
  - `tab_*`: Tab names (6 keys)
  - `option_*`: Checkbox/radio options (5 keys)
  - `version_*`: Version types (3 keys)
  - Plus: `dep_*`, `error_*`, `file_*`, `log_*`, `wow_*` prefixes
  - All keys alphabetically sorted for easy maintenance

### Operations (`src/operations/`)
Backend file system operations (optimized with `os.scandir()` and parallel processing):
- **base_scanner.py**: Base class for all scanners with ThreadPoolExecutor
- **disk_utils.py**: HDD/SSD detection, optimal worker thread calculation
- **README.md**: Performance documentation and usage patterns

**Future modules** (see `IMPLEMENTATION_ROADMAP.md`):
- file_scanner.py, folder_scanner.py, orphan_scanner.py, file_operations.py

### UI (`src/ui/`)
User interface components (theme-aware, localized):
- **app_controller.py**: Event handlers and UI state management
  - Handles: theme toggle, font changes, delete mode, verbose logging, append log
  - Dynamic button visibility control (delete log button)
- **dialog_base.py**: Base class for consistent theme-aware dialog creation
- **font_utils.py**: System font detection and utilities
- **geometry.py**: Window geometry calculations and constraints
- **main_window.py**: Main window construction with 6-tab interface
  - Tabs: File Cleaner, Folder Cleaner, Game Optimizer, Optimization Suggestions, Log, Developer
  - Log tab: Copy, Save, Delete buttons (delete visible only in append mode)
  - Developer tab: Copy/Save buttons, error badge, color-coded messages
  - Session separators with timestamp in append mode
- **ui_constants.py**: Standard dimensions and styling values

**Dialogs** (`src/ui/dialogs/`):
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
