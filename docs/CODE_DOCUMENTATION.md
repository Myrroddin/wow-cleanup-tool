"""WoW Cleanup Tool - Code Documentation

This document provides a comprehensive overview of all Python modules in the project,
explaining what each file does and how they work together.

**See also**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for directory organization and design principles.

## Table of Contents

- [Project Structure](#project-structure)
- [Main Application](#main-application-src)
- [Core Modules](#core-modules-srcccore)
- [Localization](#localization-srclocalization)
- [Operations](#operations-srcoperations)
- [UI Components](#ui-components-srcui)
- [WoW Integration](#wow-integration-srcwow)
- [Testing](#testing)

## Project Structure

```
src/
├── wow_cleanup_tool.py          # Main application entry point
├── core/                        # Core utilities and systems
├── localization/                # Translation files
├── operations/                  # File/folder scanning and cleanup
├── ui/                          # User interface components
└── wow/                         # WoW-specific path and detection logic

tests/                           # Unit tests for all modules
```

## Main Application (src/)

### wow_cleanup_tool.py
**Purpose**: Main application entry point that initializes and runs the WoW Cleanup Tool.

**Key Responsibilities**:
- Checks and installs required dependencies (Pillow, psutil, send2trash)
- Ensures only one instance runs at a time (prevents conflicts)
- Loads user settings and preferences
- Detects World of Warcraft installation path
- Shows license agreement and warnings on first run
- Builds and displays the main UI window
- Handles graceful shutdown and cleanup

**Startup Sequence**:
1. Dependency check and installation if needed
2. Single instance lock acquisition
3. Settings and localization loading
4. WoW path detection and validation
5. License agreement (first run only)
6. WoW close warning (if WoW is running)
7. Main window creation and display

## Core Modules (src/core/)

### logger.py
**Purpose**: Modern logging system using Python's built-in logging module.

**Features**:
- Dual logging: User-facing operations log + Developer debug/error log
- Automatic timestamps on all log entries
- Log file rotation to prevent excessive disk usage
- Thread-safe logging from background operations
- Real-time display in UI via TextWidgetHandler
- Persistent logging across sessions (optional)

**Key Classes**:
- `Logger`: Main logging coordinator
- `TextWidgetHandler`: Custom handler for Tkinter Text widgets
- `SessionSeparatorHandler`: Adds session markers in append mode

**See also**: [LOGGING_GUIDE.md](LOGGING_GUIDE.md) for detailed logging usage and patterns.

### settings.py
**Purpose**: Manages user preferences and application state.

**Storage Locations**:
- User settings: `~/.wow_cleanup_tool/settings.json` (per-user)
- WoW path cache: Shared location for all users (machine-wide)
- User log file: `~/.wow_cleanup_tool/user_log.txt` (if append mode enabled)

**Managed Settings**:
- Language preference
- Theme (light/dark)
- Font family and size
- Delete mode (trash vs permanent)
- Verbose logging toggle
- Window geometry (size, position)
- Dialog preferences (license acceptance, warnings)

### themes.py
**Purpose**: Provides light and dark color themes for the entire application.

**Features**:
- Comprehensive widget styling (buttons, labels, frames, etc.)
- Consistent colors across all UI elements
- Theme switching without restart
- Font-aware padding calculations
- Tooltip theming support

**Theme Data**:
- Background/foreground colors
- Button and entry field colors
- Selection highlights
- Frame and label frame styling
- Arrow colors for dropdowns

### error_handler.py
**Purpose**: Top-level error handler for uncaught exceptions.

**Features**:
- Graceful error handling when unexpected exceptions occur
- Displays error details to user
- Prints full traceback for debugging
- Waits for user input before exiting
- Works even if main UI fails to load

### background_task.py
**Purpose**: Execute long-running operations in background threads.

**Features**:
- Prevents UI freezing during I/O-heavy operations
- Thread-safe callbacks for completion and error handling
- Support for progress updates during long operations
- Automatic daemon threading (threads terminate with application)
- Safe UI updates via root.after() on main thread

**Key Methods**:
- `BackgroundTask.run()`: Execute task with completion callback
- `BackgroundTask.run_with_progress()`: Execute with progress updates

**See also**: [BACKGROUND_TASK_GUIDE.md](BACKGROUND_TASK_GUIDE.md) for usage patterns and best practices.

### bootstrap.py
**Purpose**: Ensures required Python packages are installed before startup.

**Dependencies Checked**:
- Pillow (PIL): Image handling for screenshot viewer
- psutil: Process detection (checking if WoW is running)
- send2trash: Safe file deletion (move to recycle bin)

### dependencies.py
**Purpose**: Handles automatic installation of missing dependencies.

**Features**:
- Checks for required packages (Pillow, psutil, send2trash)
- Parallel installation via ThreadPoolExecutor (up to 3 packages simultaneously)
- Thread-safe UI updates using queue-based communication
- 30-second timeout per package with --no-cache-dir flag
- Progress dialog with real-time package status
- User-friendly error messages if installation fails

### instance_utils.py / single_instance.py
**Purpose**: Prevents multiple instances of the application from running.

**Mechanism**:
- Creates lock file in temp directory
- Detects if another instance is already running
- Releases lock on clean shutdown
- Prevents file conflicts and confusion

## Localization (src/localization/)

### en_us.py
**Purpose**: English (US) translations for all UI strings.

**Contains**:
- Button labels
- Tab names
- Dialog messages
- Tooltips
- Log messages
- Error messages
- Status messages

**Translation Keys**: All strings are stored in TRANSLATIONS dictionary with
semantic keys (e.g., "btn_scan_files", "msg_log_empty")

### __init__.py (Localization class)
**Purpose**: Localization system that loads and manages translations.

**Features**:
- Language file loading
- Fallback to English if translation missing
- String formatting support for dynamic values
- Easy language switching

## Operations (src/operations/)

### base_scanner.py
**Purpose**: Base class for optimized parallel file scanning.

**Features**:
- Uses os.scandir (2-3x faster than os.walk)
- ThreadPoolExecutor for parallel scanning across game versions
- Efficient directory filtering during traversal
- Configurable worker count
- Safe symlink handling

### file_cleaner.py
**Purpose**: Scans for backup and old files (.bak, .old extensions).

**Features**:
- Inherits from BaseScanner for performance
- Recursive scanning of WoW version directories
- Skips irrelevant directories (cache, screenshots, data, etc.)
- Case-insensitive extension matching
- Batch file deletion with progress logging

### orphan_scanner.py
**Purpose**: Detects orphaned SavedVariables files from uninstalled AddOns.

**How It Works**:
1. Scans Interface/AddOns for currently installed AddOns
2. Scans WTF/Account/*/SavedVariables for .lua and .bak files
3. Identifies files that don't have corresponding AddOns
4. Protects critical Blizzard_.lua files (game-required)

**Directory Structure Handled**:
- Account-level SavedVariables (apply to all characters)
- Realm-level SavedVariables (per-realm settings)
- Character-level SavedVariables

### file_operations.py
**Purpose**: Safe file deletion utilities.

**Features**:
- Move to trash (Windows Recycle Bin) or permanent deletion
- Batch deletion with progress tracking
- Error handling for locked/in-use files
- Logging of all deletion operations
- Size calculations for freed disk space

## WoW Detection (src/wow/)

### path_manager.py
**Purpose**: Detects and manages World of Warcraft installation paths.

**Detection Methods**:
1. Windows Registry lookups (if on Windows)
2. Common installation paths (C:, D:, E:, F: drives)
3. Flavor directory detection (_retail_, _classic_, etc.)
4. Installation validation (checking for valid game files/folders)

**Flavor Support**:
- Retail (live game)
- PTR (Public Test Realm)
- Beta
- Classic
- Classic PTR/Beta
- Classic Era
- Classic Era PTR

### path_handler.py
**Purpose**: Interactive WoW path selection and validation UI.

**Features**:
- Dialog for browsing/selecting WoW folder
- Real-time path validation
- Multiple installation detection
- User confirmation for path selection
- Persistent path caching

## UI Components (src/ui/)

### main_window.py
**Purpose**: Builds the main application window with all tabs and controls.

**Structure**:
- Top control bar (WoW path, theme toggle, settings)
- Bug report button using 🐞 emoji (auto-scales with font)
- Notebook with 6 tabs (File Cleaner, Folder Cleaner, Game Optimizer, User Log, Developer Log)
- 200ms tab tooltip debouncing to prevent flicker
- Minimal update_idletasks calls for performance
- Settings persistence for window geometry
- Integration with logging system

### app_controller.py
**Purpose**: Coordinates actions between UI components and backend operations.

**Responsibilities**:
- Scan file/folder operations
- Delete selected items
- Update UI based on scan results
- Toggle selections
- Theme switching
- Settings updates

### Tabs (src/ui/tabs/)

#### file_cleaner_tab.py
**Purpose**: UI for scanning and removing .bak/.old files.

**Features**:
- Treeview showing found files with sizes
- Select all/unselect all toggle
- Per-file selection checkboxes
- Background scanning (non-blocking)
- 50ms Configure event debouncing for smooth resizing
- Dynamic wraplength based on widget width
- Size totals

#### folder_cleaner_tab.py
**Purpose**: UI for managing Cache, Errors, Logs, Screenshots folders.

**Features**:
- Sub-tabs for each WoW version (Retail, Classic, etc.)
- Checkboxes for each folder type
- Warning tooltip for Cache folder
- Screenshot browser with cached PIL Image objects
- Image.thumbnail() with LANCZOS resampling for efficient previews
- 50ms Configure event debouncing for smooth resizing
- Dynamic wraplength based on widget width
- Click preview to open full-size viewer (50% screen size)

#### game_optimizer_tab.py
**Purpose**: Reserved for future game optimization features.

#### log_tab.py / developer_tab.py
**Purpose**: Display user-facing and developer logs.

**Features**:
- Real-time log display
- Clear log button
- Copy to clipboard
- Open log folder
- Delete persistent log (log_tab only, append-mode aware)
- Timestamp toggle
- 50ms Configure event debouncing for smooth resizing
- Dynamic wraplength based on widget width

### Dialogs (src/ui/dialogs/)

#### license_dialog.py
**Purpose**: Shows GPL license agreement on first run.

#### wow_close_warning.py
**Purpose**: Warns user if WoW is running (prevents file conflicts).

#### multiple_installations.py
**Purpose**: Handles detection of multiple WoW installations.

#### screenshot_viewer.py
**Purpose**: Popup window for viewing screenshots at larger size.

**Features**:
- Displays image at 25% of screen size
- Centered on screen
- Theme-aware background
- Close via click, ESC key, or window X button

### Widgets (src/ui/widgets/)

#### tooltip.py
**Purpose**: Themed tooltips for UI elements.

**Features**:
- Fixed TkFixedFont 10pt for consistency
- Theme-aware colors (background, foreground, border)
- Smart boundary detection (280px wraplength)
- Automatic positioning to avoid screen edges
- Delay before showing (200ms for tab tooltips)

### Utility Modules (src/ui/)

#### geometry.py
**Purpose**: Window sizing, positioning, and persistence.

#### font_utils.py
**Purpose**: System font detection and management.

#### log_controls.py
**Purpose**: Log manipulation functions (clear, copy, delete).

#### ui_constants.py
**Purpose**: UI dimensions, spacing, font sizes.

#### text_widget_handler.py
**Purpose**: Text widget utilities for log display.

#### custom_tabbar.py
**Purpose**: Custom styling for tab widgets.

#### dialog_base.py
**Purpose**: Base class for consistent dialog creation.

## Testing (tests/)

All modules have corresponding test files that verify functionality:
- Mocked Tkinter widgets for UI testing
- File operation testing with temporary directories
- Settings persistence testing
- Theme application testing
- Localization testing
- Path detection testing

## Key Design Patterns

1. **Separation of Concerns**: UI, business logic, and data are separate
2. **Background Threading**: Long operations don't block UI
3. **EAFP (Easier to Ask Forgiveness than Permission)**: Try/except over checks
4. **Dependency Injection**: Components receive dependencies rather than creating them
5. **Settings Persistence**: User preferences saved across sessions
6. **Localization**: All user-facing strings are translatable
7. **Theme System**: Consistent styling across entire application
8. **Logging**: Comprehensive logging for debugging and user feedback

## File Safety

The application prioritizes file safety:
- Default: Move to trash (reversible)
- Optional: Permanent deletion
- Confirmation before bulk operations
- Protection of critical Blizzard files
- Warning if WoW is running
- Detailed logging of all operations

## Performance Optimizations

- os.scandir instead of os.walk (2-3x faster)
- ThreadPoolExecutor for parallel scanning and dependency installation
- Directory filtering during traversal (skip irrelevant folders)
- Configure event debouncing (50ms) to reduce layout calculations
- Screenshot caching with PIL Image.thumbnail() and LANCZOS resampling
- Tab tooltip debouncing (200ms) to prevent Toplevel creation churn
- Emoji icons instead of PNG for auto-scaling without image loading
- Thread-safe queue-based communication for parallel operations
- Reduced update_idletasks calls in main window
- Lazy loading of UI components
- Background threading for I/O operations

## Error Handling

- Top-level exception handler
- Per-operation error logging
- User-friendly error messages
- Graceful degradation (app works even if optional features fail)
- Detailed error logs for bug reports

---

**Related Documentation**:
- [tests_README.md](tests_README.md) - Unit test suite and coverage
- [TYPE_HINTS_AND_TESTS_SUMMARY.md](TYPE_HINTS_AND_TESTS_SUMMARY.md) - Type hints and testing details
- [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) - Development roadmap and guidelines

"""