# PowerPoint Template Guide

This guide explains how to structure your markdown documents for optimal PowerPoint generation with md2office.

## Quick Start

Use the template file `examples/input/powerpoint-template.md` as a starting point for your presentations.

## Slide Structure

### Heading Hierarchy

The PowerPoint generator uses heading levels to determine slide structure:

#### H1 (`#`) - Title Slide
- **Creates**: Title slide (first slide)
- **Usage**: Use once at the beginning of your document
- **Content**: Document title
- **Optional**: Add a subtitle paragraph immediately after H1

**Example:**
```markdown
# My Presentation Title

Optional subtitle or description
```

#### H2 (`##`) - Section Slides
- **Creates**: New slide for each H2 heading
- **Usage**: Use for major sections/topics
- **Content**: All content under H2 until the next H2 becomes slide content
- **Best Practice**: Keep sections focused and concise

**Example:**
```markdown
## Introduction

Content for introduction slides goes here.

## Main Topic

Content for main topic slides goes here.
```

#### H3 (`###`) - Subsection Headers
- **Creates**: New slide OR subsection header within current slide
- **Usage**: Use for subsections within major topics
- **Behavior**: 
  - Creates new slide if content is substantial
  - Becomes subsection header if content is brief
- **Best Practice**: Use H3 to organize content within sections

**Example:**
```markdown
## Main Topic

### Subsection A

Content for subsection A.

### Subsection B

Content for subsection B.
```

#### H4-H6 (`####`, `#####`, `######`) - Nested Content
- **Creates**: Content headers within slides
- **Usage**: Use for nested content organization
- **Best Practice**: Use sparingly for deep nesting

## Content Elements

### Lists (Bullet Points)

Lists are ideal for slide content. Use unordered lists for key points:

```markdown
## Key Features

- Feature one
- Feature two
- Feature three
  - Sub-feature 3.1
  - Sub-feature 3.2
- Feature four
```

**Guidelines:**
- Keep to 7-10 bullet points per slide
- Use nested lists for sub-points
- Keep bullet text concise (one line when possible)

### Ordered Lists

Use numbered lists for steps or sequences:

```markdown
## Implementation Steps

1. First step
2. Second step
3. Third step
```

### Paragraphs

Use paragraphs for explanations or context:

```markdown
## Overview

This section provides an overview of the topic. 
Paragraphs work well for longer explanations that 
need more context than bullet points.
```

**Guidelines:**
- Keep paragraphs short (2-3 sentences)
- Use paragraphs sparingly on slides
- Prefer bullet points for most slide content

### Code Blocks

Code blocks appear on their own slide:

```markdown
## Code Example

```python
def example_function():
    """Example code."""
    return result
```
```

**Guidelines:**
- One code block per slide
- Keep code blocks concise
- Use appropriate language tags

### Tables

Tables are displayed on slides:

```markdown
## Comparison

| Feature | Option A | Option B |
|---------|----------|----------|
| Cost    | Low      | High     |
| Quality | Good     | Excellent|
```

**Guidelines:**
- Keep tables simple (3-5 columns max)
- One table per slide
- Use for comparisons or structured data

### Images

Images are embedded in slides:

```markdown
## Visual Example

![Description of image](path/to/image.png)
```

**Guidelines:**
- 1-2 images per slide
- Use descriptive alt text
- Ensure images are accessible
- Use relative paths or absolute paths

### Links

Links become clickable hyperlinks:

```markdown
## Resources

Visit [our website](https://example.com) for more information.
```

### Text Formatting

Use markdown formatting for emphasis:

- **Bold** (`**text**`) - For strong emphasis
- *Italic* (`*text*`) - For subtle emphasis
- `Inline code` (`` `code` ``) - For code references
- ***Bold and italic*** (`***text***`) - For combined emphasis

### Blockquotes

Use blockquotes for callouts or important quotes:

```markdown
## Important Note

> This is an important callout that stands out from regular content.
```

## Best Practices

### Slide Organization

1. **Start with H1** - Always begin with a title slide
2. **Use H2 for sections** - Each major topic gets its own H2
3. **Group related content** - Keep related content under the same H2
4. **Use H3 for subsections** - Organize content within sections
5. **Keep slides focused** - One main idea per slide

### Content Guidelines

1. **Be concise** - Slides should be scannable
2. **Use bullet points** - They're easier to read on slides
3. **Limit content** - 7-10 bullet points or equivalent text per slide
4. **Use visuals** - Images and tables enhance understanding
5. **Maintain consistency** - Use consistent formatting throughout

### Structure Tips

1. **Logical flow** - Organize content in a logical sequence
2. **Clear hierarchy** - Use headings to show relationships
3. **Natural breaks** - Use H2 to create natural section breaks
4. **Progressive detail** - Start broad, get more specific

### Common Patterns

#### Pattern 1: Simple Presentation
```markdown
# Title

## Section 1
- Point 1
- Point 2

## Section 2
- Point 1
- Point 2

## Conclusion
- Summary point
```

#### Pattern 2: Detailed Presentation
```markdown
# Title

## Introduction
### Overview
Content here.

### Objectives
- Objective 1
- Objective 2

## Main Topic
### Subsection A
Content here.

### Subsection B
Content here.

## Conclusion
Summary here.
```

#### Pattern 3: Technical Presentation
```markdown
# Technical Topic

## Overview
Brief overview.

## Architecture
### Components
- Component 1
- Component 2

### Code Example
```python
code here
```

## Implementation
Details here.

## Conclusion
Summary.
```

## Template Structure

The provided template (`examples/input/powerpoint-template.md`) includes:

1. **Front matter** - Optional metadata (title, author, subtitle)
2. **Title slide** - H1 with optional subtitle
3. **Introduction section** - H2 with overview content
4. **Main sections** - Multiple H2 sections
5. **Subsections** - H3 subsections within sections
6. **Examples** - Code blocks, tables, images
7. **Conclusion** - Final summary section

## Converting to PowerPoint

Once your markdown is structured correctly:

```bash
# Convert to PowerPoint
md2office --powerpoint your-presentation.md

# Or specify output directory
md2office --powerpoint --output ./output your-presentation.md

# Use a style preset
md2office --powerpoint --style professional your-presentation.md
```

### Mermaid Diagram Support

md2office can render Mermaid diagrams as images in PowerPoint slides. To enable this feature:

1. **Install Node.js** (if not already installed): Download from [nodejs.org](https://nodejs.org/)

2. **Install mermaid-cli**:
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

3. **Use Mermaid diagrams in your markdown**:
   ```markdown
   ```mermaid
   graph LR
       A[Start] --> B[End]
   ```
   ```

The diagrams will be automatically rendered as images in your PowerPoint slides. If `mermaid-cli` is not installed, the diagram code will be displayed as text instead.

## Troubleshooting

### Too Much Content on One Slide
- Split content across multiple H2 sections
- Use H3 to create new slides
- Break long paragraphs into bullet points

### Not Enough Slides
- Add more H2 sections
- Use H3 to create additional slides
- Add more content under existing sections

### Content Not Appearing
- Check heading hierarchy (H1 → H2 → H3)
- Ensure content is under appropriate headings
- Verify markdown syntax is correct

### Slides Look Crowded
- Reduce content per slide
- Use more H2 sections to split content
- Convert paragraphs to bullet points

## Examples

See `examples/input/powerpoint-template.md` for a complete example with all supported elements.

## Additional Resources

- [PowerPoint Conversion Specification](../specs/artifacts/powerpoint-conversion-specification.md)
- [Usage Guide](usage.md)
- [Quick Start Guide](quickstart.md)

