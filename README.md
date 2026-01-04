
# WoW Cleanup Tool

A lightweight, modular utility for managing and optimizing World of Warcraft installations.

---

## Features

- 🎯 **Automatic WoW detection** or manual path selection with path caching (7-day TTL)
- 🎮 **Multi-flavor support**: Retail, Classic, Era, PTR, Beta
- 🎨 **Modern UI**: Windows 11-style theming with automatic OS theme detection
- 🌈 **Customizable appearance**: Light/dark themes, custom fonts (8–16pt, default 12)
- ⚙️ **Game Optimizer**: Scan system hardware (CPU, RAM, GPU) for performance recommendations
- 🗑️ **Safe deletion**: Move to trash or delete permanently (honored across tabs)
- 🧹 **Folder Cleaner**: Cache/log/error toggles plus screenshot viewer (preview, expand, select/unselect/remove)
- ✅ **File Cleaner**: Remove .bak/.old backups, orphaned SavedVariables, and clean AddOns.txt entries
- 📋 **Dual logging**: User log (append-aware) and developer log with rotation and centralized controls
- ⚡ **Performance**: sv-ttk UI, orjson (fast JSON), @lru_cache methods, parallel hardware detection, multi-tier caching:
  - In-Memory: Settings (10-100x faster), fonts (1-hour TTL)
  - Disk with TTL: Hardware info (30-day), WoW paths (7-day with validation)
  - Method-Level: @lru_cache on expensive flavor name translations
- 🔧 **Quality**: Full type hints, ruff/black clean, comprehensive test coverage

### Roadmap
- Release hardening and first tagged build


---

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
python -m pip install -r requirements.txt
pyinstaller src/wow_cleanup_tool.spec
```
Output: platform-specific binary under `dist/`.

### CI & Releases
- GitHub Actions workflow: `.github/workflows/build-release.yml` builds multi-platform artifacts on tags (`v*.*.*`).
- Local builds use the same `src/wow_cleanup_tool.spec` to match CI outputs.
- Report issues or request builds via [GitHub Issues](https://github.com/Myrroddin/wow-cleanup-tool/issues).

---

## Usage

1. **First run**: Accept license agreement
2. **Setup**: Auto-detect or browse for your WoW installation folder
3. **Configure**: Choose theme, font, delete mode, and logging preferences
4. **Monitor**: Use Log tabs to view activity and diagnostics (user log resets each launch unless append mode is enabled; developer log is always persisted with rotation)

---

## Documentation

📚 [Main Documentation](docs/README.md) - Overview and feature details
- [Code Documentation](docs/CODE_DOCUMENTATION.md) - Comprehensive module reference and API guide
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Directory organization and design principles
- [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md) - Current status and planned features
- [Testing Guide](docs/tests_README.md) - Running and writing tests
- [Type Hints & Tests Summary](docs/TYPE_HINTS_AND_TESTS_SUMMARY.md) - Type safety and test implementation details
- [Logging Guide](docs/LOGGING_GUIDE.md) - Logging system architecture and configuration
- [Background Tasks Guide](docs/BACKGROUND_TASK_GUIDE.md) - Threading model for scanning and deletion operations

---

## License

GNU General Public License v3.0 – see [LICENSE](LICENSE)

**⚠️ Always backup your `AddOns` and `WTF` folders before using cleanup tools!**

---

**Support:** [GitHub Issues](https://github.com/Myrroddin/wow-cleanup-tool/issues) | [Discussions](https://github.com/Myrroddin/wow-cleanup-tool/discussions)

