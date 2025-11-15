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
- **Dependencies**: `psutil` (auto-installed if missing), optional: `send2trash`, `Pillow`

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

## Technical Details

### Performance Optimizations
- **Multi-threaded scanning**: File scanning uses ThreadPoolExecutor for parallel directory traversal
- **os.scandir**: Fast directory iteration (2-3x faster than os.walk)
- **Compiled regex patterns**: Pre-compiled patterns for file extension matching
- **Chunked UI updates**: Tree view population in batches to maintain responsiveness
- **Hardware caching**: System specs cached globally to avoid repeated detection

### Cross-Platform Compatibility
- **Windows**: Full support with native GPU detection (WMIC/PowerShell)
- **macOS**: Supports Apple Silicon (M1/M2/M3/M4) and Intel Macs (sysctl, system_profiler)
- **Linux**: GPU detection via lspci, CPU info from /proc/cpuinfo

### Settings Storage
- **Per-user settings**: Stored in `~/.wow_cleanup_tool/settings.json` (window geometry, font, theme)
- **Global settings**: Stored in system-wide location (ProgramData on Windows, /etc on Unix) for WoW path, hardware cache, and shared preferences

### GPU Selection Logic
- Detects both integrated and dedicated GPUs on Intel/AMD systems
- Automatically configures WoW to use the dedicated GPU via `gxAdapter` CVar (Windows only)
- Skips GPU adapter setting on macOS/Linux (not applicable)
- Apple Silicon systems excluded (no dedicated GPU)

## Example Screenshots
![files](https://github.com/user-attachments/assets/2b2680d7-d7c0-4007-b5ad-3e03247f6ff4)
![folders](https://github.com/user-attachments/assets/5da620f1-e3e8-4ff9-abe9-4e85117a07ed)
![orphans](https://github.com/user-attachments/assets/e33a7e8e-d217-4f13-9b8b-c3c66f8015f0)

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

## Contributing

Contributions welcome! Please test changes across Windows, macOS, and Linux where possible.

## Known Limitations

- Screenshot previews require Pillow library (optional dependency)
- GPU adapter selection only applies on Windows (macOS/Linux use different mechanisms)
- Extremely large installations (100k+ files) may take 30+ seconds for initial scan

## License

Copyright © 2025 Paul Vandersypen. This project is licensed under the GNU General Public License v3.0 or later.

- SPDX-License-Identifier: GPL-3.0-or-later

See the included `LICENSE` file for the full license text and terms.
