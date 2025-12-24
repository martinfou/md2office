# Styling Guide

## Overview

This guide defines the unified styling system that ensures consistent visual design and professional appearance across Word, PowerPoint, and PDF output formats. The styling system provides a cohesive visual identity while respecting format-specific capabilities and constraints.

### Styling Philosophy

1. **Consistency**: Maintain visual consistency across all output formats
2. **Professionalism**: Ensure professional, business-appropriate appearance
3. **Readability**: Prioritize readability and accessibility
4. **Adaptability**: Adapt styles to format-specific capabilities while maintaining core identity
5. **Clarity**: Use clear visual hierarchy and spacing

### Design Principles

- **Clean and Modern**: Clean design with modern typography and spacing
- **Accessible**: Sufficient contrast and readable fonts
- **Hierarchical**: Clear visual hierarchy through typography and spacing
- **Consistent**: Consistent application of styles across formats
- **Professional**: Business-appropriate color scheme and styling

## Color Scheme

### Primary Colors

The color scheme uses Microsoft-inspired colors for professional appearance:

| Color | Hex Code | RGB | Usage |
|-------|----------|-----|-------|
| Primary Blue | #0078D4 | RGB(0, 120, 212) | Headings, links, accents |
| Secondary Blue | #00BCF2 | RGB(0, 188, 242) | Secondary accents, highlights |
| Accent Green | #107C10 | RGB(16, 124, 16) | Success indicators, positive emphasis |
| Accent Orange | #FF8C00 | RGB(255, 140, 0) | Warnings, attention (optional) |

### Text Colors

| Color | Hex Code | RGB | Usage |
|-------|----------|-----|-------|
| Primary Text | #323130 | RGB(50, 49, 48) | Body text, headings |
| Secondary Text | #605E5C | RGB(96, 94, 92) | Subtitles, captions |
| Tertiary Text | #8A8886 | RGB(138, 136, 134) | Metadata, less important text |
| Link Color | #0078D4 | RGB(0, 120, 212) | Hyperlinks |
| Link Hover | #106EBE | RGB(16, 110, 190) | Link hover state (where applicable) |

### Background Colors

| Color | Hex Code | RGB | Usage |
|-------|----------|-----|-------|
| Document Background | #FFFFFF | RGB(255, 255, 255) | Main document background |
| Code Block Background | #F5F5F5 | RGB(245, 245, 245) | Code block backgrounds |
| Table Header Background | #F2F2F2 | RGB(242, 242, 242) | Table header rows |
| Blockquote Background | #FAFAFA | RGB(250, 250, 250) | Blockquote backgrounds (optional) |
| Border Color | #CCCCCC | RGB(204, 204, 204) | Borders, dividers |

### Color Application Rules

1. **Primary Blue**: Use for headings (H1-H2), links, and key accents
2. **Primary Text**: Use for all body text and most headings
3. **Backgrounds**: Keep backgrounds light and neutral for readability
4. **Contrast**: Ensure sufficient contrast (minimum 4.5:1 for body text)
5. **Consistency**: Apply colors consistently across formats

## Typography

### Font Families

#### Body Text Fonts

**Primary Font Stack**:
- **Windows**: Segoe UI
- **Mac**: San Francisco (SF Pro Text)
- **Linux**: Ubuntu, Roboto
- **Fallback**: Arial, Helvetica, sans-serif

**Rationale**: Modern, readable sans-serif fonts that are widely available and professional.

#### Heading Fonts

**Primary Font Stack**:
- **Windows**: Segoe UI Semibold/Bold
- **Mac**: San Francisco Semibold/Bold (SF Pro Display)
- **Linux**: Ubuntu Medium/Bold, Roboto Medium/Bold
- **Fallback**: Arial Bold, Helvetica Bold, sans-serif

**Rationale**: Same font family as body text but with increased weight for hierarchy.

#### Code Fonts

**Primary Font Stack**:
- **Windows**: Consolas
- **Mac**: Menlo
- **Linux**: Ubuntu Mono, DejaVu Sans Mono
- **Fallback**: Courier New, Courier, monospace

**Rationale**: Monospace fonts optimized for code readability.

### Font Sizes

#### Unified Font Size Scale

| Element | Point Size | Pixel Equivalent (96 DPI) | Usage |
|---------|------------|---------------------------|-------|
| H1 | 18pt | 24px | Document title, major sections |
| H2 | 16pt | 21px | Major sections |
| H3 | 14pt | 19px | Subsections |
| H4 | 12pt | 16px | Sub-subsections |
| H5 | 11pt | 15px | Detail level |
| H6 | 10pt | 13px | Fine detail |
| Body Text | 11pt | 15px | Paragraphs, lists |
| Code Block | 10pt | 13px | Code blocks |
| Inline Code | 10pt | 13px | Inline code |
| Small Text | 9pt | 12px | Footnotes, captions |

