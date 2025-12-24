# Structural Mapping Specification

## Mapping Overview

This document defines the detailed structural mappings from Microsoft Copilot markdown elements to Word (.docx), PowerPoint (.pptx), and PDF document structures. These mappings serve as the foundation for format-specific conversion implementations, ensuring consistent interpretation of markdown content across all output formats.

The mappings preserve document hierarchy, formatting, and content while adapting to format-specific conventions and capabilities. Each markdown element has corresponding representations in all three output formats, with format-specific considerations documented.

## Mapping Principles

### Core Principles

1. **Hierarchy Preservation**: Maintain markdown heading hierarchy in all formats
2. **Content Fidelity**: Preserve all content and meaning from source markdown
3. **Format Adaptation**: Adapt structure to format conventions while maintaining semantics
4. **Consistency**: Ensure consistent interpretation across formats
5. **Graceful Handling**: Handle edge cases and missing content gracefully

### Mapping Strategy

- **Direct Mapping**: One-to-one correspondence where possible (e.g., headings to heading styles)
- **Structural Mapping**: Adapt structure to format conventions (e.g., headings to slides)
- **Content Mapping**: Preserve content while adapting presentation (e.g., lists to bullet points)
- **Enhancement**: Add format-specific features that enhance usability (e.g., bookmarks, TOC)

## Element Mappings

### Headers (H1-H6)

Headers are fundamental structural elements that define document hierarchy. They map differently across formats based on format conventions.

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| H1 (`#`) | Heading 1 style<br>Title page (optional)<br>Major section break | Title slide<br>Section divider slide | H1 bookmark<br>Chapter/section marker<br>TOC entry level 1 |
| H2 (`##`) | Heading 2 style<br>Section break (optional) | Slide title<br>New slide | H2 bookmark<br>TOC entry level 2 |
| H3 (`###`) | Heading 3 style | Slide subtitle<br>Content section header | H3 bookmark<br>TOC entry level 3 |
| H4 (`####`) | Heading 4 style | Slide content subsection | H4 bookmark<br>TOC entry level 4 |
| H5 (`#####`) | Heading 5 style | Slide content detail | H5 bookmark<br>TOC entry level 5 |
| H6 (`######`) | Heading 6 style | Slide content detail | H6 bookmark<br>TOC entry level 6 |

#### Word Mapping Details

- **Style Application**: Apply Word built-in heading styles (Heading 1-6)
- **Page Breaks**: Optional page break before H1 or H2 (configurable)
- **Table of Contents**: Headings automatically included in TOC generation
- **Navigation Pane**: Headings appear in Word navigation pane
- **Cross-References**: Headings can be referenced for cross-references

#### PowerPoint Mapping Details

- **Slide Structure**: 
  - H1 → Title slide or section divider
  - H2 → New slide with title
  - H3+ → Content sections within slide
- **Layout Selection**: 
  - Title slide layout for H1
  - Title and Content layout for H2 slides
  - Content layouts for nested headings
- **Content Grouping**: Content between H2 headings becomes slide content

#### PDF Mapping Details

- **Bookmarks**: All headings generate PDF bookmarks
- **Table of Contents**: Headings used for TOC generation
- **Navigation**: Bookmarks enable PDF navigation
- **Styling**: Headings styled with appropriate font sizes and weights

### Paragraphs

Paragraphs are the basic content containers in markdown.

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Paragraph (blank line separated) | Normal paragraph style<br>Text with formatting | Slide content text<br>Body text placeholder | Paragraph text<br>Formatted text block |

#### Mapping Details

- **Word**: Normal style paragraphs with preserved formatting
- **PowerPoint**: Text in content placeholders, may be split across slides if long
- **PDF**: Formatted text paragraphs with consistent spacing

### Emphasis and Strong Text

Text emphasis provides visual hierarchy and emphasis.

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Italic (`*text*` or `_text_`) | Italic formatting | Italic text formatting | Italic font style |
| Bold (`**text**` or `__text__`) | Bold formatting | Bold text formatting | Bold font weight |
| Bold Italic (`***text***`) | Bold + Italic formatting | Bold + Italic formatting | Bold + Italic font |

#### Mapping Details

- **Word**: Character-level formatting (bold, italic)
- **PowerPoint**: Character-level formatting in text boxes
- **PDF**: Font style/weight applied to text

### Lists

Lists are common structural elements that require careful mapping to preserve hierarchy and formatting.

#### Unordered Lists

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Unordered list (`-`, `*`, `+`) | Bulleted list<br>Word list formatting<br>Preserve nesting | Bullet points<br>Slide bullet list<br>Preserve nesting | Bulleted list<br>Formatted bullets<br>Preserve nesting |

