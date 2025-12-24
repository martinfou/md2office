"""
Document format generators module.
"""

# Lazy imports to handle missing dependencies gracefully
def _import_word_generator():
    try:
        from .word_generator import WordGenerator
        return WordGenerator
    except ImportError:
        return None

def _import_powerpoint_generator():
    try:
        from .powerpoint_generator import PowerPointGenerator
        return PowerPointGenerator
    except ImportError:
        return None

def _import_pdf_generator():
    try:
        from .pdf_generator import PDFGenerator
        return PDFGenerator
    except ImportError:
        return None

# Try to import generators, but don't fail if dependencies are missing
try:
    from .word_generator import WordGenerator
except (ImportError, ModuleNotFoundError):
    WordGenerator = None

try:
    from .powerpoint_generator import PowerPointGenerator
except (ImportError, ModuleNotFoundError):
    PowerPointGenerator = None

try:
    from .pdf_generator import PDFGenerator
except (ImportError, ModuleNotFoundError):
    PDFGenerator = None

__all__ = ['WordGenerator', 'PowerPointGenerator', 'PDFGenerator']

