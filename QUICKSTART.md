# PyLogger - Quick Start Guide

Welcome to PyLogger! This guide will get you up and running in just a few minutes.

## 🚀 Quick Installation

```bash
# Install from the project directory
cd py-logger
pip install -e .

# Or install requirements manually
pip install pyyaml requests
```

## 📝 Simple Example

Create a file called `quick_test.py`:

```python
from py_logger import PyLogger

# Basic configuration
config = {
    "console": {
        "enabled": True,
        "level": "INFO"
    },
    "file": {
        "enabled": True,
        "level": "DEBUG",
        "filename": "quick_test.log"
    }
}

# Initialize logger
logger = PyLogger(config=config, name="QuickTest")

# Test logging
logger.info("🎉 PyLogger is working!")
logger.debug("This debug message goes to file only")
logger.warning("⚠️ This is a warning")
logger.error("❌ This is an error")

print("✅ Check 'quick_test.log' for the complete log output!")
```

Run it:
```bash
python quick_test.py
```

## 🔧 Add Notifications (Optional)

To add Telegram notifications:

1. **Create a Telegram Bot**:
   - Message @BotFather on Telegram
   - Send `/newbot` and follow instructions
   - Save your bot token

2. **Get your Chat ID**:
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

3. **Update your config**:
   ```python
   config = {
       "console": {"enabled": True, "level": "INFO"},
       "file": {"enabled": True, "level": "DEBUG", "filename": "app.log"},
       "telegram": {
           "enabled": True,
           "level": "ERROR",
           "bot_token": "YOUR_BOT_TOKEN_HERE",
           "chat_id": "YOUR_CHAT_ID_HERE"
       }
   }
   ```

4. **Test it**:
   ```python
   logger.error("This will send a Telegram notification!")
   
   # Or send a direct message
   logger.send_telegram("🔔 Direct message bypass log levels!")
   ```

## 📋 What's Included

- ✅ **Console logging** - Immediate feedback
- ✅ **File logging** - With automatic rotation
- ✅ **Telegram notifications** - For alerts and monitoring
- ✅ **Pushover notifications** - Multi-destination support
- ✅ **Email alerts** - Critical issue notifications
- ✅ **YAML configuration** - External config files
- ✅ **Runtime control** - Enable/disable destinations on-the-fly
- ✅ **Direct messaging** - Send messages bypassing log levels

## 📚 Next Steps

1. **Explore Examples**: Check the `examples/` directory for more detailed usage
2. **Read Documentation**: See `docs/` for complete API reference
3. **Set up Notifications**: Configure Telegram, Pushover, or Email
4. **Production Setup**: Use YAML configs with environment variables

## 🆘 Need Help?

- **Examples**: Look in `examples/` directory
- **Documentation**: Check `docs/API.md` for complete reference
- **Test Configuration**: Run `python tests/test_basic.py`
- **Issues**: Open an issue on GitHub

## 🎯 Common Use Cases

```python
# Application monitoring
logger.info("Service started")
logger.error("Database connection failed")  # → Telegram alert

# Direct notifications
logger.send_telegram("🚀 Deployment completed successfully")
logger.send_email("Backup Complete", "Daily backup finished at 2AM")

# Runtime control
logger.disable_destination('console')  # Silence console in production
logger.enable_destination('telegram')  # Enable alerts

# Different log levels per destination
# Console: INFO, File: DEBUG, Telegram: ERROR, Email: CRITICAL
```

Happy logging! 🎉