# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for md2office converter.

This file defines how PyInstaller should build the executable.
"""

block_cipher = None

import os
import sys

# Get the project root (one level up from scripts/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(SPECPATH)))
src_path = os.path.join(project_root, 'src')

a = Analysis(
    [os.path.join(src_path, 'md2office', 'cli_entry.py')],
    pathex=[src_path],  # Add src to Python path
    binaries=[],
    datas=[
        (os.path.join(src_path, 'md2office'), 'md2office'),
    ],
    hiddenimports=[
        'md2office',
        'md2office.cli',
        'md2office.cli.main',
        'md2office.gui',
        'md2office.gui.main_window',
        'md2office.gui.gui_main',
        'md2office.gui.conversion_service',
        'md2office.gui.workers',
        'md2office.gui.workers.conversion_worker',
        'md2office.router',
        'md2office.generators',
        'md2office.parser',
        'md2office.config',
        'md2office.errors',
        'md2office.styling',
        'click',
        'docx',
        'pptx',
        'reportlab',
        'yaml',
        'reportlab.lib',
        'reportlab.pdfgen',
        'reportlab.platypus',
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
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

# Using onedir (folder) method for faster startup
# This creates a folder with the executable and all dependencies
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='md2office',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='md2office',
)

