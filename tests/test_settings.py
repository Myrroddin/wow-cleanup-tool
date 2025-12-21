"""Unit tests for settings management."""

import unittest
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from core import settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        # Use a temp directory for settings
        self.temp_dir = tempfile.TemporaryDirectory()
        self.orig_home = os.environ.get("HOME")
        self.orig_userprofile = os.environ.get("USERPROFILE")
        os.environ["HOME"] = self.temp_dir.name
        os.environ["USERPROFILE"] = self.temp_dir.name

    def tearDown(self):
        if self.orig_home is not None:
            os.environ["HOME"] = self.orig_home
        else:
            del os.environ["HOME"]
        if self.orig_userprofile is not None:
            os.environ["USERPROFILE"] = self.orig_userprofile
        else:
            del os.environ["USERPROFILE"]
        self.temp_dir.cleanup()

    def test_load_and_save_settings(self):
        # Save and load settings
        test_settings = {"language": "en_us", "theme": "dark", "font_size": 12}
        result = settings.save_settings(test_settings)
        self.assertTrue(result)
        loaded = settings.load_settings()
        self.assertEqual(loaded["language"], "en_us")
        self.assertEqual(loaded["theme"], "dark")
        self.assertEqual(loaded["font_size"], 12)

    def test_save_and_load_user_log(self):
        content = "Test log content"
        result = settings.save_user_log(content)
        self.assertTrue(result)
        loaded = settings.load_user_log()
        self.assertEqual(loaded, content)

    def test_get_settings_file(self):
        path = settings.get_settings_file()
        self.assertIsInstance(path, Path)

    def test_get_user_log_file(self):
        path = settings.get_user_log_file()
        self.assertIsInstance(path, Path)


if __name__ == "__main__":
    unittest.main()
