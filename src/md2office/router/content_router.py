"""
Content Router and Pipeline Orchestration

Implements Story 1.3: Content Router and Pipeline Orchestration
Routes parsed content to appropriate format generators.
"""

from typing import List, Optional, Dict, Any, Callable
from enum import Enum
from abc import ABC, abstractmethod
from ..parser.ast_builder import ASTNode, StructureAnalyzer


class OutputFormat(Enum):
    """Supported output formats."""
    WORD = "word"
    POWERPOINT = "powerpoint"
    PDF = "pdf"


class FormatGenerator(ABC):
    """Abstract base class for format generators."""
    
    @abstractmethod
    def generate(self, ast: ASTNode, options: Dict[str, Any]) -> bytes:
        """
        Generate document from AST.
        
        Args:
            ast: Root AST node
            options: Generation options
            
        Returns:
            Generated document as bytes
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Get file extension for this format."""
        pass


class ContentRouter:
    """
    Routes content to appropriate format generators.
    
    Supports single and multi-format conversion scenarios.
    """
    
    def __init__(self):
        """Initialize content router."""
        self.generators: Dict[OutputFormat, FormatGenerator] = {}
    
    def register_generator(self, format: OutputFormat, generator: FormatGenerator):
        """
        Register a format generator.
        
        Args:
            format: Output format
            generator: Format generator instance
        """
        self.generators[format] = generator
    
    def route(self, ast: ASTNode, formats: List[OutputFormat], 
              options: Optional[Dict[str, Any]] = None) -> Dict[OutputFormat, bytes]:
        """
        Route AST to specified format generators.
        
        Args:
            ast: Root AST node
            formats: List of output formats to generate
            options: Generation options
            
        Returns:
            Dictionary mapping format to generated document bytes
            
        Raises:
            ValueError: If format generator is not registered
        """
        if options is None:
            options = {}
        
        results = {}
        
        for format in formats:
            if format not in self.generators:
                raise ValueError(f"Generator for format {format.value} is not registered")
            
            generator = self.generators[format]
            results[format] = generator.generate(ast, options)
        
        return results
    
    def get_supported_formats(self) -> List[OutputFormat]:
        """Get list of supported output formats."""
        return list(self.generators.keys())


class PipelineOrchestrator:
    """
    Orchestrates the conversion pipeline.
    
    Manages the flow from markdown input through parsing,
    AST building, analysis, and format generation.
    """
    
    def __init__(self, router: ContentRouter):
        """
        Initialize pipeline orchestrator.
        
        Args:
            router: Content router instance
        """
        self.router = router
    
    def convert(self, markdown_content: str, formats: List[OutputFormat],
                options: Optional[Dict[str, Any]] = None) -> Dict[OutputFormat, bytes]:
        """
        Convert markdown to specified formats.
        
        Args:
            markdown_content: Raw markdown text
            formats: List of output formats
            options: Conversion options
            
        Returns:
            Dictionary mapping format to generated document bytes
        """
        from ..parser.markdown_parser import MarkdownParser
        from ..parser.ast_builder import ASTBuilder, StructureAnalyzer
        
        if options is None:
            options = {}
        
        # Stage 1: Parse markdown
        parser = MarkdownParser()
        tokens = parser.parse(markdown_content)
        
        # Validate tokens
        errors = parser.validate(tokens)
        if errors and not options.get('ignore_errors', False):
            raise ValueError(f"Markdown parsing errors: {errors}")
        
        # Stage 2: Build AST
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        # Stage 3: Analyze structure
        analyzer = StructureAnalyzer(ast)
        analysis = analyzer.analyze()
        
        # Add analysis to options
        if options is None:
            options = {}
        options['structure_analysis'] = analysis
        
        # Stage 4: Route to format generators
        results = self.router.route(ast, formats, options)
        
        return results
    
    def convert_file(self, input_path: str, formats: List[OutputFormat],
                     options: Optional[Dict[str, Any]] = None) -> Dict[OutputFormat, bytes]:
        """
        Convert markdown file to specified formats.
        
        Args:
            input_path: Path to markdown file
            formats: List of output formats
            options: Conversion options
            
        Returns:
            Dictionary mapping format to generated document bytes
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        return self.convert(markdown_content, formats, options)
    
    def convert_batch(self, input_paths: List[str], formats: List[OutputFormat],
                      options: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[OutputFormat, bytes]]:
        """
        Convert multiple markdown files.
        
        Args:
            input_paths: List of markdown file paths
            formats: List of output formats
            options: Conversion options
            
        Returns:
            Dictionary mapping input path to format results
        """
        results = {}
        
        for input_path in input_paths:
            try:
                file_results = self.convert_file(input_path, formats, options)
                results[input_path] = file_results
            except Exception as e:
                if options and options.get('continue_on_error', False):
                    results[input_path] = {'error': str(e)}
                else:
                    raise
        
        return results

