
# WoW Cleanup Tool

A lightweight, modular utility for managing and optimizing World of Warcraft installations.

---

## Features

- 🎯 **Automatic WoW detection** or manual path selection
- 🎮 **Multi-flavor support**: Retail, Classic, PTR, Beta
- 🎨 **Customizable UI**: Light/dark themes, custom fonts (8–16pt, default 12)
- 🗑️ **Safe deletion**: Move to trash or delete permanently
- 📋 **Dual logging system**: User activity log and developer diagnostics (dev log always persisted; user log persisted when append mode is on)
- ⚙️ **Auto-save preferences**: Theme, font, delete mode, logging settings
- 🌍 **Cross-platform**: Windows, macOS, Linux
- ✅ **File Cleaner**: Scan and safely remove .bak/.old backup files and orphaned SavedVariables

### In Development
- Folder cleaner (cache, logs, screenshots, errors)
- Game optimizer & smart suggestions

---

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

---

## Usage

1. **First run**: Accept license agreement
2. **Setup**: Auto-detect or browse for your WoW installation folder
3. **Configure**: Choose theme, font, delete mode, and logging preferences
4. **Monitor**: Use Log tabs to view activity and diagnostics (user log resets each launch unless append mode is enabled; developer log is always persisted with rotation)

---

## Documentation

📚 **For developers and contributors:**
- [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md) - Current status and planned features
- [Testing Guide](docs/tests_README.md) - Running and writing tests
- [Type Hints & Tests Summary](docs/TYPE_HINTS_AND_TESTS_SUMMARY.md) - Type safety and test implementation details
- [Background Tasks Guide](docs/BACKGROUND_TASK_GUIDE.md) - Threading model for scanning and deletion operations
- [Logging Guide](docs/LOGGING_GUIDE.md) - Logging system architecture and configuration
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Code organization and module layout

---

## License

GNU General Public License v3.0 – see [LICENSE](LICENSE)

**⚠️ Always backup your `AddOns` and `WTF` folders before using cleanup tools!**

---

**Support:** [GitHub Issues](https://github.com/Myrroddin/wow-cleanup-tool/issues) | [Discussions](https://github.com/Myrroddin/wow-cleanup-tool/discussions)

