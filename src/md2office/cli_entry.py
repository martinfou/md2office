"""
Entry point for PyInstaller builds.

This script serves as the entry point for PyInstaller-compiled executables.
It handles path resolution for frozen executables where relative imports
in __main__.py may fail.

Naming Convention:
- Named `cli_entry.py` (not `entry_point.py`) to:
  * Clearly indicate it's CLI-specific (not GUI entry point)
  * Match the pattern of other CLI-related files (cli/, cli/main.py)
  * Distinguish from generic "entry point" terminology

Why this exists:
- PyInstaller bundles Python code into executables
- Frozen executables have different import path behavior
- __main__.py uses relative imports which can fail in frozen context
- This file uses absolute imports with fallback mechanisms

Usage:
- Referenced in scripts/pyinstaller.spec as the entry point
- Automatically used when building with PyInstaller
- Not intended for direct execution in development (use __main__.py instead)

See docs/developer/entry-points.md for complete entry point architecture.
"""

import sys
from pathlib import Path

# Handle PyInstaller frozen executable path resolution
if getattr(sys, 'frozen', False):
    # Running as a compiled/bundled executable
    base_path = Path(sys.executable).parent
    # PyInstaller stores packages in _internal directory
    internal_path = base_path / '_internal'
    if internal_path.exists():
        sys.path.insert(0, str(internal_path))
    # Also add the base path in case packages are there
    sys.path.insert(0, str(base_path))

# Import strategy: Try absolute import first (works in frozen executables)
# Fall back to relative import (works in development)
# Last resort: manipulate path and try absolute again
try:
    from md2office.cli import main
except ImportError:
    # Fallback: try relative import if absolute import fails (development mode)
    try:
        from .cli import main
    except ImportError:
        # Last resort: add project root to path and try absolute import again
        # This handles edge cases where package structure is non-standard
        current_dir = Path(__file__).parent.parent.parent
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
        from md2office.cli import main

if __name__ == '__main__':
    sys.exit(main())

