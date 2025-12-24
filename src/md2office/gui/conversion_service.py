"""
Conversion Service

Shared service for CLI and GUI conversion operations.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from ..router import ConversionPipeline
from ..config import Config, merge_configs, find_config_file, load_config
from ..errors import (
    MD2OfficeError, ParseError, ConversionError, FileError,
    ConfigurationError, setup_logger
)

# Import generators (may be None if dependencies not installed)
try:
    from ..generators import WordGenerator, PowerPointGenerator, PDFGenerator
except ImportError:
    WordGenerator = None
    PowerPointGenerator = None
    PDFGenerator = None


class ConversionService:
    """
    Service for performing conversions.
    
    Provides a clean interface for both CLI and GUI to perform conversions.
    """
    
    def __init__(self):
        """Initialize conversion service."""
        self.pipeline = ConversionPipeline()
        self._ensure_generators_registered()
    
    def _ensure_generators_registered(self):
        """Ensure format generators are registered."""
        if WordGenerator is not None:
            try:
                word_gen = WordGenerator()
                self.pipeline.register_generator('word', word_gen)
            except Exception:
                pass
        
        if PowerPointGenerator is not None:
            try:
                pptx_gen = PowerPointGenerator()
                self.pipeline.register_generator('powerpoint', pptx_gen)
            except Exception:
                pass
        
        if PDFGenerator is not None:
            try:
                pdf_gen = PDFGenerator()
                self.pipeline.register_generator('pdf', pdf_gen)
            except Exception:
                pass
    
    def convert_file(
        self,
        input_path: str,
        formats: List[str],
        output_dir: str = ".",
        output_name: Optional[str] = None,
        output_suffix: Optional[str] = None,
        overwrite: bool = False,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Convert a markdown file to specified formats.
        
        Args:
            input_path: Path to markdown file
            formats: List of format names ('word', 'powerpoint', 'pdf')
            output_dir: Output directory
            output_name: Custom output filename (without extension)
            output_suffix: Suffix to add to output filename
            overwrite: Whether to overwrite existing files
            config: Additional configuration options
            
        Returns:
            Dictionary with 'success', 'output_files', and 'error' keys
        """
        try:
            input_path_obj = Path(input_path)
            
            # Validate input file
            if not input_path_obj.exists():
                return {
                    'success': False,
                    'error': f"Input file not found: {input_path}",
                    'error_type': 'FileNotFound'
                }
            
            if not input_path_obj.is_file():
                return {
                    'success': False,
                    'error': f"Input path is not a file: {input_path}",
                    'error_type': 'InvalidPath'
                }
            
            # Prepare configuration
            base_config = Config()
            # Try to find and load config file
            config_path = find_config_file(str(input_path_obj.parent))
            if config_path:
                try:
                    base_config = load_config(config_path)
                except ConfigurationError:
                    pass  # Ignore config errors
            
            # Merge with provided config
            if config:
                final_config = merge_configs(base_config, config)
            else:
                final_config = base_config
            
            # Determine output filename
            if output_name:
                base_name = output_name
            else:
                base_name = input_path_obj.stem
                if output_suffix:
                    base_name = f"{base_name}{output_suffix}"
            
            # Perform conversion
            results = self.pipeline.convert_file(
                str(input_path_obj),
                formats,
                final_config.to_dict()
            )
            
            # Check for errors in results
            if 'error' in results:
                return {
                    'success': False,
                    'error': results.get('error', 'Unknown conversion error'),
                    'error_type': 'ConversionError'
                }
            
            # Write output files
            output_dir_obj = Path(output_dir)
            output_dir_obj.mkdir(parents=True, exist_ok=True)
            
            output_files = []
            ext_map = {
                'word': '.docx',
                'powerpoint': '.pptx',
                'pdf': '.pdf'
            }
            
            for format_name, doc_bytes in results.items():
                if format_name == 'error':
                    continue
                
                ext = ext_map.get(format_name, f'.{format_name}')
                output_file = output_dir_obj / f"{base_name}{ext}"
                
                # Check if file exists
                if output_file.exists() and not overwrite:
                    return {
                        'success': False,
                        'error': f"Output file already exists: {output_file}",
                        'error_type': 'FileExists',
                        'output_file': str(output_file)
                    }
                
                # Write file
                output_file.write_bytes(doc_bytes)
                output_files.append({
                    'format': format_name,
                    'path': str(output_file),
                    'size': len(doc_bytes)
                })
            
            return {
                'success': True,
                'output_files': output_files,
                'input_file': str(input_path_obj)
            }
        
        except ParseError as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'ParseError',
                'line_number': getattr(e, 'line_number', None)
            }
        
        except ConversionError as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'ConversionError',
                'format': getattr(e, 'format', None)
            }
        
        except FileError as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': 'FileError',
                'file_path': getattr(e, 'file_path', None)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'error_type': 'UnexpectedError'
            }

