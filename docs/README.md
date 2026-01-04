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
- **Modern UI**: Windows 11-style theming with sv-ttk
- **Themes**: Light/dark mode with automatic OS theme detection (first launch)
- **Customization**: Custom fonts (8–16pt, default 12), theme toggle button
- **Delete Modes**: Move to trash (safe) or permanent deletion
- **Logging**:
  - Dual-channel logs (user operations + developer diagnostics)
  - Automatic rotation, thread-safe for parallel operations
  - Session preservation with append mode
- **Performance**: Fast JSON serialization (orjson) and result caching (lru_cache)
- **Localization**: 98+ translation keys, robust English support, easy expansion
- **Settings**: Auto-save theme, font, delete mode, verbose logging, geometry
- **Chat Timestamps**: Toggle timestamps in both User Log and Developer Log
- **Modular UI**: Tab-based architecture with centralized log controls
- **Screenshot Viewer**: 
  - Dynamic preview with click-to-expand popup (50% screen)
  - Cached images for instant re-selection

### Coming Soon 🛠️
- File/folder cleanup (.bak, .old, cache, logs, errors, screenshots)
- Game optimizer with smart suggestions

## Installation

### Requirements
- Python 3.10+
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
- Theme (light/dark), font (system + size), delete mode (trash/permanent)
- Verbose logging, append log (preserve sessions)

**Logs**:
- **User Log**: Operations log (copy/save/delete)
- **Developer Log**: Debug/error messages with color coding

## Development

**Structure**:
```
src/
├── core/          # Settings, logging, themes, dependencies
├── localization/  # Translations (98+ keys)
├── operations/    # File/folder scanning and cleanup
├── ui/            # Interface components
│   ├── dialogs/   # Dialog windows
│   ├── tabs/      # Modular tab classes
│   ├── widgets/   # Custom widgets (Tooltip)
│   └── main_window.py   # Main window builder
└── wow/           # Path detection, validation, version management
```

**Key Features**:
- Type hints throughout
- Fast scanning with `os.scandir()` and parallel processing
- Configure event debouncing for smooth UI resizing
- Thread-safe queue-based communication for background tasks

## Documentation

- [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) — Detailed module reference
- [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) — Features and progress
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — Architecture overview
- [LOGGING_GUIDE.md](LOGGING_GUIDE.md) — Logging system details
- [TYPE_HINTS_AND_TESTS_SUMMARY.md](TYPE_HINTS_AND_TESTS_SUMMARY.md) — Type hints and testing
- [BACKGROUND_TASK_GUIDE.md](BACKGROUND_TASK_GUIDE.md) — Threading patterns
- [tests_README.md](tests_README.md) — Test execution guide

## Recent Updates (January 3, 2026)

### Performance Optimizations
- **Configure Event Debouncing**: 50ms debounce on all tabs prevents layout calculation churn during window resizing
- **Screenshot Caching**: PIL Image caching with thumbnail() and LANCZOS resampling for instant re-selection
- **Tab Tooltip Debouncing**: 200ms debounce eliminates Motion event Toplevel creation overhead
- **Emoji Icons**: Bug report button uses 🐞 emoji (auto-scales with font, no PNG loading)
- **Parallel Dependencies**: ThreadPoolExecutor with queue-based thread-safe UI updates (3 workers, 30s timeout)
- **Fixed Tooltips**: TkFixedFont 10pt with smart boundary detection (280px wraplength)
- **Minimal UI Updates**: Reduced update_idletasks calls in main window

### New Features
- **GameVersion Class**: Centralized game version representation (`src/wow/version_manager.py`)
  - Type-safe version handling across tabs
  - Immutable attributes (flavor_dir, display_name, path)
  - Conversion methods (from_tuple, to_tuple)
  
- **Screenshot Interaction**: Localized help text (`desc_screenshot_interaction`)
  - Click to preview, click preview to expand (50% screen size)
  - ESC or click-outside to close popup

### Improvements
- FolderCleanerTab refactored to use GameVersion objects
- PathManager.validate_installation() returns GameVersion list
- All tabs use dynamic wraplength based on widget width
- Comprehensive test coverage for GameVersion functionality

---

## License

GPL-3.0 - See [LICENSE](../LICENSE) for details
