#!/usr/bin/env python3
"""
Test script for MarkdownViewer widget.

This script tests the markdown viewer functionality without requiring
the full GUI application to be running.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from md2office.gui.widgets.markdown_viewer import MarkdownViewer


def test_markdown_conversion():
    """Test markdown to HTML conversion."""
    viewer = MarkdownViewer()
    
    # Test basic markdown
    test_markdown = """# Test Document

This is a **test** document with *formatting*.

## Code Block

```python
def hello():
    print("Hello, World!")
```

## Mermaid Diagram

```mermaid
graph TD
    A[Start] --> B[End]
```
"""
    
    try:
        html = viewer._markdown_to_html(test_markdown)
        print("✓ Markdown conversion successful")
        print(f"  HTML length: {len(html)} characters")
        
        # Check for Mermaid div
        if 'class="mermaid"' in html:
            print("✓ Mermaid diagram detected and converted")
        else:
            print("⚠ Mermaid diagram not found in HTML")
        
        # Check for code block
        if '<pre><code' in html:
            print("✓ Code blocks detected")
        
        return True
    except Exception as e:
        print(f"✗ Markdown conversion failed: {e}")
        return False


def test_mermaid_detection():
    """Test Mermaid diagram detection."""
    viewer = MarkdownViewer()
    
    test_cases = [
        ("```mermaid\ngraph TD\nA --> B\n```", True, "Explicit mermaid tag"),
        ("```\ngraph TD\nA --> B\n```", True, "Heuristic detection"),
        ("```python\nprint('hello')\n```", False, "Python code block"),
    ]
    
    all_passed = True
    for markdown, should_be_mermaid, description in test_cases:
        html = viewer._basic_markdown_to_html(markdown)
        processed = viewer._process_mermaid_blocks(html)
        is_mermaid = 'class="mermaid"' in processed
        
        if is_mermaid == should_be_mermaid:
            print(f"✓ {description}: {'Detected' if is_mermaid else 'Not detected'} (correct)")
        else:
            print(f"✗ {description}: Expected {should_be_mermaid}, got {is_mermaid}")
            all_passed = False
    
    return all_passed


def test_image_path_resolution():
    """Test image path resolution."""
    viewer = MarkdownViewer()
    
    # Create a temporary base path
    base_path = Path("/tmp/test")
    
    html_with_image = '<img src="test.png" alt="Test">'
    processed = viewer._process_image_paths(html_with_image, base_path)
    
    # Should convert to file:// URL
    if 'file://' in processed or 'data:image' in processed:
        print("✓ Image path processing works")
        return True
    else:
        print("⚠ Image path processing may not be working correctly")
        return False


if __name__ == "__main__":
    print("Testing MarkdownViewer widget...")
    print("-" * 50)
    
    results = []
    
    print("\n1. Testing markdown conversion:")
    results.append(test_markdown_conversion())
    
    print("\n2. Testing Mermaid detection:")
    results.append(test_mermaid_detection())
    
    print("\n3. Testing image path resolution:")
    results.append(test_image_path_resolution())
    
    print("\n" + "-" * 50)
    if all(results):
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)

