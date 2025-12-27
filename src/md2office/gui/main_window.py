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
    QProgressBar, QGroupBox, QComboBox, QTextEdit, QSplitter,
    QMenuBar, QMenu
)
from PySide6.QtCore import Qt, Signal, QThread, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QShortcut, QKeySequence, QCloseEvent, QAction

from .workers.conversion_worker import ConversionWorker
from .widgets.markdown_viewer import MarkdownViewer
from .widgets.markdown_editor import MarkdownEditor


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
        self.setMinimumSize(1200, 700)
        
        # Ensure application quits when window is closed
        self.setAttribute(Qt.WA_QuitOnClose, True)
        
        # Conversion state
        self.current_worker: Optional[ConversionWorker] = None
        
        # Current markdown file path
        self.current_markdown_path: Optional[Path] = None
        
        # Create menu bar first
        self._create_menu_bar()
        
        # Create UI
        self._create_ui()
        self._setup_drag_drop()
        self._setup_shortcuts()
        
        # Connect editor to preview (after UI is created)
        self.markdown_editor.content_changed.connect(self._on_editor_content_changed)
        self.markdown_editor.modification_changed.connect(self._on_modification_changed)
    
    def _create_menu_bar(self):
        """Create menu bar with file operations."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # New
        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.setStatusTip("Create a new document")
        new_action.triggered.connect(self._new_file)
        file_menu.addAction(new_action)
        
        # Open
        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.setStatusTip("Open a markdown file")
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # Save
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.setStatusTip("Save the current document")
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)
        self.save_action = save_action
        
        # Save As
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.setStatusTip("Save the document with a new name")
        save_as_action.triggered.connect(self._save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Close
        close_action = QAction("&Close", self)
        close_action.setShortcut(QKeySequence.Close)
        close_action.setStatusTip("Close the current document")
        close_action.triggered.connect(self._close_document)
        file_menu.addAction(close_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def _create_ui(self):
        """Create user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with splitter
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create main horizontal splitter
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Left pane: Conversion controls
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(16)
        left_layout.setContentsMargins(16, 16, 16, 16)
        
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
        left_layout.addWidget(file_group)
        
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
        
        left_layout.addWidget(format_group)
        
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
        left_layout.addWidget(output_group)
        
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
        
        left_layout.addWidget(options_group)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        left_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.status_label)
        
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
        
        left_layout.addLayout(button_layout)
        
        left_layout.addStretch()
        
        # Add left widget to main splitter
        main_splitter.addWidget(left_widget)
        
        # Middle and right panes: Editor and Preview
        editor_preview_splitter = QSplitter(Qt.Horizontal)
        
        # Middle pane: Markdown editor
        editor_group = QGroupBox("Editor")
        editor_layout = QVBoxLayout(editor_group)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        
        self.markdown_editor = MarkdownEditor()
        editor_layout.addWidget(self.markdown_editor)
        
        editor_preview_splitter.addWidget(editor_group)
        
        # Right pane: Markdown preview
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        self.markdown_viewer = MarkdownViewer()
        preview_layout.addWidget(self.markdown_viewer)
        
        editor_preview_splitter.addWidget(preview_group)
        
        # Set editor/preview splitter proportions (50% each)
        editor_preview_splitter.setSizes([500, 500])
        editor_preview_splitter.setStretchFactor(0, 1)
        editor_preview_splitter.setStretchFactor(1, 1)
        
        # Add editor/preview splitter to main splitter
        main_splitter.addWidget(editor_preview_splitter)
        
        # Set main splitter proportions (25% controls, 75% editor+preview)
        main_splitter.setSizes([300, 900])
        main_splitter.setStretchFactor(0, 0)
        main_splitter.setStretchFactor(1, 1)
    
    def _setup_drag_drop(self):
        """Setup drag and drop functionality."""
        self.setAcceptDrops(True)
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        # Meta+W (Windows key + W) to close window
        close_shortcut = QShortcut(QKeySequence("Meta+W"), self)
        close_shortcut.activated.connect(self.close)
        
        # Ctrl+Q to quit application (alternative)
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self._quit_application)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        if not self._check_unsaved_changes():
            event.ignore()
            return
        
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith('.md'):
                self._update_preview(file_path)
            else:
                QMessageBox.warning(
                    self,
                    "Invalid File",
                    "Please drop a markdown (.md) file."
                )
    
    def _browse_file(self):
        """Browse for input file."""
        if not self._check_unsaved_changes():
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Markdown File",
            "",
            "Markdown Files (*.md);;All Files (*)"
        )
        if file_path:
            self._update_preview(file_path)
    
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
        # Check if we have content
        content = self.markdown_editor.get_content()
        if not content.strip():
            return False, "No content to convert."
        
        # Check file path (use editor's current file or file path edit)
        file_path = None
        if self.markdown_editor.current_file:
            file_path = str(self.markdown_editor.current_file)
        else:
            file_path = self.file_path_edit.text().strip()
        
        if not file_path:
            return False, "Please save the document first or select an input file."
        
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
        # Get content from editor
        content = self.markdown_editor.get_content()
        if not content.strip():
            QMessageBox.warning(self, "Validation Error", "No content to convert.")
            return
        
        # Use editor's current file or prompt for save
        file_path = self.markdown_editor.current_file
        if not file_path:
            # Need to save file first
            reply = QMessageBox.question(
                self,
                "Save Required",
                "You need to save the document before converting. Save now?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self._save_file_as()
                file_path = self.markdown_editor.current_file
            else:
                return
        
        if not file_path:
            QMessageBox.warning(self, "Validation Error", "Please save the document first.")
            return
        
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
    
    def closeEvent(self, event: QCloseEvent):
        """
        Handle window close event.
        
        Checks if a conversion is in progress and prompts the user
        before closing if necessary.
        """
        # Check for unsaved changes first
        if not self._check_unsaved_changes():
            event.ignore()
            return
        
        # Check if conversion is in progress
        if self.current_worker and self.current_worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Conversion in Progress",
                "A conversion is currently in progress. Do you want to cancel it and close?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Stop the worker
                self.current_worker.terminate()
                self.current_worker.wait(3000)  # Wait up to 3 seconds
                if self.current_worker.isRunning():
                    self.current_worker.kill()
                event.accept()
            else:
                event.ignore()
        else:
            # No conversion in progress, close normally
            event.accept()
    
    def _update_preview(self, file_path: str):
        """
        Update markdown preview when file is selected.
        
        Args:
            file_path: Path to markdown file
        """
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                self.current_markdown_path = path
                # Load file into editor
                if self.markdown_editor.load_file(path):
                    self.file_path_edit.setText(str(path))
                    self._update_window_title()
            else:
                self.markdown_viewer.clear()
                self.current_markdown_path = None
        except Exception as e:
            # Silently handle preview errors - don't interrupt user workflow
            self.markdown_viewer.clear()
            self.current_markdown_path = None
    
    def _on_editor_content_changed(self, content: str):
        """Handle editor content changes - update preview."""
        base_path = self.markdown_editor.current_file.parent if self.markdown_editor.current_file else None
        self.markdown_viewer.set_markdown(content, base_path)
    
    def _on_modification_changed(self, modified: bool):
        """Handle modification state changes."""
        self._update_window_title()
        self.save_action.setEnabled(True)
    
    def _update_window_title(self):
        """Update window title with file name and modification indicator."""
        if self.markdown_editor.current_file:
            file_name = self.markdown_editor.current_file.name
            modified = "*" if self.markdown_editor.is_modified else ""
            self.setWindowTitle(f"md2office - {file_name}{modified}")
        else:
            modified = "*" if self.markdown_editor.is_modified else ""
            self.setWindowTitle(f"md2office - Untitled{modified}")
    
    def _new_file(self):
        """Create a new document."""
        if not self._check_unsaved_changes():
            return
        
        self.markdown_editor.new_file()
        self.file_path_edit.clear()
        self.current_markdown_path = None
        self._update_window_title()
    
    def _open_file(self):
        """Open a markdown file."""
        if not self._check_unsaved_changes():
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            "",
            "Markdown Files (*.md *.markdown);;All Files (*)"
        )
        
        if file_path:
            path = Path(file_path)
            if self.markdown_editor.load_file(path):
                self.file_path_edit.setText(file_path)
                self.current_markdown_path = path
                self._update_window_title()
            else:
                QMessageBox.warning(
                    self,
                    "Open Failed",
                    f"Could not open file: {file_path}"
                )
    
    def _handle_file_overwrite(self, file_path: Path) -> Optional[Path]:
        """
        Handle file overwrite prompt and backup creation.
        
        Args:
            file_path: Path to the file that may be overwritten
            
        Returns:
            Path to save to (may be modified for backup), or None if cancelled
        """
        if not file_path.exists():
            return file_path
        
        # File exists - prompt user
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("File Already Exists")
        msg.setText(f"The file '{file_path.name}' already exists.")
        msg.setInformativeText("What would you like to do?")
        
        # Add custom buttons
        overwrite_btn = msg.addButton("Overwrite", QMessageBox.DestructiveRole)
        backup_btn = msg.addButton("Create Backup", QMessageBox.ActionRole)
        cancel_btn = msg.addButton("Cancel", QMessageBox.RejectRole)
        
        msg.setDefaultButton(backup_btn)
        msg.exec()
        
        clicked_button = msg.clickedButton()
        
        if clicked_button == cancel_btn:
            return None
        elif clicked_button == overwrite_btn:
            return file_path
        elif clicked_button == backup_btn:
            # Create backup file
            backup_path = self._create_backup(file_path)
            if backup_path:
                QMessageBox.information(
                    self,
                    "Backup Created",
                    f"Backup created: {backup_path.name}\n\nProceeding with save..."
                )
                return file_path  # Save to original path
            else:
                QMessageBox.warning(
                    self,
                    "Backup Failed",
                    "Could not create backup file. Save cancelled."
                )
                return None
        
        return None
    
    def _create_backup(self, file_path: Path) -> Optional[Path]:
        """
        Create a backup of an existing file.
        
        Args:
            file_path: Path to the file to backup
            
        Returns:
            Path to the backup file, or None if backup failed
        """
        try:
            # Try multiple backup naming strategies
            backup_strategies = [
                # Strategy 1: Add .bak extension
                file_path.with_suffix(file_path.suffix + '.bak'),
                # Strategy 2: Add timestamp
                file_path.parent / f"{file_path.stem}_{self._get_timestamp()}{file_path.suffix}",
                # Strategy 3: Add _backup before extension
                file_path.parent / f"{file_path.stem}_backup{file_path.suffix}",
            ]
            
            for backup_path in backup_strategies:
                if not backup_path.exists():
                    # Copy file to backup location
                    import shutil
                    shutil.copy2(file_path, backup_path)
                    return backup_path
            
            # All strategies failed (files exist)
            QMessageBox.warning(
                self,
                "Backup Failed",
                f"Could not create backup: all backup file names are already in use."
            )
            return None
            
        except Exception as e:
            QMessageBox.warning(
                self,
                "Backup Failed",
                f"Error creating backup: {str(e)}"
            )
            return None
    
    def _get_timestamp(self) -> str:
        """Get timestamp string for backup files."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _save_file(self):
        """Save the current document."""
        if self.markdown_editor.current_file:
            file_path = self.markdown_editor.current_file
            
            # Check if file exists and handle overwrite/backup
            result_path = self._handle_file_overwrite(file_path)
            if result_path is None:
                return  # User cancelled
            
            if self.markdown_editor.save_file(result_path):
                QMessageBox.information(self, "Saved", "File saved successfully.")
            else:
                QMessageBox.warning(self, "Save Failed", "Could not save file.")
        else:
            self._save_file_as()
    
    def _save_file_as(self):
        """Save the document with a new name."""
        # Suggest current file name or "untitled.md"
        suggested_name = ""
        if self.markdown_editor.current_file:
            suggested_name = str(self.markdown_editor.current_file)
        elif self.current_markdown_path:
            suggested_name = str(self.current_markdown_path)
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Markdown File",
            suggested_name,
            "Markdown Files (*.md *.markdown);;All Files (*)"
        )
        
        if file_path:
            path = Path(file_path)
            
            # Check if file exists and handle overwrite/backup
            result_path = self._handle_file_overwrite(path)
            if result_path is None:
                return  # User cancelled
            
            if self.markdown_editor.save_file(result_path):
                self.file_path_edit.setText(str(result_path))
                self.current_markdown_path = result_path
                self._update_window_title()
                QMessageBox.information(self, "Saved", "File saved successfully.")
            else:
                QMessageBox.warning(self, "Save Failed", "Could not save file.")
    
    def _close_document(self):
        """Close the current document."""
        if not self._check_unsaved_changes():
            return
        
        self.markdown_editor.clear()
        self.file_path_edit.clear()
        self.current_markdown_path = None
        self._update_window_title()
    
    def _check_unsaved_changes(self) -> bool:
        """
        Check for unsaved changes and prompt user if needed.
        
        Returns:
            True if safe to proceed, False if user cancelled
        """
        if self.markdown_editor.is_modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them before continuing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if reply == QMessageBox.Save:
                # Save the file (may prompt for overwrite/backup if file exists)
                self._save_file()
                # Only proceed if save was successful (file is no longer modified)
                return not self.markdown_editor.is_modified
            elif reply == QMessageBox.Discard:
                # Discard changes - reset modification state without saving
                if self.markdown_editor.current_file and self.markdown_editor.current_file.exists():
                    # Reload from disk to discard changes
                    self.markdown_editor.load_file(self.markdown_editor.current_file)
                else:
                    # No file - just reset the modification state
                    self.markdown_editor.reset_modified_state()
                return True
            else:  # Cancel
                return False
        
        return True
    
    def _quit_application(self):
        """Quit the application."""
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            app.quit()

