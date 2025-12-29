
# WoW Cleanup Tool

A lightweight, modular utility for managing and optimizing World of Warcraft installations.

---

## Features

- 🎯 **Automatic WoW detection** or manual path selection
- 🎮 **Multi-flavor support**: Retail, Classic, PTR, Beta
- 🎨 **Customizable UI**: Light/dark themes, custom fonts (9–16pt)
- 🗑️ **Safe deletion**: Move to trash or delete permanently
- 📋 **Dual logging system**: User activity log and developer diagnostics
- ⚙️ **Auto-save preferences**: Theme, font, delete mode, logging settings
- 🌍 **Cross-platform**: Windows, macOS, Linux

### Coming Soon
- File/folder cleanup (.bak, .old, cache, logs)
- Orphaned SavedVariables cleanup
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
python src/wow_cleanup_tool.py
```
*Dependencies install automatically on first run.*

### Build Executable
```bash
pip install pyinstaller
pyinstaller src/wow_cleanup_tool.spec
```
Output: `dist/WoW Cleanup Tool` (platform-specific executable)

---

## Usage

1. **First run**: Accept license agreement
2. **Setup**: Auto-detect or browse for your WoW installation folder
3. **Configure**: Choose theme, font, delete mode, and logging preferences
4. **Monitor**: Use Log tabs to view activity and diagnostics

---

## Documentation

📚 **For developers and contributors:**
- [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md) - Current status and planned features
- [Logging Guide](docs/LOGGING_GUIDE.md) - Logging system details
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Code organization
- [Testing Guide](docs/tests_README.md) - Running and writing tests

---

## License

GNU General Public License v3.0 – see [LICENSE](LICENSE)

**⚠️ Always backup your `AddOns` and `WTF` folders before using cleanup tools!**

---

**Support:** [GitHub Issues](https://github.com/Myrroddin/wow-cleanup-tool/issues) | [Discussions](https://github.com/Myrroddin/wow-cleanup-tool/discussions)

