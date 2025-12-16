"""Unit tests for WoWCleanupTool main application logic (smoke tests)."""

import unittest
import sys
import os
import tkinter as tk
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from wow_cleanup_tool import WoWCleanupTool


class TestWoWCleanupToolSmoke(unittest.TestCase):
    def setUp(self):
        # Patch dialogs and UI methods to avoid actual UI interaction
        self.patcher_license = patch("ui.show_license_dialog", return_value=True)
        self.patcher_warning = patch("ui.show_wow_close_warning", return_value=None)
        self.patcher_logger = patch(
            "logging.handlers.RotatingFileHandler", autospec=True
        )
        self.mock_license = self.patcher_license.start()
        self.mock_warning = self.patcher_warning.start()
        self.mock_logger = self.patcher_logger.start()
        self.mock_logger.return_value.level = 20  # logging.INFO
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests

    def tearDown(self):
        self.patcher_license.stop()
        self.patcher_warning.stop()
        self.patcher_logger.stop()
        self.root.destroy()

    def test_app_initialization(self):
        # Should not raise
        try:
            app = WoWCleanupTool(self.root)
        except Exception as e:
            self.fail(f"WoWCleanupTool init raised: {e}")

    def test_app_on_close(self):
        app = WoWCleanupTool(self.root)
        # Should not raise
        try:
            app.on_close()
        except Exception as e:
            self.fail(f"WoWCleanupTool.on_close raised: {e}")


if __name__ == "__main__":
    unittest.main()
