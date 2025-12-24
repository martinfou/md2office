# Formatting Specification

## Overview

This specification defines detailed formatting rules and consistency guidelines for converting Microsoft Copilot-generated markdown to Word, PowerPoint, and PDF formats. The rules ensure consistent formatting, professional appearance, and proper handling of all markdown elements across all output formats.

### Formatting Principles

1. **Consistency**: Apply formatting rules consistently across all formats
2. **Preservation**: Preserve markdown structure and content faithfully
3. **Adaptation**: Adapt formatting to format-specific capabilities while maintaining consistency
4. **Quality**: Ensure professional, polished output
5. **Accessibility**: Maintain accessibility through proper formatting

## General Formatting Rules

### Document Structure

#### Heading Hierarchy

- **Maintain Hierarchy**: Preserve markdown heading hierarchy (H1 > H2 > H3, etc.)
- **No Level Skipping**: Don't skip heading levels (e.g., H1 followed by H3)
- **Consistent Styling**: Apply consistent heading styles across formats
- **Spacing**: Apply consistent spacing before and after headings

#### Content Organization

- **Sequential Flow**: Maintain content order from markdown
- **Grouping**: Group content under appropriate headings
- **Section Boundaries**: Use heading levels to define section boundaries
- **Page/Slide Breaks**: Insert breaks at major sections (configurable)

### Text Formatting

#### Paragraph Formatting

- **Font**: Use unified font family (Segoe UI/Arial/Helvetica)
- **Size**: 11pt for body text (18pt for PowerPoint slides)
- **Line Spacing**: 1.15x for body text
- **Alignment**: Left-aligned (default), support center/right/justify
- **Spacing**: 6pt after paragraphs

#### Emphasis Formatting

- **Bold**: Font weight 700 (Bold)
- **Italic**: Font style Italic
- **Bold Italic**: Font weight 700 + Font style Italic
- **Strikethrough**: Single strikethrough line
- **Preservation**: Preserve emphasis in all contexts (paragraphs, lists, tables)

### Spacing Rules

#### Vertical Spacing

| Element | Spacing Before | Spacing After |
|---------|----------------|---------------|
| H1 | 24pt | 12pt |
| H2 | 20pt | 8pt |
| H3 | 16pt | 6pt |
| H4 | 12pt | 4pt |
| H5 | 10pt | 4pt |
| H6 | 8pt | 2pt |
| Paragraph | 0pt | 6pt |
| List | 0pt | 6pt |
| Code Block | 6pt | 6pt |
| Blockquote | 6pt | 6pt |
| Table | 6pt | 6pt |
| Image | 6pt | 6pt |

#### Horizontal Spacing

- **Indentation**: 0.25" per list nesting level
- **Blockquote Indent**: 0.5" left indent
- **Code Block Padding**: 6pt all sides
- **Table Cell Padding**: 6pt all sides

## Element-Specific Formatting Rules

### Headers

#### Formatting Rules

