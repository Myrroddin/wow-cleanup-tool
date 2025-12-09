# WoW Cleanup Tool

A lightweight utility for managing and optimizing World of Warcraft installations.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [License](#license)

---

## Features

### Available Now ✅
- **WoW Detection**: Automatic detection or manual path selection
- **Multi-Flavor Support**: Retail, Classic, Classic Era, PTR, Beta
- **Themes**: Light/dark mode with custom fonts (9-16pt)
- **Delete Modes**: Move to trash (safe) or permanent deletion
- **Logging**: 
  - Dual-channel logs (user operations + developer diagnostics)
  - Automatic rotation (1MB user, 5MB dev)
  - Session preservation with append mode
  - Thread-safe for parallel operations
- **Localization**: 97 translation keys, 13 language support structure
- **Settings**: Auto-save theme, font, delete mode, verbose logging, geometry

### Coming Soon 🚧
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
python wow_cleanup_tool.py
```
Dependencies install automatically on first run.

### Build Executable
```bash
pip install pyinstaller
pyinstaller wow_cleanup_tool.spec
```
Output: `dist/WoW Cleanup Tool.exe`

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
modules/
├── core/          # Settings, logging, themes
├── localization/  # Translations (97 keys)
├── ui/            # Interface components
├── wow/           # Path detection, validation
└── operations/    # Cleanup features (future)
```

**Testing**:
```bash
# Run all tests (45 tests, 100% passing)
python -m unittest discover tests/ -v

# Run specific suite
python -m unittest tests.test_path_manager
```

**Documentation**:
- [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) - Feature development guide
- [LOGGING_GUIDE.md](LOGGING_GUIDE.md) - Logging system details
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Module documentation

**Key Features**:
- Type hints for IDE support
- `os.scandir()` for performance
- Base classes for extensibility
- Parallel processing support

## License

GNU General Public License v3.0 - see [LICENSE](LICENSE)

**⚠️ Always backup your `AddOns` and `WTF` folders before using cleanup tools!**

---

**Support**: [GitHub Issues](https://github.com/Myrroddin/wow-cleanup-tool/issues) | [Discussions](https://github.com/Myrroddin/wow-cleanup-tool/discussions)
