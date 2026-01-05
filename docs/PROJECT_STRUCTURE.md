# Project Structure

## Directory Map

```
  wow-cleanup-tool/
  ├── .github/                 # CI/CD and issue templates
  ├── assets/icons/            # Application icons
  ├── docs/                    # Documentation set
  ├── src/                     # Application code
  │   ├── core/                # Settings, logging, theming, deps, caching, background tasks
  │   ├── localization/        # Translation keys (English default)
  │   ├── operations/          # File/folder scanning, hardware detection, delete helpers
  │   ├── ui/                  # Main window, tabs, dialogs, widgets, font utilities
  │   ├── wow/                 # WoW path detection, caching, version metadata
  │   ├── wow_cleanup_tool.py  # Entry point
  │   └── wow_cleanup_tool.spec# PyInstaller config
  ├── tests/                   # Unit tests (pytest framework)
  ├── LICENSE | README.md | requirements.txt
```

## Design Principles

- **Separation**: core infra, operations logic, WoW detection, UI layers.
- **Modularity**: clear import flow (core → localization/operations/wow → ui → main), single responsibility per module.
- **Caching Strategy**: Multi-tiered caching with TTL
  - In-memory: Settings, fonts (1-hour TTL)
  - Disk with TTL: Hardware (30-day), WoW paths (7-day)
  - Method-level: `@lru_cache` on expensive computations
- **Performance**: `os.scandir()` for I/O, ThreadPoolExecutor for scanning/installs/hardware detection, parallel GPU detection, 50ms UI debounce, LANCZOS screenshot caching, queue-driven UI updates.
- **UX**: localized text with fallback, theme-aware UI, persistent settings, delete-mode awareness across tabs.
- **Extensibility**: BaseScanner for new cleaners, batch file operations, themed dialogs/widgets, translation audit tooling.

## Build & Automation

- PyInstaller: builds standalone executables with platform icons and hidden imports for all new modules.
- GitHub Actions: releases on tags (`.github/workflows/build-release.yml`) for Windows/macOS/Linux.
- Dependencies: pinned in `requirements.txt`; runtime bootstrap installs Pillow, send2trash, sv-ttk, darkdetect, orjson, psutil, GPUtil, py-cpuinfo when missing.

## Data & Caching

- **Settings**: `~/.wow_cleanup_tool/settings.json` (theme, font, language, geometry, delete mode, verbose/append) with in-memory cache.
- **Hardware Cache**: `~/.wow_cleanup_tool/hardware_cache.json` (CPU, RAM, GPU info) with 30-day TTL.
- **WoW Path Cache**: `~/.wow_cleanup_tool/path_cache.json` (detected installation path) with 7-day TTL and path validation.
- **Logs**: `~/.wow_cleanup_tool/user_log.txt` (append optional) and dev log with rotation.
- **Font Cache**: In-memory system fonts list with 1-hour TTL and manual invalidation support.
- **Tabs**: File Cleaner, Folder Cleaner, Game Optimizer (with hardware scanning), User Log, Developer Log; log controls respect append and delete mode.

## Quick Import Guide

- Main startup: `Logger`, `load_settings`, `Localization`, `MainWindow`, `PathManager`.
- Caching: `timed_cache`, `SettingsCache`, `HardwareScanner`, `invalidate_settings_cache`. (Path caching handled by `settings.py`)
- UI helpers: `apply_theme`, `DialogDimensions`, `BaseDialog`, `get_available_fonts`, `invalidate_font_cache`.
- Operations: `BaseScanner`, `FileCleaner`, `HardwareScanner`, `delete_files_batch`.

## Testing Checklist

- [ ] Run application to verify imports
- [ ] Check linting errors (ruff)
- [ ] Update `wow_cleanup_tool.spec` if modules added/moved
- [ ] Update this document and `IMPLEMENTATION_ROADMAP.md`
- [ ] Test PyInstaller build: `pyinstaller src/wow_cleanup_tool.spec`
- [ ] Ensure localization keys are sorted and covered
- [ ] Add/adjust unit tests for new code

---

Related docs: [CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md) · [LOGGING_GUIDE.md](LOGGING_GUIDE.md) · [BACKGROUND_TASK_GUIDE.md](BACKGROUND_TASK_GUIDE.md) · [tests_README.md](tests_README.md) · [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)
