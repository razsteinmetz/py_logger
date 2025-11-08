# PyLogger Examples

This directory contains practical examples of how to use PyLogger in different scenarios.

## Examples Overview

### 1. `basic_usage.py`
- Simple console and file logging setup
- Dictionary-based configuration
- Basic logging operations
- Good starting point for new users

### 2. `full_config.py`
- Demonstrates all available destinations
- Shows complete configuration options
- Tests all notification methods
- Requires API keys and credentials setup

### 3. `runtime_control.py`
- Dynamic enable/disable of destinations
- Runtime configuration changes
- Log level modifications
- Configuration saving

### 4. `direct_messages.py`
- Bypass log level restrictions
- Send immediate notifications
- Multiple use cases demonstration
- Custom recipient support

### 5. `yaml_config.py`
- Load configuration from YAML file
- Environment variable usage
- External configuration management

### 6. `multifile_project.py`
- **NEW**: Multi-file project example
- Demonstrates centralized logger setup
- Shows module-specific logging
- Best practices for larger projects

## Configuration Files

### `example_config.yaml`
Complete example configuration showing all available options with comments.

## Running Examples

1. **Install PyLogger**:
   ```bash
   pip install -e .
   ```

2. **Set up credentials** (for notification examples):
   ```bash
   # Telegram
   export TELEGRAM_BOT_TOKEN="your_bot_token"
   export TELEGRAM_CHAT_ID="your_chat_id"
   
   # Pushover
   export PUSHOVER_USER_KEY="your_user_key"
   export PUSHOVER_API_TOKEN="your_api_token"
   
   # Email
   export EMAIL_USERNAME="your_email@gmail.com"
   export EMAIL_PASSWORD="your_app_password"
   export ALERT_EMAIL="admin@company.com"
   ```

3. **Run examples**:
   ```bash
   python basic_usage.py
   python runtime_control.py
   python direct_messages.py  # Needs credentials
   ```

## Setting Up Credentials

### Telegram Bot
1. Create a bot with @BotFather on Telegram
2. Get your bot token
3. Find your chat ID by messaging your bot and visiting:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`

### Pushover
1. Create account at pushover.net
2. Create an application to get API token
3. Get your user key from your dashboard

### Email (Gmail)
1. Enable 2-factor authentication
2. Create an app-specific password
3. Use your email and app password

## Customization

Copy `example_config.yaml` to create your own configuration:

```bash
cp example_config.yaml my_config.yaml
# Edit my_config.yaml with your settings
python yaml_config.py  # Uses example_config.yaml by default
```

## Tips

- Start with `basic_usage.py` to understand the fundamentals
- Use `runtime_control.py` to learn dynamic configuration
- Test with `direct_messages.py` to verify your API credentials
- Customize `example_config.yaml` for your production setup