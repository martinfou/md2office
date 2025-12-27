#!/usr/bin/env python3
"""Debug PowerPoint generation step by step."""
import sys
from pathlib import Path
from io import BytesIO

sys.path.insert(0, str(Path(__file__).parent / "src"))

from md2office.parser import MarkdownParser, ASTBuilder
from md2office.generators.powerpoint_generator import PowerPointGenerator
from md2office.parser.ast_builder import NodeType

md_file = Path("examples/input/formation-copilot-365.md")
content = md_file.read_text(encoding='utf-8')

parser = MarkdownParser()
tokens = parser.parse(content)
builder = ASTBuilder()
ast = builder.build(tokens)

# Create generator and add debug tracking
generator = PowerPointGenerator()

# Monkey patch to track slide creation
original_create_title = generator._create_title_slide
original_create_section = generator._create_section_slide
original_create_content = generator._create_content_slide

slide_creations = []

def tracked_create_title(heading, options):
    slide_creations.append(('title', heading.content if heading else 'None'))
    return original_create_title(heading, options)

def tracked_create_section(heading, options):
    slide_creations.append(('section', heading.content if heading else 'None'))
    return original_create_section(heading, options)

def tracked_create_content(heading, options):
    slide_creations.append(('content', heading.content if heading else 'None'))
    return original_create_content(heading, options)

generator._create_title_slide = tracked_create_title
generator._create_section_slide = tracked_create_section
generator._create_content_slide = tracked_create_content

# Generate
pptx_bytes = generator.generate(ast, {})

print("Slide creation tracking:")
print("=" * 60)
for i, (slide_type, content) in enumerate(slide_creations, 1):
    print(f"{i}. {slide_type}: {content[:60]}")

print(f"\nTotal slides created: {len(slide_creations)}")

# Verify with pptx
try:
    from pptx import Presentation
    pres = Presentation(BytesIO(pptx_bytes))
    print(f"Actual slides in presentation: {len(pres.slides)}")
except ImportError:
    print("(Cannot verify - python-pptx not available)")

