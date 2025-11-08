"""
Full configuration example for PyLogger.

Demonstrates all available destinations and features.
Note: You'll need to set up your API keys and credentials for this to work.
"""

import os
from py_logger import PyLogger

def main():
    # Full configuration with all destinations
    config = {
        "console": {
            "enabled": True,
            "level": "INFO",
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        },
        "file": {
            "enabled": True,
            "level": "DEBUG", 
            "filename": "full_example.log",
            "max_size": 5242880,  # 5MB
            "backup_count": 5,
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
        },
        "telegram": {
            "enabled": True,  # Make sure you have valid credentials
            "level": "ERROR",
            "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here"),
            "chat_id": os.getenv("TELEGRAM_CHAT_ID", "your_chat_id_here"),
            "format": "🔴 <b>%(levelname)s</b>: %(message)s\n<i>App: %(name)s</i>",
            "parse_mode": "HTML"
        },
        "pushover": {
            "enabled": True,  # Make sure you have valid credentials
            "level": "WARNING",
            "format": "%(levelname)s: %(message)s\nApp: %(name)s",
            "destinations": [
                {
                    "name": "primary",
                    "user_key": os.getenv("PUSHOVER_USER_KEY", "your_user_key_here"),
                    "api_token": os.getenv("PUSHOVER_API_TOKEN", "your_api_token_here"),
                    "priority": 1
                }
            ]
        },
        "email": {
            "enabled": True,  # Make sure you have valid SMTP settings
            "level": "CRITICAL",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "use_tls": True,
            "username": os.getenv("EMAIL_USERNAME", "your_email@gmail.com"),
            "password": os.getenv("EMAIL_PASSWORD", "your_app_password"),
            "from_email": os.getenv("EMAIL_USERNAME", "your_email@gmail.com"),
            "to_emails": [
                os.getenv("ALERT_EMAIL", "admin@company.com")
            ],
            "subject_prefix": "[FULL EXAMPLE ALERT]"
        }
    }
    
    # Initialize logger with configuration
    logger = PyLogger(config=config, name="FullExampleApp")
    
    print("PyLogger Full Example")
    print(f"Available destinations: {logger.get_destinations()}")
    print(f"Enabled destinations: {logger.get_enabled_destinations()}")
    print()
    
    # Test different log levels
    logger.debug("Debug message - only visible in file")
    logger.info("Info message - console and file")
    logger.warning("Warning message - console, file, and pushover")
    logger.error("Error message - console, file, pushover, and telegram")
    
    # Test direct messages (bypass log levels)
    print("Sending direct messages...")
    
    # Direct Telegram message
    if logger.is_destination_enabled('telegram'):
        success = logger.send_telegram("🚀 Direct Telegram message from PyLogger!")
        print(f"Telegram direct message: {'✓' if success else '✗'}")
    
    # Direct Pushover message
    if logger.is_destination_enabled('pushover'):
        results = logger.send_pushover(
            "Direct Pushover message from PyLogger!",
            title="PyLogger Test",
            priority=0
        )
        success = any(results)
        print(f"Pushover direct message: {'✓' if success else '✗'}")
    
    # Direct email
    if logger.is_destination_enabled('email'):
        success = logger.send_email(
            "PyLogger Test Email",
            "This is a direct email message from PyLogger!\n\nIt bypasses the log level restrictions."
        )
        print(f"Email direct message: {'✓' if success else '✗'}")
    
    # Test runtime configuration changes
    print("\nTesting runtime configuration changes...")
    
    # Temporarily disable console logging
    logger.disable_destination('console')
    logger.info("This message won't appear in console")
    
    # Re-enable console logging
    logger.enable_destination('console')
    logger.info("Console logging re-enabled")
    
    # Change log level for a destination
    logger.set_level('file', 'WARNING')
    logger.info("This info message won't go to file (now WARNING level)")
    logger.warning("This warning will go to file")
    
    # Test destination testing
    print("\nTesting all destinations...")
    test_results = logger.test_destinations()
    for destination, success in test_results.items():
        status = "✓" if success else "✗"
        print(f"  {destination}: {status}")
    
    # Simulate a critical error
    try:
        raise ValueError("Simulated critical error for demonstration")
    except ValueError:
        logger.critical("Critical error occurred!")
        logger.exception("Exception details")
    
    logger.info("Full example completed")

if __name__ == "__main__":
    main()