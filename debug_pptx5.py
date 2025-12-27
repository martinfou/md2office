#!/usr/bin/env python3
"""Debug - check actual nested structure."""
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

def find_all_sections(node, path=""):
    """Find all sections recursively."""
    sections = []
    if node.node_type == NodeType.SECTION:
        level = node.level or 0
        heading_text = "No heading"
        for child in node.children:
            if child.node_type == NodeType.HEADING:
                heading_text = child.content[:40]
                break
        sections.append((path, level, heading_text, len(node.children)))
        
        # Check if heading has section children
        for child in node.children:
            if child.node_type == NodeType.HEADING:
                for subchild in child.children:
                    if subchild.node_type == NodeType.SECTION:
                        sections.extend(find_all_sections(subchild, f"{path}->heading->section"))
            elif child.node_type == NodeType.SECTION:
                sections.extend(find_all_sections(child, f"{path}->section"))
    
    for child in node.children:
        if child.node_type != NodeType.SECTION:
            sections.extend(find_all_sections(child, path))
    
    return sections

all_sections = find_all_sections(ast)
print("All sections found:")
print("=" * 60)
for path, level, heading, child_count in all_sections:
    print(f"Level {level}: {heading} (path: {path}, children: {child_count})")

