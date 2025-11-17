# WoW Cleanup Tool

A comprehensive maintenance and optimization suite for World of Warcraft, helping you clean up unnecessary files, manage addons, and optimize game performance across all WoW versions (Retail, Classic, Classic Era, PTR, and Beta).

## Features

### 🗂️ File Cleaner
Scans and removes backup files (`.bak` and `.old`) that accumulate over time from WoW updates, addon installations, and configuration changes.

- **Multi-threaded scanning** for fast directory traversal across all WoW versions
- **Selective deletion** with checkbox selection for individual files
- **Safe deletion** options: Move to Recycle Bin/Trash or permanent deletion
- **Batch operations** with "Select All" toggle

### 📁 Folder Cleaner
Safely removes temporary and log folders that can consume significant disk space.

- Cleans **Logs**, **Errors**, and other temporary folders per WoW version
- **Per-version tabs** for granular control
- Displays folder sizes before deletion
- **Screenshot management** with preview support (if available)

### 🧹 Orphan Cleaner
Detects and removes SavedVariables files for uninstalled addons, keeping your WTF folder clean.

- **Scans all levels**: Account, Realm, and Character SavedVariables
- **Smart detection**: Identifies orphaned addon data by comparing against currently installed addons
- **Preserves Blizzard files**: Core game SavedVariables are never touched
- **AddOns.txt Rebuilding**: Automatically rebuilds addon lists to remove references to deleted addons

### ⚙️ Game Optimizer
Hardware-based graphics preset recommendations and automatic GPU selection for optimal performance.

- **Cross-platform hardware detection**: CPU (full name), RAM, GPU across Windows, macOS, and Linux
- **System requirement integration**: Uses official Blizzard requirements for Retail and Classic
- **Intelligent presets**: Low, Medium, High, and Ultra settings tailored to your hardware tier
- **Dedicated GPU selection**: Automatically configures WoW to use discrete GPU on systems with both integrated and dedicated graphics (Intel/AMD CPUs)
- **Per-version optimization**: Separate recommendations for Retail, Classic, and Classic Era
- **One-click application**: Apply presets directly to `Config.wtf`

### 📊 Additional Features

- **Multi-language Support**: Full interface translation in 7 languages (English, German, French, Spanish EU/MX, Portuguese, Korean) with 4 more using English fallback. See **[LOCALIZATION.md](LOCALIZATION.md)** for details.
- **Verbose Logging**: Optional detailed operation logs for troubleshooting
- **Theme Support**: Light and dark themes with OS-native styling
- **Font Customization**: Adjustable font family and size (6-16pt)
- **Update Checker**: Automatic GitHub release checking at startup
- **Geometry Persistence**: Window size and position saved between sessions
- **Multi-version Support**: Automatically detects all installed WoW versions including PTR and Beta

## Safety Precautions

### ⚠️ Important Warnings

1. **Always backup your WoW folder before major cleanups**
   - Consider creating a backup of your `WTF` folder, especially before using Orphan Cleaner
   - Use the "Move to Recycle Bin" option instead of permanent deletion until you're confident

2. **Game Optimizer Requirements**
   - The optimizer requires that each WoW version has been launched at least once
   - Launch the game and reach the Character Select screen before using the optimizer
   - The optimizer will display instructions if required directories (`WTF`, `Interface`, `AddOns`) are missing

3. **Orphan Cleaner Considerations**
   - SavedVariables are only "orphaned" if the corresponding addon is completely uninstalled
   - If you plan to reinstall an addon later, consider keeping its SavedVariables
   - Blizzard_*.lua files (core game data) are automatically excluded and never deleted

4. **Folder Cleaner Caution**
   - Screenshots folder deletion is permanent (or moves to trash)
   - Review folder contents before cleaning, especially if you value error logs for troubleshooting

5. **Config.wtf Modifications**
   - Game Optimizer writes directly to `Config.wtf`
   - Existing settings are preserved; only graphics-related CVars are updated
   - Close WoW before applying optimizer presets to avoid conflicts

### 🛡️ Safe Practices

- **Test on one version first**: Try File/Folder/Orphan cleaners on a single WoW version before running on all versions
- **Use Recycle Bin mode**: Enable "Move to Recycle Bin" in settings for reversible deletions
- **Review selections**: Uncheck items you're unsure about before processing
- **Enable Verbose Logging**: Helps track exactly what was changed (useful for troubleshooting)

## Installation & Usage

### Requirements
- **Python 3.8+** (64-bit recommended for large WoW installations)
- **Required Dependencies**: `psutil` (auto-installed if missing)
- **Optional Dependencies**:
  - `send2trash`: Enables "Move to Recycle Bin" option for safe deletion (highly recommended)
  - `Pillow`: Enables screenshot preview in Folder Cleaner

**Note**: If optional dependencies fail to install, the affected UI elements will be disabled (greyed out) with tooltips explaining how to manually install them. The tool remains fully functional without these packages, but with reduced features.

### Running the Tool

**Windows:**
```powershell
python wow_cleanup_tool.py
```

