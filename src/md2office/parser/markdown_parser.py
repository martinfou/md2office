"""
Markdown Parser Implementation

Implements Story 1.1: Markdown Parser Implementation
Handles Microsoft Copilot-generated markdown with GFM extensions.
"""

import re
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    """Types of markdown tokens."""
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    CODE_BLOCK = "code_block"
    INLINE_CODE = "inline_code"
    TABLE = "table"
    BLOCKQUOTE = "blockquote"
    HORIZONTAL_RULE = "horizontal_rule"
    LINK = "link"
    IMAGE = "image"
    EMPHASIS = "emphasis"
    STRONG = "strong"
    TEXT = "text"
    FRONT_MATTER = "front_matter"
    LINE_BREAK = "line_break"


@dataclass
class Token:
    """Represents a parsed markdown token."""
    type: TokenType
    content: str
    level: Optional[int] = None  # For headings, list depth
    language: Optional[str] = None  # For code blocks
    metadata: Optional[Dict[str, Any]] = None
    line_number: Optional[int] = None


class MarkdownParser:
    """
    Parser for Microsoft Copilot-generated markdown.
    
    Supports:
    - Standard markdown syntax (CommonMark)
    - GitHub Flavored Markdown (GFM) extensions
    - Copilot-specific formatting patterns
    - Front-matter metadata
    """
    
    def __init__(self):
        """Initialize the markdown parser."""
        self.front_matter_pattern = re.compile(
            r'^---\s*\n(.*?)\n---\s*\n',
            re.MULTILINE | re.DOTALL
        )
        self.heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        self.code_block_pattern = re.compile(
            r'^```(\w+)?\n(.*?)```',
            re.MULTILINE | re.DOTALL
        )
        self.inline_code_pattern = re.compile(r'`([^`]+)`')
        self.list_item_pattern = re.compile(r'^(\s*)([-*+]|\d+\.)\s+(.+)$', re.MULTILINE)
        self.table_pattern = re.compile(
            r'^\|(.+)\|\s*\n\|([-:\s|]+)\|\s*\n((?:\|.+\|\s*\n?)+)',
            re.MULTILINE
        )
        self.link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        self.image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
        self.emphasis_pattern = re.compile(r'(\*{1,3}|_{1,3})([^*_]+)\1')
        self.blockquote_pattern = re.compile(r'^>\s+(.+)$', re.MULTILINE)
        self.horizontal_rule_pattern = re.compile(r'^[-*_]{3,}\s*$', re.MULTILINE)
    
    def parse(self, markdown_content: str) -> List[Token]:
        """
        Parse markdown content into tokens.
        
        Args:
            markdown_content: Raw markdown text
            
        Returns:
            List of parsed tokens
            
        Raises:
            ValueError: If markdown is malformed
        """
        tokens = []
        lines = markdown_content.split('\n')
        line_number = 0
        
        # Extract front-matter if present
        front_matter_match = self.front_matter_pattern.match(markdown_content)
        if front_matter_match:
            front_matter_content = front_matter_match.group(1)
            tokens.append(Token(
                type=TokenType.FRONT_MATTER,
                content=front_matter_content,
                metadata=self._parse_front_matter(front_matter_content),
                line_number=1
            ))
            # Remove front-matter from content for further processing
            markdown_content = self.front_matter_pattern.sub('', markdown_content)
        
        # Split content into blocks
        blocks = self._split_into_blocks(markdown_content)
        
        for block in blocks:
            block_lines = block.split('\n')
            block_start_line = line_number + 1
            
            # Try to match different block types
            if self._is_heading(block):
                token = self._parse_heading(block, block_start_line)
                if token:
                    tokens.append(token)
            elif self._is_code_block(block):
                token = self._parse_code_block(block, block_start_line)
                if token:
                    tokens.append(token)
            elif self._is_table(block):
                token = self._parse_table(block, block_start_line)
                if token:
                    tokens.append(token)
            elif self._is_blockquote(block):
                token = self._parse_blockquote(block, block_start_line)
                if token:
                    tokens.append(token)
            elif self._is_horizontal_rule(block):
                tokens.append(Token(
                    type=TokenType.HORIZONTAL_RULE,
                    content=block.strip(),
                    line_number=block_start_line
                ))
            elif self._is_list(block):
                list_tokens = self._parse_list(block, block_start_line)
                tokens.extend(list_tokens)
            else:
                # Regular paragraph
                token = self._parse_paragraph(block, block_start_line)
                if token:
                    tokens.append(token)
            
            line_number += len(block_lines)
        
        return tokens
    
    def _split_into_blocks(self, content: str) -> List[str]:
        """Split content into logical blocks (paragraphs, code blocks, etc.)."""
        # First, extract code blocks to preserve them
        code_blocks = []
        code_block_placeholders = []
        
        def replace_code_block(match):
            placeholder = f"__CODE_BLOCK_{len(code_blocks)}__"
            code_blocks.append(match.group(0))
            code_block_placeholders.append(placeholder)
            return placeholder
        
        content_with_placeholders = self.code_block_pattern.sub(
            replace_code_block,
            content
        )
        
        # Split by double newlines (paragraph boundaries)
        blocks = re.split(r'\n\s*\n', content_with_placeholders)
        
        # Restore code blocks
        for i, block in enumerate(blocks):
            for j, placeholder in enumerate(code_block_placeholders):
                if placeholder in block:
                    blocks[i] = block.replace(placeholder, code_blocks[j])
        
        return [b.strip() for b in blocks if b.strip()]
    
    def _is_heading(self, block: str) -> bool:
        """Check if block is a heading."""
        return bool(self.heading_pattern.match(block.strip()))
    
    def _is_code_block(self, block: str) -> bool:
        """Check if block is a code block."""
        return bool(self.code_block_pattern.match(block))
    
    def _is_table(self, block: str) -> bool:
        """Check if block is a table."""
        return bool(self.table_pattern.match(block))
    
    def _is_blockquote(self, block: str) -> bool:
        """Check if block is a blockquote."""
        return bool(self.blockquote_pattern.match(block))
    
    def _is_horizontal_rule(self, block: str) -> bool:
        """Check if block is a horizontal rule."""
        return bool(self.horizontal_rule_pattern.match(block.strip()))
    
    def _is_list(self, block: str) -> bool:
        """Check if block contains list items."""
        return bool(self.list_item_pattern.search(block))
    
    def _parse_heading(self, block: str, line_number: int) -> Optional[Token]:
        """Parse a heading block."""
        match = self.heading_pattern.match(block.strip())
        if match:
            level = len(match.group(1))
            content = match.group(2).strip()
            return Token(
                type=TokenType.HEADING,
                content=content,
                level=level,
                line_number=line_number
            )
        return None
    
    def _parse_code_block(self, block: str, line_number: int) -> Optional[Token]:
        """Parse a code block."""
        match = self.code_block_pattern.search(block)
        if match:
            language = match.group(1) if match.group(1) else None
            code_content = match.group(2)
            return Token(
                type=TokenType.CODE_BLOCK,
                content=code_content,
                language=language,
                line_number=line_number
            )
        return None
    
    def _parse_table(self, block: str, line_number: int) -> Optional[Token]:
        """Parse a table block."""
        match = self.table_pattern.search(block)
        if match:
            header_row = match.group(1)
            separator_row = match.group(2)
            data_rows = match.group(3)
            
            # Parse table structure
            headers = [cell.strip() for cell in header_row.split('|')[1:-1]]
            rows = []
            for row in data_rows.strip().split('\n'):
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                if cells:
                    rows.append(cells)
            
            return Token(
                type=TokenType.TABLE,
                content=block,
                metadata={
                    'headers': headers,
                    'rows': rows,
                    'column_count': len(headers)
                },
                line_number=line_number
            )
        return None
    
    def _parse_blockquote(self, block: str, line_number: int) -> Optional[Token]:
        """Parse a blockquote block."""
        lines = block.split('\n')
        content_lines = []
        for line in lines:
            match = self.blockquote_pattern.match(line)
            if match:
                content_lines.append(match.group(1))
        
        if content_lines:
            return Token(
                type=TokenType.BLOCKQUOTE,
                content='\n'.join(content_lines),
                line_number=line_number
            )
        return None
    
    def _parse_list(self, block: str, line_number: int) -> List[Token]:
        """Parse a list block."""
        tokens = []
        lines = block.split('\n')
        current_line = line_number
        
        for line in lines:
            match = self.list_item_pattern.match(line)
            if match:
                indent = len(match.group(1))
                marker = match.group(2)
                content = match.group(3)
                
                # Determine if ordered or unordered
                is_ordered = marker.rstrip('.').isdigit()
                depth = indent // 2  # Assuming 2-space indentation
                
                tokens.append(Token(
                    type=TokenType.LIST_ITEM,
                    content=content,
                    level=depth,
                    metadata={
                        'ordered': is_ordered,
                        'marker': marker
                    },
                    line_number=current_line
                ))
            current_line += 1
        
        return tokens
    
    def _parse_paragraph(self, block: str, line_number: int) -> Optional[Token]:
        """Parse a paragraph block."""
        if not block.strip():
            return None
        
        # Process inline elements (links, images, emphasis, code)
        content = block
        
        return Token(
            type=TokenType.PARAGRAPH,
            content=content,
            metadata=self._extract_inline_elements(content),
            line_number=line_number
        )
    
    def _extract_inline_elements(self, text: str) -> Dict[str, Any]:
        """Extract inline elements from text."""
        metadata = {
            'links': [],
            'images': [],
            'emphasis': [],
            'code': []
        }
        
        # Extract links
        for match in self.link_pattern.finditer(text):
            metadata['links'].append({
                'text': match.group(1),
                'url': match.group(2)
            })
        
        # Extract images
        for match in self.image_pattern.finditer(text):
            metadata['images'].append({
                'alt': match.group(1),
                'src': match.group(2)
            })
        
        # Extract inline code
        for match in self.inline_code_pattern.finditer(text):
            metadata['code'].append(match.group(1))
        
        # Extract emphasis
        for match in self.emphasis_pattern.finditer(text):
            emphasis_type = 'bold_italic' if len(match.group(1)) == 3 else \
                           'bold' if len(match.group(1)) == 2 else 'italic'
            metadata['emphasis'].append({
                'type': emphasis_type,
                'text': match.group(2)
            })
        
        return metadata
    
    def _parse_front_matter(self, content: str) -> Dict[str, Any]:
        """Parse YAML front-matter."""
        metadata = {}
        # Simple YAML parsing (can be enhanced with PyYAML later)
        for line in content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                metadata[key] = value
        return metadata
    
    def validate(self, tokens: List[Token]) -> List[str]:
        """
        Validate parsed tokens and return list of errors.
        
        Args:
            tokens: List of parsed tokens
            
        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        
        # Check for common issues
        heading_levels = []
        for token in tokens:
            if token.type == TokenType.HEADING:
                level = token.level
                if heading_levels and level > heading_levels[-1] + 1:
                    errors.append(
                        f"Line {token.line_number}: Heading level jumps from "
                        f"H{heading_levels[-1]} to H{level}"
                    )
                heading_levels.append(level)
        
        return errors

