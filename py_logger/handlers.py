"""
Custom handlers for different logging destinations.

Provides handler classes for Telegram, Pushover, Email, rotating files, and console.
"""

import logging
import smtplib
import requests
import json
from typing import Dict, Any, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging.handlers import RotatingFileHandler as StandardRotatingFileHandler
from pathlib import Path


class BaseDestinationHandler(logging.Handler):
    """Base class for all destination handlers."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.enabled = config.get('enabled', False)
        
        # Set log level
        level = config.get('level', 'INFO').upper()
        self.setLevel(getattr(logging, level))
        
        # Set formatter
        format_string = config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        date_format = config.get('date_format', '%Y-%m-%d %H:%M:%S')
        formatter = logging.Formatter(format_string, date_format)
        self.setFormatter(formatter)
    
    def emit(self, record: logging.LogRecord) -> None:
        """Override this method in subclasses."""
        if not self.enabled:
            return
        super().emit(record)


class ConsoleHandler(BaseDestinationHandler):
    """Console logging handler."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record to console."""
        if not self.enabled:
            return
        self.stream_handler.emit(record)
    
    def setLevel(self, level) -> None:
        """Set log level for both this handler and the stream handler."""
        super().setLevel(level)
        if hasattr(self, 'stream_handler'):
            self.stream_handler.setLevel(level)


class RotatingFileHandler(BaseDestinationHandler):
    """Rotating file logging handler."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        filename = config.get('filename', 'app.log')
        max_size = config.get('max_size', 10485760)  # 10MB
        backup_count = config.get('backup_count', 5)
        
        # Create directory if it doesn't exist
        log_path = Path(filename)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.file_handler = StandardRotatingFileHandler(
            filename=filename,
            maxBytes=max_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        self.file_handler.setFormatter(self.formatter)
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record to file."""
        if not self.enabled:
            return
        self.file_handler.emit(record)
    
    def setLevel(self, level) -> None:
        """Set log level for both this handler and the file handler."""
        super().setLevel(level)
        if hasattr(self, 'file_handler'):
            self.file_handler.setLevel(level)


class TelegramHandler(BaseDestinationHandler):
    """Telegram logging handler."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.bot_token = config.get('bot_token', '')
        self.chat_id = config.get('chat_id', '')
        self.parse_mode = config.get('parse_mode', 'HTML')
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record to Telegram."""
        if not self.enabled or not self.bot_token or not self.chat_id:
            return
        
        try:
            message = self.format(record)
            self._send_telegram_message(message)
        except Exception as e:
            # Don't let handler exceptions break the application
            print(f"TelegramHandler error: {e}")
    
    def _send_telegram_message(self, message: str, parse_mode: Optional[str] = None) -> bool:
        """Send a message to Telegram."""
        if not self.bot_token or not self.chat_id:
            return False
        
        data = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': parse_mode or self.parse_mode
        }
        
        try:
            response = requests.post(self.api_url, data=data, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Failed to send Telegram message: {e}")
            return False
    
    def send_direct_message(self, message: str, parse_mode: Optional[str] = None) -> bool:
        """Send a direct message bypassing log level."""
        return self._send_telegram_message(message, parse_mode)


class PushoverHandler(BaseDestinationHandler):
    """Pushover logging handler."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.destinations = config.get('destinations', [])
        self.api_url = "https://api.pushover.net/1/messages.json"
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record to Pushover."""
        if not self.enabled or not self.destinations:
            return
        
        try:
            message = self.format(record)
            title = f"{record.levelname}: {record.name}"
            self._send_to_all_destinations(message, title)
        except Exception as e:
            print(f"PushoverHandler error: {e}")
    
    def _send_pushover_message(self, destination: Dict[str, Any], message: str, 
                              title: Optional[str] = None, priority: Optional[int] = None) -> bool:
        """Send a message to a Pushover destination."""
        user_key = destination.get('user_key')
        api_token = destination.get('api_token')
        
        if not user_key or not api_token:
            return False
        
        data = {
            'token': api_token,
            'user': user_key,
            'message': message,
            'title': title or 'Application Log',
            'priority': priority if priority is not None else destination.get('priority', 0)
        }
        
        try:
            response = requests.post(self.api_url, data=data, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Failed to send Pushover message to {destination.get('name', 'unknown')}: {e}")
            return False
    
    def _send_to_all_destinations(self, message: str, title: Optional[str] = None, 
                                 priority: Optional[int] = None) -> List[bool]:
        """Send message to all configured Pushover destinations."""
        results = []
        for destination in self.destinations:
            result = self._send_pushover_message(destination, message, title, priority)
            results.append(result)
        return results
    
    def send_direct_message(self, message: str, destination: Optional[str] = None, 
                           priority: Optional[int] = None, title: Optional[str] = None) -> List[bool]:
        """Send a direct message bypassing log level."""
        if destination:
            # Send to specific destination
            dest_config = None
            for dest in self.destinations:
                if dest.get('name') == destination:
                    dest_config = dest
                    break
            
            if dest_config:
                return [self._send_pushover_message(dest_config, message, title, priority)]
            else:
                print(f"Pushover destination '{destination}' not found")
                return [False]
        else:
            # Send to all destinations
            return self._send_to_all_destinations(message, title, priority)


class EmailHandler(BaseDestinationHandler):
    """Email logging handler."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.smtp_server = config.get('smtp_server', '')
        self.smtp_port = config.get('smtp_port', 587)
        self.use_tls = config.get('use_tls', True)
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.from_email = config.get('from_email', '')
        self.to_emails = config.get('to_emails', [])
        self.subject_prefix = config.get('subject_prefix', '[ALERT]')
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record to email."""
        if not self.enabled or not self._is_configured():
            return
        
        try:
            message = self.format(record)
            subject = f"{self.subject_prefix} {record.levelname}: {record.name}"
            self._send_email(subject, message)
        except Exception as e:
            print(f"EmailHandler error: {e}")
    
    def _is_configured(self) -> bool:
        """Check if email handler is properly configured."""
        required_fields = [
            self.smtp_server, self.username, self.password, 
            self.from_email, self.to_emails
        ]
        return all(required_fields)
    
    def _send_email(self, subject: str, message: str, to_emails: Optional[List[str]] = None) -> bool:
        """Send an email."""
        if not self._is_configured():
            return False
        
        recipients = to_emails or self.to_emails
        if not recipients:
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def send_direct_message(self, subject: str, message: str, to_emails: Optional[List[str]] = None) -> bool:
        """Send a direct email bypassing log level."""
        full_subject = f"{self.subject_prefix} {subject}" if not subject.startswith(self.subject_prefix) else subject
        return self._send_email(full_subject, message, to_emails)