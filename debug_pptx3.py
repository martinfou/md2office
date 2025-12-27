#!/usr/bin/env python3
"""Debug - check what children are being processed."""
import sys
from pathlib import Path

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

# Find the H1 section
h1_section = None
for child in ast.children:
    if child.node_type == NodeType.SECTION and child.level == 1:
        h1_section = child
        break

if h1_section:
    print("H1 Section children:")
    print("=" * 60)
    for i, child in enumerate(h1_section.children, 1):
        node_type = child.node_type.value
        level = f" level={child.level}" if child.level else ""
        content_preview = ""
        if child.node_type == NodeType.HEADING:
            content_preview = f": {child.content[:50]}"
        elif child.node_type == NodeType.SECTION:
            # Find heading in section
            for subchild in child.children:
                if subchild.node_type == NodeType.HEADING:
                    content_preview = f": {subchild.content[:50]}"
                    break
        print(f"{i}. {node_type}{level}{content_preview}")
    
    # Count section children
    section_children = [c for c in h1_section.children if c.node_type == NodeType.SECTION]
    print(f"\nTotal SECTION children: {len(section_children)}")
    print(f"Total children: {len(h1_section.children)}")

