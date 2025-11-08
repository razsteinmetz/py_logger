"""
Standard Library Integration Example for PyLogger.

This example demonstrates how PyLogger integrates seamlessly with 
Python's standard logging library using PyLogger.setup().
"""

import sys
import os
# Add parent directory to Python path
sys.path.insert(0, 'c:/Users/raz/OneDrive - Sage/Pycharm/PycharmProjects/py_logger')

from py_logger import PyLogger, send_telegram, send_pushover, send_email
import logging

# Configuration for PyLogger - simpler structure for this example
config = {
    'destinations': {
        'console': {
            'enabled': True,
            'level': 'DEBUG'
        },
        'file': {
            'enabled': True, 
            'level': 'INFO',
            'filename': 'standard_integration.log',
            'max_size': 1048576,
            'backup_count': 3
        },
        'telegram': {
            'enabled': False,  # Set to True and add credentials to test
            'level': 'ERROR',
            'bot_token': '${TELEGRAM_BOT_TOKEN}',
            'chat_id': '${TELEGRAM_CHAT_ID}'
        }
    }
}


def simulate_business_module():
    """Simulate a business logic module using standard logging."""
    print("\n--- Simulating business_module.py ---")
    
    # This is how any module in your project would get a logger
    logger = logging.getLogger(__name__ + '.business')
    
    logger.debug("Processing business logic...")
    logger.info("User authentication successful")
    logger.warning("API rate limit approaching") 
    logger.error("Database connection failed, retrying...")
    
    print("Business module used standard logging.getLogger() - no PyLogger imports needed!")


def simulate_utils_module():
    """Simulate a utilities module using standard logging."""
    print("\n--- Simulating utils.py ---")
    
    # Standard Python logging - works seamlessly with PyLogger
    logger = logging.getLogger(__name__ + '.utils')
    
    logger.debug("Utility function called")
    logger.info("File processing completed")
    logger.warning("Temporary file cleanup needed")
    
    print("Utils module also used standard logging.getLogger() seamlessly!")


if __name__ == "__main__":
    print("PyLogger Standard Library Integration Example")
    print("=" * 50)
    print("Key benefits:")
    print("- One-time setup with PyLogger.setup()")
    print("- Standard logging.getLogger() works everywhere")
    print("- Automatic module name detection") 
    print("- Direct messaging available from any module")
    print("- Zero learning curve for existing Python developers")
    
    print("\n1. Setting up PyLogger with standard library integration...")
    
    # ONE-TIME SETUP: Configure PyLogger to integrate with standard logging
    PyLogger.setup(config=config)
    print("   PyLogger.setup() called - standard logging is now enhanced!")
    
    print("\n2. Now any module can use standard logging.getLogger()...")
    
    # From this point forward, any module can use standard logging
    # and it will automatically use PyLogger's enhanced functionality
    
    # Demonstrate main module logging
    main_logger = logging.getLogger(__name__)
    main_logger.info("Main application started")
    main_logger.warning("This is a warning from main")
    main_logger.error("This is an error from main") 
    
    # Simulate other modules using standard logging
    simulate_business_module()
    simulate_utils_module()
    
    print("\n" + "=" * 50)
    print("Integration Complete!")
    print()
    print("What happened:")
    print("1. PyLogger.setup(config) was called once")
    print("2. All subsequent logging.getLogger() calls automatically use PyLogger")
    print("3. Each logger gets appropriate module name automatically")
    print("4. No PyLogger imports needed in other modules")
    print("5. Direct messaging functions available globally")
    print()
    print("Check 'standard_integration.log' file for logged messages!")