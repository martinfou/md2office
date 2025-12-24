"""
PDF Document Generator

Implements Epic 4: PDF Conversion
Generates PDF documents from AST using ReportLab.
"""

from typing import Dict, Any, Optional, List
from io import BytesIO
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, black, gray
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        Table, TableStyle, Preformatted, Image as RLImage
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from ..parser.ast_builder import ASTNode, NodeType
from ..router.content_router import FormatGenerator, OutputFormat
from ..errors import ConversionError, FileError
from ..styling.style import StylePreset, get_style_preset


class PDFGenerator(FormatGenerator):
    """
    Generates PDF documents from AST.
    
    Implements Story 4.1: PDF Document Generator Core
    """
    
    def __init__(self):
        """Initialize PDF generator."""
        if not REPORTLAB_AVAILABLE:
            raise ImportError(
                "ReportLab is required for PDF generation. "
                "Install with: pip install reportlab"
            )
        self.buffer: Optional[BytesIO] = None
        self.doc: Optional[SimpleDocTemplate] = None
        self.story: List = []
        self.current_style_preset: Optional[StylePreset] = None
        self.bookmarks: List[Dict[str, Any]] = []
        self.page_width = letter[0]
        self.page_height = letter[1]
    
    def generate(self, ast: ASTNode, options: Dict[str, Any]) -> bytes:
        """
        Generate PDF document from AST.
        
        Args:
            ast: Root AST node
            options: Generation options
            
        Returns:
            Generated PDF document as bytes
            
        Raises:
            ConversionError: If generation fails
        """
        try:
            # Initialize buffer and document
            self.buffer = BytesIO()
            
            # Get page size
            page_size = options.get('page_size', 'letter')
            if page_size == 'A4':
                self.page_width, self.page_height = A4
            else:
                self.page_width, self.page_height = letter
            
            # Create document
            self.doc = SimpleDocTemplate(
                self.buffer,
                pagesize=(self.page_width, self.page_height),
                rightMargin=inch,
                leftMargin=inch,
                topMargin=inch,
                bottomMargin=inch
            )
            
            self.story = []
            self.bookmarks = []
            
            # Get style preset
            style_name = options.get('style', 'default')
            self.current_style_preset = get_style_preset(style_name)
            
            # Set document metadata
            self._set_document_metadata(ast, options)
            
            # Add table of contents if requested
            if options.get('table_of_contents', False):
                self._add_table_of_contents(ast)
            
            # Process AST nodes
            self._process_node(ast, options)
            
            # Build PDF
            self.doc.build(
                self.story,
                onFirstPage=self._on_first_page,
                onLaterPages=self._on_later_pages
            )
            
            # Add bookmarks if requested
            if options.get('bookmarks', True) and self.bookmarks:
                self._add_bookmarks()
            
            return self.buffer.getvalue()
        
        except Exception as e:
            raise ConversionError(
                f"Failed to generate PDF document: {str(e)}",
                format="pdf",
                stage="generation"
            ) from e
    
    def get_file_extension(self) -> str:
        """Get file extension for PDF format."""
        return ".pdf"
    
    def _set_document_metadata(self, ast: ASTNode, options: Dict[str, Any]):
        """Set PDF document metadata."""
        title = ast.metadata.get('title')
        if not title:
            first_h1 = self._find_first_heading(ast, 1)
            if first_h1:
                title = first_h1.content
        
        if title:
            self.doc.title = title
        
        author = ast.metadata.get('author') or options.get('author')
        if author:
            self.doc.author = author
        
        subject = ast.metadata.get('subject', '')
        if subject:
            self.doc.subject = subject
    
    def _process_node(self, node: ASTNode, options: Dict[str, Any]):
        """Process AST node and add to PDF story."""
        if node.node_type == NodeType.DOCUMENT:
            for child in node.children:
                self._process_node(child, options)
        
        elif node.node_type == NodeType.SECTION:
            # Process section (may add page break)
            if options.get('page_breaks', False) and node.level == 1:
                self.story.append(PageBreak())
            
            for child in node.children:
                self._process_node(child, options)
        
        elif node.node_type == NodeType.HEADING:
            self._add_heading(node, options)
        
        elif node.node_type == NodeType.PARAGRAPH:
            self._add_paragraph(node, options)
        
        elif node.node_type == NodeType.LIST:
            self._add_list(node, options)
        
        elif node.node_type == NodeType.TABLE:
            self._add_table(node, options)
        
        elif node.node_type == NodeType.CODE_BLOCK:
            self._add_code_block(node, options)
        
        elif node.node_type == NodeType.BLOCKQUOTE:
            self._add_blockquote(node, options)
        
        elif node.node_type == NodeType.HORIZONTAL_RULE:
            self._add_horizontal_rule()
        
        elif node.node_type == NodeType.IMAGE:
            self._add_image(node, options)
        
        # Process children recursively
        for child in node.children:
            if child.node_type not in [NodeType.HEADING, NodeType.PARAGRAPH,
                                      NodeType.LIST, NodeType.TABLE,
                                      NodeType.CODE_BLOCK, NodeType.BLOCKQUOTE,
                                      NodeType.HORIZONTAL_RULE, NodeType.IMAGE]:
                self._process_node(child, options)
    
    def _add_heading(self, node: ASTNode, options: Dict[str, Any]):
        """Add heading to PDF."""
        level = node.level or 1
        content = node.content
        
        # Get heading style
        if self.current_style_preset:
            heading_style_def = self.current_style_preset.get_heading_style(level)
            font_size = heading_style_def.font.size
            font_weight = heading_style_def.font.weight
        else:
            # Default sizes
            font_sizes = {1: 24, 2: 20, 3: 16, 4: 14, 5: 12, 6: 11}
            font_size = font_sizes.get(level, 12)
            font_weight = 'bold'
        
        # Create paragraph style
        style_name = f'Heading{level}'
        styles = getSampleStyleSheet()
        
        if style_name not in styles.byName:
            heading_style = ParagraphStyle(
                name=style_name,
                parent=styles['Normal'],
                fontSize=font_size,
                fontName='Helvetica-Bold' if font_weight == 'bold' else 'Helvetica',
                spaceBefore=12 if level == 1 else 8,
                spaceAfter=6,
                textColor=black
            )
            styles.add(heading_style)
        else:
            heading_style = styles[style_name]
        
        # Add bookmark
        if options.get('bookmarks', True):
            self.bookmarks.append({
                'level': level,
                'title': content,
                'page': len(self.story)  # Approximate page number
            })
        
        # Add paragraph
        para = Paragraph(content, heading_style)
        self.story.append(para)
        self.story.append(Spacer(1, 0.2 * inch))
    
    def _add_paragraph(self, node: ASTNode, options: Dict[str, Any]):
        """Add paragraph to PDF."""
        content = node.content
        
        # Get paragraph style
        styles = getSampleStyleSheet()
        para_style = styles['Normal']
        
        if self.current_style_preset:
            para_def = self.current_style_preset.paragraph_style
            para_style = ParagraphStyle(
                name='CustomNormal',
                parent=styles['Normal'],
                fontSize=para_def.font.size,
                leading=para_def.font.size * para_def.line_height,
                spaceAfter=para_def.spacing_after,
                alignment=TA_JUSTIFY if para_def.alignment == 'justify' else TA_LEFT
            )
        
        para = Paragraph(content, para_style)
        self.story.append(para)
        self.story.append(Spacer(1, 0.1 * inch))
    
    def _add_list(self, node: ASTNode, options: Dict[str, Any]):
        """Add list to PDF."""
        styles = getSampleStyleSheet()
        
        for list_item in node.children:
            if list_item.node_type == NodeType.LIST_ITEM:
                is_ordered = list_item.metadata.get('ordered', False)
                content = list_item.content
                
                # Create bullet or number
                if is_ordered:
                    marker = list_item.metadata.get('marker', '1.')
                    text = f"{marker} {content}"
                else:
                    text = f"• {content}"
                
                # Add indentation for nested lists
                level = list_item.level or 0
                indent = level * 0.25 * inch
                
                para_style = ParagraphStyle(
                    name='ListItem',
                    parent=styles['Normal'],
                    leftIndent=indent,
                    fontSize=11,
                    spaceAfter=4
                )
                
                para = Paragraph(text, para_style)
                self.story.append(para)
        
        self.story.append(Spacer(1, 0.1 * inch))
    
    def _add_table(self, node: ASTNode, options: Dict[str, Any]):
        """Add table to PDF."""
        if not node.metadata:
            return
        
        headers = node.metadata.get('headers', [])
        rows = node.metadata.get('rows', [])
        
        if not headers:
            return
        
        # Build table data
        table_data = [headers]
        table_data.extend(rows)
        
        # Create table
        table = Table(table_data)
        
        # Style table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#FFFFFF')),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.2 * inch))
    
    def _add_code_block(self, node: ASTNode, options: Dict[str, Any]):
        """Add code block to PDF."""
        content = node.content
        
        # Use Preformatted for code blocks
        code_style = ParagraphStyle(
            name='CodeBlock',
            fontName='Courier',
            fontSize=9,
            leftIndent=0.25 * inch,
            rightIndent=0.25 * inch,
            backColor=HexColor('#F5F5F5'),
            borderColor=HexColor('#CCCCCC'),
            borderWidth=1,
            borderPadding=8,
            spaceBefore=6,
            spaceAfter=6
        )
        
        # Use Preformatted to preserve formatting
        code = Preformatted(content, code_style, maxLineLength=80)
        self.story.append(code)
        self.story.append(Spacer(1, 0.2 * inch))
    
    def _add_blockquote(self, node: ASTNode, options: Dict[str, Any]):
        """Add blockquote to PDF."""
        content = node.content
        
        quote_style = ParagraphStyle(
            name='Blockquote',
            parent=getSampleStyleSheet()['Normal'],
            leftIndent=0.5 * inch,
            rightIndent=0.5 * inch,
            fontStyle='italic',
            fontSize=11,
            spaceBefore=6,
            spaceAfter=6
        )
        
        para = Paragraph(content, quote_style)
        self.story.append(para)
        self.story.append(Spacer(1, 0.1 * inch))
    
    def _add_horizontal_rule(self):
        """Add horizontal rule to PDF."""
        # Create a simple line using a table
        line_table = Table([['']], colWidths=[self.page_width - 2 * inch])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 1, gray),
        ]))
        self.story.append(line_table)
        self.story.append(Spacer(1, 0.2 * inch))
    
    def _add_image(self, node: ASTNode, options: Dict[str, Any]):
        """Add image to PDF."""
        image_src = node.attributes.get('src')
        if not image_src:
            return
        
        # Resolve image path
        image_path = Path(image_src)
        if not image_path.is_absolute():
            base_path = options.get('base_path', '.')
            image_path = Path(base_path) / image_path
        
        if not image_path.exists():
            if options.get('skip_missing_images', False):
                return
            raise FileError(
                f"Image file not found: {image_src}",
                file_path=str(image_path),
                operation="read"
            )
        
        try:
            # Add image
            img = RLImage(str(image_path), width=6 * inch, height=None)
            self.story.append(img)
            self.story.append(Spacer(1, 0.2 * inch))
        
        except Exception as e:
            raise FileError(
                f"Failed to add image: {str(e)}",
                file_path=str(image_path),
                operation="read"
            ) from e
    
    def _add_table_of_contents(self, ast: ASTNode):
        """Add table of contents page."""
        styles = getSampleStyleSheet()
        
        # TOC title
        toc_title = Paragraph("Table of Contents", styles['Heading1'])
        self.story.append(toc_title)
        self.story.append(Spacer(1, 0.3 * inch))
        
        # Extract headings for TOC
        headings = []
        self._extract_headings_for_toc(ast, headings)
        
        # Add TOC entries
        for heading in headings:
            level = heading['level']
            content = heading['content']
            indent = (level - 1) * 0.25 * inch
            
            toc_style = ParagraphStyle(
                name='TOC',
                parent=styles['Normal'],
                leftIndent=indent,
                fontSize=11,
                spaceAfter=4
            )
            
            para = Paragraph(content, toc_style)
            self.story.append(para)
        
        self.story.append(PageBreak())
    
    def _extract_headings_for_toc(self, node: ASTNode, headings: List[Dict]):
        """Extract headings for table of contents."""
        if node.node_type == NodeType.HEADING:
            headings.append({
                'level': node.level or 1,
                'content': node.content
            })
        
        for child in node.children:
            self._extract_headings_for_toc(child, headings)
    
    def _add_bookmarks(self):
        """Add bookmarks to PDF."""
        # Bookmarks are added during heading processing
        # ReportLab handles bookmarks through outline
        pass
    
    def _on_first_page(self, canvas_obj, doc):
        """Callback for first page."""
        self._add_page_number(canvas_obj, doc)
    
    def _on_later_pages(self, canvas_obj, doc):
        """Callback for later pages."""
        self._add_page_number(canvas_obj, doc)
    
    def _add_page_number(self, canvas_obj, doc):
        """Add page number to footer."""
        page_num = canvas_obj.getPageNumber()
        text = f"Page {page_num}"
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica', 9)
        canvas_obj.drawCentredString(
            self.page_width / 2.0,
            0.75 * inch,
            text
        )
        canvas_obj.restoreState()
    
    def _find_first_heading(self, node: ASTNode, level: int) -> Optional[ASTNode]:
        """Find first heading of specified level."""
        if node.node_type == NodeType.HEADING and node.level == level:
            return node
        
        for child in node.children:
            result = self._find_first_heading(child, level)
            if result:
                return result
        
        return None

