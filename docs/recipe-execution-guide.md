# Recipe Execution Guide

This guide provides instructions for an LLM to execute the Copilot Markdown to Office Document Converter recipe. Follow these steps sequentially to execute all personas and generate all required artifacts.

## Overview

You are executing a multi-persona recipe that creates comprehensive specifications for a portable CLI tool converting Microsoft Copilot-generated markdown documents into Word, PowerPoint, and PDF formats. The recipe consists of 11 personas working in sequence, each generating specific artifacts that build upon previous work.

## Execution Context

- **Recipe Location**: `recipes/copilot-markdown-to-office-document-converter/`
- **Artifacts Folder**: `artifacts/` (at the same level as `personas/`)
- **Recipe Analysis Reports**: `artifacts/recipe-analysis-report/` (subfolder for Recipe Manager and Recipe Analyst outputs)
- **Persona Files**: `personas/` directory contains 11 persona specification files

## Execution Instructions

### Pre-Execution Setup

1. **Verify directory structure**:
   - Confirm `artifacts/` folder exists
   - Confirm `personas/` folder exists with all 11 persona files
   - Confirm `artifacts/recipe-definition.md` and `artifacts/recipe-requirements.md` exist

2. **Create recipe-analysis-report subfolder** (if it doesn't exist):
   - Create `artifacts/recipe-analysis-report/` directory for Recipe Manager and Recipe Analyst outputs

### Execution Sequence

Execute each persona in the exact order specified below. Read the persona file, execute the instructions, and generate the required output artifacts before proceeding to the next persona.

#### Step 1: Markdown Parser Specialist

**Persona File**: `personas/01-markdown-parser-specialist.md`

**Actions**:
1. Read `personas/01-markdown-parser-specialist.md` to understand the persona's role and instructions
2. Read `artifacts/recipe-definition.md` and `artifacts/recipe-requirements.md` for context
3. Execute the persona's instructions to analyze Microsoft Copilot markdown structure
4. Generate `artifacts/markdown-analysis.md` with comprehensive markdown structure analysis

**Verification**: Confirm `artifacts/markdown-analysis.md` exists and contains markdown structure analysis

#### Step 2: Document Structure Architect

**Persona File**: `personas/02-document-structure-architect.md`

**Actions**:
1. Read `personas/02-document-structure-architect.md` to understand the persona's role and instructions
2. Read `artifacts/markdown-analysis.md` (from Step 1) as input
3. Execute the persona's instructions to design conversion architecture
4. Generate `artifacts/conversion-architecture.md` with overall conversion strategy
5. Generate `artifacts/structural-mapping-specification.md` with detailed structural mappings

**Verification**: Confirm both `artifacts/conversion-architecture.md` and `artifacts/structural-mapping-specification.md` exist

#### Step 3: Word Document Specialist

**Persona File**: `personas/03-word-document-specialist.md`

**Actions**:
1. Read `personas/03-word-document-specialist.md` to understand the persona's role and instructions
2. Read `artifacts/conversion-architecture.md` and `artifacts/structural-mapping-specification.md` (from Step 2) as inputs
3. Execute the persona's instructions to design Word conversion specification
4. Generate `artifacts/word-conversion-specification.md` with complete Word conversion mappings

**Verification**: Confirm `artifacts/word-conversion-specification.md` exists

#### Step 4: PowerPoint Specialist

**Persona File**: `personas/04-powerpoint-specialist.md`

**Actions**:
1. Read `personas/04-powerpoint-specialist.md` to understand the persona's role and instructions
2. Read `artifacts/conversion-architecture.md` and `artifacts/structural-mapping-specification.md` (from Step 2) as inputs
3. Execute the persona's instructions to design PowerPoint conversion specification
4. Generate `artifacts/powerpoint-conversion-specification.md` with complete PowerPoint conversion strategy

**Verification**: Confirm `artifacts/powerpoint-conversion-specification.md` exists

#### Step 5: PDF Generation Specialist

**Persona File**: `personas/05-pdf-generation-specialist.md`

**Actions**:
1. Read `personas/05-pdf-generation-specialist.md` to understand the persona's role and instructions
2. Read `artifacts/conversion-architecture.md` and `artifacts/structural-mapping-specification.md` (from Step 2) as inputs
3. Execute the persona's instructions to design PDF conversion specification
4. Generate `artifacts/pdf-conversion-specification.md` with complete PDF conversion approach

**Note**: PDF support is optional based on user requirements, but create a complete specification.

**Verification**: Confirm `artifacts/pdf-conversion-specification.md` exists

#### Step 6: Styling and Formatting Expert

**Persona File**: `personas/06-styling-and-formatting-expert.md`

**Actions**:
1. Read `personas/06-styling-and-formatting-expert.md` to understand the persona's role and instructions
2. Read `artifacts/word-conversion-specification.md`, `artifacts/powerpoint-conversion-specification.md`, and `artifacts/pdf-conversion-specification.md` (from Steps 3-5) as inputs
3. Execute the persona's instructions to ensure consistent styling across formats
4. Generate `artifacts/styling-guide.md` with comprehensive styling system
5. Generate `artifacts/formatting-specification.md` with detailed formatting rules

**Verification**: Confirm both `artifacts/styling-guide.md` and `artifacts/formatting-specification.md` exist

#### Step 7: Image and Media Handler

**Persona File**: `personas/07-image-and-media-handler.md`

**Actions**:
1. Read `personas/07-image-and-media-handler.md` to understand the persona's role and instructions
2. Read `artifacts/markdown-analysis.md` (from Step 1) and all conversion specifications (from Steps 3-5) as inputs
3. Execute the persona's instructions to define media handling requirements
4. Generate `artifacts/media-handling-specification.md` with image and media processing rules

**Verification**: Confirm `artifacts/media-handling-specification.md` exists

#### Step 8: CLI and Cross-Platform Build Specialist

**Persona File**: `personas/08-cli-and-cross-platform-build-specialist.md`

**Actions**:
1. Read `personas/08-cli-and-cross-platform-build-specialist.md` to understand the persona's role and instructions
2. Read all conversion specifications (from Steps 3-5) as inputs
3. Execute the persona's instructions to design CLI interface and build strategy
4. Generate `artifacts/cli-design-specification.md` with complete CLI design
5. Generate `artifacts/cross-platform-build-guide.md` with build strategy for Windows and Mac

**Verification**: Confirm both `artifacts/cli-design-specification.md` and `artifacts/cross-platform-build-guide.md` exist

#### Step 9: Quality Assurance Tester

**Persona File**: `personas/09-quality-assurance-tester.md`

**Actions**:
1. Read `personas/09-quality-assurance-tester.md` to understand the persona's role and instructions
2. Read all conversion specifications and `artifacts/cli-design-specification.md` (from previous steps) as inputs
3. Execute the persona's instructions to create comprehensive test cases
4. Generate `artifacts/test-suite-specification.md` with test cases
5. Generate `artifacts/quality-assurance-plan.md` with QA strategy

**Verification**: Confirm both `artifacts/test-suite-specification.md` and `artifacts/quality-assurance-plan.md` exist

#### Step 10: Recipe Manager

**Persona File**: `personas/10-recipe-manager.md`

**Actions**:
1. Read `personas/10-recipe-manager.md` to understand the persona's role and instructions
2. Read `artifacts/recipe-definition.md` and review ALL artifacts generated by previous personas (Steps 1-9)
3. Execute the persona's instructions to compile summary reports
4. Generate `artifacts/recipe-analysis-report/project-status-dashboard.md` with project status
5. Generate `artifacts/recipe-analysis-report/recipe-summary-report.md` with executive summary

**Critical**: Recipe Manager outputs MUST be written to `artifacts/recipe-analysis-report/` subfolder, not directly to `artifacts/`.

**Verification**: Confirm both files exist in `artifacts/recipe-analysis-report/` folder

#### Step 11: Recipe Analyst

**Persona File**: `personas/11-recipe-analyst.md`

**Actions**:
1. Read `personas/11-recipe-analyst.md` to understand the persona's role and instructions
2. Read `artifacts/recipe-definition.md` and review ALL artifacts generated by ALL previous personas (Steps 1-10)
3. Read Recipe Manager reports: `artifacts/recipe-analysis-report/project-status-dashboard.md` and `artifacts/recipe-analysis-report/recipe-summary-report.md`
4. Execute the persona's instructions to perform comprehensive analysis
5. Generate `artifacts/recipe-analysis-report/gap-analysis-report.md` with gap analysis
6. Generate `artifacts/recipe-analysis-report/quality-assessment-report.md` with quality metrics, risk assessment, and recommendations

**Critical**: Recipe Analyst outputs MUST be written to `artifacts/recipe-analysis-report/` subfolder, not directly to `artifacts/`.

**Verification**: Confirm both files exist in `artifacts/recipe-analysis-report/` folder

## Post-Execution Verification

After completing all 11 steps, verify:

1. **All artifacts exist**:
   - `artifacts/markdown-analysis.md`
   - `artifacts/conversion-architecture.md`
   - `artifacts/structural-mapping-specification.md`
   - `artifacts/word-conversion-specification.md`
   - `artifacts/powerpoint-conversion-specification.md`
   - `artifacts/pdf-conversion-specification.md`
   - `artifacts/styling-guide.md`
   - `artifacts/formatting-specification.md`
   - `artifacts/media-handling-specification.md`
   - `artifacts/cli-design-specification.md`
   - `artifacts/cross-platform-build-guide.md`
   - `artifacts/test-suite-specification.md`
   - `artifacts/quality-assurance-plan.md`

2. **Recipe analysis reports exist**:
   - `artifacts/recipe-analysis-report/project-status-dashboard.md`
   - `artifacts/recipe-analysis-report/recipe-summary-report.md`
   - `artifacts/recipe-analysis-report/gap-analysis-report.md`
   - `artifacts/recipe-analysis-report/quality-assessment-report.md`

3. **File locations are correct**:
   - Standard persona artifacts are in `artifacts/` folder
   - Recipe Manager and Recipe Analyst artifacts are in `artifacts/recipe-analysis-report/` subfolder

## Important Notes

- **Execute personas sequentially**: Do not skip steps or execute out of order
- **Read input files**: Always read the required input files before generating outputs
- **File paths**: Use relative paths (`artifacts/...`) not absolute paths
- **Recipe Manager/Analyst**: Their outputs go to `artifacts/recipe-analysis-report/` subfolder
- **Quality**: Generate comprehensive, detailed artifacts following each persona's instructions
- **Definition of Done**: Check each persona's "Definition of Done" checklist before proceeding

## User Instructions

To execute this recipe, ask your LLM to:
1. Read this execution guide (`recipe-execution-guide.md`)
2. Execute all 11 personas in sequence following the instructions above
3. Generate all required artifacts in the correct locations
4. Verify completion using the post-execution verification checklist

The LLM should execute this guide automatically without requiring manual intervention for each persona step.

