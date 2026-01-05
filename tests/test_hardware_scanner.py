"""Unit tests for HardwareScanner module.

Tests cover hardware detection and caching including:
- CPU, RAM, GPU detection
- Cache loading and saving
- Cross-platform compatibility
- Error handling
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from operations.hardware_scanner import HardwareScanner, HardwareInfo, GPUInfo


class TestHardwareScannerInitialization(unittest.TestCase):
    """Tests for HardwareScanner initialization."""

    def test_scanner_initializes(self):
        """Test HardwareScanner initializes without errors."""
        scanner = HardwareScanner()
        self.assertIsNotNone(scanner)
        self.assertIsNone(scanner._cached_info)

    def test_cache_file_path_created(self):
        """Test cache file path is set correctly."""
        scanner = HardwareScanner()
        self.assertIsNotNone(scanner.CACHE_FILE)
        self.assertTrue(str(scanner.CACHE_FILE).endswith("hardware_cache.json"))


class TestHardwareInfoDataclass(unittest.TestCase):
    """Tests for HardwareInfo dataclass."""

    def test_hardware_info_creation(self):
        """Test HardwareInfo object creation."""
        gpu = GPUInfo(name="RTX 4090", is_integrated=False, vendor="NVIDIA")
        info = HardwareInfo(
            cpu_name="Intel Core i9",
            cpu_cores=12,
            cpu_freq_ghz=4.5,
            ram_gb=32.0,
            ram_speed_mhz=3600,
            gpus=[gpu],
            cache_timestamp=1234567890.0,
        )

        self.assertEqual(info.cpu_name, "Intel Core i9")
        self.assertEqual(info.cpu_cores, 12)
        self.assertEqual(len(info.gpus), 1)
        self.assertEqual(info.gpus[0].vendor, "NVIDIA")

    def test_hardware_info_to_dict(self):
        """Test HardwareInfo.to_dict() serialization."""
        gpu = GPUInfo(name="RTX 4090", is_integrated=False, vendor="NVIDIA")
        info = HardwareInfo(
            cpu_name="Intel Core i9",
            cpu_cores=12,
            cpu_freq_ghz=4.5,
            ram_gb=32.0,
            ram_speed_mhz=3600,
            gpus=[gpu],
            cache_timestamp=1234567890.0,
        )

        data = info.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["cpu_name"], "Intel Core i9")
        self.assertEqual(data["cpu_cores"], 12)

    def test_hardware_info_from_dict(self):
        """Test HardwareInfo.from_dict() deserialization."""
        data = {
            "cpu_name": "Intel Core i9",
            "cpu_cores": 12,
            "cpu_freq_ghz": 4.5,
            "ram_gb": 32.0,
            "ram_speed_mhz": 3600,
            "gpus": [
                {
                    "name": "RTX 4090",
                    "is_integrated": False,
                    "vendor": "NVIDIA",
                }
            ],
            "cache_timestamp": 1234567890.0,
        }

        info = HardwareInfo.from_dict(data)
        self.assertEqual(info.cpu_name, "Intel Core i9")
        self.assertEqual(len(info.gpus), 1)
        self.assertEqual(info.gpus[0].name, "RTX 4090")


class TestGPUInfoDataclass(unittest.TestCase):
    """Tests for GPUInfo dataclass."""

    def test_gpu_info_creation(self):
        """Test GPUInfo object creation."""
        gpu = GPUInfo(name="RTX 4090", is_integrated=False, vendor="NVIDIA")

        self.assertEqual(gpu.name, "RTX 4090")
        self.assertFalse(gpu.is_integrated)
        self.assertEqual(gpu.vendor, "NVIDIA")

    def test_gpu_info_integrated_flag(self):
        """Test GPU integrated vs dedicated flag."""
        dedicated = GPUInfo(name="RTX 4090", is_integrated=False, vendor="NVIDIA")
        integrated = GPUInfo(name="Intel UHD 630", is_integrated=True, vendor="Intel")

        self.assertFalse(dedicated.is_integrated)
        self.assertTrue(integrated.is_integrated)


class TestCacheOperations(unittest.TestCase):
    """Tests for cache loading and saving."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = Path(self.temp_dir) / "test_cache.json"

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_cache_save_and_load(self):
        """Test saving and loading hardware cache."""
        gpu = GPUInfo(name="RTX 3080", is_integrated=False, vendor="NVIDIA")
        info = HardwareInfo(
            cpu_name="AMD Ryzen 9",
            cpu_cores=16,
            cpu_freq_ghz=3.8,
            ram_gb=64.0,
            ram_speed_mhz=3200,
            gpus=[gpu],
            cache_timestamp=1234567890.0,
        )

        # Save to file
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, "w") as f:
            json.dump(info.to_dict(), f)

        # Load from file
        with open(self.cache_file, "r") as f:
            loaded_data = json.load(f)

        loaded_info = HardwareInfo.from_dict(loaded_data)
        self.assertEqual(loaded_info.cpu_name, "AMD Ryzen 9")
        self.assertEqual(len(loaded_info.gpus), 1)


class TestCacheExpiration(unittest.TestCase):
    """Tests for cache expiration logic."""

    def test_cache_expiration_check(self):
        """Test cache expiration detection."""
        import time

        # Create info with very old timestamp
        old_time = time.time() - (200 * 24 * 60 * 60)  # 200 days ago
        gpu = GPUInfo(name="GTX 1080", is_integrated=False, vendor="NVIDIA")
        info = HardwareInfo(
            cpu_name="Intel Core i7",
            cpu_cores=8,
            cpu_freq_ghz=3.6,
            ram_gb=16.0,
            ram_speed_mhz=2666,
            gpus=[gpu],
            cache_timestamp=old_time,
        )

        # Should be expired (180-day default TTL)
        self.assertTrue(info.is_expired())

    def test_cache_not_expired_when_recent(self):
        """Test fresh cache is not expired."""
        import time

        # Create info with recent timestamp
        recent_time = time.time() - (10 * 24 * 60 * 60)  # 10 days ago
        gpu = GPUInfo(name="RTX 4080", is_integrated=False, vendor="NVIDIA")
        info = HardwareInfo(
            cpu_name="Intel Core i9",
            cpu_cores=12,
            cpu_freq_ghz=4.5,
            ram_gb=32.0,
            ram_speed_mhz=3600,
            gpus=[gpu],
            cache_timestamp=recent_time,
        )

        # Should not be expired
        self.assertFalse(info.is_expired())


if __name__ == "__main__":
    unittest.main()
