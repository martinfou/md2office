# Test Suite Specification

## Overview

This specification defines comprehensive test cases for validating the accuracy and quality of markdown-to-office document conversion. The test suite covers all markdown elements, edge cases, format-specific validation, and CLI functionality to ensure the conversion tool produces accurate, high-quality outputs.

### Test Strategy

1. **Comprehensive Coverage**: Test all markdown elements and conversion scenarios
2. **Edge Case Testing**: Test boundary conditions and error scenarios
3. **Format Validation**: Validate output quality for each format
4. **Integration Testing**: Test end-to-end conversion workflows
5. **Regression Testing**: Ensure changes don't break existing functionality

### Test Approach

- **Unit Tests**: Test individual components (parser, generators)
- **Integration Tests**: Test complete conversion workflows
- **End-to-End Tests**: Test full CLI functionality
- **Visual Validation**: Manual review of output quality
- **Automated Validation**: Automated checks for structure and content

## Test Categories

### 1. Markdown Element Tests

Test conversion of individual markdown elements to ensure correct mapping and formatting.

### 2. Edge Case Tests

Test boundary conditions, error scenarios, and unusual inputs.

### 3. Format-Specific Tests

Test format-specific features and validation requirements.

### 4. CLI Functionality Tests

Test command-line interface, options, and error handling.

### 5. Integration Tests

Test complete workflows and cross-format consistency.

## Test Cases

### Markdown Element Tests

#### Headers (H1-H6)

| Test ID | Test Case | Input | Expected Word | Expected PowerPoint | Expected PDF |
|---------|-----------|-------|---------------|---------------------|--------------|
| HDR-001 | H1 Header | `# Title` | Heading 1 style, 18pt, bold | Title slide with title | H1 bookmark, 18pt |
| HDR-002 | H2 Header | `## Section` | Heading 2 style, 16pt, bold | Slide title, 32pt | H2 bookmark, 16pt |
| HDR-003 | H3 Header | `### Subsection` | Heading 3 style, 14pt, bold | Slide subtitle, 24pt | H3 bookmark, 14pt |
| HDR-004 | H4-H6 Headers | `####`, `#####`, `######` | Heading 4-6 styles | Content headers | H4-H6 bookmarks |
| HDR-005 | Header Hierarchy | H1 → H2 → H3 | Hierarchy preserved | Slide hierarchy preserved | Bookmark hierarchy preserved |
| HDR-006 | Header with Special Chars | `# Header (with) [brackets]` | Special chars preserved | Special chars preserved | Special chars preserved |
| HDR-007 | Multiple H1 Headers | Multiple `#` headers | Multiple H1 sections | Multiple title slides | Multiple H1 bookmarks |
| HDR-008 | Skipped Levels | H1 → H3 (skip H2) | Handle gracefully | Handle gracefully | Handle gracefully |

#### Paragraphs

| Test ID | Test Case | Input | Expected Word | Expected PowerPoint | Expected PDF |
|---------|-----------|-------|---------------|---------------------|--------------|
| PARA-001 | Simple Paragraph | `This is a paragraph.` | Normal style, 11pt | Body text, 18pt | Paragraph text, 11pt |
| PARA-002 | Multiple Paragraphs | Two paragraphs separated by blank line | Two paragraphs with spacing | Two text blocks | Two paragraphs |
| PARA-003 | Paragraph with Line Break | `Line 1  \nLine 2` | Hard line break preserved | Line break preserved | Line break preserved |
| PARA-004 | Long Paragraph | Very long paragraph (>500 words) | Wrapped text | Split across slides if needed | Wrapped text |
| PARA-005 | Paragraph with Emphasis | `This is **bold** and *italic*` | Bold and italic preserved | Bold and italic preserved | Bold and italic preserved |

#### Lists

