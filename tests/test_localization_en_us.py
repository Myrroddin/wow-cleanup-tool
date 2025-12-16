"""Unit tests for en_us localization keys and values."""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from localization import en_us


class TestEnUsLocalization(unittest.TestCase):
    def test_all_keys_are_strings(self):
        for key in en_us.TRANSLATIONS.keys():
            self.assertIsInstance(key, str)

    def test_all_values_are_strings(self):
        for value in en_us.TRANSLATIONS.values():
            self.assertIsInstance(value, str)

    def test_required_startup_keys_exist(self):
        required = [
            "startup_success",
            "startup_error_see_devlog",
            "dev_startup_import_error",
            "dev_startup_dependency_error",
            "dev_startup_settings_error",
            "dev_startup_localization_error",
        ]
        for key in required:
            self.assertIn(key, en_us.TRANSLATIONS)


if __name__ == "__main__":
    unittest.main()
