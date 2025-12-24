"""
GUI Main Entry Point

Launches the md2office graphical user interface.
"""

import sys
from PySide6.QtWidgets import QApplication
from .main_window import MainWindow


def main():
    """Launch GUI application."""
    # Check if QApplication already exists
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("md2office")
    app.setOrganizationName("md2office")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