1. **Style Application**: Apply appropriate heading style (Heading 1-6)
2. **Font Weight**: Bold for all headings
3. **Font Size**: Follow unified font size scale (18pt H1, 16pt H2, etc.)
4. **Color**: Primary Blue (#0078D4) for H1-H2, Primary Text (#323130) for H3-H6
5. **Spacing**: Apply consistent spacing before and after
6. **Keep Together**: Keep heading with following paragraph (where possible)

#### Format-Specific Rules

**Word**:
- Use built-in Heading 1-6 styles
- Enable "Keep with next" for H1-H3
- Optional page break before H1

**PowerPoint**:
- H1 → Title slide (44pt)
- H2 → Slide title (32pt)
- H3+ → Content headers (24pt, 20pt, etc.)

**PDF**:
- Generate bookmarks from all headings
- Apply unified font sizes
- Optional page break before H1

### Paragraphs

#### Formatting Rules

1. **Font**: Unified font family, 11pt (18pt for PowerPoint)
2. **Line Spacing**: 1.15x for body text
3. **Alignment**: Left-aligned (default)
4. **Spacing**: 6pt after paragraph
5. **Indentation**: No first-line indentation (block style)

#### Format-Specific Rules

**Word**:
- Use Normal style
- Apply unified font and spacing
- Support center/right/justify alignment

**PowerPoint**:
- Use slide body text style (18pt)
- May be converted to bullet points if appropriate
- Support text wrapping

**PDF**:
- Apply unified typography
- Support multiple alignment options
- Preserve line breaks

### Lists

#### Unordered Lists

**Formatting Rules**:
1. **Bullet Style**: Round bullet (•)
2. **Indentation**: 0.25" per nesting level
3. **Font**: Same as body text (11pt)
4. **Spacing**: 3pt between items
5. **Nesting**: Preserve nesting with indentation

**Format-Specific Rules**:

**Word**:
- Use Word bulleted list formatting
- Apply consistent indentation
- Support nested lists

**PowerPoint**:
- Use slide bullet points
- Larger font (18pt) for readability
- Preserve nesting

**PDF**:
- Format as bulleted list
- Apply unified indentation
- Preserve nesting

#### Ordered Lists

**Formatting Rules**:
1. **Number Format**: Arabic numerals (1, 2, 3...)
2. **Indentation**: 0.25" per nesting level
3. **Font**: Same as body text (11pt)
4. **Spacing**: 3pt between items
5. **Continuation**: Continue numbering across list breaks (Word)

**Format-Specific Rules**:

**Word**:
- Use Word numbered list formatting
- Continue numbering automatically
- Apply consistent indentation

**PowerPoint**:
- Use slide numbered list
- Larger font (18pt) for readability
- Preserve numbering

**PDF**:
- Format as numbered list
- Apply unified indentation
- Preserve numbering

#### Task Lists

**Formatting Rules**:
1. **Checkbox Style**: ☐ (unchecked), ☑ (checked)
2. **Indentation**: 0.25" per nesting level
3. **Font**: Same as body text (11pt)
4. **Spacing**: 3pt between items
5. **State Preservation**: Preserve checked/unchecked state

**Format-Specific Rules**:

**Word**:
- Use checkbox symbols or content controls
- Preserve checked state
- Apply consistent formatting

**PowerPoint**:
- Use checkbox symbols
- Larger font (18pt) for readability
- Preserve checked state

**PDF**:
- Use checkbox symbols
- Preserve checked state
- Apply unified formatting

### Code Blocks

#### Fenced Code Blocks

**Formatting Rules**:
1. **Font**: Monospace (Consolas/Menlo/Courier New), 10pt
2. **Background**: #F5F5F5 (light gray)
3. **Border**: Optional 1pt solid #CCCCCC
4. **Padding**: 6pt all sides
5. **Line Spacing**: 1.0x (single spacing)
6. **Preservation**: Preserve whitespace, indentation, line breaks

**Format-Specific Rules**:

**Word**:
- Formatted paragraph or text box
- Monospace font with background
- Preserve full content

**PowerPoint**:
- Text box with formatting
- May truncate if very long
- Split across slides if necessary

**PDF**:
- Formatted text block
- Monospace font with background
- Preserve full content

#### Inline Code

**Formatting Rules**:
1. **Font**: Monospace (Consolas/Menlo/Courier New), 10pt
2. **Background**: #F5F5F5 (light gray)
3. **No Border**: Character-level formatting only
4. **No Padding**: Inline with text

**Format-Specific Rules**:

**Word**:
- Character-level formatting
- Monospace font with background
- Preserve in all contexts

**PowerPoint**:
- Character-level formatting
- Monospace font with background
- Preserve in all contexts

**PDF**:
- Character-level formatting
- Monospace font with background
- Preserve in all contexts

### Tables

#### Formatting Rules

1. **Borders**: 1pt solid #000000 (black)
2. **Header Row**: Bold font, #F2F2F2 background
3. **Cell Padding**: 6pt all sides
4. **Alignment**: Preserve markdown alignment (left/center/right)
5. **Row Height**: Auto-height based on content
6. **Column Width**: Auto-fit or equal width

#### Format-Specific Rules

**Word**:
- Word table object
- Apply unified borders and styling
- Support page breaks for large tables

**PowerPoint**:
- PowerPoint table object
- Fit to slide width
- May simplify for large tables

**PDF**:
- PDF table structure
- Apply unified borders and styling
- Support page breaks for large tables

### Images

#### Formatting Rules

1. **Embedding**: Embed images directly (not linked)
2. **Sizing**: Preserve aspect ratio, scale to fit
3. **Placement**: Inline with text flow
4. **Alignment**: Left-aligned (default), center/right if specified
5. **Alt Text**: Preserve alt text for accessibility
6. **Border**: No border (default), optional border for emphasis

#### Format-Specific Rules

**Word**:
- Inline image embedding
- Default width: 6.5" (or page width minus margins)
- Preserve alt text in image properties

**PowerPoint**:
- Slide image embedding
- Default width: 9.5" (fit to slide)
- Preserve alt text

**PDF**:
- Embedded image object
- Default width: 6" (or content width)
- Preserve alt text in metadata

### Links

#### Formatting Rules

1. **Display Text**: Show link text, not raw URL (unless autolink)
2. **URL Resolution**: Resolve reference links to actual URLs
3. **Styling**: Blue color (#0078D4), underlined
4. **Clickability**: Make links clickable in all formats
5. **Preservation**: Preserve links in all contexts

#### Format-Specific Rules

**Word**:
- Hyperlink fields (not just formatted text)
- Blue color, underlined
- Clickable in Word

**PowerPoint**:
- Hyperlinks in text
- Blue color, underlined
- Clickable in PowerPoint

**PDF**:
- Hyperlink annotations
- Blue color, underlined
- Clickable in PDF viewers

### Blockquotes

#### Formatting Rules

1. **Indentation**: 0.5" left indent
2. **Border**: Optional 3pt solid #CCCCCC left border
3. **Background**: Optional #FAFAFA light background
4. **Font Style**: Optional italic
5. **Spacing**: 6pt before and after
6. **Nesting**: Support nested blockquotes with increased indentation

#### Format-Specific Rules

**Word**:
- Formatted paragraph with indentation
- Optional left border and background
- Preserve nesting

**PowerPoint**:
- Text box with indentation
- Optional styling
- May be on dedicated slide

**PDF**:
- Formatted text block with indentation
- Optional border and background
- Preserve nesting

### Horizontal Rules

#### Formatting Rules

1. **Style**: 2pt solid #CCCCCC line
2. **Width**: Full width of content area
3. **Placement**: Between paragraphs
4. **Page Breaks**: Optional page break before (configurable)

#### Format-Specific Rules

**Word**:
- Horizontal line shape
- Optional page break before

**PowerPoint**:
- Visual separator or new slide trigger
- Full-width line

**PDF**:
- Horizontal line
- Optional page break before

## Consistency Guidelines

### Cross-Format Consistency

1. **Color Scheme**: Apply unified color scheme consistently
2. **Typography**: Maintain consistent font families and sizes (scaled appropriately)
3. **Spacing**: Apply consistent spacing rules
4. **Element Styling**: Apply consistent styling to all elements
5. **Hierarchy**: Maintain consistent visual hierarchy

### Format-Specific Adaptations

1. **Word**: Leverage Word's style system while maintaining unified appearance
2. **PowerPoint**: Scale fonts and spacing for presentation while maintaining visual identity
3. **PDF**: Apply unified styling directly with font embedding

### Quality Standards

1. **Readability**: Ensure sufficient contrast and readable fonts
2. **Professionalism**: Maintain professional appearance
3. **Consistency**: Apply formatting consistently throughout
4. **Accessibility**: Ensure accessibility through proper formatting

## Edge Cases and Special Situations

### Long Content

#### Long Code Blocks

- **Word**: Preserve full content
- **PowerPoint**: Truncate or split across slides
- **PDF**: Preserve full content, may span pages

#### Long Tables

- **Word**: Support page breaks, repeat header row
- **PowerPoint**: Simplify or split across slides
- **PDF**: Support page breaks, repeat header row

#### Long Lists

- **Word**: Continue list formatting
- **PowerPoint**: Split across slides if needed
- **PDF**: Continue list formatting

### Missing or Broken Content

#### Missing Images

- **Action**: Log warning, use placeholder or skip
- **Placeholder**: Use text placeholder "[Image: alt text]"
- **Consistency**: Handle consistently across formats

#### Broken Links

- **Action**: Preserve link text, mark as broken
- **Display**: Show link text with warning indicator (optional)
- **Consistency**: Handle consistently across formats

#### Malformed Tables

- **Action**: Attempt to parse, fallback to text
- **Fallback**: Display as formatted text
- **Consistency**: Handle consistently across formats

### Special Characters

#### Unicode Characters

- **Preservation**: Preserve all Unicode characters
- **Font Support**: Ensure font supports required characters
- **Fallback**: Use fallback fonts if needed

#### Special Markdown Syntax

- **Code Blocks**: Preserve markdown syntax in code blocks
- **Escaped Characters**: Handle escaped characters correctly
- **HTML Entities**: Convert HTML entities to characters

## Formatting Quality Checklist

### Document-Level Checks

- [ ] Consistent heading hierarchy
- [ ] Consistent spacing throughout
- [ ] Consistent font usage
- [ ] Consistent color scheme
- [ ] Proper page/slide breaks

### Element-Level Checks

- [ ] Headings properly styled
- [ ] Lists properly formatted with indentation
- [ ] Code blocks with correct font and background
- [ ] Tables with borders and header styling
- [ ] Images properly sized and embedded
- [ ] Links clickable and properly styled
- [ ] Blockquotes with proper indentation

### Format-Specific Checks

**Word**:
- [ ] Styles applied correctly
- [ ] Navigation pane shows headings
- [ ] Table of contents works (if generated)
- [ ] Images embedded correctly

**PowerPoint**:
- [ ] Slide structure logical
- [ ] Fonts readable on slides
- [ ] Content fits on slides
- [ ] Images sized appropriately

**PDF**:
- [ ] Bookmarks generated correctly
- [ ] Fonts embedded
- [ ] Links clickable
- [ ] Table of contents works (if generated)

## Conclusion

This formatting specification provides comprehensive rules for consistent formatting across Word, PowerPoint, and PDF formats. By following these rules, the conversion tool will produce documents with professional appearance, consistent styling, and proper handling of all markdown elements.

