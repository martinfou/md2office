# PDF Conversion Specification

## Overview

This specification defines the complete conversion strategy from Microsoft Copilot-generated markdown to PDF format. The conversion preserves document structure, layout, and formatting while creating a professional PDF document with navigation features like bookmarks and table of contents. Note: PDF support is optional based on user requirements, but this specification provides a complete implementation guide.

### Conversion Goals

1. **Layout Preservation**: Maintain document layout and formatting from markdown
2. **Structure Preservation**: Preserve heading hierarchy and document structure
3. **Navigation Features**: Generate bookmarks and optional table of contents
4. **Professional Appearance**: Apply consistent typography and styling
5. **Content Fidelity**: Preserve all content including code, tables, and images

### Conversion Approach

The conversion supports two primary approaches:

1. **Direct PDF Generation**: Generate PDF directly from markdown AST
2. **Indirect PDF Generation**: Generate PDF from Word intermediate format (Word → PDF)

**Recommended Approach**: Direct PDF generation for better control and consistency, with Word→PDF as fallback for complex features.

## Generation Method

### Direct PDF Generation

Generate PDF directly from markdown AST using PDF generation libraries.

**Advantages**:
- Full control over PDF structure and formatting
- No intermediate format conversion artifacts
- Faster processing
- Consistent output

**Technology Options**:
- **JavaScript/TypeScript**: PDFKit, jsPDF, pdfmake
- **Python**: ReportLab, WeasyPrint, pdfkit
- **C#/.NET**: iTextSharp, PdfSharp

### Indirect PDF Generation (Word → PDF)

Generate PDF by first creating Word document, then converting to PDF.

**Advantages**:
- Leverages Word's formatting capabilities
- Better handling of complex layouts
- Consistent with Word output

**Disadvantages**:
- Requires Word or conversion library
- May introduce conversion artifacts
- Slower processing

**Technology Options**:
- **Word → PDF Conversion**: LibreOffice, pandoc, Word automation
- **Library-based**: Use Word generation library, then PDF conversion

### Recommended Implementation

**Primary Method**: Direct PDF generation using PDFKit (JavaScript) or ReportLab (Python)

**Fallback Method**: Word → PDF conversion for complex documents requiring Word-specific features

## Layout Strategy

### Page Layout

#### Page Size

- **US Letter**: 8.5" × 11" (215.9mm × 279.4mm) - Default for US
- **A4**: 210mm × 297mm (8.27" × 11.69") - Default for international
- **Configurable**: Support custom page sizes

#### Margins

- **Top Margin**: 1" (2.54cm)
- **Bottom Margin**: 1" (2.54cm)
- **Left Margin**: 1" (2.54cm)
- **Right Margin**: 1" (2.54cm)
- **Gutter**: 0" (no gutter for single-page layout)

#### Content Area

- **Width**: Page width minus left and right margins
- **Height**: Page height minus top and bottom margins
- **US Letter**: 6.5" × 9" content area
- **A4**: ~6.27" × ~9.69" content area

### Page Structure

#### Header and Footer

**Header** (optional):
- **Content**: Document title or section name
- **Font**: 9pt, regular
- **Alignment**: Center or right
- **Border**: Optional bottom border

**Footer** (optional):
- **Content**: Page number, date, or document info
- **Font**: 9pt, regular
- **Alignment**: Center
- **Format**: "Page X of Y" or just "X"

#### Page Breaks

- **Natural Breaks**: Automatic page breaks when content exceeds page height
- **Section Breaks**: Optional page break before H1 or H2 (configurable)
- **Manual Breaks**: Support horizontal rules as page breaks (configurable)

### Document Structure

#### Document Metadata

Set PDF document properties:

- **Title**: From first H1 or front-matter
- **Author**: From front-matter or default
- **Subject**: From front-matter or extracted from content
- **Keywords**: From front-matter or extracted
- **Creator**: Tool name and version
- **Producer**: PDF library name and version
- **Creation Date**: Current date/time
- **Modification Date**: Current date/time

