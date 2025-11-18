# WoW Cleanup Tool

A comprehensive maintenance and optimization suite for World of Warcraft, helping you clean up unnecessary files, manage addons, and optimize game performance across all WoW versions (Retail, Classic, Classic Era, PTR, and Beta).

## Table of Contents

- [Features](#features)
  - [File Cleaner](#️-file-cleaner)
  - [Folder Cleaner](#-folder-cleaner)
  - [Orphan Cleaner](#-orphan-cleaner)
  - [Game Optimizer](#️-game-optimizer)
  - [Optimization Suggestions](#-optimization-suggestions)
  - [Additional Features](#-additional-features)
- [Screenshots](#screenshots)
- [Safety Precautions](#safety-precautions)
- [Installation & Usage](#installation--usage)
  - [Requirements](#requirements)
  - [Running the Tool](#running-the-tool)
  - [First-Time Setup](#first-time-setup)
  - [Using Each Tool](#using-each-tool)
- [Technical Information](#technical-information)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Bug Reports & Feature Requests](#bug-reports--feature-requests)
- [Support](#support)
- [Documentation](#documentation)
- [Known Limitations](#known-limitations)
- [License](#license)

## Features

### 🗂️ File Cleaner
Scans and removes backup files (`.bak` and `.old`) that accumulate from WoW updates and addon installations. Multi-threaded scanning with selective deletion and safe deletion options (Recycle Bin or permanent).

### 📁 Folder Cleaner
Safely removes temporary folders (Logs, Errors, Screenshots) that consume disk space. Per-version tabs with folder size display and screenshot preview support (click preview to enlarge). Individual screenshot files can be selectively deleted, and the Screenshots folder is automatically removed when all screenshot images are deleted.

### 🧹 Orphan Cleaner
Detects and removes SavedVariables files for uninstalled addons. Scans all levels (Account, Realm, Character) with smart detection that preserves Blizzard core files. Includes AddOns.txt rebuilding.

### ⚙️ Game Optimizer
Hardware-based graphics preset recommendations with automatic GPU selection. Cross-platform hardware detection, intelligent presets (Low/Medium/High/Ultra), and one-click application to Config.wtf.

### 💡 Optimization Suggestions
Manual optimization tips including: Clean Game Data Folder, Reinstall WoW (Clean Install), Enable HDR, Verify Monitor Refresh Rate, Enable Smart Access Memory/Resizable BAR, and Enable XMP Memory Profile. Each with detailed tooltips explaining benefits, risks, and instructions.

### 📊 Additional Features
- **12 Languages**: Full translation in all 11 WoW languages plus Ukrainian
- **Themes**: Light and dark modes with customizable fonts
- **Update Checker**: Automatic GitHub release checking
- **Multi-version Support**: Retail, Classic, Classic Era, PTR, Beta

## Screenshots

![File Cleaner](https://github.com/user-attachments/assets/2b2680d7-d7c0-4007-b5ad-3e03247f6ff4)
![Folder Cleaner](https://github.com/user-attachments/assets/5da620f1-e3e8-4ff9-abe9-4e85117a07ed)
![Orphan Cleaner](https://github.com/user-attachments/assets/e33a7e8e-d217-4f13-9b8b-c3c66f8015f0)
![Game Optimizer](https://github.com/user-attachments/assets/d9b031de-d4c6-4326-a26f-cf9ac7a61ac9)
![Optimization Suggestions](https://github.com/user-attachments/assets/optimization-suggestions-screenshot)

*Note: Optimization Suggestions screenshot placeholder - actual screenshot to be added*

## Safety Precautions

**⚠️ Important:**
- **Backup your WoW folder** before major cleanups, especially your `WTF` folder before using Orphan Cleaner
- **Launch each WoW version once** (reach Character Select) before using Game Optimizer
- **Use "Move to Recycle Bin"** for reversible deletions until confident
- **Close WoW** before applying optimizer presets to avoid conflicts

See [Technical Details](Technical-Details.md) for detailed safety information and best practices.

## Installation & Usage

### Download Pre-built Executables (Recommended)

Download the latest release for your platform from [GitHub Releases](https://github.com/Myrroddin/wow-cleanup-tool/releases):

- **Windows**: `WoW Cleanup Tool.exe` - Double-click to run
- **macOS**: `WoW-Cleanup-Tool-macOS.dmg` - Mount and drag to Applications
- **Linux**: `WoW-Cleanup-Tool-Linux.tar.gz` - Extract and run `./"WoW Cleanup Tool"`

No Python installation required for pre-built executables!

### Running from Source

Alternatively, run from Python source:

#### Requirements
- **Python 3.8+** (3.12 recommended for building executables)
- **Auto-installed dependencies**: `psutil`, `send2trash`, `Pillow`

All required packages are automatically installed on first run if missing.

#### Running
```bash
python wow_cleanup_tool.py
```

### Quick Start
1. Click "Browse" and select your World of Warcraft folder
2. Choose "Move to Recycle Bin" for safe deletions
3. Use each tab to scan and clean as needed
4. (Optional) Scan hardware in Game Optimizer for preset recommendations

For detailed usage instructions, see [Technical Details](Technical-Details.md).

## Troubleshooting

**Common Issues:**
- **"Invalid Folder"**: Select the root WoW folder (contains `_retail_`, `_classic_`, etc.)
- **"Requires launch"**: Launch WoW version and reach Character Select to create required directories
- **Hardware not detected**: Some systems require elevated permissions for GPU detection
- **Changes not applied**: Close WoW before applying optimizer presets

See [Technical Details](Technical-Details.md) for advanced troubleshooting.

## Documentation

- **[README.md](README.md)** - This file: Overview and quick start
- **[BUILD.md](BUILD.md)** - Building executables and creating releases
- **[Technical Details](Technical-Details.md)** - Architecture, optimizations, and advanced usage
- **[LOCALIZATION.md](LOCALIZATION.md)** - Translation guide and language support
- **[LICENSE](LICENSE)** - GPL-3.0 license

## Contributing

Contributions welcome! See [Technical Details](Technical-Details.md) for architecture details. Please test changes across platforms where possible.

## Bug Reports & Feature Requests

- **[Report a Bug](https://github.com/Myrroddin/wow-cleanup-tool/issues/new?template=bug_report.yml)** - Submit detailed bug reports with logs and system info
- **[Request a Feature](https://github.com/Myrroddin/wow-cleanup-tool/issues/new?template=feature_request.yml)** - Suggest improvements or new features
- **[Discussions](https://github.com/Myrroddin/wow-cleanup-tool/discussions)** - General questions and community support

## Support

[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/c/Myrroddin) [![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/paypalme/PVandersypen)

## License

Copyright © 2025 Paul Vandersypen. Licensed under GPL-3.0-or-later. See [LICENSE](LICENSE) for details.
