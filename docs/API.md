# API Reference

## PyLogger Class

### Constructor

```python
PyLogger(config_path=None, config=None, name=None)
```

**Parameters:**
- `config_path` (str, optional): Path to YAML configuration file
- `config` (dict, optional): Configuration dictionary
- `name` (str, optional): Logger name. Defaults to calling module name

**Raises:**
- `ValueError`: If configuration is invalid

### Logging Methods

#### Standard Logging Interface

```python
logger.debug(message, *args, **kwargs)
logger.info(message, *args, **kwargs)
logger.warning(message, *args, **kwargs)
logger.warn(message, *args, **kwargs)  # Alias for warning
logger.error(message, *args, **kwargs)
logger.critical(message, *args, **kwargs)
logger.exception(message, *args, **kwargs)
logger.log(level, message, *args, **kwargs)
```

**Parameters:**
- `message` (str): Log message
- `level` (int or str): Log level (for `log()` method)
- `*args`: Positional arguments for string formatting
- `**kwargs`: Keyword arguments for logging

### Direct Message Methods

#### send_telegram()

```python
send_telegram(message, parse_mode=None) -> bool
```

Send direct Telegram message bypassing log levels.

**Parameters:**
- `message` (str): Message to send
- `parse_mode` (str, optional): Parse mode ("HTML", "Markdown", "MarkdownV2")

**Returns:**
- `bool`: True if message sent successfully

#### send_pushover()

```python
send_pushover(message, destination=None, priority=None, title=None) -> List[bool]
```

Send direct Pushover message bypassing log levels.

**Parameters:**
- `message` (str): Message to send
- `destination` (str, optional): Specific destination name
- `priority` (int, optional): Message priority (-2 to 2)
- `title` (str, optional): Message title

**Returns:**
- `List[bool]`: Results for each destination

#### send_email()

```python
send_email(subject, message, to_emails=None) -> bool
```

Send direct email bypassing log levels.

**Parameters:**
- `subject` (str): Email subject
- `message` (str): Email body
- `to_emails` (List[str], optional): Recipient emails

**Returns:**
- `bool`: True if email sent successfully

### Configuration Management

#### is_destination_enabled()

```python
is_destination_enabled(destination) -> bool
```

Check if a destination is enabled.

**Parameters:**
- `destination` (str): Destination name

**Returns:**
- `bool`: True if destination is enabled

#### enable_destination()

```python
enable_destination(destination) -> None
```

Enable a destination at runtime.

**Parameters:**
- `destination` (str): Destination name

#### disable_destination()

```python
disable_destination(destination) -> None
```

Disable a destination at runtime.

**Parameters:**
- `destination` (str): Destination name

#### update_config()

```python
update_config(new_config) -> None
```

Update configuration at runtime.

**Parameters:**
- `new_config` (dict): New configuration dictionary

#### get_config()

```python
get_config() -> Dict[str, Any]
```

Get current configuration.

**Returns:**
- `dict`: Current configuration dictionary

#### save_config()

```python
save_config(file_path) -> None
```

Save current configuration to YAML file.

**Parameters:**
- `file_path` (str): Path to save configuration

### Utility Methods

#### set_level()

```python
set_level(destination, level) -> None
```

Set log level for specific destination.

**Parameters:**
- `destination` (str): Destination name
- `level` (str or int): Log level

#### get_destinations()

```python
get_destinations() -> List[str]
```

Get list of available destinations.

**Returns:**
- `List[str]`: Destination names

#### get_enabled_destinations()

```python
get_enabled_destinations() -> List[str]
```

Get list of enabled destinations.

**Returns:**
- `List[str]`: Enabled destination names

#### test_destinations()

```python
test_destinations() -> Dict[str, bool]
```

Test all destinations by sending test messages.

**Returns:**
- `dict`: Test results for each destination

## Configuration Classes

### LoggerConfig

Configuration manager class.

#### Constructor

```python
LoggerConfig(config_path=None, config=None)
```

**Parameters:**
- `config_path` (str, optional): Path to YAML configuration file
- `config` (dict, optional): Configuration dictionary

### Handler Classes

All handlers inherit from `BaseDestinationHandler`.

#### ConsoleHandler

```python
ConsoleHandler(config)
```

Handles console output.

#### RotatingFileHandler

```python
RotatingFileHandler(config)
```

Handles file output with rotation.

#### TelegramHandler

```python
TelegramHandler(config)
```

Handles Telegram messages.

**Methods:**
- `send_direct_message(message, parse_mode=None) -> bool`

#### PushoverHandler

```python
PushoverHandler(config)
```

Handles Pushover notifications.

**Methods:**
- `send_direct_message(message, destination=None, priority=None, title=None) -> List[bool]`

#### EmailHandler

```python
EmailHandler(config)
```

Handles email notifications.

**Methods:**
- `send_direct_message(subject, message, to_emails=None) -> bool`

## Configuration Structure

### Console Configuration

```python
{
    "enabled": bool,
    "level": str,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "format": str,  # Log format string
    "date_format": str  # Date format string
}
```

### File Configuration

```python
{
    "enabled": bool,
    "level": str,
    "filename": str,
    "max_size": int,  # Maximum file size in bytes
    "backup_count": int,  # Number of backup files
    "format": str,
    "date_format": str
}
```

### Telegram Configuration

```python
{
    "enabled": bool,
    "level": str,
    "bot_token": str,
    "chat_id": str,
    "format": str,
    "parse_mode": str  # HTML, Markdown, MarkdownV2
}
```

### Pushover Configuration

```python
{
    "enabled": bool,
    "level": str,
    "format": str,
    "destinations": [
        {
            "name": str,
            "user_key": str,
            "api_token": str,
            "priority": int  # -2 to 2
        }
    ]
}
```

### Email Configuration

```python
{
    "enabled": bool,
    "level": str,
    "smtp_server": str,
    "smtp_port": int,
    "use_tls": bool,
    "username": str,
    "password": str,
    "from_email": str,
    "to_emails": List[str],
    "subject_prefix": str,
    "format": str,
    "date_format": str
}
```

## Exceptions

### ConfigValidationError

Raised when configuration validation fails.

```python
class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass
```

## Constants

### Log Levels

- `DEBUG` = 10
- `INFO` = 20  
- `WARNING` = 30
- `ERROR` = 40
- `CRITICAL` = 50

### Valid Destinations

- `console`
- `file` 
- `telegram`
- `pushover`
- `email`

## Context Manager

PyLogger supports context manager usage:

```python
with PyLogger(config=config) as logger:
    logger.info("This will properly clean up resources")
```