| Test ID | Test Case | Input | Expected Word | Expected PowerPoint | Expected PDF |
|---------|-----------|-------|---------------|---------------------|--------------|
| LST-001 | Unordered List | `- Item 1\n- Item 2` | Bulleted list | Bullet points | Bulleted list |
| LST-002 | Ordered List | `1. First\n2. Second` | Numbered list | Numbered list | Numbered list |
| LST-003 | Nested Lists | `- Item\n  - Nested` | Nested bullets | Nested bullets | Nested bullets |
| LST-004 | Task List | `- [ ] Task\n- [x] Done` | Checkbox list | Checkbox bullets | Checkbox list |
| LST-005 | Mixed Lists | Ordered + unordered | Mixed formatting | Mixed formatting | Mixed formatting |
| LST-006 | Deep Nesting | 5+ levels nested | Deep nesting preserved | Deep nesting preserved | Deep nesting preserved |
| LST-007 | Empty List Items | `- \n- Item` | Handle gracefully | Handle gracefully | Handle gracefully |
| LST-008 | List Continuation | List across sections | Continue numbering | Continue formatting | Continue numbering |

#### Code Blocks

| Test ID | Test Case | Input | Expected Word | Expected PowerPoint | Expected PDF |
|---------|-----------|-------|---------------|---------------------|--------------|
| CODE-001 | Fenced Code Block | ` ```python\ncode\n``` ` | Monospace, background | Monospace, background | Monospace, background |
| CODE-002 | Inline Code | `` `code` `` | Inline monospace | Inline monospace | Inline monospace |
| CODE-003 | Code with Language | ` ```javascript\ncode\n``` ` | Language preserved | Language preserved | Language preserved |
| CODE-004 | Long Code Block | 100+ lines of code | Full content preserved | Truncate or split | Full content preserved |
| CODE-005 | Code with Special Chars | Code with `*`, `#`, `[]` | Special chars preserved | Special chars preserved | Special chars preserved |
| CODE-006 | Nested Code Blocks | Code block in list | Formatting preserved | Formatting preserved | Formatting preserved |
| CODE-007 | Code Block Indentation | Indented code | Indentation preserved | Indentation preserved | Indentation preserved |

#### Tables

| Test ID | Test Case | Input | Expected Word | Expected PowerPoint | Expected PDF |
|---------|-----------|-------|---------------|---------------------|--------------|
| TBL-001 | Simple Table | 2x2 table | Word table object | PowerPoint table | PDF table |
| TBL-002 | Table Alignment | Left/center/right aligned | Alignment preserved | Alignment preserved | Alignment preserved |
| TBL-003 | Table Header | Header row | Bold header, shaded | Bold header, shaded | Bold header, shaded |
| TBL-004 | Large Table | 10x10 table | Table spans pages | Simplify or split | Table spans pages |
| TBL-005 | Table with Code | Code in cells | Code formatting preserved | Code formatting preserved | Code formatting preserved |
| TBL-006 | Table with Images | Images in cells | Images embedded | Images embedded | Images embedded |
| TBL-007 | Empty Cells | Table with empty cells | Empty cells preserved | Empty cells preserved | Empty cells preserved |
| TBL-008 | Malformed Table | Invalid table syntax | Handle gracefully | Handle gracefully | Handle gracefully |

#### Images

| Test ID | Test Case | Input | Expected Word | Expected PowerPoint | Expected PDF |
|---------|-----------|-------|---------------|---------------------|--------------|
| IMG-001 | Inline Image | `![alt](image.png)` | Image embedded inline | Image on slide | Image embedded |
| IMG-002 | Image with Alt Text | `![Description](img.png)` | Alt text preserved | Alt text preserved | Alt text preserved |
| IMG-003 | Relative Path Image | `![alt](./images/img.png)` | Path resolved | Path resolved | Path resolved |
| IMG-004 | Absolute Path Image | `![alt](/path/img.png)` | Path used as-is | Path used as-is | Path used as-is |
| IMG-005 | URL Image | `![alt](https://example.com/img.png)` | Image downloaded and embedded | Image downloaded | Image downloaded |
| IMG-006 | Missing Image | `![alt](missing.png)` | Placeholder or skip | Placeholder or skip | Placeholder or skip |
| IMG-007 | Large Image | 2000x2000px image | Scaled down | Scaled down | Scaled down |
| IMG-008 | Multiple Images | Multiple images | All embedded | All embedded | All embedded |
| IMG-009 | Image Formats | PNG, JPEG, GIF, SVG | All formats supported | All formats supported | SVG converted |

