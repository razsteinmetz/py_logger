# PyLogger

A comprehensive, reusable Python logging package that extends the standard logging library with multiple notification destinations.

## Features

- **Multiple Destinations**: Log to Telegram, Pushover, Email, Files, and Console
- **Flexible Configuration**: Configure via YAML file or Python dictionaries
- **Individual Log Levels**: Each destination can have its own log level
- **Runtime Control**: Enable/disable destinations during program execution
- **Message Broadcasting**: Send direct messages bypassing log level restrictions
- **File Rotation**: Automatic log file rotation with size and count limits
- **Easy Integration**: Drop-in replacement for standard Python logging

## Quick Start

### Installation

```bash
pip install py-logger
```

### Basic Usage

```python
from py_logger import PyLogger

# Initialize with configuration file
logger = PyLogger(config_path="logging_config.yaml")

# Or initialize with dictionary
config = {
    "console": {
        "enabled": True,
        "level": "INFO"
    },
    "file": {
        "enabled": True,
        "level": "DEBUG",
        "filename": "app.log"
    }
}
logger = PyLogger(config=config)

# Use like standard logging
logger.info("Application started")
logger.error("Something went wrong")

# Send direct messages (bypass log levels)
logger.send_telegram("Critical alert!")
logger.send_email("System notification", "The backup completed successfully")
```

## Multi-File Project Usage

PyLogger integrates seamlessly with Python's standard logging library. Set it up once in your main program, then use standard `logging.getLogger()` in all other modules.

### Project Structure Example

```
my_project/
├── config/
│   └── logging_config.yaml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── api.py
│   └── utils.py
└── requirements.txt
```

### 1. Setup in Main Program

**main.py**:
```python
# src/main.py
from py_logger import PyLogger
import logging
from .database import DatabaseManager
from .api import APIHandler

def main():
    # Setup PyLogger once at application startup
    PyLogger.setup(config_path="config/logging_config.yaml", name="MyApplication")
    
    # Now use standard logging everywhere
    logger = logging.getLogger(__name__)
    logger.info("Application starting...")
    
    # Initialize components
    db = DatabaseManager()
    api = APIHandler()
    
    try:
        logger.info("Connecting to database...")
        db.connect()
        
        logger.info("Starting API server...")
        api.start_server()
        
        logger.info("Application started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        # Direct messaging available from anywhere
        from py_logger import send_telegram
        send_telegram(f"🔴 Application startup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
```

### 2. Use Standard Logging in Other Modules

**database.py**:
```python
# src/database.py
import logging

# Just use standard logging - PyLogger is already configured!
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        logger.debug("DatabaseManager initialized")
        self.connection = None
    
    def connect(self):
        logger.info("Attempting database connection...")
        try:
            # Database connection logic here
            self.connection = "connected"  # Placeholder
            logger.info("Database connected successfully")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            # Direct messaging when needed
            from py_logger import send_email
            send_email("DB Alert", f"Database connection failed: {e}")
            raise
    
    def execute_query(self, query):
        logger.debug(f"Executing query: {query}")
        # Query execution logic
        logger.debug("Query executed successfully")
```

**api.py**:
```python
# src/api.py
import logging

# Standard logging - automatically uses PyLogger destinations
logger = logging.getLogger(__name__)

class APIHandler:
    def __init__(self):
        logger.debug("APIHandler initialized")
    
    def start_server(self):
        logger.info("Starting API server on port 8080")
        # Server startup logic
        logger.info("API server started successfully")
    
    def handle_request(self, request):
        logger.debug(f"Handling request: {request}")
        
        try:
            # Request handling logic
            logger.info(f"Request processed successfully: {request}")
        except Exception as e:
            logger.warning(f"Request failed: {request} - {e}")
            # No alerts for individual request failures
```

**utils.py**:
```python
# src/utils.py
import logging
from py_logger import send_telegram, send_pushover

# Standard logging works everywhere
logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug("Processing data...")
    
    try:
        # Data processing logic
        result = len(data)  # Placeholder
        logger.debug(f"Data processed: {result} items")
        return result
        
    except Exception as e:
        logger.error(f"Data processing failed: {e}")
        raise

def send_notification(message, urgent=False):
    """Send notifications using PyLogger direct messaging."""
    logger.info(f"Sending notification: {message}")
    
    if urgent:
        # Send immediate notifications bypassing log levels
        send_telegram(f"🚨 URGENT: {message}")
        send_pushover(message, priority=2)  # Emergency priority
    else:
        # Regular notification
        send_telegram(f"ℹ️ {message}")
```

