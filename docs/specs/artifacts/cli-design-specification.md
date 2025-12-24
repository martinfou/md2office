# CLI Design Specification

## Overview

This specification defines the command-line interface (CLI) for the Copilot Markdown to Office Document Converter tool. The CLI provides an intuitive, user-friendly interface for converting markdown files to Word, PowerPoint, and PDF formats. The design emphasizes ease of use, clear error messages, and flexible options for various conversion scenarios.

### Design Philosophy

1. **Simplicity**: Simple, intuitive command syntax
2. **Flexibility**: Support single files, multiple files, and directories
3. **Clarity**: Clear error messages and user feedback
4. **Efficiency**: Fast conversion with progress indicators
5. **Consistency**: Consistent behavior across platforms

### CLI Goals

- **Easy to Use**: Intuitive command syntax for both technical and non-technical users
- **Flexible**: Support various conversion scenarios (single file, batch, directory)
- **Informative**: Provide clear feedback and error messages
- **Efficient**: Fast conversion with progress indicators
- **Cross-Platform**: Consistent behavior on Windows and Mac

## Command Syntax

### Base Command

The tool uses a single base command with options and arguments:

```
md2office [OPTIONS] <input>
```

**Command Name**: `md2office` (or `md2doc` as alternative)

**Input**: 
- Single markdown file: `document.md`
- Multiple files: `file1.md file2.md file3.md`
- Directory: `./documents/` (converts all .md files in directory)
- Wildcard: `*.md` (shell expansion)

### Basic Usage Patterns

#### Single File Conversion

```bash
# Convert to Word
md2office --word document.md

# Convert to PowerPoint
md2office --powerpoint document.md

# Convert to PDF
md2office --pdf document.md

# Convert to multiple formats
md2office --word --powerpoint --pdf document.md
```

#### Multiple File Conversion

```bash
# Convert multiple files to Word
md2office --word file1.md file2.md file3.md

# Convert with wildcard
md2office --word *.md

# Convert directory
md2office --word ./documents/
```

#### Output Directory Specification

```bash
# Specify output directory
md2office --word --output ./output document.md

# Output to specific directory
md2office --word --output /path/to/output document.md
```

## Command-Line Options

### Output Format Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--word` | `-w` | Convert to Word (.docx) format | No |
| `--powerpoint` | `-p` | Convert to PowerPoint (.pptx) format | No |
| `--pdf` | None | Convert to PDF format | No |
| `--all` | `-a` | Convert to all formats (Word, PowerPoint, PDF) | No |

**Notes**:
- At least one format option must be specified
- Multiple format options can be combined
- `--all` is equivalent to `--word --powerpoint --pdf`

### Output Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Specify output directory | Current directory |
| `--name` | `-n` | Specify output filename (without extension) | Input filename |
| `--overwrite` | None | Overwrite existing files without prompting | Prompt if exists |
| `--suffix` | None | Add suffix to output filename | No suffix |

**Examples**:
```bash
# Output to specific directory
md2office --word --output ./output document.md

# Custom output filename
md2office --word --name report document.md
# Output: report.docx

# Add suffix
md2office --word --suffix -converted document.md
# Output: document-converted.docx
```

### Configuration Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--config` | `-c` | Specify configuration file path | No config file |
| `--style` | `-s` | Specify style preset (default, minimal, professional) | default |

**Configuration File**:
- JSON or YAML format
- Specifies default options, styling, formatting preferences
- Example: `md2office --config config.json document.md`

### Information Options

| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Show help message and exit |
| `--version` | `-v` | Show version information and exit |
| `--verbose` | None | Show detailed progress information |
| `--quiet` | `-q` | Suppress non-error output |

### Advanced Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--page-breaks` | None | Insert page breaks at major sections | No |
| `--toc` | None | Generate table of contents (Word/PDF) | No |
| `--bookmarks` | None | Generate bookmarks (PDF) | Yes (PDF) |
| `--images` | None | Image optimization level (low, medium, high) | medium |

## Command Examples

### Basic Conversion Examples

