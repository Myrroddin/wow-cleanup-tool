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

    def test_required_user_log_keys_exist(self):
        """Test that all required user log localization keys exist."""
        required_keys = [
            "user_log_normal_app_started",
            "user_log_normal_app_failure",
            "user_log_normal_no_game_versions",
            "user_log_normal_wow_detected",
            "user_log_normal_wow_validated",
            "user_log_normal_removed_files",
            "user_log_verbose_wow_detected",
            "user_log_verbose_wow_validated",
            "user_log_verbose_removed_file",
        ]

        for key in required_keys:
            self.assertIn(key, en_us.TRANSLATIONS, f"Missing key: {key}")

    def test_removed_files_key_format(self):
        """Test that removed_files key has format placeholders."""
        key = "user_log_normal_removed_files"
        value = en_us.TRANSLATIONS[key]
        self.assertIn("{}", value)

    def test_verbose_removed_file_key_format(self):
        """Test that verbose_removed_file key has format placeholders."""
        key = "user_log_verbose_removed_file"
        value = en_us.TRANSLATIONS[key]
        self.assertIn("{}", value)

    def test_unknown_version_key_exists(self):
        """Test that unknown_version key exists."""
        self.assertIn("unknown_version", en_us.TRANSLATIONS)
        self.assertEqual(en_us.TRANSLATIONS["unknown_version"], "Unknown version")
