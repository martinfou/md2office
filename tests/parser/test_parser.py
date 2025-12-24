"""
Tests for Markdown Parser

Implements tests for parser module including MarkdownParser and ASTBuilder.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from md2office.parser import MarkdownParser, ASTBuilder, ASTNode, NodeType


class TestMarkdownParser:
    """Test suite for MarkdownParser."""
    
    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return MarkdownParser()
    
    def test_parse_simple_text(self, parser):
        """Test parsing simple text."""
        markdown = "Hello, world!"
        result = parser.parse(markdown)
        assert result is not None
    
    def test_parse_headings(self, parser):
        """Test parsing headings."""
        markdown = "# Heading 1\n## Heading 2"
        result = parser.parse(markdown)
        assert result is not None
    
    def test_parse_empty_string(self, parser):
        """Test parsing empty string."""
        markdown = ""
        result = parser.parse(markdown)
        assert result is not None


class TestASTBuilder:
    """Test suite for ASTBuilder."""
    
    @pytest.fixture
    def builder(self):
        """Create AST builder instance."""
        return ASTBuilder()
    
    def test_build_ast_from_text(self, builder):
        """Test building AST from text."""
        from md2office.parser import MarkdownParser
        markdown = "# Title\n\nSome content."
        parser = MarkdownParser()
        tokens = parser.parse(markdown)
        ast = builder.build(tokens)
        assert ast is not None
        assert isinstance(ast, ASTNode)
    
    def test_build_ast_empty(self, builder):
        """Test building AST from empty content."""
        from md2office.parser import MarkdownParser
        markdown = ""
        parser = MarkdownParser()
        tokens = parser.parse(markdown)
        ast = builder.build(tokens)
        assert ast is not None


class TestASTNode:
    """Test suite for ASTNode."""
    
    def test_create_node(self):
        """Test creating an AST node."""
        node = ASTNode(NodeType.DOCUMENT)
        assert node.node_type == NodeType.DOCUMENT
        assert node.children == []
    
    def test_add_child(self):
        """Test adding child nodes."""
        parent = ASTNode(NodeType.DOCUMENT)
        child = ASTNode(NodeType.PARAGRAPH)
        parent.add_child(child)
        assert len(parent.children) == 1
        assert parent.children[0] == child

