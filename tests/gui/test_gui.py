"""
Tests for GUI components.

Note: These tests require PySide6 to be installed.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path (now in subdirectory, go up two levels)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

# Check if PySide6 is available
try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

# Only run GUI tests if PySide6 is available
pytestmark = pytest.mark.skipif(
    not PYSIDE6_AVAILABLE,
    reason="PySide6 not available"
)


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


@pytest.fixture
def main_window(qapp):
    """Create main window instance."""
    from md2office.gui.main_window import MainWindow
    return MainWindow()


class TestMainWindow:
    """Tests for MainWindow."""
    
    def test_window_creation(self, main_window):
        """Test that window is created successfully."""
        assert main_window is not None
        assert main_window.windowTitle() == "md2office - Markdown to Office Document Converter"
    
    def test_file_path_edit_exists(self, main_window):
        """Test that file path edit exists."""
        assert main_window.file_path_edit is not None
        assert main_window.file_path_edit.isReadOnly()
    
    def test_format_checkboxes_exist(self, main_window):
        """Test that format checkboxes exist."""
        assert main_window.word_checkbox is not None
        assert main_window.powerpoint_checkbox is not None
        assert main_window.pdf_checkbox is not None
        assert main_window.all_formats_checkbox is not None
    
    def test_all_formats_toggle(self, main_window):
        """Test all formats checkbox behavior."""
        # Initially, individual checkboxes should be enabled
        assert main_window.word_checkbox.isEnabled()
        assert main_window.powerpoint_checkbox.isEnabled()
        assert main_window.pdf_checkbox.isEnabled()
        
        # Check all formats
        main_window.all_formats_checkbox.setChecked(True)
        assert not main_window.word_checkbox.isEnabled()
        assert not main_window.powerpoint_checkbox.isEnabled()
        assert not main_window.pdf_checkbox.isEnabled()
        assert main_window.word_checkbox.isChecked()
        assert main_window.powerpoint_checkbox.isChecked()
        assert main_window.pdf_checkbox.isChecked()
        
        # Uncheck all formats
        main_window.all_formats_checkbox.setChecked(False)
        assert main_window.word_checkbox.isEnabled()
        assert main_window.powerpoint_checkbox.isEnabled()
        assert main_window.pdf_checkbox.isEnabled()
    
    def test_get_selected_formats(self, main_window):
        """Test getting selected formats."""
        # Default: only Word should be checked
        main_window.word_checkbox.setChecked(True)
        main_window.powerpoint_checkbox.setChecked(False)
        main_window.pdf_checkbox.setChecked(False)
        main_window.all_formats_checkbox.setChecked(False)
        
        formats = main_window._get_selected_formats()
        assert 'word' in formats
        assert len(formats) == 1
        
        # Check all formats checkbox
        main_window.all_formats_checkbox.setChecked(True)
        formats = main_window._get_selected_formats()
        assert 'word' in formats
        assert 'powerpoint' in formats
        assert 'pdf' in formats
        assert len(formats) == 3
    
    def test_validate_inputs_no_file(self, main_window):
        """Test input validation with no file."""
        main_window.file_path_edit.setText("")
        valid, msg = main_window._validate_inputs()
        assert not valid
        assert "select an input file" in msg.lower()
    
    def test_validate_inputs_no_formats(self, main_window, tmp_path):
        """Test input validation with no formats selected."""
        # Create a test markdown file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test")
        
        main_window.file_path_edit.setText(str(test_file))
        main_window.word_checkbox.setChecked(False)
        main_window.powerpoint_checkbox.setChecked(False)
        main_window.pdf_checkbox.setChecked(False)
        main_window.all_formats_checkbox.setChecked(False)
        
        valid, msg = main_window._validate_inputs()
        assert not valid
        assert "format" in msg.lower()
    
    def test_validate_inputs_valid(self, main_window, tmp_path):
        """Test input validation with valid inputs."""
        # Create a test markdown file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test")
        
        main_window.file_path_edit.setText(str(test_file))
        main_window.word_checkbox.setChecked(True)
        main_window.output_dir_edit.setText(str(tmp_path))
        
        valid, msg = main_window._validate_inputs()
        assert valid
        assert msg == ""
    
    def test_get_config(self, main_window):
        """Test getting configuration from UI."""
        main_window.toc_checkbox.setChecked(True)
        main_window.page_breaks_checkbox.setChecked(True)
        main_window.skip_images_checkbox.setChecked(True)
        main_window.style_combo.setCurrentText("professional")
        
        config = main_window._get_config()
        assert config['tableOfContents'] is True
        assert config['pageBreaks'] is True
        assert config['skipMissingImages'] is True
        assert config['style'] == "professional"
        assert config['overwrite'] is False


class TestConversionService:
    """Tests for ConversionService."""
    
    def test_service_creation(self):
        """Test that service can be created."""
        from md2office.gui.conversion_service import ConversionService
        service = ConversionService()
        assert service is not None
        assert service.pipeline is not None
    
    def test_convert_file_not_found(self, tmp_path):
        """Test conversion with non-existent file."""
        from md2office.gui.conversion_service import ConversionService
        service = ConversionService()
        
        result = service.convert_file(
            input_path=str(tmp_path / "nonexistent.md"),
            formats=['word']
        )
        
        assert not result['success']
        assert 'error' in result
        assert result['error_type'] == 'FileNotFound'
    
    def test_convert_file_invalid_format(self, tmp_path):
        """Test conversion with invalid file format."""
        from md2office.gui.conversion_service import ConversionService
        service = ConversionService()
        
        # Create a non-markdown file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Not markdown")
        
        result = service.convert_file(
            input_path=str(test_file),
            formats=['word']
        )
        
        # Should still attempt conversion (validation happens in UI)
        # This test mainly checks that service doesn't crash


class TestConversionWorker:
    """Tests for ConversionWorker."""
    
    def test_worker_creation(self, tmp_path):
        """Test that worker can be created."""
        from md2office.gui.workers.conversion_worker import ConversionWorker
        
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test")
        
        worker = ConversionWorker(
            input_path=str(test_file),
            formats=['word'],
            output_dir=str(tmp_path)
        )
        
        assert worker is not None
        assert worker.input_path == str(test_file)
        assert worker.formats == ['word']

