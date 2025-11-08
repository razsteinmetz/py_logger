"""
Simple tests for PyLogger package.

Run with: python -m pytest tests/
"""

import pytest
import tempfile
import os
from pathlib import Path

from py_logger import PyLogger, LoggerConfig
from py_logger.config import ConfigValidationError


class TestLoggerConfig:
    """Test configuration management."""
    
    def test_default_config(self):
        """Test default configuration loading."""
        config = LoggerConfig()
        assert config.is_destination_enabled('console') == True
        assert config.is_destination_enabled('file') == False
        assert config.get_log_level('console') == 'INFO'
    
    def test_dict_config(self):
        """Test dictionary configuration."""
        test_config = {
            'console': {'enabled': True, 'level': 'DEBUG'},
            'file': {'enabled': True, 'level': 'INFO', 'filename': 'test.log'}
        }
        config = LoggerConfig(config=test_config)
        assert config.is_destination_enabled('console') == True
        assert config.is_destination_enabled('file') == True
        assert config.get_log_level('console') == 'DEBUG'
    
    def test_yaml_config(self):
        """Test YAML configuration loading."""
        yaml_content = """
console:
  enabled: true
  level: WARNING

file:
  enabled: true
  level: DEBUG
  filename: test.log
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            f.flush()
            
            config = LoggerConfig(config_path=f.name)
            assert config.is_destination_enabled('console') == True
            assert config.get_log_level('console') == 'WARNING'
            
            # Clean up
            os.unlink(f.name)
    
    def test_invalid_config(self):
        """Test invalid configuration handling."""
        with pytest.raises(ConfigValidationError):
            LoggerConfig(config={'invalid_destination': {'enabled': True}})
    
    def test_enable_disable_destination(self):
        """Test runtime enable/disable of destinations."""
        config = LoggerConfig()
        
        # Initially file is disabled
        assert config.is_destination_enabled('file') == False
        
        # Enable file destination
        config.enable_destination('file')
        assert config.is_destination_enabled('file') == True
        
        # Disable it again
        config.disable_destination('file')
        assert config.is_destination_enabled('file') == False


class TestPyLogger:
    """Test PyLogger main functionality."""
    
    def test_basic_initialization(self):
        """Test basic logger initialization."""
        logger = PyLogger(name="TestLogger")
        assert logger.name == "TestLogger"
        assert 'console' in logger.get_destinations()
    
    def test_dict_config_initialization(self):
        """Test initialization with dictionary config."""
        config = {
            'console': {'enabled': True, 'level': 'INFO'},
            'file': {'enabled': True, 'level': 'DEBUG', 'filename': 'test.log'}
        }
        logger = PyLogger(config=config)
        assert logger.is_destination_enabled('console') == True
        assert logger.is_destination_enabled('file') == True
    
    def test_logging_methods(self):
        """Test standard logging methods."""
        logger = PyLogger(name="TestLogger")
        
        # These should not raise exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
    
    def test_destination_management(self):
        """Test destination enable/disable at runtime."""
        config = {
            'console': {'enabled': True, 'level': 'INFO'},
            'file': {'enabled': False, 'level': 'DEBUG', 'filename': 'test.log'}
        }
        logger = PyLogger(config=config)
        
        # Initially file is disabled
        assert logger.is_destination_enabled('file') == False
        
        # Enable file destination
        logger.enable_destination('file')
        assert logger.is_destination_enabled('file') == True
        
        # Disable console
        logger.disable_destination('console')
        assert logger.is_destination_enabled('console') == False
    
    def test_level_setting(self):
        """Test setting log levels at runtime."""
        logger = PyLogger()
        
        # This should not raise an exception
        logger.set_level('console', 'DEBUG')
        logger.set_level('console', 10)  # Numeric level
    
    def test_config_update(self):
        """Test runtime configuration updates."""
        logger = PyLogger()
        
        new_config = {
            'console': {'level': 'ERROR'},
            'file': {'enabled': True, 'level': 'DEBUG', 'filename': 'updated.log'}
        }
        
        # This should not raise an exception
        logger.update_config(new_config)
        assert logger.is_destination_enabled('file') == True
    
    def test_context_manager(self):
        """Test context manager functionality."""
        config = {'console': {'enabled': True, 'level': 'INFO'}}
        
        with PyLogger(config=config) as logger:
            assert logger is not None
            logger.info("Test message in context")
    
    def test_direct_messages_without_credentials(self):
        """Test direct message methods without credentials (should fail gracefully)."""
        logger = PyLogger()
        
        # These should return False but not raise exceptions
        assert logger.send_telegram("Test message") == False
        assert logger.send_pushover("Test message") == [False]
        assert logger.send_email("Test Subject", "Test message") == False


def test_package_imports():
    """Test that all package imports work correctly."""
    from py_logger import PyLogger, LoggerConfig
    from py_logger.handlers import (
        TelegramHandler, PushoverHandler, EmailHandler,
        RotatingFileHandler, ConsoleHandler
    )
    from py_logger.config import ConfigValidationError
    
    # All imports should work without errors
    assert PyLogger is not None
    assert LoggerConfig is not None


if __name__ == "__main__":
    # Simple test runner
    import sys
    
    print("Running basic PyLogger tests...")
    
    try:
        # Test configuration
        print("Testing configuration...")
        config = LoggerConfig()
        assert config.is_destination_enabled('console')
        print("✓ Configuration tests passed")
        
        # Test basic logger
        print("Testing logger...")
        logger = PyLogger(name="TestRun")
        logger.info("Test message")
        print("✓ Logger tests passed")
        
        # Test imports
        print("Testing imports...")
        test_package_imports()
        print("✓ Import tests passed")
        
        print("\n🎉 All basic tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)