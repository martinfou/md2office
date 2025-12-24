"""
AST Builder and Structure Analyzer

Implements Story 1.2: AST Builder and Structure Analyzer
Builds Abstract Syntax Tree from parsed markdown tokens.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from .markdown_parser import Token, TokenType


class NodeType(Enum):
    """Types of AST nodes."""
    DOCUMENT = "document"
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    LIST_ITEM = "list_item"
    CODE_BLOCK = "code_block"
    INLINE_CODE = "inline_code"
    TABLE = "table"
    TABLE_ROW = "table_row"
    TABLE_CELL = "table_cell"
    BLOCKQUOTE = "blockquote"
    HORIZONTAL_RULE = "horizontal_rule"
    LINK = "link"
    IMAGE = "image"
    EMPHASIS = "emphasis"
    STRONG = "strong"
    TEXT = "text"
    SECTION = "section"


@dataclass
class ASTNode:
    """
    Represents a node in the Abstract Syntax Tree.
    
    Attributes:
        node_type: Type of the node
        content: Text content of the node
        children: Child nodes
        parent: Parent node (None for root)
        level: Hierarchy level (for headings, list depth)
        metadata: Additional metadata
        attributes: Node attributes (for links, images, etc.)
    """
    node_type: NodeType
    content: str = ""
    children: List['ASTNode'] = field(default_factory=list)
    parent: Optional['ASTNode'] = None
    level: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def add_child(self, child: 'ASTNode'):
        """Add a child node and set its parent."""
        child.parent = self
        self.children.append(child)
    
    def get_siblings(self) -> List['ASTNode']:
        """Get sibling nodes."""
        if self.parent is None:
            return []
        return [node for node in self.parent.children if node != self]
    
    def get_ancestors(self) -> List['ASTNode']:
        """Get all ancestor nodes."""
        ancestors = []
        current = self.parent
        while current is not None:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def find_children(self, node_type: NodeType) -> List['ASTNode']:
        """Find all children of a specific type."""
        return [child for child in self.children if child.node_type == node_type]
    
    def __repr__(self):
        return f"ASTNode(type={self.node_type.value}, level={self.level}, children={len(self.children)})"


class ASTBuilder:
    """
    Builds an Abstract Syntax Tree from parsed markdown tokens.
    
    Creates a hierarchical structure that preserves document organization
    and enables structure analysis for conversion routing.
    """
    
    def __init__(self):
        """Initialize the AST builder."""
        self.root: Optional[ASTNode] = None
        self.current_section: Optional[ASTNode] = None
        self.heading_stack: List[ASTNode] = []
    
    def build(self, tokens: List[Token]) -> ASTNode:
        """
        Build AST from tokens.
        
        Args:
            tokens: List of parsed markdown tokens
            
        Returns:
            Root AST node representing the document
        """
        self.root = ASTNode(
            node_type=NodeType.DOCUMENT,
            content="",
            metadata={}
        )
        self.current_section = self.root
        self.heading_stack = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.type == TokenType.FRONT_MATTER:
                # Store front-matter in document metadata
                self.root.metadata.update(token.metadata or {})
            
            elif token.type == TokenType.HEADING:
                node = self._build_heading_node(token)
                self._insert_heading_node(node)
            
            elif token.type == TokenType.CODE_BLOCK:
                node = self._build_code_block_node(token)
                self.current_section.add_child(node)
            
            elif token.type == TokenType.TABLE:
                node = self._build_table_node(token)
                self.current_section.add_child(node)
            
            elif token.type == TokenType.BLOCKQUOTE:
                node = self._build_blockquote_node(token)
                self.current_section.add_child(node)
            
            elif token.type == TokenType.HORIZONTAL_RULE:
                node = self._build_horizontal_rule_node(token)
                self.current_section.add_child(node)
            
            elif token.type == TokenType.LIST_ITEM:
                # Collect consecutive list items
                list_items = [token]
                j = i + 1
                while j < len(tokens) and tokens[j].type == TokenType.LIST_ITEM:
                    list_items.append(tokens[j])
                    j += 1
                
                list_node = self._build_list_node(list_items)
                self.current_section.add_child(list_node)
                i = j - 1  # Skip processed items
            
            elif token.type == TokenType.PARAGRAPH:
                node = self._build_paragraph_node(token)
                self.current_section.add_child(node)
            
            i += 1
        
        return self.root
    
    def _build_heading_node(self, token: Token) -> ASTNode:
        """Build a heading node."""
        return ASTNode(
            node_type=NodeType.HEADING,
            content=token.content,
            level=token.level,
            metadata={'line_number': token.line_number}
        )
    
    def _build_paragraph_node(self, token: Token) -> ASTNode:
        """Build a paragraph node with inline elements."""
        node = ASTNode(
            node_type=NodeType.PARAGRAPH,
            content=token.content,
            metadata=token.metadata or {}
        )
        
        # Process inline elements
        if token.metadata:
            # Extract links
            for link_info in token.metadata.get('links', []):
                link_node = ASTNode(
                    node_type=NodeType.LINK,
                    content=link_info['text'],
                    attributes={'url': link_info['url']}
                )
                node.add_child(link_node)
            
            # Extract images
            for image_info in token.metadata.get('images', []):
                image_node = ASTNode(
                    node_type=NodeType.IMAGE,
                    content=image_info['alt'],
                    attributes={'src': image_info['src']}
                )
                node.add_child(image_node)
        
        return node
    
    def _build_code_block_node(self, token: Token) -> ASTNode:
        """Build a code block node."""
        return ASTNode(
            node_type=NodeType.CODE_BLOCK,
            content=token.content,
            metadata={
                'language': token.language,
                'line_number': token.line_number
            }
        )
    
    def _build_table_node(self, token: Token) -> ASTNode:
        """Build a table node."""
        table_node = ASTNode(
            node_type=NodeType.TABLE,
            content="",
            metadata=token.metadata or {}
        )
        
        if token.metadata:
            headers = token.metadata.get('headers', [])
            rows = token.metadata.get('rows', [])
            
            # Create header row
            if headers:
                header_row = ASTNode(
                    node_type=NodeType.TABLE_ROW,
                    content="",
                    metadata={'is_header': True}
                )
                for header_text in headers:
                    cell = ASTNode(
                        node_type=NodeType.TABLE_CELL,
                        content=header_text,
                        metadata={'is_header': True}
                    )
                    header_row.add_child(cell)
                table_node.add_child(header_row)
            
            # Create data rows
            for row_data in rows:
                row_node = ASTNode(
                    node_type=NodeType.TABLE_ROW,
                    content="",
                    metadata={'is_header': False}
                )
                for cell_text in row_data:
                    cell = ASTNode(
                        node_type=NodeType.TABLE_CELL,
                        content=cell_text,
                        metadata={'is_header': False}
                    )
                    row_node.add_child(cell)
                table_node.add_child(row_node)
        
        return table_node
    
    def _build_blockquote_node(self, token: Token) -> ASTNode:
        """Build a blockquote node."""
        return ASTNode(
            node_type=NodeType.BLOCKQUOTE,
            content=token.content,
            metadata={'line_number': token.line_number}
        )
    
    def _build_horizontal_rule_node(self, token: Token) -> ASTNode:
        """Build a horizontal rule node."""
        return ASTNode(
            node_type=NodeType.HORIZONTAL_RULE,
            content="",
            metadata={'line_number': token.line_number}
        )
    
    def _build_list_node(self, list_items: List[Token]) -> ASTNode:
        """Build a list node from list item tokens."""
        list_node = ASTNode(
            node_type=NodeType.LIST,
            content="",
            metadata={}
        )
        
        # Group items by depth
        current_items = []
        current_depth = None
        
        for token in list_items:
            depth = token.level or 0
            
            if current_depth is None:
                current_depth = depth
            
            if depth == current_depth:
                current_items.append(token)
            else:
                # Process current level
                if current_items:
                    self._add_list_items_to_node(list_node, current_items, current_depth)
                current_items = [token]
                current_depth = depth
        
        # Process remaining items
        if current_items:
            self._add_list_items_to_node(list_node, current_items, current_depth)
        
        return list_node
    
    def _add_list_items_to_node(self, list_node: ASTNode, items: List[Token], depth: int):
        """Add list items to a list node."""
        is_ordered = items[0].metadata.get('ordered', False) if items[0].metadata else False
        
        for token in items:
            item_node = ASTNode(
                node_type=NodeType.LIST_ITEM,
                content=token.content,
                level=depth,
                metadata={
                    'ordered': is_ordered,
                    'marker': token.metadata.get('marker', '-'),
                    'line_number': token.line_number
                }
            )
            list_node.add_child(item_node)
    
    def _insert_heading_node(self, heading_node: ASTNode):
        """
        Insert a heading node at the appropriate level in the hierarchy.
        
        Maintains proper heading hierarchy and creates sections.
        """
        level = heading_node.level
        
        # Pop heading stack until we find appropriate parent
        while self.heading_stack:
            top_heading = self.heading_stack[-1]
            if top_heading.level < level:
                # Current heading is a child of top heading
                break
            self.heading_stack.pop()
        
        # Create section node for this heading
        section_node = ASTNode(
            node_type=NodeType.SECTION,
            content="",
            level=level,
            metadata={'heading': heading_node.content}
        )
        section_node.add_child(heading_node)
        
        # Add section to appropriate parent
        if self.heading_stack:
            parent_section = self.heading_stack[-1]
            parent_section.add_child(section_node)
        else:
            self.root.add_child(section_node)
        
        # Update current section and heading stack
        self.current_section = section_node
        self.heading_stack.append(heading_node)


class StructureAnalyzer:
    """
    Analyzes AST structure for conversion routing decisions.
    
    Provides insights about document hierarchy, content types,
    and structural metadata.
    """
    
    def __init__(self, ast: ASTNode):
        """
        Initialize structure analyzer with AST.
        
        Args:
            ast: Root AST node
        """
        self.ast = ast
        self._analysis_cache: Dict[str, Any] = {}
    
    def analyze(self) -> Dict[str, Any]:
        """
        Perform comprehensive structure analysis.
        
        Returns:
            Dictionary containing analysis results
        """
        if self._analysis_cache:
            return self._analysis_cache
        
        analysis = {
            'heading_hierarchy': self._analyze_heading_hierarchy(),
            'content_types': self._analyze_content_types(),
            'sections': self._analyze_sections(),
            'toc_candidates': self._extract_toc_candidates(),
            'metadata': self._extract_metadata(),
            'statistics': self._calculate_statistics()
        }
        
        self._analysis_cache = analysis
        return analysis
    
    def _analyze_heading_hierarchy(self) -> Dict[str, Any]:
        """Analyze heading hierarchy and nesting patterns."""
        headings = []
        
        def collect_headings(node: ASTNode):
            if node.node_type == NodeType.HEADING:
                headings.append({
                    'level': node.level,
                    'content': node.content,
                    'path': self._get_node_path(node)
                })
            for child in node.children:
                collect_headings(child)
        
        collect_headings(self.ast)
        
        # Analyze hierarchy
        max_level = max([h['level'] for h in headings]) if headings else 0
        level_counts = {}
        for heading in headings:
            level = heading['level']
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            'headings': headings,
            'max_level': max_level,
            'level_counts': level_counts,
            'total_headings': len(headings)
        }
    
    def _analyze_content_types(self) -> Dict[str, int]:
        """Analyze content types present in document."""
        content_types = {}
        
        def count_types(node: ASTNode):
            node_type = node.node_type.value
            content_types[node_type] = content_types.get(node_type, 0) + 1
            for child in node.children:
                count_types(child)
        
        count_types(self.ast)
        return content_types
    
    def _analyze_sections(self) -> List[Dict[str, Any]]:
        """Analyze document sections."""
        sections = []
        
        def collect_sections(node: ASTNode):
            if node.node_type == NodeType.SECTION:
                sections.append({
                    'level': node.level,
                    'heading': node.metadata.get('heading', ''),
                    'child_count': len(node.children),
                    'content_types': self._get_section_content_types(node)
                })
            for child in node.children:
                collect_sections(child)
        
        collect_sections(self.ast)
        return sections
    
    def _get_section_content_types(self, section_node: ASTNode) -> Dict[str, int]:
        """Get content types within a section."""
        content_types = {}
        
        def count_in_section(node: ASTNode):
            if node.node_type != NodeType.SECTION and node.node_type != NodeType.HEADING:
                node_type = node.node_type.value
                content_types[node_type] = content_types.get(node_type, 0) + 1
            for child in node.children:
                count_in_section(child)
        
        count_in_section(section_node)
        return content_types
    
    def _extract_toc_candidates(self) -> List[Dict[str, Any]]:
        """Extract table of contents candidates from headings."""
        toc_candidates = []
        
        def collect_toc(node: ASTNode, depth: int = 0):
            if node.node_type == NodeType.HEADING:
                toc_candidates.append({
                    'level': node.level,
                    'content': node.content,
                    'depth': depth
                })
            for child in node.children:
                if child.node_type == NodeType.HEADING:
                    collect_toc(child, depth + 1)
                elif child.node_type == NodeType.SECTION:
                    collect_toc(child, depth)
        
        collect_toc(self.ast)
        return toc_candidates
    
    def _extract_metadata(self) -> Dict[str, Any]:
        """Extract document metadata."""
        metadata = self.ast.metadata.copy()
        
        # Extract title from first H1 heading
        first_h1 = self._find_first_heading(1)
        if first_h1:
            metadata['title'] = first_h1.content
        
        return metadata
    
    def _find_first_heading(self, level: int) -> Optional[ASTNode]:
        """Find first heading of specified level."""
        def search(node: ASTNode):
            if node.node_type == NodeType.HEADING and node.level == level:
                return node
            for child in node.children:
                result = search(child)
                if result:
                    return result
            return None
        
        return search(self.ast)
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """Calculate document statistics."""
        stats = {
            'total_nodes': 0,
            'total_sections': 0,
            'total_paragraphs': 0,
            'total_lists': 0,
            'total_tables': 0,
            'total_code_blocks': 0,
            'total_images': 0,
            'total_links': 0
        }
        
        def count(node: ASTNode):
            stats['total_nodes'] += 1
            
            if node.node_type == NodeType.SECTION:
                stats['total_sections'] += 1
            elif node.node_type == NodeType.PARAGRAPH:
                stats['total_paragraphs'] += 1
            elif node.node_type == NodeType.LIST:
                stats['total_lists'] += 1
            elif node.node_type == NodeType.TABLE:
                stats['total_tables'] += 1
            elif node.node_type == NodeType.CODE_BLOCK:
                stats['total_code_blocks'] += 1
            elif node.node_type == NodeType.IMAGE:
                stats['total_images'] += 1
            elif node.node_type == NodeType.LINK:
                stats['total_links'] += 1
            
            for child in node.children:
                count(child)
        
        count(self.ast)
        return stats
    
    def _get_node_path(self, node: ASTNode) -> str:
        """Get path to node from root."""
        path = []
        current = node
        
        while current and current != self.ast:
            if current.node_type == NodeType.HEADING:
                path.insert(0, f"H{current.level}: {current.content[:30]}")
            current = current.parent
        
        return " > ".join(path)