#### Format-Specific Adaptations

**Word**:
- H1: 18pt (matches unified scale)
- Body: 11pt (matches unified scale)
- Code: 10pt (matches unified scale)

**PowerPoint**:
- Title Slide Title: 44pt (larger for presentation)
- Slide Title (H2): 32pt (larger for readability)
- Body Text: 18pt (larger for presentation)
- Code: 10pt (smaller to fit on slides)

**PDF**:
- H1: 18pt (matches unified scale)
- Body: 11pt (matches unified scale)
- Code: 10pt (matches unified scale)

### Font Weights

| Weight | Usage | Examples |
|--------|-------|----------|
| Regular (400) | Body text, paragraphs | Normal paragraph text |
| Medium (500) | Subtle emphasis | Optional for H4-H6 |
| Semibold (600) | Headings H3-H6 | Subsection headings |
| Bold (700) | Headings H1-H2, emphasis | Major headings, bold text |

### Line Spacing

| Element | Line Spacing | Spacing Type |
|---------|--------------|--------------|
| Body Text | 1.15x | Multiple (slightly more than single) |
| Headings | 1.2x | Multiple |
| Code Blocks | 1.0x | Single (exact line spacing) |
| Lists | 1.15x | Multiple (matches body text) |

### Paragraph Spacing

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

## Visual Hierarchy

### Heading Hierarchy

The heading hierarchy creates clear document structure:

```
H1 (18pt, Bold) - Document Title
  └── H2 (16pt, Bold) - Major Section
      └── H3 (14pt, Bold) - Subsection
          └── H4 (12pt, Bold) - Sub-subsection
              └── H5 (11pt, Bold) - Detail
                  └── H6 (10pt, Bold) - Fine Detail
```

### Visual Separation

#### Section Separation

