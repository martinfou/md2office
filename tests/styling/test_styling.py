"""
Tests for Styling System

Implements tests for styling module including Style and StyleManager.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from md2office.styling import StyleManager, StylePreset
from md2office.styling.style import (
    FontFamily,
    FontStyle,
    ParagraphStyle,
    HeadingStyle,
)


class TestFontFamily:
    """Test suite for FontFamily enum."""
    
    def test_font_family_values(self):
        """Test font family enum values."""
        assert FontFamily.SANS_SERIF.value == "sans-serif"
        assert FontFamily.SERIF.value == "serif"
        assert FontFamily.MONOSPACE.value == "monospace"


class TestFontStyle:
    """Test suite for FontStyle."""
    
    def test_create_font_style(self):
        """Test creating font style."""
        style = FontStyle(
            family="Arial",
            size=12.0,
            weight="bold",
            color="#000000"
        )
        assert style.family == "Arial"
        assert style.size == 12.0
        assert style.weight == "bold"
        assert style.color == "#000000"
    
    def test_font_style_defaults(self):
        """Test font style defaults."""
        style = FontStyle()
        assert style.family == "sans-serif"
        assert style.size == 12.0
        assert style.weight == "normal"


class TestParagraphStyle:
    """Test suite for ParagraphStyle."""
    
    def test_create_paragraph_style(self):
        """Test creating paragraph style."""
        style = ParagraphStyle()
        assert style is not None


class TestHeadingStyle:
    """Test suite for HeadingStyle."""
    
    def test_create_heading_style(self):
        """Test creating heading style."""
        style = HeadingStyle()
        assert style is not None
        assert style.font is not None


class TestStyleManager:
    """Test suite for StyleManager."""
    
    @pytest.fixture
    def style_manager(self):
        """Create style manager instance."""
        return StyleManager()
    
    def test_style_manager_initialization(self, style_manager):
        """Test style manager initialization."""
        assert style_manager is not None
    
    def test_get_default_preset(self, style_manager):
        """Test getting default preset."""
        preset = style_manager.get_preset("default")
        assert preset is not None
        assert isinstance(preset, StylePreset)
    
    def test_register_custom_preset(self, style_manager):
        """Test registering custom preset."""
        custom_preset = StylePreset(name="custom")
        style_manager.register_preset(custom_preset)
        # Verify preset was registered
        assert style_manager.get_preset("custom") == custom_preset