#### Bookmarks (Navigation)

Generate PDF bookmarks from heading hierarchy:

- **H1**: Level 1 bookmark (top-level)
- **H2**: Level 2 bookmark (under H1)
- **H3**: Level 3 bookmark (under H2)
- **H4-H6**: Level 4-6 bookmarks (nested)

**Bookmark Structure**:
```
Document Title (H1)
├── Section 1 (H2)
│   ├── Subsection 1.1 (H3)
│   └── Subsection 1.2 (H3)
├── Section 2 (H2)
│   └── Subsection 2.1 (H3)
└── Section 3 (H2)
```

#### Table of Contents (Optional)

Generate table of contents page from heading hierarchy:

- **Placement**: After title page or at beginning
- **Format**: List of headings with page numbers
- **Styling**: Consistent with document style
- **Depth**: Configurable (typically H1-H3)

## Element Mappings

### Headers (H1-H6)

Headers map to PDF headings with bookmarks and styling.

| Markdown | PDF Style | Font Family | Font Size | Font Weight | Color | Spacing Before | Spacing After | Bookmark Level |
|----------|-----------|-------------|-----------|-------------|-------|----------------|---------------|---------------|
| H1 (`#`) | Heading 1 | Sans-serif (Helvetica/Arial) | 18pt | Bold | #000000 | 24pt | 12pt | Level 1 |
| H2 (`##`) | Heading 2 | Sans-serif (Helvetica/Arial) | 16pt | Bold | #000000 | 20pt | 8pt | Level 2 |
| H3 (`###`) | Heading 3 | Sans-serif (Helvetica/Arial) | 14pt | Bold | #000000 | 16pt | 6pt | Level 3 |
| H4 (`####`) | Heading 4 | Sans-serif (Helvetica/Arial) | 12pt | Bold | #000000 | 12pt | 4pt | Level 4 |
| H5 (`#####`) | Heading 5 | Sans-serif (Helvetica/Arial) | 11pt | Bold | #000000 | 10pt | 4pt | Level 5 |
| H6 (`######`) | Heading 6 | Sans-serif (Helvetica/Arial) | 10pt | Bold | #000000 | 8pt | 2pt | Level 6 |

#### Header Implementation Details

- **Bookmarks**: All headings generate PDF bookmarks for navigation
- **Page Breaks**: Optional page break before H1 (configurable)
- **Keep Together**: Keep heading with following paragraph (if possible)
- **TOC Entries**: Headings included in table of contents (if generated)

### Paragraphs

Paragraphs are formatted text blocks with consistent spacing.

| Markdown | PDF Style | Font Family | Font Size | Line Spacing | Spacing Before | Spacing After | Alignment |
|----------|-----------|-------------|-----------|--------------|----------------|---------------|-----------|
| Paragraph | Body Text | Serif (Times) or Sans-serif (Helvetica) | 11pt | 1.15 | 0pt | 6pt | Left |

#### Paragraph Implementation Details

- **Font**: Serif (Times, Times New Roman) or Sans-serif (Helvetica, Arial)
- **Line Spacing**: 1.15x (slightly more than single spacing)
- **Spacing**: 6pt after paragraph
- **Alignment**: Left-aligned (default), support center/right/justify if specified
- **Indentation**: No first-line indentation (block style)

### Emphasis and Strong Text

Text emphasis maps to PDF text formatting.

| Markdown | PDF Formatting | Font Style/Weight |
|----------|----------------|-------------------|
| Italic (`*text*` or `_text_`) | Italic | Font style: Italic |
| Bold (`**text**` or `__text__`) | Bold | Font weight: Bold |
| Bold Italic (`***text***`) | Bold + Italic | Font weight: Bold, Font style: Italic |

#### Emphasis Implementation Details

- **Character Formatting**: Apply formatting at character level
- **Font Consistency**: Use same font family as paragraph
- **Preservation**: Preserve emphasis in all contexts

