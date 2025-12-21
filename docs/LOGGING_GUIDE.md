

# Logging System - User & Developer Guide

## Overview

WoW Cleanup Tool uses a modern, dual-channel logging system built on Python's `logging` module. All log actions in the UI (copy, save, clear, delete) are handled by a centralized log controls utility (`src/ui/log_controls.py`), ensuring consistent behavior for both User Log and Developer Log tabs. The modular UI delegates log actions to this utility for maintainability and testability. Logs are automatically rotated, support append mode, and are thread-safe for parallel operations.

**Log and Developer tabs now feature a visible text area and log control buttons (Clear, Save, Copy), using a grid-based modular layout.**


## Features

### Dual Log Channels
- **User Log** (`~/.wow_cleanup_tool/user_log.txt`)
  - INFO and essential messages only
  - Rotates at 1MB, keeps 5 backups
  - Append mode: logs persist across sessions (newest at top)
- **Developer Log** (`~/.wow_cleanup_tool/dev_log.txt`)
  - DEBUG, INFO, WARNING, ERROR
  - Rotates at 5MB, keeps 3 backups
  - Always verbose, includes stack traces for errors

### Log Controls Utility
- All log actions (copy, save, clear, delete) are handled by `src/ui/log_controls.py`
- Log tab and Developer tab both use this utility for consistent UI/UX
- Delete button is visible only when append mode is enabled
- Log controls respect delete mode (trash vs permanent)

### Log Levels
| Level   | User Log | Dev Log | Description                      |
|---------|----------|---------|----------------------------------|
| DEBUG   | ❌       | ✅      | Detailed diagnostic information  |
| INFO    | ✅       | ✅      | General informational messages   |
| WARNING | ❌       | ✅      | Warning messages                 |
| ERROR   | ❌       | ✅      | Error messages with stack traces |

### Log Format
**User Log:** `[YYYY-MM-DD HH:MM:SS] Message text`
**Developer Log:** `[YYYY-MM-DD HH:MM:SS] [LEVEL] Message text`

## Usage for Developers

### Basic Logging


```python
from src.core.logger import Logger

# Initialize logger
logger = Logger(verbose=True, append_mode=True)

# User-facing messages (Log tab)
logger.log("Operation completed successfully")

# Verbose messages (Log tab, if verbose enabled)
logger.verbose("Deleted file: addon_backup.bak")

# Developer messages (Developer tab)
logger.debug("Scanning directory: C:\\WoW\\_retail_")
logger.warning("Using fallback path detection method")
logger.error("Failed to delete file: Permission denied")
```



### Attach to UI Widgets
```python
# Attach to Log tab text widget (now a grid-based tk.Text)
logger.attach_text_widget(user_log_text_widget)

# Attach to Developer tab text widget (now a grid-based tk.Text)
logger.attach_dev_text_widget(dev_log_text_widget)
```


### Configuration
```python
# Enable/disable verbose logging
logger.set_verbose(True)   # Show all operations
logger.set_verbose(False)  # Show only important messages

# Enable/disable append mode
logger.set_append_mode(True)   # Keep logs across sessions
logger.set_append_mode(False)  # Clear logs on restart

# Set error callback for badge updates
logger.set_error_callback(lambda count: update_error_badge(count))
```


### Advanced: Custom Handlers
You can add custom handlers (e.g., email, syslog, JSON) to the developer logger:
```python
import logging
import logging.handlers
dev_logger = logging.getLogger('wow_cleanup.dev')
email_handler = logging.handlers.SMTPHandler(
  mailhost='smtp.example.com',
  fromaddr='app@example.com',
  toaddrs=['admin@example.com'],
  subject='WoW Cleanup Tool - Critical Error')
email_handler.setLevel(logging.ERROR)
dev_logger.addHandler(email_handler)
```


## Log File Locations

### Windows
```
C:\Users\<YourName>\.wow_cleanup_tool\
├── user_log.txt          (current user log)
├── user_log.txt.1        (backup 1)
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
All logging methods work seamlessly:
```python
logger.log("Message")           # User log
logger.verbose("Verbose msg")  # User log (if verbose)
logger.debug("Debug msg")      # Developer log
logger.error("Error msg")      # Developer log
logger.warning("Warning msg")  # Developer log
logger.set_verbose(True)
logger.attach_text_widget(widget)
```


## Benefits

### For Users
- Log files never grow huge (automatic rotation)
- Logs persist across sessions (append mode)
- Can analyze old logs (numbered backups)
- Timestamps on every message

### For Developers
- Thread-safe logging (parallel operations)
- Standard Python logging (compatible with tools)
- Easy to extend (add handlers)
- Professional logging practices
- Better debugging with log levels


## Troubleshooting

### Logs not appearing in UI?
Check that widgets are attached:
```python
logger.attach_text_widget(user_widget)
logger.attach_dev_text_widget(dev_widget)
```

### Want to change rotation settings?
Edit `src/core/logger.py` in `_setup_file_handlers()`:
```python
user_file_handler = logging.handlers.RotatingFileHandler(
  user_log_file,
  maxBytes=2 * 1024 * 1024,  # 2MB instead of 1MB
  backupCount=10,            # 10 backups instead of 5
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
- Email notifications for critical errors
- Syslog integration for server deployments
- JSON-formatted logs for log analysis tools
- Compressed log rotation (gzip old logs)
- Network logging (send logs to central server)
- Filtering by module/function name
- Performance metrics logging

---

For more information: https://docs.python.org/3/library/logging.html
