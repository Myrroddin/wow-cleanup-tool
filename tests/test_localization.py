"""Unit tests for localization module."""
import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.localization import (
    load_translations, 
    Localization, 
    get_translation_completeness,
    get_language_display_name,
    DEFAULT_LANGUAGE,
    AVAILABLE_LANGUAGES
)


class TestLoadTranslations(unittest.TestCase):
    """Tests for load_translations function."""
    
    def test_load_default_language(self):
        """Test loading the default language (en_us)."""
        translations = load_translations(DEFAULT_LANGUAGE)
        self.assertIsInstance(translations, dict)
        self.assertGreater(len(translations), 0)
        # Check for some expected keys
        self.assertIn('title_main_window', translations)
        self.assertIn('tab_file_cleaner', translations)
    
    def test_load_invalid_language(self):
        """Test loading an invalid language code falls back to English."""
        translations = load_translations('invalid_lang')
        self.assertIsInstance(translations, dict)
        # Invalid language falls back to English, not empty
        self.assertGreater(len(translations), 0)
    
    def test_all_available_languages_exist(self):
        """Test that all languages in AVAILABLE_LANGUAGES can be loaded."""
        for lang_code in AVAILABLE_LANGUAGES.keys():
            # Note: Most languages don't have translation files yet,
            # so they'll return empty dicts - this is expected behavior
            translations = load_translations(lang_code)
            self.assertIsInstance(translations, dict)


class TestLocalizationClass(unittest.TestCase):
    """Tests for Localization class."""
    
    def test_initialization_default_language(self):
        """Test Localization initializes with default language."""
        loc = Localization()
        self.assertIsNotNone(loc.translations)
        self.assertIsNotNone(loc.fallback)
        # Fallback should be English
        self.assertGreater(len(loc.fallback), 0)
    
    def test_initialization_custom_language(self):
        """Test Localization initializes with custom language."""
        loc = Localization('de')
        self.assertIsNotNone(loc.translations)
        self.assertIsNotNone(loc.fallback)
    
    def test_translation_key_exists(self):
        """Test retrieving translation for existing key."""
        loc = Localization()
        result = loc._('title_main_window')
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, 'title_main_window')  # Should return actual translation
    
    def test_translation_key_missing(self):
        """Test retrieving translation for missing key falls back."""
        loc = Localization()
        result = loc._('nonexistent_key')
        self.assertEqual(result, 'nonexistent_key')  # Should return key itself
    
    def test_translation_with_formatting(self):
        """Test translation with format arguments."""
        loc = Localization()
        # Assuming msg_cache_cleared exists and has format placeholders
        result = loc._('msg_cache_cleared', 'Test Value')
        self.assertIsInstance(result, str)


class TestTranslationHelpers(unittest.TestCase):
    """Tests for helper functions."""
    
    def test_get_translation_completeness_default(self):
        """Test completeness calculation for default language."""
        completeness = get_translation_completeness(DEFAULT_LANGUAGE)
        self.assertEqual(completeness, 100)  # Default language is always 100%
    
    def test_get_translation_completeness_invalid(self):
        """Test completeness for invalid language falls back to 100%."""
        completeness = get_translation_completeness('invalid')
        # Invalid language falls back to English, which is 100%
        self.assertEqual(completeness, 100)
    
    def test_get_language_display_name_valid(self):
        """Test getting display name for valid language."""
        name = get_language_display_name('en_us')
        self.assertEqual(name, 'English')
    
    def test_get_language_display_name_invalid(self):
        """Test getting display name for invalid language."""
        name = get_language_display_name('invalid')
        self.assertEqual(name, 'invalid')  # Returns the code itself


class TestLocalizationConstants(unittest.TestCase):
    """Tests for module constants."""
    
    def test_default_language_is_english(self):
        """Test DEFAULT_LANGUAGE is set to English."""
        self.assertEqual(DEFAULT_LANGUAGE, 'en_us')
    
    def test_available_languages_structure(self):
        """Test AVAILABLE_LANGUAGES has correct structure."""
        self.assertIsInstance(AVAILABLE_LANGUAGES, dict)
        self.assertGreater(len(AVAILABLE_LANGUAGES), 0)
        # Check that English is available (use en_us, not en)
        self.assertIn('en_us', AVAILABLE_LANGUAGES)
    
    def test_available_languages_has_display_names(self):
        """Test all languages have display names."""
        for lang_code, display_name in AVAILABLE_LANGUAGES.items():
            self.assertIsInstance(lang_code, str)
            self.assertIsInstance(display_name, str)
            self.assertGreater(len(display_name), 0)


if __name__ == '__main__':
    unittest.main()
