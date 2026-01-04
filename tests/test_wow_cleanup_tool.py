"""Unit tests for WoWCleanupTool main application logic (smoke tests)."""

import unittest
import tempfile
import sys
import os
import tkinter as tk
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from wow_cleanup_tool import WoWCleanupTool


class TestWoWCleanupToolSmoke(unittest.TestCase):
    def setUp(self):
        # Patch dialogs and UI methods to avoid actual UI interaction
        self.temp_dir = tempfile.TemporaryDirectory()
        self.orig_home = os.environ.get("HOME")
        self.orig_userprofile = os.environ.get("USERPROFILE")
        os.environ["HOME"] = self.temp_dir.name
        os.environ["USERPROFILE"] = self.temp_dir.name
        self.patcher_license = patch("ui.show_license_dialog", return_value=True)
        self.patcher_warning = patch("ui.show_wow_close_warning", return_value=None)
        self.patcher_logger = patch(
            "logging.handlers.RotatingFileHandler", autospec=True
        )
        self.mock_license = self.patcher_license.start()
        self.mock_warning = self.patcher_warning.start()
        self.mock_logger = self.patcher_logger.start()
        self.mock_logger.return_value.level = 20  # logging.INFO
        try:
            self.root = tk.Tk()
            self.root.withdraw()  # Hide window during tests
        except tk.TclError:
            # Tkinter not available in test environment
            self.root = None

    def tearDown(self):
        self.patcher_license.stop()
        self.patcher_warning.stop()
        self.patcher_logger.stop()
        # Only destroy if the root window still exists
        if self.root is not None:
            try:
                if self.root.winfo_exists():
                    self.root.destroy()
            except Exception:
                pass
        if self.orig_home is not None:
            os.environ["HOME"] = self.orig_home
        else:
            del os.environ["HOME"]
        if self.orig_userprofile is not None:
            os.environ["USERPROFILE"] = self.orig_userprofile
        else:
            del os.environ["USERPROFILE"]
        self.temp_dir.cleanup()

    @unittest.skipIf(tk is None, "Tkinter not available")
    def test_app_initialization(self):
        # Should not raise
        if self.root is None:
            self.skipTest("Tkinter not available")
        try:
            WoWCleanupTool(self.root)
        except Exception as e:
            self.fail(f"WoWCleanupTool init raised: {e}")

    @unittest.skipIf(tk is None, "Tkinter not available")
    def test_app_on_close(self):
        if self.root is None:
            self.skipTest("Tkinter not available")
        app = WoWCleanupTool(self.root)
        # Should not raise, and should handle double-destroy gracefully
        try:
            app.on_close()
        except Exception as e:
            import tkinter

            if isinstance(
                e, tkinter.TclError
            ) and "application has been destroyed" in str(e):
                pass  # Acceptable: window already destroyed
            else:
                self.fail(f"WoWCleanupTool.on_close raised: {e}")


if __name__ == "__main__":
    unittest.main()
