# Test Coverage

This document describes the test coverage requirements and verification for the md2office project.

## Coverage Configuration

### Threshold

The project requires **minimum 80% code coverage** for all tests.

**Configuration Location:** `pyproject.toml`
```toml
[tool.pytest.ini_options]
addopts = [
    ...
    "--cov-fail-under=80",
]
```

### What This Means

- Tests must achieve at least 80% code coverage
- If coverage falls below 80%, pytest will fail
- This ensures code quality and reduces regression risk

## Running Tests with Coverage

### Basic Coverage Report

```bash
# Run tests with coverage
pytest --cov=md2office --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=md2office --cov-report=html

# View HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage Reports

Coverage reports are generated in multiple formats:

1. **Terminal Output** (`--cov-report=term-missing`)
   - Shows coverage percentage per module
   - Highlights missing lines

2. **HTML Report** (`--cov-report=html`)
   - Generated in `htmlcov/` directory
   - Interactive browser-based report
   - Shows line-by-line coverage

3. **XML Report** (`--cov-report=xml`)
   - Generated as `coverage.xml`
   - Used by CI/CD tools and IDEs

## Coverage Verification

### Manual Verification

To verify coverage meets the threshold:

```bash
# Run tests - will fail if coverage < 80%
pytest

# Check coverage percentage
pytest --cov=md2office --cov-report=term | grep TOTAL
```

### CI/CD Integration

If CI/CD is configured, coverage verification should:

1. Run tests with coverage: `pytest --cov=md2office`
2. Fail the build if coverage < 80% (automatic via `--cov-fail-under=80`)
3. Upload coverage reports for review

**Example CI Configuration:**
```yaml
- name: Run tests with coverage
  run: pytest --cov=md2office --cov-report=xml --cov-report=html

- name: Check coverage threshold
  run: pytest --cov=md2office --cov-fail-under=80
```

## Coverage Goals

### Current Target
- **Minimum:** 80% overall coverage
- **Enforced:** Yes (via pytest configuration)

### Module-Specific Goals
- **Critical Modules:** 95%+ coverage
  - Parser (`md2office.parser`)
  - Router (`md2office.router`)
  - Generators (`md2office.generators`)
- **Supporting Modules:** 80%+ coverage
  - Configuration (`md2office.config`)
  - Error handling (`md2office.errors`)
  - Styling (`md2office.styling`)

### Long-term Goal
- **Target:** 90%+ overall coverage
- **Timeline:** Future release

## Improving Coverage

### Finding Gaps

1. **Generate HTML Report:**
   ```bash
   pytest --cov=md2office --cov-report=html
   ```

2. **Open `htmlcov/index.html`** in browser

3. **Review Red Lines:**
   - Red lines = not covered by tests
   - Yellow lines = partially covered

### Adding Tests

Focus on:
- Edge cases
- Error handling paths
- Boundary conditions
- Integration scenarios

### Excluding Code from Coverage

Sometimes code should be excluded from coverage:

```python
# pragma: no cover
def debug_function():
    """Only used during development."""
    pass
```

Or configure in `pyproject.toml`:
```toml
[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "if __name__ == .__main__.:",
]
```

## Coverage Reports Location

- **HTML Reports:** `htmlcov/` (gitignored)
- **XML Reports:** `coverage.xml` (gitignored)
- **Terminal Output:** Displayed during test run

**Note:** Coverage reports are excluded from git (see `.gitignore`).

## Troubleshooting

### Coverage Not Meeting Threshold

**Problem:** Tests fail with "Coverage too low" error

**Solutions:**
1. Review coverage report: `pytest --cov=md2office --cov-report=html`
2. Identify uncovered code
3. Add tests for missing coverage
4. Re-run tests to verify

### Coverage Report Not Generated

**Problem:** No `htmlcov/` directory after running tests

**Solutions:**
1. Ensure `--cov-report=html` is included
2. Check pytest configuration in `pyproject.toml`
3. Verify coverage plugin is installed: `pip install pytest-cov`

### False Coverage Failures

**Problem:** Coverage shows < 80% but code seems well-tested

**Solutions:**
1. Check if test files are excluded from coverage
2. Verify source paths are correct in `pyproject.toml`
3. Review `[tool.coverage.run]` configuration

## See Also

- [Test Structure](test-structure.md) - Test organization
- [Contributing Guide](../contributing.md) - How to contribute tests
- [pytest Documentation](https://docs.pytest.org/) - Testing framework docs
- [Coverage.py Documentation](https://coverage.readthedocs.io/) - Coverage tool docs

---

**Last Updated:** 2024