```bash
# Convert single file to Word
md2office --word document.md

# Convert to all formats
md2office --all document.md

# Convert with custom output directory
md2office --word --output ./output document.md

# Convert multiple files
md2office --word file1.md file2.md file3.md

# Convert directory
md2office --word ./documents/
```

### Advanced Examples

```bash
# Convert with table of contents
md2office --word --toc document.md

# Convert with page breaks
md2office --word --page-breaks document.md

# Convert with custom styling
md2office --word --style professional document.md

# Convert with configuration file
md2office --word --config config.json document.md

# Quiet mode (suppress output)
md2office --word --quiet document.md

# Verbose mode (detailed output)
md2office --word --verbose document.md
```

### Batch Processing Examples

```bash
# Convert all .md files in current directory
md2office --word *.md

# Convert directory recursively (if supported)
md2office --word --recursive ./documents/

# Convert with progress indicator
md2office --word --verbose ./documents/
```

## User Experience

### Error Messages

#### Error Message Format

```
Error: <error-type>: <description>
  <context>
  <suggestion>
```

#### Error Types

1. **File Not Found**
   ```
   Error: File not found: document.md
     The specified file does not exist.
     Suggestion: Check the file path and try again.
   ```

2. **Invalid Format Option**
   ```
   Error: No output format specified
     At least one format option (--word, --powerpoint, --pdf) must be specified.
     Suggestion: Use --word, --powerpoint, --pdf, or --all
   ```

3. **Invalid Markdown**
   ```
   Error: Invalid markdown syntax in document.md
     Line 42: Unexpected character
     Suggestion: Check markdown syntax and try again.
   ```

4. **Missing Dependencies**
   ```
   Error: Missing image file: images/photo.png
     The referenced image file does not exist.
     Suggestion: Check image paths or use --skip-missing-images
   ```

5. **Permission Denied**
   ```
   Error: Permission denied: ./output/
     Cannot write to output directory.
     Suggestion: Check directory permissions or use a different output location.
   ```

### Progress Indicators

#### Single File Conversion

```
Converting document.md to Word format...
  Parsing markdown... ✓
  Processing images... ✓
  Generating document... ✓
  Writing output... ✓
Done! Output: document.docx
```

#### Batch Conversion

```
Converting 5 files to Word format...
  [1/5] file1.md... ✓
  [2/5] file2.md... ✓
  [3/5] file3.md... ✓
  [4/5] file4.md... ✓
  [5/5] file5.md... ✓
Done! 5 files converted successfully.
```

#### Verbose Mode

```
Converting document.md to Word format...
  Parsing markdown...
    Found 12 headings
    Found 3 code blocks
    Found 5 images
  Processing images...
    Resizing image1.png (1200x800 -> 800x533)
    Optimizing image2.jpg (compression: 85%)
  Generating document...
    Creating document structure...
    Applying styles...
    Embedding images...
  Writing output...
    File size: 2.3 MB
Done! Output: document.docx
```

### Help System

#### Help Command Output

```
md2office - Markdown to Office Document Converter

USAGE:
    md2office [OPTIONS] <input>

ARGUMENTS:
    <input>    Markdown file(s) or directory to convert

OPTIONS:
    Output Format:
        --word, -w              Convert to Word (.docx) format
        --powerpoint, -p         Convert to PowerPoint (.pptx) format
        --pdf                    Convert to PDF format
        --all, -a                Convert to all formats

    Output Options:
        --output, -o <dir>       Output directory (default: current directory)
        --name, -n <name>        Output filename (without extension)
        --overwrite              Overwrite existing files without prompting

    Configuration:
        --config, -c <file>      Configuration file path
        --style, -s <preset>     Style preset (default, minimal, professional)

    Information:
        --help, -h               Show this help message
        --version, -v            Show version information
        --verbose                Show detailed progress information
        --quiet, -q              Suppress non-error output

EXAMPLES:
    # Convert to Word
    md2office --word document.md

    # Convert to all formats
    md2office --all document.md

    # Convert with custom output directory
    md2office --word --output ./output document.md

    # Convert multiple files
    md2office --word file1.md file2.md file3.md

For more information, visit: https://github.com/example/md2office
```

