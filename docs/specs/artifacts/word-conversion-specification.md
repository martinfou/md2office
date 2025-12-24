# Word Conversion Specification

## Overview

This specification defines the complete conversion strategy from Microsoft Copilot-generated markdown to Microsoft Word (.docx) format. The conversion preserves document structure, formatting, and content while adapting markdown elements to Word's native document model. The specification ensures professional document appearance, proper hierarchy preservation, and compatibility with Word's styling system.

### Conversion Goals

1. **Structure Preservation**: Maintain markdown heading hierarchy as Word heading styles
2. **Content Fidelity**: Preserve all content including text, code, tables, and images
3. **Professional Formatting**: Apply consistent, professional styling throughout
4. **Word Compatibility**: Leverage Word's built-in features (styles, TOC, navigation)
5. **Accessibility**: Maintain document structure for screen readers and navigation

### Conversion Approach

The conversion follows a structured approach:
1. Parse markdown into AST (as defined in conversion architecture)
2. Transform AST nodes to Word document elements
3. Apply Word styles and formatting
4. Embed media and resources
5. Generate final .docx file

## Document Structure

### Word Document Organization

Word documents are organized hierarchically:

```
Word Document (.docx)
├── Document Properties (metadata)
│   ├── Title
│   ├── Author
│   ├── Subject
│   └── Keywords
├── Document Sections
│   ├── Section 1 (default)
│   │   ├── Paragraphs
│   │   ├── Headings (with styles)
│   │   ├── Lists
│   │   ├── Tables
│   │   ├── Images
│   │   └── Code Blocks
│   └── Additional Sections (optional)
└── Relationships
    ├── Images
    ├── Hyperlinks
    └── Styles
```

### Document Sections

- **Default Section**: Single section for most documents
- **Section Breaks**: Optional section breaks at H1 boundaries for different page layouts
- **Page Breaks**: Optional page breaks before major headings (H1/H2)

### Document Metadata

Extract and set document properties from markdown:

- **Title**: From first H1 heading or front-matter
- **Author**: From front-matter or default
- **Subject**: From document content or front-matter
- **Keywords**: From front-matter or extracted from content
- **Creation Date**: Current date/time
- **Last Modified**: Current date/time

## Element Mappings

### Headers (H1-H6)

Markdown headers map directly to Word's built-in heading styles, preserving hierarchy and enabling Word features like table of contents and navigation pane.

| Markdown | Word Style | Font Family | Font Size | Font Weight | Color | Spacing Before | Spacing After | Keep With Next |
|----------|------------|-------------|-----------|-------------|-------|----------------|---------------|----------------|
| H1 (`#`) | Heading 1 | Calibri (or theme font) | 18pt | Bold | Theme Color | 12pt | 6pt | Yes |
| H2 (`##`) | Heading 2 | Calibri (or theme font) | 16pt | Bold | Theme Color | 10pt | 4pt | Yes |
| H3 (`###`) | Heading 3 | Calibri (or theme font) | 14pt | Bold | Theme Color | 8pt | 4pt | Yes |
| H4 (`####`) | Heading 4 | Calibri (or theme font) | 12pt | Bold | Theme Color | 6pt | 2pt | Yes |
| H5 (`#####`) | Heading 5 | Calibri (or theme font) | 11pt | Bold | Theme Color | 4pt | 2pt | No |
| H6 (`######`) | Heading 6 | Calibri (or theme font) | 10pt | Bold | Theme Color | 4pt | 2pt | No |

#### Header Implementation Details

- **Style Application**: Use Word's built-in heading styles (Heading 1-6)
- **Navigation**: Headings automatically appear in Word navigation pane
- **Table of Contents**: Headings can be used for auto-generated TOC
- **Cross-References**: Headings can be referenced for cross-references
- **Page Breaks**: Optional page break before H1 (configurable)
- **Section Breaks**: Optional section break before H1 for different page layouts (configurable)

#### Header Style Customization

If custom styling is needed:
- Override built-in heading styles
- Maintain consistent font family and sizes
- Preserve hierarchy through size differences
- Use theme colors for consistency

### Paragraphs

Regular markdown paragraphs map to Word's Normal style with appropriate spacing.

