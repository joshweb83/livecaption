# -*- mode: python ; coding: utf-8 -*-
"""
Live Caption - PyInstaller Spec File
Version: 1.0.2

This file configures how PyInstaller builds the Windows executable.

IMPORTANT: Data files (config.yaml, themes/) are bundled into the EXE.
At runtime, they are extracted to sys._MEIPASS temporary directory.
The application must use sys._MEIPASS to access these files.
"""

import os
from pathlib import Path

block_cipher = None

# Get the directory where this spec file is located
SPEC_DIR = os.path.dirname(os.path.abspath(SPECPATH))

# Data files to include in the bundle
# Format: (source, destination_in_bundle)
# '.' means root of the bundle (sys._MEIPASS at runtime)
datas = [
    # Config file - placed at root of bundle
    (os.path.join(SPEC_DIR, 'config.yaml'), '.'),
    # Themes directory - maintains directory structure
    (os.path.join(SPEC_DIR, 'themes'), 'themes'),
    # README for reference
    (os.path.join(SPEC_DIR, 'README.md'), '.'),
]

# Verify data files exist before building
for src, _ in datas:
    if not os.path.exists(src):
        raise FileNotFoundError(f"Required data file not found: {src}")

# Analysis: Analyze the Python script and find all dependencies
a = Analysis(
    ['main.py'],
    pathex=[SPEC_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # PyQt5 GUI framework
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        # Speech recognition
        'faster_whisper',
        'ctranslate2',
        # Translation
        'transformers',
        'sentencepiece',
        'sacremoses',
        # Deep learning
        'torch',
        'torchaudio',
        # Audio
        'pyaudio',
        'sounddevice',
        'numpy',
        # Configuration
        'yaml',
        'pyyaml',
        # Logging
        'loguru',
        # System
        'psutil',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary packages to reduce size
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
        'tkinter',
        'test',
        'tests',
        'unittest',
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

# EXE: Create the executable (single file mode)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LiveCaption',
    debug=False,  # Set to True for debugging
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress with UPX for smaller file size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI application)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='assets/icon.ico',  # Uncomment when icon file is available
)
