# WoW Cleanup Tool

Lightweight utility for managing and cleaning World of Warcraft installations.

## Features

- WoW detection with manual override; multi-flavor (Retail, Classic, Era, PTR, Beta)
- Modern UI (sv-ttk) with theme toggle, custom fonts, and 50ms resize debouncing
- Delete modes: recycle bin or permanent; respects user choice across tabs
- Folder Cleaner: cache/log/error cleanup plus screenshot viewer with select/unselect/remove
- File Cleaner: .bak/.old cleanup and AddOns.txt repair; background scanning
- Dual-channel logging with rotation, append mode, and centralized log controls
- Localization-first (100 keys, English default); full type hints; ruff + pytest coverage

## Quick Links

- [Project Structure](PROJECT_STRUCTURE.md)
- [Implementation Roadmap](IMPLEMENTATION_ROADMAP.md)
- [Code Documentation](CODE_DOCUMENTATION.md)
- [Logging Guide](LOGGING_GUIDE.md)
- [Background Tasks Guide](BACKGROUND_TASK_GUIDE.md)
- [Testing Guide](tests_README.md)
- [Type Hints & Tests Summary](TYPE_HINTS_AND_TESTS_SUMMARY.md)
- [Operations Module](../src/operations/README.md)
- GitHub CI: `.github/workflows/build-release.yml` (PyInstaller builds on tags)

## Installation

Requirements: Python 3.10+ on Windows/macOS/Linux.

Run from source:
```bash
git clone https://github.com/Myrroddin/wow-cleanup-tool.git
cd wow-cleanup-tool
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src/wow_cleanup_tool.py
```

Build executable:
```bash
python -m pip install -r requirements.txt
pyinstaller src/wow_cleanup_tool.spec
```
Output goes to `dist/` (platform-specific).

Dependencies: pinned in `requirements.txt`; bootstrap installs Pillow, send2trash, sv-ttk, darkdetect, orjson as needed.

## Usage

1. Accept GPL-3.0 license on first launch.
2. Let the app auto-detect WoW or browse manually.
3. Choose theme, font size, delete mode, and logging options.

- **Logs**: User Log (operations) and Developer Log (debug/errors) support copy/save/delete.
- **Screenshots**: Preview, expand, select/unselect all, and remove (trash or permanent).

## Development Notes

- Architecture overview: see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).
- Module-level details: see [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md).
- Roadmap/status: see [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md).

## License

GPL-3.0 — see [LICENSE](../LICENSE).
