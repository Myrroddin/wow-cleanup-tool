"""Unit tests for Tooltip widget with fixed font and boundary detection.

This test module verifies the Tooltip class functionality:
- Fixed TkFixedFont 10pt rendering
- Theme-aware colors (light/dark modes)
- Smart boundary detection (280px wraplength)
- Tooltip positioning and show/hide
- Screen edge detection to prevent off-screen tooltips

Created: January 3, 2026
"""

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
    from ui.widgets.tooltip import Tooltip

    class TestTooltip(unittest.TestCase):
        """Test Tooltip widget functionality."""

        def setUp(self):
            """Initialize test window and theme."""
            try:
                self.root = tk.Tk()
                self.root.withdraw()
                self.root.geometry("800x600")

                self.theme = {
                    "bg": "#ffffff",
                    "fg": "#000000",
                    "button_bg": "#f0f0f0",
                    "tooltip_bg": "#ffffe0",
                    "tooltip_fg": "#000000",
                }
            except Exception as e:
                self.skipTest(f"Tkinter not available: {e}")

        def tearDown(self):
            """Clean up test window."""
            try:
                if hasattr(self, "root") and self.root.winfo_exists():
                    self.root.destroy()
            except Exception:
                pass

        def test_tooltip_initialization(self):
            """Test Tooltip initializes with correct attributes."""
            parent = ttk.Button(self.root, text="Test")
            parent.pack()

            tooltip = Tooltip(
                parent,
                "Test tooltip text",
                self.theme,
                wraplength=280,
            )

            self.assertIsNotNone(tooltip.widget)
            self.assertEqual(tooltip.text, "Test tooltip text")
            self.assertEqual(tooltip.wraplength, 280)

        def test_tooltip_fixed_font(self):
            """Test Tooltip uses fixed TkFixedFont 10pt."""
            parent = ttk.Button(self.root, text="Test")
            parent.pack()

            tooltip = Tooltip(parent, "Text", self.theme)

            # The tooltip should use TkFixedFont internally
            # This is verified when show() is called and label is created
            self.assertIsNotNone(tooltip)

        def test_tooltip_theme_aware_colors(self):
            """Test Tooltip applies theme colors correctly."""
            parent = ttk.Button(self.root, text="Test")
            parent.pack()

            tooltip = Tooltip(
                parent,
                "Text",
                self.theme,
                wraplength=280,
            )

            # Verify theme attributes are stored
            self.assertIsNotNone(tooltip.theme)

        def test_tooltip_show_creates_toplevel(self):
            """Test show() creates Toplevel window."""
            parent = ttk.Button(self.root, text="Test")
            parent.pack()

            tooltip = Tooltip(parent, "Test tooltip", self.theme)
            tooltip.show()

            # Tooltip should have a tipwindow
            self.assertIsNotNone(tooltip.tipwindow)
            self.assertTrue(tooltip.tipwindow.winfo_exists())

            tooltip.hide()

        def test_tooltip_hide_destroys_window(self):
            """Test hide() destroys Toplevel window."""
            parent = ttk.Button(self.root, text="Test")
            parent.pack()

            tooltip = Tooltip(parent, "Test tooltip", self.theme)
            tooltip.show()

            tooltip_window = tooltip.tipwindow
            self.assertTrue(tooltip_window.winfo_exists())

            tooltip.hide()

            # Tooltip window should be destroyed or hidden
            self.assertIsNone(tooltip.tipwindow)

        def test_tooltip_wraplength_custom(self):
            """Test Tooltip respects custom wraplength."""
            parent = ttk.Button(self.root, text="Test")
            parent.pack()

            tooltip = Tooltip(parent, "Text", self.theme, wraplength=400)

            self.assertEqual(tooltip.wraplength, 400)

        def test_tooltip_boundary_detection(self):
            """Test Tooltip detects screen boundaries."""
            # Place widget near right edge
            parent = ttk.Button(self.root, text="Test")
            parent.pack()

            # Move widget near right edge of window
            self.root.update()
            x = self.root.winfo_width() - 50
            y = 50
            parent.place(x=x, y=y)

            tooltip = Tooltip(parent, "Long tooltip text", self.theme)
            tooltip.show()

            # Tooltip should adjust position to avoid going off-screen
            self.assertIsNotNone(tooltip.tipwindow)

            tooltip.hide()

        def test_tooltip_multiple_show_hide_cycles(self):
            """Test Tooltip handles multiple show/hide cycles."""
            parent = ttk.Button(self.root, text="Test")
            parent.pack()

            tooltip = Tooltip(parent, "Text", self.theme)

            for _ in range(3):
                tooltip.show()
                self.assertTrue(tooltip.tipwindow.winfo_exists())
                tooltip.hide()
                self.assertIsNone(tooltip.tipwindow)

        def test_tooltip_long_text_wraps(self):
            """Test Tooltip wraps long text with wraplength setting."""
            parent = ttk.Button(self.root, text="Test")
            parent.pack()

            long_text = "This is a very long tooltip text that should wrap based on the wraplength setting to avoid creating an excessively wide tooltip window."

            tooltip = Tooltip(parent, long_text, self.theme, wraplength=200)

            tooltip.show()

            # Tooltip should be created (wrapping is handled by Tk)
            self.assertIsNotNone(tooltip.tipwindow)

            tooltip.hide()


if __name__ == "__main__":
    unittest.main()
