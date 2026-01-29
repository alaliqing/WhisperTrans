# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for WhisperTrans macOS app bundle.
Builds a standalone .app that includes Python, all dependencies, and assets.
"""

import os
import sys

block_cipher = None

# Get the project root directory
project_root = os.path.dirname(SPECPATH)

# Analysis phase - collect all dependencies
a = Analysis(
    [os.path.join(project_root, 'web_app.py')],
    pathex=[project_root],
    binaries=[],
    datas=[
        # Bundle Flask templates and static files
        (os.path.join(project_root, 'templates'), 'templates'),
        (os.path.join(project_root, 'static'), 'static'),
        # Include .env.example as template for configuration
        (os.path.join(project_root, '.env.example'), '.'),
        # Include whisper_trans.py module
        (os.path.join(project_root, 'whisper_trans.py'), '.'),
    ],
    hiddenimports=[
        # Flask hidden imports
        'werkzeug',
        'werkzeug.exceptions',
        'werkzeug.security',
        'jinja2',
        'jinja2.ext',
        # Whisper/PyTorch hidden imports
        'whisper',
        'whisper.transcoder',
        'whisper.audio',
        'whisper.tokenizer',
        'torch',
        'torch.nn',
        'torch.nn.functional',
        'torch.nn.quantized',
        'torch.quantization',
        'numpy',
        'numpy.core._multiarray_umath',
        'frozenlist',
        # Additional PyTorch modules
        'torch._C',
        'torch.cuda',
        'torch.cuda.amps',
        # Audio processing
        'ffmpeg',
        'ffmpeg.python',
        # Standard library modules
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude test modules and unused packages to reduce size
        'pytest', 'unittest', 'test', 'tests',
        'tkinter', 'matplotlib', 'IPython',
        'PIL',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Filter phase - create executable archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WhisperTrans',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Use UPX compression to reduce size by ~30-40%
    console=False,  # Hide console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Collect all binaries and data files
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WhisperTrans',
)

# Create macOS app bundle
app = BUNDLE(
    coll,
    name='WhisperTrans.app',
    icon=os.path.join(project_root, 'packaging', 'app-icon', 'icon.icns'),
    bundle_identifier='com.alaliqing.whispertrans',
    info_plist=os.path.join(project_root, 'packaging', 'Info.plist'),
)
