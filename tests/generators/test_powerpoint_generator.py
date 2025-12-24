"""
Tests for PowerPoint Document Generator

Implements Story 3.5: PowerPoint Testing and Validation
"""

import pytest
import sys
from pathlib import Path

# Add src to path (now in subdirectory, go up two levels)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from md2office.parser import MarkdownParser, ASTBuilder
from md2office.generators import PowerPointGenerator
from md2office.errors import ConversionError


class TestPowerPointGenerator:
    """Test suite for PowerPoint generator."""
    
    @pytest.fixture
    def powerpoint_generator(self):
        """Create PowerPoint generator instance."""
        try:
            return PowerPointGenerator()
        except ImportError:
            pytest.skip("python-pptx not available")
    
    @pytest.fixture
    def sample_markdown(self):
        """Sample markdown content for testing."""
        return """# Test Presentation

This is a test presentation.

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
    
    def test_generator_initialization(self, powerpoint_generator):
        """Test PowerPoint generator initialization."""
        assert powerpoint_generator is not None
    
    def test_generate_basic_presentation(self, powerpoint_generator, sample_markdown):
        """Test generating a basic PowerPoint presentation."""
        # Parse markdown
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        
        # Build AST
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        # Generate PowerPoint presentation
        options = {}
        pptx_bytes = powerpoint_generator.generate(ast, options)
        
        # Verify presentation was generated
        assert pptx_bytes is not None
        assert len(pptx_bytes) > 0
        
        # Verify it's a valid PPTX file (starts with ZIP signature)
        assert pptx_bytes[:2] == b'PK'  # ZIP file signature
    
    def test_generate_with_metadata(self, powerpoint_generator):
        """Test generating presentation with metadata."""
        markdown = """---
title: Test Presentation
author: Test Author
---

# Test Presentation

Content here.
"""
        parser = MarkdownParser()
        tokens = parser.parse(markdown)
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        options = {}
        pptx_bytes = powerpoint_generator.generate(ast, options)
        assert pptx_bytes is not None
    
    def test_generate_with_style_preset(self, powerpoint_generator, sample_markdown):
        """Test generating presentation with style preset."""
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        options = {'style': 'professional'}
        pptx_bytes = powerpoint_generator.generate(ast, options)
        assert pptx_bytes is not None
    
    def test_slide_structure(self, powerpoint_generator, sample_markdown):
        """Test that slides are created correctly."""
        parser = MarkdownParser()
        tokens = parser.parse(sample_markdown)
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        options = {}
        pptx_bytes = powerpoint_generator.generate(ast, options)
        
        # Verify presentation structure
        from pptx import Presentation
        from io import BytesIO
        
        pres = Presentation(BytesIO(pptx_bytes))
        assert len(pres.slides) > 0  # Should have at least title slide
    
    def test_file_extension(self, powerpoint_generator):
        """Test file extension method."""
        assert powerpoint_generator.get_file_extension() == ".pptx"


class TestPowerPointGeneratorIntegration:
    """Integration tests for PowerPoint generator."""
    
    def test_full_conversion_pipeline(self):
        """Test full conversion pipeline from markdown to PowerPoint."""
        try:
            from md2office.router import ConversionPipeline
            from md2office.generators import PowerPointGenerator
            
            pipeline = ConversionPipeline()
            pptx_gen = PowerPointGenerator()
            pipeline.register_generator('powerpoint', pptx_gen)
            
            markdown = """# Test Presentation

This is a **test** presentation.
"""
            results = pipeline.convert(markdown, ['powerpoint'])
            
            assert 'powerpoint' in results
            assert results['powerpoint'] is not None
            assert len(results['powerpoint']) > 0
        
        except ImportError:
            pytest.skip("python-pptx not available")

