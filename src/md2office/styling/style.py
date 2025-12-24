"""
Styling System Foundation

Implements Story 1.6: Styling System Foundation
Unified styling system for consistent visual design across formats.
"""

from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, field


class FontFamily(Enum):
    """Font family options."""
    SANS_SERIF = "sans-serif"
    SERIF = "serif"
    MONOSPACE = "monospace"


@dataclass
class FontStyle:
    """Font style definition."""
    family: str = "sans-serif"
    size: float = 12.0
    weight: str = "normal"  # normal, bold
    style: str = "normal"  # normal, italic
    color: str = "#000000"


@dataclass
class HeadingStyle:
    """Heading style definition."""
    font: FontStyle = field(default_factory=lambda: FontStyle(size=16.0, weight="bold"))
    spacing_before: float = 12.0
    spacing_after: float = 6.0
    page_break_before: bool = False


@dataclass
class ParagraphStyle:
    """Paragraph style definition."""
    font: FontStyle = field(default_factory=FontStyle)
    spacing_before: float = 0.0
    spacing_after: float = 6.0
    alignment: str = "left"  # left, center, right, justify
    line_height: float = 1.5


@dataclass
class CodeBlockStyle:
    """Code block style definition."""
    font: FontStyle = field(default_factory=lambda: FontStyle(
        family="monospace",
        size=10.0
    ))
    background_color: str = "#F5F5F5"
    border_color: str = "#CCCCCC"
    border_width: float = 1.0
    padding: float = 8.0


@dataclass
class TableStyle:
    """Table style definition."""
    header_background: str = "#E8E8E8"
    header_font: FontStyle = field(default_factory=lambda: FontStyle(weight="bold"))
    border_color: str = "#CCCCCC"
    border_width: float = 1.0
    cell_padding: float = 6.0


@dataclass
class StylePreset:
    """
    Complete style preset for a document format.
    
    Defines all styling elements for consistent visual design.
    """
    name: str
    heading_styles: Dict[int, HeadingStyle] = field(default_factory=dict)
    paragraph_style: ParagraphStyle = field(default_factory=ParagraphStyle)
    code_block_style: CodeBlockStyle = field(default_factory=CodeBlockStyle)
    table_style: TableStyle = field(default_factory=TableStyle)
    link_color: str = "#0066CC"
    blockquote_border_color: str = "#CCCCCC"
    blockquote_background: str = "#F9F9F9"
    
    def get_heading_style(self, level: int) -> HeadingStyle:
        """
        Get heading style for level.
        
        Args:
            level: Heading level (1-6)
            
        Returns:
            Heading style, or default if not defined
        """
        if level in self.heading_styles:
            return self.heading_styles[level]
        
        # Return default heading style
        return HeadingStyle(
            font=FontStyle(size=16.0 - (level - 1) * 2, weight="bold"),
            spacing_before=12.0 if level == 1 else 8.0,
            spacing_after=6.0
        )


