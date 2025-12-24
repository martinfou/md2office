"""
Conversion Worker Thread

Background thread for performing conversions without blocking the UI.
"""

from PySide6.QtCore import QThread, Signal
from typing import List, Dict, Any, Optional
from ..conversion_service import ConversionService


class ConversionWorker(QThread):
    """
    Worker thread for file conversion.
    
    Performs conversion in background to keep UI responsive.
    """
    
    # Signals
    progress_updated = Signal(int, str)  # percentage, status message
    file_started = Signal(str)  # input file path
    file_completed = Signal(str, bool)  # input file path, success
    finished = Signal(dict)  # result dictionary
    
    def __init__(
        self,
        input_path: str,
        formats: List[str],
        output_dir: str = ".",
        output_name: Optional[str] = None,
        output_suffix: Optional[str] = None,
        overwrite: bool = False,
        config: Optional[Dict[str, Any]] = None,
        parent=None
    ):
        """
        Initialize conversion worker.
        
        Args:
            input_path: Path to markdown file
            formats: List of format names
            output_dir: Output directory
            output_name: Custom output filename
            output_suffix: Suffix for output filename
            overwrite: Whether to overwrite existing files
            config: Configuration options
            parent: Parent QObject
        """
        super().__init__(parent)
        self.input_path = input_path
        self.formats = formats
        self.output_dir = output_dir
        self.output_name = output_name
        self.output_suffix = output_suffix
        self.overwrite = overwrite
        self.config = config or {}
        self.service = ConversionService()
    
    def run(self):
        """Execute conversion in background thread."""
        try:
            # Emit start signal
            self.file_started.emit(self.input_path)
            self.progress_updated.emit(10, "Starting conversion...")
            
            # Perform conversion
            self.progress_updated.emit(30, "Reading markdown file...")
            result = self.service.convert_file(
                input_path=self.input_path,
                formats=self.formats,
                output_dir=self.output_dir,
                output_name=self.output_name,
                output_suffix=self.output_suffix,
                overwrite=self.overwrite,
                config=self.config
            )
            
            self.progress_updated.emit(80, "Writing output files...")
            
            # Emit completion signal
            success = result.get('success', False)
            self.file_completed.emit(self.input_path, success)
            
            self.progress_updated.emit(100, "Conversion complete" if success else "Conversion failed")
            
            # Emit finished signal with result
            self.finished.emit(result)
        
        except Exception as e:
            # Handle unexpected errors
            error_result = {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'error_type': 'UnexpectedError'
            }
            self.file_completed.emit(self.input_path, False)
            self.finished.emit(error_result)

