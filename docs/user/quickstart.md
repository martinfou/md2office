# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Optional: Mermaid Diagram Support

For PowerPoint presentations with Mermaid diagrams, install `mermaid-cli`:

```bash
# Requires Node.js (install from https://nodejs.org/)
npm install -g @mermaid-js/mermaid-cli
```

**Note**: Mermaid diagrams will be rendered as images in PowerPoint slides. If `mermaid-cli` is not installed, the diagram code will be displayed as text instead.

## Quick Start (Automated)

### macOS/Linux

```bash
# Make script executable (first time only)
chmod +x start_application.sh

# Run the application
./start_application.sh --help

# Convert a markdown file
./start_application.sh --word document.md

# Convert to all formats
./start_application.sh --all --output ./output document.md
```

### Windows

```cmd
# Run the application
start_application.bat --help

# Convert a markdown file
start_application.bat --word document.md

# Convert to all formats
start_application.bat --all --output ./output document.md
```

## Manual Setup

If you prefer to set up manually:

### 1. Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 3. Run the Application

```bash
# Show help
python -m md2office --help

# Convert markdown to Word
python -m md2office --word document.md

# Convert to all formats
python -m md2office --all --output ./output document.md

# Convert directory
python -m md2office --word --output ./output ./documents/
```

## Example Usage

### Basic Conversion

```bash
# Convert single file to Word
./start_application.sh --word README.md

# Convert to PowerPoint
./start_application.sh --powerpoint presentation.md

# Convert to PDF
./start_application.sh --pdf document.md

# Convert to all formats
./start_application.sh --all document.md
```

### Advanced Options

```bash
# Custom output directory
./start_application.sh --word --output ./output document.md

# Custom filename
./start_application.sh --word --name report document.md

# Add suffix to filename
./start_application.sh --word --suffix -converted document.md

# Use style preset
./start_application.sh --word --style professional document.md

# Generate table of contents
./start_application.sh --word --toc document.md

# Add page breaks
./start_application.sh --word --page-breaks document.md

# Verbose output
./start_application.sh --word --verbose document.md
```

### Batch Processing

```bash
# Convert multiple files
./start_application.sh --word file1.md file2.md file3.md

# Convert all markdown files in directory
./start_application.sh --word ./documents/
```

## Configuration File

Create a `.md2office.json` file in your project directory:

```json
{
  "defaultFormats": ["word", "powerpoint"],
  "outputDirectory": "./output",
  "style": "professional",
  "pageBreaks": true,
  "tableOfContents": true,
  "bookmarks": true
}
```

Then use it:

```bash
./start_application.sh --config .md2office.json document.md
```

## Troubleshooting

### Virtual Environment Issues

If the script fails to create a virtual environment:

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Try creating venv manually
python3 -m venv venv
source venv/bin/activate
```

### Missing Dependencies

If you get import errors:

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Permission Issues (macOS/Linux)

If you get permission errors:

```bash
chmod +x start_application.sh
```

## Next Steps

1. **Test the installation**: Run `./start_application.sh --help`
2. **Convert a test file**: Try converting the included `test-dry-run.md`
3. **Read the documentation**: Check `README.md` for more details
4. **Build binaries**: See `docs/developer/build.md` for creating portable executables

## Getting Help

```bash
# Show help
./start_application.sh --help

# Show version
./start_application.sh --version
```

