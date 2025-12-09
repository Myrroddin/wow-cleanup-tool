# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for WoW Cleanup Tool.

This file defines how PyInstaller should build the executable.
You can use this locally or the GitHub Actions workflow will use similar settings.

Usage:
    pyinstaller wow_cleanup_tool.spec
"""

import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Determine platform-specific icon and executable name
if sys.platform == 'win32':
    icon_file = 'wow_cleanup_icon/wow_cleanup_icon.ico'
    exe_name = 'WoW Cleanup Tool'
elif sys.platform == 'darwin':
    icon_file = 'wow_cleanup_icon/wow_cleanup_icon.icns'
    exe_name = 'WoW Cleanup Tool'
else:  # Linux and others
    icon_file = 'wow_cleanup_icon/46df463a-9eb4-433a-b4b0-5e6df94328d3-0.png'
    exe_name = 'WoW Cleanup Tool'

a = Analysis(
    ['wow_cleanup_tool.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('LICENSE', '.'),  # License file displayed to users
        ('modules', 'modules'),  # All Python modules (PyInstaller will compile to .pyc)
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.font',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.ImageDraw',
        'psutil',
        'send2trash',
        # Core Modules
        'modules',
        'modules.core',
        'modules.core.dependencies',
        'modules.core.geometry',
        'modules.core.global_settings',
        'modules.core.logger',
        'modules.core.settings',
        'modules.core.single_instance',
        'modules.core.themes',
        # Localization Modules
        'modules.localization',
        'modules.localization.en_us',
        # UI Modules
        'modules.ui',
        'modules.ui.app_controller',
        'modules.ui.dialog_base',
        'modules.ui.font_utils',
        'modules.ui.geometry',
        'modules.ui.main_window',
        'modules.ui.ui_constants',
        'modules.ui.dialogs',
        'modules.ui.dialogs.license_dialog',
        'modules.ui.dialogs.multiple_installations',
        'modules.ui.dialogs.wow_close_warning',
        # WoW Modules
        'modules.wow',
        'modules.wow.game_optimizer',
        'modules.wow.game_validation',
        'modules.wow.path_handler',
        'modules.wow.path_manager',
        # Operations Modules
        'modules.operations',
        'modules.operations.base_scanner',
        'modules.operations.disk_utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tests',  # Exclude unit tests from executable
        'pytest',
        'unittest',
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
    icon=icon_file,
)

# macOS-specific app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='WoW Cleanup Tool.app',
        icon=icon_file,
        bundle_identifier='com.myrroddin.wowcleanuptool',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
        },
    )
