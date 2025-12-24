"""
Logging system for md2office.

Provides structured logging with different log levels and output formats.
"""

import logging
import sys
from typing import Optional
from enum import Enum


class LogLevel(Enum):
    """Log levels."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for terminal output."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'
    }
    
    def format(self, record):
        """Format log record with colors."""
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logger(name: str = 'md2office', level: LogLevel = LogLevel.INFO,
                 verbose: bool = False, quiet: bool = False) -> logging.Logger:
    """
    Set up logger with appropriate configuration.
    
    Args:
        name: Logger name
        level: Log level
        verbose: Enable verbose (DEBUG) logging
        quiet: Suppress non-error output
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Don't add handlers if already configured
    if logger.handlers:
        return logger
    
    # Set log level
    if quiet:
        log_level = logging.ERROR
    elif verbose:
        log_level = logging.DEBUG
    else:
        log_level = level.value
    
    logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(log_level)
    
    # Create formatter
    if sys.stderr.isatty() and not quiet:
        formatter = ColoredFormatter(
            '%(levelname)s: %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str = 'md2office') -> logging.Logger:
    """
    Get logger instance.
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    # Set up default logger if not configured
    if not logger.handlers:
        setup_logger(name)
    
    return logger

