"""Unit tests for WoW path manager module."""
import unittest
import sys
import os
import tempfile
import shutil


# Add src directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from wow.path_manager import PathManager


class TestPathManagerInitialization(unittest.TestCase):
    """Tests for PathManager initialization."""
    
    def test_initialization(self):
        """Test PathManager initializes with correct default values."""
        pm = PathManager()
        self.assertIsNone(pm.wow_path)
        self.assertIsInstance(pm.detected_flavors, dict)
        self.assertEqual(len(pm.detected_flavors), 0)


class TestPathManagerConstants(unittest.TestCase):
    """Tests for PathManager class constants."""
    
    def test_common_paths_structure(self):
        """Test COMMON_PATHS is a list of strings."""
        self.assertIsInstance(PathManager.COMMON_PATHS, list)
        self.assertGreater(len(PathManager.COMMON_PATHS), 0)
        for path in PathManager.COMMON_PATHS:
            self.assertIsInstance(path, str)
    
    def test_wow_flavors_structure(self):
        """Test WOW_FLAVORS has correct structure."""
        self.assertIsInstance(PathManager.WOW_FLAVORS, dict)
        self.assertGreater(len(PathManager.WOW_FLAVORS), 0)
        # Check expected flavors exist
        self.assertIn('_retail_', PathManager.WOW_FLAVORS)
        self.assertIn('_classic_', PathManager.WOW_FLAVORS)
    
    def test_wow_flavors_display_names(self):
        """Test all flavors have localization keys."""
        for flavor_dir, loc_key in PathManager.WOW_FLAVORS.items():
            self.assertIsInstance(flavor_dir, str)
            self.assertIsInstance(loc_key, str)
            self.assertTrue(flavor_dir.startswith('_'))
            self.assertTrue(flavor_dir.endswith('_'))
            # Check that loc_key follows expected pattern
            self.assertTrue(loc_key.startswith('flavor_'))


class TestFlavorDisplayNames(unittest.TestCase):
    """Tests for flavor display name localization."""
    
    def test_get_flavor_display_name_without_localization(self):
        """Test getting flavor display names without localization instance."""
        pm = PathManager()
        
        # Should return English fallback
        self.assertEqual(pm.get_flavor_display_name('_retail_'), 'Retail (Live)')
        self.assertEqual(pm.get_flavor_display_name('_classic_'), 'Classic')
        self.assertEqual(pm.get_flavor_display_name('_ptr_'), 'Public Test Realm')
        self.assertEqual(pm.get_flavor_display_name('_beta_'), 'Beta')
        self.assertEqual(pm.get_flavor_display_name('_classic_era_'), 'Classic Era')
    
    def test_get_flavor_display_name_unknown_flavor(self):
        """Test getting display name for unknown flavor."""
        pm = PathManager()
        
        # Should return the flavor_dir itself as fallback
        self.assertEqual(pm.get_flavor_display_name('_unknown_'), '_unknown_')


class TestPathValidation(unittest.TestCase):
    """Tests for path validation methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pm = PathManager()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_validate_nonexistent_path(self):
        """Test validation of nonexistent path."""
        result = self.pm.validate_wow_path('C:\\NonexistentPath\\WoW')
        self.assertFalse(result)
    
    def test_validate_empty_path(self):
        """Test validation of empty path."""
        result = self.pm.validate_wow_path('')
        self.assertFalse(result)
    
    def test_validate_none_path(self):
        """Test validation of None-like path."""
        # Type checker doesn't allow None, but empty string tests same logic
        result = self.pm.validate_wow_path('')
        self.assertFalse(result)
    
    def test_validate_path_without_flavors(self):
        """Test validation of path without flavor directories."""
        # Create empty directory
        result = self.pm.validate_wow_path(self.temp_dir)
        self.assertFalse(result)
    
    def test_validate_path_with_valid_flavor(self):
        """Test validation of path with a valid flavor directory."""
        # Create a realistic WoW structure
        retail_path = os.path.join(self.temp_dir, '_retail_')
        wtf_path = os.path.join(retail_path, 'WTF')
        account_path = os.path.join(wtf_path, 'Account')
        
        os.makedirs(account_path)
        
        # Create a dummy account folder to make it populated
        test_account = os.path.join(account_path, 'TESTACCOUNT')
        os.makedirs(test_account)
        
        # Should now be valid
        result = self.pm.validate_wow_path(self.temp_dir)
        self.assertTrue(result)


class TestFlavorDetection(unittest.TestCase):
    """Tests for flavor detection methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pm = PathManager()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_detect_flavors_no_path(self):
        """Test flavor detection with no path set."""
        flavors = self.pm.detect_flavors()
        self.assertIsInstance(flavors, dict)
        self.assertEqual(len(flavors), 0)
    
    def test_detect_flavors_empty_directory(self):
        """Test flavor detection in empty directory."""
        flavors = self.pm.detect_flavors(self.temp_dir)
        self.assertIsInstance(flavors, dict)
        self.assertEqual(len(flavors), 0)
    
    def test_detect_single_flavor(self):
        """Test detection of single flavor."""
        # Create retail flavor
        retail_path = os.path.join(self.temp_dir, '_retail_')
        wtf_path = os.path.join(retail_path, 'WTF')
        account_path = os.path.join(wtf_path, 'Account')
        os.makedirs(account_path)
        
        # Create populated account
        test_account = os.path.join(account_path, 'TESTACCOUNT')
        os.makedirs(test_account)
        
        flavors = self.pm.detect_flavors(self.temp_dir)
        self.assertEqual(len(flavors), 1)
        self.assertIn('_retail_', flavors)
    
    def test_detect_multiple_flavors(self):
        """Test detection of multiple flavors."""
        # Create retail and classic flavors
        for flavor in ['_retail_', '_classic_']:
            flavor_path = os.path.join(self.temp_dir, flavor)
            wtf_path = os.path.join(flavor_path, 'WTF')
            account_path = os.path.join(wtf_path, 'Account')
            os.makedirs(account_path)
            
            # Create populated account
            test_account = os.path.join(account_path, 'TESTACCOUNT')
            os.makedirs(test_account)
        
        flavors = self.pm.detect_flavors(self.temp_dir)
        self.assertEqual(len(flavors), 2)
        self.assertIn('_retail_', flavors)
        self.assertIn('_classic_', flavors)


