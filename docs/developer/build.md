# Build Guide

This guide explains how to build portable binaries for md2office converter.

## Prerequisites

- Python 3.8 or higher
- pip
- PyInstaller: `pip install pyinstaller`

## Building Locally

### Windows

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build binary
pyinstaller --onefile --name md2office --console src/md2office/__main__.py

# Binary will be in dist/md2office.exe
```

### macOS (Intel)

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build binary
pyinstaller --onefile --name md2office --console src/md2office/__main__.py

# Binary will be in dist/md2office
```

### macOS (Apple Silicon / ARM)

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build binary (use arch -arm64 to ensure ARM build)
arch -arm64 pyinstaller --onefile --name md2office --console src/md2office/__main__.py

# Binary will be in dist/md2office
```

## Using the Build Script

Alternatively, use the provided build script:

```bash
python build.py
```

## Build Options

### PyInstaller Options

- `--onefile`: Create a single executable file
- `--console`: Show console window (for CLI)
- `--name`: Name of the executable
- `--clean`: Clean PyInstaller cache before building
- `--noconfirm`: Overwrite output directory without asking

### Advanced Options

To reduce binary size, you can exclude unused modules:

```bash
pyinstaller --onefile --name md2office --console \
  --exclude-module matplotlib \
  --exclude-module numpy \
  src/md2office/__main__.py
```

## Testing the Binary

After building, test the binary:

```bash
# Windows
dist\md2office.exe --help

# macOS/Linux
dist/md2office --help
```

## Binary Size Optimization

The binary size can be optimized by:

1. **Excluding unused modules**: Use `--exclude-module` for modules not needed
2. **Using UPX compression**: PyInstaller uses UPX by default if available
3. **Stripping debug symbols**: Use `--strip` flag (Linux/macOS)

## Cross-Platform Building

### Building for Windows from macOS/Linux

PyInstaller can cross-compile, but it's recommended to build on the target platform or use CI/CD.

### Building for macOS from Linux

Not directly supported. Use macOS machine or CI/CD.

## CI/CD Builds

GitHub Actions workflows are configured to automatically build binaries for all platforms when tags are pushed.

See `.github/workflows/build.yml` for details.

## Troubleshooting

### Import Errors

If you get import errors at runtime, add the missing module to `hiddenimports` in `pyinstaller.spec`:

```python
hiddenimports=[
    'missing_module',
]
```

### Large Binary Size

- Check for unnecessary dependencies
- Use `--exclude-module` to remove unused modules
- Consider using `--onedir` instead of `--onefile` (creates directory with dependencies)

### Binary Not Working

- Ensure all dependencies are included
- Check PyInstaller logs in `build/` directory
- Test on clean system without Python installed

## Distribution

After building, distribute the binary from `dist/` directory:

- Windows: `md2office.exe`
- macOS: `md2office` (may need to be signed for distribution)

