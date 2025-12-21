
# WoW Cleanup Tool

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
- Log and Developer tabs now feature a visible text area and log controls (Clear, Save, Copy), using a grid-based modular layout
- Centralized log controls utility (copy, save, clear, delete) for both logs
- Modular UI: each main tab and log tab is a separate class in `src/ui/tabs/`
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
4. Use Log and Developer tabs for activity and diagnostics. Both tabs now display logs in a text area with grid-based layout and log control buttons.

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
- [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md)
- [Logging Guide](docs/LOGGING_GUIDE.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)

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
Tests are isolated/mocked for file-based code. See `docs/tests_README.md` for details.

## License

GNU General Public License v3.0 – see [LICENSE](LICENSE)

**⚠️ Always backup your `AddOns` and `WTF` folders before using cleanup tools!**

---

**Support:** [GitHub Issues](https://github.com/Myrroddin/wow-cleanup-tool/issues) | [Discussions](https://github.com/Myrroddin/wow-cleanup-tool/discussions)
