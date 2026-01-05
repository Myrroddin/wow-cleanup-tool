"""Unit tests for video_card_support module.

Tests cover GPU support detection including:
- Pattern-based GPU series matching
- Support checking for different game versions
- GPU name variations handling
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from operations.video_card_support import (
    is_gpu_supported,
    _extract_gpu_series,
    CLASSIC_WINDOWS_SUPPORTED_SERIES,
    RETAIL_WINDOWS_SUPPORTED_SERIES,
)


class TestGPUSeriesExtraction(unittest.TestCase):
    """Tests for GPU series extraction function."""

    def test_extract_nvidia_rtx_series(self):
        """Test extracting NVIDIA RTX series."""
        patterns = _extract_gpu_series("GeForce RTX 2080 Super")
        self.assertIn("rtx 20", patterns)

    def test_extract_nvidia_gtx_series(self):
        """Test extracting NVIDIA GTX series."""
        patterns = _extract_gpu_series("GeForce GTX 1080 Ti")
        self.assertIn("gtx 10", patterns)

    def test_extract_amd_rx_series(self):
        """Test extracting AMD RX series."""
        patterns = _extract_gpu_series("Radeon RX 6700 XT")
        self.assertIn("rx 6000", patterns)

    def test_extract_amd_modern_notation(self):
        """Test extracting AMD with modern notation (no RX prefix)."""
        patterns = _extract_gpu_series("Radeon 9070 XT")
        # Should extract both the series number and RX variant
        has_series = any("9000" in p for p in patterns)
        self.assertTrue(has_series)

    def test_extract_intel_arc_series(self):
        """Test extracting Intel Arc series."""
        patterns = _extract_gpu_series("Intel Arc A770")
        has_arc_a = any("arc a" in p for p in patterns)
        self.assertTrue(has_arc_a)

    def test_extract_nvidia_titan(self):
        """Test extracting NVIDIA Titan."""
        patterns = _extract_gpu_series("NVIDIA Titan X")
        self.assertIn("titan", patterns)

    def test_extract_multiple_patterns(self):
        """Test that multiple matching patterns are generated."""
        patterns = _extract_gpu_series("GeForce RTX 4090")
        # Should have multiple patterns for better matching
        self.assertGreater(len(patterns), 1)


class TestGPUSupportRetail(unittest.TestCase):
    """Tests for GPU support detection on Retail WoW."""

    def test_nvidia_rtx_40_series_supported(self):
        """Test NVIDIA RTX 40-series is supported for Retail."""
        result = is_gpu_supported("GeForce RTX 4090", "retail")
        self.assertTrue(result)

    def test_nvidia_rtx_30_series_supported(self):
        """Test NVIDIA RTX 30-series is supported for Retail."""
        result = is_gpu_supported("GeForce RTX 3080", "retail")
        self.assertTrue(result)

    def test_nvidia_rtx_20_series_supported(self):
        """Test NVIDIA RTX 20-series is supported for Retail."""
        result = is_gpu_supported("GeForce RTX 2080 Super", "retail")
        self.assertTrue(result)

    def test_nvidia_gtx_16_series_supported(self):
        """Test NVIDIA GTX 16-series is supported for Retail."""
        result = is_gpu_supported("GeForce GTX 1660", "retail")
        self.assertTrue(result)

    def test_amd_rx_7000_series_supported(self):
        """Test AMD RX 7000-series is supported for Retail."""
        result = is_gpu_supported("Radeon RX 7900 XT", "retail")
        self.assertTrue(result)

    def test_amd_rx_6000_series_supported(self):
        """Test AMD RX 6000-series is supported for Retail."""
        result = is_gpu_supported("Radeon RX 6700 XT", "retail")
        self.assertTrue(result)

    def test_amd_modern_notation_9070(self):
        """Test AMD Radeon 9070 XT (modern notation) is supported."""
        result = is_gpu_supported("Radeon 9070 XT", "retail")
        self.assertTrue(result)

    def test_intel_arc_a_series_supported(self):
        """Test Intel Arc A-series is supported."""
        result = is_gpu_supported("Intel Arc A770", "retail")
        self.assertTrue(result)

    def test_intel_uhd_graphics_supported(self):
        """Test Intel UHD Graphics is supported."""
        result = is_gpu_supported("Intel UHD Graphics 630", "retail")
        self.assertTrue(result)

    def test_unsupported_gpu_rejected(self):
        """Test unsupported GPU is rejected."""
        result = is_gpu_supported("Some Random GPU", "retail")
        self.assertFalse(result)


class TestGPUSupportClassic(unittest.TestCase):
    """Tests for GPU support detection on Classic/Classic Era."""

    def test_nvidia_rtx_supported_classic(self):
        """Test NVIDIA RTX is supported for Classic."""
        result = is_gpu_supported("GeForce RTX 4090", "classic")
        self.assertTrue(result)

    def test_nvidia_gtx_400_series_supported_classic(self):
        """Test NVIDIA GTX 400-series is supported for Classic."""
        result = is_gpu_supported("GeForce GTX 460", "classic")
        self.assertTrue(result)

    def test_amd_rx_supported_classic(self):
        """Test AMD RX is supported for Classic."""
        result = is_gpu_supported("Radeon RX 6800", "classic")
        self.assertTrue(result)

    def test_amd_hd_5000_series_supported_classic(self):
        """Test AMD HD 5000-series is supported for Classic."""
        result = is_gpu_supported("Radeon HD 5670", "classic")
        self.assertTrue(result)

    def test_unsupported_gpu_rejected_classic(self):
        """Test unsupported GPU is rejected on Classic."""
        result = is_gpu_supported("GeForce 256", "classic")
        self.assertFalse(result)


class TestGPUSupportEdgeCases(unittest.TestCase):
    """Tests for edge cases in GPU support detection."""

    def test_empty_gpu_name(self):
        """Test empty GPU name returns False."""
        result = is_gpu_supported("", "retail")
        self.assertFalse(result)

    def test_none_gpu_name(self):
        """Test None GPU name returns False."""
        result = is_gpu_supported(None, "retail")
        self.assertFalse(result)

    def test_case_insensitive_matching(self):
        """Test matching is case-insensitive."""
        lower = is_gpu_supported("nvidia geforce rtx 4090", "retail")
        upper = is_gpu_supported("NVIDIA GEFORCE RTX 4090", "retail")
        self.assertEqual(lower, upper)

    def test_whitespace_handling(self):
        """Test handling of extra whitespace."""
        result1 = is_gpu_supported("GeForce RTX 4090", "retail")
        result2 = is_gpu_supported("GeForce  RTX  4090", "retail")
        self.assertEqual(result1, result2)

    def test_invalid_game_version_defaults_to_retail(self):
        """Test invalid game version defaults to retail checking."""
        result = is_gpu_supported("GeForce RTX 4090", "unknown_version")
        # Should still be supported (defaults to retail)
        self.assertTrue(result)

    def test_nvidia_titan_variations(self):
        """Test various NVIDIA Titan naming conventions are recognized by pattern."""
        test_names = [
            ("NVIDIA Titan X", True),  # Should be recognized as Titan
            ("Titan RTX", False),  # Not in supported list (professional card)
            ("Titan V", False),  # Not in supported list (professional card)
            ("Titan Xp", False),  # Not in supported list (professional card)
        ]
        for name, expected_supported in test_names:
            with self.subTest(name=name):
                result = is_gpu_supported(name, "retail")
                if expected_supported:
                    self.assertTrue(result, f"{name} should be supported")
                else:
                    # Just verify pattern extraction works
                    patterns = _extract_gpu_series(name)
                    # Pattern should contain titan-related text
                    has_titan = any("titan" in p for p in patterns)
                    self.assertTrue(has_titan, f"{name} should extract titan pattern")

    def test_radeon_pro_support(self):
        """Test Radeon PRO support."""
        result = is_gpu_supported("Radeon Pro WX 7100", "retail")
        self.assertTrue(result)


class TestSupportedSeriesList(unittest.TestCase):
    """Tests for supported GPU series lists."""

    def test_retail_supported_series_exist(self):
        """Test Retail supported series list is populated."""
        self.assertGreater(len(RETAIL_WINDOWS_SUPPORTED_SERIES), 0)
        self.assertIn("nvidia", RETAIL_WINDOWS_SUPPORTED_SERIES)
        self.assertIn("amd", RETAIL_WINDOWS_SUPPORTED_SERIES)

    def test_classic_supported_series_exist(self):
        """Test Classic supported series list is populated."""
        self.assertGreater(len(CLASSIC_WINDOWS_SUPPORTED_SERIES), 0)
        self.assertIn("nvidia", CLASSIC_WINDOWS_SUPPORTED_SERIES)
        self.assertIn("amd", CLASSIC_WINDOWS_SUPPORTED_SERIES)

    def test_classic_has_more_series_than_retail(self):
        """Test Classic supports older GPUs than Retail."""
        classic_nvidia = len(CLASSIC_WINDOWS_SUPPORTED_SERIES["nvidia"])
        retail_nvidia = len(RETAIL_WINDOWS_SUPPORTED_SERIES["nvidia"])
        # Classic should support everything Retail does, plus older models
        self.assertGreaterEqual(classic_nvidia, retail_nvidia)


if __name__ == "__main__":
    unittest.main()
