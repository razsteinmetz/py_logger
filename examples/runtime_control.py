"""
Runtime control example for PyLogger.

Demonstrates dynamic enable/disable of destinations and configuration updates.
"""

from py_logger import PyLogger
import time

def main():
    # Start with minimal configuration
    config = {
        "console": {
            "enabled": True,
            "level": "INFO"
        },
        "file": {
            "enabled": False,  # Start disabled
            "level": "DEBUG",
            "filename": "runtime_control.log"
        },
        "telegram": {
            "enabled": False,  # Start disabled
            "level": "ERROR",
            "bot_token": "dummy_token",
            "chat_id": "dummy_chat_id"
        }
    }
    
    logger = PyLogger(config=config, name="RuntimeControlExample")
    
    print("Runtime Control Example")
    print("=" * 50)
    
    # Initial state
    print(f"Initial enabled destinations: {logger.get_enabled_destinations()}")
    logger.info("Starting with minimal configuration")
    
    # Enable file logging at runtime
    print("\n1. Enabling file logging...")
    logger.enable_destination('file')
    print(f"Enabled destinations: {logger.get_enabled_destinations()}")
    logger.info("File logging has been enabled")
    logger.debug("This debug message now goes to file")
    
    # Change log levels at runtime
    print("\n2. Changing console log level to DEBUG...")
    logger.set_level('console', 'DEBUG')
    logger.debug("This debug message now appears in console too")
    
    # Disable and re-enable destinations
    print("\n3. Temporarily disabling console...")
    logger.disable_destination('console')
    logger.info("This message only goes to file (console disabled)")
    
    print("4. Re-enabling console...")
    logger.enable_destination('console') 
    logger.info("Console logging restored")
    
    # Update configuration at runtime
    print("\n5. Updating configuration...")
    new_config = {
        "console": {
            "format": "🚀 %(levelname)s: %(message)s",
            "level": "WARNING"
        },
        "file": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    }
    
    logger.update_config(new_config)
    logger.info("This info message won't show in console (now WARNING level)")
    logger.warning("But this warning will show with new format")
    
    # Check destination status
    print("\n6. Destination status check...")
    for dest in ['console', 'file', 'telegram']:
        status = "enabled" if logger.is_destination_enabled(dest) else "disabled"
        print(f"  {dest}: {status}")
    
    # Simulate a monitoring scenario
    print("\n7. Simulating monitoring scenario...")
    
    for i in range(3):
        logger.info(f"Processing item {i+1}")
        time.sleep(0.1)  # Brief pause
        
        if i == 1:  # Simulate an issue
            logger.warning(f"Issue detected with item {i+1}")
    
    # Test configuration saving
    print("\n8. Saving current configuration...")
    logger.save_config("runtime_generated_config.yaml")
    print("Configuration saved to 'runtime_generated_config.yaml'")
    
    # Display current configuration
    print("\n9. Current configuration:")
    current_config = logger.get_config()
    for dest, conf in current_config.items():
        if conf.get('enabled'):
            level = conf.get('level', 'N/A')
            print(f"  {dest}: enabled, level={level}")
        else:
            print(f"  {dest}: disabled")
    
    logger.info("Runtime control example completed")

if __name__ == "__main__":
    main()