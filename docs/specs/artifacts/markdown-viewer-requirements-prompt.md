# CFT Prompt: Markdown Viewer with Mermaid.js Support - Requirements Document

## Context

You are a technical requirements analyst working on the **md2office** application, a Python-based markdown to Office document converter (Word, PowerPoint, PDF) built with PySide6/Qt. The application currently provides:

- **CLI interface** for command-line conversions
- **GUI interface** (`MainWindow`) with file selection, format options, and conversion controls
- **Conversion capabilities** to Word (.docx), PowerPoint (.pptx), and PDF formats
- **Markdown parsing** infrastructure via the `md2office.parser` module
- **Styling system** for consistent document formatting

The application uses:
- **PySide6** (Qt6) for the GUI framework
- **Python 3.8+** as the runtime
- **Markdown parsing** libraries (likely markdown or similar)
- **Cross-platform support** (Windows, macOS, Linux)

**Current State:**
- Users can select markdown files and convert them to Office formats
- There is **no preview/viewer functionality** - users cannot see the markdown content before conversion
- Mermaid.js diagrams are mentioned in documentation but are **not currently rendered** in any viewer
- The GUI is functional but lacks a preview pane

**Business Need:**
Users need to preview markdown content (including Mermaid.js diagrams) before converting to Office formats to:
- Verify content accuracy and formatting
- Check diagram rendering before conversion
- Reduce conversion errors and rework
- Improve user confidence in the conversion process

**Technical Constraints:**
- Must integrate seamlessly with existing PySide6 GUI architecture
- Must maintain cross-platform compatibility
- Should not significantly impact application startup time or memory footprint
- Must handle large markdown files efficiently
- Should support real-time preview updates as markdown files change

**User Personas:**
- **Content creators** who generate markdown with Mermaid diagrams using Microsoft Copilot
- **Technical writers** who need to verify diagram accuracy before conversion
- **Business users** who want to preview documents before sharing in Office formats

## Task

Create a comprehensive, detailed requirements document for implementing a **markdown viewer component with Mermaid.js support** in the md2office application. The requirements document should serve as a complete specification for a programmer to implement this feature.

The document must include:

### 1. Executive Summary
- Brief overview of the feature
- Business justification and user benefits
- High-level technical approach

### 2. Functional Requirements
- **FR-1**: Markdown rendering and display
  - Render standard markdown syntax (headings, lists, tables, code blocks, links, images)
  - Support GitHub Flavored Markdown (GFM) features
  - Handle frontmatter/metadata
  - Display syntax highlighting for code blocks
  
- **FR-2**: Mermaid.js diagram rendering
  - Detect and render Mermaid code blocks (```mermaid)
  - Support all Mermaid diagram types (flowchart, sequence, class, state, ER, gantt, pie, gitgraph, etc.)
  - Handle diagram errors gracefully with user-friendly messages
  - Support Mermaid configuration and themes
  
- **FR-3**: Viewer integration with existing GUI
  - Add preview pane to MainWindow (split view or tabbed interface)
  - Sync preview with selected markdown file
  - Update preview when markdown file changes (optional: file watching)
  - Maintain existing conversion workflow
  
- **FR-4**: User interaction features
  - Scroll synchronization (optional)
  - Zoom controls for preview
  - Copy rendered content
  - Print preview (optional)
  - Export preview as HTML/image (optional)

### 3. Technical Requirements
- **TR-1**: Technology stack and dependencies
  - Specify Python libraries for markdown rendering (e.g., markdown, markdown2, mistune)
  - Specify Mermaid.js integration approach (Python wrapper, QWebEngineView, or embedded JS)
  - List all new dependencies and version requirements
  - Consider security implications of JavaScript execution
  
- **TR-2**: Architecture and design
  - Component structure and class hierarchy
  - Integration points with existing codebase
  - Data flow from markdown file → parser → renderer → viewer
  - Threading model (if preview rendering is async)
  
- **TR-3**: Performance requirements
  - Maximum acceptable preview rendering time for typical documents (< 2 seconds)
  - Memory usage constraints
  - Handling of large files (> 10MB markdown)
  - Lazy loading strategies for long documents
  
- **TR-4**: Error handling
  - Invalid markdown syntax handling
  - Mermaid diagram syntax errors
  - Missing image/media file handling
  - Network issues (if Mermaid.js loaded from CDN)

### 4. UI/UX Requirements
- **UX-1**: Layout and positioning
  - Where the preview pane appears (side-by-side, tabbed, or toggleable)
  - Responsive sizing and resizing behavior
  - Minimum/maximum pane sizes
  
- **UX-2**: Visual design
  - Styling consistency with existing GUI theme
  - Dark/light mode support (if applicable)
  - Font selection and sizing
  - Color scheme for code blocks and syntax highlighting
  
- **UX-3**: User feedback
  - Loading indicators during preview generation
  - Error messages for rendering failures
  - Status indicators for preview state (up-to-date, outdated, error)

### 5. Implementation Phases
Break down implementation into logical phases:
- **Phase 1**: Basic markdown rendering (MVP)
- **Phase 2**: Mermaid.js integration
- **Phase 3**: Advanced features (file watching, export, etc.)

### 6. Testing Requirements
- Unit tests for markdown parsing
- Unit tests for Mermaid diagram detection
- Integration tests for viewer component
- UI tests for preview functionality
- Performance tests for large files
- Cross-platform compatibility tests

### 7. Documentation Requirements
- User documentation updates
- Developer documentation for the new component
- API documentation for public interfaces

### 8. Acceptance Criteria
- Clear, testable criteria for feature completion
- Performance benchmarks
- Browser compatibility (if using web view)

### 9. Risks and Mitigations
- Technical risks (JavaScript execution in Qt, performance, security)
- Mitigation strategies for each identified risk

### 10. Future Enhancements
- Optional features for future iterations
- Extensibility considerations

## Format

The requirements document must be structured as a **comprehensive technical specification** suitable for a software developer. Use the following format:

**Document Structure:**
- Use Markdown format (.md file)
- Include a table of contents
- Use clear section headings with hierarchical numbering
- Include code examples where relevant
- Use diagrams (Mermaid.js syntax) to illustrate architecture and workflows
- Include tables for requirements traceability
- Add appendices for reference materials

**Writing Style:**
- **Technical and precise** - Use technical terminology appropriate for Python/Qt developers
- **Actionable** - Each requirement should be implementable without ambiguity
- **Comprehensive** - Cover all aspects from high-level design to low-level implementation details
- **Well-organized** - Use consistent formatting and clear structure
- **Reference existing code** - Reference existing md2office codebase structure and patterns where relevant

**Code Examples:**
- Include Python code snippets showing expected class structures
- Show Qt widget integration examples
- Provide Mermaid.js usage examples
- Include configuration examples

**Diagrams:**
- Use Mermaid.js syntax for:
  - Component architecture diagrams
  - Data flow diagrams
  - User interaction flowcharts
  - Class relationship diagrams

**Tables:**
- Requirements traceability matrix
- Dependency version table
- Performance benchmarks table
- Browser/Platform compatibility matrix

**Appendices:**
- Reference links to Mermaid.js documentation
- Reference links to Qt QWebEngineView documentation
- Example markdown files with Mermaid diagrams
- Example rendered outputs

**File Naming:**
The document should be named: `markdown-viewer-mermaid-requirements.md`

**Length:**
The document should be comprehensive but focused - approximately 15-25 pages when rendered, covering all necessary details without excessive verbosity.

---

**Output:** Generate a complete requirements document following the CTF structure above, ready for a programmer to implement the markdown viewer with Mermaid.js support in the md2office application.

