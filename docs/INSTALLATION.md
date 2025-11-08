# Installation and Setup Guide

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/py-logger.git
cd py-logger

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### From PyPI (When Published)

```bash
pip install py-logger-advanced
```

## Dependencies

PyLogger requires Python 3.7+ and the following packages:
- `pyyaml>=6.0` - For YAML configuration file support
- `requests>=2.25.0` - For Telegram and Pushover API calls

## Quick Setup

### 1. Basic Configuration

Create a simple configuration to get started:

```python
from py_logger import PyLogger

config = {
    "console": {"enabled": True, "level": "INFO"},
    "file": {"enabled": True, "level": "DEBUG", "filename": "app.log"}
}

logger = PyLogger(config=config)
logger.info("Hello, PyLogger!")
```

### 2. YAML Configuration

Create a `config.yaml` file:

```yaml
console:
  enabled: true
  level: INFO

file:
  enabled: true
  level: DEBUG
  filename: "app.log"
  max_size: 10485760  # 10MB
  backup_count: 5
```

Use it in your application:

```python
from py_logger import PyLogger

logger = PyLogger(config_path="config.yaml")
logger.info("Configured from YAML!")
```

## Service Setup

### Telegram Bot Setup

1. **Create a Bot**:
   - Message @BotFather on Telegram
   - Send `/newbot` command
   - Follow the prompts to create your bot
   - Save the bot token

2. **Get Chat ID**:
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Find your chat ID in the response

3. **Configure**:
   ```yaml
   telegram:
     enabled: true
     level: ERROR
     bot_token: "your_bot_token_here"
     chat_id: "your_chat_id_here"
   ```

### Pushover Setup

1. **Create Account**:
   - Sign up at [pushover.net](https://pushover.net)
   - Note your user key from the dashboard

2. **Create Application**:
   - Go to "Create an Application/API Token"
   - Create your application and note the API token

3. **Configure**:
   ```yaml
   pushover:
     enabled: true
     level: WARNING
     destinations:
       - name: "primary"
         user_key: "your_user_key"
         api_token: "your_api_token"
         priority: 1
   ```

### Email Setup

#### Gmail Setup

1. **Enable 2FA**: Enable two-factor authentication on your Google account
2. **Create App Password**: 
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate an app password for PyLogger
3. **Configure**:
   ```yaml
   email:
     enabled: true
     level: CRITICAL
     smtp_server: "smtp.gmail.com"
     smtp_port: 587
     use_tls: true
     username: "your_email@gmail.com"
     password: "your_app_password"
     from_email: "your_email@gmail.com"
     to_emails: ["admin@company.com"]
   ```

#### Other Email Providers

**Outlook/Hotmail**:
```yaml
email:
  smtp_server: "smtp-mail.outlook.com"
  smtp_port: 587
  use_tls: true
```

**Yahoo**:
```yaml
email:
  smtp_server: "smtp.mail.yahoo.com"
  smtp_port: 587
  use_tls: true
```

## Environment Variables

For security, use environment variables for sensitive data:

```bash
# .env file or environment
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
export PUSHOVER_USER_KEY="your_user_key"
export PUSHOVER_API_TOKEN="your_api_token"
export EMAIL_USERNAME="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
```

Then reference them in YAML:
```yaml
telegram:
  bot_token: "${TELEGRAM_BOT_TOKEN}"
  chat_id: "${TELEGRAM_CHAT_ID}"
```

## Testing Configuration

Test programmatically:
```python
logger = PyLogger(config_path="config.yaml")
results = logger.test_destinations()
print(results)  # Shows success/failure for each destination
```

## Production Recommendations

1. **Log Rotation**: Always enable file rotation for production:
   ```yaml
   file:
     max_size: 50485760  # 50MB
     backup_count: 10
   ```

2. **Appropriate Levels**: Use appropriate log levels for notifications:
   - Console: INFO or WARNING
   - File: DEBUG (for troubleshooting)
   - Telegram: ERROR or CRITICAL
   - Email: CRITICAL only

3. **Error Handling**: PyLogger handles errors gracefully, but monitor your logs for handler errors.

4. **Rate Limiting**: Be aware of API rate limits:
   - Telegram: 30 messages/second
   - Pushover: 10,000 messages/month (free)
   - Email: Depends on provider

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **API Failures**: Check your tokens and network connectivity
3. **Permission Errors**: Ensure write permissions for log files
4. **YAML Errors**: Validate YAML syntax

### Debug Mode

Enable debug logging to troubleshoot:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

logger = PyLogger(config_path="config.yaml")
```

### Test Individual Components

```python
# Test Telegram only
from py_logger.handlers import TelegramHandler
handler = TelegramHandler({
    "enabled": True,
    "bot_token": "your_token",
    "chat_id": "your_chat_id"
})
handler._send_telegram_message("Test message")
```