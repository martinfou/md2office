"""
Tests for Word Document Generator

Implements Story 2.5: Word Testing and Validation
"""

import pytest
import sys
from pathlib import Path

# Add src to path (now in subdirectory, go up two levels)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from md2office.parser import MarkdownParser, ASTBuilder
from md2office.generators import WordGenerator
from md2office.errors import ConversionError


class TestWordGenerator:
    """Test suite for Word generator."""
    
    @pytest.fixture
    def word_generator(self):
        """Create Word generator instance."""
        try:
            return WordGenerator()
        except ImportError:
            pytest.skip("python-docx not available")
    
    @pytest.fixture
    def sample_markdown(self):
        """Sample markdown content for testing."""
        return """# Test Document

This is a test document with **bold** and *italic* text.

## Section 1

Some content here.

### Subsection

- Item 1
- Item 2
  - Nested item

## Section 2

```python
def hello():
    print("Hello, World!")
```

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
    
    def test_generator_initialization(self, word_generator):
        """Test Word generator initialization."""
        assert word_generator is not None
    
    def test_generate_basic_document(self, word_generator, sample_markdown):
        """Test generating a basic Word document."""
        # Parse markdown
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        
        # Build AST
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        # Generate Word document
        options = {}
        doc_bytes = word_generator.generate(ast, options)
        
        # Verify document was generated
        assert doc_bytes is not None
        assert len(doc_bytes) > 0
        
        # Verify it's a valid DOCX file (starts with ZIP signature)
        assert doc_bytes[:2] == b'PK'  # ZIP file signature
    
    def test_generate_with_metadata(self, word_generator):
        """Test generating document with metadata."""
        markdown = """---
title: Test Document
author: Test Author
---

# Test Document

Content here.
"""
        parser = MarkdownParser()
        tokens = parser.parse(markdown)
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        options = {}
        doc_bytes = word_generator.generate(ast, options)
        assert doc_bytes is not None
    
    def test_generate_with_style_preset(self, word_generator, sample_markdown):
        """Test generating document with style preset."""
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        options = {'style': 'professional'}
        doc_bytes = word_generator.generate(ast, options)
        assert doc_bytes is not None
    
    def test_generate_with_table_of_contents(self, word_generator, sample_markdown):
        """Test generating document with table of contents."""
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        options = {'table_of_contents': True}
        doc_bytes = word_generator.generate(ast, options)
        assert doc_bytes is not None
    
    def test_generate_with_page_breaks(self, word_generator, sample_markdown):
        """Test generating document with page breaks."""
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        options = {'page_breaks': True}
        doc_bytes = word_generator.generate(ast, options)
        assert doc_bytes is not None
    
    def test_file_extension(self, word_generator):
        """Test file extension method."""
        assert word_generator.get_file_extension() == ".docx"


class TestWordGeneratorIntegration:
    """Integration tests for Word generator."""
    
    def test_full_conversion_pipeline(self):
        """Test full conversion pipeline from markdown to Word."""
        try:
            from md2office.router import ConversionPipeline
            from md2office.generators import WordGenerator
            
            pipeline = ConversionPipeline()
            word_gen = WordGenerator()
            pipeline.register_generator('word', word_gen)
            
            markdown = """# Test Document

This is a **test** document.
"""
            results = pipeline.convert(markdown, ['word'])
            
            assert 'word' in results
            assert results['word'] is not None
            assert len(results['word']) > 0
        
        except ImportError:
            pytest.skip("python-docx not available")

