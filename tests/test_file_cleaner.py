"""Unit tests for FileCleaner module."""

import unittest
import sys
import os
import tempfile
import shutil

# Add src directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from operations.file_cleaner import FileCleaner


class TestFileCleaner(unittest.TestCase):
    """Tests for FileCleaner functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = FileCleaner(max_workers=2)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test FileCleaner initializes correctly."""
        scanner = FileCleaner(max_workers=4)
        self.assertEqual(scanner.max_workers, 4)
        self.assertIsNone(scanner.logger)

    def test_bak_old_pattern(self):
        """Test regex pattern matches .bak and .old files."""
        pattern = FileCleaner.BAK_OLD_PATTERN

        # Should match
        self.assertTrue(pattern.search("file.bak"))
        self.assertTrue(pattern.search("file.old"))
        self.assertTrue(pattern.search("FILE.BAK"))  # Case insensitive
        self.assertTrue(pattern.search("FILE.OLD"))
        self.assertTrue(pattern.search("my.config.bak"))
        self.assertTrue(pattern.search(".bak"))  # Hidden file with .bak extension

        # Should not match
        self.assertIsNone(pattern.search("file.txt"))
        self.assertIsNone(pattern.search("backup"))
        self.assertIsNone(pattern.search("old_file"))
        self.assertIsNone(pattern.search("bakfile"))

    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        results = self.scanner._scan_version(self.temp_dir)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)

    def test_scan_directory_with_bak_files(self):
        """Test scanning directory with .bak files."""
        # Create test files
        test_files = ["config.bak", "settings.old", "data.txt", "backup.BAK"]
        for filename in test_files:
            file_path = os.path.join(self.temp_dir, filename)
            open(file_path, "w").close()

        results = self.scanner._scan_version(self.temp_dir)

        # Should find 3 .bak/.old files
        self.assertEqual(len(results), 3)

        # Verify correct files found
        result_names = {os.path.basename(p) for p in results}
        self.assertIn("config.bak", result_names)
        self.assertIn("settings.old", result_names)
        self.assertIn("backup.BAK", result_names)
        self.assertNotIn("data.txt", result_names)

    def test_scan_nested_directories(self):
        """Test scanning nested directory structure."""
        # Create nested structure
        subdir1 = os.path.join(self.temp_dir, "subdir1")
        subdir2 = os.path.join(subdir1, "subdir2")
        os.makedirs(subdir2)

        # Create files at different levels
        open(os.path.join(self.temp_dir, "root.bak"), "w").close()
        open(os.path.join(subdir1, "level1.old"), "w").close()
        open(os.path.join(subdir2, "level2.bak"), "w").close()
        open(os.path.join(subdir2, "normal.txt"), "w").close()

        results = self.scanner._scan_version(self.temp_dir)

        # Should find all 3 .bak/.old files recursively
        self.assertEqual(len(results), 3)

        result_names = {os.path.basename(p) for p in results}
        self.assertIn("root.bak", result_names)
        self.assertIn("level1.old", result_names)
        self.assertIn("level2.bak", result_names)

    def test_scan_with_permission_errors(self):
        """Test scanner handles permission errors gracefully."""
        # Create a directory with a file
        subdir = os.path.join(self.temp_dir, "test")
        os.makedirs(subdir)
        test_file = os.path.join(subdir, "test.bak")
        open(test_file, "w").close()

        # Scanner should handle errors and continue
        # (On Windows, we can't easily create permission issues in temp dir,
        # so this test mainly verifies no exceptions are raised)
        results = self.scanner._scan_version(self.temp_dir)
        self.assertIsInstance(results, list)


class TestFileCleanerWithPathManager(unittest.TestCase):
    """Tests for FileCleaner integration with PathManager."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = FileCleaner(max_workers=2)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_scan_all_flavors_mock(self):
        """Test scan_all_flavors with mock PathManager."""

        # Create mock PathManager
        class MockPathManager:
            def detect_flavors(self, wow_path):
                return {"_retail_": "Retail (Live)", "_classic_": "Classic"}

        # Create fake flavor directories
        retail_dir = os.path.join(self.temp_dir, "_retail_")
        classic_dir = os.path.join(self.temp_dir, "_classic_")
        os.makedirs(retail_dir)
        os.makedirs(classic_dir)

        # Add some .bak files
        open(os.path.join(retail_dir, "retail.bak"), "w").close()
        open(os.path.join(classic_dir, "classic.old"), "w").close()

        mock_pm = MockPathManager()
        results = self.scanner.scan_all_flavors(self.temp_dir, mock_pm)

        # Should have results for both flavors
        self.assertIn("_retail_", results)
        self.assertIn("_classic_", results)
        self.assertEqual(len(results["_retail_"]), 1)
        self.assertEqual(len(results["_classic_"]), 1)


if __name__ == "__main__":
    unittest.main()
