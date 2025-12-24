"""
Inline Markdown Formatter

Helper module for parsing and formatting inline markdown elements
(bold, italic, links, code) within paragraphs.
"""

import re
from typing import List, Tuple, Optional, Dict

try:
    from docx.shared import RGBColor
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    # Dummy classes for when docx is not available
    class RGBColor:
        def __init__(self, r, g, b):
            self.r = r
            self.g = g
            self.b = b
    
    class OxmlElement:
        def __init__(self, name):
            self.name = name
        def set(self, *args, **kwargs):
            pass
        def append(self, *args, **kwargs):
            pass
    
    class qn:
        @staticmethod
        def __call__(name):
            return name


class InlineFormatter:
    """Formats inline markdown elements in Word paragraphs."""
    
    def __init__(self):
        """Initialize inline formatter."""
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx is required for InlineFormatter")
        # Patterns for inline markdown
        self.bold_pattern = re.compile(r'\*\*([^*]+)\*\*|__([^_]+)__')
        self.italic_pattern = re.compile(r'\*([^*]+)\*|_([^_]+)_')
        self.code_pattern = re.compile(r'`([^`]+)`')
        self.link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        self.image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    
    def format_text(self, paragraph, text: str, base_font_size=None, base_font_name=None):
        """
        Format text with inline markdown elements.
        
        Args:
            paragraph: Word paragraph object
            text: Text with inline markdown
            base_font_size: Base font size in points
            base_font_name: Base font name
        """
        # Parse text into segments with formatting
        segments = self._parse_inline_markdown(text)
        
        for segment in segments:
            run = paragraph.add_run(segment['text'])
            
            # Apply base font
            if base_font_size:
                run.font.size = base_font_size
            if base_font_name:
                run.font.name = base_font_name
            
            # Apply formatting
            if segment.get('bold'):
                run.font.bold = True
            if segment.get('italic'):
                run.font.italic = True
            if segment.get('code'):
                run.font.name = 'Courier New'
                if base_font_size:
                    run.font.size = base_font_size * 0.9  # Slightly smaller for code
                run.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)  # Red for code
            
            # Handle links
            if segment.get('link_url'):
                self._add_hyperlink(paragraph, run, segment['link_url'], segment['text'])
    
    def _parse_inline_markdown(self, text: str) -> List[Dict]:
        """
        Parse inline markdown into segments with formatting info.
        
        Returns:
            List of segments with text and formatting properties
        """
        segments = []
        current_pos = 0
        
        # Find all formatting markers
        markers = []
        
        # Find bold markers
        for match in self.bold_pattern.finditer(text):
            markers.append({
                'start': match.start(),
                'end': match.end(),
                'type': 'bold',
                'content': match.group(1) or match.group(2)
            })
        
        # Find italic markers (not overlapping with bold)
        for match in self.italic_pattern.finditer(text):
            # Check if this is part of a bold marker
            is_bold_part = False
            for bold_marker in markers:
                if bold_marker['start'] <= match.start() < bold_marker['end']:
                    is_bold_part = True
                    break
            if not is_bold_part:
                markers.append({
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'italic',
                    'content': match.group(1) or match.group(2)
                })
        
        # Find code markers
        for match in self.code_pattern.finditer(text):
            markers.append({
                'start': match.start(),
                'end': match.end(),
                'type': 'code',
                'content': match.group(1)
            })
        
        # Find link markers
        for match in self.link_pattern.finditer(text):
            markers.append({
                'start': match.start(),
                'end': match.end(),
                'type': 'link',
                'content': match.group(1),
                'url': match.group(2)
            })
        
        # Sort markers by position
        markers.sort(key=lambda x: x['start'])
        
        # Build segments
        pos = 0
        for marker in markers:
            # Add text before marker
            if marker['start'] > pos:
                segments.append({
                    'text': text[pos:marker['start']],
                    'bold': False,
                    'italic': False,
                    'code': False
                })
            
            # Add formatted segment
            segment = {
                'text': marker['content'],
                'bold': marker['type'] == 'bold',
                'italic': marker['type'] == 'italic',
                'code': marker['type'] == 'code'
            }
            
            if marker['type'] == 'link':
                segment['link_url'] = marker['url']
            
            segments.append(segment)
            pos = marker['end']
        
        # Add remaining text
        if pos < len(text):
            segments.append({
                'text': text[pos:],
                'bold': False,
                'italic': False,
                'code': False
            })
        
        # If no markers found, return plain text
        if not segments:
            segments.append({
                'text': text,
                'bold': False,
                'italic': False,
                'code': False
            })
        
        return segments
    
    def _add_hyperlink(self, paragraph, run, url: str, text: str):
        """
        Add hyperlink to paragraph.
        
        Args:
            paragraph: Word paragraph
            run: Text run
            url: Hyperlink URL
            text: Link text
        """
        # Create hyperlink element
        hyperlink = OxmlElement('w:hyperlink')
        hyperlink.set(qn('r:id'), 'rId1')  # Relationship ID (simplified)
        
        # Create run for hyperlink
        run_element = OxmlElement('w:r')
        run_properties = OxmlElement('w:rPr')
        
        # Set hyperlink formatting (blue, underlined)
        color = OxmlElement('w:color')
        color.set(qn('w:val'), '0000FF')
        run_properties.append(color)
        
        underline = OxmlElement('w:u')
        underline.set(qn('w:val'), 'single')
        run_properties.append(underline)
        
        run_element.append(run_properties)
        
        # Add text
        text_element = OxmlElement('w:t')
        text_element.text = text
        run_element.append(text_element)
        
        hyperlink.append(run_element)
        
        # Insert hyperlink (simplified - full implementation needs relationship management)
        # For now, just format the run as a link
        run.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
        run.font.underline = True

