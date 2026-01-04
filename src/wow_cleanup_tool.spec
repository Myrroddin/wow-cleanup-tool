# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for WoW Cleanup Tool (v1.0 - Feature Complete).

Ensures assets, license, and all source modules are bundled consistently across
platforms. Features include automatic WoW detection, multi-flavor support,
file cleaning with AddOns.txt integration, dual logging system, font-aware
UI scaling, and defensive error handling.

Run with:

    pyinstaller src/wow_cleanup_tool.spec
"""

import sys
from pathlib import Path

block_cipher = None

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
SRC_DIR = BASE_DIR
ENTRYPOINT = SRC_DIR / "wow_cleanup_tool.py"

# Determine platform-specific icon and executable name
if sys.platform == "win32":
    icon_file = REPO_ROOT / "assets" / "icons" / "wow_cleanup_icon.ico"
    exe_name = "WoW Cleanup Tool"
elif sys.platform == "darwin":
    icon_file = REPO_ROOT / "assets" / "icons" / "wow_cleanup_icon.icns"
    exe_name = "WoW Cleanup Tool"
else:  # Linux and others
    icon_file = REPO_ROOT / "assets" / "icons" / "wow_cleanup_icon.png"
    exe_name = "WoW Cleanup Tool"

# Datas: include license, assets, and full source tree
datas = [
    (str(REPO_ROOT / "LICENSE"), "."),
    (str(REPO_ROOT / "assets"), "assets"),
    (str(SRC_DIR), "src"),
]

a = Analysis(
    [str(ENTRYPOINT)],
    pathex=[str(SRC_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "tkinter",
        "tkinter.ttk",
        "tkinter.font",
        "sv_ttk",
        "darkdetect",
        "orjson",
        "tkinter.messagebox",
        "tkinter.filedialog",
        "PIL",
        "PIL.Image",
        "PIL.ImageTk",
        "PIL.ImageDraw",
        "send2trash",
        # Core Modules
        "core",
        "core.dependencies",
        "core.logger",
        "core.settings",
        "core.single_instance",
        "core.themes",
        # Localization Modules
        "localization",
        "localization.en_us",
        # UI Modules
        "ui",
        "ui.app_controller",
        "ui.dialog_base",
        "ui.font_utils",
        "ui.geometry",
        "ui.log_controls",
        "ui.main_window",
        "ui.ui_constants",
        "ui.dialogs",
        "ui.dialogs.license_dialog",
        "ui.dialogs.multiple_installations",
        "ui.dialogs.wow_close_warning",
        "ui.tabs",
        "ui.tabs.developer_tab",
        "ui.tabs.file_cleaner_tab",
        "ui.tabs.folder_cleaner_tab",
        "ui.tabs.game_optimizer_tab",
        "ui.tabs.log_tab",
        "ui.widgets",
        "ui.widgets.tooltip",
        # WoW Modules
        "wow",
        "wow.path_handler",
        "wow.path_manager",
        # Operations Modules
        "operations",
        "operations.base_scanner",
        "operations.file_cleaner",
        "operations.file_operations",
        "operations.orphan_scanner",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tests",  # Exclude unit tests from executable
        "pytest",
        "unittest",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(icon_file),
)

# macOS-specific app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='WoW Cleanup Tool.app',
        icon=str(icon_file),
        bundle_identifier='com.myrroddin.wowcleanuptool',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
        },
    )