| Markdown | Word Style | Font Family | Font Size | Line Spacing | Spacing Before | Spacing After |
|----------|------------|-------------|-----------|--------------|----------------|---------------|
| Paragraph | Normal | Calibri (or theme font) | 11pt | Single (1.0) | 0pt | 6pt |

#### Paragraph Implementation Details

- **Style**: Use Word's Normal style or custom paragraph style
- **Spacing**: Consistent spacing between paragraphs (6pt after)
- **Alignment**: Left-aligned (default), support center/right if specified
- **Indentation**: No indentation (first line or hanging) unless specified
- **Line Breaks**: Preserve hard line breaks (two trailing spaces in markdown)

### Emphasis and Strong Text

Text emphasis maps to Word character-level formatting.

| Markdown | Word Formatting | Font Style/Weight |
|----------|-----------------|-------------------|
| Italic (`*text*` or `_text_`) | Italic | Font style: Italic |
| Bold (`**text**` or `__text__`) | Bold | Font weight: Bold |
| Bold Italic (`***text***`) | Bold + Italic | Font weight: Bold, Font style: Italic |

#### Emphasis Implementation Details

- **Character Formatting**: Apply formatting at character level within paragraphs
- **Nested Emphasis**: Support nested emphasis (bold within italic, etc.)
- **Font Consistency**: Use same font family as paragraph
- **Preservation**: Preserve emphasis in all contexts (paragraphs, lists, tables, etc.)

### Lists

Markdown lists map to Word's list formatting system, preserving nesting and formatting.

#### Unordered Lists

| Markdown | Word List Type | Bullet Style | Indentation | Font |
|----------|----------------|--------------|-------------|------|
| `- item` | Bulleted List | Round bullet (•) | 0.25" per level | Same as paragraph |
| `* item` | Bulleted List | Round bullet (•) | 0.25" per level | Same as paragraph |
| `+ item` | Bulleted List | Round bullet (•) | 0.25" per level | Same as paragraph |

#### Ordered Lists

| Markdown | Word List Type | Number Format | Indentation | Font |
|----------|----------------|---------------|-------------|------|
| `1. item` | Numbered List | Arabic numerals (1, 2, 3...) | 0.25" per level | Same as paragraph |
| `2. item` | Numbered List | Arabic numerals (continues) | 0.25" per level | Same as paragraph |

#### Task Lists (GFM)

| Markdown | Word Format | Checkbox Style | Indentation |
|----------|------------|----------------|-------------|
| `- [ ]` (unchecked) | Bulleted List with Checkbox | ☐ (empty checkbox) | 0.25" per level |
| `- [x]` (checked) | Bulleted List with Checkbox | ☑ (checked checkbox) | 0.25" per level |

#### List Implementation Details