class StyleManager:
    """
    Manages style presets and application.
    
    Provides access to predefined style presets and allows
    custom style creation and inheritance.
    """
    
    def __init__(self):
        """Initialize style manager."""
        self.presets: Dict[str, StylePreset] = {}
        self._load_default_presets()
    
    def _load_default_presets(self):
        """Load default style presets."""
        # Default preset
        default = StylePreset(
            name="default",
            heading_styles={
                1: HeadingStyle(
                    font=FontStyle(size=24.0, weight="bold"),
                    spacing_before=0.0,
                    spacing_after=12.0,
                    page_break_before=False
                ),
                2: HeadingStyle(
                    font=FontStyle(size=20.0, weight="bold"),
                    spacing_before=12.0,
                    spacing_after=8.0
                ),
                3: HeadingStyle(
                    font=FontStyle(size=16.0, weight="bold"),
                    spacing_before=8.0,
                    spacing_after=6.0
                )
            },
            paragraph_style=ParagraphStyle(
                font=FontStyle(size=12.0),
                spacing_after=6.0,
                line_height=1.5
            ),
            code_block_style=CodeBlockStyle(
                font=FontStyle(family="monospace", size=10.0),
                background_color="#F5F5F5",
                border_color="#CCCCCC",
                padding=8.0
            ),
            table_style=TableStyle(
                header_background="#E8E8E8",
                border_color="#CCCCCC",
                cell_padding=6.0
            )
        )
        self.presets["default"] = default
        
        # Minimal preset
        minimal = StylePreset(
            name="minimal",
            heading_styles={
                1: HeadingStyle(
                    font=FontStyle(size=20.0, weight="bold"),
                    spacing_before=0.0,
                    spacing_after=8.0
                ),
                2: HeadingStyle(
                    font=FontStyle(size=18.0, weight="bold"),
                    spacing_before=8.0,
                    spacing_after=6.0
                ),
                3: HeadingStyle(
                    font=FontStyle(size=16.0, weight="bold"),
                    spacing_before=6.0,
                    spacing_after=4.0
                )
            },
            paragraph_style=ParagraphStyle(
                font=FontStyle(size=11.0),
                spacing_after=4.0,
                line_height=1.4
            ),
            code_block_style=CodeBlockStyle(
                font=FontStyle(family="monospace", size=9.0),
                background_color="#FAFAFA",
                border_color="#DDDDDD",
                padding=6.0
            ),
            table_style=TableStyle(
                header_background="#F0F0F0",
                border_color="#DDDDDD",
                cell_padding=4.0
            )
        )
        self.presets["minimal"] = minimal
        
        # Professional preset
        professional = StylePreset(
            name="professional",
            heading_styles={
                1: HeadingStyle(
                    font=FontStyle(size=28.0, weight="bold", color="#1A1A1A"),
                    spacing_before=0.0,
                    spacing_after=16.0,
                    page_break_before=True
                ),
                2: HeadingStyle(
                    font=FontStyle(size=22.0, weight="bold", color="#2A2A2A"),
                    spacing_before=16.0,
                    spacing_after=12.0
                ),
                3: HeadingStyle(
                    font=FontStyle(size=18.0, weight="bold", color="#3A3A3A"),
                    spacing_before=12.0,
                    spacing_after=8.0
                )
            },
            paragraph_style=ParagraphStyle(
                font=FontStyle(size=12.0, color="#333333"),
                spacing_after=8.0,
                line_height=1.6,
                alignment="justify"
            ),
            code_block_style=CodeBlockStyle(
                font=FontStyle(family="monospace", size=10.0),
                background_color="#F8F8F8",
                border_color="#D0D0D0",
                border_width=1.5,
                padding=10.0
            ),
            table_style=TableStyle(
                header_background="#E0E0E0",
                header_font=FontStyle(weight="bold", color="#1A1A1A"),
                border_color="#B0B0B0",
                border_width=1.5,
                cell_padding=8.0
            ),
            link_color="#0066CC",
            blockquote_border_color="#CCCCCC",
            blockquote_background="#F5F5F5"
        )
        self.presets["professional"] = professional
    
    def get_preset(self, name: str) -> StylePreset:
        """
        Get style preset by name.
        
        Args:
            name: Preset name
            
        Returns:
            Style preset
            
        Raises:
            ValueError: If preset not found
        """
        if name not in self.presets:
            raise ValueError(f"Style preset '{name}' not found. Available: {list(self.presets.keys())}")
        return self.presets[name]
    
    def register_preset(self, preset: StylePreset):
        """
        Register a custom style preset.
        
        Args:
            preset: Style preset to register
        """
        self.presets[preset.name] = preset
    
    def create_custom_preset(self, base_name: str, overrides: Dict[str, Any]) -> StylePreset:
        """
        Create custom preset by inheriting from base and applying overrides.
        
        Args:
            base_name: Base preset name
            overrides: Style overrides
            
        Returns:
            New custom preset
        """
        base = self.get_preset(base_name)
        
        # Create copy of base preset
        import copy
        custom = copy.deepcopy(base)
        custom.name = overrides.get('name', f"{base_name}_custom")
        
        # Apply overrides (simplified - full implementation would handle all fields)
        if 'heading_styles' in overrides:
            for level, style_dict in overrides['heading_styles'].items():
                if level in custom.heading_styles:
                    # Update existing heading style
                    for key, value in style_dict.items():
                        setattr(custom.heading_styles[level], key, value)
                else:
                    # Create new heading style
                    custom.heading_styles[level] = HeadingStyle(**style_dict)
        
        if 'paragraph_style' in overrides:
            for key, value in overrides['paragraph_style'].items():
                setattr(custom.paragraph_style, key, value)
        
        return custom


# Global style manager instance
_style_manager = StyleManager()


def get_style_preset(name: str) -> StylePreset:
    """
    Get style preset by name.
    
    Args:
        name: Preset name
        
    Returns:
        Style preset
    """
    return _style_manager.get_preset(name)


def apply_style(preset: StylePreset, format_type: str) -> Dict[str, Any]:
    """
    Apply style preset to format-specific representation.
    
    Args:
        preset: Style preset
        format_type: Target format ('word', 'powerpoint', 'pdf')
        
    Returns:
        Format-specific style dictionary
    """
    # This would be implemented format-specifically
    # For now, return a generic representation
    return {
        'preset_name': preset.name,
        'format': format_type,
        'headings': {level: {
            'font_size': style.font.size,
            'font_weight': style.font.weight,
            'spacing_before': style.spacing_before,
            'spacing_after': style.spacing_after
        } for level, style in preset.heading_styles.items()},
        'paragraph': {
            'font_size': preset.paragraph_style.font.size,
            'line_height': preset.paragraph_style.line_height,
            'spacing_after': preset.paragraph_style.spacing_after
        },
        'code_block': {
            'background_color': preset.code_block_style.background_color,
            'border_color': preset.code_block_style.border_color,
            'padding': preset.code_block_style.padding
        }
    }