#### Links

| Test ID | Test Case | Input | Expected Word | Expected PowerPoint | Expected PDF |
|---------|-----------|-------|---------------|---------------------|--------------|
| LINK-001 | Inline Link | `[text](url)` | Hyperlink field | Hyperlink | Hyperlink annotation |
| LINK-002 | Reference Link | `[text][ref]` | Resolved hyperlink | Resolved hyperlink | Resolved hyperlink |
| LINK-003 | Autolink | `<https://example.com>` | Hyperlink | Hyperlink | Hyperlink |
| LINK-004 | Link with Title | `[text](url "title")` | Title preserved | Title preserved | Title preserved |
| LINK-005 | Broken Link | Invalid URL | Handle gracefully | Handle gracefully | Handle gracefully |
| LINK-006 | Link in Table | Link in table cell | Link preserved | Link preserved | Link preserved |
| LINK-007 | Link in List | Link in list item | Link preserved | Link preserved | Link preserved |

#### Emphasis

| Test ID | Test Case | Input | Expected Word | Expected PowerPoint | Expected PDF |
|---------|-----------|-------|---------------|---------------------|--------------|
| EMP-001 | Bold Text | `**bold**` | Bold formatting | Bold formatting | Bold formatting |
| EMP-002 | Italic Text | `*italic*` | Italic formatting | Italic formatting | Italic formatting |
| EMP-003 | Bold Italic | `***both***` | Bold + italic | Bold + italic | Bold + italic |
| EMP-004 | Strikethrough | `~~strike~~` | Strikethrough | Strikethrough | Strikethrough |
| EMP-005 | Nested Emphasis | `**bold *italic* bold**` | Nested preserved | Nested preserved | Nested preserved |

#### Blockquotes

| Test ID | Test Case | Input | Expected Word | Expected PowerPoint | Expected PDF |
|---------|-----------|-------|---------------|---------------------|--------------|
| BQ-001 | Simple Blockquote | `> Quote text` | Indented paragraph | Text box | Indented block |
| BQ-002 | Multi-Paragraph Quote | `> Para 1\n> Para 2` | Multiple paragraphs | Multiple paragraphs | Multiple paragraphs |
| BQ-003 | Nested Blockquote | `> > Nested` | Increased indent | Increased indent | Increased indent |
| BQ-004 | Blockquote with Code | `> Code block` | Code formatting preserved | Code formatting preserved | Code formatting preserved |

#### Horizontal Rules

| Test ID | Test Case | Input | Expected Word | Expected PowerPoint | Expected PDF |
|---------|-----------|-------|---------------|---------------------|--------------|
| HR-001 | Horizontal Rule | `---` | Horizontal line | Slide separator | Horizontal line |
| HR-002 | HR as Page Break | `---` (with flag) | Page break | New slide | Page break |

### Edge Case Tests

