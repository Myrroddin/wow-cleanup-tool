"""Unit tests for error handler utility."""

import unittest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from core import error_handler


class TestErrorHandler(unittest.TestCase):
    def test_handle_top_level_exception(self):
        # Patch input and traceback.print_exc to avoid blocking
        with patch("builtins.input", return_value=""), patch(
            "traceback.print_exc"
        ) as mock_print_exc:
            try:
                error_handler.handle_top_level_exception(Exception("test error"))
            except Exception as e:
                self.fail(f"handle_top_level_exception raised: {e}")
            mock_print_exc.assert_called()


if __name__ == "__main__":
    unittest.main()
