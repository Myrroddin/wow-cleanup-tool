"""Unit tests for theme padding scaling (TButton)."""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

try:
    import tkinter as tk
    from tkinter import ttk

    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False

if TK_AVAILABLE:
    from core.themes import apply_theme

    class TestThemesButtonPadding(unittest.TestCase):
        """Verify TButton padding scales with font size and honors minimums."""

        def setUp(self):
            try:
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

        @staticmethod
        def _get_padding(style):
            pad = style.lookup("TButton", "padding")
            if isinstance(pad, str):
                try:
                    return tuple(int(x) for x in pad.split())
                except ValueError:
                    return None
            if isinstance(pad, (tuple, list)):
                try:
                    return tuple(int(x) for x in pad)
                except Exception:
                    return None
            return None

        def test_padding_scales_with_font_size(self):
            # Small font should use minimum padding safeguards
            apply_theme(self.root, "light", "TkDefaultFont", 8)
            style = ttk.Style(self.root)
            pad_small = self._get_padding(style)
            self.assertIsNotNone(pad_small)
            self.assertEqual(len(pad_small), 2)
            self.assertGreaterEqual(pad_small[0], 6)
            self.assertGreaterEqual(pad_small[1], 3)

            # Larger font should increase padding proportionally
            apply_theme(self.root, "light", "TkDefaultFont", 16)
            style = ttk.Style(self.root)
            pad_large = self._get_padding(style)
            self.assertIsNotNone(pad_large)
            self.assertEqual(len(pad_large), 2)
            self.assertGreaterEqual(pad_large[0], pad_small[0])
            self.assertGreaterEqual(pad_large[1], pad_small[1])
            self.assertGreaterEqual(pad_large[0], 11)  # int(16 * 0.7)
            self.assertGreaterEqual(pad_large[1], 7)  # int(16 * 0.45)

else:

    class TestThemesButtonPadding(unittest.TestCase):
        """Stub when Tkinter is unavailable."""

        def test_tk_unavailable(self):
            self.skipTest("Tkinter not available")


if __name__ == "__main__":
    unittest.main()
