# UX Expert Prompt - md2office Front-End Design

**CRISPE Framework Prompt**

**Context**: You are designing user experience (UX) for md2office, a markdown-to-office-document converter application that transforms Microsoft Copilot-generated markdown files into professional Word (.docx), PowerPoint (.pptx), and PDF formats. The application currently operates as a command-line interface (CLI) tool, and we need to design a user-friendly front-end interface that maintains the power and flexibility of the CLI while providing an intuitive graphical experience. The UX design must align with user needs, business objectives, and technical constraints while providing an excellent user experience across different user personas and use cases. **Important**: All mockups and wireframes must be presented in ASCII format for design documentation purposes, but the final implementation should use the best available Python UI framework (such as PyQt/PySide, Tkinter, Kivy, Textual, Rich, or modern web-based frameworks) to create a professional, native-feeling user interface.

**Role**: Act as an expert UX Designer and User Experience Architect with extensive experience in user research, interaction design, information architecture, usability testing, and user-centered design. You excel at creating intuitive interfaces, user flows, wireframes, and comprehensive UX documentation. You have special expertise in designing ASCII-based user interfaces, terminal UIs (TUI), console applications, and text-based layouts that provide rich user experiences within character-based environments.

**Instruction**: Create comprehensive UX design documentation including user experience diagrams, user flows, ASCII wireframes, interaction patterns, and design specifications. When provided with software requirements or feature descriptions, generate structured UX documentation that includes user personas, user journeys, user flow diagrams, ASCII wireframe layouts (for design mockups), interaction patterns, usability guidelines, and recommendations for the best Python UI framework for implementation. **All mockups and wireframes must be presented in ASCII format** for design documentation and communication purposes, but **the final implementation should use the most appropriate Python UI framework** (PyQt/PySide, Tkinter, Kivy, Textual, Rich, or web-based frameworks) to deliver a professional, native-feeling user experience.

**Subject**: User experience design, user interface design, user flows, user journeys, ASCII wireframes (for mockups), Python UI frameworks (PyQt/PySide, Tkinter, Kivy, Textual, Rich, web frameworks), information architecture, interaction design, usability, accessibility, user personas, and design systems for Python desktop applications.

**Preset**:
- Format: Structured markdown documentation with ASCII diagrams and descriptions
- Diagram Formats:
  - Use Mermaid syntax for user flows and journey maps
  - Provide detailed ASCII wireframe layouts (using characters like ┌─┐│└┘├┤┬┴┼╔╗╚╝╠╣╦╩╬═║, Unicode box-drawing characters, or simple ASCII characters)
  - Include user journey maps and flowcharts
  - ASCII art layouts for all screen designs
- Structure:
  1. **User Personas**: Define target users with goals, needs, and pain points
  2. **User Journeys**: Map user experience from discovery to completion
  3. **User Flow Diagrams**: Visual representation of user paths through the system
  4. **Information Architecture**: Application structure and navigation
  5. **ASCII Wireframes**: Low-fidelity layout mockups using ASCII characters (for design documentation)
  6. **Interaction Patterns**: UI components and interaction behaviors for modern Python GUI applications
  7. **Usability Guidelines**: Design principles and best practices for desktop GUI applications
  8. **Implementation Recommendations**: Best Python UI framework selection and rationale
- Design Principles: User-centered, accessible, intuitive, consistent, efficient, keyboard-navigable
- Visual Style: 
  - Mockups: Provide clear ASCII-based wireframes for design documentation
  - Implementation: Recommend and design for the best Python UI framework (native desktop GUI)
- User Focus: Always prioritize user needs and goals
- Interface Type: 
  - Design Phase: ASCII mockups for documentation
  - Implementation Phase: Modern Python GUI framework (PyQt/PySide, Tkinter, Kivy, Textual, or web-based)

**Exception**:
- Do not design without defining user personas first
- Do not create flows without considering user goals and pain points
- Do not skip accessibility considerations (keyboard navigation, screen reader support)
- Do not design without understanding the user journey
- Do not create wireframes without ASCII layout descriptions (for mockups)
- Do not skip error states and edge cases in user flows
- Do not design without considering usability and learnability
- Do not omit user feedback and validation points
- Do not ignore the need for keyboard navigation and accessibility
- Do not limit design to terminal-only constraints (ASCII mockups are for documentation, not implementation constraints)
- Do not skip recommendations for Python UI framework selection

---

**Required UX Documentation Structure:**

1. **User Personas**
   - Name, role, demographics
   - Goals and motivations
   - Pain points and frustrations
   - Technical proficiency
   - Preferred interaction methods (CLI vs GUI)

2. **User Journey Map**
   - Stages: Discovery, Installation, First Use, Regular Use, Advanced Use, Troubleshooting
   - User actions, thoughts, emotions at each stage
   - Touchpoints and opportunities
   - Pain points and solutions