| Test ID | Test Case | Input | Expected Behavior |
|---------|-----------|-------|-------------------|
| EDGE-001 | Empty Document | Empty markdown file | Handle gracefully, error or empty output |
| EDGE-002 | Very Long Document | 10,000+ lines | Process successfully, maintain performance |
| EDGE-003 | Special Characters | Unicode, emoji | Characters preserved |
| EDGE-004 | Malformed Markdown | Invalid syntax | Handle gracefully, report errors |
| EDGE-005 | Missing Images | All images missing | Placeholders or skip, continue conversion |
| EDGE-006 | Broken References | Invalid links, images | Handle gracefully, continue conversion |
| EDGE-007 | Deep Nesting | 10+ levels nested | Handle gracefully, preserve structure |
| EDGE-008 | Very Wide Table | 20+ columns | Handle gracefully, may need simplification |
| EDGE-009 | Very Long Code Block | 1000+ lines | Preserve full content (Word/PDF), handle (PPT) |
| EDGE-010 | Mixed Content Types | All elements mixed | All elements converted correctly |
| EDGE-011 | No Headings | Document without headings | Handle gracefully, use paragraph structure |
| EDGE-012 | Only Headings | Document with only headings | Handle gracefully, create structure |
| EDGE-013 | Whitespace Only | Document with only whitespace | Handle gracefully, create empty output |
| EDGE-014 | Invalid File Path | Non-existent file | Error message, exit with error code |

### Format-Specific Tests

#### Word Format Tests

| Test ID | Test Case | Validation Criteria |
|---------|-----------|-------------------|
| WORD-001 | Document Opens | Word opens document without errors |
| WORD-002 | Styles Applied | Heading styles correctly applied |
| WORD-003 | Navigation Pane | Headings appear in navigation pane |
| WORD-004 | Table of Contents | TOC generated correctly (if requested) |
| WORD-005 | Images Embedded | Images embedded, not linked |
| WORD-006 | Links Functional | Hyperlinks are clickable |
| WORD-007 | Page Breaks | Page breaks inserted correctly (if requested) |
| WORD-008 | Document Properties | Metadata set correctly |

#### PowerPoint Format Tests

| Test ID | Test Case | Validation Criteria |
|---------|-----------|-------------------|
| PPT-001 | Presentation Opens | PowerPoint opens presentation without errors |
| PPT-002 | Slide Structure | Slide structure matches heading hierarchy |
| PPT-003 | Slide Layouts | Appropriate layouts used |
| PPT-004 | Images Embedded | Images embedded on slides |
| PPT-005 | Content Fits | Content fits on slides appropriately |
| PPT-006 | Slide Transitions | Transitions applied (if specified) |
| PPT-007 | Theme Applied | Consistent theme across slides |

#### PDF Format Tests

| Test ID | Test Case | Validation Criteria |
|---------|-----------|-------------------|
| PDF-001 | PDF Opens | PDF opens without errors |
| PDF-002 | Bookmarks | Bookmarks match heading hierarchy |
| PDF-003 | Table of Contents | TOC generated correctly (if requested) |
| PDF-004 | Images Embedded | Images embedded, not linked |
| PDF-005 | Links Functional | Hyperlinks are clickable |
| PDF-006 | Font Embedding | Fonts embedded for consistent rendering |
| PDF-007 | Page Layout | Page layout preserved correctly |

### CLI Functionality Tests

| Test ID | Test Case | Command | Expected Behavior |
|---------|-----------|---------|-------------------|
| CLI-001 | Basic Conversion | `md2office --word doc.md` | Converts to Word |
| CLI-002 | Multiple Formats | `md2office --word --powerpoint doc.md` | Converts to both formats |
| CLI-003 | Output Directory | `md2office --word -o ./output doc.md` | Outputs to specified directory |
| CLI-004 | Custom Name | `md2office --word -n report doc.md` | Uses custom filename |
| CLI-005 | Help Command | `md2office --help` | Shows help message |
| CLI-006 | Version Command | `md2office --version` | Shows version information |
| CLI-007 | Invalid File | `md2office --word missing.md` | Error message, exit code 2 |
| CLI-008 | No Format Specified | `md2office doc.md` | Error message, exit code 64 |
| CLI-009 | Batch Conversion | `md2office --word *.md` | Converts all files |
| CLI-010 | Verbose Mode | `md2office --word --verbose doc.md` | Shows detailed output |
| CLI-011 | Quiet Mode | `md2office --word --quiet doc.md` | Suppresses output |
| CLI-012 | Configuration File | `md2office --word -c config.json doc.md` | Uses configuration |

