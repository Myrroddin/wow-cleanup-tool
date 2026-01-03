# WoW Cleanup Tool

A lightweight utility for managing and optimizing World of Warcraft installations.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

---

## Features

### Available Now ✅
- **WoW Detection**: Automatic detection or manual path selection
- **Multi-Flavor Support**: Retail, Classic, Classic Era, PTR, Beta
- **Themes**: Light/dark mode with custom fonts (8–16pt, default 12)
- **Delete Modes**: Move to trash (safe) or permanent deletion
- **Logging**:
  - Dual-channel logs (user operations + developer diagnostics)
  - Automatic rotation (1MB user, 5MB dev)
  - Session preservation with append mode (user log); dev log always persisted
  - Thread-safe for parallel operations
- **Localization**: 98+ translation keys, robust English support, easy expansion
- **Settings**: Auto-save theme, font, delete mode, verbose logging, geometry
- **Chat Timestamps**: Toggle timestamps in both User Log and Developer Log
- **Modular UI**: Each main tab (File Cleaner, Folder Cleaner, Game Optimizer, Log, Developer) is implemented as a separate class in `src/ui/tabs/`
- **Log Controls Utility**: All log actions (copy, save, clear, delete) are handled by `src/ui/log_controls.py` for both user and developer logs
- **Custom Widgets**: Tooltip and future widgets are in `src/ui/widgets/`
- **Main Window Refactor**: `main_window.py` delegates tab UI and log actions to dedicated modules, improving maintainability and testability
- **Screenshot Viewer**: 
  - Dynamic preview panel below screenshot list
  - Click-to-expand 50% screen popup viewer
  - Help text with interaction instructions
  - ESC/click-outside to close popup
- **GameVersion Architecture**: Centralized game version management via immutable `GameVersion` class for type-safe version handling

### Coming Soon 🛠️
- File cleanup (.bak, .old, temps)
- Folder cleanup (cache, logs, errors)
- Game optimizer
- Smart optimization suggestions

## Installation

### Requirements
- Python 3.8+
- Windows, macOS, or Linux

### Run from Source
```bash
git clone https://github.com/Myrroddin/wow-cleanup-tool.git
cd wow-cleanup-tool
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src/wow_cleanup_tool.py
```