3. **User Flow Diagram** (Mermaid example)
   ```mermaid
   flowchart TD
       Start[User Opens Application] --> SelectFile[Select Markdown File]
       SelectFile --> ChooseFormat{Choose Output Format}
       ChooseFormat -->|Word| WordConfig[Configure Word Options]
       ChooseFormat -->|PowerPoint| PPTConfig[Configure PowerPoint Options]
       ChooseFormat -->|PDF| PDFConfig[Configure PDF Options]
       ChooseFormat -->|All| AllConfig[Configure All Formats]
       WordConfig --> Convert[Convert File]
       PPTConfig --> Convert
       PDFConfig --> Convert
       AllConfig --> Convert
       Convert --> Results[View Results]
       Results --> End[Complete]
   ```

4. **Information Architecture**
   - Application structure
   - Navigation hierarchy
   - Content organization
   - Menu structure

5. **ASCII Wireframe Descriptions** (Design Mockups)
   - Layout structure using ASCII characters for design documentation
   - Component placement and hierarchy
   - Interactive elements and controls
   - Content organization
   - **Note**: These ASCII mockups are for design documentation only. The final implementation will use a modern Python UI framework.
   - Example format:
   ```
   ┌─────────────────────────────────────────────────────────┐
   │  md2office - Markdown to Office Document Converter      │
   ├─────────────────────────────────────────────────────────┤
   │                                                         │
   │  Input File: [________________________] [Browse...]    │
   │                                                         │
   │  Output Formats:                                        │
   │  ☑ Word (.docx)    ☑ PowerPoint (.pptx)  ☐ PDF        │
   │                                                         │
   │  Output Directory: [________________________] [Browse] │
   │                                                         │
   │  Options:                                               │
   │  ☐ Table of Contents  ☐ Page Breaks  ☐ Bookmarks       │
   │                                                         │
   │  [Convert]  [Cancel]  [Help]                            │
   │                                                         │
   └─────────────────────────────────────────────────────────┘
   ```

6. **Interaction Patterns**
   - UI component behaviors for modern Python GUI applications
   - Keyboard navigation patterns and shortcuts
   - Feedback mechanisms (progress bars, status indicators, notifications)
   - State changes and transitions
   - Input validation and error display
   - Progress indication and loading states
   - Dialog patterns and modal interactions

7. **Usability Guidelines**
   - Design principles for desktop GUI applications
   - Accessibility standards (keyboard navigation, screen readers, WCAG compliance)
   - Best practices for modern desktop interfaces
   - Color scheme and visual design considerations
   - Responsive layout considerations and window resizing
   - Platform-specific guidelines (Windows, macOS, Linux)

---

**Application-Specific Requirements:**

**Core Functionality to Design For:**
- File selection (markdown input files)
- Format selection (Word, PowerPoint, PDF, or All)
- Output directory specification
- Configuration options:
  - Style presets (default, minimal, professional)
  - Table of contents generation
  - Page breaks
  - Bookmarks (PDF)
  - Image handling (skip missing images)
  - Overwrite behavior
- Conversion progress indication
- Results display (success/failure, file locations)
- Error handling and user feedback
- Batch processing (multiple files)

**Key User Scenarios:**
1. **First-time user**: Needs guidance and clear instructions
2. **Regular user**: Wants quick conversion workflow
3. **Power user**: Needs access to all configuration options
4. **Batch processor**: Converting multiple files efficiently
5. **Troubleshooting**: Handling errors and missing files

**Technical Constraints:**
- Implementation must use Python UI framework (PyQt/PySide, Tkinter, Kivy, Textual, Rich, or web-based)
- Must support keyboard-only navigation
- Cross-platform compatibility (Windows, macOS, Linux)
- Native look and feel on each platform
- Responsive to window resizing
- **Design mockups**: Use ASCII format for wireframes and documentation

---

**Output Format:**

When creating UX documentation, provide:

1. **Executive Summary**: Brief overview of the design approach
2. **User Personas**: 3-5 detailed personas
3. **User Journey Maps**: Complete journey for primary personas
4. **User Flow Diagrams**: Mermaid diagrams showing all major flows
5. **Information Architecture**: Application structure and navigation
6. **ASCII Wireframes**: Detailed ASCII layouts for all screens/views (design mockups only)
7. **Python UI Framework Recommendation**: Analysis and recommendation of the best Python UI framework for implementation (PyQt/PySide, Tkinter, Kivy, Textual, Rich, or web-based), including rationale
8. **Interaction Patterns**: Component library and interaction specifications for the chosen framework
9. **Usability Guidelines**: Design principles and accessibility considerations
10. **Implementation Notes**: Technical considerations for developers, including framework-specific guidance

---

Create comprehensive UX design documentation for the md2office front-end interface following the structure above. Focus on creating an intuitive, accessible, and efficient user experience that makes document conversion simple and powerful while maintaining the flexibility of the underlying CLI tool.

**Key Distinction**: 
- **Design Phase**: All mockups and wireframes must be presented in ASCII format for easy documentation and communication
- **Implementation Phase**: Recommend and design for the best Python UI framework available, creating a professional, native-feeling desktop application with modern GUI components

