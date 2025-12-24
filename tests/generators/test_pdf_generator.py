"""
Tests for PDF Document Generator

Implements Story 4.3: PDF Testing and Validation
"""

import pytest
import sys
from pathlib import Path

# Add src to path (now in subdirectory, go up two levels)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from md2office.parser import MarkdownParser, ASTBuilder
from md2office.generators import PDFGenerator
from md2office.errors import ConversionError


class TestPDFGenerator:
    """Test suite for PDF generator."""
    
    @pytest.fixture
    def pdf_generator(self):
        """Create PDF generator instance."""
        try:
            return PDFGenerator()
        except ImportError:
            pytest.skip("ReportLab not available")
    
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

## Section 2

```python
def hello():
    print("Hello, World!")
```

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
    
    def test_generator_initialization(self, pdf_generator):
        """Test PDF generator initialization."""
        assert pdf_generator is not None
    
    def test_generate_basic_document(self, pdf_generator, sample_markdown):
        """Test generating a basic PDF document."""
        # Parse markdown
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        
        # Build AST
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        # Generate PDF document
        options = {}
        pdf_bytes = pdf_generator.generate(ast, options)
        
        # Verify document was generated
        assert pdf_bytes is not None
        assert len(pdf_bytes) > 0
        
        # Verify it's a valid PDF file (starts with PDF signature)
        assert pdf_bytes[:4] == b'%PDF'
    
    def test_generate_with_metadata(self, pdf_generator):
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
        pdf_bytes = pdf_generator.generate(ast, options)
        assert pdf_bytes is not None
        assert pdf_bytes[:4] == b'%PDF'
    
    def test_generate_with_style_preset(self, pdf_generator, sample_markdown):
        """Test generating document with style preset."""
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        options = {'style': 'professional'}
        pdf_bytes = pdf_generator.generate(ast, options)
        assert pdf_bytes is not None
        assert pdf_bytes[:4] == b'%PDF'
    
    def test_generate_with_table_of_contents(self, pdf_generator, sample_markdown):
        """Test generating document with table of contents."""
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        options = {'table_of_contents': True}
        pdf_bytes = pdf_generator.generate(ast, options)
        assert pdf_bytes is not None
        assert pdf_bytes[:4] == b'%PDF'
    
    def test_generate_with_page_breaks(self, pdf_generator, sample_markdown):
        """Test generating document with page breaks."""
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        options = {'page_breaks': True}
        pdf_bytes = pdf_generator.generate(ast, options)
        assert pdf_bytes is not None
        assert pdf_bytes[:4] == b'%PDF'
    
    def test_file_extension(self, pdf_generator):
        """Test file extension method."""
        assert pdf_generator.get_file_extension() == ".pdf"


class TestPDFGeneratorIntegration:
    """Integration tests for PDF generator."""
    
    def test_full_conversion_pipeline(self):
        """Test full conversion pipeline from markdown to PDF."""
        try:
            from md2office.router import ConversionPipeline
            from md2office.generators import PDFGenerator
            
            pipeline = ConversionPipeline()
            pdf_gen = PDFGenerator()
            pipeline.register_generator('pdf', pdf_gen)
            
            markdown = """# Test Document

This is a **test** document.
"""
            results = pipeline.convert(markdown, ['pdf'])
            
            assert 'pdf' in results
            assert results['pdf'] is not None
            assert len(results['pdf']) > 0
            assert results['pdf'][:4] == b'%PDF'
        
        except ImportError:
            pytest.skip("ReportLab not available")

