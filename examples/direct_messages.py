"""
Direct messages example for PyLogger.

Demonstrates sending direct messages that bypass log level restrictions.
"""

import os
from py_logger import PyLogger

def main():
    # Configuration with high log levels to demonstrate bypassing
    config = {
        "console": {
            "enabled": True,
            "level": "ERROR"  # High level - info/warning won't show
        },
        "telegram": {
            "enabled": True,
            "level": "CRITICAL",  # Very high level
            "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", "Bot Token Here"),
            "chat_id": os.getenv("TELEGRAM_CHAT_ID", "Chat_id here")
        },
        "pushover": {
            "enabled": True,
            "level": "CRITICAL",  # Very high level
            "destinations": [
                {
                    "name": "admin",
                    "user_key": os.getenv("PUSHOVER_USER_KEY", "user_key_here"),
                    "api_token": os.getenv("PUSHOVER_API_TOKEN", "api_token_here"),
                    "priority": 0
                }
            ]
        },
        "email": {
            "enabled": True,
            "level": "CRITICAL",  # Very high level
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "username": os.getenv("EMAIL_USERNAME", "your_email@gmail.com"),
            "password": os.getenv("EMAIL_PASSWORD", "your_password"),
            "from_email": os.getenv("EMAIL_USERNAME", "your_email@gmail.com"),
            "to_emails": [os.getenv("ALERT_EMAIL", "admin@company.com")]
        }
    }
    
    logger = PyLogger(config=config, name="DirectMessageExample")
    
    print("Direct Messages Example")
    print("=" * 40)
    print("All destinations are set to CRITICAL level")
    print("Normal logging won't trigger notifications")
    print()
    
    # These won't trigger notifications due to high log levels
    print("1. Normal logging (won't trigger notifications):")
    logger.info("This info message won't trigger any notifications")
    logger.warning("This warning won't trigger notifications either")
    logger.error("Even this error won't trigger notifications")
    
    print("\n2. Direct messages (bypass log levels):")
    
    # Direct Telegram message
    if logger.is_destination_enabled('telegram'):
        print("   Sending direct Telegram message...")
        success = logger.send_telegram(
            "🔔 <b>Direct Alert!</b>\nThis message bypasses log levels.\n<i>Sent via PyLogger</i>",
            parse_mode="HTML"
        )
        print(f"   Telegram: {'✓ Sent' if success else '✗ Failed'}")
    
    # Direct Pushover messages
    if logger.is_destination_enabled('pushover'):
        print("   Sending direct Pushover messages...")
        
        # Send to all destinations
        results = logger.send_pushover(
            "Direct Pushover alert! This bypasses log level restrictions.",
            title="PyLogger Direct Alert",
            priority=1  # High priority
        )
        success = any(results)
        print(f"   Pushover (all): {'✓ Sent' if success else '✗ Failed'}")
        
        # Send to specific destination
        results = logger.send_pushover(
            "This message is sent to admin destination only.",
            destination="admin",
            title="Admin Alert",
            priority=0
        )
        success = any(results)
        print(f"   Pushover (admin): {'✓ Sent' if success else '✗ Failed'}")
    
    # Direct email
    if logger.is_destination_enabled('email'):
        print("   Sending direct email...")
        success = logger.send_email(
            "Direct Email Alert from PyLogger",
            """This is a direct email message sent via PyLogger.
            
Key features:
- Bypasses log level restrictions
- Can be sent anytime
- Useful for notifications and alerts
- Supports custom recipients

Sent from PyLogger Direct Message Example"""
        )
        print(f"   Email: {'✓ Sent' if success else '✗ Failed'}")
        
        # Send to custom recipients
        custom_emails = ["custom@example.com"]  # Replace with real emails
        success = logger.send_email(
            "Custom Recipients Test",
            "This email was sent to custom recipients.",
            to_emails=custom_emails
        )
        print(f"   Email (custom recipients): {'✓ Sent' if success else '✗ Failed'}")
    
    # Use cases for direct messages
    print("\n3. Practical use cases:")
    
    # Application startup notification
    logger.send_telegram("🚀 Application started successfully")
    
    # Scheduled task completion
    logger.send_pushover(
        "Daily backup completed successfully",
        title="Backup Status",
        priority=0
    )
    
    # Custom alert
    logger.send_email(
        "Weekly Report Ready",
        "The weekly analytics report has been generated and is ready for review."
    )
    
    # System health check
    logger.send_telegram("💚 System health check passed")
    
    print("   ✓ Sent various notification examples")
    
    # Now send a critical log message that WILL trigger notifications
    print("\n4. Critical log message (will trigger notifications):")
    logger.critical("This critical message will trigger all notifications!")
    
    print("\nDirect messages example completed!")
    print("Check your Telegram, Pushover, and email for the messages.")

if __name__ == "__main__":
    main()