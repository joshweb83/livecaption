# -*- mode: python ; coding: utf-8 -*-
"""
Live Caption - PyInstaller Spec File
Version: 1.0.1

This file configures how PyInstaller builds the Windows executable.
"""

block_cipher = None

# Analysis: Analyze the Python script and find all dependencies
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.yaml', '.'),
        ('themes', 'themes'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'faster_whisper',
        'transformers',
        'torch',
        'yaml',
        'loguru',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ: Create a compressed archive of Python modules
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# EXE: Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LiveCaption',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress with UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',  # Uncomment and provide icon file
)