### Version Information

#### Version Command Output

```
md2office version 1.0.0
Copyright (c) 2024

Markdown to Office Document Converter
Converts markdown files to Word, PowerPoint, and PDF formats.

Platform: Windows x64 / macOS x64 / macOS ARM64
Build date: 2024-01-15
```

## Configuration File

### Configuration File Format

**JSON Format** (recommended):

```json
{
  "defaultFormats": ["word", "powerpoint"],
  "outputDirectory": "./output",
  "style": "professional",
  "pageBreaks": true,
  "tableOfContents": true,
  "imageOptimization": "medium",
  "overwrite": false
}
```

**YAML Format**:

```yaml
defaultFormats:
  - word
  - powerpoint
outputDirectory: ./output
style: professional
pageBreaks: true
tableOfContents: true
imageOptimization: medium
overwrite: false
```

### Configuration Options

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `defaultFormats` | array | Default output formats | [] |
| `outputDirectory` | string | Default output directory | "." |
| `style` | string | Style preset | "default" |
| `pageBreaks` | boolean | Insert page breaks | false |
| `tableOfContents` | boolean | Generate TOC | false |
| `imageOptimization` | string | Image optimization level | "medium" |
| `overwrite` | boolean | Overwrite existing files | false |

## Exit Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 0 | Success | Conversion completed successfully |
| 1 | General Error | Unspecified error occurred |
| 2 | File Error | File not found or cannot be read |
| 3 | Parse Error | Markdown parsing error |
| 4 | Conversion Error | Document conversion error |
| 5 | Output Error | Cannot write output file |
| 64 | Usage Error | Invalid command-line arguments |

## Implementation Notes

### CLI Framework Options

#### JavaScript/TypeScript

- **Commander.js**: Popular CLI framework
- **Yargs**: Feature-rich CLI framework
- **Ink**: React-based CLI (for complex UIs)

#### Python

- **Click**: Popular CLI framework
- **argparse**: Standard library option
- **Typer**: Modern CLI framework

#### Go

- **Cobra**: Popular CLI framework
- **urfave/cli**: Simple CLI framework

### Input Validation

1. **File Existence**: Check if input files exist
2. **File Format**: Validate markdown file extension
3. **Output Directory**: Check if output directory exists and is writable
4. **Option Validation**: Validate option combinations

### Error Handling

1. **Graceful Degradation**: Continue processing other files if one fails
2. **Error Logging**: Log errors to stderr
3. **Exit Codes**: Use appropriate exit codes
4. **User Feedback**: Provide clear error messages

### Performance Considerations

1. **Parallel Processing**: Process multiple files in parallel (if supported)
2. **Progress Updates**: Provide progress indicators for long operations
3. **Memory Management**: Handle large files efficiently
4. **Caching**: Cache processed images and resources

## Platform-Specific Considerations

### Windows

- **Path Separators**: Handle both `/` and `\` path separators
- **File Extensions**: Case-insensitive file extensions
- **Long Paths**: Support long file paths (if needed)
- **Console Encoding**: Handle UTF-8 encoding properly

### macOS

- **Path Separators**: Use `/` path separators
- **File Extensions**: Case-sensitive file extensions
- **Permissions**: Handle macOS file permissions
- **Console Encoding**: Handle UTF-8 encoding properly

### Cross-Platform Consistency

- **Path Handling**: Use platform-agnostic path handling
- **Line Endings**: Handle different line endings (CRLF vs LF)
- **File Permissions**: Handle platform-specific permissions
- **Error Messages**: Consistent error messages across platforms

## Conclusion

This CLI design specification provides a comprehensive interface for the markdown-to-office document converter tool. The design emphasizes simplicity, flexibility, and user-friendly error handling while supporting various conversion scenarios. Implementation should follow these specifications to create an intuitive and efficient CLI tool.

