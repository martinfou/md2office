#!/usr/bin/env python3
"""
Dry Run Test Script

Tests the md2office converter implementation without generating actual output files.
Validates that all components work together correctly.
"""

import sys
import os
from pathlib import Path

# Add src to path (dry_run.py is now in scripts/, so go up one level)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("=" * 60)
    print("TEST 1: Module Imports")
    print("=" * 60)
    
    try:
        from md2office.parser import MarkdownParser, ASTBuilder, StructureAnalyzer
        print("✅ Parser modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import parser modules: {e}")
        return False
    
    try:
        from md2office.router import ConversionPipeline, ContentRouter
        print("✅ Router modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import router modules: {e}")
        return False
    
    try:
        from md2office.errors import MD2OfficeError, ParseError, ConversionError
        print("✅ Error modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import error modules: {e}")
        return False
    
    try:
        from md2office.config import Config, load_config
        print("✅ Config modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import config modules: {e}")
        return False
    
    try:
        from md2office.styling import StylePreset, get_style_preset
        print("✅ Styling modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import styling modules: {e}")
        return False
    
    try:
        from md2office.generators import WordGenerator, PowerPointGenerator, PDFGenerator
        print("✅ Generator modules imported successfully")
    except ImportError as e:
        print(f"⚠️  Generator modules not available (dependencies may be missing): {e}")
        print("   This is expected if python-docx, python-pptx, or reportlab are not installed")
        # Don't fail - generators are optional for basic testing
    
    try:
        from md2office.cli import cli, main
        print("✅ CLI modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import CLI modules: {e}")
        return False
    
    print()
    return True


