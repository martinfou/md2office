"""
CLI Main Module

Implements Epic 5: CLI Implementation
Command-line interface for md2office converter.
"""

import sys
import os
from pathlib import Path
from typing import List, Optional

try:
    import click
    CLICK_AVAILABLE = True
except ImportError:
    CLICK_AVAILABLE = False
    # Create dummy click decorator if not available
    def click_command(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    def click_argument(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    def click_option(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    def click_version_option(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    click = type('click', (), {
        'command': click_command,
        'argument': click_argument,
        'option': click_option,
        'Choice': lambda *args, **kwargs: lambda x: x,
        'Path': lambda *args, **kwargs: lambda x: x,
        'version_option': click_version_option,
        'echo': print,
        'prompt': lambda *args, **kwargs: input(),
    })()

from ..router import ConversionPipeline
# Import generators (may be None if dependencies not installed)
try:
    from ..generators import WordGenerator, PowerPointGenerator, PDFGenerator
except ImportError:
    WordGenerator = None
    PowerPointGenerator = None
    PDFGenerator = None
from ..config import Config, load_config, find_config_file, merge_configs
from ..errors import (
    MD2OfficeError, ParseError, ConversionError, FileError,
    ConfigurationError, setup_logger, get_logger
)

__version__ = "0.1.0"


def ensure_generators_registered(pipeline: ConversionPipeline):
    """Ensure format generators are registered."""
    if WordGenerator is not None:
        try:
            word_gen = WordGenerator()
            pipeline.register_generator('word', word_gen)
        except Exception:
            pass  # Generator initialization failed
    
    if PowerPointGenerator is not None:
        try:
            pptx_gen = PowerPointGenerator()
            pipeline.register_generator('powerpoint', pptx_gen)
        except Exception:
            pass  # Generator initialization failed
    
    if PDFGenerator is not None:
        try:
            pdf_gen = PDFGenerator()
            pipeline.register_generator('pdf', pdf_gen)
        except Exception:
            pass  # Generator initialization failed


@click.command()
@click.argument('inputs', nargs=-1, required=False, type=click.Path(exists=True))
@click.option('--gui', is_flag=True, help='Launch graphical user interface')
@click.option('--word', '-w', is_flag=True, help='Convert to Word (.docx) format')
@click.option('--powerpoint', '-p', is_flag=True, help='Convert to PowerPoint (.pptx) format')
@click.option('--pdf', is_flag=True, help='Convert to PDF format')
@click.option('--all', '-a', is_flag=True, help='Convert to all formats')
@click.option('--output', '-o', type=click.Path(), default='.', help='Output directory')
@click.option('--name', '-n', type=str, help='Output filename (without extension)')
@click.option('--suffix', type=str, help='Add suffix to output filename')
@click.option('--overwrite', is_flag=True, help='Overwrite existing files without prompting')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--style', '-s', type=click.Choice(['default', 'minimal', 'professional']), 
              default='default', help='Style preset')
@click.option('--verbose', is_flag=True, help='Show detailed progress information')
@click.option('--quiet', '-q', is_flag=True, help='Suppress non-error output')
@click.option('--page-breaks', is_flag=True, help='Insert page breaks at major sections')
@click.option('--toc', is_flag=True, help='Generate table of contents (Word/PDF)')
@click.option('--bookmarks/--no-bookmarks', default=True, help='Generate bookmarks (PDF)')
@click.option('--skip-missing-images', is_flag=True, help='Skip missing image files')
@click.version_option(version=__version__, prog_name='md2office')
def cli(inputs, gui, word, powerpoint, pdf, all, output, name, suffix, overwrite,
        config, style, verbose, quiet, page_breaks, toc, bookmarks, skip_missing_images):
    """
    Convert markdown files to Word, PowerPoint, and PDF formats.
    
    INPUTS: Markdown file(s) or directory to convert
    
    If no inputs are provided and --gui is not specified, GUI will be launched automatically.
    """
    # Check for GUI mode
    if gui or (not inputs and not any([word, powerpoint, pdf, all])):
        try:
            from ..gui.gui_main import main as gui_main
            gui_main()
            return
        except ImportError:
            if gui:
                click.echo("Error: GUI is not available. PySide6 may not be installed.", err=True)
                click.echo("\nInstall GUI dependencies with:", err=True)
                click.echo("  pip install PySide6", err=True)
                click.echo("\nOr install all dependencies:", err=True)
                click.echo("  pip install -r requirements.txt", err=True)
                sys.exit(1)
            # If GUI not available and no explicit --gui flag, continue with CLI
    
    # Set up logging
    logger = setup_logger(verbose=verbose, quiet=quiet)
    
    try:
        # Validate inputs
        if not inputs:
            click.echo("Error: No input files specified", err=True)
            click.echo("\nUsage: md2office [OPTIONS] INPUT [INPUT ...]", err=True)
            click.echo("  INPUT: Markdown file(s) or directory containing .md files", err=True)
            click.echo("\nExample:", err=True)
            click.echo("  md2office --word document.md", err=True)
            click.echo("  md2office --all --output ./output ./docs/", err=True)
            sys.exit(1)
        
        # Determine output formats
        formats = []
        if all:
            formats = ['word', 'powerpoint', 'pdf']
        else:
            if word:
                formats.append('word')
            if powerpoint:
                formats.append('powerpoint')
            if pdf:
                formats.append('pdf')
        
        if not formats:
            click.echo("Error: No output format specified", err=True)
            click.echo("\nPlease specify at least one output format:", err=True)
            click.echo("  --word, -w       Convert to Word (.docx) format", err=True)
            click.echo("  --powerpoint, -p Convert to PowerPoint (.pptx) format", err=True)
            click.echo("  --pdf            Convert to PDF format", err=True)
            click.echo("  --all, -a        Convert to all formats", err=True)
            click.echo("\nExample:", err=True)
            click.echo("  md2office --word document.md", err=True)
            sys.exit(1)
        
        # Load configuration file if specified
        base_config = Config()
        if config:
            try:
                base_config = load_config(config)
            except ConfigurationError as e:
                click.echo(f"Error loading configuration file '{config}': {e}", err=True)
                if hasattr(e, 'suggestion') and e.suggestion:
                    click.echo(f"Suggestion: {e.suggestion}", err=True)
                click.echo("\nPlease check:", err=True)
                click.echo("  - File exists and is readable", err=True)
                click.echo("  - File is valid JSON or YAML", err=True)
                click.echo("  - Configuration keys are correct", err=True)
                sys.exit(1)
        else:
            # Try to find config file automatically
            config_path = find_config_file()
            if config_path:
                try:
                    base_config = load_config(config_path)
                except ConfigurationError:
                    pass  # Ignore errors in auto-found config
        
        # Merge CLI options with config
        cli_options = {
            'style': style,
            'pageBreaks': page_breaks,
            'tableOfContents': toc,
            'bookmarks': bookmarks,
            'skipMissingImages': skip_missing_images,
            'overwrite': overwrite,
            'verbose': verbose,
            'quiet': quiet
        }
        
        config_obj = merge_configs(base_config, cli_options)
        
        # Initialize pipeline
        pipeline = ConversionPipeline()
        ensure_generators_registered(pipeline)
        
        # Collect input files
        input_files = []
        for input_path in inputs:
            path = Path(input_path)
            if path.is_file():
                if path.suffix.lower() == '.md':
                    input_files.append(str(path))
            elif path.is_dir():
                # Add all .md files in directory
                for md_file in path.glob('*.md'):
                    input_files.append(str(md_file))
            else:
                click.echo(f"Warning: '{input_path}' is not a valid file or directory", err=True)
                click.echo(f"  Skipping: {input_path}", err=True)
        
        if not input_files:
            click.echo("Error: No markdown files found", err=True)
            click.echo("\nPlease check:", err=True)
            click.echo("  - Input files have .md extension", err=True)
            click.echo("  - Files exist and are readable", err=True)
            click.echo("  - Directory contains .md files (if using directory input)", err=True)
            click.echo("\nExample:", err=True)
            click.echo("  md2office --word document.md", err=True)
            click.echo("  md2office --all ./docs/", err=True)
            sys.exit(1)
        
        # Process files
        output_dir = Path(output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        success_count = 0
        error_count = 0
        
        for input_file in input_files:
            try:
                input_path = Path(input_file)
                
                # Determine output filename
                if name:
                    base_name = name
                else:
                    base_name = input_path.stem
                    if suffix:
                        base_name = f"{base_name}{suffix}"
                
                # Convert
                if not quiet:
                    click.echo(f"Converting {input_path.name}...", err=True)
                
                results = pipeline.convert_file(
                    str(input_path),
                    formats,
                    config_obj.to_dict()
                )
                
                # Write output files
                for format_name, doc_bytes in results.items():
                    if format_name == 'error':
                        continue
                    
                    ext_map = {
                        'word': '.docx',
                        'powerpoint': '.pptx',
                        'pdf': '.pdf'
                    }
                    ext = ext_map.get(format_name, f'.{format_name}')
                    output_file = output_dir / f"{base_name}{ext}"
                    
                    # Check if file exists
                    if output_file.exists() and not overwrite:
                        if not quiet:
                            response = click.prompt(
                                f"{output_file.name} already exists. Overwrite? [y/N]",
                                default='n'
                            )
                            if response.lower() != 'y':
                                continue
                    
                    # Write file
                    output_file.write_bytes(doc_bytes)
                    
                    if not quiet:
                        click.echo(f"  Created: {output_file}", err=True)
                
                success_count += 1
                
            except Exception as e:
                error_count += 1
                input_path = Path(input_file)
                
                if isinstance(e, ParseError):
                    click.echo(f"\nError: Failed to parse '{input_path.name}'", err=True)
                    if hasattr(e, 'line_number') and e.line_number:
                        click.echo(f"  Location: Line {e.line_number}", err=True)
                    click.echo(f"  Reason: {e.message}", err=True)
                    if hasattr(e, 'suggestion') and e.suggestion:
                        click.echo(f"  Suggestion: {e.suggestion}", err=True)
                    if verbose and hasattr(e, 'content') and e.content:
                        click.echo(f"  Content: {e.content[:100]}...", err=True)
                
                elif isinstance(e, ConversionError):
                    click.echo(f"\nError: Failed to convert '{input_path.name}'", err=True)
                    if hasattr(e, 'format') and e.format:
                        click.echo(f"  Format: {e.format.upper()}", err=True)
                    if hasattr(e, 'stage') and e.stage:
                        click.echo(f"  Stage: {e.stage}", err=True)
                    click.echo(f"  Reason: {e.message}", err=True)
                    if hasattr(e, 'suggestion') and e.suggestion:
                        click.echo(f"  Suggestion: {e.suggestion}", err=True)
                    # Check for common issues
                    if 'image' in str(e).lower() or 'file' in str(e).lower():
                        click.echo("\n  Common solutions:", err=True)
                        click.echo("    - Use --skip-missing-images to skip missing images", err=True)
                        click.echo("    - Check that image paths in markdown are correct", err=True)
                        click.echo("    - Ensure image files exist relative to markdown file", err=True)
                
                elif isinstance(e, FileError):
                    click.echo(f"\nError: File operation failed for '{input_path.name}'", err=True)
                    if hasattr(e, 'file_path') and e.file_path:
                        click.echo(f"  File: {e.file_path}", err=True)
                    if hasattr(e, 'operation') and e.operation:
                        click.echo(f"  Operation: {e.operation}", err=True)
                    click.echo(f"  Reason: {e.message}", err=True)
                    if hasattr(e, 'suggestion') and e.suggestion:
                        click.echo(f"  Suggestion: {e.suggestion}", err=True)
                
                elif isinstance(e, ConfigurationError):
                    click.echo(f"\nError: Configuration error", err=True)
                    click.echo(f"  Reason: {e.message}", err=True)
                    if hasattr(e, 'suggestion') and e.suggestion:
                        click.echo(f"  Suggestion: {e.suggestion}", err=True)
                
                elif isinstance(e, MD2OfficeError):
                    click.echo(f"\nError converting '{input_path.name}': {e.message}", err=True)
                    if hasattr(e, 'context') and e.context:
                        context_str = ", ".join([f"{k}={v}" for k, v in e.context.items()])
                        click.echo(f"  Context: {context_str}", err=True)
                    if hasattr(e, 'suggestion') and e.suggestion:
                        click.echo(f"  Suggestion: {e.suggestion}", err=True)
                
                else:
                    click.echo(f"\nError: Unexpected error converting '{input_path.name}'", err=True)
                    click.echo(f"  Type: {type(e).__name__}", err=True)
                    click.echo(f"  Message: {str(e)}", err=True)
                    click.echo("\n  This may be a bug. Please report it with:", err=True)
                    click.echo("    - The full error message (use --verbose)", err=True)
                    click.echo("    - Your input file (if possible)", err=True)
                    click.echo("    - Your command line arguments", err=True)
                    if verbose:
                        import traceback
                        click.echo("\n  Full traceback:", err=True)
                        traceback.print_exc()
                    else:
                        click.echo("\n  Run with --verbose for more details", err=True)
        
        # Summary
        if not quiet:
            click.echo(f"\nConversion complete: {success_count} succeeded, {error_count} failed", err=True)
        
        if error_count > 0:
            sys.exit(1)
    
    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user", err=True)
        click.echo("Conversion cancelled. Partial files may have been created.", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"\nUnexpected error: {type(e).__name__}: {str(e)}", err=True)
        click.echo("\nThis appears to be an unexpected error. Please:", err=True)
        click.echo("  1. Run with --verbose for detailed error information", err=True)
        click.echo("  2. Check that all dependencies are installed:", err=True)
        click.echo("     pip install -r requirements.txt", err=True)
        click.echo("  3. Report this issue with the full error details", err=True)
        if verbose:
            import traceback
            click.echo("\nFull traceback:", err=True)
            traceback.print_exc()
        sys.exit(1)


def main():
    """
    Main entry point for CLI/GUI.
    
    Detects whether to launch GUI or CLI based on arguments.
    
    Raises:
        SystemExit: If Click is not available or CLI execution fails
    """
    # Check if GUI should be launched (no arguments)
    if len(sys.argv) == 1:
        try:
            from ..gui.gui_main import main as gui_main
            gui_main()
            return
        except ImportError:
            # GUI not available, fall through to CLI
            pass
    
    if not CLICK_AVAILABLE:
        click.echo("Error: Click is required for CLI", err=True)
        click.echo("\nInstall Click with:", err=True)
        click.echo("  pip install click", err=True)
        click.echo("\nOr install all dependencies:", err=True)
        click.echo("  pip install -r requirements.txt", err=True)
        sys.exit(1)
    
    cli()


if __name__ == '__main__':
    main()