- **List Formatting**: Use Word's list formatting (List Bullet, List Number styles)
- **Nesting**: Preserve list nesting with indentation (0.25" per level)
- **Mixed Lists**: Support mixing ordered and unordered lists
- **List Continuation**: Continue numbering/formatting across paragraphs if needed
- **Task Lists**: Use checkbox symbols or Word content controls for task lists
- **Spacing**: Consistent spacing between list items (6pt after)

#### List Style Specifications

**Bulleted List Style**:
- Font: Same as Normal paragraph
- Bullet: Round bullet (•) or custom bullet
- Indentation: 0.25" hanging indent
- Spacing: 6pt after each item

**Numbered List Style**:
- Font: Same as Normal paragraph
- Numbering: Arabic numerals (1, 2, 3...)
- Indentation: 0.25" hanging indent
- Spacing: 6pt after each item
- Continue numbering: Yes (across list breaks)

**Task List Style**:
- Font: Same as Normal paragraph
- Bullet: Checkbox symbol (☐/☑) or content control
- Indentation: 0.25" hanging indent
- Spacing: 6pt after each item

### Links

Markdown links map to Word hyperlink fields with display text and target URLs.

| Markdown | Word Element | Display Text | Target URL | Style |
|----------|-------------|--------------|------------|-------|
| `[text](url)` | Hyperlink Field | "text" | url | Blue, underlined |
| `[text][ref]` | Hyperlink Field | "text" | resolved URL | Blue, underlined |
| `<url>` | Hyperlink Field | url | url | Blue, underlined |

#### Link Implementation Details

- **Hyperlink Fields**: Use Word hyperlink fields (not just formatted text)
- **Display Text**: Show link text, not raw URL (unless autolink)
- **URL Resolution**: Resolve reference links to actual URLs
- **Styling**: Blue color (#0563C1), underlined
- **Hover**: Show URL in tooltip
- **Clickable**: Links are clickable in Word
- **External Links**: Mark external links appropriately

#### Link Style Specifications

- **Font Color**: Blue (#0563C1 or theme link color)
- **Underline**: Single underline
- **Font**: Same as surrounding text
- **Hover Effect**: Show URL in status bar or tooltip

### Images

Markdown images map to Word inline images embedded in the document.

| Markdown | Word Element | Placement | Sizing | Alt Text |
|----------|-------------|-----------|--------|----------|
| `![alt](url)` | Inline Image | Inline with text | Preserve aspect ratio | Stored in image properties |

#### Image Implementation Details

- **Embedding**: Embed images directly in Word document (not linked)
- **Format Support**: PNG, JPEG, GIF, SVG (convert SVG to PNG if needed)
- **Placement**: Inline with text flow
- **Sizing**: 
  - Preserve aspect ratio
  - Default width: 6.5" (or page width minus margins)
  - Scale proportionally if too large
- **Alt Text**: Store alt text in image properties for accessibility
- **Path Resolution**: Resolve relative paths relative to markdown file location
- **Missing Images**: Use placeholder or skip with warning

#### Image Style Specifications

- **Alignment**: Left-aligned (default), center/right if specified
- **Text Wrapping**: Inline with text (default)
- **Borders**: No border (default), optional border for emphasis
- **Caption**: Optional caption below image (if specified in markdown)

#### Image Path Resolution

1. **Relative Paths**: Resolve relative to markdown file directory
2. **Absolute Paths**: Use as-is
3. **URLs**: Download and embed (or link, configurable)
4. **Missing Images**: Log warning, use placeholder or skip

### Code Blocks

Markdown code blocks map to Word formatted paragraphs or text boxes with monospace font and background.

#### Fenced Code Blocks

| Markdown | Word Element | Font | Background | Border | Preserve Formatting |
|----------|-------------|------|------------|--------|---------------------|
| ` ```lang` | Formatted Paragraph or Text Box | Monospace (Courier New, 10pt) | Light gray (#F5F5F5) | Optional (1pt solid #CCCCCC) | Yes (whitespace, line breaks) |

#### Inline Code

| Markdown | Word Formatting | Font | Background |
|----------|----------------|------|------------|
| `` `code` `` | Character Formatting | Monospace (Courier New, 10pt) | Light gray (#F5F5F5) |

#### Code Block Implementation Details

- **Font**: Monospace font (Courier New, Consolas, or Lucida Console)
- **Font Size**: 10pt (slightly smaller than body text)
- **Background**: Light gray (#F5F5F5) for code blocks
- **Border**: Optional 1pt solid border (#CCCCCC)
- **Formatting Preservation**: 
  - Preserve whitespace and indentation
  - Preserve line breaks
  - Preserve special characters
- **Language Identifier**: Preserve language identifier in comment or metadata
- **Long Code Blocks**: Preserve full content (no truncation)

#### Code Block Style Specifications

**Fenced Code Block**:
- Font: Courier New, 10pt
- Background: #F5F5F5 (light gray)
- Border: 1pt solid #CCCCCC (optional)
- Padding: 6pt all sides
- Line Spacing: Single (1.0)
- Indentation: Preserve original indentation

**Inline Code**:
- Font: Courier New, 10pt
- Background: #F5F5F5 (light gray)
- No border
- No padding (character-level formatting)

### Tables

Markdown tables map to Word table objects with proper formatting and alignment.

| Markdown | Word Element | Borders | Header Row | Alignment | Styling |
|----------|-------------|---------|------------|-----------|---------|
| Pipe table | Word Table | Yes (1pt solid) | Bold formatting | Preserved | Light shading for header |

#### Table Implementation Details

- **Table Structure**: Create Word table object with correct rows/columns
- **Borders**: 1pt solid borders (#000000 or theme color)
- **Header Row**: 
  - Bold font weight
  - Light background shading (#F2F2F2)
  - Bottom border (2pt) for emphasis
- **Column Alignment**: 
  - Left: `:---` → Left-aligned
  - Center: `:---:` → Center-aligned
  - Right: `---:` → Right-aligned
  - Default: Left-aligned
- **Cell Padding**: 6pt all sides
- **Row Height**: Auto-height based on content
- **Column Width**: Auto-fit or equal width

#### Table Style Specifications

**Table Borders**:
- All borders: 1pt solid #000000
- Header bottom border: 2pt solid #000000
- Optional: Use Word table styles for consistent appearance

**Header Row**:
- Font: Bold
- Background: #F2F2F2 (light gray)
- Alignment: Preserve markdown alignment

**Data Rows**:
- Font: Normal weight
- Background: White (alternating rows optional)
- Alignment: Preserve markdown alignment

**Cell Formatting**:
- Padding: 6pt all sides
- Vertical alignment: Top
- Text wrapping: Wrap text within cells

### Blockquotes

Markdown blockquotes map to Word formatted paragraphs with indentation and optional styling.

| Markdown | Word Element | Indentation | Border | Background | Font Style |
|----------|-------------|-------------|--------|------------|------------|
| `> text` | Formatted Paragraph | Left: 0.5" | Left border (optional) | Light background (optional) | Italic (optional) |

#### Blockquote Implementation Details

- **Indentation**: Left indent 0.5" from margin
- **Border**: Optional left border (3pt solid #CCCCCC)
- **Background**: Optional light background (#FAFAFA)
- **Font Style**: Optional italic styling
- **Spacing**: 6pt before and after
- **Nesting**: Support nested blockquotes with increased indentation

#### Blockquote Style Specifications

- **Left Indent**: 0.5" from left margin
- **Left Border**: 3pt solid #CCCCCC (optional)
- **Background**: #FAFAFA (optional)
- **Font Style**: Normal (or italic if specified)
- **Spacing**: 6pt before, 6pt after
- **Right Indent**: No right indent

### Horizontal Rules

Markdown horizontal rules map to Word horizontal lines or page breaks.

| Markdown | Word Element | Style | Placement |
|----------|-------------|-------|-----------|
| `---` | Horizontal Line | 1pt solid #CCCCCC | Between paragraphs |
| `---` (configurable) | Page Break | N/A | Before horizontal rule |

#### Horizontal Rule Implementation Details

- **Default**: Horizontal line shape (1pt solid #CCCCCC)
- **Width**: Full width of text area
- **Placement**: Between paragraphs
- **Optional**: Page break before horizontal rule (configurable)
- **Styling**: Simple line, no special effects

### Strikethrough (GFM)

Markdown strikethrough maps to Word strikethrough character formatting.

| Markdown | Word Formatting | Font Style |
|----------|----------------|------------|
| `~~text~~` | Strikethrough | Single strikethrough line |

#### Strikethrough Implementation Details

- **Character Formatting**: Apply strikethrough at character level
- **Style**: Single strikethrough line through text
- **Color**: Same as text color (or gray if desired)
- **Preservation**: Preserve in all contexts

## Style Definitions

### Word Style System

Word uses a style system with built-in styles and custom styles. The conversion leverages Word's built-in styles where possible and defines custom styles when needed.

#### Built-in Styles Used

- **Heading 1-6**: For markdown headers
- **Normal**: For paragraphs
- **List Bullet**: For unordered lists
- **List Number**: For ordered lists
- **Hyperlink**: For links (Word applies automatically)

#### Custom Styles (if needed)

- **Code Block**: For fenced code blocks
- **Inline Code**: For inline code (character style)
- **Blockquote**: For blockquotes
- **Table Header**: For table header rows (if custom styling needed)

### Complete Style Specifications

#### Heading Styles (Built-in)

**Heading 1**:
- Font: Calibri (or theme font), 18pt, Bold
- Color: Theme color (or #000000)
- Spacing: 12pt before, 6pt after
- Keep with next: Yes
- Page break before: Optional (configurable)

**Heading 2**:
- Font: Calibri (or theme font), 16pt, Bold
- Color: Theme color (or #000000)
- Spacing: 10pt before, 4pt after
- Keep with next: Yes

**Heading 3**:
- Font: Calibri (or theme font), 14pt, Bold
- Color: Theme color (or #000000)
- Spacing: 8pt before, 4pt after
- Keep with next: Yes

**Heading 4-6**: Similar pattern with decreasing sizes

#### Normal Style (Built-in)

- Font: Calibri (or theme font), 11pt, Regular
- Color: #000000 (black)
- Line spacing: Single (1.0)
- Spacing: 0pt before, 6pt after
- Alignment: Left

#### Code Block Style (Custom)

- Font: Courier New, 10pt, Regular
- Color: #000000 (black)
- Background: #F5F5F5 (light gray)
- Border: 1pt solid #CCCCCC (optional)
- Padding: 6pt all sides
- Line spacing: Single (1.0)
- Indentation: Preserve original

#### Blockquote Style (Custom)

- Font: Calibri (or theme font), 11pt, Regular (or Italic)
- Color: #000000 (black)
- Background: #FAFAFA (optional)
- Left indent: 0.5"
- Left border: 3pt solid #CCCCCC (optional)
- Spacing: 6pt before, 6pt after

## Formatting Rules

### Structure Preservation Rules

1. **Heading Hierarchy**: Maintain heading levels (H1 > H2 > H3, etc.)
2. **List Nesting**: Preserve list nesting with indentation
3. **Table Structure**: Maintain table rows, columns, and alignment
4. **Code Formatting**: Preserve whitespace, indentation, and line breaks in code
5. **Content Order**: Maintain content order from markdown

### Formatting Preservation Rules

1. **Text Formatting**: Preserve bold, italic, strikethrough
2. **Link Formatting**: Preserve link text and URLs
3. **Image Formatting**: Preserve image alt text and sizing
4. **Table Formatting**: Preserve column alignment and structure
5. **Code Formatting**: Preserve code formatting exactly

### Word-Specific Enhancements

1. **Table of Contents**: Generate TOC from heading hierarchy (optional)
2. **Cross-References**: Enable cross-references to headings (optional)
3. **Page Breaks**: Insert page breaks at major sections (optional)
4. **Section Breaks**: Insert section breaks for different layouts (optional)
5. **Document Properties**: Set title, author, and metadata

## Implementation Notes

### Word Document Generation

#### Technology Stack Options

1. **JavaScript/TypeScript**:
   - Library: `docx` (npm package)
   - Pros: Cross-platform, good API
   - Cons: May have limitations for advanced features

2. **Python**:
   - Library: `python-docx`
   - Pros: Mature, feature-rich
   - Cons: Requires Python runtime

3. **C#/.NET**:
   - Library: OpenXML SDK
   - Pros: Native Word support, full feature set
   - Cons: Windows-focused (though .NET Core is cross-platform)

#### Document Generation Process

1. **Create Document**: Initialize Word document object
2. **Set Properties**: Set document metadata (title, author, etc.)
3. **Process AST**: Iterate through AST nodes
4. **Apply Styles**: Apply Word styles to elements
5. **Embed Media**: Embed images and handle links
6. **Generate File**: Write .docx file

#### Key Implementation Considerations

- **Style Application**: Use Word's style system consistently
- **Media Embedding**: Embed images as binary data in document
- **Link Handling**: Create hyperlink fields, not just formatted text
- **Table Creation**: Use Word table objects, not formatted text
- **Code Blocks**: Use formatted paragraphs or text boxes with styling
- **List Formatting**: Use Word's list formatting system

### Error Handling

- **Missing Images**: Log warning, use placeholder or skip
- **Broken Links**: Preserve link text, mark as broken
- **Malformed Tables**: Attempt to parse, fallback to text
- **Invalid Code Blocks**: Preserve as plain text with formatting
- **Parse Errors**: Report error location, continue with partial conversion

### Performance Considerations

- **Large Documents**: Process in chunks if needed
- **Image Optimization**: Optimize images before embedding
- **Memory Management**: Stream processing for very large documents
- **Caching**: Cache parsed AST and style definitions

### Testing Priorities

1. **All Markdown Elements**: Test each element type
2. **Nested Structures**: Test deeply nested lists and headings
3. **Edge Cases**: Test malformed content, missing resources
4. **Large Documents**: Test with large markdown files
5. **Formatting Preservation**: Verify formatting matches markdown
6. **Word Compatibility**: Test in different Word versions

## Conclusion

This Word conversion specification provides comprehensive mappings from markdown elements to Word document structures. The specification ensures professional document appearance, proper structure preservation, and compatibility with Word's features. Implementation should follow these mappings to create high-quality Word documents from markdown source files.

