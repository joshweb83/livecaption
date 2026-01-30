# -*- mode: python ; coding: utf-8 -*-
"""
Live Caption - PyInstaller Spec File
Version: 1.0.3

This file configures how PyInstaller builds the Windows executable.

IMPORTANT: Data files (config.yaml, themes/) are bundled into the EXE.
At runtime, they are extracted to sys._MEIPASS temporary directory.
The application must use sys._MEIPASS to access these files.
"""

block_cipher = None

# Data files to include in the bundle
# Format: (source, destination_in_bundle)
# '.' means root of the bundle (sys._MEIPASS at runtime)
# Note: Paths are relative to the spec file location
datas = [
    ('config.yaml', '.'),
    ('themes', 'themes'),
    ('README.md', '.'),
]

# Analysis: Analyze the Python script and find all dependencies
a = Analysis(
    ['main.py'],
    pathex=[],
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
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 디버깅용 콘솔 활성화
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
