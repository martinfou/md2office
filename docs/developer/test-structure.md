# Test Structure Documentation

This document describes the test structure for the md2office project, including current test coverage and recommendations for test organization.

See also: [Test Coverage](test-coverage.md) for coverage requirements and verification.

## Current Test Structure

```
tests/
├── __init__.py
├── test_cli.py              # CLI interface tests
├── test_gui.py               # GUI interface tests
├── test_pdf_generator.py     # PDF generator tests
├── test_powerpoint_generator.py  # PowerPoint generator tests
└── test_word_generator.py    # Word generator tests
```

## Test Coverage by Module

### ✅ Covered Modules

| Module | Test File | Status |
|--------|-----------|--------|
| CLI | `test_cli.py` | ✅ Covered |
| GUI | `test_gui.py` | ✅ Covered |
| PDF Generator | `test_pdf_generator.py` | ✅ Covered |
| PowerPoint Generator | `test_powerpoint_generator.py` | ✅ Covered |
| Word Generator | `test_word_generator.py` | ✅ Covered |

### ⚠️ Missing Test Coverage

| Module | Recommended Test File | Priority |
|--------|----------------------|----------|
| Parser | `test_parser.py` | High |
| Router | `test_router.py` | High |
| Styling | `test_styling.py` | Medium |
| Config | `test_config.py` | Medium |
| Errors | `test_errors.py` | Medium |

## Source Code Structure

```
src/md2office/
├── cli/              # ✅ test_cli.py
├── gui/              # ✅ test_gui.py
├── parser/           # ⚠️ Missing: test_parser.py
├── router/           # ⚠️ Missing: test_router.py
├── generators/       # ✅ test_*_generator.py (partial)
│   ├── word_generator.py      # ✅ test_word_generator.py
│   ├── powerpoint_generator.py # ✅ test_powerpoint_generator.py
│   ├── pdf_generator.py       # ✅ test_pdf_generator.py
│   └── inline_formatter.py    # ⚠️ No dedicated tests
├── styling/          # ⚠️ Missing: test_styling.py
├── config/           # ⚠️ Missing: test_config.py
└── errors/           # ⚠️ Missing: test_errors.py
```

## Recommended Test Organization

### Test File Naming Convention

- Test files should mirror source structure: `test_<module>.py`
- Test classes: `Test<ClassName>`
- Test functions: `test_<function_name>`

### Test Categories

Tests should be organized by category using pytest markers:

- `@pytest.mark.unit` - Unit tests for individual components
- `@pytest.mark.integration` - Integration tests for component interactions
- `@pytest.mark.slow` - Tests that take significant time
- `@pytest.mark.requires_docx` - Tests requiring python-docx
- `@pytest.mark.requires_pptx` - Tests requiring python-pptx
- `@pytest.mark.requires_pdf` - Tests requiring reportlab

## Priority Test Additions

### High Priority

1. **`test_parser.py`** - Markdown parsing is core functionality
   - Test AST building
   - Test markdown element parsing
   - Test edge cases and error handling

2. **`test_router.py`** - Content routing is critical
   - Test pipeline execution
   - Test content routing logic
   - Test format-specific routing

### Medium Priority

3. **`test_styling.py`** - Styling affects output quality
   - Test style application
   - Test style presets
   - Test style inheritance

4. **`test_config.py`** - Configuration affects behavior
   - Test config loading
   - Test config merging
   - Test config validation

5. **`test_errors.py`** - Error handling is important
   - Test exception types
   - Test error messages
   - Test error context

## Test Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
    "--tb=short",
    "--cov=md2office",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-report=xml",
    "--cov-fail-under=80",
    "--durations=10",
]
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=md2office --cov-report=html

# Run specific test file
pytest tests/test_cli.py

# Run specific test
pytest tests/test_cli.py::test_cli_basic_conversion

# Run by marker
pytest -m unit
pytest -m "not slow"
```

## Test Coverage Goals

- **Current Target:** 80% coverage (configured in pytest)
- **Long-term Goal:** 90%+ coverage
- **Critical Modules:** 95%+ coverage (parser, router, generators)

## Test Data

Test fixtures and sample data should be organized:

```
tests/
├── fixtures/          # Test fixtures (if needed)
│   └── sample.md
└── data/              # Test data files
    ├── sample.md
    └── edge_cases/
```

## Integration with CI/CD

Tests should run automatically in CI/CD pipeline:

- Run on every commit
- Run on pull requests
- Fail build if coverage drops below threshold
- Generate coverage reports

## Best Practices

1. **Isolation:** Each test should be independent
2. **Fixtures:** Use pytest fixtures for common setup
3. **Mocking:** Mock external dependencies (file I/O, network)
4. **Naming:** Use descriptive test names
5. **Documentation:** Document complex test scenarios
6. **Edge Cases:** Test edge cases and error conditions

## Next Steps

1. Create `test_parser.py` with comprehensive parser tests
2. Create `test_router.py` with pipeline and routing tests
3. Add tests for styling, config, and errors modules
4. Increase test coverage to meet 80% threshold
5. Add integration tests for end-to-end workflows