- **Major Sections (H2)**: 20pt spacing before, clear visual break
- **Subsections (H3)**: 16pt spacing before, moderate visual break
- **Horizontal Rules**: 2pt solid line (#CCCCCC) for major separations

#### Content Grouping

- **Paragraphs**: 6pt spacing after for readability
- **Lists**: 6pt spacing before and after
- **Code Blocks**: 6pt spacing before and after with background
- **Blockquotes**: 6pt spacing before and after with indentation

### Emphasis Styles

| Markdown | Visual Style | Font Weight | Color |
|----------|--------------|-------------|-------|
| Bold (`**text**`) | Bold | 700 (Bold) | Same as text |
| Italic (`*text*`) | Italic | 400 (Regular) | Same as text |
| Bold Italic (`***text***`) | Bold + Italic | 700 (Bold) | Same as text |
| Strikethrough (`~~text~~`) | Strikethrough | 400 (Regular) | Same as text or gray |

## Format-Specific Adaptations

### Word Adaptations

#### Style System

- **Use Built-in Styles**: Leverage Word's built-in heading styles (Heading 1-6)
- **Override Styles**: Customize built-in styles to match unified styling
- **Theme Colors**: Apply color scheme through Word theme colors
- **Paragraph Styles**: Use Normal style for body text with custom spacing

#### Formatting Application

- **Heading Styles**: Apply Heading 1-6 styles with unified font sizes
- **Body Text**: Use Normal style with 11pt font, 1.15x line spacing
- **Code Blocks**: Custom style with monospace font, background, border
- **Lists**: Use Word list formatting with consistent indentation

#### Word-Specific Features

- **Table of Contents**: Auto-generate from heading styles
- **Navigation Pane**: Headings appear automatically
- **Cross-References**: Enable cross-references to headings
- **Document Properties**: Set title, author, keywords

### PowerPoint Adaptations

#### Slide Scaling

PowerPoint requires larger fonts for presentation readability:

- **Title Slide**: 44pt (much larger than Word/PDF)
- **Slide Titles (H2)**: 32pt (larger for slides)
- **Body Text**: 18pt (larger for presentation)
- **Code**: 10pt (smaller to fit on slides)

#### Color Application

- **Slide Background**: White (#FFFFFF)
- **Title Colors**: Primary Blue (#0078D4) for title slide, dark gray (#323130) for slide titles
- **Text Colors**: Primary Text (#323130) for body text
- **Accents**: Use Primary Blue for key elements

#### Slide Layouts

- **Title Slide**: Title in Primary Blue (#0078D4), 44pt
- **Content Slides**: Title in dark gray (#323130), 32pt
- **Consistent Spacing**: Apply unified spacing rules scaled for slides

### PDF Adaptations

#### Typography

- **Font Embedding**: Embed fonts in PDF for consistent rendering
- **Font Selection**: Use serif (Times) or sans-serif (Helvetica/Arial) based on preference
- **Sizes**: Match unified font size scale exactly
- **Line Spacing**: Apply unified line spacing (1.15x for body)

#### Color Application

- **Text Colors**: Use unified text colors (#323130 for primary)
- **Backgrounds**: Use unified background colors (#F5F5F5 for code blocks)
- **Links**: Use unified link color (#0078D4)

#### PDF-Specific Features

- **Bookmarks**: Generate from heading hierarchy with unified styling
- **Table of Contents**: Optional TOC with unified typography
- **Metadata**: Set PDF metadata (title, author, keywords)

## Element-Specific Styling

### Code Blocks

#### Unified Styling

- **Font**: Monospace font stack (Consolas/Menlo/Courier New)
- **Font Size**: 10pt
- **Background**: #F5F5F5 (light gray)
- **Border**: Optional 1pt solid #CCCCCC
- **Padding**: 6pt all sides
- **Line Spacing**: 1.0x (single spacing)

#### Format Adaptations

- **Word**: Formatted paragraph or text box with background
- **PowerPoint**: Text box with background, may truncate if long
- **PDF**: Formatted text block with background and border

### Tables

#### Unified Styling

- **Borders**: 1pt solid #000000 (black)
- **Header Row**: Bold font, #F2F2F2 background
- **Cell Padding**: 6pt all sides
- **Alignment**: Preserve markdown alignment (left/center/right)

#### Format Adaptations

- **Word**: Word table object with unified styling
- **PowerPoint**: PowerPoint table with unified styling, fit to slide
- **PDF**: PDF table with unified styling, may span pages

### Lists

#### Unified Styling

- **Bullet Style**: Round bullet (•)
- **Number Format**: Arabic numerals (1, 2, 3...)
- **Indentation**: 0.25" per nesting level
- **Spacing**: 3pt between items
- **Font**: Same as body text (11pt)

#### Format Adaptations

- **Word**: Word list formatting with unified indentation
- **PowerPoint**: Slide bullet points with unified styling
- **PDF**: Formatted lists with unified indentation

### Blockquotes

#### Unified Styling

- **Indentation**: 0.5" left indent
- **Border**: Optional 3pt solid #CCCCCC left border
- **Background**: Optional #FAFAFA light background
- **Font Style**: Optional italic
- **Spacing**: 6pt before and after

#### Format Adaptations

- **Word**: Formatted paragraph with indentation and optional border
- **PowerPoint**: Text box with indentation and optional styling
- **PDF**: Formatted text block with indentation and optional border

### Images

#### Unified Styling

- **Placement**: Inline with text flow
- **Sizing**: Preserve aspect ratio, scale to fit
- **Alignment**: Left-aligned (default), center/right if specified
- **Border**: No border (default), optional border for emphasis

#### Format Adaptations

- **Word**: Inline image, embedded, alt text preserved
- **PowerPoint**: Slide image, embedded, sized for slide
- **PDF**: Embedded image, inline or block placement

## Consistency Guidelines

### Cross-Format Consistency

1. **Color Scheme**: Use unified color scheme across all formats
2. **Typography**: Maintain consistent font families and sizes (scaled appropriately)
3. **Spacing**: Apply consistent spacing rules (scaled for PowerPoint)
4. **Hierarchy**: Maintain consistent visual hierarchy
5. **Element Styling**: Apply consistent styling to code blocks, tables, lists

### Format-Specific Considerations

1. **Word**: Leverage Word's style system while maintaining unified appearance
2. **PowerPoint**: Scale fonts and spacing for presentation while maintaining visual identity
3. **PDF**: Apply unified styling directly with font embedding for consistency

### Quality Standards

1. **Readability**: Ensure sufficient contrast and readable fonts
2. **Professionalism**: Maintain professional, business-appropriate appearance
3. **Consistency**: Apply styles consistently throughout documents
4. **Accessibility**: Ensure accessibility through proper contrast and structure

## Examples

### Heading Example

```
# Document Title (H1, 18pt, Bold, #0078D4)

## Major Section (H2, 16pt, Bold, #323130)

### Subsection (H3, 14pt, Bold, #323130)
```

### Code Block Example

```
Background: #F5F5F5
Font: Consolas, 10pt
Border: 1pt solid #CCCCCC (optional)
Padding: 6pt all sides
```

### Table Example

```
Header: Bold, #F2F2F2 background
Borders: 1pt solid #000000
Cell Padding: 6pt all sides
```

## Conclusion

This styling guide provides a unified styling system that ensures consistent, professional appearance across Word, PowerPoint, and PDF formats. By following these guidelines, the conversion tool will produce documents with cohesive visual identity while respecting format-specific capabilities and constraints.

