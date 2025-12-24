# GUI User Guide

The md2office graphical user interface provides an intuitive way to convert markdown files to Word, PowerPoint, and PDF formats without using the command line.

## Launching the GUI

You can launch the GUI in several ways:

### Method 1: Command Line Flag
```bash
md2office --gui
```

### Method 2: No Arguments
```bash
md2office
```
If you run md2office without any arguments or input files, it automatically launches the GUI.

### Method 3: Python Module
```bash
python -m md2office --gui
```

## GUI Features

### Main Window

The GUI provides a clean, user-friendly interface with the following sections:

#### 1. Input File Selection

- **File Path Field**: Shows the selected markdown file path
- **Browse Button**: Opens a file picker to select markdown files
- **Drag and Drop**: Simply drag markdown files from your file manager and drop them into the application window

#### 2. Output Format Selection

Choose which formats you want to generate:

- ☑ **Word (.docx)** - Generate Word documents
- ☑ **PowerPoint (.pptx)** - Generate PowerPoint presentations  
- ☑ **PDF** - Generate PDF documents
- ☑ **All Formats** - Generate all three formats at once

**Note**: Checking "All Formats" automatically selects all individual format checkboxes.

#### 3. Output Directory

- **Output Path Field**: Specify where converted files should be saved
- **Browse Button**: Select an output directory using the file picker
- **Default**: If left empty, files are saved in the same directory as the input file

#### 4. Conversion Controls

- **Convert Button**: Starts the conversion process
- **Progress Bar**: Shows conversion progress
- **Status Messages**: Displays current operation status

## Using the GUI

### Basic Workflow

1. **Select Input File**
   - Click "Browse..." next to the Input File field
   - Navigate to your markdown file and select it
   - Or drag and drop a markdown file into the window

2. **Choose Output Formats**
   - Check the boxes for Word, PowerPoint, PDF, or select "All Formats"

3. **Set Output Directory** (Optional)
   - Click "Browse..." next to Output Directory
   - Select where you want the converted files saved
   - Leave empty to save in the same folder as the input file

4. **Start Conversion**
   - Click the "Convert" button
   - Watch the progress bar as files are converted
   - Wait for the "Conversion complete!" message

### Drag and Drop

The GUI supports drag-and-drop for quick file selection:

1. Open the md2office GUI
2. Open your file manager
3. Drag a markdown file (.md) into the md2office window
4. The file path will automatically populate
5. Select formats and click Convert

### Batch Conversion

To convert multiple files:

1. Select the first file and convert it
2. After conversion completes, select another file
3. Repeat as needed

**Note**: The GUI currently converts one file at a time. For batch processing multiple files, use the CLI with wildcards:
```bash
md2office --all *.md
```

## Error Handling

The GUI provides clear error messages if something goes wrong:

- **File Not Found**: If the input file doesn't exist
- **Invalid Format**: If the file isn't a valid markdown file
- **Permission Errors**: If the output directory isn't writable
- **Conversion Errors**: If the conversion process fails

Error messages appear in a popup dialog with details about what went wrong.

## Tips and Best Practices

### Performance
- Converting to all formats takes longer than a single format
- Large markdown files may take more time to process
- The GUI remains responsive during conversion (uses background threads)

### File Organization
- Use descriptive output directories to keep converted files organized
- Consider creating separate folders for different document types
- The GUI remembers your last output directory selection

### Format Selection
- **Word (.docx)**: Best for documents that need editing
- **PowerPoint (.pptx)**: Best for presentations and slides
- **PDF**: Best for final documents and sharing

### Keyboard Shortcuts
- **Enter**: Start conversion (when file is selected)
- **Escape**: Close dialogs
- **Tab**: Navigate between fields

## Troubleshooting

### GUI Won't Launch

**Problem**: GUI doesn't appear when running `md2office --gui`

**Solutions**:
- Ensure PySide6 is installed: `pip install PySide6`
- Check Python version (3.8+ required)
- Try running from project root: `python -m md2office --gui`

### Conversion Fails

**Problem**: Conversion button does nothing or shows error

**Solutions**:
- Verify the input file exists and is readable
- Check that output directory is writable
- Ensure at least one format is selected
- Check file permissions

### Drag and Drop Not Working

**Problem**: Can't drag files into the window

**Solutions**:
- Ensure you're dragging a `.md` file
- Try using the Browse button instead
- Check that the GUI window has focus

### Progress Bar Stuck

**Problem**: Progress bar doesn't move during conversion

**Solutions**:
- Wait a moment - large files take time
- Check system resources (CPU/memory)
- Try converting a smaller file first
- Check console/terminal for error messages

## Advanced Usage

### Configuration

The GUI uses the same configuration system as the CLI. Configuration files are automatically loaded from:
- `~/.md2office/config.yaml` (user config)
- `./md2office.yaml` (project config)

See [Configuration Guide](usage.md#configuration) for details.

### Integration

The GUI can be integrated into workflows:
- Use CLI for automated batch processing
- Use GUI for interactive, one-off conversions
- Both use the same conversion engine for consistent results

## See Also

- [CLI Usage Guide](usage.md) - Command-line interface documentation
- [Quick Start Guide](quickstart.md) - Getting started with md2office
- [Build Guide](../developer/build.md) - Building from source

---

**Last Updated**: 2024

