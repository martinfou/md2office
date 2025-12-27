#!/usr/bin/env python3
"""Debug - check document structure."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from md2office.parser import MarkdownParser, ASTBuilder
from md2office.parser.ast_builder import NodeType

md_file = Path("examples/input/formation-copilot-365.md")
content = md_file.read_text(encoding='utf-8')

parser = MarkdownParser()
tokens = parser.parse(content)
builder = ASTBuilder()
ast = builder.build(tokens)

print("Document direct children:")
print("=" * 60)
for i, child in enumerate(ast.children, 1):
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
        # Count all descendants
        def count_descendants(n):
            count = 0
            for c in n.children:
                if c.node_type == NodeType.SECTION:
                    count += 1 + count_descendants(c)
            return count
        desc_count = count_descendants(child)
        content_preview += f" ({desc_count} nested sections)"
    print(f"{i}. {node_type}{level}{content_preview}")

print(f"\nTotal document children: {len(ast.children)}")

# Check if H2 sections are siblings of H1
h1_section = None
for child in ast.children:
    if child.node_type == NodeType.SECTION and child.level == 1:
        h1_section = child
        break

if h1_section:
    print(f"\nH1 section index: {ast.children.index(h1_section)}")
    print("Siblings of H1 section:")
    for i, sibling in enumerate(ast.children):
        if sibling != h1_section and sibling.node_type == NodeType.SECTION:
            level = sibling.level or 0
            for subchild in sibling.children:
                if subchild.node_type == NodeType.HEADING:
                    print(f"  {i}. Section level={level}: {subchild.content[:50]}")
                    break

