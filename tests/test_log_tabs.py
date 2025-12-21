"""Unit tests for LogTab and DeveloperTab UI classes."""

import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

try:
    import tkinter as tk

    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False

if TK_AVAILABLE:
    from ui.tabs.log_tab import LogTab
    from ui.tabs.developer_tab import DeveloperTab

    class DummyLoc:
        def _(self, key):
            return key

    class DummyLogControls:
        pass

    class TestLogTabUI(unittest.TestCase):
        def setUp(self):
            try:
                self.root = tk.Tk()
                self.root.withdraw()
            except Exception:
                self.root = None
            self.loc = DummyLoc()
            self.log_controls = DummyLogControls()

        def tearDown(self):
            if hasattr(self, "root") and self.root:
                try:
                    self.root.destroy()
                except Exception:
                    pass

        def test_log_tab_widgets_created(self):
            if not self.root:
                self.skipTest("Tkinter root not initialized.")
            tab = LogTab(self.root, self.loc, self.log_controls)
            self.assertIsNotNone(tab.frame)
            self.assertTrue(hasattr(tab, "log_text"))
            controls = tab.frame.grid_slaves(row=0, column=0)[0]
            btn_texts = [
                w.cget("text") for w in controls.winfo_children() if hasattr(w, "cget")
            ]
            self.assertIn("btn_clear_log", btn_texts)
            self.assertIn("btn_save_log", btn_texts)
            self.assertIn("btn_copy_log", btn_texts)

        def test_log_tab_grid_layout(self):
            if not self.root:
                self.skipTest("Tkinter root not initialized.")
            tab = LogTab(self.root, self.loc, self.log_controls)
            info = tab.log_text.grid_info()
            self.assertEqual(int(info["row"]), 1)
            self.assertEqual(int(info["column"]), 0)

    class TestDeveloperTabUI(unittest.TestCase):
        def setUp(self):
            try:
                self.root = tk.Tk()
                self.root.withdraw()
            except Exception:
                self.root = None
            self.loc = DummyLoc()
            self.log_controls = DummyLogControls()

        def tearDown(self):
            if hasattr(self, "root") and self.root:
                try:
                    self.root.destroy()
                except Exception:
                    pass

        def test_developer_tab_widgets_created(self):
            if not self.root:
                self.skipTest("Tkinter root not initialized.")
            tab = DeveloperTab(self.root, self.loc, self.log_controls)
            self.assertIsNotNone(tab.frame)
            self.assertTrue(hasattr(tab, "log_text"))
            controls = tab.frame.grid_slaves(row=0, column=0)[0]
            btn_texts = [
                w.cget("text") for w in controls.winfo_children() if hasattr(w, "cget")
            ]
            self.assertIn("btn_clear_log", btn_texts)
            self.assertIn("btn_save_log", btn_texts)
            self.assertIn("btn_copy_log", btn_texts)

        def test_developer_tab_grid_layout(self):
            if not self.root:
                self.skipTest("Tkinter root not initialized.")
            tab = DeveloperTab(self.root, self.loc, self.log_controls)
            info = tab.log_text.grid_info()
            self.assertEqual(int(info["row"]), 1)
            self.assertEqual(int(info["column"]), 0)


if __name__ == "__main__":
    unittest.main()
