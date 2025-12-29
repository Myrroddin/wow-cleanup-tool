"""
Modern logging system for WoW Cleanup Tool using Python's built-in logging module.

Provides dual logging: user-facing operations log and developer debug/error log,
with automatic timestamps, log rotation, and flexible formatting.
"""

import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable


class TextWidgetHandler(logging.Handler):
    """Custom logging handler that writes to a Tkinter Text widget."""

    def __init__(self, text_widget=None, tag: Optional[str] = None):
        """Initialize the handler.

        Args:
            text_widget: tkinter.Text widget to write to
            tag: Optional tag name for text formatting
        """
        super().__init__()
        self.text_widget = text_widget
        self.tag = tag

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record to the text widget.

        Args:
            record: LogRecord to emit
        """
        if not self.text_widget:
            return

        try:
            msg = self.format(record)

            def update():
                try:
                    self.text_widget.configure(state="normal")
                    if self.tag:
                        self.text_widget.insert("end", msg + "\n", self.tag)
                    else:
                        self.text_widget.insert("end", msg + "\n")
                    self.text_widget.see("end")
                    self.text_widget.configure(state="disabled")
                except Exception:
                    pass

            # Schedule UI update on main thread
            if self.text_widget.winfo_exists():
                self.text_widget.after(0, update)
        except Exception:
            self.handleError(record)

    def set_widget(self, text_widget) -> None:
        """Set or update the text widget.

        Args:
            text_widget: New tkinter.Text widget
        """
        self.text_widget = text_widget


class SessionSeparatorHandler(logging.Handler):
    """Handler that adds session separators on first log entry."""

    def __init__(self, text_widget=None, session_width: int = 70):
        """Initialize handler.

        Args:
            text_widget: tkinter.Text widget for session separator
            session_width: Width of separator line
        """
        super().__init__()
        self.text_widget = text_widget
        self.session_width = session_width
        self.session_started = False

    def emit(self, record: logging.LogRecord) -> None:
        """Add session separator before first message.

        Args:
            record: LogRecord (triggers separator check)
        """
        if self.session_started or not self.text_widget:
            return

        try:
            separator = (
                f"\n{'=' * self.session_width}\n"
                f"  Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"{'=' * self.session_width}\n"
            )

            def update():
                try:
                    self.text_widget.configure(state="normal")
                    self.text_widget.insert("1.0", separator)
                    self.text_widget.configure(state="disabled")
                except Exception:
                    pass

            if self.text_widget.winfo_exists():
                self.text_widget.after(0, update)

            self.session_started = True
        except Exception:
            pass

    def set_widget(self, text_widget) -> None:
        """Set or update the text widget.

        Args:
            text_widget: New tkinter.Text widget
        """
        self.text_widget = text_widget
        self.session_started = False


class WoWLogger:
    def set_timestamps_enabled(self, enabled: bool) -> None:
        """Enable or disable timestamps in user and developer logs."""
        if enabled:
            user_fmt = "[%(asctime)s] %(message)s"
            dev_fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
        else:
            user_fmt = "%(message)s"
            dev_fmt = "[%(levelname)s] %(message)s"

        self.user_formatter = logging.Formatter(user_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        self.dev_formatter = logging.Formatter(dev_fmt, datefmt="%Y-%m-%d %H:%M:%S")

        # Update all handlers with new formatters
        for handler in self.user_logger.handlers:
            if hasattr(handler, "setFormatter"):
                handler.setFormatter(self.user_formatter)
        for handler in self.dev_logger.handlers:
            if hasattr(handler, "setFormatter"):
                handler.setFormatter(self.dev_formatter)

    def __init__(self, verbose: bool = False, append_mode: bool = False):
        """Initialize the logging system.

        Args:
            verbose: Enable verbose logging to user log
            append_mode: Preserve logs across sessions
        """
        self._verbose = verbose
        self._append_mode = append_mode
        self.error_count = 0
        self.error_callback: Optional[Callable] = None

        # Create loggers
        self.user_logger = logging.getLogger("wow_cleanup.user")
        self.dev_logger = logging.getLogger("wow_cleanup.dev")

        # Set levels
        self.user_logger.setLevel(logging.INFO)
        self.dev_logger.setLevel(logging.DEBUG)

        # Prevent propagation to root logger
        self.user_logger.propagate = False
        self.dev_logger.propagate = False

        # Create formatters
        self.user_formatter = logging.Formatter(
            "[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.dev_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Text widget handlers (will be set when UI is ready)
        self.user_text_handler: Optional[TextWidgetHandler] = None
        self.dev_text_handler: Optional[TextWidgetHandler] = None
        self.session_handler: Optional[SessionSeparatorHandler] = None

        # File handlers
        self._setup_file_handlers()

        # Previous log content (for append mode)
        self.previous_log: Optional[str] = None
        if self._append_mode:
            self.load_previous_log()

    def _setup_file_handlers(self) -> None:
        """Set up rotating file handlers for persistent logging."""
        log_dir = Path.home() / ".wow_cleanup_tool"
        log_dir.mkdir(parents=True, exist_ok=True)

        # User log file handler (with rotation)
        user_log_file = log_dir / "user_log.txt"
        if not self._append_mode and user_log_file.exists():
            user_log_file.unlink()  # Clear log if not in append mode

        user_file_handler = logging.handlers.RotatingFileHandler(
            user_log_file, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"  # 1MB
        )
        user_file_handler.setFormatter(self.user_formatter)
        user_file_handler.setLevel(logging.INFO)
        self.user_logger.addHandler(user_file_handler)

        # Developer log file handler (with rotation, separate file)
        dev_log_file = log_dir / "dev_log.txt"
        dev_file_handler = logging.handlers.RotatingFileHandler(
            dev_log_file,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3,
            encoding="utf-8",
        )
        dev_file_handler.setFormatter(self.dev_formatter)
        dev_file_handler.setLevel(logging.DEBUG)
        self.dev_logger.addHandler(dev_file_handler)

    def set_verbose(self, verbose: bool) -> None:
        """Enable or disable verbose logging.

        Args:
            verbose: True to enable verbose/debug messages in user log
        """
        self._verbose = verbose

    def set_append_mode(self, append_mode: bool) -> None:
        """Enable or disable append mode for user log.

        Args:
            append_mode: True to preserve log across sessions
        """
        self._append_mode = append_mode

    def set_error_callback(self, callback: Callable) -> None:
        """Set callback function to notify when errors occur.

        Args:
            callback: Function to call with error count
        """
        self.error_callback = callback

    def load_previous_log(self) -> bool:
        """Load previous session logs from disk if append mode is enabled.

        Returns:
            True if logs were loaded, False otherwise
        """
        if not self._append_mode:
            return False

        from core.settings import load_user_log

        previous_content = load_user_log()

        if previous_content:
            self.previous_log = previous_content
            return True
        return False

    def attach_text_widget(self, text_widget) -> None:
        """Attach a tk.Text widget for user logs.

        Args:
            text_widget: tkinter.Text widget for main log tab
        """
        try:
            text_widget.configure(state="normal")
            text_widget.delete("1.0", "end")

            # Load current log file content directly from disk
            try:
                log_dir = Path.home() / ".wow_cleanup_tool"
                user_log_file = log_dir / "user_log.txt"
                if user_log_file.exists():
                    with open(user_log_file, "r", encoding="utf-8") as f:
                        log_content = f.read()
                        if log_content:
                            text_widget.insert("end", log_content)
            except Exception:
                pass

            # Add previous sessions if append mode
            if self.previous_log:
                text_widget.insert("end", self.previous_log)
                if not self.previous_log.endswith("\n"):
                    text_widget.insert("end", "\n")

            text_widget.configure(state="disabled")
        except Exception:
            pass

        # Create or update text widget handler
        if self.user_text_handler:
            self.user_text_handler.set_widget(text_widget)
        else:
            self.user_text_handler = TextWidgetHandler(text_widget)
            self.user_text_handler.setFormatter(self.user_formatter)
            self.user_text_handler.setLevel(logging.INFO)
            self.user_logger.addHandler(self.user_text_handler)

        # Create or update session separator handler
        if self._append_mode:
            if self.session_handler:
                self.session_handler.set_widget(text_widget)
            else:
                self.session_handler = SessionSeparatorHandler(text_widget)
                self.session_handler.setLevel(logging.INFO)
                self.user_logger.addHandler(self.session_handler)

    def attach_dev_text_widget(self, dev_text_widget) -> None:
        """Attach a tk.Text widget for developer logs.

        Args:
            dev_text_widget: tkinter.Text widget for developer tab
        """
        try:
            dev_text_widget.configure(state="normal")
            dev_text_widget.delete("1.0", "end")

            # Load current developer log file content directly from disk
            try:
                log_dir = Path.home() / ".wow_cleanup_tool"
                dev_log_file = log_dir / "dev_log.txt"
                if dev_log_file.exists():
                    with open(dev_log_file, "r", encoding="utf-8") as f:
                        log_content = f.read()
                        if log_content:
                            dev_text_widget.insert("end", log_content)
            except Exception:
                pass

            dev_text_widget.configure(state="disabled")
        except Exception:
            pass

        # Create or update dev text widget handler
        if self.dev_text_handler:
            self.dev_text_handler.set_widget(dev_text_widget)
        else:
            self.dev_text_handler = TextWidgetHandler(dev_text_widget)
            self.dev_text_handler.setFormatter(self.dev_formatter)
            self.dev_text_handler.setLevel(logging.DEBUG)
            self.dev_logger.addHandler(self.dev_text_handler)

    def clear(self) -> None:
        """Clear text widget contents.

        Note: File logs are preserved (managed by rotation).
        """
        if self.user_text_handler and self.user_text_handler.text_widget:
            try:
                widget = self.user_text_handler.text_widget
                widget.configure(state="normal")
                widget.delete("1.0", "end")
                widget.configure(state="disabled")
            except Exception:
                pass

        if self.dev_text_handler and self.dev_text_handler.text_widget:
            try:
                widget = self.dev_text_handler.text_widget
                widget.configure(state="normal")
                widget.delete("1.0", "end")
                widget.configure(state="disabled")
            except Exception:
                pass

        self.error_count = 0
        if self.error_callback:
            try:
                self.error_callback(0)
            except Exception:
                pass

    def log(self, text: str) -> None:
        """Log a user-facing message (always shown)."""
        self.user_logger.info(text)

    def verbose(self, text: str) -> None:
        """Log verbose operation message (shown only if verbose enabled)."""
        if self._verbose:
            self.user_logger.info(text)

    def debug(self, text: str) -> None:
        """Log debug message (only shown in developer tab)."""
        self.dev_logger.debug(text)

    def error(self, text: str) -> None:
        """Log error message (developer tab, increments error count)."""
        self.error_count += 1
        self.dev_logger.error(text)

    def warning(self, text: str) -> None:
        """Log warning message (developer tab)."""
        self.dev_logger.warning(text)

    def set_verbose(self, verbose: bool) -> None:
        self._verbose = verbose

    def set_append_mode(self, append: bool) -> None:
        self._append_mode = append

    def error(self, text: str) -> None:
        """Log error message (only shown in developer tab).

        Args:
            text: Error message to log
        """
        self.dev_logger.error(text)
        self.error_count += 1

        if self.error_callback:
            try:
                self.error_callback(self.error_count)
            except Exception:
                pass

    def warning(self, text: str) -> None:
        """Log warning message (shown in developer tab).

        Args:
            text: Warning message to log
        """
        self.dev_logger.warning(text)

    def get_lines(self) -> list:
        """Get user log content as list of lines (for compatibility).

        Returns:
            List of log lines from text widget
        """
        if self.user_text_handler and self.user_text_handler.text_widget:
            try:
                content = self.user_text_handler.text_widget.get("1.0", "end-1c")
                return content.split("\n") if content else []
            except Exception:
                return []
        return []

    def get_dev_log(self) -> str:
        """Get developer log content from dev text widget.

        Returns:
            Developer log content, or empty string if not available
        """
        if self.dev_text_handler and self.dev_text_handler.text_widget:
            try:
                return self.dev_text_handler.text_widget.get("1.0", "end-1c")
            except Exception:
                return ""
        return ""

    def save_log_to_disk(self) -> bool:
        """Save current user log to disk if append mode is enabled.

        Returns:
            True if saved successfully, False otherwise
        """
        if not self._append_mode:
            return False

        if self.user_text_handler and self.user_text_handler.text_widget:
            try:
                log_content = self.user_text_handler.text_widget.get("1.0", "end-1c")

                from core.settings import save_user_log

                return save_user_log(log_content)
            except Exception:
                return False
        return False


# Primary logger class exported as Logger
Logger = WoWLogger
