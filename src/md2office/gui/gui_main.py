"""
GUI Main Entry Point

Launches the md2office graphical user interface.
"""

import os
import sys
from PySide6.QtWidgets import QApplication
from .main_window import MainWindow


def main():
    """Launch GUI application."""
    # Remove invalid style overrides from environment variables
    # This prevents warnings about unavailable styles like 'kvantum'
    if 'QT_STYLE_OVERRIDE' in os.environ:
        style_override = os.environ.get('QT_STYLE_OVERRIDE', '')
        # Only keep valid styles (Windows, Fusion are always available)
        if style_override not in ['Windows', 'Fusion']:
            # Remove invalid style override
            del os.environ['QT_STYLE_OVERRIDE']
    
    # Check if QApplication already exists
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("md2office")
    app.setOrganizationName("md2office")
    
    # Set a valid style explicitly to avoid warnings
    # Fusion is a cross-platform, modern style that's always available
    try:
        app.setStyle('Fusion')
    except Exception:
        # Fallback to Windows style if Fusion fails
        try:
            app.setStyle('Windows')
        except Exception:
            pass  # Use default if both fail
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