### 3. Configuration File

**config/logging_config.yaml**:
```yaml
console:
  enabled: true
  level: INFO
  format: "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s"

file:
  enabled: true
  level: DEBUG
  filename: "logs/app.log"
  max_size: 10485760  # 10MB
  backup_count: 5
  format: "%(asctime)s | %(name)-20s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s"

telegram:
  enabled: true
  level: ERROR
  bot_token: "${TELEGRAM_BOT_TOKEN}"
  chat_id: "${TELEGRAM_CHAT_ID}"
  format: "🔴 <b>%(levelname)s</b> from <i>%(name)s</i>:\n%(message)s"

email:
  enabled: true
  level: CRITICAL
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  username: "${EMAIL_USERNAME}"
  password: "${EMAIL_PASSWORD}"
  from_email: "${EMAIL_USERNAME}"
  to_emails: ["${ALERT_EMAIL}"]
  subject_prefix: "[MY APP ALERT]"
```

### 4. Environment Configuration

Create a `.env` file or set environment variables:

```bash
# .env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ALERT_EMAIL=admin@company.com
```

### 5. Alternative: Dictionary Configuration

If you prefer configuration in code:

```python
# main.py
from py_logger import PyLogger
import logging

config = {
    "console": {"enabled": True, "level": "INFO"},
    "file": {"enabled": True, "level": "DEBUG", "filename": "logs/app.log"},
    "telegram": {
        "enabled": True,
        "level": "ERROR",
        "bot_token": "your_bot_token",
        "chat_id": "your_chat_id"
    }
}

# Setup PyLogger
PyLogger.setup(config=config, name="MyApp")

# Use standard logging everywhere else
logger = logging.getLogger(__name__)
logger.info("Application started")
```

### Best Practices for Multi-File Projects

1. **Single Setup**: Call `PyLogger.setup()` only once in your main program
2. **Standard Logging**: Use `logging.getLogger(__name__)` in all modules
3. **Module Names**: PyLogger automatically uses module names for better organization
4. **Direct Messaging**: Import `send_telegram`, `send_pushover`, `send_email` when needed
5. **Environment Variables**: Use environment variables for sensitive configuration
6. **Hierarchical Naming**: Standard logging's hierarchical naming works naturally
7. **No Imports Needed**: Other modules don't need to import PyLogger directly

### Key Advantages

- **Zero Learning Curve**: Uses standard Python logging patterns
- **No Custom Setup**: No need for custom logger setup functions
- **Module Isolation**: Modules don't need to know about PyLogger
- **Drop-in Replacement**: Works with existing logging code
- **Automatic Integration**: All logging automatically gets PyLogger features

## Quick Reference

### Single File Usage
```python
from py_logger import PyLogger

logger = PyLogger(config={"console": {"enabled": True, "level": "INFO"}})
logger.info("Hello, PyLogger!")
```

### Multi-File Project Setup
```python
# main.py
from py_logger import PyLogger
import logging

# Setup PyLogger once
PyLogger.setup(config_path="config.yaml", name="MyApp")

# any_module.py  
import logging
logger = logging.getLogger(__name__)  # Standard logging!
logger.info("Module loaded")
```

### Direct Messaging
```python
# Available from anywhere after setup
from py_logger import send_telegram, send_pushover, send_email

send_telegram("🚨 Critical alert!")
send_pushover("Warning message", priority=1)
send_email("Alert", "System notification")
```

### Runtime Control
```python
logger.disable_destination('console')  # Silence console
logger.enable_destination('telegram')  # Enable alerts
logger.set_level('file', 'WARNING')   # Change log level
```

## Configuration

PyLogger supports two configuration formats: **flat structure** (for YAML files) and **nested structure** (for Python dictionaries).

### Python Dictionary Configuration (Nested Format)

```python
config = {
    'destinations': {
        'console': {
            'enabled': True,
            'level': 'DEBUG'
        },
        'file': {
            'enabled': True, 
            'level': 'INFO',
            'filename': 'app.log',
            'max_size': 1048576,
            'backup_count': 3
        },
        'telegram': {
            'enabled': False,
            'level': 'ERROR',
            'bot_token': '${TELEGRAM_BOT_TOKEN}',
            'chat_id': '${TELEGRAM_CHAT_ID}'
        }
    }
}

# Use with PyLogger.setup()
PyLogger.setup(config=config)
```

### YAML Configuration Example (Flat Format)

