"""
PyLogger - A comprehensive Python logging package with multiple destinations.

Provides advanced logging capabilities including:
- Telegram notifications
- Pushover notifications  
- Email notifications
- File logging with rotation
- Console logging
- Configuration via YAML or dict
- Direct message sending capabilities
"""

__version__ = "1.0.0"
__author__ = "Raz Steinmetz"
__email__ = "raz.steinmetz@gmail.com"

from .logger import PyLogger, send_telegram, send_pushover, send_email
from .config import LoggerConfig
from .handlers import (
    TelegramHandler,
    PushoverHandler, 
    EmailHandler,
    RotatingFileHandler,
    ConsoleHandler
)

__all__ = [
    'PyLogger',
    'LoggerConfig',
    'TelegramHandler',
    'PushoverHandler',
    'EmailHandler', 
    'RotatingFileHandler',
    'ConsoleHandler',
    'send_telegram',
    'send_pushover', 
    'send_email'
]