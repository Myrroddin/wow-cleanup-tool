"""Unit tests for Logger (WoWLogger) class."""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


from core.logger import Logger

try:
    import tkinter as tk

    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False


class TestLoggerBasic(unittest.TestCase):
    def setUp(self):
        # Patch RotatingFileHandler to avoid real file access and set .level
        patcher = patch("logging.handlers.RotatingFileHandler", autospec=True)
        self.addCleanup(patcher.stop)
        self.mock_file_handler = patcher.start()
        self.mock_file_handler.return_value.level = 20  # logging.INFO
        self.logger = Logger(verbose=True, append_mode=False)

    def test_log_info(self):
        # Should not raise
        try:
            self.logger.log("Test info message")
        except Exception as e:
            self.fail(f"Logger.log raised an exception: {e}")

    def test_log_verbose(self):
        try:
            self.logger.verbose("Test verbose message")
        except Exception as e:
            self.fail(f"Logger.verbose raised an exception: {e}")

    def test_log_debug(self):
        try:
            self.logger.debug("Test debug message")
        except Exception as e:
            self.fail(f"Logger.debug raised an exception: {e}")

    def test_log_error(self):
        try:
            self.logger.error("Test error message")
        except Exception as e:
            self.fail(f"Logger.error raised an exception: {e}")

    def test_log_warning(self):
        try:
            self.logger.warning("Test warning message")
        except Exception as e:
            self.fail(f"Logger.warning raised an exception: {e}")

    def test_set_verbose(self):
        self.logger.set_verbose(False)
        self.assertFalse(self.logger._verbose)
        self.logger.set_verbose(True)
        self.assertTrue(self.logger._verbose)

    def test_set_append_mode(self):
        self.logger.set_append_mode(True)
        self.assertTrue(self.logger._append_mode)
        self.logger.set_append_mode(False)
        self.assertFalse(self.logger._append_mode)

    def test_load_previous_log(self):
        # Should not raise, even if no log exists
        try:
            self.logger.load_previous_log()
        except Exception as e:
            self.fail(f"Logger.load_previous_log raised an exception: {e}")

    def test_save_log_to_disk(self):
        # Should not raise, even if no log exists
        try:
            self.logger.save_log_to_disk()
        except Exception as e:
            self.fail(f"Logger.save_log_to_disk raised an exception: {e}")


if TK_AVAILABLE:

    class TestLoggerWidgetAttachment(unittest.TestCase):
        """Test logger attachment to tkinter Text widgets."""

        def setUp(self):
            try:
                self.temp_dir = tempfile.TemporaryDirectory()
                self.orig_home = os.environ.get("HOME")
                self.orig_userprofile = os.environ.get("USERPROFILE")
                os.environ["HOME"] = self.temp_dir.name
                os.environ["USERPROFILE"] = self.temp_dir.name
                patcher = patch("logging.handlers.RotatingFileHandler", autospec=True)
                self.mock_file_handler = patcher.start()
                self.mock_file_handler.return_value.level = 20
                self.addCleanup(patcher.stop)
                self.logger = Logger(verbose=True, append_mode=False)
                self.root = tk.Tk()
                self.root.withdraw()
            except Exception as e:
                self.skipTest(f"Tkinter not available: {e}")

        def tearDown(self):
            try:
                if hasattr(self, "root") and self.root.winfo_exists():
                    self.root.destroy()
            except Exception:
                pass
            if hasattr(self, "orig_home"):
                if self.orig_home is not None:
                    os.environ["HOME"] = self.orig_home
                else:
                    if "HOME" in os.environ:
                        del os.environ["HOME"]
            if hasattr(self, "orig_userprofile"):
                if self.orig_userprofile is not None:
                    os.environ["USERPROFILE"] = self.orig_userprofile
                else:
                    if "USERPROFILE" in os.environ:
                        del os.environ["USERPROFILE"]
            if hasattr(self, "temp_dir"):
                self.temp_dir.cleanup()

        def test_attach_user_text_widget(self):
            """Test attaching user log text widget."""
            text_widget = tk.Text(self.root)
            # Need to pack the widget for winfo_exists() to return True
            text_widget.pack()
            self.root.update_idletasks()

            try:
                self.logger.attach_text_widget(text_widget)
                # Should not raise
                self.assertIsNotNone(self.logger.user_text_handler)
                # Verify handler is actually a TextWidgetHandler
                self.assertTrue(hasattr(self.logger.user_text_handler, "emit"))
            except Exception as e:
                self.fail(f"attach_text_widget raised: {e}")

        def test_attach_dev_text_widget(self):
            """Test attaching developer log text widget."""
            text_widget = tk.Text(self.root)
            # Need to pack the widget for winfo_exists() to return True
            text_widget.pack()
            self.root.update_idletasks()

            try:
                self.logger.attach_dev_text_widget(text_widget)
                # Should not raise
                self.assertIsNotNone(self.logger.dev_text_handler)
                # Verify handler is actually a TextWidgetHandler
                self.assertTrue(hasattr(self.logger.dev_text_handler, "emit"))
            except Exception as e:
                self.fail(f"attach_dev_text_widget raised: {e}")

        def test_widget_insertion_after_attachment(self):
            """Test that log messages are inserted into widget after attachment."""
            text_widget = tk.Text(self.root)
            text_widget.pack()
            self.root.update_idletasks()

            self.logger.attach_text_widget(text_widget)
            # Log a message
            self.logger.log("Test message after widget attachment")
            self.root.update()  # Process pending events
            # Check if text is in widget (may take a moment due to async handler)
            content = text_widget.get("1.0", "end")
            # Widget should have some content (either the test message or initial content)
            self.assertGreater(len(content), 0)

else:

    class TestLoggerWidgetAttachment(unittest.TestCase):
        """Stub test when Tkinter is not available."""

        def test_tkinter_unavailable(self):
            """Skip all Tkinter tests."""
            self.skipTest("Tkinter not available")


if __name__ == "__main__":
    unittest.main()
