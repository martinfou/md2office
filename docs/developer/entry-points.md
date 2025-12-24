# Entry Point Architecture

This document describes the entry point architecture for the md2office application, explaining how the application can be invoked and how the different entry points work together.

## Overview

The md2office application provides multiple ways to be invoked:

1. **Command-line entry point** (via `pip install`)
2. **Module execution** (`python -m md2office`)
3. **PyInstaller executable** (bundled binary)

All entry points ultimately call the same `main()` function from `md2office.cli.main`.

## Entry Point Structure

```
md2office/
├── __main__.py          # Module entry point
├── cli_entry.py         # PyInstaller entry point
└── cli/
    ├── __init__.py      # CLI package exports
    └── main.py          # Main CLI implementation
```

## Entry Points

### 1. Command-Line Entry Point (`md2office`)

**Definition:** `pyproject.toml`
```toml
[project.scripts]
md2office = "md2office.cli:main"
```

**How it works:**
- When installed via `pip install .`, setuptools creates a console script named `md2office`
- The script imports `main` from `md2office.cli` module
- `md2office/cli/__init__.py` exports `main` from `cli/main.py`
- This allows the command to be invoked as: `md2office [OPTIONS] <input>`

**Usage:**
```bash
md2office --word document.md
md2office --all --output ./output document.md
```

### 2. Module Entry Point (`python -m md2office`)

**File:** `src/md2office/__main__.py`

**How it works:**
- Python's `-m` flag looks for `__main__.py` in the package
- `__main__.py` imports `main` from `.cli` (which resolves to `md2office.cli`)
- Calls `main()` function

**Usage:**
```bash
python -m md2office --word document.md
```

**Code:**
```python
from .cli import main

if __name__ == '__main__':
    main()
```

### 3. PyInstaller Entry Point (`cli_entry.py`)

**File:** `src/md2office/cli_entry.py`

**Purpose:** 
- Used as the entry point for PyInstaller builds
- Handles path resolution for frozen executables
- Provides fallback import mechanisms

**How it works:**
1. Detects if running as frozen executable (`sys.frozen`)
2. Adds PyInstaller's `_internal` directory to `sys.path`
3. Attempts to import `main` from `md2office.cli`
4. Falls back to relative imports if absolute import fails
5. Calls `main()` and exits with its return code

**Why separate from `__main__.py`:**
- PyInstaller has issues with relative imports in `__main__.py`
- `cli_entry.py` provides explicit path handling for frozen executables
- Ensures reliable execution in bundled binaries

**Referenced in:** `scripts/pyinstaller.spec`
```python
a = Analysis(
    [os.path.join(src_path, 'md2office', 'cli_entry.py')],
    ...
)
```

## Entry Point Flow

```
User Invocation
    │
    ├─→ pip install → md2office command → md2office.cli:main
    │
    ├─→ python -m md2office → __main__.py → md2office.cli:main
    │
    └─→ ./md2office (binary) → cli_entry.py → md2office.cli:main
                                    │
                                    └─→ md2office/cli/__init__.py
                                            │
                                            └─→ md2office/cli/main.py
                                                    │
                                                    └─→ main() function
```

## CLI Module Structure

### `md2office/cli/__init__.py`
- Exports `cli` (Click command decorator) and `main` function
- Imports from `cli/main.py`
- Provides clean public API: `from md2office.cli import main`

### `md2office/cli/main.py`
- Contains the actual CLI implementation
- Defines `cli()` function (Click command)
- Defines `main()` function (entry point wrapper)
- Handles GUI/CLI mode detection
- Processes command-line arguments
- Orchestrates conversion pipeline

## GUI Entry Point

The CLI also supports launching a GUI:

**Detection:**
- If `--gui` flag is provided, or
- If no input files and no format flags are provided

**Code:** `md2office/cli/main.py`
```python
if gui or (not inputs and not any([word, powerpoint, pdf, all])):
    from ..gui.gui_main import main as gui_main
    gui_main()
    return
```

**Usage:**
```bash
md2office --gui
md2office  # Launches GUI if no arguments
```

## Import Resolution

The entry points use the following import resolution order:

1. **Absolute import:** `from md2office.cli import main`
2. **Relative import:** `from .cli import main` (fallback)
3. **Path manipulation:** Add project root to `sys.path` (last resort)

This ensures the application works in:
- Development mode (source code)
- Installed package (pip install)
- Frozen executable (PyInstaller)

## Testing Entry Points

To test that entry points work correctly:

```bash
# Test CLI entry point (after pip install)
md2office --help

# Test module entry point
python -m md2office --help

# Test PyInstaller entry point (after build)
./dist/md2office/md2office --help
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError: No module named 'md2office'`:

1. **Development:** Ensure you're in the project root and `src/` is in Python path
2. **Installed:** Run `pip install -e .` to install in editable mode
3. **Frozen:** Check that `cli_entry.py` path resolution is working

### Entry Point Not Found

If `md2office` command is not found after installation:

1. Check installation: `pip show md2office`
2. Verify entry point: `pip show -f md2office | grep -A 5 "Entry-points"`
3. Reinstall: `pip install -e .`

## Summary

All entry points converge on `md2office.cli.main.main()`, which:
- Detects GUI vs CLI mode
- Parses command-line arguments
- Loads configuration
- Initializes conversion pipeline
- Executes conversions
- Handles errors and provides feedback

This architecture ensures consistent behavior regardless of how the application is invoked.