#### Ordered Lists

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Ordered list (`1.`, `2.`, etc.) | Numbered list<br>Word numbering<br>Preserve sequence | Numbered list<br>Slide numbered list<br>Preserve sequence | Numbered list<br>Formatted numbers<br>Preserve sequence |

#### Task Lists (GFM)

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Task list (`- [ ]`, `- [x]`) | Checkbox list<br>Word checkbox control<br>Preserve checked state | Bullet list with checkmarks<br>Symbol bullets (✓/☐)<br>Preserve checked state | Formatted list with checkmarks<br>Unicode symbols<br>Preserve checked state |

#### List Nesting

- **Word**: Nested lists use Word's list formatting with indentation
- **PowerPoint**: Nested lists use indented bullet/number formatting
- **PDF**: Nested lists maintain indentation and formatting

### Links

Links connect content and provide navigation.

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Inline link (`[text](url)`) | Hyperlink field<br>Clickable link<br>Preserve URL | Hyperlink<br>Clickable link<br>Preserve URL | Hyperlink annotation<br>Clickable link<br>Preserve URL |
| Reference link (`[text][ref]`) | Hyperlink (resolved)<br>Clickable link | Hyperlink (resolved)<br>Clickable link | Hyperlink (resolved)<br>Clickable link |
| Autolink (`<url>`) | Hyperlink<br>Auto-detected URL | Hyperlink<br>Auto-detected URL | Hyperlink<br>Auto-detected URL |

#### Mapping Details

- **Word**: Hyperlink fields with display text and target URL
- **PowerPoint**: Hyperlinks in text with clickable targets
- **PDF**: Link annotations with clickable areas

### Images

Images enhance visual content and require path resolution and embedding.

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Image (`![alt](url)`) | Inline image<br>Embedded image<br>Alt text preserved | Image on slide<br>Embedded image<br>Alt text preserved | Embedded image<br>Image object<br>Alt text preserved |

#### Mapping Details

- **Word**: 
  - Inline images embedded in document
  - Alt text stored in image properties
  - Image sizing and positioning preserved
- **PowerPoint**: 
  - Images placed on slides
  - Alt text for accessibility
  - Image sizing and positioning
- **PDF**: 
  - Images embedded in PDF
  - Alt text for accessibility
  - Image positioning and sizing

#### Image Path Resolution

- Resolve relative paths relative to markdown file location
- Support absolute paths
- Handle missing images gracefully (placeholder or skip)
- Optimize images during embedding (optional)

### Code Blocks

