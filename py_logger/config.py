"""
Configuration management for PyLogger.

Handles loading and validation of configuration from YAML files or dictionaries.
"""

import yaml
import os
from typing import Dict, Any, Optional, List
from pathlib import Path


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


class LoggerConfig:
    """Manages logger configuration loading and validation."""
    
    # Default configuration structure
    DEFAULT_CONFIG = {
        'console': {
            'enabled': True,
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'date_format': '%Y-%m-%d %H:%M:%S'
        },
        'file': {
            'enabled': False,
            'level': 'DEBUG',
            'filename': 'app.log',
            'max_size': 10485760,  # 10MB
            'backup_count': 5,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'date_format': '%Y-%m-%d %H:%M:%S'
        },
        'telegram': {
            'enabled': False,
            'level': 'ERROR',
            'bot_token': '',
            'chat_id': '',
            'format': '🔴 %(levelname)s: %(message)s',
            'parse_mode': 'HTML'
        },
        'pushover': {
            'enabled': False,
            'level': 'WARNING',
            'destinations': [],
            'format': '%(levelname)s: %(message)s'
        },
        'email': {
            'enabled': False,
            'level': 'CRITICAL',
            'smtp_server': '',
            'smtp_port': 587,
            'use_tls': True,
            'username': '',
            'password': '',
            'from_email': '',
            'to_emails': [],
            'subject_prefix': '[ALERT]',
            'format': '%(asctime)s - %(levelname)s: %(message)s',
            'date_format': '%Y-%m-%d %H:%M:%S'
        }
    }
    
    VALID_LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    VALID_DESTINATIONS = ['console', 'file', 'telegram', 'pushover', 'email']
    
    def __init__(self, config_path: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to YAML configuration file
            config: Dictionary configuration
        """
        self.config_path = config_path
        self.config = self._load_config(config_path, config)
        self._validate_config()
    
    def _load_config(self, config_path: Optional[str], config_dict: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Load configuration from file or dictionary."""
        if config_path and config_dict:
            raise ConfigValidationError("Cannot specify both config_path and config dictionary")
        
        if config_path:
            return self._load_from_yaml(config_path)
        elif config_dict:
            return self._merge_config(config_dict)
        else:
            return self.DEFAULT_CONFIG.copy()
    
    def _load_from_yaml(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise ConfigValidationError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                yaml_config = yaml.safe_load(file)
            
            # Expand environment variables
            yaml_config = self._expand_env_vars(yaml_config)
            
            return self._merge_config(yaml_config or {})
            
        except yaml.YAMLError as e:
            raise ConfigValidationError(f"Invalid YAML configuration: {e}")
        except Exception as e:
            raise ConfigValidationError(f"Error loading configuration file: {e}")
    
    def _expand_env_vars(self, config: Any) -> Any:
        """Recursively expand environment variables in configuration."""
        if isinstance(config, dict):
            return {key: self._expand_env_vars(value) for key, value in config.items()}
        elif isinstance(config, list):
            return [self._expand_env_vars(item) for item in config]
        elif isinstance(config, str) and config.startswith('${') and config.endswith('}'):
            env_var = config[2:-1]
            return os.getenv(env_var, config)
        else:
            return config
    
    def _merge_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge user configuration with defaults."""
        merged = self.DEFAULT_CONFIG.copy()
        
        # Handle both flat and nested 'destinations' structure
        if 'destinations' in user_config:
            # Nested structure: config = {'destinations': {'console': {...}, 'file': {...}}}
            destinations_config = user_config['destinations']
        else:
            # Flat structure: config = {'console': {...}, 'file': {...}}
            destinations_config = user_config
        
        for destination in self.VALID_DESTINATIONS:
            if destination in destinations_config:
                if destination in merged:
                    merged[destination].update(destinations_config[destination])
                else:
                    merged[destination] = destinations_config[destination]
        
        return merged
    
    def _validate_config(self) -> None:
        """Validate the configuration structure and values."""
        if not isinstance(self.config, dict):
            raise ConfigValidationError("Configuration must be a dictionary")
        
        for destination in self.config:
            if destination not in self.VALID_DESTINATIONS:
                raise ConfigValidationError(f"Invalid destination: {destination}")
            
            dest_config = self.config[destination]
            if not isinstance(dest_config, dict):
                raise ConfigValidationError(f"Configuration for {destination} must be a dictionary")
            
            # Validate log level
            if 'level' in dest_config:
                level = dest_config['level'].upper()
                if level not in self.VALID_LOG_LEVELS:
                    raise ConfigValidationError(f"Invalid log level for {destination}: {level}")
            
            # Validate destination-specific configurations
            self._validate_destination_config(destination, dest_config)
    
    def _validate_destination_config(self, destination: str, config: Dict[str, Any]) -> None:
        """Validate destination-specific configuration."""
        if destination == 'file':
            if config.get('enabled', False):
                if not config.get('filename'):
                    raise ConfigValidationError("File destination requires 'filename'")
                
                max_size = config.get('max_size', 0)
                if not isinstance(max_size, int) or max_size <= 0:
                    raise ConfigValidationError("File 'max_size' must be a positive integer")
                
                backup_count = config.get('backup_count', 0)
                if not isinstance(backup_count, int) or backup_count < 0:
                    raise ConfigValidationError("File 'backup_count' must be a non-negative integer")
        
        elif destination == 'telegram':
            if config.get('enabled', False):
                if not config.get('bot_token'):
                    raise ConfigValidationError("Telegram destination requires 'bot_token'")
                if not config.get('chat_id'):
                    raise ConfigValidationError("Telegram destination requires 'chat_id'")
        
        elif destination == 'pushover':
            if config.get('enabled', False):
                destinations = config.get('destinations', [])
                if not destinations:
                    raise ConfigValidationError("Pushover destination requires at least one destination")
                
                for idx, dest in enumerate(destinations):
                    if not isinstance(dest, dict):
                        raise ConfigValidationError(f"Pushover destination {idx} must be a dictionary")
                    if not dest.get('user_key'):
                        raise ConfigValidationError(f"Pushover destination {idx} requires 'user_key'")
                    if not dest.get('api_token'):
                        raise ConfigValidationError(f"Pushover destination {idx} requires 'api_token'")
        
        elif destination == 'email':
            if config.get('enabled', False):
                required_fields = ['smtp_server', 'username', 'password', 'from_email', 'to_emails']
                for field in required_fields:
                    if not config.get(field):
                        raise ConfigValidationError(f"Email destination requires '{field}'")
                
                to_emails = config.get('to_emails', [])
                if not isinstance(to_emails, list) or not to_emails:
                    raise ConfigValidationError("Email 'to_emails' must be a non-empty list")
                
                smtp_port = config.get('smtp_port', 587)
                if not isinstance(smtp_port, int) or smtp_port <= 0:
                    raise ConfigValidationError("Email 'smtp_port' must be a positive integer")
    
    def get_destination_config(self, destination: str) -> Dict[str, Any]:
        """Get configuration for a specific destination."""
        if destination not in self.VALID_DESTINATIONS:
            raise ValueError(f"Invalid destination: {destination}")
        
        return self.config.get(destination, {})
    
    def is_destination_enabled(self, destination: str) -> bool:
        """Check if a destination is enabled."""
        dest_config = self.get_destination_config(destination)
        return dest_config.get('enabled', False)
    
    def get_log_level(self, destination: str) -> str:
        """Get log level for a destination."""
        dest_config = self.get_destination_config(destination)
        return dest_config.get('level', 'INFO').upper()
    
    def enable_destination(self, destination: str) -> None:
        """Enable a destination at runtime."""
        if destination not in self.VALID_DESTINATIONS:
            raise ValueError(f"Invalid destination: {destination}")
        
        if destination not in self.config:
            self.config[destination] = self.DEFAULT_CONFIG[destination].copy()
        
        self.config[destination]['enabled'] = True
    
    def disable_destination(self, destination: str) -> None:
        """Disable a destination at runtime."""
        if destination in self.config:
            self.config[destination]['enabled'] = False
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Update configuration at runtime."""
        # Merge the new configuration
        for destination, dest_config in new_config.items():
            if destination in self.VALID_DESTINATIONS:
                if destination in self.config:
                    self.config[destination].update(dest_config)
                else:
                    self.config[destination] = dest_config
        
        # Re-validate the updated configuration
        self._validate_config()
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self.config.copy()
    
    def save_to_yaml(self, file_path: str) -> None:
        """Save current configuration to YAML file."""
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.config, file, default_flow_style=False, indent=2)