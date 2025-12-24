# Copilot Markdown to Office Document Converter

## Purpose

This recipe creates a comprehensive specification and implementation plan for a portable CLI tool that converts Microsoft Copilot-generated markdown documents into Microsoft Word (.docx), PowerPoint (.pptx), and optionally PDF formats. The tool will be distributed as a self-contained binary executable that works on Windows and Mac without installation or external dependencies. This enables users to transform AI-generated markdown content into professional business documents and presentations, making Copilot-generated content accessible to stakeholders who require standard Office formats. The recipe produces detailed technical specifications, conversion mappings, CLI design, cross-platform build strategies, and quality assurance frameworks that guide the development of a production-ready conversion tool.

## Personas

Markdown Parser Specialist: Analyzes Microsoft Copilot-generated markdown syntax, structure, and formatting conventions. Identifies Copilot-specific markdown features and extensions that differ from standard markdown. Creates a comprehensive markdown structure analysis document that maps all markdown elements and their characteristics. Produces markdown-analysis.md early in the recipe to inform conversion strategies.

Document Structure Architect: Designs the overall conversion strategy and mapping rules from markdown elements to target document formats. Creates structural mappings that define how markdown headings, lists, tables, and other elements translate to Word, PowerPoint, and PDF structures. Produces conversion-architecture.md and structural-mapping-specification.md that serve as the foundation for format-specific implementations.

Word Document Specialist: Expert in Microsoft Word (.docx) format, document structure, and Word styling conventions. Designs how markdown elements map to Word document elements including heading styles, list formatting, table structures, and code block presentation. Creates word-conversion-specification.md that details the complete mapping from markdown to Word format with styling guidelines.

PowerPoint Specialist: Expert in Microsoft PowerPoint (.pptx) format, slide design, and presentation layouts. Determines how markdown content should be structured into slides based on heading hierarchy and content types. Designs slide layout strategies, bullet point handling, and visual presentation approaches. Produces powerpoint-conversion-specification.md with slide mapping rules and layout guidelines.

PDF Generation Specialist: Expert in PDF format creation, layout preservation, and PDF standards. Handles PDF conversion requirements including formatting preservation, image embedding, and document structure. Creates pdf-conversion-specification.md that defines PDF generation approach, layout strategies, and formatting rules. Note: PDF support is optional based on user requirements.

Styling and Formatting Expert: Handles visual design, formatting rules, and styling consistency across all output formats. Ensures professional appearance and consistent visual presentation. Defines color schemes, fonts, spacing, and visual hierarchy. Produces styling-guide.md and formatting-specification.md that ensure consistent output quality across all formats.

Image and Media Handler: Manages embedded images, media files, and their integration into output documents. Handles image optimization, placement strategies, and media file processing requirements. Defines how images are embedded, resized, and positioned in each output format. Produces media-handling-specification.md with image processing rules and media integration guidelines.

CLI and Cross-Platform Build Specialist: Designs the command-line interface, user experience, and command syntax for the conversion tool. Handles cross-platform binary compilation strategies for Windows and Mac, ensuring the tool is portable and self-contained with all dependencies bundled. Creates cli-design-specification.md and cross-platform-build-guide.md that define the CLI interface and build process.

Quality Assurance Tester: Validates conversion accuracy, tests edge cases, and ensures output quality matches source markdown. Creates comprehensive test cases covering various markdown structures, edge cases, and format-specific scenarios. Produces test-suite-specification.md and quality-assurance-plan.md that ensure robust testing coverage.

Recipe Manager: Ensures all personas complete their work successfully. Tracks completion status and deadlines. Creates summary reports and status dashboards. Coordinates communication between personas. Generates artifacts in the recipe-analysis-report folder including project-status-dashboard.md and recipe-summary-report.md.