```yaml
# logging_config.yaml
console:
  enabled: true
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

file:
  enabled: true
  level: DEBUG
  filename: "app.log"
  max_size: 10485760  # 10MB
  backup_count: 5
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

telegram:
  enabled: false
  level: ERROR
  bot_token: "YOUR_BOT_TOKEN"
  chat_id: "YOUR_CHAT_ID"
  format: "🔴 %(levelname)s: %(message)s"

pushover:
  enabled: false
  level: WARNING
  destinations:
    - name: "admin"
      user_key: "USER_KEY_1"
      api_token: "API_TOKEN_1"
      priority: 1
    - name: "team"
      user_key: "USER_KEY_2" 
      api_token: "API_TOKEN_2"
      priority: 0
  format: "%(levelname)s: %(message)s"

email:
  enabled: false
  level: CRITICAL
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  username: "your_email@gmail.com"
  password: "your_app_password"
  from_email: "your_email@gmail.com"
  to_emails:
    - "admin@company.com"
    - "alerts@company.com"
  subject_prefix: "[APP ALERT]"
  format: "%(asctime)s - %(levelname)s: %(message)s"
```

### Dictionary Configuration Example

```python
config = {
    "console": {
        "enabled": True,
        "level": "INFO"
    },
    "file": {
        "enabled": True,
        "level": "DEBUG", 
        "filename": "app.log",
        "max_size": 10485760,  # 10MB
        "backup_count": 5
    },
    "telegram": {
        "enabled": True,
        "level": "ERROR",
        "bot_token": "YOUR_BOT_TOKEN",
        "chat_id": "YOUR_CHAT_ID"
    },
    "pushover": {
        "enabled": True,
        "level": "WARNING",
        "destinations": [
            {
                "name": "admin",
                "user_key": "USER_KEY",
                "api_token": "API_TOKEN",
                "priority": 1
            }
        ]
    },
    "email": {
        "enabled": True,
        "level": "CRITICAL",
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "username": "your_email@gmail.com",
        "password": "your_app_password",
        "from_email": "your_email@gmail.com",
        "to_emails": ["admin@company.com"]
    }
}
```

## API Reference

### PyLogger Class

#### Initialization

```python
PyLogger(config_path=None, config=None, name=None)
```

- `config_path`: Path to YAML configuration file
- `config`: Dictionary with configuration
- `name`: Logger name (defaults to calling module name)

#### Logging Methods

Standard logging methods with the same interface as Python's logging module:

```python
logger.debug(message)
logger.info(message)
logger.warning(message)
logger.error(message)
logger.critical(message)
```

#### Direct Message Methods

Send messages directly, bypassing log level restrictions:

```python
logger.send_telegram(message, parse_mode='HTML')
logger.send_pushover(message, destination=None, priority=None)
logger.send_email(subject, message, to_emails=None)
```

#### Runtime Control

```python
# Enable/disable destinations at runtime
logger.enable_destination('telegram')
logger.disable_destination('console')

# Check if destination is enabled
if logger.is_destination_enabled('file'):
    logger.info("File logging is active")

# Update configuration at runtime
logger.update_config({'telegram': {'level': 'INFO'}})
```

## Advanced Usage

### Custom Formatters

```python
config = {
    "console": {
        "enabled": True,
        "level": "INFO",
        "format": "%(asctime)s | %(levelname)-8s | %(message)s",
        "date_format": "%Y-%m-%d %H:%M:%S"
    }
}
```

### Environment Variables

Use environment variables in configuration:

```yaml
telegram:
  enabled: true
  level: ERROR
  bot_token: "${TELEGRAM_BOT_TOKEN}"
  chat_id: "${TELEGRAM_CHAT_ID}"
```

### Multiple Pushover Destinations

```python
config = {
    "pushover": {
        "enabled": True,
        "level": "WARNING",
        "destinations": [
            {
                "name": "ops_team",
                "user_key": "USER_KEY_1",
                "api_token": "API_TOKEN_1", 
                "priority": 1
            },
            {
                "name": "dev_team",
                "user_key": "USER_KEY_2",
                "api_token": "API_TOKEN_2",
                "priority": 0
            }
        ]
    }
}
```

## Examples

See the `examples/` directory for complete working examples:

- `basic_usage.py` - Simple console and file logging
- `full_config.py` - All destinations configured
- `runtime_control.py` - Dynamic enable/disable of destinations
- `direct_messages.py` - Using direct message capabilities

## Requirements

- Python 3.7+
- PyYAML
- requests (for Telegram and Pushover)
- smtplib (included with Python)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions and support, please open an issue on GitHub.