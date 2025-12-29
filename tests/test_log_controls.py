"""Unit tests for log controls utility functions."""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch, call
from pathlib import Path
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

try:
    import tkinter as tk

    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False

if TK_AVAILABLE:
    from ui.log_controls import (
        clear_user_log,
        copy_user_log,
        open_log_folder,
        delete_user_log,
        clear_dev_log,
        copy_dev_log,
    )

    class DummyLoc:
        def _(self, key):
            return key

    class TestClearUserLog(unittest.TestCase):
        def setUp(self):
            if TK_AVAILABLE:
                try:
                    self.root = tk.Tk()
                    self.root.withdraw()
                    self.log_text = tk.Text(self.root, state="disabled")
                except Exception:
                    self.root = None
                    self.log_text = None

        def tearDown(self):
            if hasattr(self, "root") and self.root:
                try:
                    self.root.destroy()
                except Exception:
                    pass

        def test_clear_user_log_clears_display(self):
            if not self.log_text:
                self.skipTest("Tkinter not available")
            self.log_text.configure(state="normal")
            self.log_text.insert("1.0", "Test content")
            self.log_text.configure(state="disabled")
            clear_user_log(self.log_text)
            content = self.log_text.get("1.0", "end-1c")
            self.assertEqual(content, "")

        @patch("ui.log_controls.get_user_log_file")
        def test_clear_user_log_deletes_file_when_append_off(self, mock_get_file):
            if not self.log_text:
                self.skipTest("Tkinter not available")
            # Create a temp file
            with tempfile.NamedTemporaryFile(delete=False) as f:
                temp_file = Path(f.name)
            mock_get_file.return_value = temp_file

            # Mock logger with append mode OFF
            mock_logger = MagicMock()
            mock_logger._append_mode = False

            clear_user_log(self.log_text, mock_logger)

            # File should be deleted
            self.assertFalse(temp_file.exists())

        @patch("ui.log_controls.get_user_log_file")
        def test_clear_user_log_preserves_file_when_append_on(self, mock_get_file):
            if not self.log_text:
                self.skipTest("Tkinter not available")
            # Create a temp file
            with tempfile.NamedTemporaryFile(delete=False) as f:
                temp_file = Path(f.name)
            mock_get_file.return_value = temp_file

            # Mock logger with append mode ON
            mock_logger = MagicMock()
            mock_logger._append_mode = True

            clear_user_log(self.log_text, mock_logger)

            # File should still exist
            self.assertTrue(temp_file.exists())
            # Clean up
            temp_file.unlink()

    class TestCopyUserLog(unittest.TestCase):
        def setUp(self):
            if TK_AVAILABLE:
                try:
                    self.root = tk.Tk()
                    self.root.withdraw()
                    self.log_text = tk.Text(self.root)
                    self.loc = DummyLoc()
                except Exception:
                    self.root = None
                    self.log_text = None

        def tearDown(self):
            if hasattr(self, "root") and self.root:
                try:
                    self.root.destroy()
                except Exception:
                    pass

        @patch("ui.log_controls.messagebox")
        def test_copy_user_log_copies_to_clipboard(self, mock_msgbox):
            if not self.log_text:
                self.skipTest("Tkinter not available")
            test_content = "Test log content"
            self.log_text.insert("1.0", test_content)
            copy_user_log(self.root, self.log_text, self.loc)
            clipboard = self.root.clipboard_get()
            self.assertEqual(clipboard, test_content)

    class TestOpenLogFolder(unittest.TestCase):
        @patch("ui.log_controls.get_user_log_file")
        @patch("ui.log_controls.os.startfile")
        @patch("ui.log_controls.sys.platform", "win32")
        def test_open_log_folder_windows(self, mock_startfile, mock_get_file):
            temp_dir = Path(tempfile.mkdtemp())
            mock_get_file.return_value = temp_dir / "user_log.txt"
            open_log_folder()
            mock_startfile.assert_called_once_with(temp_dir)
            # Clean up
            temp_dir.rmdir()

        @patch("ui.log_controls.get_user_log_file")
        @patch("ui.log_controls.subprocess.run")
        @patch("ui.log_controls.sys.platform", "darwin")
        def test_open_log_folder_macos(self, mock_run, mock_get_file):
            temp_dir = Path(tempfile.mkdtemp())
            mock_get_file.return_value = temp_dir / "user_log.txt"
            open_log_folder()
            mock_run.assert_called_once_with(["open", str(temp_dir)])
            # Clean up
            temp_dir.rmdir()

        @patch("ui.log_controls.get_user_log_file")
        @patch("ui.log_controls.subprocess.run")
        @patch("ui.log_controls.sys.platform", "linux")
        def test_open_log_folder_linux(self, mock_run, mock_get_file):
            temp_dir = Path(tempfile.mkdtemp())
            mock_get_file.return_value = temp_dir / "user_log.txt"
            open_log_folder()
            mock_run.assert_called_once_with(["xdg-open", str(temp_dir)])
            # Clean up
            temp_dir.rmdir()

    class TestDeleteUserLog(unittest.TestCase):
        @patch("ui.log_controls.messagebox")
        @patch("ui.log_controls.get_user_log_file")
        def test_delete_user_log_to_trash(self, mock_get_file, mock_msgbox):
            # Create a temp file
            with tempfile.NamedTemporaryFile(delete=False) as f:
                temp_file = Path(f.name)
            mock_get_file.return_value = temp_file

            settings = {"delete_mode": "trash"}
            loc = DummyLoc()

            # Patch send2trash at the point it's imported (inside the function)
            with patch("send2trash.send2trash") as mock_trash:
                delete_user_log(settings, loc)
                mock_trash.assert_called_once_with(str(temp_file))

        @patch("ui.log_controls.messagebox")
        @patch("ui.log_controls.get_user_log_file")
        def test_delete_user_log_permanently(self, mock_get_file, mock_msgbox):
            # Create a temp file
            with tempfile.NamedTemporaryFile(delete=False) as f:
                temp_file = Path(f.name)
            mock_get_file.return_value = temp_file

            settings = {"delete_mode": "permanent"}
            loc = DummyLoc()

            delete_user_log(settings, loc)
            # File should be deleted
            self.assertFalse(temp_file.exists())

    class TestClearDevLog(unittest.TestCase):
        def setUp(self):
            if TK_AVAILABLE:
                try:
                    self.root = tk.Tk()
                    self.root.withdraw()
                    self.dev_text = tk.Text(self.root, state="disabled")
                except Exception:
                    self.root = None
                    self.dev_text = None

        def tearDown(self):
            if hasattr(self, "root") and self.root:
                try:
                    self.root.destroy()
                except Exception:
                    pass

        def test_clear_dev_log_clears_display(self):
            if not self.dev_text:
                self.skipTest("Tkinter not available")
            self.dev_text.configure(state="normal")
            self.dev_text.insert("1.0", "Test dev content")
            self.dev_text.configure(state="disabled")
            clear_dev_log(self.dev_text)
            content = self.dev_text.get("1.0", "end-1c")
            self.assertEqual(content, "")

    class TestCopyDevLog(unittest.TestCase):
        def setUp(self):
            if TK_AVAILABLE:
                try:
                    self.root = tk.Tk()
                    self.root.withdraw()
                    self.loc = DummyLoc()
                except Exception:
                    self.root = None

        def tearDown(self):
            if hasattr(self, "root") and self.root:
                try:
                    self.root.destroy()
                except Exception:
                    pass

        @patch("ui.log_controls.messagebox")
        def test_copy_dev_log_copies_to_clipboard(self, mock_msgbox):
            if not self.root:
                self.skipTest("Tkinter not available")
            mock_logger = MagicMock()
            test_content = "Test dev log content"
            mock_logger.get_dev_log.return_value = test_content
            copy_dev_log(self.root, mock_logger, self.loc)
            clipboard = self.root.clipboard_get()
            self.assertEqual(clipboard, test_content)


if __name__ == "__main__":
    unittest.main()