Recipe Analyst: Analyzes all artifacts and creates comprehensive reports identifying contradictions between artifacts. Identifies trends and insights across conversion specifications. Performs gap analysis to identify missing elements or unaddressed requirements. Creates quality metrics and completeness scoring for all artifacts. Generates risk assessment reports with mitigation strategies. Produces prioritized recommendations with implementation roadmaps. Generates artifacts in the recipe-analysis-report folder including gap-analysis-report.md and quality-assessment-report.md.

## Sequence

1. Markdown Parser Specialist analyzes Microsoft Copilot markdown structure and syntax - Analyzes Copilot-generated markdown to identify all markdown elements, syntax patterns, and Copilot-specific features. Documents markdown structure, formatting conventions, and any extensions or variations from standard markdown. Produces markdown-analysis.md.

2. Document Structure Architect designs conversion architecture and structural mappings - Uses markdown-analysis.md to design the overall conversion strategy. Creates structural mappings that define how markdown elements translate to Word, PowerPoint, and PDF document structures. Establishes conversion rules and architectural patterns. Produces conversion-architecture.md and structural-mapping-specification.md.

3. Word Document Specialist creates Word conversion specification - Uses conversion-architecture.md and structural-mapping-specification.md to design detailed Word (.docx) conversion mappings. Defines how markdown elements map to Word document elements, heading styles, list formatting, table structures, and code block presentation. Produces word-conversion-specification.md.

4. PowerPoint Specialist creates PowerPoint conversion specification - Uses conversion-architecture.md and structural-mapping-specification.md to design PowerPoint (.pptx) conversion strategy. Determines how markdown content structures into slides based on heading hierarchy. Designs slide layouts, bullet point handling, and visual presentation approaches. Produces powerpoint-conversion-specification.md.

5. PDF Generation Specialist creates PDF conversion specification - Uses conversion-architecture.md and structural-mapping-specification.md to design PDF conversion approach. Defines PDF generation strategies, layout preservation methods, and formatting rules. Produces pdf-conversion-specification.md. Note: This step may be marked as optional based on user requirements.

6. Styling and Formatting Expert creates styling and formatting specifications - Reviews word-conversion-specification.md, powerpoint-conversion-specification.md, and pdf-conversion-specification.md to ensure consistent visual design across all formats. Defines color schemes, fonts, spacing, visual hierarchy, and formatting rules. Produces styling-guide.md and formatting-specification.md.

7. Image and Media Handler creates media handling specification - Uses markdown-analysis.md and all conversion specifications to define image and media processing requirements. Specifies how images are embedded, optimized, resized, and positioned in each output format. Produces media-handling-specification.md.

8. CLI and Cross-Platform Build Specialist creates CLI design and build specifications - Uses all conversion specifications to design the command-line interface. Defines command syntax, flags, options, and user experience. Creates cross-platform build strategy for Windows and Mac portable binaries. Produces cli-design-specification.md and cross-platform-build-guide.md.

9. Quality Assurance Tester creates test suite and QA plan - Reviews all conversion specifications and CLI design to create comprehensive test cases. Defines test scenarios covering various markdown structures, edge cases, and format-specific validation requirements. Produces test-suite-specification.md and quality-assurance-plan.md.

10. Recipe Manager compiles summary report and status dashboard - Reviews all artifacts generated by previous personas. Creates executive summary compiling main information from each artifact. Generates project status dashboard showing overall recipe progress and completion status. Produces recipe-analysis-report/project-status-dashboard.md and recipe-analysis-report/recipe-summary-report.md.

11. Recipe Analyst performs gap analysis and quality assessment - Analyzes all artifacts for contradictions, missing elements, and quality issues. Identifies trends and insights across conversion specifications. Performs gap analysis to identify unaddressed requirements. Creates quality metrics and completeness scoring. Generates risk assessment with mitigation strategies. Produces prioritized recommendations with implementation roadmaps. Produces recipe-analysis-report/gap-analysis-report.md and recipe-analysis-report/quality-assessment-report.md.