def test_markdown_parsing():
    """Test markdown parsing."""
    print("=" * 60)
    print("TEST 2: Markdown Parsing")
    print("=" * 60)
    
    try:
        from md2office.parser import MarkdownParser
        
        markdown_content = """# Test Document

This is a **test** document with *formatting*.

## Section 1

- Item 1
- Item 2

```python
def test():
    pass
```

| Header | Value |
|--------|-------|
| Test   | Data  |
"""
        
        parser = MarkdownParser()
        tokens = parser.parse(markdown_content)
        
        print(f"✅ Parsed {len(tokens)} tokens")
        
        # Validate tokens
        errors = parser.validate(tokens)
        if errors:
            print(f"⚠️  Validation warnings: {len(errors)}")
            for error in errors[:3]:  # Show first 3
                print(f"   - {error}")
        else:
            print("✅ No validation errors")
        
        print()
        return True, tokens
    
    except Exception as e:
        print(f"❌ Markdown parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_ast_building(tokens):
    """Test AST building."""
    print("=" * 60)
    print("TEST 3: AST Building")
    print("=" * 60)
    
    if tokens is None:
        print("⚠️  Skipping AST test (no tokens)")
        return False, None
    
    try:
        from md2office.parser import ASTBuilder, StructureAnalyzer
        
        builder = ASTBuilder()
        ast = builder.build(tokens)
        
        print(f"✅ AST built successfully")
        print(f"   Root node type: {ast.node_type.value}")
        print(f"   Root children: {len(ast.children)}")
        
        # Analyze structure
        analyzer = StructureAnalyzer(ast)
        analysis = analyzer.analyze()
        
        print(f"✅ Structure analysis complete")
        print(f"   Total headings: {analysis['heading_hierarchy']['total_headings']}")
        print(f"   Sections: {len(analysis['sections'])}")
        print(f"   Content types: {len(analysis['content_types'])}")
        
        print()
        return True, ast
    
    except Exception as e:
        print(f"❌ AST building failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_generators(ast):
    """Test format generators."""
    print("=" * 60)
    print("TEST 4: Format Generators")
    print("=" * 60)
    
    if ast is None:
        print("⚠️  Skipping generator tests (no AST)")
        return False
    
    results = {}
    
    # Test Word Generator
    try:
        from md2office.generators import WordGenerator
        if WordGenerator is None:
            print("⚠️  Word generator not available (python-docx not installed)")
            results['word'] = False
        else:
            word_gen = WordGenerator()
            print("✅ Word generator initialized")
            print("   ✅ Word generator ready")
            results['word'] = True
    except ImportError:
        print("⚠️  Word generator not available (python-docx not installed)")
        results['word'] = False
    except Exception as e:
        print(f"❌ Word generator error: {e}")
        results['word'] = False
    
    # Test PowerPoint Generator
    try:
        from md2office.generators import PowerPointGenerator
        if PowerPointGenerator is None:
            print("⚠️  PowerPoint generator not available (python-pptx not installed)")
            results['powerpoint'] = False
        else:
            pptx_gen = PowerPointGenerator()
            print("✅ PowerPoint generator initialized")
            print("   ✅ PowerPoint generator ready")
            results['powerpoint'] = True
    except ImportError:
        print("⚠️  PowerPoint generator not available (python-pptx not installed)")
        results['powerpoint'] = False
    except Exception as e:
        print(f"❌ PowerPoint generator error: {e}")
        results['powerpoint'] = False
    
    # Test PDF Generator
    try:
        from md2office.generators import PDFGenerator
        if PDFGenerator is None:
            print("⚠️  PDF generator not available (reportlab not installed)")
            results['pdf'] = False
        else:
            pdf_gen = PDFGenerator()
            print("✅ PDF generator initialized")
            print("   ✅ PDF generator ready")
            results['pdf'] = True
    except ImportError:
        print("⚠️  PDF generator not available (reportlab not installed)")
        results['pdf'] = False
    except Exception as e:
        print(f"❌ PDF generator error: {e}")
        results['pdf'] = False
    
    print()
    return results


def test_pipeline(ast):
    """Test conversion pipeline."""
    print("=" * 60)
    print("TEST 5: Conversion Pipeline")
    print("=" * 60)
    
    if ast is None:
        print("⚠️  Skipping pipeline test (no AST)")
        return False
    
    try:
        from md2office.router import ConversionPipeline
        from md2office.generators import WordGenerator, PowerPointGenerator, PDFGenerator
        
        pipeline = ConversionPipeline()
        
        # Register generators (if available)
        generators_registered = 0
        
        try:
            word_gen = WordGenerator()
            pipeline.register_generator('word', word_gen)
            generators_registered += 1
            print("✅ Word generator registered")
        except:
            print("⚠️  Word generator not available")
        
        try:
            pptx_gen = PowerPointGenerator()
            pipeline.register_generator('powerpoint', pptx_gen)
            generators_registered += 1
            print("✅ PowerPoint generator registered")
        except:
            print("⚠️  PowerPoint generator not available")
        
        try:
            pdf_gen = PDFGenerator()
            pipeline.register_generator('pdf', pdf_gen)
            generators_registered += 1
            print("✅ PDF generator registered")
        except:
            print("⚠️  PDF generator not available")
        
        if generators_registered == 0:
            print("⚠️  No generators available for testing")
            return False
        
        print(f"✅ Pipeline initialized with {generators_registered} generator(s)")
        print()
        return True
    
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration():
    """Test configuration system."""
    print("=" * 60)
    print("TEST 6: Configuration System")
    print("=" * 60)
    
    try:
        from md2office.config import Config, get_default_config
        
        # Test default config
        default_config = get_default_config()
        print(f"✅ Default config loaded ({len(default_config)} options)")
        
        # Test config object
        config = Config()
        print("✅ Config object created")
        
        # Test config methods
        output_dir = config.get_output_directory()
        style = config.get_style_preset()
        print(f"   Default output directory: {output_dir}")
        print(f"   Default style preset: {style}")
        
        # Test config updates
        config.set('style', 'professional')
        assert config.get('style') == 'professional'
        print("✅ Config updates work correctly")
        
        print()
        return True
    
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_styling():
    """Test styling system."""
    print("=" * 60)
    print("TEST 7: Styling System")
    print("=" * 60)
    
    try:
        from md2office.styling import get_style_preset, StyleManager
        
        # Test style presets
        presets = ['default', 'minimal', 'professional']
        
        for preset_name in presets:
            try:
                preset = get_style_preset(preset_name)
                print(f"✅ Style preset '{preset_name}' loaded")
                print(f"   Heading styles: {len(preset.heading_styles)}")
            except Exception as e:
                print(f"❌ Failed to load preset '{preset_name}': {e}")
                return False
        
        print()
        return True
    
    except Exception as e:
        print(f"❌ Styling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling."""
    print("=" * 60)
    print("TEST 8: Error Handling")
    print("=" * 60)
    
    try:
        from md2office.errors import (
            MD2OfficeError, ParseError, ConversionError,
            FileError, ConfigurationError, setup_logger
        )
        
        # Test error creation
        parse_error = ParseError("Test error", line_number=10)
        print(f"✅ ParseError created: {parse_error.message}")
        
        conversion_error = ConversionError("Test conversion error", format="word")
        print(f"✅ ConversionError created: {conversion_error.message}")
        
        file_error = FileError("Test file error", file_path="test.md", operation="read")
        print(f"✅ FileError created: {file_error.message}")
        
        # Test logger
        logger = setup_logger(verbose=False, quiet=False)
        print("✅ Logger initialized")
        
        print()
        return True
    
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cli_structure():
    """Test CLI structure."""
    print("=" * 60)
    print("TEST 9: CLI Structure")
    print("=" * 60)
    
    try:
        from md2office.cli import cli, main
        
        # Check if Click is available
        try:
            import click
            print("✅ Click framework available")
            
            # Test CLI function exists
            assert callable(cli)
            assert callable(main)
            print("✅ CLI functions available")
            
        except ImportError:
            print("⚠️  Click not available (CLI won't work)")
            return False
        
        print()
        return True
    
    except Exception as e:
        print(f"❌ CLI structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all dry run tests."""
    print("\n" + "=" * 60)
    print("MD2OFFICE DRY RUN TEST SUITE")
    print("=" * 60)
    print()
    
    results = {}
    
    # Test 1: Imports
    results['imports'] = test_imports()
    # Continue even if some imports fail - we'll test what's available
    
    # Test 2: Markdown Parsing
    success, tokens = test_markdown_parsing()
    results['parsing'] = success
    
    # Test 3: AST Building
    success, ast = test_ast_building(tokens)
    results['ast'] = success
    
    # Test 4: Generators
    generator_results = test_generators(ast)
    results['generators'] = any(generator_results.values())
    
    # Test 5: Pipeline
    results['pipeline'] = test_pipeline(ast)
    
    # Test 6: Configuration
    results['config'] = test_configuration()
    
    # Test 7: Styling
    results['styling'] = test_styling()
    
    # Test 8: Error Handling
    results['errors'] = test_error_handling()
    
    # Test 9: CLI Structure
    results['cli'] = test_cli_structure()
    
    # Summary
    print("=" * 60)
    print("DRY RUN SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    # Core tests (should always pass)
    core_tests = ['imports', 'parsing', 'ast', 'config', 'styling', 'errors']
    core_passed = sum(1 for test in core_tests if results.get(test))
    
    # Optional tests (may fail if dependencies missing)
    optional_tests = ['generators', 'pipeline', 'cli']
    optional_passed = sum(1 for test in optional_tests if results.get(test))
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        if test_name in optional_tests:
            status += " (optional - requires dependencies)"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Core Tests: {core_passed}/{len(core_tests)} passed")
    print(f"Optional Tests: {optional_passed}/{len(optional_tests)} passed")
    print(f"Overall: {passed_tests}/{total_tests} passed ({passed_tests/total_tests*100:.1f}%)")
    print()
    
    # Check dependencies
    print("=" * 60)
    print("DEPENDENCY CHECK")
    print("=" * 60)
    
    dependencies = {
        'python-docx': 'Word generation',
        'python-pptx': 'PowerPoint generation',
        'reportlab': 'PDF generation',
        'click': 'CLI interface',
        'PyYAML': 'YAML config support'
    }
    
    missing_deps = []
    for dep, purpose in dependencies.items():
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep} installed ({purpose})")
        except ImportError:
            print(f"⚠️  {dep} not installed ({purpose})")
            missing_deps.append(dep)
    
    print()
    
    if core_passed == len(core_tests):
        print("✅ Core implementation is working correctly!")
        if missing_deps:
            print(f"\n⚠️  Note: {len(missing_deps)} optional dependency(ies) missing.")
            print("   Install with: pip install " + " ".join(missing_deps))
        else:
            print("\n🎉 All dependencies installed! Full functionality available.")
        return True
    else:
        print("❌ Core tests failed. Review errors above.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