**macOS/Linux:**
```bash
python3 wow_cleanup_tool.py
```

### First-Time Setup

1. **Select WoW Folder**: Click "Browse" in Options and navigate to your World of Warcraft installation directory
2. **Scan Hardware** (Optional): Click "Scan Hardware" in the Game Optimizer tab to detect your system specs
3. **Choose Deletion Mode**: Select "Move to Recycle Bin" for safer operations or "Delete Permanently" for irreversible removal
4. **Adjust Theme/Font**: Customize appearance in Options section

### Using Each Tool

**File Cleaner:**
1. Click "Scan for .bak / .old Files"
2. Review detected files in the tree view
3. Select/deselect files as needed
4. Click "Process Selected Files"

**Folder Cleaner:**
1. Navigate to version-specific tabs (Retail, Classic, etc.)
2. Review folder sizes and contents
3. Check folders you want to clean
4. Click "Clean Selected Folders"

**Orphan Cleaner:**
1. Click "Scan for Orphans"
2. Review orphaned SavedVariables grouped by version
3. Select orphans to remove
4. Click "Process Selected Orphans"
5. Optionally click "Rebuild AddOns.txt" to clean addon lists

**Game Optimizer:**
1. Click "Scan Hardware" (one-time, results cached)
2. Navigate to version tabs to see preset recommendations
3. Choose a preset from the dropdown (defaults to suggested tier)
4. Click "Apply" to write settings to Config.wtf

## Technical Information

For detailed technical documentation including architecture, performance optimizations, cross-platform implementation details, and advanced topics, see the **[Technical Details Wiki](Technical-Details.md)**.

Topics covered in the technical documentation:
- Module architecture and design patterns
- Performance optimizations (multi-threading, caching, chunked operations)
- Cross-platform compatibility details (Windows, macOS, Linux)
- Hardware detection system internals
- Config.wtf management and CVar application
- Localization system (11 languages)
- Advanced debugging and troubleshooting

## Example Screenshots
![files](https://github.com/user-attachments/assets/2b2680d7-d7c0-4007-b5ad-3e03247f6ff4)
![folders](https://github.com/user-attachments/assets/5da620f1-e3e8-4ff9-abe9-4e85117a07ed)
![orphans](https://github.com/user-attachments/assets/e33a7e8e-d217-4f13-9b8b-c3c66f8015f0)
![optimizer](https://github.com/user-attachments/assets/d9b031de-d4c6-4326-a26f-cf9ac7a61ac9)

## Troubleshooting

**"Invalid Folder" error:**
- Ensure you've selected the root World of Warcraft folder (contains `_retail_`, `_classic_`, etc.)
- Path should point to the folder containing version subdirectories, not a version folder itself

**Optimizer shows "requires launch" message:**
- Launch the affected WoW version and reach Character Select screen
- This creates required directories (WTF, Interface/AddOns)

**Hardware scan shows "Not detected":**
- Some systems may require elevated permissions for full GPU detection
- CPU and RAM detection should work on all platforms

**Changes not taking effect in-game:**
- Close WoW completely before applying optimizer presets
- Verify Config.wtf was modified (check file timestamp)

For more troubleshooting help, see the **[Technical Details Wiki](Technical-Details.md)**.

## Contributing

Contributions welcome! Please test changes across Windows, macOS, and Linux where possible. See the **[Technical Details Wiki](Technical-Details.md)** for architecture and implementation details.

## Support

If you find this tool useful, consider supporting its development:

[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/c/Myrroddin) [![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/paypalme/PVandersypen)

## Documentation

- **[README.md](README.md)** - User guide, features, installation, and usage
- **[Technical Details Wiki](Technical-Details.md)** - Architecture, optimizations, cross-platform details
- **[LOCALIZATION.md](LOCALIZATION.md)** - Translation guide and language support details
- **[LICENSE](LICENSE)** - Full GPL-3.0 license text

## Known Limitations

- Screenshot previews require Pillow library (disabled with helpful tooltip if not installed)
- "Move to Recycle Bin" option requires send2trash library (disabled with tooltip if not installed)
- GPU adapter selection only applies on Windows (macOS/Linux use different mechanisms)
- Extremely large installations (100k+ files) may take 30+ seconds for initial scan

For detailed technical limitations and workarounds, see the **[Technical Details Wiki](Technical-Details.md)**.

### Graceful Degradation

The tool implements graceful degradation for optional dependencies:
- **Missing send2trash**: "Move to Recycle Bin" radio button is disabled and greyed out. Hovering shows installation instructions.
- **Missing Pillow**: Screenshot preview canvas is disabled and greyed out. All screenshot checkboxes remain functional for deletion, but preview-on-click is unavailable.

Both features display tooltips with manual installation commands when the dependency is missing.

## License

Copyright © 2025 Paul Vandersypen. This project is licensed under the GNU General Public License v3.0 or later.

- SPDX-License-Identifier: GPL-3.0-or-later

See the included `LICENSE` file for the full license text and terms.
