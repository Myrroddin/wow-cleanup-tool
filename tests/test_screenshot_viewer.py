"""Tests for screenshot viewer dialog."""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


class TestScreenshotViewer(unittest.TestCase):
    """Test suite for ScreenshotViewer dialog."""

    def test_screenshot_viewer_initialization(self):
        """Test screenshot viewer initialization."""
        from ui.dialogs.screenshot_viewer import ScreenshotViewer

        mock_parent = MagicMock()
        mock_loc = MagicMock()
        settings = {"theme": "dark", "font_family": "Arial", "font_size": 10}

        viewer = ScreenshotViewer(
            mock_parent, mock_loc, "dark", settings, "/path/to/screenshot.png"
        )

        self.assertEqual(viewer.image_path, "/path/to/screenshot.png")
        self.assertIsNone(viewer.photo_image)
        self.assertEqual(viewer.theme_name, "dark")
        self.assertEqual(viewer.settings, settings)

    def test_screenshot_viewer_attributes(self):
        """Test screenshot viewer has expected attributes."""
        from ui.dialogs.screenshot_viewer import ScreenshotViewer

        mock_parent = MagicMock()
        mock_loc = MagicMock()
        settings = {"theme": "light"}

        viewer = ScreenshotViewer(
            mock_parent, mock_loc, "light", settings, "/some/path.jpg"
        )

        # Verify core attributes
        self.assertTrue(hasattr(viewer, "image_path"))
        self.assertTrue(hasattr(viewer, "photo_image"))
        self.assertTrue(hasattr(viewer, "show"))


if __name__ == "__main__":
    unittest.main()