### Lists

Lists are formatted with bullets or numbers and proper indentation.

#### Unordered Lists

| Markdown | PDF Format | Bullet Style | Font Size | Indentation |
|----------|------------|--------------|-----------|-------------|
| `- item` | Bulleted List | Round bullet (•) | 11pt | 0.25" per level |

#### Ordered Lists

| Markdown | PDF Format | Number Format | Font Size | Indentation |
|----------|-----------|---------------|-----------|-------------|
| `1. item` | Numbered List | Arabic numerals (1, 2, 3...) | 11pt | 0.25" per level |

#### Task Lists (GFM)

| Markdown | PDF Format | Checkbox Style | Font Size |
|----------|------------|----------------|-----------|
| `- [ ]` (unchecked) | Bulleted List with Checkbox | ☐ (empty checkbox) | 11pt |
| `- [x]` (checked) | Bulleted List with Checkbox | ☑ (checked checkbox) | 11pt |

#### List Implementation Details

- **Bullet Style**: Round bullet (•) or custom bullet
- **Numbering**: Arabic numerals (1, 2, 3...)
- **Indentation**: 0.25" per nesting level
- **Spacing**: 3pt between list items
- **Font**: Same as body text (11pt)
- **Nesting**: Preserve list nesting with indentation

### Links

Links become clickable PDF hyperlinks.

| Markdown | PDF Element | Display Text | Target URL | Style |
|----------|-------------|--------------|------------|-------|
| `[text](url)` | Hyperlink Annotation | "text" | url | Blue, underlined |
| `[text][ref]` | Hyperlink Annotation | "text" | resolved URL | Blue, underlined |
| `<url>` | Hyperlink Annotation | url | url | Blue, underlined |

#### Link Implementation Details

