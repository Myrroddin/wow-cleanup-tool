

# Logging System - User & Developer Guide

## Overview

WoW Cleanup Tool uses a modern, dual-channel logging system built on Python's `logging` module. All log actions in the UI (copy, save, clear, delete) are handled by a centralized log controls utility (`src/ui/log_controls.py`), ensuring consistent behavior for both User Log and Developer Log tabs. The modular UI delegates log actions to this utility for maintainability and testability. Logs are automatically rotated, support append mode, and are thread-safe for parallel operations.

**Log and Developer tabs now feature a visible text area and log control buttons (Clear, Save, Copy), using a grid-based modular layout.**


## Features

### Dual Log Channels
- **User Log** (`~/.wow_cleanup_tool/user_log.txt`)
  - INFO and essential messages only
  - Rotates at 1MB, keeps 5 backups
  - Append mode: logs persist across sessions (newest at top); when append is off, the file is cleared on startup
- **Developer Log** (`~/.wow_cleanup_tool/dev_log.txt`)
  - DEBUG, INFO, WARNING, ERROR
  - Rotates at 5MB, keeps 3 backups
  - Always verbose, includes stack traces for errors; persisted across sessions by default

### Log Controls Utility (Feature-Complete)
- All log actions (clear, open folder, copy, delete) are handled by `src/ui/log_controls.py`
- **User Log Tab** (4 buttons):
  - Clear Session Log: Append-mode-aware (clears display + deletes file when OFF; display only when ON)
  - Delete Log File: Dynamically dims when append OFF, enabled when append ON
  - Open Log Folder: Cross-platform folder opening (Windows/macOS/Linux)
  - Copy to Clipboard: Full log contents
- **Developer Log Tab** (3 buttons):
  - Clear Session Log: Clears display only
  - Open Log Folder: Cross-platform folder opening
  - Copy to Clipboard: Full developer log contents
- Delete button uses overlay technique for visual dimming without theme/geometry conflicts
- Log controls respect delete mode (trash vs permanent) for file deletion
- Descriptions with word-wrapping explain each tab's purpose
- Grid-based layout ensures consistent spacing and alignment

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

### Universal Logging Pattern: logger.log() vs logger.verbose()

**IMPORTANT:** Never call both `logger.log()` AND `logger.verbose()` for the same action. Use an if/else pattern:

```python
# When both verbose and normal messages exist:
if getattr(self.logger, "_verbose", False):
    # Verbose mode ON: show detailed message
    self.logger.verbose(f"[Retail] removed {filepath}")
else:
    # Verbose mode OFF: show summary message
    self.logger.log(f"[Retail]: removed {count} file(s).")

# When only one message exists (no verbose alternative):
logger.log("Simple status message")  # No if/else needed
```

**The Rule:**
- `logger.log()` is used when there's NO verbose alternative OR when verbose mode is OFF
- `logger.verbose()` is used when there IS a verbose alternative AND verbose mode is ON
- **NEVER both for the same action** (prevents duplicate log entries)

**Developer logs are simple:**
- `logger.error()`, `logger.debug()`, `logger.warning()` always log (no branching needed)
- Only user-facing logs need the if/else pattern


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
