"""
Conversion Pipeline

High-level pipeline interface for markdown conversion.
"""

from typing import List, Optional, Dict, Any
from .content_router import ContentRouter, OutputFormat, PipelineOrchestrator


class ConversionPipeline:
    """
    High-level conversion pipeline interface.
    
    Provides a simple interface for converting markdown files
    to various output formats.
    """
    
    def __init__(self):
        """Initialize conversion pipeline."""
        self.router = ContentRouter()
        self.orchestrator = PipelineOrchestrator(self.router)
    
    def convert(self, markdown_content: str, formats: List[str],
                options: Optional[Dict[str, Any]] = None) -> Dict[str, bytes]:
        """
        Convert markdown content to specified formats.
        
        Args:
            markdown_content: Raw markdown text
            formats: List of format names ('word', 'powerpoint', 'pdf')
            options: Conversion options
            
        Returns:
            Dictionary mapping format name to document bytes
        """
        output_formats = [self._parse_format(f) for f in formats]
        results = self.orchestrator.convert(markdown_content, output_formats, options)
        
        # Convert enum keys to string keys
        return {format.value: data for format, data in results.items()}
    
    def convert_file(self, input_path: str, formats: List[str],
                     options: Optional[Dict[str, Any]] = None) -> Dict[str, bytes]:
        """
        Convert markdown file to specified formats.
        
        Args:
            input_path: Path to markdown file
            formats: List of format names
            options: Conversion options
            
        Returns:
            Dictionary mapping format name to document bytes
        """
        output_formats = [self._parse_format(f) for f in formats]
        results = self.orchestrator.convert_file(input_path, output_formats, options)
        
        # Convert enum keys to string keys
        return {format.value: data for format, data in results.items()}
    
    def convert_batch(self, input_paths: List[str], formats: List[str],
                      options: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, bytes]]:
        """
        Convert multiple markdown files.
        
        Args:
            input_paths: List of markdown file paths
            formats: List of format names
            options: Conversion options
            
        Returns:
            Dictionary mapping input path to format results
        """
        output_formats = [self._parse_format(f) for f in formats]
        results = self.orchestrator.convert_batch(input_paths, output_formats, options)
        
        # Convert enum keys to string keys in nested dictionaries
        converted_results = {}
        for path, file_results in results.items():
            if isinstance(file_results, dict) and 'error' not in file_results:
                converted_results[path] = {
                    format.value: data for format, data in file_results.items()
                }
            else:
                converted_results[path] = file_results
        
        return converted_results
    
    def register_generator(self, format_name: str, generator):
        """
        Register a format generator.
        
        Args:
            format_name: Format name ('word', 'powerpoint', 'pdf')
            generator: Format generator instance
        """
        format_enum = self._parse_format(format_name)
        self.router.register_generator(format_enum, generator)
    
    def _parse_format(self, format_name: str) -> OutputFormat:
        """
        Parse format name to OutputFormat enum.
        
        Args:
            format_name: Format name string
            
        Returns:
            OutputFormat enum value
        """
        format_map = {
            'word': OutputFormat.WORD,
            'docx': OutputFormat.WORD,
            'powerpoint': OutputFormat.POWERPOINT,
            'pptx': OutputFormat.POWERPOINT,
            'pdf': OutputFormat.PDF
        }
        
        format_name_lower = format_name.lower()
        if format_name_lower not in format_map:
            raise ValueError(f"Unsupported format: {format_name}")
        
        return format_map[format_name_lower]

