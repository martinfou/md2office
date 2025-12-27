"""
Markdown Editor Widget

Provides a text editor for editing markdown source code with syntax awareness.
"""

from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QTextDocument


class MarkdownHighlighter(QSyntaxHighlighter):
    """Basic syntax highlighter for markdown."""
    
    def __init__(self, parent: QTextDocument):
        super().__init__(parent)
        self._setup_formats()
    
    def _setup_formats(self):
        """Setup text formats for syntax highlighting."""
        # Headers
        header_format = QTextCharFormat()
        header_format.setForeground(QColor("#0066cc"))
        header_format.setFontWeight(QFont.Bold)
        self.header_format = header_format
        
        # Bold
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        self.bold_format = bold_format
        
        # Italic
        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        self.italic_format = italic_format
        
        # Code
        code_format = QTextCharFormat()
        code_format.setForeground(QColor("#c7254e"))
        code_format.setBackground(QColor("#f9f2f4"))
        code_format.setFontFamily("Courier New")
        self.code_format = code_format
        
        # Links
        link_format = QTextCharFormat()
        link_format.setForeground(QColor("#0066cc"))
        link_format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        self.link_format = link_format
    
    def highlightBlock(self, text: str):
        """Apply syntax highlighting to a block of text."""
        import re
        
        # Headers (# Header)
        pattern = r'^(#{1,6})\s+(.+)$'
        for match in re.finditer(pattern, text):
            self.setFormat(match.start(), match.end(), self.header_format)
        
        # Bold (**text**)
        pattern = r'\*\*(.+?)\*\*'
        for match in re.finditer(pattern, text):
            self.setFormat(match.start(), match.end(), self.bold_format)
        
        # Italic (*text*)
        pattern = r'(?<!\*)\*([^*]+?)\*(?!\*)'
        for match in re.finditer(pattern, text):
            self.setFormat(match.start(), match.end(), self.italic_format)
        
        # Inline code (`code`)
        pattern = r'`([^`]+)`'
        for match in re.finditer(pattern, text):
            self.setFormat(match.start(), match.end(), self.code_format)
        
        # Links [text](url)
        pattern = r'\[([^\]]+)\]\([^\)]+\)'
        for match in re.finditer(pattern, text):
            self.setFormat(match.start(), match.end(), self.link_format)


class MarkdownEditor(QPlainTextEdit):
    """
    Text editor widget for markdown source code.
    
    Provides syntax highlighting, file operations, and change tracking.
    """
    
    # Signals
    content_changed = Signal(str)  # Emitted when content changes (for preview)
    modification_changed = Signal(bool)  # Emitted when modification state changes
    
    def __init__(self, parent=None):
        """Initialize markdown editor."""
        super().__init__(parent)
        
        # Current file path
        self._current_file: Optional[Path] = None
        
        # Modification state
        self._is_modified = False
        
        # Setup editor
        self._setup_editor()
        
        # Setup syntax highlighting
        self.highlighter = MarkdownHighlighter(self.document())
        
        # Debounce timer for preview updates
        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self._emit_content_changed)
        
        # Connect text changes
        self.textChanged.connect(self._on_text_changed)
    
    def _setup_editor(self):
        """Setup editor appearance and behavior."""
        # Use monospace font
        font = QFont("Courier New", 10)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)
        
        # Set tab width (4 spaces)
        self.setTabStopDistance(40)
        
        # Enable line numbers (optional, can be added later)
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        
        # Set placeholder text
        self.setPlaceholderText("Start typing markdown here...\n\nOr use File → Open to load a file.")
    
    def _on_text_changed(self):
        """Handle text changes."""
        # Mark as modified
        if not self._is_modified:
            self._is_modified = True
            self.modification_changed.emit(True)
        
        # Debounce preview updates (500ms delay)
        self._preview_timer.stop()
        self._preview_timer.start(500)
    
    def _emit_content_changed(self):
        """Emit content changed signal for preview update."""
        self.content_changed.emit(self.toPlainText())
    
    def load_file(self, file_path: Path) -> bool:
        """
        Load markdown content from file.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not file_path.exists():
                return False
            
            content = file_path.read_text(encoding='utf-8')
            self.setPlainText(content)
            self._current_file = file_path
            self._is_modified = False
            self.modification_changed.emit(False)
            
            return True
        except Exception:
            return False
    
    def save_file(self, file_path: Optional[Path] = None) -> bool:
        """
        Save markdown content to file.
        
        Args:
            file_path: Path to save to (uses current file if None)
            
        Returns:
            True if successful, False otherwise
        """
        target_file = file_path or self._current_file
        if not target_file:
            return False
        
        try:
            content = self.toPlainText()
            target_file.write_text(content, encoding='utf-8')
            self._current_file = target_file
            self._is_modified = False
            self.modification_changed.emit(False)
            return True
        except Exception:
            return False
    
    def new_file(self):
        """Create a new empty document."""
        self.setPlainText("")
        self._current_file = None
        self._is_modified = False
        self.modification_changed.emit(False)
    
    def clear(self):
        """Clear the editor content."""
        self.setPlainText("")
        self._current_file = None
        self._is_modified = False
        self.modification_changed.emit(False)
    
    def reset_modified_state(self):
        """Reset the modification state without saving."""
        self._is_modified = False
        self.modification_changed.emit(False)
    
    @property
    def current_file(self) -> Optional[Path]:
        """Get current file path."""
        return self._current_file
    
    @property
    def is_modified(self) -> bool:
        """Check if document has unsaved changes."""
        return self._is_modified
    
    def get_content(self) -> str:
        """Get current markdown content."""
        return self.toPlainText()

