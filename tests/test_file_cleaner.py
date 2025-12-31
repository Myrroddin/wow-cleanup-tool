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

    def test_bak_old_file_detection(self):
        """Test FileCleaner detects .bak and .old files."""
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
    """Tests for FileCleaner integration with version scanning."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = FileCleaner(max_workers=2)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_scan_versions_multiple_flavors(self):
        """Test scan_versions with multiple flavor directories."""
        # Create fake flavor directories
        retail_dir = os.path.join(self.temp_dir, "_retail_")
        classic_dir = os.path.join(self.temp_dir, "_classic_")
        os.makedirs(retail_dir)
        os.makedirs(classic_dir)

        # Add some .bak files
        open(os.path.join(retail_dir, "retail.bak"), "w").close()
        open(os.path.join(classic_dir, "classic.old"), "w").close()

        # Scan both versions
        versions = [(retail_dir, "Retail"), (classic_dir, "Classic")]
        results = self.scanner.scan_versions(versions)

        # Should have results for both flavors
        self.assertIn("Retail", results)
        self.assertIn("Classic", results)
        self.assertEqual(len(results["Retail"]), 1)
        self.assertEqual(len(results["Classic"]), 1)

    def test_scan_versions_empty_list(self):
        """Test scan_versions with empty version list."""
        results = self.scanner.scan_versions([])
        self.assertEqual(results, {})

    def test_skip_dirs_custom(self):
        """Test FileCleaner respects custom skip directories."""
        # Create structure with cache directory
        cache_dir = os.path.join(self.temp_dir, "cache")
        normal_dir = os.path.join(self.temp_dir, "addons")
        os.makedirs(cache_dir)
        os.makedirs(normal_dir)

        # Add .bak files to both
        open(os.path.join(cache_dir, "cached.bak"), "w").close()
        open(os.path.join(normal_dir, "addon.bak"), "w").close()

        # Scanner with cache in skip list should not find cached.bak
        results = self.scanner._scan_version(self.temp_dir)

        # Should find addon.bak but skip cache/cached.bak
        result_names = {os.path.basename(p) for p in results}
        self.assertIn("addon.bak", result_names)
        self.assertNotIn("cached.bak", result_names)


if __name__ == "__main__":
    unittest.main()
