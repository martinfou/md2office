"""
Tests for Error Handling System

Implements tests for errors module including exceptions and logging.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from md2office.errors import (
    MD2OfficeError,
    ConfigurationError,
    ParseError,
    ConversionError,
    FileError,
    ValidationError,
)


class TestMD2OfficeError:
    """Test suite for base MD2OfficeError."""
    
    def test_create_error(self):
        """Test creating base error."""
        error = MD2OfficeError("Test error")
        assert "Test error" in str(error)
        assert error.message == "Test error"
    
    def test_error_with_context(self):
        """Test error with context."""
        context = {"file": "test.md"}
        error = MD2OfficeError("Test error", context=context)
        assert error.context == context
    
    def test_error_with_suggestion(self):
        """Test error with suggestion."""
        suggestion = "Try again"
        error = MD2OfficeError("Test error", suggestion=suggestion)
        assert error.suggestion == suggestion


class TestConfigurationError:
    """Test suite for ConfigurationError."""
    
    def test_create_configuration_error(self):
        """Test creating configuration error."""
        error = ConfigurationError("Invalid config")
        assert isinstance(error, MD2OfficeError)
        assert "Invalid config" in str(error)


class TestParseError:
    """Test suite for ParseError."""
    
    def test_create_parse_error(self):
        """Test creating parse error."""
        error = ParseError("Parse failed")
        assert isinstance(error, MD2OfficeError)
        assert "Parse failed" in str(error)


class TestConversionError:
    """Test suite for ConversionError."""
    
    def test_create_conversion_error(self):
        """Test creating conversion error."""
        error = ConversionError("Conversion failed")
        assert isinstance(error, MD2OfficeError)
        assert "Conversion failed" in str(error)


class TestFileError:
    """Test suite for FileError."""
    
    def test_create_file_error(self):
        """Test creating file error."""
        error = FileError("File not found")
        assert isinstance(error, MD2OfficeError)
        assert "File not found" in str(error)


class TestValidationError:
    """Test suite for ValidationError."""
    
    def test_create_validation_error(self):
        """Test creating validation error."""
        error = ValidationError("Validation failed")
        assert isinstance(error, MD2OfficeError)
        assert "Validation failed" in str(error)

