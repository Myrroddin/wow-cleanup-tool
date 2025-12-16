"""Unit tests for Logger (WoWLogger) class."""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


from core.logger import Logger


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


if __name__ == "__main__":
    unittest.main()
