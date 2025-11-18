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

# Determine platform-specific icon
if sys.platform == 'win32':
    icon_file = 'wow_cleanup_icon.ico'
elif sys.platform == 'darwin':
    icon_file = 'wow_cleanup_icon.icns'
else:  # Linux and others
    icon_file = 'wow_cleanup_icon/46df463a-9eb4-433a-b4b0-5e6df94328d3-0.png'

a = Analysis(
    ['wow_cleanup_tool.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Modules', 'Modules'),
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
        'psutil',
        'send2trash',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='WoW Cleanup Tool',
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
