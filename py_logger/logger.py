"""
Main PyLogger class that orchestrates all logging destinations.

Provides a unified interface for logging to multiple destinations with
individual configuration and control capabilities.
"""

import logging
import inspect
from typing import Dict, Any, Optional, List, Union
from .config import LoggerConfig, ConfigValidationError
from .handlers import (
    ConsoleHandler,
    RotatingFileHandler, 
    TelegramHandler,
    PushoverHandler,
    EmailHandler
)

# Global PyLogger instance for standard library integration
_global_pylogger = None


class PyLogger:
    """
    Advanced logging class with multiple destination support.
    
    Features:
    - Multiple destinations (console, file, telegram, pushover, email)
    - Individual log levels per destination
    - Runtime enable/disable of destinations
    - Direct message sending bypassing log levels
    - Configuration via YAML or dictionary
    - Integration with standard logging.getLogger()
    """
    
    def __init__(self, config_path: Optional[str] = None, config: Optional[Dict[str, Any]] = None, 
                 name: Optional[str] = None):
        """
        Initialize PyLogger.
        
        Args:
            config_path: Path to YAML configuration file
            config: Dictionary configuration
            name: Logger name (defaults to calling module name)
        """
        # Determine logger name
        if name is None:
            frame = inspect.currentframe().f_back
            name = frame.f_globals.get('__name__', 'PyLogger')
        
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Set to lowest level, handlers will filter
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Load configuration
        try:
            self.config_manager = LoggerConfig(config_path, config)
        except ConfigValidationError as e:
            raise ValueError(f"Configuration error: {e}")
        
        # Initialize handlers
        self.handlers = {}
        self._setup_handlers()
    
    @classmethod
    def setup(cls, config_path: Optional[str] = None, config: Optional[Dict[str, Any]] = None, 
              name: Optional[str] = None) -> 'PyLogger':
        """
        Setup PyLogger as the global logger for use with standard logging.getLogger().
        
        After calling this method, you can use logging.getLogger() in any module
        and it will use PyLogger's configured destinations.
        
        Args:
            config_path: Path to YAML configuration file
            config: Dictionary configuration  
            name: Logger name (defaults to root logger)
            
        Returns:
            PyLogger: The configured PyLogger instance
            
        Example:
            # In main.py
            from py_logger import PyLogger
            PyLogger.setup(config_path="config.yaml", name="MyApp")
            
            # In any other module
            import logging
            logger = logging.getLogger()  # Gets the PyLogger instance
            logger.info("This uses PyLogger destinations!")
        """
        global _global_pylogger
        
        if name is None:
            name = "root"
        
        # Create PyLogger instance
        pylogger = cls(config_path=config_path, config=config, name=name)
        _global_pylogger = pylogger
        
        # Replace the root logger's handlers with PyLogger's handlers
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        
        # Add PyLogger's handlers to root logger
        for handler in pylogger.handlers.values():
            root_logger.addHandler(handler)
        
        root_logger.setLevel(logging.DEBUG)
        
        # Store reference to PyLogger in root logger for direct message access
        root_logger.pylogger = pylogger
        
        return pylogger
    
    @staticmethod
    def get_instance() -> Optional['PyLogger']:
        """Get the global PyLogger instance if one was set up."""
        return _global_pylogger
    
    def _setup_handlers(self) -> None:
        """Setup all configured handlers."""
        config = self.config_manager.to_dict()
        
        # Console handler
        if 'console' in config:
            self.handlers['console'] = ConsoleHandler(config['console'])
            self.logger.addHandler(self.handlers['console'])
        
        # File handler
        if 'file' in config:
            self.handlers['file'] = RotatingFileHandler(config['file'])
            self.logger.addHandler(self.handlers['file'])
        
        # Telegram handler
        if 'telegram' in config:
            self.handlers['telegram'] = TelegramHandler(config['telegram'])
            self.logger.addHandler(self.handlers['telegram'])
        
        # Pushover handler
        if 'pushover' in config:
            self.handlers['pushover'] = PushoverHandler(config['pushover'])
            self.logger.addHandler(self.handlers['pushover'])
        
        # Email handler
        if 'email' in config:
            self.handlers['email'] = EmailHandler(config['email'])
            self.logger.addHandler(self.handlers['email'])
    
    def _refresh_handlers(self) -> None:
        """Refresh handlers after configuration changes."""
        # Remove old handlers
        for handler in list(self.logger.handlers):
            self.logger.removeHandler(handler)
        
        # Clear handlers dict
        self.handlers.clear()
        
        # Setup new handlers
        self._setup_handlers()
    
    # Standard logging interface
    def debug(self, message: str, *args, **kwargs) -> None:
        """Log a debug message."""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """Log an info message."""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """Log a warning message."""
        self.logger.warning(message, *args, **kwargs)
    
    def warn(self, message: str, *args, **kwargs) -> None:
        """Log a warning message (alias for warning)."""
        self.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """Log an error message."""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """Log a critical message."""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs) -> None:
        """Log an exception with traceback."""
        self.logger.exception(message, *args, **kwargs)
    
    def log(self, level: Union[int, str], message: str, *args, **kwargs) -> None:
        """Log a message at the specified level."""
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        self.logger.log(level, message, *args, **kwargs)
    
    # Direct messaging methods
    def send_telegram(self, message: str, parse_mode: Optional[str] = None) -> bool:
        """
        Send a direct Telegram message bypassing log level.
        
        Args:
            message: Message to send
            parse_mode: Parse mode (HTML, Markdown, etc.)
            
        Returns:
            bool: True if message was sent successfully
        """
        handler = self.handlers.get('telegram')
        if handler and isinstance(handler, TelegramHandler):
            return handler.send_direct_message(message, parse_mode)
        return False
    
    def send_pushover(self, message: str, destination: Optional[str] = None, 
                     priority: Optional[int] = None, title: Optional[str] = None) -> List[bool]:
        """
        Send a direct Pushover message bypassing log level.
        
        Args:
            message: Message to send
            destination: Specific destination name (optional)
            priority: Message priority (-2 to 2)
            title: Message title
            
        Returns:
            List[bool]: Results for each destination
        """
        handler = self.handlers.get('pushover')
        if handler and isinstance(handler, PushoverHandler):
            return handler.send_direct_message(message, destination, priority, title)
        return [False]
    
    def send_email(self, subject: str, message: str, to_emails: Optional[List[str]] = None) -> bool:
        """
        Send a direct email message bypassing log level.
        
        Args:
            subject: Email subject
            message: Email message
            to_emails: List of recipient emails (optional, uses config default)
            
        Returns:
            bool: True if email was sent successfully
        """
        handler = self.handlers.get('email')
        if handler and isinstance(handler, EmailHandler):
            return handler.send_direct_message(subject, message, to_emails)
        return False
    
    # Configuration management
    def is_destination_enabled(self, destination: str) -> bool:
        """
        Check if a destination is enabled.
        
        Args:
            destination: Destination name
            
        Returns:
            bool: True if destination is enabled
        """
        return self.config_manager.is_destination_enabled(destination)
    
    def enable_destination(self, destination: str) -> None:
        """
        Enable a destination at runtime.
        
        Args:
            destination: Destination name to enable
        """
        self.config_manager.enable_destination(destination)
        handler = self.handlers.get(destination)
        if handler:
            handler.enabled = True
        else:
            # If handler doesn't exist, recreate all handlers
            self._refresh_handlers()
    
    def disable_destination(self, destination: str) -> None:
        """
        Disable a destination at runtime.
        
        Args:
            destination: Destination name to disable
        """
        self.config_manager.disable_destination(destination)
        handler = self.handlers.get(destination)
        if handler:
            handler.enabled = False
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Update configuration at runtime.
        
        Args:
            new_config: New configuration dictionary
        """
        self.config_manager.update_config(new_config)
        self._refresh_handlers()
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get current configuration.
        
        Returns:
            Dict[str, Any]: Current configuration dictionary
        """
        return self.config_manager.to_dict()
    
    def save_config(self, file_path: str) -> None:
        """
        Save current configuration to YAML file.
        
        Args:
            file_path: Path to save configuration
        """
        self.config_manager.save_to_yaml(file_path)
    
    # Context manager support
    def __enter__(self):
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and cleanup."""
        # Close all handlers
        for handler in self.handlers.values():
            if hasattr(handler, 'close'):
                handler.close()
    
    # Additional utility methods
    def set_level(self, destination: str, level: Union[str, int]) -> None:
        """
        Set log level for a specific destination.
        
        Args:
            destination: Destination name
            level: Log level (string or int)
        """
        handler = self.handlers.get(destination)
        if handler:
            if isinstance(level, str):
                level = getattr(logging, level.upper())
            handler.setLevel(level)
            
            # Update config as well
            self.config_manager.config[destination]['level'] = logging.getLevelName(level)
    
    def get_destinations(self) -> List[str]:
        """
        Get list of available destinations.
        
        Returns:
            List[str]: List of destination names
        """
        return list(self.handlers.keys())
    
    def get_enabled_destinations(self) -> List[str]:
        """
        Get list of enabled destinations.
        
        Returns:
            List[str]: List of enabled destination names
        """
        return [dest for dest in self.handlers.keys() if self.is_destination_enabled(dest)]
    
    def test_destinations(self) -> Dict[str, bool]:
        """
        Test all destinations by sending a test message.
        
        Returns:
            Dict[str, bool]: Test results for each destination
        """
        results = {}
        test_message = "PyLogger test message"
        
        for destination in self.handlers.keys():
            if not self.is_destination_enabled(destination):
                results[destination] = False
                continue
                
            try:
                if destination == 'console':
                    self.info(test_message)
                    results[destination] = True
                elif destination == 'file':
                    self.info(test_message)
                    results[destination] = True
                elif destination == 'telegram':
                    results[destination] = self.send_telegram(test_message)
                elif destination == 'pushover':
                    push_results = self.send_pushover(test_message, title="PyLogger Test")
                    results[destination] = any(push_results)
                elif destination == 'email':
                    results[destination] = self.send_email("PyLogger Test", test_message)
                else:
                    results[destination] = False
            except Exception as e:
                print(f"Test failed for {destination}: {e}")
                results[destination] = False
        
        return results


# Convenience functions for standard logging integration
def send_telegram(message: str, parse_mode: Optional[str] = None) -> bool:
    """Send a Telegram message using the global PyLogger instance."""
    instance = PyLogger.get_instance()
    if instance:
        return instance.send_telegram(message, parse_mode)
    
    # Fallback: try to get from root logger
    root_logger = logging.getLogger()
    if hasattr(root_logger, 'pylogger'):
        return root_logger.pylogger.send_telegram(message, parse_mode)
    
    return False


def send_pushover(message: str, destination: Optional[str] = None, 
                 priority: Optional[int] = None, title: Optional[str] = None) -> List[bool]:
    """Send a Pushover message using the global PyLogger instance."""
    instance = PyLogger.get_instance()
    if instance:
        return instance.send_pushover(message, destination, priority, title)
    
    # Fallback: try to get from root logger
    root_logger = logging.getLogger()
    if hasattr(root_logger, 'pylogger'):
        return root_logger.pylogger.send_pushover(message, destination, priority, title)
    
    return [False]


def send_email(subject: str, message: str, to_emails: Optional[List[str]] = None) -> bool:
    """Send an email using the global PyLogger instance."""
    instance = PyLogger.get_instance()
    if instance:
        return instance.send_email(subject, message, to_emails)
    
    # Fallback: try to get from root logger
    root_logger = logging.getLogger()
    if hasattr(root_logger, 'pylogger'):
        return root_logger.pylogger.send_email(subject, message, to_emails)
    
    return False