class TestPathGetters(unittest.TestCase):
    """Tests for path getter methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pm = PathManager()
        self.temp_dir = tempfile.mkdtemp()
        self.pm.wow_path = self.temp_dir
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_get_flavor_path_no_wow_path(self):
        """Test get_flavor_path with no WoW path set."""
        pm = PathManager()  # New instance without wow_path
        result = pm.get_flavor_path('_retail_')
        self.assertIsNone(result)
    
    def test_get_flavor_path_nonexistent_flavor(self):
        """Test get_flavor_path for nonexistent flavor."""
        result = self.pm.get_flavor_path('_retail_')
        self.assertIsNone(result)
    
    def test_get_flavor_path_existing_flavor(self):
        """Test get_flavor_path for existing flavor."""
        retail_path = os.path.join(self.temp_dir, '_retail_')
        os.makedirs(retail_path)
        
        result = self.pm.get_flavor_path('_retail_')
        self.assertIsNotNone(result)
        if result:  # Type narrowing for type checker
            self.assertTrue(os.path.exists(result))
    
    def test_get_addons_path_nonexistent(self):
        """Test get_addons_path for nonexistent path."""
        result = self.pm.get_addons_path('_retail_')
        self.assertIsNone(result)
    
    def test_get_addons_path_existing(self):
        """Test get_addons_path for existing path."""
        addons_path = os.path.join(self.temp_dir, '_retail_', 'Interface', 'AddOns')
        os.makedirs(addons_path)
        
        result = self.pm.get_addons_path('_retail_')
        self.assertIsNotNone(result)
        if result:  # Type narrowing for type checker
            self.assertTrue(os.path.exists(result))
    
    def test_get_wtf_path_nonexistent(self):
        """Test get_wtf_path for nonexistent path."""
        result = self.pm.get_wtf_path('_retail_')
        self.assertIsNone(result)
    
    def test_get_wtf_path_existing(self):
        """Test get_wtf_path for existing path."""
        wtf_path = os.path.join(self.temp_dir, '_retail_', 'WTF')
        os.makedirs(wtf_path)
        
        result = self.pm.get_wtf_path('_retail_')
        self.assertIsNotNone(result)
        if result:  # Type narrowing for type checker
            self.assertTrue(os.path.exists(result))
    
    def test_get_screenshots_path_no_wow_path(self):
        """Test get_screenshots_path with no WoW path."""
        pm = PathManager()
        result = pm.get_screenshots_path()
        self.assertIsNone(result)
    
    def test_get_logs_path_no_wow_path(self):
        """Test get_logs_path with no WoW path."""
        pm = PathManager()
        result = pm.get_logs_path()
        self.assertIsNone(result)


class TestValidateInstallation(unittest.TestCase):
    """Tests for validate_installation method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pm = PathManager()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_validate_installation_invalid_path(self):
        """Test validate_installation with invalid path."""
        is_valid, flavors = self.pm.validate_installation('')
        self.assertFalse(is_valid)
        self.assertEqual(len(flavors), 0)
    
    def test_validate_installation_no_flavors(self):
        """Test validate_installation with no flavors."""
        is_valid, flavors = self.pm.validate_installation(self.temp_dir)
        self.assertFalse(is_valid)
        self.assertEqual(len(flavors), 0)
    
    def test_validate_installation_with_flavors(self):
        """Test validate_installation with valid flavors."""
        # Create retail flavor
        retail_path = os.path.join(self.temp_dir, '_retail_')
        wtf_path = os.path.join(retail_path, 'WTF')
        account_path = os.path.join(wtf_path, 'Account')
        os.makedirs(account_path)
        
        # Create populated account
        test_account = os.path.join(account_path, 'TESTACCOUNT')
        os.makedirs(test_account)
        
        is_valid, flavors = self.pm.validate_installation(self.temp_dir)
        self.assertTrue(is_valid)
        self.assertEqual(len(flavors), 1)
        self.assertEqual(flavors[0][0], '_retail_')


class TestHasPopulatedDirectory(unittest.TestCase):
    """Tests for _has_populated_directory helper method."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pm = PathManager()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_empty_directory(self):
        """Test empty directory returns False."""
        result = self.pm._has_populated_directory(self.temp_dir)
        self.assertFalse(result)
    
    def test_populated_directory(self):
        """Test populated directory returns True."""
        # Create a file
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        result = self.pm._has_populated_directory(self.temp_dir)
        self.assertTrue(result)
    
    def test_nonexistent_directory(self):
        """Test nonexistent directory returns False."""
        result = self.pm._has_populated_directory('C:\\NonexistentDirectory')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
