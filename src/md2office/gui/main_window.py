"""
Main Window

Main application window for md2office GUI.
"""

import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QCheckBox, QFileDialog, QMessageBox,
    QProgressBar, QGroupBox, QComboBox, QTextEdit
)
from PySide6.QtCore import Qt, Signal, QThread, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent

from .workers.conversion_worker import ConversionWorker


class MainWindow(QMainWindow):
    """
    Main application window.
    
    Provides basic conversion interface with file selection,
    format selection, and conversion controls.
    """
    
    def __init__(self, parent=None):
        """Initialize main window."""
        super().__init__(parent)
        self.setWindowTitle("md2office - Markdown to Office Document Converter")
        self.setMinimumSize(600, 500)
        
        # Conversion state
        self.current_worker: Optional[ConversionWorker] = None
        
        # Create UI
        self._create_ui()
        self._setup_drag_drop()
    
    def _create_ui(self):
        """Create user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # File Selection Section
        file_group = QGroupBox("Input File")
        file_layout = QVBoxLayout(file_group)
        
        file_input_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Select a markdown file or drag and drop here...")
        self.file_path_edit.setReadOnly(True)
        file_input_layout.addWidget(self.file_path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_file)
        file_input_layout.addWidget(browse_btn)
        
        file_layout.addLayout(file_input_layout)
        layout.addWidget(file_group)
        
        # Format Selection Section
        format_group = QGroupBox("Output Formats")
        format_layout = QVBoxLayout(format_group)
        
        self.word_checkbox = QCheckBox("Word (.docx)")
        self.word_checkbox.setChecked(True)
        format_layout.addWidget(self.word_checkbox)
        
        self.powerpoint_checkbox = QCheckBox("PowerPoint (.pptx)")
        format_layout.addWidget(self.powerpoint_checkbox)
        
        self.pdf_checkbox = QCheckBox("PDF")
        format_layout.addWidget(self.pdf_checkbox)
        
        self.all_formats_checkbox = QCheckBox("All Formats")
        self.all_formats_checkbox.toggled.connect(self._on_all_formats_toggled)
        format_layout.addWidget(self.all_formats_checkbox)
        
        layout.addWidget(format_group)
        
        # Output Directory Section
        output_group = QGroupBox("Output Directory")
        output_layout = QVBoxLayout(output_group)
        
        output_input_layout = QHBoxLayout()
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setText(".")
        self.output_dir_edit.setPlaceholderText("Output directory...")
        output_input_layout.addWidget(self.output_dir_edit)
        
        output_browse_btn = QPushButton("Browse...")
        output_browse_btn.clicked.connect(self._browse_output_dir)
        output_input_layout.addWidget(output_browse_btn)
        
        output_layout.addLayout(output_input_layout)
        layout.addWidget(output_group)
        
        # Basic Options Section
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)
        
        self.toc_checkbox = QCheckBox("Table of Contents")
        options_layout.addWidget(self.toc_checkbox)
        
        self.page_breaks_checkbox = QCheckBox("Page Breaks")
        options_layout.addWidget(self.page_breaks_checkbox)
        
        self.skip_images_checkbox = QCheckBox("Skip Missing Images")
        options_layout.addWidget(self.skip_images_checkbox)
        
        # Style preset
        style_layout = QHBoxLayout()
        style_layout.addWidget(QLabel("Style Preset:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(["default", "minimal", "professional"])
        style_layout.addWidget(self.style_combo)
        style_layout.addStretch()
        options_layout.addLayout(style_layout)
        
        layout.addWidget(options_group)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setDefault(True)
        self.convert_btn.clicked.connect(self._start_conversion)
        button_layout.addWidget(self.convert_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        layout.addStretch()
    
    def _setup_drag_drop(self):
        """Setup drag and drop functionality."""
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith('.md'):
                self.file_path_edit.setText(file_path)
            else:
                QMessageBox.warning(
                    self,
                    "Invalid File",
                    "Please drop a markdown (.md) file."
                )
    
    def _browse_file(self):
        """Browse for input file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Markdown File",
            "",
            "Markdown Files (*.md);;All Files (*)"
        )
        if file_path:
            self.file_path_edit.setText(file_path)
    
    def _browse_output_dir(self):
        """Browse for output directory."""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.output_dir_edit.text() or "."
        )
        if dir_path:
            self.output_dir_edit.setText(dir_path)
    
    def _on_all_formats_toggled(self, checked: bool):
        """Handle all formats checkbox toggle."""
        if checked:
            self.word_checkbox.setChecked(True)
            self.powerpoint_checkbox.setChecked(True)
            self.pdf_checkbox.setChecked(True)
            self.word_checkbox.setEnabled(False)
            self.powerpoint_checkbox.setEnabled(False)
            self.pdf_checkbox.setEnabled(False)
        else:
            self.word_checkbox.setEnabled(True)
            self.powerpoint_checkbox.setEnabled(True)
            self.pdf_checkbox.setEnabled(True)
    
    def _get_selected_formats(self) -> List[str]:
        """Get list of selected output formats."""
        if self.all_formats_checkbox.isChecked():
            return ['word', 'powerpoint', 'pdf']
        
        formats = []
        if self.word_checkbox.isChecked():
            formats.append('word')
        if self.powerpoint_checkbox.isChecked():
            formats.append('powerpoint')
        if self.pdf_checkbox.isChecked():
            formats.append('pdf')
        
        return formats
    
    def _validate_inputs(self):
        """Validate user inputs."""
        # Check file path
        file_path = self.file_path_edit.text().strip()
        if not file_path:
            return False, "Please select an input file."
        
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            return False, f"Input file not found: {file_path}"
        
        if not file_path_obj.is_file():
            return False, f"Input path is not a file: {file_path}"
        
        if not file_path.lower().endswith('.md'):
            return False, "Input file must be a markdown (.md) file."
        
        # Check formats
        formats = self._get_selected_formats()
        if not formats:
            return False, "Please select at least one output format."
        
        # Check output directory
        output_dir = self.output_dir_edit.text().strip() or "."
        output_dir_obj = Path(output_dir)
        if output_dir_obj.exists() and not output_dir_obj.is_dir():
            return False, f"Output path exists but is not a directory: {output_dir}"
        
        return True, ""
    
    def _get_config(self) -> Dict[str, Any]:
        """Get configuration from UI."""
        return {
            'style': self.style_combo.currentText(),
            'tableOfContents': self.toc_checkbox.isChecked(),
            'pageBreaks': self.page_breaks_checkbox.isChecked(),
            'skipMissingImages': self.skip_images_checkbox.isChecked(),
            'overwrite': False  # MVP: always prompt
        }
    
    def _start_conversion(self):
        """Start conversion process."""
        # Validate inputs
        valid, error_msg = self._validate_inputs()
        if not valid:
            QMessageBox.warning(self, "Validation Error", error_msg)
            return
        
        # Check if conversion already in progress
        if self.current_worker and self.current_worker.isRunning():
            QMessageBox.information(
                self,
                "Conversion in Progress",
                "A conversion is already in progress. Please wait for it to complete."
            )
            return
        
        # Get inputs
        file_path = self.file_path_edit.text().strip()
        formats = self._get_selected_formats()
        output_dir = self.output_dir_edit.text().strip() or "."
        config = self._get_config()
        
        # Disable convert button
        self.convert_btn.setEnabled(False)
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Starting conversion...")
        
        # Create and start worker
        self.current_worker = ConversionWorker(
            input_path=file_path,
            formats=formats,
            output_dir=output_dir,
            overwrite=False,
            config=config
        )
        
        # Connect signals
        self.current_worker.progress_updated.connect(self._on_progress_updated)
        self.current_worker.finished.connect(self._on_conversion_finished)
        
        # Start conversion
        self.current_worker.start()
    
    def _on_progress_updated(self, percentage: int, message: str):
        """Handle progress update."""
        self.progress_bar.setValue(percentage)
        self.status_label.setText(message)
    
    def _on_conversion_finished(self, result: Dict[str, Any]):
        """Handle conversion completion."""
        self.progress_bar.setVisible(False)
        self.convert_btn.setEnabled(True)
        
        if result.get('success'):
            # Show success message
            output_files = result.get('output_files', [])
            file_list = "\n".join([f"  • {f['path']}" for f in output_files])
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Conversion Complete")
            msg.setText("Conversion completed successfully!")
            msg.setDetailedText(f"Input: {result.get('input_file', 'Unknown')}\n\nOutput files:\n{file_list}")
            
            # Add buttons
            open_location_btn = msg.addButton("Open Location", QMessageBox.ActionRole)
            msg.addButton("OK", QMessageBox.AcceptRole)
            
            msg.exec()
            
            # Handle open location
            if msg.clickedButton() == open_location_btn:
                output_dir = Path(output_files[0]['path']).parent
                if sys.platform == 'win32':
                    import os
                    os.startfile(str(output_dir))
                elif sys.platform == 'darwin':
                    import subprocess
                    subprocess.run(['open', str(output_dir)])
                else:
                    import subprocess
                    subprocess.run(['xdg-open', str(output_dir)])
            
            self.status_label.setText("Conversion complete!")
        else:
            # Show error message
            error_msg = result.get('error', 'Unknown error occurred')
            error_type = result.get('error_type', 'Error')
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Conversion Failed")
            msg.setText(f"Conversion failed: {error_type}")
            msg.setDetailedText(error_msg)
            msg.exec()
            
            self.status_label.setText(f"Conversion failed: {error_type}")

