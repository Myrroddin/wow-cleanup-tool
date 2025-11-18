# Building and Releasing WoW Cleanup Tool

This document explains how to create releases with automatically built executables for Windows, macOS, and Linux.

## Automatic Builds with GitHub Actions

The repository is configured to automatically build executables for all three platforms when you create a release tag.

### How to Create a Release

1. **Update the version** in `wow_cleanup_tool.py`:
   ```python
   APP_VERSION = "v1.0.0"  # Update this
   ```

2. **Commit and push** your changes:
   ```bash
   git add .
   git commit -m "Release v1.0.0"
   git push
   ```

3. **Create and push a tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

4. **Wait for the build** (5-10 minutes):
   - GitHub Actions will automatically:
     - Build Windows executable (.exe)
     - Build macOS application (.dmg)
     - Build Linux executable (.tar.gz)
     - Create a GitHub release with all three files attached

5. **Check the release**:
   - Go to: https://github.com/Myrroddin/wow-cleanup-tool/releases
   - Your new release will have all three executables ready for download

### What Gets Built

- **Windows**: `WoW Cleanup Tool.exe` (uses `wow_cleanup_icon.ico`)
- **macOS**: `WoW-Cleanup-Tool-macOS.dmg` containing `WoW Cleanup Tool.app` (uses `wow_cleanup_icon.icns`)
- **Linux**: `WoW-Cleanup-Tool-Linux.tar.gz` containing `WoW Cleanup Tool` (uses PNG icon)

All builds use **Python 3.12** for consistency and compatibility.

### Version Tag Format

The workflow triggers on tags matching the pattern `v*.*.*`:
- ✅ `v1.0.0`
- ✅ `v2.1.3`
- ✅ `v1.0.0-beta`
- ❌ `1.0.0` (missing 'v' prefix)
- ❌ `release-1.0` (wrong format)

## Manual Local Builds

You can also build executables locally for testing.

### Prerequisites

```bash
pip install pyinstaller
pip install -r requirements.txt
```

### Build Using Spec File

The easiest way to build locally:

```bash
pyinstaller wow_cleanup_tool.spec
```

This will create the executable in the `dist/` folder.

### Platform-Specific Builds

#### Windows

```bash
pyinstaller --onefile --windowed --name "WoW Cleanup Tool" --icon "wow_cleanup_icon.ico" --add-data "Modules;Modules" wow_cleanup_tool.py
```

#### macOS

```bash
pyinstaller --onefile --windowed --name "WoW Cleanup Tool" --icon "wow_cleanup_icon.icns" --add-data "Modules:Modules" wow_cleanup_tool.py
```

To create a DMG:
```bash
mkdir -p dist/dmg
cp -r "dist/WoW Cleanup Tool.app" dist/dmg/
hdiutil create -volname "WoW Cleanup Tool" -srcfolder dist/dmg -ov -format UDZO dist/WoW-Cleanup-Tool-macOS.dmg
```

#### Linux

```bash
pyinstaller --onefile --windowed --name "WoW Cleanup Tool" --icon "wow_cleanup_icon/46df463a-9eb4-433a-b4b0-5e6df94328d3-0.png" --add-data "Modules:Modules" wow_cleanup_tool.py
```

To create a tarball:
```bash
cd dist
tar -czf WoW-Cleanup-Tool-Linux.tar.gz "WoW Cleanup Tool"
```

## Troubleshooting

### Build Fails on GitHub Actions

1. Check the Actions tab: https://github.com/Myrroddin/wow-cleanup-tool/actions
2. Click on the failed workflow run
3. Expand the failed step to see error details
4. Common issues:
   - Missing dependencies in `requirements.txt`
   - Missing icon files
   - Incorrect file paths in `--add-data`

### Executable Doesn't Run

1. **Windows**: Missing DLLs
   - Solution: Build on Windows or use GitHub Actions

2. **macOS**: "App is damaged" or security warning
   - Solution: Users need to right-click → Open, or go to System Preferences → Security & Privacy

3. **Linux**: Permission denied
   - Solution: `chmod +x "WoW Cleanup Tool"`

### Testing Before Release

1. Create a test tag:
   ```bash
   git tag v0.0.1-test
   git push origin v0.0.1-test
   ```

2. Download the built executables from the release

3. Test on each platform

4. If good, delete the test tag and create the real release:
   ```bash
   git tag -d v0.0.1-test
   git push origin :refs/tags/v0.0.1-test
   git tag v1.0.0
   git push origin v1.0.0
   ```

## Monitoring Builds

You can watch the build progress in real-time:
1. Go to: https://github.com/Myrroddin/wow-cleanup-tool/actions
2. Click on the running workflow
3. Watch each platform build in parallel

## Release Notes

The workflow automatically generates release notes based on commits since the last tag. You can edit these after the release is created.

## Download Statistics

GitHub provides download statistics for each release asset. Check them at:
`https://github.com/Myrroddin/wow-cleanup-tool/releases`

## Icon Files

The build process uses:
- **Windows**: `wow_cleanup_icon.ico` (256x256 multi-size ICO)
- **macOS**: `wow_cleanup_icon.icns` (512x512 ICNS)
- **Linux**: `wow_cleanup_icon/46df463a-9eb4-433a-b4b0-5e6df94328d3-0.png`

Make sure these files exist in your repository before creating a release.
