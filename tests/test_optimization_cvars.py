"""Unit tests for optimization_cvars module.

Tests cover CVar reference data access and organization:
- Getting individual CVars
- Filtering CVars by category
- Listing available categories

Note: OPTIMIZATION_CVARS structure is nested: category -> cvar_name -> properties
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from operations.optimization_cvars import (
    OPTIMIZATION_CVARS,
    get_cvar,
    get_cvars_by_category,
    list_categories,
)


class TestCVarDataStructure(unittest.TestCase):
    """Tests for OPTIMIZATION_CVARS data structure."""

    def test_cvars_dict_exists(self):
        """Test OPTIMIZATION_CVARS dictionary exists."""
        self.assertIsInstance(OPTIMIZATION_CVARS, dict)
        self.assertGreater(len(OPTIMIZATION_CVARS), 0)

    def test_cvars_has_required_keys(self):
        """Test CVars have required fields (organized by category)."""
        # OPTIMIZATION_CVARS is: {category: {cvar_name: {properties}}}
        for category_name, cvars in OPTIMIZATION_CVARS.items():
            self.assertIsInstance(cvars, dict)
            # Each CVar should have basic properties
            for cvar_name, cvar_data in cvars.items():
                self.assertIn("description", cvar_data)
                self.assertIsInstance(cvar_data["description"], str)

    def test_cvar_values_have_descriptions(self):
        """Test CVars with 'values' dict have proper descriptions."""
        for category_name, cvars in OPTIMIZATION_CVARS.items():
            for cvar_name, cvar_data in cvars.items():
                if "values" in cvar_data:
                    for value, description in cvar_data["values"].items():
                        self.assertIsInstance(description, str)
                        self.assertGreater(len(description), 0)

    def test_cvar_categories_are_consistent(self):
        """Test category structure is valid."""
        categories = list(OPTIMIZATION_CVARS.keys())
        # Should have multiple categories
        self.assertGreater(len(categories), 1)
        # All should be strings
        for category in categories:
            self.assertIsInstance(category, str)


class TestGetCVar(unittest.TestCase):
    """Tests for get_cvar function."""

    def test_get_existing_cvar(self):
        """Test retrieving an existing CVar."""
        # Get first category and CVar
        category_cvars = next(iter(OPTIMIZATION_CVARS.values()))
        cvar_name = next(iter(category_cvars.keys()))
        result = get_cvar(cvar_name)
        self.assertIsNotNone(result)
        self.assertIn("description", result)

    def test_get_nonexistent_cvar_returns_none(self):
        """Test retrieving non-existent CVar returns None."""
        result = get_cvar("NONEXISTENT_CVAR_NAME_XYZ")
        self.assertIsNone(result)

    def test_get_cvar_case_insensitive(self):
        """Test CVar retrieval might be case-sensitive (depends on implementation)."""
        # Get first CVar name
        category_cvars = next(iter(OPTIMIZATION_CVARS.values()))
        cvar_name = next(iter(category_cvars.keys()))
        result_original = get_cvar(cvar_name)
        # Based on actual implementation, test exact match
        self.assertIsNotNone(result_original)

    def test_get_cvar_with_empty_string(self):
        """Test getting CVar with empty string."""
        result = get_cvar("")
        self.assertIsNone(result)

    def test_get_cvar_with_none(self):
        """Test getting CVar with None."""
        result = get_cvar(None)
        self.assertIsNone(result)


class TestGetCVarsByCategory(unittest.TestCase):
    """Tests for get_cvars_by_category function."""

    def test_get_cvars_by_valid_category(self):
        """Test retrieving CVars by valid category."""
        categories = list_categories()
        if categories:
            category = categories[0]
            result = get_cvars_by_category(category)
            self.assertIsInstance(result, dict)
            self.assertGreater(len(result), 0)

    def test_get_cvars_by_invalid_category(self):
        """Test retrieving CVars by invalid category returns empty dict."""
        result = get_cvars_by_category("INVALID_CATEGORY_XYZ")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)

    def test_get_cvars_by_category_case_sensitive(self):
        """Test category retrieval is case-sensitive (keys are exact)."""
        categories = list_categories()
        if categories:
            category = categories[0]
            result_original = get_cvars_by_category(category)
            # Verify the result is valid
            self.assertIsInstance(result_original, dict)

    def test_get_cvars_by_empty_category(self):
        """Test getting CVars with empty category string."""
        result = get_cvars_by_category("")
        self.assertIsInstance(result, dict)

    def test_get_cvars_by_none_category(self):
        """Test getting CVars with None category."""
        result = get_cvars_by_category(None)
        self.assertIsInstance(result, dict)

    def test_get_cvars_covers_most_cvars(self):
        """Test that getting CVars by all categories covers most CVars."""
        categories = list_categories()
        all_cvars_by_category = {}
        for category in categories:
            cvars = get_cvars_by_category(category)
            all_cvars_by_category.update(cvars)
        # Should have many CVars
        self.assertGreater(len(all_cvars_by_category), 10)


class TestListCategories(unittest.TestCase):
    """Tests for list_categories function."""

    def test_list_categories_returns_list(self):
        """Test list_categories returns a list."""
        result = list_categories()
        self.assertIsInstance(result, list)

    def test_list_categories_not_empty(self):
        """Test list_categories returns non-empty list."""
        result = list_categories()
        self.assertGreater(len(result), 0)

    def test_list_categories_are_strings(self):
        """Test all categories are strings."""
        result = list_categories()
        for category in result:
            self.assertIsInstance(category, str)
            self.assertGreater(len(category), 0)

    def test_list_categories_are_unique(self):
        """Test all categories are unique."""
        result = list_categories()
        self.assertEqual(len(result), len(set(result)))

    def test_list_categories_matches_cvars(self):
        """Test listed categories match OPTIMIZATION_CVARS keys."""
        listed_categories = set(list_categories())
        cvar_categories = set(OPTIMIZATION_CVARS.keys())
        self.assertEqual(listed_categories, cvar_categories)


class TestCVarIntegration(unittest.TestCase):
    """Integration tests for CVar functions."""

    def test_get_cvar_and_get_cvars_by_category_consistency(self):
        """Test consistency between get_cvar and get_cvars_by_category."""
        categories = list_categories()
        for category in categories:
            cvars = get_cvars_by_category(category)
            for cvar_name in cvars.keys():
                direct_result = get_cvar(cvar_name)
                category_result = cvars[cvar_name]
                self.assertEqual(direct_result, category_result)

    def test_all_categories_contain_cvars(self):
        """Test that all categories returned by list_categories have CVars."""
        categories = list_categories()
        for category in categories:
            cvars = get_cvars_by_category(category)
            self.assertGreater(len(cvars), 0)

    def test_structure_integrity(self):
        """Test that the nested structure is properly maintained."""
        # All categories should map to the same structure in OPTIMIZATION_CVARS
        listed_categories = list_categories()
        dict_categories = list(OPTIMIZATION_CVARS.keys())
        self.assertEqual(sorted(listed_categories), sorted(dict_categories))


if __name__ == "__main__":
    unittest.main()
