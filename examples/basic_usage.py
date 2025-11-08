"""
Basic usage example for PyLogger.

Demonstrates simple console and file logging.
"""

from py_logger import PyLogger

def main():
    # Configuration using dictionary
    config = {
        "console": {
            "enabled": True,
            "level": "INFO",
            "format": "%(asctime)s | %(levelname)-8s | %(message)s"
        },
        "file": {
            "enabled": True,
            "level": "DEBUG",
            "filename": "example_app.log",
            "max_size": 1048576,  # 1MB
            "backup_count": 3
        }
    }
    
    # Initialize logger
    logger = PyLogger(config=config, name="ExampleApp")
    
    # Basic logging
    logger.info("Application started")
    logger.debug("Debug information - only goes to file")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    try:
        # Simulate an operation that might fail
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("Division by zero error occurred")
    
    # Check which destinations are enabled
    print(f"Available destinations: {logger.get_destinations()}")
    print(f"Enabled destinations: {logger.get_enabled_destinations()}")
    
    logger.info("Application finished")

if __name__ == "__main__":
    main()