#!/usr/bin/env python3
"""Debug script to inspect AST structure."""
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

def print_ast(node, indent=0):
    prefix = "  " * indent
    node_type = node.node_type.value
    level = f" level={node.level}" if node.level else ""
    content_preview = node.content[:50] if node.content else ""
    print(f"{prefix}{node_type}{level}: {content_preview}")
    
    for child in node.children:
        print_ast(child, indent + 1)

print("AST Structure:")
print("=" * 60)
print_ast(ast)
print("=" * 60)

# Count sections by level
def count_by_level(node, counts=None):
    if counts is None:
        counts = {}
    if node.node_type == NodeType.SECTION:
        level = node.level or 0
        counts[level] = counts.get(level, 0) + 1
    for child in node.children:
        count_by_level(child, counts)
    return counts

counts = count_by_level(ast)
print("\nSection counts by level:")
for level in sorted(counts.keys()):
    print(f"  Level {level}: {counts[level]} sections")

