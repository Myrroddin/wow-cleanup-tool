# Logging System Guide

## Overview

Dual-channel logging system built on Python's `logging` module with automatic rotation, append mode, and thread-safe operations. All log actions (copy, save, clear, delete) handled by `src/ui/log_controls.py` for consistent behavior.


## Log Channels

**User Log** (`~/.wow_cleanup_tool/user_log.txt`): INFO messages, 1MB rotation, 5 backups, append mode toggleable
**Developer Log** (`~/.wow_cleanup_tool/dev_log.txt`): DEBUG/INFO/WARNING/ERROR, 5MB rotation, 3 backups, always verbose


### Log Controls (src/ui/log_controls.py)
- **User Log Tab**: Clear Session Log (append-aware), Delete Log File (dimmed when append OFF), Open Log Folder, Copy to Clipboard
- **Developer Log Tab**: Clear Session Log (display only), Open Log Folder, Copy to Clipboard
- Respects delete mode (trash vs permanent), cross-platform folder opening, grid-based layout

| Level   | User Log | Dev Log | Description                      |
|---------|----------|---------|----------------------------------|
| DEBUG   | ❌       | ✅      | Detailed diagnostic information  |
| INFO    | ✅       | ✅      | General informational messages   |
| WARNING | ❌       | ✅      | Warning messages                 |
| ERROR   | ❌       | ✅      | Error messages with stack traces |


**Log Format**: User Log: `[YYYY-MM-DD HH:MM:SS] Message`; Developer Log: `[YYYY-MM-DD HH:MM:SS] [LEVEL] Message`


**File Cleaner Output Examples**:
- Normal: `[retail]: removed 5 file(s)` or `[retail]: removed 2 line(s) from AddOns.txt`
- Verbose: `[retail]: removed addon_backup.bak` or `[retail]: removed Addon1 from AddOns.txt`


## Usage for Developers


### Basic Logging
```python
from core.logger import Logger

logger = Logger(verbose=True, append_mode=True)
logger.log("Operation completed successfully")  # User Log
logger.verbose("Deleted file: addon_backup.bak")  # User Log (if verbose)
logger.debug("Scanning directory: C:\\WoW\\_retail_")  # Developer Log
logger.warning("Using fallback path detection method")  # Developer Log
logger.error("Failed to delete file: Permission denied")  # Developer Log
```


### Critical Pattern: logger.log() vs logger.verbose()
**Never call both for the same action** - use if/else to prevent duplicate entries:

```python
# When both verbose and normal messages exist:
if getattr(self.logger, "_verbose", False):
    self.logger.verbose(f"[Retail] removed {filepath}")  # Detailed
else:
    self.logger.log(f"[Retail]: removed {count} file(s).")  # Summary

# When only one message exists:
logger.log("Simple status message")  # No if/else needed
```


**Rule**: `logger.log()` when verbose OFF or no verbose alternative; `logger.verbose()` when verbose ON with alternative. Developer logs (`error()`, `debug()`, `warning()`) always log without branching.


### Configuration & UI Integration
```python
# Attach to UI widgets
logger.attach_text_widget(user_log_text_widget)
logger.attach_dev_text_widget(dev_log_text_widget)

# Configure logging behavior
logger.set_verbose(True)        # Show all operations
logger.set_append_mode(True)    # Keep logs across sessions
logger.set_error_callback(lambda count: update_error_badge(count))
```


### Custom Handlers (Advanced)
```python
# Add custom handlers (email, syslog, JSON)
import logging.handlers
dev_logger = logging.getLogger('wow_cleanup.dev')
email_handler = logging.handlers.SMTPHandler(
    mailhost='smtp.example.com', fromaddr='app@example.com',
    toaddrs=['admin@example.com'], subject='Critical Error')
email_handler.setLevel(logging.ERROR)
dev_logger.addHandler(email_handler)
```


## Log File Locations
**Windows**: `C:\Users\<YourName>\.wow_cleanup_tool\user_log.txt[.1-.5]`, `dev_log.txt[.1-.3]`
**Linux/macOS**: `~/.wow_cleanup_tool/user_log.txt[.1-.5]`, `dev_log.txt[.1-.3]`

## Troubleshooting

**Logs not in UI?** Verify widgets attached: `logger.attach_text_widget(widget)`, `logger.attach_dev_text_widget(dev_widget)`

**Change rotation?** Edit `src/core/logger.py` in `_setup_file_handlers()`:
```python
user_file_handler = RotatingFileHandler(
    user_log_file, maxBytes=2*1024*1024, backupCount=10, encoding='utf-8')
```

**Console output?** Add StreamHandler:
```python
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logger.dev_formatter)
logger.dev_logger.addHandler(console)
```

## Benefits
- **Users**: Automatic rotation, persistent logs, backups, timestamps
- **Developers**: Thread-safe, standard Python logging, extensible, professional practices

---
Documentation: https://docs.python.org/3/library/logging.html
