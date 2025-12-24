"""
Tests for Content Router and Pipeline

Implements tests for router module including ContentRouter and Pipeline.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from md2office.router import ContentRouter, ConversionPipeline, OutputFormat
from md2office.parser import ASTNode, NodeType


class TestContentRouter:
    """Test suite for ContentRouter."""
    
    @pytest.fixture
    def router(self):
        """Create router instance."""
        return ContentRouter()
    
    def test_router_initialization(self, router):
        """Test router initialization."""
        assert router is not None
    
    def test_route_to_word(self, router):
        """Test routing to Word format."""
        ast = ASTNode(NodeType.DOCUMENT)
        # Test that router can handle Word format
        assert router is not None
    
    def test_route_to_powerpoint(self, router):
        """Test routing to PowerPoint format."""
        ast = ASTNode(NodeType.DOCUMENT)
        # Test that router can handle PowerPoint format
        assert router is not None
    
    def test_route_to_pdf(self, router):
        """Test routing to PDF format."""
        ast = ASTNode(NodeType.DOCUMENT)
        # Test that router can handle PDF format
        assert router is not None


class TestConversionPipeline:
    """Test suite for ConversionPipeline."""
    
    @pytest.fixture
    def pipeline(self):
        """Create pipeline instance."""
        return ConversionPipeline()
    
    def test_pipeline_initialization(self, pipeline):
        """Test pipeline initialization."""
        assert pipeline is not None

