"""Unit tests for OrphanScanner module.

Tests cover orphan SavedVariables detection including:
- Detection of orphaned addon .lua and .bak files
- Protection of Blizzard_ .lua files
- Proper handling of directory structures
- Edge cases and error handling

Created: January 1, 2026
"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from operations.orphan_scanner import OrphanScanner


class MockLogger:
    """Mock logger for testing."""

    def __init__(self):
        self.messages = []
        self.errors = []

    def error(self, msg):
        """Log error message."""
        self.errors.append(msg)


class TestOrphanScannerBasic(unittest.TestCase):
    """Tests for OrphanScanner basic functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = OrphanScanner(max_workers=2)
        self.mock_logger = MockLogger()

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test OrphanScanner initializes correctly."""
        scanner = OrphanScanner(max_workers=4)
        self.assertEqual(scanner.max_workers, 4)
        self.assertIsNone(scanner.logger)

    def test_get_installed_addons(self):
        """Test detection of installed addons from Interface/AddOns directory."""
        # Create mock addon directories
        addons_path = os.path.join(self.temp_dir, "Interface", "AddOns")
        os.makedirs(addons_path)

        addon_names = ["DBM-Core", "Recount", "AtlasLoot"]
        for addon_name in addon_names:
            addon_dir = os.path.join(addons_path, addon_name)
            os.makedirs(addon_dir)

        # Get installed addons
        installed = self.scanner._get_installed_addons(addons_path)

        # Should have all addons (case-insensitive)
        self.assertEqual(len(installed), 3)
        self.assertIn("dbm-core", installed)
        self.assertIn("recount", installed)
        self.assertIn("atlasloot", installed)

    def test_get_installed_addons_empty_directory(self):
        """Test handling of empty Interface/AddOns directory."""
        addons_path = os.path.join(self.temp_dir, "Interface", "AddOns")
        os.makedirs(addons_path)

        installed = self.scanner._get_installed_addons(addons_path)

        self.assertEqual(len(installed), 0)

    def test_get_installed_addons_nonexistent_path(self):
        """Test handling of nonexistent Interface/AddOns directory."""
        addons_path = os.path.join(self.temp_dir, "nonexistent", "AddOns")

        installed = self.scanner._get_installed_addons(addons_path)

        self.assertEqual(len(installed), 0)


class TestOrphanDetection(unittest.TestCase):
    """Tests for orphan SavedVariables detection."""

    def setUp(self):
        """Set up test fixtures with WoW directory structure."""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = OrphanScanner(max_workers=2, logger=None)

        # Create WoW version structure
        self.version_path = os.path.join(self.temp_dir, "_retail_")
        os.makedirs(self.version_path)

        # Create Interface/AddOns directory
        self.addons_path = os.path.join(self.version_path, "Interface", "AddOns")
        os.makedirs(self.addons_path)

        # Create WTF/Account/SavedVariables
        self.sv_path = os.path.join(
            self.version_path, "WTF", "Account", "TestAccount", "SavedVariables"
        )
        os.makedirs(self.sv_path)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_detect_orphaned_lua_file(self):
        """Test detection of orphaned .lua file."""
        # Create installed addon
        os.makedirs(os.path.join(self.addons_path, "InstalledAddon"))

        # Create both installed and orphaned SavedVariables
        with open(os.path.join(self.sv_path, "InstalledAddon.lua"), "w") as f:
            f.write("-- installed addon")
        with open(os.path.join(self.sv_path, "OrphanedAddon.lua"), "w") as f:
            f.write("-- orphaned addon")

        orphans = self.scanner._scan_version(self.version_path)

        # Should only find the orphaned addon
        self.assertEqual(len(orphans), 1)
        self.assertTrue(orphans[0].endswith("OrphanedAddon.lua"))

    def test_detect_orphaned_bak_file(self):
        """Test detection of orphaned .bak file."""
        # No installed addons for these files
        with open(os.path.join(self.sv_path, "OldAddon.bak"), "w") as f:
            f.write("-- backup")

        orphans = self.scanner._scan_version(self.version_path)

        # Should find the orphaned .bak file
        self.assertEqual(len(orphans), 1)
        self.assertTrue(orphans[0].endswith("OldAddon.bak"))

    def test_skip_blizzard_lua_files(self):
        """Test that Blizzard_ .lua files are NOT marked as orphans."""
        # Create Blizzard_ SavedVariables (these are core game files)
        with open(
            os.path.join(self.sv_path, "Blizzard_CompactRaidFrames.lua"), "w"
        ) as f:
            f.write("-- blizzard file")

        orphans = self.scanner._scan_version(self.version_path)

        # Should NOT find any orphans (Blizzard_ .lua files are protected)
        self.assertEqual(len(orphans), 0)

    def test_blizzard_bak_files_are_orphaned(self):
        """Test that Blizzard_ .bak files CAN be marked as orphans."""
        # Create Blizzard_ .bak file (backup, safe to remove)
        with open(
            os.path.join(self.sv_path, "Blizzard_CompactRaidFrames.bak"), "w"
        ) as f:
            f.write("-- blizzard backup")

        orphans = self.scanner._scan_version(self.version_path)

        # Should find the orphaned .bak file (even though it's Blizzard_)
        self.assertEqual(len(orphans), 1)
        self.assertTrue(orphans[0].endswith("Blizzard_CompactRaidFrames.bak"))

    def test_ignore_non_lua_bak_files(self):
        """Test that non-.lua and non-.bak files are ignored."""
        # Create various files
        with open(os.path.join(self.sv_path, "addon.txt"), "w") as f:
            f.write("text file")
        with open(os.path.join(self.sv_path, "addon.db"), "w") as f:
            f.write("database file")

        orphans = self.scanner._scan_version(self.version_path)

        # Should find no orphans
        self.assertEqual(len(orphans), 0)


class TestRealmLevelSavedVariables(unittest.TestCase):
    """Tests for account-level SavedVariables."""

    def setUp(self):
        """Set up test fixtures with account-level structure."""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = OrphanScanner(max_workers=2)

        self.version_path = os.path.join(self.temp_dir, "_classic_")
        os.makedirs(self.version_path)

        # Create Interface/AddOns
        self.addons_path = os.path.join(self.version_path, "Interface", "AddOns")
        os.makedirs(self.addons_path)

        # Create account-level SavedVariables
        self.account_sv_path = os.path.join(
            self.version_path,
            "WTF",
            "Account",
            "TestAccount",
            "SavedVariables",
        )
        os.makedirs(self.account_sv_path)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_detect_account_level_orphans(self):
        """Test detection of orphaned files in account-level SavedVariables."""
        # Create installed addon
        os.makedirs(os.path.join(self.addons_path, "InstalledAddon"))

        # Create SavedVariables at account level (shared across all characters)
        with open(os.path.join(self.account_sv_path, "InstalledAddon.lua"), "w") as f:
            f.write("-- installed")
        with open(os.path.join(self.account_sv_path, "OrphanedAddon.lua"), "w") as f:
            f.write("-- orphaned")

        orphans = self.scanner._scan_version(self.version_path)

        # Should find the orphaned addon
        self.assertEqual(len(orphans), 1)
        self.assertTrue(orphans[0].endswith("OrphanedAddon.lua"))


class TestScanVersions(unittest.TestCase):
    """Tests for scan_versions method (multi-version scanning)."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = OrphanScanner(max_workers=2)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_scan_empty_versions_list(self):
        """Test scanning with empty versions list."""
        result = self.scanner.scan_versions([])

        self.assertEqual(result, {})

    def test_scan_multiple_versions(self):
        """Test scanning multiple WoW versions."""
        # Create two versions
        for flavor in ["_retail_", "_classic_"]:
            version_path = os.path.join(self.temp_dir, flavor)
            os.makedirs(version_path)

            # Create Interface/AddOns
            addons_path = os.path.join(version_path, "Interface", "AddOns")
            os.makedirs(addons_path)
            os.makedirs(os.path.join(addons_path, "MyAddon"))

            # Create account-level SavedVariables
            sv_path = os.path.join(
                version_path, "WTF", "Account", "Acc1", "SavedVariables"
            )
            os.makedirs(sv_path)
            with open(os.path.join(sv_path, "MyAddon.lua"), "w") as f:
                f.write("data")
            with open(os.path.join(sv_path, "Orphaned.lua"), "w") as f:
                f.write("orphan")

        # Scan both versions
        versions = [
            (os.path.join(self.temp_dir, "_retail_"), "Retail"),
            (os.path.join(self.temp_dir, "_classic_"), "Classic"),
        ]
        results = self.scanner.scan_versions(versions)

        # Should find results for both versions
        self.assertEqual(len(results), 2)
        self.assertIn("Retail", results)
        self.assertIn("Classic", results)

        # Each should have 1 orphaned addon
        self.assertEqual(len(results["Retail"]), 1)
        self.assertEqual(len(results["Classic"]), 1)


if __name__ == "__main__":
    unittest.main()
