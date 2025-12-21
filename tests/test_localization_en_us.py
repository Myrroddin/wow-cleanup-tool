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

    # No required startup keys remain; all previous keys are now hard-coded or obsolete.


if __name__ == "__main__":
    unittest.main()
