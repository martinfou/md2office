"""
Build script for creating cross-platform binaries.

This is the main build script used by build.sh (macOS/Linux) and build.bat (Windows).
Uses PyInstaller to create standalone executables for Windows, macOS, and Linux.

The platform-specific wrapper scripts (build.sh/build.bat) handle:
- Virtual environment setup
- Dependency installation
- Then call this script to perform the actual build

This centralizes build logic and avoids duplication.
"""

import sys
import subprocess
import platform
from pathlib import Path


def build_binary():
    """Build binary executable using PyInstaller."""
    try:
        import PyInstaller.__main__
    except ImportError:
        print("Error: PyInstaller is required for building binaries.")
        print("Install with: pip install pyinstaller")
        sys.exit(1)
    
    # Get the main entry point (build.py is now in scripts/, so go up one level)
    project_root = Path(__file__).parent.parent
    # Use cli_entry.py instead of __main__.py to avoid relative import issues with PyInstaller
    main_script = project_root / "src" / "md2office" / "cli_entry.py"
    
    if not main_script.exists():
        print(f"Error: Main script not found: {main_script}")
        sys.exit(1)
    
    # PyInstaller arguments
    # Using --onedir (folder method) instead of --onefile for faster startup
    system = platform.system()
    
    # Windows uses ';' as separator, Unix uses ':'
    path_sep = ';' if system == 'Windows' else ':'
    add_data_path = f'{project_root / "src" / "md2office"}{path_sep}md2office'
    
    # Add src directory to path so PyInstaller can find the md2office package
    src_path = str(project_root / "src")
    
    args = [
        str(main_script),
        '--name=md2office',
        '--onedir',  # Folder method for faster startup
        '--console',
        '--clean',
        '--noconfirm',
        f'--paths={src_path}',  # Add src to Python path
        f'--add-data={add_data_path}',
        '--hidden-import=md2office',
        '--hidden-import=md2office.cli',
        '--hidden-import=md2office.cli.main',
        '--hidden-import=md2office.router',
        '--hidden-import=md2office.generators',
        '--hidden-import=md2office.parser',
        '--hidden-import=md2office.config',
        '--hidden-import=md2office.errors',
        '--hidden-import=md2office.styling',
        '--hidden-import=click',
        '--hidden-import=docx',
        '--hidden-import=pptx',
        '--hidden-import=reportlab',
        '--hidden-import=yaml',
        '--collect-all=reportlab',
        '--collect-all=docx',
        '--collect-all=pptx',
    ]
    
    # Platform-specific options
    if system == 'Windows':
        args.append('--icon=NONE')  # Can add icon file later
    elif system == 'Darwin':  # macOS
        args.append('--icon=NONE')
    
    print(f"Building binary for {system}...")
    print(f"Command: pyinstaller {' '.join(args)}")
    
    try:
        PyInstaller.__main__.run(args)
        print("\nBuild completed successfully!")
        print(f"Binary location: dist/md2office/md2office{'.exe' if system == 'Windows' else ''}")
        print(f"All files are in: dist/md2office/")
        print("\nNote: The executable and all dependencies are in the 'md2office' folder.")
        print("      This folder method provides faster startup compared to single-file builds.")
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    build_binary()

