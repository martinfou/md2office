# File Requirements Guide

This document explains which files are needed and why.

## ✅ Required Files

### 1. `requirements.txt` ✅ **KEEP**
**Purpose**: Runtime dependencies only  
**Used by**: 
- Users installing the package
- CI/CD pipelines
- Production deployments

**Contains**: Only packages needed to run the application
- PyYAML
- python-docx
- python-pptx
- reportlab
- click

**Status**: ✅ Cleaned - removed dev dependencies

---

### 2. `requirements-dev.txt` ✅ **KEEP**
**Purpose**: Development dependencies  
**Used by**: 
- Developers setting up the project
- CI/CD for testing and linting
- Pre-commit hooks

**Contains**: Testing, linting, and development tools
- pytest, pytest-cov, etc.
- black, flake8, mypy, isort
- pre-commit
- Security tools (bandit, safety, pip-audit)
- Documentation tools (sphinx)

**Status**: ✅ Correct - includes base requirements via `-r requirements.txt`

---

### 3. `SECURITY.md` ✅ **KEEP**
**Purpose**: Security policy and vulnerability reporting  
**Used by**:
- GitHub (shows in Security tab)
- Users reporting security issues
- Security researchers

**Why needed**:
- ✅ GitHub automatically detects and displays this file
- ✅ Provides clear security reporting process
- ✅ Industry best practice for open source projects
- ✅ Required for responsible disclosure

**Status**: ✅ Keep - important for open source projects

---

### 4. `setup.py` ❌ **REMOVED**
**Purpose**: Legacy Python packaging (PEP 517/518)  
**Status**: ✅ **Removed** - Using modern `pyproject.toml` instead

**Why removed**:
- ✅ `pyproject.toml` is the modern standard (PEP 518, PEP 621)
- ✅ All functionality covered by `pyproject.toml`
- ✅ `pip install -e .` works with `pyproject.toml` (Python 3.8+)
- ✅ Cleaner, single source of truth
- ✅ Better tool support (black, isort, mypy, pytest configs)

**What replaced it**:
- All package metadata → `pyproject.toml` `[project]` section
- Entry points → `pyproject.toml` `[project.scripts]`
- Package discovery → `pyproject.toml` `[tool.setuptools]`
- Build config → `pyproject.toml` `[build-system]`

---

## 📊 Summary

| File | Status | Reason |
|------|--------|--------|
| `requirements.txt` | ✅ **KEEP** | Runtime dependencies - essential |
| `requirements-dev.txt` | ✅ **KEEP** | Dev dependencies - needed for development |
| `SECURITY.md` | ✅ **KEEP** | Security policy - GitHub best practice |
| `setup.py` | ❌ **REMOVED** | Replaced by `pyproject.toml` (modern standard) |
| `pyproject.toml` | ✅ **KEEP** | Modern Python packaging (replaces setup.py) |

## 🔄 What Changed

### `requirements.txt` - Cleaned ✅
**Before**: Mixed runtime + dev dependencies  
**After**: Only runtime dependencies

```diff
- pytest>=7.2.0          # Moved to requirements-dev.txt
- pytest-cov>=4.0.0      # Moved to requirements-dev.txt
- black>=23.0.0          # Moved to requirements-dev.txt
- flake8>=6.0.0          # Moved to requirements-dev.txt
- mypy>=1.0.0            # Moved to requirements-dev.txt
- pyinstaller>=5.0.0     # Moved to requirements-dev.txt
```

**Now contains only**:
- PyYAML
- python-docx
- python-pptx
- reportlab
- click

## 💡 Recommendations

1. **Keep all files** - They serve different purposes
2. **`pyproject.toml` replaces `setup.py`** - Modern Python standard
3. **`SECURITY.md` is important** - GitHub uses it automatically
4. **Separate runtime vs dev** - Makes installation faster for users

## 🚀 Usage

```bash
# For users (runtime only)
pip install -r requirements.txt

# For developers (includes dev tools)
pip install -r requirements-dev.txt

# Or install package (editable mode)
pip install -e .  # Uses pyproject.toml (modern Python 3.8+)
```

---

**Last Updated**: 2024

