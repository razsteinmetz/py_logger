"""
YAML configuration example for PyLogger.

Demonstrates loading configuration from a YAML file.
"""

from py_logger import PyLogger
import os

def main():
    print("YAML Configuration Example")
    print("=" * 40)
    
    # Check if example config exists
    config_path = "example_config.yaml"
    
    if not os.path.exists(config_path):
        print(f"Config file '{config_path}' not found.")
        print("Please copy and customize 'example_config.yaml' from the examples directory.")
        return
    
    # Load logger from YAML file
    try:
        logger = PyLogger(config_path=config_path, name="YAMLConfigExample")
        
        print(f"Configuration loaded from: {config_path}")
        print(f"Available destinations: {logger.get_destinations()}")
        print(f"Enabled destinations: {logger.get_enabled_destinations()}")
        print()
        
        # Test logging
        logger.debug("Debug message from YAML config example")
        logger.info("Application started with YAML configuration")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        
        # Test each destination if enabled
        enabled_dests = logger.get_enabled_destinations()
        
        if 'telegram' in enabled_dests:
            logger.send_telegram("🎯 Test message from YAML config example")
        
        if 'pushover' in enabled_dests:
            logger.send_pushover("Test notification from YAML config", title="PyLogger Test")
        
        if 'email' in enabled_dests:
            logger.send_email("Test from PyLogger", "This is a test email from the YAML config example")
        
        logger.info("YAML configuration example completed")
        
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print("Please check your YAML file format and environment variables.")

if __name__ == "__main__":
    main()