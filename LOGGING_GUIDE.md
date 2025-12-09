# Python Logging System - User Guide

## Overview
The WoW Cleanup Tool now uses Python's built-in `logging` module for professional-grade logging with automatic rotation, timestamps, and thread safety.

## Features

### Automatic Log Rotation
- **User Log** (`~/.wow_cleanup_tool/user_log.txt`)
  - Maximum size: 1MB per file
  - Keeps 5 backup files (`user_log.txt.1`, `user_log.txt.2`, etc.)
  - Automatically rotates when size limit reached
  
- **Developer Log** (`~/.wow_cleanup_tool/dev_log.txt`)
  - Maximum size: 5MB per file
  - Keeps 3 backup files
  - Contains all DEBUG, INFO, WARNING, ERROR messages

### Log Levels

The system uses standard Python log levels:

| Level | User Log | Dev Log | Description |
|-------|----------|---------|-------------|
| DEBUG | ❌ | ✅ | Detailed diagnostic information |
| INFO | ✅ | ✅ | General informational messages |
| WARNING | ❌ | ✅ | Warning messages (NEW) |
| ERROR | ❌ | ✅ | Error messages with stack traces |

### Log Format

**User Log Format:**
```
[YYYY-MM-DD HH:MM:SS] Message text
```

Example:
```
[2025-12-08 14:32:15] Application started successfully!
[2025-12-08 14:32:16] Detecting World of Warcraft installation...
```

**Developer Log Format:**
```
[YYYY-MM-DD HH:MM:SS] [LEVEL] Message text
```

Example:
```
[2025-12-08 14:32:15] [INFO] Initializing WoW Cleanup Tool
[2025-12-08 14:32:16] [DEBUG] PathManager initialized
[2025-12-08 14:32:18] [ERROR] Failed to access registry: Access denied
[2025-12-08 14:32:19] [WARNING] WoW path not found in registry
```

## Usage for Developers

### Basic Logging

```python
from modules.core.logger import Logger

# Initialize logger
logger = Logger(verbose=True, append_mode=True)

# User-facing messages (appears in Log tab)
logger.log("Operation completed successfully")

# Verbose messages (only shown if verbose=True)
logger.verbose("Deleted file: addon_backup.bak")

# Developer messages (appears in Developer tab)
logger.debug("Scanning directory: C:\\WoW\\_retail_")
logger.warning("Using fallback path detection method")
logger.error("Failed to delete file: Permission denied")
```

### Attach to UI Widgets

```python
# Attach to Log tab text widget
logger.attach_text_widget(user_log_text_widget)

# Attach to Developer tab text widget  
logger.attach_dev_text_widget(dev_log_text_widget)
```

### Configuration

```python
# Enable/disable verbose logging
logger.set_verbose(True)  # Show all operations
logger.set_verbose(False)  # Show only important messages

# Enable/disable append mode
logger.set_append_mode(True)  # Keep logs across sessions
logger.set_append_mode(False)  # Clear logs on restart

# Set error callback for badge updates
logger.set_error_callback(lambda count: update_error_badge(count))
```

### Advanced: Custom Handlers

To add custom logging handlers (e.g., email alerts on errors):

```python
import logging
import logging.handlers

# Get the developer logger
dev_logger = logging.getLogger('wow_cleanup.dev')

# Add email handler for critical errors
email_handler = logging.handlers.SMTPHandler(
    mailhost='smtp.example.com',
    fromaddr='app@example.com',
    toaddrs=['admin@example.com'],
    subject='WoW Cleanup Tool - Critical Error'
)
email_handler.setLevel(logging.ERROR)
dev_logger.addHandler(email_handler)
```

## Log File Locations

### Windows
```
C:\Users\<YourName>\.wow_cleanup_tool\
├── user_log.txt          (current user log)
├── user_log.txt.1        (backup 1)
├── user_log.txt.2        (backup 2)
├── ...
├── dev_log.txt           (current developer log)
├── dev_log.txt.1         (backup 1)
└── dev_log.txt.2         (backup 2)
```

### Linux/macOS
```
~/.wow_cleanup_tool/
├── user_log.txt
├── user_log.txt.1
├── ...
├── dev_log.txt
└── dev_log.txt.1
```

## API Reference

**The logging API is simple and consistent:**

All logging methods work seamlessly:

```python
# Standard logging methods
logger.log("Message")
logger.verbose("Verbose message")
logger.debug("Debug message")
logger.error("Error message")
logger.warning("Warning message")
logger.set_verbose(True)
logger.attach_text_widget(widget)
```

## Benefits

### For Users
- ✅ Log files never grow huge (automatic rotation)
- ✅ Better performance (buffered file writes)
- ✅ Can analyze old logs (numbered backups)
- ✅ Timestamps on every message

### For Developers
- ✅ Thread-safe logging (parallel operations)
- ✅ Standard Python logging (compatible with tools)
- ✅ Easy to extend (add handlers)
- ✅ Professional logging practices
- ✅ Better debugging with log levels

## Troubleshooting

### Logs not appearing in UI?
Check that widgets are attached:
```python
logger.attach_text_widget(user_widget)
logger.attach_dev_text_widget(dev_widget)
```

### Want to change rotation settings?
Edit `modules/core/logger.py` in `_setup_file_handlers()`:
```python
user_file_handler = logging.handlers.RotatingFileHandler(
    user_log_file,
    maxBytes=2 * 1024 * 1024,  # 2MB instead of 1MB
    backupCount=10,             # 10 backups instead of 5
    encoding='utf-8'
)
```

### Want logs to go to console too?
Add a StreamHandler:
```python
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logger.dev_formatter)
logger.dev_logger.addHandler(console)
```

## Future Enhancements

Possible additions with Python's logging module:
- Email notifications for critical errors
- Syslog integration for server deployments
- JSON-formatted logs for log analysis tools
- Compressed log rotation (gzip old logs)
- Network logging (send logs to central server)
- Filtering by module/function name
- Performance metrics logging

---

**For more information:** https://docs.python.org/3/library/logging.html
