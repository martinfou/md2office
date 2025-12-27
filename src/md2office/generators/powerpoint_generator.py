"""
PowerPoint Document Generator

Implements Epic 3: PowerPoint Conversion
Generates Microsoft PowerPoint (.pptx) presentations from AST.
"""

from typing import Dict, Any, Optional, List
from io import BytesIO
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    PPTX_AVAILABLE = True
except ImportError:
    PPTX_AVAILABLE = False

from ..parser.ast_builder import ASTNode, NodeType
from ..router.content_router import FormatGenerator, OutputFormat
from ..errors import ConversionError, FileError
from ..styling.style import StylePreset, get_style_preset


class PowerPointGenerator(FormatGenerator):
    """
    Generates PowerPoint (.pptx) presentations from AST.
    
    Implements Story 3.1: PowerPoint Document Generator Core
    """
    
    def __init__(self):
        """Initialize PowerPoint generator."""
        if not PPTX_AVAILABLE:
            raise ImportError(
                "python-pptx is required for PowerPoint generation. "
                "Install with: pip install python-pptx"
            )
        self.presentation: Optional[Presentation] = None
        self.current_slide = None
        self.current_style_preset: Optional[StylePreset] = None
        self.slide_width = Inches(10)
        self.slide_height = Inches(7.5)
    
    def generate(self, ast: ASTNode, options: Dict[str, Any]) -> bytes:
        """
        Generate PowerPoint presentation from AST.
        
        Args:
            ast: Root AST node
            options: Generation options
            
        Returns:
            Generated PowerPoint presentation as bytes
            
        Raises:
            ConversionError: If generation fails
        """
        try:
            # Initialize presentation
            self.presentation = Presentation()
            self.presentation.slide_width = self.slide_width
            self.presentation.slide_height = self.slide_height
            
            # Get style preset
            style_name = options.get('style', 'default')
            self.current_style_preset = get_style_preset(style_name)
            
            # Set presentation metadata
            self._set_presentation_metadata(ast, options)
            
            # Process AST nodes
            self._process_node(ast, options)
            
            # Save to bytes
            output = BytesIO()
            self.presentation.save(output)
            return output.getvalue()
        
        except Exception as e:
            raise ConversionError(
                f"Failed to generate PowerPoint presentation: {str(e)}",
                format="powerpoint",
                stage="generation"
            ) from e
    
    def get_file_extension(self) -> str:
        """Get file extension for PowerPoint format."""
        return ".pptx"
    
    def _set_presentation_metadata(self, ast: ASTNode, options: Dict[str, Any]):
        """Set presentation metadata."""
        # Get title from AST metadata or first H1
        title = ast.metadata.get('title')
        if not title:
            first_h1 = self._find_first_heading(ast, 1)
            if first_h1:
                title = first_h1.content
        
        if title:
            self.presentation.core_properties.title = title
        
        # Get author from metadata or options
        author = ast.metadata.get('author') or options.get('author')
        if author:
            self.presentation.core_properties.author = author
    
    def _process_node(self, node: ASTNode, options: Dict[str, Any]):
        """
        Process AST node and add to presentation.
        
        Args:
            node: AST node to process
            options: Generation options
        """
        if node.node_type == NodeType.DOCUMENT:
            # Process all children of document
            for child in node.children:
                self._process_node(child, options)
        
        elif node.node_type == NodeType.SECTION:
            # Process section - may create new slide
            # Section processing handles its own children, so don't recurse here
            self._process_section(node, options)
        
        elif node.node_type == NodeType.HEADING:
            self._process_heading(node, options)
        
        elif node.node_type == NodeType.PARAGRAPH:
            self._add_paragraph_to_slide(node, options)
        
        elif node.node_type == NodeType.LIST:
            self._add_list_to_slide(node, options)
        
        elif node.node_type == NodeType.TABLE:
            self._add_table_to_slide(node, options)
        
        elif node.node_type == NodeType.CODE_BLOCK:
            self._add_code_block_to_slide(node, options)
        
        elif node.node_type == NodeType.BLOCKQUOTE:
            self._add_blockquote_to_slide(node, options)
        
        elif node.node_type == NodeType.IMAGE:
            self._add_image_to_slide(node, options)
        
        # Process children recursively (but not for SECTION nodes - they handle their own children)
        # Also skip already-processed content nodes
        for child in node.children:
            if child.node_type not in [NodeType.HEADING, NodeType.PARAGRAPH,
                                      NodeType.LIST, NodeType.TABLE,
                                      NodeType.CODE_BLOCK, NodeType.BLOCKQUOTE,
                                      NodeType.IMAGE, NodeType.SECTION]:
                self._process_node(child, options)
    
    def _process_section(self, node: ASTNode, options: Dict[str, Any]):
        """Process section node - creates slides based on heading level."""
        level = node.level or 1
        
        # Find heading in section
        heading = None
        for child in node.children:
            if child.node_type == NodeType.HEADING:
                heading = child
                break
        
        if level == 1:
            # H1 section - create title slide
            self._create_title_slide(heading, options)
        elif level == 2:
            # H2 section - create section header slide
            self._create_section_slide(heading, options)
        else:
            # H3+ section - may create content slide or add to current slide
            self._create_content_slide(heading, options)
        
        # Process section content (excluding heading and nested sections)
        # Nested sections will be processed separately to create their own slides
        # Note: Sections can be nested under headings, so we need to check heading children too
        for child in node.children:
            if child.node_type == NodeType.HEADING:
                # Heading already processed above, but check if it has nested sections as children
                for heading_child in child.children:
                    if heading_child.node_type == NodeType.SECTION:
                        # Process nested sections that are children of the heading
                        self._process_section(heading_child, options)
                    else:
                        # Process other heading children (content)
                        self._process_node(heading_child, options)
            elif child.node_type == NodeType.SECTION:
                # Process nested sections to create new slides
                self._process_section(child, options)
            else:
                # Process content nodes (paragraphs, lists, etc.)
                self._process_node(child, options)
    
    def _process_heading(self, node: ASTNode, options: Dict[str, Any]):
        """Process heading node."""
        level = node.level or 1
        
        if level == 1:
            self._create_title_slide(node, options)
        elif level == 2:
            self._create_section_slide(node, options)
        else:
            # H3+ - add as slide title or content header
            if not self.current_slide:
                self._create_content_slide(node, options)
            else:
                # Add as subsection header in current slide
                self._add_subsection_header(node, options)
    
    def _create_title_slide(self, heading: Optional[ASTNode], options: Dict[str, Any]):
        """Create title slide from H1 heading."""
        layout = self.presentation.slide_layouts[0]  # Title slide layout
        slide = self.presentation.slides.add_slide(layout)
        self.current_slide = slide
        
        title = slide.shapes.title
        subtitle = slide.placeholders[1] if len(slide.placeholders) > 1 else None
        
        if heading:
            title.text = heading.content
        else:
            title.text = "Presentation"
        
        # Set subtitle if available
        if subtitle:
            # Try to get subtitle from metadata or first paragraph
            subtitle_text = options.get('subtitle', '')
            if subtitle_text:
                subtitle.text = subtitle_text
    
    def _create_section_slide(self, heading: Optional[ASTNode], options: Dict[str, Any]):
        """Create section header slide from H2 heading."""
        layout = self.presentation.slide_layouts[1]  # Title and Content layout
        slide = self.presentation.slides.add_slide(layout)
        self.current_slide = slide
        
        title = slide.shapes.title
        if heading:
            title.text = heading.content
        else:
            title.text = "Section"
    
    def _create_content_slide(self, heading: Optional[ASTNode], options: Dict[str, Any]):
        """Create content slide."""
        layout = self.presentation.slide_layouts[1]  # Title and Content layout
        slide = self.presentation.slides.add_slide(layout)
        self.current_slide = slide
        
        title = slide.shapes.title
        if heading:
            title.text = heading.content
        else:
            title.text = ""
    
    def _add_subsection_header(self, node: ASTNode, options: Dict[str, Any]):
        """Add subsection header to current slide."""
        if not self.current_slide:
            return
        
        # Find content placeholder
        content_placeholder = None
        for shape in self.current_slide.shapes:
            if hasattr(shape, 'placeholder_format') and shape.placeholder_format.idx == 1:
                content_placeholder = shape
                break
        
        if content_placeholder and hasattr(content_placeholder, 'text_frame'):
            text_frame = content_placeholder.text_frame
            p = text_frame.add_paragraph()
            p.text = node.content
            p.level = (node.level or 3) - 2  # Convert H3+ to paragraph level
            p.font.bold = True
            p.font.size = Pt(20)
    
    def _add_paragraph_to_slide(self, node: ASTNode, options: Dict[str, Any]):
        """Add paragraph to current slide."""
        if not self.current_slide:
            self._create_content_slide(None, options)
        
        # Find content placeholder
        content_placeholder = None
        for shape in self.current_slide.shapes:
            if hasattr(shape, 'placeholder_format') and shape.placeholder_format.idx == 1:
                content_placeholder = shape
                break
        
        if content_placeholder and hasattr(content_placeholder, 'text_frame'):
            text_frame = content_placeholder.text_frame
            p = text_frame.add_paragraph()
            p.text = node.content
            p.font.size = Pt(18)
            p.space_after = Pt(12)
    
    def _add_list_to_slide(self, node: ASTNode, options: Dict[str, Any]):
        """Add list to current slide."""
        if not self.current_slide:
            self._create_content_slide(None, options)
        
        # Find content placeholder
        content_placeholder = None
        for shape in self.current_slide.shapes:
            if hasattr(shape, 'placeholder_format') and shape.placeholder_format.idx == 1:
                content_placeholder = shape
                break
        
        if content_placeholder and hasattr(content_placeholder, 'text_frame'):
            text_frame = content_placeholder.text_frame
            
            for list_item in node.children:
                if list_item.node_type == NodeType.LIST_ITEM:
                    p = text_frame.add_paragraph()
                    p.text = list_item.content
                    p.level = list_item.level or 0
                    p.font.size = Pt(18)
                    
                    # Set bullet style
                    is_ordered = list_item.metadata.get('ordered', False)
                    if is_ordered:
                        # Numbered list (simplified - full implementation would handle numbering)
                        p.text = f"{list_item.metadata.get('marker', '1.')} {list_item.content}"
    
    def _add_table_to_slide(self, node: ASTNode, options: Dict[str, Any]):
        """Add table to current slide."""
        if not self.current_slide:
            self._create_content_slide(None, options)
        
        if not node.metadata:
            return
        
        headers = node.metadata.get('headers', [])
        rows = node.metadata.get('rows', [])
        
        if not headers:
            return
        
        # Create table shape
        left = Inches(1)
        top = Inches(2)
        width = Inches(8)
        height = Inches(min(4, len(rows) * 0.5 + 1))
        
        table_shape = self.current_slide.shapes.add_table(
            rows=len(rows) + 1,
            cols=len(headers),
            left=left,
            top=top,
            width=width,
            height=height
        )
        
        table = table_shape.table
        
        # Add header row
        for col_idx, header in enumerate(headers):
            cell = table.cell(0, col_idx)
            cell.text = header
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0xE8, 0xE8, 0xE8)
            
            # Make header text bold
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
        
        # Add data rows
        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_data in enumerate(row_data):
                if col_idx < len(headers):
                    cell = table.cell(row_idx + 1, col_idx)
                    cell.text = cell_data
    
    def _add_code_block_to_slide(self, node: ASTNode, options: Dict[str, Any]):
        """Add code block to current slide."""
        if not self.current_slide:
            self._create_content_slide(None, options)
        
        content = node.content
        language = node.metadata.get('language', '')
        
        # Create text box for code
        left = Inches(1)
        top = Inches(2)
        width = Inches(8)
        height = Inches(4)
        
        text_box = self.current_slide.shapes.add_textbox(left, top, width, height)
        text_frame = text_box.text_frame
        text_frame.word_wrap = True
        
        # Set background color
        fill = text_box.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(0xF5, 0xF5, 0xF5)
        
        # Add code text
        p = text_frame.paragraphs[0]
        p.text = content
        p.font.name = 'Courier New'
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    
    def _add_blockquote_to_slide(self, node: ASTNode, options: Dict[str, Any]):
        """Add blockquote to current slide."""
        if not self.current_slide:
            self._create_content_slide(None, options)
        
        content = node.content
        
        # Find content placeholder
        content_placeholder = None
        for shape in self.current_slide.shapes:
            if hasattr(shape, 'placeholder_format') and shape.placeholder_format.idx == 1:
                content_placeholder = shape
                break
        
        if content_placeholder and hasattr(content_placeholder, 'text_frame'):
            text_frame = content_placeholder.text_frame
            p = text_frame.add_paragraph()
            p.text = content
            p.font.italic = True
            p.font.size = Pt(16)
            p.left_indent = Inches(0.5)
    
    def _add_image_to_slide(self, node: ASTNode, options: Dict[str, Any]):
        """Add image to current slide."""
        if not self.current_slide:
            self._create_content_slide(None, options)
        
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
            # Add image to slide
            left = Inches(1)
            top = Inches(2)
            width = Inches(6)
            
            self.current_slide.shapes.add_picture(str(image_path), left, top, width=width)
        
        except Exception as e:
            raise FileError(
                f"Failed to add image: {str(e)}",
                file_path=str(image_path),
                operation="read"
            ) from e
    
    def _find_first_heading(self, node: ASTNode, level: int) -> Optional[ASTNode]:
        """Find first heading of specified level."""
        if node.node_type == NodeType.HEADING and node.level == level:
            return node
        
        for child in node.children:
            result = self._find_first_heading(child, level)
            if result:
                return result
        
        return None

