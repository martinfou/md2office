"""
Error Handling and Logging System

Implements Story 1.4: Error Handling and Logging System
Comprehensive error types and exception handling.
"""

from typing import Optional, Dict, Any


class MD2OfficeError(Exception):
    """
    Base exception for all md2office errors.
    
    Provides consistent error formatting and user-friendly messages.
    """
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None,
                 suggestion: Optional[str] = None):
        """
        Initialize error.
        
        Args:
            message: Error message
            context: Additional context information
            suggestion: Suggested action to resolve error
        """
        super().__init__(message)
        self.message = message
        self.context = context or {}
        self.suggestion = suggestion
    
    def __str__(self) -> str:
        """Format error message with context and suggestion."""
        parts = [f"Error: {self.message}"]
        
        if self.context:
            context_str = ", ".join([f"{k}={v}" for k, v in self.context.items()])
            parts.append(f"  Context: {context_str}")
        
        if self.suggestion:
            parts.append(f"  Suggestion: {self.suggestion}")
        
        return "\n".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        return {
            'error': self.__class__.__name__,
            'message': self.message,
            'context': self.context,
            'suggestion': self.suggestion
        }


class ParseError(MD2OfficeError):
    """Error during markdown parsing."""
    
    def __init__(self, message: str, line_number: Optional[int] = None,
                 content: Optional[str] = None):
        """
        Initialize parse error.
        
        Args:
            message: Error message
            line_number: Line number where error occurred
            content: Content that caused error
        """
        context = {}
        if line_number is not None:
            context['line_number'] = line_number
        if content:
            context['content'] = content[:100]  # Limit content length
        
        suggestion = "Check markdown syntax and try again."
        if line_number:
            suggestion = f"Check markdown syntax at line {line_number} and try again."
        
        super().__init__(message, context, suggestion)
        self.line_number = line_number
        self.content = content


class ConversionError(MD2OfficeError):
    """Error during document conversion."""
    
    def __init__(self, message: str, format: Optional[str] = None,
                 stage: Optional[str] = None):
        """
        Initialize conversion error.
        
        Args:
            message: Error message
            format: Output format that failed
            stage: Conversion stage where error occurred
        """
        context = {}
        if format:
            context['format'] = format
        if stage:
            context['stage'] = stage
        
        suggestion = "Check input markdown and conversion options."
        
        super().__init__(message, context, suggestion)
        self.format = format
        self.stage = stage


class FileError(MD2OfficeError):
    """Error related to file operations."""
    
    def __init__(self, message: str, file_path: Optional[str] = None,
                 operation: Optional[str] = None):
        """
        Initialize file error.
        
        Args:
            message: Error message
            file_path: File path that caused error
            operation: Operation that failed (read, write, etc.)
        """
        context = {}
        if file_path:
            context['file_path'] = file_path
        if operation:
            context['operation'] = operation
        
        suggestion = "Check file path and permissions."
        if operation == 'read':
            suggestion = "Check that the file exists and is readable."
        elif operation == 'write':
            suggestion = "Check directory permissions and disk space."
        
        super().__init__(message, context, suggestion)
        self.file_path = file_path
        self.operation = operation


class ConfigurationError(MD2OfficeError):
    """Error in configuration."""
    
    def __init__(self, message: str, config_key: Optional[str] = None,
                 config_file: Optional[str] = None):
        """
        Initialize configuration error.
        
        Args:
            message: Error message
            config_key: Configuration key that caused error
            config_file: Configuration file path
        """
        context = {}
        if config_key:
            context['config_key'] = config_key
        if config_file:
            context['config_file'] = config_file
        
        suggestion = "Check configuration file syntax and values."
        
        super().__init__(message, context, suggestion)
        self.config_key = config_key
        self.config_file = config_file


class ValidationError(MD2OfficeError):
    """Error in input validation."""
    
    def __init__(self, message: str, field: Optional[str] = None,
                 value: Optional[Any] = None):
        """
        Initialize validation error.
        
        Args:
            message: Error message
            field: Field that failed validation
            value: Invalid value
        """
        context = {}
        if field:
            context['field'] = field
        if value is not None:
            context['value'] = str(value)
        
        suggestion = "Check input values and try again."
        
        super().__init__(message, context, suggestion)
        self.field = field
        self.value = value