### Build Executable
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pyinstaller src/wow_cleanup_tool.spec
```
Output: `dist/WoW Cleanup Tool` (platform-specific executable)

## Usage

**First Run**:
1. Accept GPL-3.0 license
2. Auto-detect WoW path (or browse manually)
3. Configure preferences

**Settings**:
- **Theme**: Light/dark toggle
- **Font**: System font + size
- **Delete Mode**: Trash (safe) or permanent
- **Verbose Logging**: Detailed operations
- **Append Log**: Preserve across sessions

**Logs**:
- **Log Tab**: User operations (copy/save/delete)
- **Developer Tab**: Debug/error messages with color coding

## Development

**Structure**:
```
src/
├── core/          # Settings, logging, themes
├── localization/  # Translations (98+ keys)
├── operations/    # Cleanup features
├── ui/            # Interface components
│   ├── dialogs/   # Dialog windows
│   ├── tabs/      # Modular tab classes (FileCleanerTab, LogTab, etc.)
│   ├── widgets/   # Custom widgets (Tooltip, ScreenshotViewer, etc.)
│   ├── log_controls.py  # Log controls utility
│   └── main_window.py   # Main window builder (delegates to tabs/utilities)
├── wow/           # Path detection, validation, version management
└── tests/         # 151+ comprehensive unit tests
```

**Running Tests**:
```bash
pytest --maxfail=1 --disable-warnings
```

## Documentation

**For Code Understanding**:
- [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) — Detailed module reference with TOC
  - Main application entry point
  - Core utilities (logger, settings, themes)
  - Localization and operations
  - UI components and WoW integration
  
**For Development**:
- [TYPE_HINTS_AND_TESTS_SUMMARY.md](TYPE_HINTS_AND_TESTS_SUMMARY.md) — Type hints and testing strategy with TOC
  - Type hints coverage across all modules
  - Unit test details (151 tests, 98%+ coverage)
  - Test coverage breakdown by module

**For Project Planning**:
- [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) — Features and progress tracking
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — Architecture overview
- [LOGGING_GUIDE.md](LOGGING_GUIDE.md) — Logging system details
- [BACKGROUND_TASK_GUIDE.md](BACKGROUND_TASK_GUIDE.md) — Threading and async patterns
- [tests_README.md](tests_README.md) — Test execution and writing

## Recent Updates (January 3, 2026)

### New Features
- **GameVersion Class**: Centralized game version representation (`src/wow/version_manager.py`)
  - Type-safe version handling across tabs
  - Immutable attributes (flavor_dir, display_name, path)
  - Conversion methods (from_tuple, to_tuple)
  
- **Screenshot Interaction Instructions**: Localized help text (`desc_screenshot_interaction`)
  - Displayed above preview pane
  - Clear click-to-preview, click-to-expand instructions
  
- **Larger Screenshot Popup**: Increased from 25% to 50% of screen size
  - Better visibility while remaining centered
  - Aspect ratio preserved

### Improvements
- FolderCleanerTab refactored to use GameVersion objects
- Fixed screenshot popup click handler
- Updated PathManager.validate_installation() to return GameVersion list
- Improved test coverage for new GameVersion functionality

---

## License

GPL-3.0 - See [LICENSE](../LICENSE) for details

A lightweight, modular utility for managing and optimizing World of Warcraft installations.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [License](#license)

---

## Features

### Available Now
- Automatic WoW detection or manual path selection
- Multi-flavor support: Retail, Classic, PTR, Beta
- Light/dark themes, custom fonts (9–16pt)
- Safe delete (trash) or permanent deletion
- Dual logs: user actions & developer diagnostics (append mode, rotation)
- Centralized log controls utility (copy, save, clear, delete)
- Modular UI: each main tab is a separate class
- 98+ translation keys, easy localization (sorted, robust fallback)
- Auto-save for theme, font, delete mode, logging, geometry
- Custom widgets (e.g., tooltip)
- Settings and logs are per-user, cross-platform

### Planned
- File/folder cleanup (.bak, .old, cache, logs)
- Game optimizer & smart suggestions

## Installation

**Requirements:**
- Python 3.8+
- Windows, macOS, or Linux

**Run from source:**
```bash
git clone https://github.com/Myrroddin/wow-cleanup-tool.git
cd wow-cleanup-tool
python src/wow_cleanup_tool.py
```
Dependencies install automatically on first run.

**Build executable:**
```bash
pip install pyinstaller
pyinstaller src/wow_cleanup_tool.spec
```
Output: `dist/WoW Cleanup Tool.exe`

## Usage

1. Accept license on first run
2. Auto-detect or browse for WoW path
3. Configure preferences (theme, font, delete mode, logging)
4. Use Log and Developer tabs for activity and diagnostics

## Development

**Structure:**
```
src/
├── core/          # Settings, logging, themes
├── localization/  # Translations (sorted keys)
├── operations/    # Cleanup features (future)
├── ui/            # Interface components
│   ├── dialogs/   # Dialog windows
│   ├── tabs/      # Modular tab classes
│   ├── widgets/   # Custom widgets
│   ├── log_controls.py  # Log controls utility
│   └── main_window.py   # Main window builder
├── wow/           # Path detection, validation
└── wow_cleanup_tool.py  # Main application entry point
assets/
└── icons/         # Application icons
docs/              # Documentation
tests/             # Unit tests
```

**Docs:**
- [Implementation Roadmap](IMPLEMENTATION_ROADMAP.md)
- [Logging Guide](LOGGING_GUIDE.md)
- [Project Structure](PROJECT_STRUCTURE.md)

**Other highlights:**
- Type hints throughout
- Fast file scanning with `os.scandir()`
- Extensible base classes
- Parallel processing support

## Testing

Run all tests:
```bash
python -m unittest discover tests/ -v
```
Run a specific suite:
```bash
python -m unittest tests.test_path_manager
```
Tests are isolated/mocked for file-based code. See `tests_README.md` for details.

## License

GNU General Public License v3.0 – see [LICENSE](LICENSE)

**⚠️ Always backup your `AddOns` and `WTF` folders before using cleanup tools!**

---

**Support:** [GitHub Issues](https://github.com/Myrroddin/wow-cleanup-tool/issues) | [Discussions](https://github.com/Myrroddin/wow-cleanup-tool/discussions)
```bash
# Run all tests (45 tests, 100% passing)
python -m unittest discover tests/ -v

# Run specific suite
python -m unittest tests.test_path_manager
```bash
git clone https://github.com/Myrroddin/wow-cleanup-tool.git
cd wow-cleanup-tool
python src/wow_cleanup_tool.py
```
Dependencies install automatically on first run.

### Build Executable
```bash
pip install pyinstaller
pyinstaller src/wow_cleanup_tool.spec
```
Output: `dist/WoW Cleanup Tool.exe`
## License

GNU General Public License v3.0 - see [LICENSE](LICENSE)

**⚠️ Always backup your `AddOns` and `WTF` folders before using cleanup tools!**

---

**Support**: [GitHub Issues](https://github.com/Myrroddin/wow-cleanup-tool/issues) | [Discussions](https://github.com/Myrroddin/wow-cleanup-tool/discussions)
