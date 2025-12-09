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
        ('src', 'src'),  # All Python modules (PyInstaller will compile to .pyc)
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
        'core',
        'core.dependencies',
        'core.geometry',
        'core.global_settings',
        'core.logger',
        'core.settings',
        'core.single_instance',
        'core.themes',
        # Localization Modules
        'localization',
        'localization.en_us',
        # UI Modules
        'ui',
        'ui.app_controller',
        'ui.dialog_base',
        'ui.font_utils',
        'ui.geometry',
        'ui.main_window',
        'ui.ui_constants',
        'ui.dialogs',
        'ui.dialogs.license_dialog',
        'ui.dialogs.multiple_installations',
        'ui.dialogs.wow_close_warning',
        # WoW Modules
        'wow',
        'wow.game_optimizer',
        'wow.game_validation',
        'wow.path_handler',
        'wow.path_manager',
        # Operations Modules
        'operations',
        'modules.operations.base_scanner',
        'modules.operations.disk_utils',
        'modules.operations.file_cleaner',
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
