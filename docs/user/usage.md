# MD2Office - Usage Guide

## Quick Start

The easiest way to get started is using the provided startup script:

### macOS/Linux

```bash
# Make executable (first time only)
chmod +x start_application.sh

# Show help
./start_application.sh --help

# Convert markdown to Word
./start_application.sh --word document.md

# Convert to all formats
./start_application.sh --all --output ./output document.md
```

### Windows

```cmd
# Show help
start_application.bat --help

# Convert markdown to Word
start_application.bat --word document.md

# Convert to all formats
start_application.bat --all --output ./output document.md
```

## What the Script Does

The `start_application.sh` (or `.bat` on Windows) script:

1. ✅ **Creates virtual environment** (`venv/`) if it doesn't exist
2. ✅ **Activates the virtual environment**
3. ✅ **Upgrades pip** to latest version
4. ✅ **Installs all dependencies** from `requirements.txt`
5. ✅ **Installs the md2office package** in development mode
6. ✅ **Runs the application** with your provided arguments

## Examples

### Basic Conversion

```bash
# Convert to Word
./start_application.sh --word README.md

# Convert to PowerPoint
./start_application.sh --powerpoint presentation.md

# Convert to PDF
./start_application.sh --pdf document.md

# Convert to all formats at once
./start_application.sh --all document.md
```

### With Options

```bash
# Custom output directory
./start_application.sh --word --output ./output document.md

# Custom filename
./start_application.sh --word --name report document.md

# Use professional style
./start_application.sh --word --style professional document.md

# Generate table of contents
./start_application.sh --word --toc document.md

# Add page breaks
./start_application.sh --word --page-breaks document.md
```

### Batch Processing

```bash
# Convert multiple files
./start_application.sh --word file1.md file2.md file3.md

# Convert entire directory
./start_application.sh --word --output ./output ./documents/
```

## Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .

# 4. Run
python -m md2office --word document.md
```

## Troubleshooting

### Script Permission Denied (macOS/Linux)

```bash
chmod +x start_application.sh
```

### Virtual Environment Already Exists

The script will reuse the existing virtual environment. To start fresh:

```bash
rm -rf venv
./start_application.sh --help
```

### Dependencies Not Installing

Make sure you have Python 3.8+ and pip:

```bash
python3 --version
pip --version
```

### Import Errors

If you get import errors, activate the venv and reinstall:

```bash
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Next Steps

- Read `quickstart.md` for more examples
- Check `build.md` for creating portable binaries
- See `dry-run-report.md` for implementation status

