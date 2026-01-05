"""Unit tests for config_handler module.

Tests cover Config.wtf file operations including:
- Reading and parsing CVars
- Writing CVars
- GPU name cleaning
- Best GPU selection
"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from operations.config_handler import (
    read_config,
    write_config,
    update_cvar,
    get_cvar,
    clean_gpu_name,
    select_best_gpu,
)


class TestConfigReading(unittest.TestCase):
    """Tests for reading Config.wtf files."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "Config.wtf"

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_read_empty_config(self):
        """Test reading empty Config.wtf file."""
        self.config_file.touch()
        cvars = read_config(self.config_file)
        self.assertEqual(cvars, {})

    def test_read_config_with_cvars(self):
        """Test reading Config.wtf with CVars."""
        content = 'SET gxAdapter "NVIDIA GeForce RTX 4090"\nSET maxFPS "240"\n'
        self.config_file.write_text(content)

        cvars = read_config(self.config_file)
        self.assertEqual(len(cvars), 2)
        self.assertEqual(cvars["gxAdapter"], "NVIDIA GeForce RTX 4090")
        self.assertEqual(cvars["maxFPS"], "240")

    def test_read_nonexistent_config(self):
        """Test reading nonexistent Config.wtf returns empty dict."""
        nonexistent = Path(self.temp_dir) / "nonexistent.wtf"
        cvars = read_config(nonexistent)
        self.assertEqual(cvars, {})

    def test_read_config_ignores_comments(self):
        """Test that comments are not parsed as CVars."""
        content = '-- This is a comment\nSET maxFPS "60"\n'
        self.config_file.write_text(content)

        cvars = read_config(self.config_file)
        self.assertEqual(len(cvars), 1)
        self.assertEqual(cvars["maxFPS"], "60")


class TestConfigWriting(unittest.TestCase):
    """Tests for writing Config.wtf files."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "Config.wtf"

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_write_config_creates_file(self):
        """Test write_config creates file if it doesn't exist."""
        cvars = {"maxFPS": "120", "gxAdapter": "RTX 4090"}
        success = write_config(self.config_file, cvars)

        self.assertTrue(success)
        self.assertTrue(self.config_file.exists())

    def test_write_config_content(self):
        """Test write_config writes correct format."""
        cvars = {"maxFPS": "120", "vsync": "0"}
        write_config(self.config_file, cvars)

        content = self.config_file.read_text()
        self.assertIn('SET maxFPS "120"', content)
        self.assertIn('SET vsync "0"', content)

    def test_write_config_overwrites_existing(self):
        """Test write_config overwrites existing file."""
        # Write initial content
        cvars1 = {"maxFPS": "60"}
        write_config(self.config_file, cvars1)

        # Overwrite with new content
        cvars2 = {"maxFPS": "240", "vsync": "1"}
        write_config(self.config_file, cvars2)

        content = self.config_file.read_text()
        self.assertIn('SET maxFPS "240"', content)
        self.assertIn('SET vsync "1"', content)

    def test_write_config_sorted_output(self):
        """Test write_config outputs CVars in sorted order."""
        cvars = {"zebra": "1", "apple": "2", "middle": "3"}
        write_config(self.config_file, cvars)

        content = self.config_file.read_text()
        lines = content.strip().split("\n")

        # Extract CVar names in order
        names = [line.split()[1] for line in lines]
        self.assertEqual(names, sorted(names))


class TestCVarOperations(unittest.TestCase):
    """Tests for individual CVar operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "Config.wtf"
        # Create a config with some CVars
        initial = {"maxFPS": "60", "vsync": "1"}
        write_config(self.config_file, initial)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_update_cvar_existing(self):
        """Test updating an existing CVar."""
        success = update_cvar(self.config_file, "maxFPS", "240")

        self.assertTrue(success)
        cvars = read_config(self.config_file)
        self.assertEqual(cvars["maxFPS"], "240")

    def test_update_cvar_new(self):
        """Test creating a new CVar."""
        success = update_cvar(self.config_file, "newCVar", "value")

        self.assertTrue(success)
        cvars = read_config(self.config_file)
        self.assertEqual(cvars["newCVar"], "value")

    def test_get_cvar_existing(self):
        """Test retrieving an existing CVar."""
        value = get_cvar(self.config_file, "maxFPS")
        self.assertEqual(value, "60")

    def test_get_cvar_nonexistent(self):
        """Test retrieving a nonexistent CVar returns None."""
        value = get_cvar(self.config_file, "nonexistent")
        self.assertIsNone(value)


class TestGPUNameCleaning(unittest.TestCase):
    """Tests for GPU name cleaning function."""

    def test_clean_nvidia_prefix(self):
        """Test cleaning NVIDIA prefix."""
        result = clean_gpu_name("NVIDIA GeForce RTX 4090")
        self.assertEqual(result, "GeForce RTX 4090")

    def test_clean_amd_prefix(self):
        """Test cleaning AMD prefix."""
        result = clean_gpu_name("AMD Radeon RX 7900 XT")
        self.assertEqual(result, "Radeon RX 7900 XT")

    def test_clean_intel_prefix(self):
        """Test cleaning Intel prefix."""
        result = clean_gpu_name("Intel UHD Graphics 630")
        self.assertEqual(result, "UHD Graphics 630")

    def test_clean_apple_prefix(self):
        """Test cleaning Apple prefix."""
        result = clean_gpu_name("Apple M1 GPU")
        self.assertEqual(result, "M1 GPU")

    def test_clean_no_prefix(self):
        """Test GPU without prefix is unchanged."""
        result = clean_gpu_name("GeForce RTX 4090")
        self.assertEqual(result, "GeForce RTX 4090")

    def test_clean_multiple_spaces(self):
        """Test cleaning handles multiple spaces."""
        result = clean_gpu_name("NVIDIA  GeForce  RTX 4090")
        # Should still remove NVIDIA prefix
        self.assertNotIn("NVIDIA", result)


class TestSelectBestGPU(unittest.TestCase):
    """Tests for GPU selection logic."""

    def test_select_single_gpu(self):
        """Test selecting from single GPU."""
        from operations.hardware_scanner import GPUInfo

        gpus = [GPUInfo(name="RTX 4090", is_integrated=False, vendor="NVIDIA")]
        best = select_best_gpu(gpus)
        self.assertEqual(best, "RTX 4090")

    def test_select_prefers_dedicated(self):
        """Test selection prefers dedicated over integrated."""
        from operations.hardware_scanner import GPUInfo

        gpus = [
            GPUInfo(name="Intel UHD", is_integrated=True, vendor="Intel"),
            GPUInfo(name="RTX 4090", is_integrated=False, vendor="NVIDIA"),
        ]
        best = select_best_gpu(gpus)
        self.assertEqual(best, "RTX 4090")

    def test_select_empty_list(self):
        """Test selection with empty list returns None."""
        best = select_best_gpu([])
        self.assertIsNone(best)

    def test_select_only_integrated(self):
        """Test selection when only integrated GPUs available."""
        from operations.hardware_scanner import GPUInfo

        gpus = [
            GPUInfo(name="Intel UHD 630", is_integrated=True, vendor="Intel"),
            GPUInfo(name="Intel Iris Xe", is_integrated=True, vendor="Intel"),
        ]
        best = select_best_gpu(gpus)
        self.assertIsNotNone(best)
        # Should be cleaned name without "Intel " prefix
        self.assertEqual(best, "UHD 630")


if __name__ == "__main__":
    unittest.main()
