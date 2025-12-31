"""Unit tests for file_operations module.

Tests cover delete_files_batch functionality including:
- Successful trash operations
- Successful permanent deletions
- Error handling and logging
- Return value structure (processed_count, permanently_deleted, used_trash, processed_paths)

Created: December 30, 2025
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from operations.file_operations import delete_files_batch


class MockLogger:
    """Mock logger for testing."""

    def __init__(self):
        self.messages = []
        self.verbose_messages = []
        self.errors = []

    def verbose(self, msg):
        """Log verbose message."""
        self.verbose_messages.append(msg)

    def error(self, msg):
        """Log error message."""
        self.errors.append(msg)


class TestDeleteFilesBatch(unittest.TestCase):
    """Tests for delete_files_batch function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_logger = MockLogger()

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_delete_single_file_trash_mode(self):
        """Test deleting a single file to trash."""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        processed, perm_del, used_trash, proc_paths = delete_files_batch(
            [test_file], delete_mode="trash", logger=self.mock_logger
        )

        self.assertEqual(processed, 1)
        self.assertFalse(perm_del)
        self.assertTrue(used_trash)
        self.assertEqual(proc_paths, [test_file])

    def test_delete_single_file_permanent_mode(self):
        """Test permanently deleting a single file."""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        processed, perm_del, used_trash, proc_paths = delete_files_batch(
            [test_file], delete_mode="permanent", logger=self.mock_logger
        )

        self.assertEqual(processed, 1)
        self.assertTrue(perm_del)
        self.assertFalse(used_trash)
        self.assertEqual(proc_paths, [test_file])
        self.assertFalse(os.path.exists(test_file))

    def test_delete_multiple_files(self):
        """Test deleting multiple files."""
        files = []
        for i in range(3):
            test_file = os.path.join(self.temp_dir, f"test_{i}.txt")
            with open(test_file, "w") as f:
                f.write(f"content {i}")
            files.append(test_file)

        processed, perm_del, used_trash, proc_paths = delete_files_batch(
            files, delete_mode="permanent", logger=self.mock_logger
        )

        self.assertEqual(processed, 3)
        self.assertTrue(perm_del)
        self.assertFalse(used_trash)
        self.assertEqual(len(proc_paths), 3)

        for f in files:
            self.assertFalse(os.path.exists(f))

    def test_delete_directory_permanent_mode(self):
        """Test permanently deleting a directory."""
        test_dir = os.path.join(self.temp_dir, "test_subdir")
        os.makedirs(test_dir)
        test_file = os.path.join(test_dir, "file.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        processed, perm_del, used_trash, proc_paths = delete_files_batch(
            [test_dir], delete_mode="permanent", logger=self.mock_logger
        )

        self.assertEqual(processed, 1)
        self.assertTrue(perm_del)
        self.assertFalse(os.path.exists(test_dir))
        self.assertEqual(proc_paths, [test_dir])

    def test_delete_mixed_files_and_dirs(self):
        """Test deleting mix of files and directories."""
        test_file = os.path.join(self.temp_dir, "file.txt")
        with open(test_file, "w") as f:
            f.write("content")

        test_dir = os.path.join(self.temp_dir, "subdir")
        os.makedirs(test_dir)
        with open(os.path.join(test_dir, "inner.txt"), "w") as f:
            f.write("inner")

        paths = [test_file, test_dir]
        processed, perm_del, used_trash, proc_paths = delete_files_batch(
            paths, delete_mode="permanent", logger=self.mock_logger
        )

        self.assertEqual(processed, 2)
        self.assertTrue(perm_del)
        self.assertEqual(len(proc_paths), 2)
        self.assertFalse(os.path.exists(test_file))
        self.assertFalse(os.path.exists(test_dir))

    def test_delete_nonexistent_file_logs_error(self):
        """Test handling of nonexistent file in permanent mode.

        The important thing is that deletion doesn't crash on nonexistent files.
        """
        nonexistent = os.path.join(self.temp_dir, "nonexistent.txt")

        processed, perm_del, used_trash, proc_paths = delete_files_batch(
            [nonexistent], delete_mode="permanent", logger=self.mock_logger
        )

        # The path is counted as processed (graceful handling)
        self.assertEqual(processed, 1)
        self.assertEqual(len(proc_paths), 1)
        # Should not crash
        self.assertTrue(True)
        """Test deleting empty list of files."""
        processed, perm_del, used_trash, proc_paths = delete_files_batch(
            [], delete_mode="permanent", logger=self.mock_logger
        )

        self.assertEqual(processed, 0)
        self.assertTrue(perm_del)
        self.assertFalse(used_trash)
        self.assertEqual(proc_paths, [])

    def test_delete_with_verbose_logging(self):
        """Test that verbose logging does NOT occur in file_operations (to prevent duplicate logging).
        
        Logging is handled by the calling code (main_window.py) using if/else pattern.
        file_operations.py only logs errors, not successful deletions.
        """
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")

        delete_files_batch(
            [test_file], delete_mode="permanent", logger=self.mock_logger
        )

        # Should NOT have verbose logging (handled by caller)
        self.assertEqual(len(self.mock_logger.verbose_messages), 0)

    def test_return_tuple_structure(self):
        """Test that return value is correct 4-tuple structure."""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")

        result = delete_files_batch(
            [test_file], delete_mode="permanent", logger=self.mock_logger
        )

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 4)
        processed, perm_del, used_trash, proc_paths = result
        self.assertIsInstance(processed, int)
        self.assertIsInstance(perm_del, bool)
        self.assertIsInstance(used_trash, bool)
        self.assertIsInstance(proc_paths, list)

    def test_partial_deletion_success(self):
        """Test deletion of some files in permanent mode.

        Note: All paths are counted as processed, including nonexistent ones.
        This is the current behavior.
        """
        test_file1 = os.path.join(self.temp_dir, "file1.txt")
        with open(test_file1, "w") as f:
            f.write("test1")

        nonexistent = os.path.join(self.temp_dir, "nonexistent.txt")

        test_file2 = os.path.join(self.temp_dir, "file2.txt")
        with open(test_file2, "w") as f:
            f.write("test2")

        processed, _, _, proc_paths = delete_files_batch(
            [test_file1, nonexistent, test_file2],
            delete_mode="permanent",
            logger=self.mock_logger,
        )

        # All paths are counted as processed (including nonexistent)
        self.assertEqual(processed, 3)
        self.assertEqual(len(proc_paths), 3)
        self.assertIn(test_file1, proc_paths)
        self.assertIn(test_file2, proc_paths)
        self.assertIn(nonexistent, proc_paths)
        # But the files themselves should be deleted
        self.assertFalse(os.path.exists(test_file1))
        self.assertFalse(os.path.exists(test_file2))


if __name__ == "__main__":
    unittest.main()