Code blocks preserve formatting and syntax information.

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Fenced code block (```lang) | Formatted code block<br>Monospace font<br>Background color<br>Language preserved | Code block on slide<br>Monospace font<br>Background color<br>May be truncated | Formatted code block<br>Monospace font<br>Background color<br>Language preserved |
| Inline code (`` `code` ``) | Inline code formatting<br>Monospace font<br>Background color | Inline code formatting<br>Monospace font | Inline code formatting<br>Monospace font |

#### Mapping Details

- **Word**: 
  - Code blocks in formatted text boxes or paragraphs
  - Monospace font (Courier New, Consolas, etc.)
  - Background color (light gray)
  - Language identifier preserved in comment or metadata
- **PowerPoint**: 
  - Code blocks in text boxes with formatting
  - May need truncation for very long code
  - Monospace font and background
- **PDF**: 
  - Formatted code blocks with monospace font
  - Background color for readability
  - Language information preserved

### Tables

Tables organize structured data and require careful formatting preservation.

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Table (pipe-delimited) | Word table<br>Preserve alignment<br>Header row formatting | PowerPoint table<br>Preserve alignment<br>Header row formatting | PDF table<br>Preserve alignment<br>Header row formatting |

#### Mapping Details

- **Word**: 
  - Native Word table object
  - Column alignment preserved (left, center, right)
  - Header row with bold formatting
  - Table styling applied
- **PowerPoint**: 
  - PowerPoint table object on slide
  - Column alignment preserved
  - Header row formatting
  - Table styling consistent with slide theme
- **PDF**: 
  - Formatted table with borders
  - Column alignment preserved
  - Header row styling
  - Table layout preserved

#### Table Alignment Mapping

- `:---` (left) → Left alignment
- `:---:` (center) → Center alignment
- `---:` (right) → Right alignment
- `---` (default) → Left alignment

### Blockquotes

Blockquotes emphasize quoted or important content.

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Blockquote (`> text`) | Formatted quote<br>Indentation<br>Border/background (optional) | Text box with quote styling<br>Indentation<br>Visual distinction | Formatted quote block<br>Indentation<br>Border/background |

#### Mapping Details

- **Word**: 
  - Indented paragraph with quote style
  - Optional left border or background color
  - Preserve nested blockquotes
- **PowerPoint**: 
  - Text box with quote formatting
  - Indentation and visual styling
  - May be on dedicated slide for emphasis
- **PDF**: 
  - Formatted quote block with indentation
  - Optional border or background
  - Preserve formatting

### Horizontal Rules

Horizontal rules provide visual separation.

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Horizontal rule (`---`) | Horizontal line<br>Page break (optional)<br>Section break (optional) | Slide separator<br>New slide (optional) | Horizontal line<br>Page break (optional) |

#### Mapping Details

- **Word**: 
  - Horizontal line shape or border
  - Optional page break before/after
  - Optional section break
- **PowerPoint**: 
  - Visual separator on slide
  - May trigger new slide (configurable)
- **PDF**: 
  - Horizontal line
  - Optional page break

### Strikethrough (GFM)

Strikethrough indicates deleted or deprecated content.

| Markdown | Word (.docx) | PowerPoint (.pptx) | PDF |
|----------|--------------|-------------------|-----|
| Strikethrough (`~~text~~`) | Strikethrough formatting | Strikethrough text | Strikethrough font style |

#### Mapping Details

- **Word**: Character-level strikethrough formatting
- **PowerPoint**: Text strikethrough formatting
- **PDF**: Strikethrough font style applied

## Structure Preservation Rules

### Document Hierarchy

#### Hierarchy Preservation

1. **Heading Levels**: Maintain relative heading levels across formats
   - H1 > H2 > H3 hierarchy preserved
   - Don't skip heading levels
   - Maintain logical nesting

2. **Content Grouping**: Content belongs to nearest parent heading
   - Paragraphs, lists, code blocks belong to preceding heading
   - Content hierarchy follows markdown structure

3. **Section Boundaries**: Major sections defined by H1 or H2
   - H1 typically starts new major section
   - H2 starts new subsection
   - Section boundaries affect format-specific structure (slides, pages)

### Format-Specific Structure Adaptation

#### Word Structure

- **Linear Flow**: Content flows sequentially from top to bottom
- **Section Breaks**: Optional section breaks at H1/H2 boundaries
- **Page Breaks**: Optional page breaks for major sections
- **Table of Contents**: Generated from heading hierarchy
- **Navigation**: Headings appear in navigation pane

#### PowerPoint Structure

- **Slide Hierarchy**: 
  - H1 → Title slide or section divider
  - H2 → Slide titles
  - H3+ → Slide content sections
- **Content Distribution**: 
  - Content under H2 becomes slide content
  - Long content may split across multiple slides
  - Lists become bullet points
- **Slide Layouts**: 
  - Title slide for H1
  - Title and Content for H2 slides
  - Content layouts for nested content

#### PDF Structure

- **Document Flow**: Linear document structure like Word
- **Bookmarks**: Generated from heading hierarchy
- **Table of Contents**: Optional TOC page from headings
- **Page Breaks**: Natural page breaks, optional at sections
- **Navigation**: Bookmarks enable PDF navigation

## Format-Specific Considerations

### Word (.docx) Considerations

#### Document Structure

- Use Word built-in styles (Heading 1-6, Normal, List styles)
- Support Word-specific features:
  - Table of Contents (auto-generated)
  - Cross-references
  - Footnotes/endnotes (if needed)
  - Document properties (title, author, etc.)

#### Styling

- Apply consistent paragraph and character styles
- Use Word theme colors and fonts
- Support custom style sheets
- Preserve formatting from markdown (bold, italic, etc.)

#### Media Handling

- Embed images inline with text
- Support image sizing and positioning
- Preserve image alt text
- Handle image formats (PNG, JPEG, GIF, SVG)

#### Advanced Features

- Page breaks at section boundaries (optional)
- Section breaks for different page layouts (optional)
- Headers and footers (optional)
- Page numbering (optional)

### PowerPoint (.pptx) Considerations

#### Slide Structure

- Determine slide boundaries from heading hierarchy
- Select appropriate slide layouts based on content
- Handle content overflow (split across slides or truncate)
- Create title slide from document title (H1)

#### Content Adaptation

- Convert lists to bullet points
- Adapt paragraphs to slide text
- Handle code blocks (may need truncation)
- Position images appropriately on slides

#### Visual Design

- Apply consistent slide theme
- Use slide master for consistent styling
- Maintain visual hierarchy
- Support slide transitions (optional)

#### Content Splitting

- Long sections may need multiple slides
- Code blocks may need truncation or scrolling
- Tables may need simplification for slides
- Images sized appropriately for slide dimensions

### PDF Considerations

#### Document Structure

- Generate bookmarks from heading hierarchy
- Create table of contents (optional)
- Maintain document flow and pagination
- Support hyperlinks and navigation

#### Formatting Preservation

- Preserve text formatting (bold, italic, etc.)
- Maintain code block formatting
- Preserve table structure and alignment
- Handle image embedding and positioning

#### Layout

- Page size and margins (configurable)
- Page breaks at appropriate points
- Header and footer (optional)
- Page numbering (optional)

#### Accessibility

- Preserve alt text for images
- Generate bookmarks for navigation
- Support screen readers
- Maintain document structure

## Conversion Rules Table

### Comprehensive Mapping Reference

| Markdown Element | Syntax | Word Mapping | PowerPoint Mapping | PDF Mapping | Notes |
|-----------------|--------|--------------|-------------------|-------------|-------|
| H1 | `# Title` | Heading 1 style<br>Optional page break | Title slide<br>Section divider | H1 bookmark<br>TOC level 1 | Document title |
| H2 | `## Section` | Heading 2 style<br>Optional section break | Slide title<br>New slide | H2 bookmark<br>TOC level 2 | Major section |
| H3 | `### Subsection` | Heading 3 style | Slide subtitle<br>Content header | H3 bookmark<br>TOC level 3 | Subsection |
| H4 | `#### Detail` | Heading 4 style | Slide content subsection | H4 bookmark<br>TOC level 4 | Detail level |
| H5 | `##### Item` | Heading 5 style | Slide content detail | H5 bookmark<br>TOC level 5 | Rare |
| H6 | `###### Point` | Heading 6 style | Slide content detail | H6 bookmark<br>TOC level 6 | Very rare |
| Paragraph | Blank line separated | Normal paragraph | Slide text content | Paragraph text | Basic content |
| Bold | `**text**` | Bold formatting | Bold text | Bold font | Emphasis |
| Italic | `*text*` | Italic formatting | Italic text | Italic font | Emphasis |
| Bold Italic | `***text***` | Bold + Italic | Bold + Italic | Bold + Italic | Combined |
| Unordered List | `- item` | Bulleted list | Bullet points | Bulleted list | Common |
| Ordered List | `1. item` | Numbered list | Numbered list | Numbered list | Sequential |
| Task List | `- [ ]` / `- [x]` | Checkbox list | Checkmark bullets | Checkmark list | GFM |
| Inline Link | `[text](url)` | Hyperlink | Hyperlink | Link annotation | Navigation |
| Reference Link | `[text][ref]` | Hyperlink (resolved) | Hyperlink (resolved) | Link (resolved) | Reusable |
| Image | `![alt](url)` | Embedded image | Slide image | Embedded image | Visual |
| Inline Code | `` `code` `` | Monospace format | Monospace format | Monospace font | Code |
| Code Block | ` ```lang` | Formatted block | Formatted block | Formatted block | Code |
| Table | `\| col \|` | Word table | PowerPoint table | PDF table | Data |
| Blockquote | `> text` | Quote style | Quote text box | Quote block | Quote |
| Horizontal Rule | `---` | Horizontal line | Slide separator | Horizontal line | Separator |
| Strikethrough | `~~text~~` | Strikethrough | Strikethrough | Strikethrough | GFM |

## Edge Case Handling

### Missing or Malformed Content

- **Missing Images**: Use placeholder or skip with warning
- **Broken Links**: Preserve link text, mark as broken
- **Malformed Tables**: Attempt to parse, fallback to text
- **Invalid Code Blocks**: Preserve as plain text

### Content Overflow

- **Long Code Blocks**: 
  - Word: Full content preserved
  - PowerPoint: May truncate or use scrolling text box
  - PDF: Full content preserved
- **Wide Tables**: 
  - Word: Auto-fit or horizontal scroll
  - PowerPoint: May need simplification
  - PDF: Page width constraints
- **Long Paragraphs**: 
  - Word: Natural wrapping
  - PowerPoint: May split across slides
  - PDF: Natural wrapping

### Special Characters

- Preserve special characters in content
- Handle Unicode characters correctly
- Escape special characters in code blocks
- Preserve markdown syntax in code blocks

## Implementation Notes

### Mapping Implementation

1. **Parse Markdown**: Generate AST with all elements
2. **Analyze Structure**: Identify hierarchy and relationships
3. **Apply Mappings**: Transform AST nodes according to mappings
4. **Generate Output**: Create format-specific documents

### Format-Specific Transformations

- **Word**: Apply Word styles and formatting
- **PowerPoint**: Structure content into slides
- **PDF**: Generate PDF with bookmarks and formatting

### Testing Priorities

- Test all markdown elements in each format
- Verify hierarchy preservation
- Test edge cases and malformed content
- Validate format-specific features

## Conclusion

This structural mapping specification provides comprehensive mappings from markdown elements to Word, PowerPoint, and PDF formats. The mappings preserve document structure, content, and formatting while adapting to format-specific conventions. These mappings serve as the foundation for format-specific conversion implementations, ensuring consistent and accurate conversion across all output formats.