- **Hyperlink Annotations**: Create PDF hyperlink annotations
- **Display Text**: Show link text, not raw URL (unless autolink)
- **URL Resolution**: Resolve reference links to actual URLs
- **Styling**: Blue color (#0000FF), underlined
- **Clickable**: Links are clickable in PDF viewers
- **External Links**: Mark external links appropriately

### Images

Images are embedded in PDF with proper sizing and positioning.

| Markdown | PDF Element | Placement | Sizing | Alt Text |
|----------|-------------|-----------|--------|----------|
| `![alt](url)` | Embedded Image | Inline with text | Preserve aspect ratio | Preserved in metadata |

#### Image Implementation Details

- **Embedding**: Embed images directly in PDF (not linked)
- **Format Support**: PNG, JPEG, GIF (SVG converted to PNG)
- **Placement**: Inline with text flow
- **Sizing**: 
  - Default width: 6" (or content width)
  - Preserve aspect ratio
  - Scale down if too large
- **Alt Text**: Preserve alt text in image metadata for accessibility
- **Path Resolution**: Resolve relative paths relative to markdown file
- **Missing Images**: Use placeholder or skip with warning

#### Image Positioning

- **Inline**: Images flow with text
- **Block**: Images on their own line (centered or left-aligned)
- **Floating**: Optional floating images (if supported by PDF library)

### Code Blocks

Code blocks are formatted with monospace font and background.

#### Fenced Code Blocks

| Markdown | PDF Element | Font | Background | Border | Padding |
|----------|-------------|------|------------|--------|---------|
| ` ```lang` | Formatted Text Block | Monospace (Courier, 10pt) | Light gray (#F5F5F5) | Optional (1pt solid) | 6pt all sides |

#### Inline Code

| Markdown | PDF Formatting | Font | Background |
|----------|----------------|------|------------|
| `` `code` `` | Character Formatting | Monospace (Courier, 10pt) | Light gray (#F5F5F5) |

#### Code Block Implementation Details

- **Font**: Monospace font (Courier, Courier New, or Consolas)
- **Font Size**: 10pt (slightly smaller than body text)
- **Background**: Light gray (#F5F5F5)
- **Border**: Optional 1pt solid border (#CCCCCC)
- **Padding**: 6pt all sides
- **Formatting Preservation**: 
  - Preserve whitespace and indentation
  - Preserve line breaks
  - Preserve special characters
- **Language Identifier**: Preserve language identifier in comment or metadata
- **Long Code Blocks**: Preserve full content, may span multiple pages

### Tables

Tables are formatted with borders and proper alignment.

| Markdown | PDF Element | Borders | Header Row | Alignment | Styling |
|----------|-------------|---------|------------|-----------|---------|
| Pipe table | PDF Table | Yes (1pt solid) | Bold, shaded | Preserved | Professional |

#### Table Implementation Details

- **Table Structure**: Create PDF table with correct rows/columns
- **Borders**: 1pt solid borders (#000000)
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
- **Page Breaks**: Tables may span multiple pages if large

### Blockquotes

Blockquotes are formatted with indentation and optional styling.

| Markdown | PDF Element | Indentation | Border | Background | Font Style |
|----------|-------------|-------------|--------|------------|------------|
| `> text` | Formatted Text Block | Left: 0.5" | Left border (optional) | Light background (optional) | Italic (optional) |

#### Blockquote Implementation Details

- **Indentation**: Left indent 0.5" from margin
- **Border**: Optional left border (3pt solid #CCCCCC)
- **Background**: Optional light background (#FAFAFA)
- **Font Style**: Optional italic
- **Spacing**: 6pt before and after
- **Nesting**: Support nested blockquotes with increased indentation

### Horizontal Rules

Horizontal rules create visual separators or page breaks.

| Markdown | PDF Element | Style | Placement |
|----------|-------------|-------|-----------|
| `---` | Horizontal Line | 2pt solid #CCCCCC | Between paragraphs |
| `---` (configurable) | Page Break | N/A | Before horizontal rule |

#### Horizontal Rule Implementation Details

- **Default**: Horizontal line (2pt solid #CCCCCC)
- **Width**: Full width of content area
- **Placement**: Between paragraphs
- **Optional**: Page break before horizontal rule (configurable)

### Strikethrough (GFM)

Strikethrough text is formatted with strikethrough style.

| Markdown | PDF Formatting | Font Style |
|----------|----------------|------------|
| `~~text~~` | Strikethrough | Single strikethrough line |

#### Strikethrough Implementation Details

- **Character Formatting**: Apply strikethrough at character level
- **Style**: Single strikethrough line through text
- **Color**: Same as text color (or gray if desired)

## Typography

### Font Specifications

#### Body Text

- **Font Family**: Serif (Times, Times New Roman) or Sans-serif (Helvetica, Arial)
- **Font Size**: 11pt
- **Font Weight**: Regular
- **Line Spacing**: 1.15x (slightly more than single)
- **Color**: #000000 (black)

#### Headings

- **Font Family**: Sans-serif (Helvetica, Arial) - matches modern PDF style
- **Font Sizes**: 
  - H1: 18pt
  - H2: 16pt
  - H3: 14pt
  - H4: 12pt
  - H5: 11pt
  - H6: 10pt
- **Font Weight**: Bold
- **Color**: #000000 (black)

#### Code

- **Font Family**: Monospace (Courier, Courier New, Consolas)
- **Font Size**: 10pt
- **Font Weight**: Regular
- **Background**: #F5F5F5 (light gray)
- **Color**: #000000 (black)

### Font Selection Strategy

**Primary Fonts**:
- **Serif**: Times, Times New Roman (for body text, if serif preferred)
- **Sans-serif**: Helvetica, Arial (for headings and modern look)
- **Monospace**: Courier, Courier New (for code)

**Font Embedding**: Embed fonts in PDF to ensure consistent rendering across platforms

### Typography Rules

1. **Consistency**: Use consistent fonts throughout document
2. **Hierarchy**: Maintain clear font size hierarchy for headings
3. **Readability**: Ensure sufficient contrast and spacing
4. **Line Length**: Optimal line length for readability (~65-75 characters)

## Document Features

### Bookmarks

Generate PDF bookmarks from heading hierarchy:

- **Structure**: Hierarchical bookmark tree matching heading structure
- **Navigation**: Enable easy navigation through document
- **Depth**: Support all heading levels (H1-H6)
- **Styling**: Use default PDF viewer bookmark styling

### Table of Contents

Optional table of contents page:

- **Placement**: After title page or at beginning
- **Format**: List format with page numbers
- **Depth**: Typically H1-H3 (configurable)
- **Styling**: Consistent with document style
- **Page Numbers**: Right-aligned page numbers

### Hyperlinks

- **Internal Links**: Links to headings within document (if supported)
- **External Links**: Links to URLs (clickable)
- **Styling**: Blue color, underlined
- **Functionality**: Clickable in PDF viewers

### Metadata

Set PDF document metadata:

- **Title**: Document title
- **Author**: Author name
- **Subject**: Document subject
- **Keywords**: Keywords for search
- **Creator**: Tool name
- **Producer**: PDF library name

## Implementation Notes

### PDF Generation Libraries

#### JavaScript/TypeScript Options

1. **PDFKit**:
   - Pros: Good control, streaming support
   - Cons: Lower-level API, more code required

2. **jsPDF**:
   - Pros: Simple API, good for basic documents
   - Cons: Limited layout control

3. **pdfmake**:
   - Pros: Good layout control, declarative API
   - Cons: May have limitations

#### Python Options

1. **ReportLab**:
   - Pros: Mature, feature-rich, good control
   - Cons: More complex API

2. **WeasyPrint**:
   - Pros: CSS-based styling, HTML/CSS input
   - Cons: Requires HTML intermediate

3. **pdfkit** (wkhtmltopdf wrapper):
   - Pros: HTML/CSS input, good styling
   - Cons: Requires external binary

### Document Generation Process

1. **Initialize PDF**: Create PDF document object
2. **Set Metadata**: Set document properties
3. **Process AST**: Iterate through AST nodes
4. **Apply Layout**: Apply page layout and margins
5. **Generate Content**: Add text, images, tables, code
6. **Create Bookmarks**: Generate bookmarks from headings
7. **Generate TOC**: Create table of contents (if requested)
8. **Finalize**: Write PDF file

### Key Implementation Considerations

- **Page Breaks**: Handle automatic and manual page breaks
- **Image Embedding**: Embed images as binary data
- **Font Embedding**: Embed fonts for consistent rendering
- **Bookmark Generation**: Create bookmarks from heading hierarchy
- **Table Formatting**: Format tables with borders and alignment
- **Code Formatting**: Format code blocks with monospace font and background

### Error Handling

- **Missing Images**: Log warning, use placeholder or skip
- **Broken Links**: Preserve link text, mark as broken
- **Malformed Tables**: Attempt to parse, fallback to text
- **Long Content**: Handle content that exceeds page height
- **Parse Errors**: Report error location, continue with partial conversion

### Performance Considerations

- **Large Documents**: Handle documents with many pages
- **Image Optimization**: Optimize images before embedding
- **Memory Management**: Stream processing for very large documents
- **Font Embedding**: Consider subsetting fonts to reduce file size

### Testing Priorities

1. **All Elements**: Test each markdown element in PDF
2. **Bookmarks**: Verify bookmark structure and navigation
3. **Page Breaks**: Test page break handling
4. **Images**: Test image embedding and sizing
5. **Tables**: Test table formatting and page breaks
6. **Code Blocks**: Test code block formatting
7. **Large Documents**: Test with large markdown files
8. **Cross-Platform**: Test PDF rendering on different platforms

## Conclusion

This PDF conversion specification provides comprehensive mappings from markdown elements to PDF format. The specification ensures professional document appearance, proper structure preservation, and navigation features like bookmarks and table of contents. Implementation should follow these mappings to create high-quality PDF documents from markdown source files.

