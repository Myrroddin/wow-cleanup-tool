# Project Structure

## Directory Map

```
wow-cleanup-tool/
├── .github/                 # CI/CD and issue templates
├── assets/icons/            # Application icons
├── docs/                    # Documentation set
├── src/                     # Application code
│   ├── core/                # Settings, logging, theming, deps, background tasks
│   ├── localization/        # Translation keys (English default)
│   ├── operations/          # File/folder scanning and delete helpers
│   ├── ui/                  # Main window, tabs, dialogs, widgets
│   ├── wow/                 # WoW path detection and version metadata
│   ├── wow_cleanup_tool.py  # Entry point
│   └── wow_cleanup_tool.spec# PyInstaller config
├── tests/                   # Unit tests (~194 collected; 192 pass, 2 skip)
├── tools/                   # Dev utilities (i18n audit)
├── LICENSE | README.md | requirements.txt | test_results.txt
```

## Design Principles

- Separation: core infra, operations logic, WoW detection, UI layers.
- Modularity: clear import flow (core → localization/operations/wow → ui → main), single responsibility per module.
- Performance: `os.scandir()` for I/O, ThreadPoolExecutor for scanning/installs, 50ms UI debounce, LANCZOS screenshot caching, queue-driven UI updates.
- UX: localized text with fallback, theme-aware UI, persistent settings, delete-mode awareness across tabs.
- Extensibility: BaseScanner for new cleaners, batch file operations, themed dialogs/widgets, translation audit tooling.

## Build & Automation

- PyInstaller: builds standalone executables with platform icons and hidden imports.
- GitHub Actions: releases on tags (`.github/workflows/build-release.yml`) for Windows/macOS/Linux.
- Dependencies: pinned in `requirements.txt`; runtime bootstrap installs Pillow, send2trash, sv-ttk, darkdetect, orjson when missing.

## Data & Logging

- Settings: `~/.wow_cleanup_tool/settings.json` (theme, font, language, geometry, delete mode, verbose/append).
- WoW cache: `<WoW_Install>/.wow_cleanup_cache.json` (per-install path cache).
- Logs: `~/.wow_cleanup_tool/user_log.txt` (append optional) and dev log with rotation.
- Tabs: File Cleaner, Folder Cleaner, Game Optimizer (placeholder), User Log, Developer Log; log controls respect append and delete mode.

## Quick Import Guide

- Main startup: `Logger`, `load_settings`, `Localization`, `MainWindow`, `PathManager`.
- UI helpers: `apply_theme`, `DialogDimensions`, `BaseDialog`.
- Operations: `BaseScanner`, `FileCleaner`, `delete_files_batch`.

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
