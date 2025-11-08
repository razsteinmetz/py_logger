"""
Simple demonstration script for PyLogger.

This script shows PyLogger working with basic configuration.
Run this to verify the installation and basic functionality.
"""

from py_logger import PyLogger
import os

def main():
    print("=" * 60)
    print("🎉 PyLogger Demonstration")
    print("=" * 60)
    
    # Create a simple configuration
    config = {
        "console": {
            "enabled": True,
            "level": "INFO",
            "format": "%(asctime)s | %(levelname)-8s | %(message)s"
        },
        "file": {
            "enabled": True,
            "level": "DEBUG",
            "filename": "pylogger_demo.log",
            "max_size": 1048576,  # 1MB
            "backup_count": 3,
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
        }
    }
    
    # Initialize PyLogger
    print("📋 Initializing PyLogger...")
    logger = PyLogger(config=config, name="PyLoggerDemo")
    
    # Show configuration status
    print(f"✅ Available destinations: {logger.get_destinations()}")
    print(f"✅ Enabled destinations: {logger.get_enabled_destinations()}")
    print()
    
    # Demonstrate different log levels
    print("📝 Testing different log levels:")
    logger.debug("This is a DEBUG message (file only)")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    
    print()
    print("🔧 Testing runtime configuration changes:")
    
    # Test runtime changes
    logger.disable_destination('console')
    logger.info("This message won't appear in console (console disabled)")
    
    logger.enable_destination('console')
    logger.info("Console logging re-enabled!")
    
    # Test configuration update
    logger.update_config({
        'console': {
            'format': '🚀 %(levelname)s: %(message)s'
        }
    })
    logger.warning("This warning has a new format!")
    
    print()
    print("📊 Testing destination status:")
    for dest in ['console', 'file', 'telegram', 'pushover', 'email']:
        status = "enabled" if logger.is_destination_enabled(dest) else "disabled"
        print(f"  {dest}: {status}")
    
    print()
    print("🎯 Demonstrating exception logging:")
    try:
        # Simulate an error
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("Caught an exception with full traceback")
    
    # Show file output information
    print()
    print(f"📁 Log file created: pylogger_demo.log")
    if os.path.exists("pylogger_demo.log"):
        size = os.path.getsize("pylogger_demo.log")
        print(f"📏 Log file size: {size} bytes")
    
    print()
    print("=" * 60)
    print("✅ PyLogger demonstration completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Check 'pylogger_demo.log' for complete log output")
    print("2. Explore examples/ directory for more advanced usage")
    print("3. See docs/ for full API documentation")
    print("4. Configure Telegram/Pushover/Email for notifications")

if __name__ == "__main__":
    main()