### Integration Tests

| Test ID | Test Case | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| INT-001 | End-to-End Conversion | Complete markdown → Word conversion | Successful conversion |
| INT-002 | Multi-Format Conversion | Convert to all formats simultaneously | All formats generated correctly |
| INT-003 | Batch Processing | Convert directory of files | All files converted |
| INT-004 | Cross-Format Consistency | Compare content across formats | Content consistent across formats |
| INT-005 | Large Document | Convert 1000+ line document | Successful conversion, good performance |
| INT-006 | Complex Document | Document with all element types | All elements converted correctly |

## Test Data

### Sample Markdown Files

#### Basic Document (`test-basic.md`)

```markdown
# Document Title

This is a paragraph with **bold** and *italic* text.

## Section 1

- Item 1
- Item 2
- Item 3

### Subsection

1. First item
2. Second item
```

#### Complex Document (`test-complex.md`)

```markdown
# Complex Document

## Introduction

This document contains various markdown elements.

### Code Example

```python
def hello():
    print("Hello, World!")
```

### Table Example

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

### Image Example

![Image](image.png)

## Conclusion

> This is a blockquote.

---

End of document.
```

#### Edge Case Document (`test-edge.md`)

```markdown
# Edge Cases

## Special Characters

Unicode: 中文, 日本語, 한국어
Emoji: 😀 🎉 ✅

## Empty Sections

## Very Long Content

[Very long paragraph...]

## Nested Structures

- Level 1
  - Level 2
    - Level 3
      - Level 4
```

## Validation Criteria

### Word Format Validation

1. **Document Structure**: Document opens without errors
2. **Styles**: Heading styles (Heading 1-6) correctly applied
3. **Navigation**: Headings appear in navigation pane
4. **Content**: All content preserved and formatted correctly
5. **Images**: Images embedded (not linked)
6. **Links**: Hyperlinks are clickable
7. **Tables**: Tables formatted correctly
8. **Lists**: Lists formatted correctly

### PowerPoint Format Validation

1. **Presentation**: Presentation opens without errors
2. **Slide Structure**: Slide structure matches heading hierarchy
3. **Layouts**: Appropriate slide layouts used
4. **Content**: Content fits on slides appropriately
5. **Images**: Images embedded on slides
6. **Formatting**: Consistent formatting across slides
7. **Theme**: Consistent theme applied

### PDF Format Validation

1. **PDF Structure**: PDF opens without errors
2. **Bookmarks**: Bookmarks match heading hierarchy
3. **Content**: All content preserved
4. **Images**: Images embedded correctly
5. **Links**: Hyperlinks are clickable
6. **Fonts**: Fonts embedded for consistent rendering
7. **Layout**: Page layout preserved correctly

## Implementation Notes

### Test Framework

- **Unit Tests**: Use testing framework (Go: testing, Python: pytest, JS: Jest)
- **Integration Tests**: End-to-end test framework
- **Visual Validation**: Manual review checklist
- **Automated Validation**: Scripts to check structure and content

### Test Execution

1. **Unit Tests**: Run automatically on code changes
2. **Integration Tests**: Run on pull requests
3. **End-to-End Tests**: Run before releases
4. **Visual Validation**: Manual review before releases

### Test Coverage Goals

- **Code Coverage**: >80% code coverage
- **Element Coverage**: 100% of markdown elements tested
- **Edge Case Coverage**: All edge cases tested
- **Format Coverage**: All formats validated

## Conclusion

This test suite specification provides comprehensive test cases for validating markdown-to-office document conversion. The test cases cover all markdown elements, edge cases, format-specific validation, and CLI functionality to ensure accurate, high-quality conversions.

