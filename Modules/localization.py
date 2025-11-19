"""
Localization module for WoW Cleanup Tool.

Supports the 11 languages available in World of Warcraft plus Ukrainian:
- English (enUS)
- German (deDE)
- French (frFR)
- Spanish - Spain (esES)
- Spanish - Mexico (esMX)
- Portuguese (ptBR)
- Italian (itIT)
- Russian (ruRU)
- Korean (koKR)
- Chinese - Simplified (zhCN)
- Chinese - Traditional (zhTW)
- Ukrainian (ukUA) - Bonus language
"""

import importlib
import os

DEFAULT_LANGUAGE = "enUS"
LOCALES_DIR = os.path.join(os.path.dirname(__file__), "..", "Locales")

AVAILABLE_LANGUAGES = {
    "enUS": "English",
    "deDE": "Deutsch",
    "frFR": "Français",
    "esES": "Español (EU)",
    "esMX": "Español (MX)",
    "ptBR": "Português",
    "itIT": "Italiano",
    "ruRU": "Русский",
    "koKR": "한국어",
    "zhCN": "简体中文",
    "zhTW": "繁體中文",
    "ukUA": "Українська"
}

def load_translations(lang_code):
    try:
        module = importlib.import_module(f"Locales.{lang_code}")
        return getattr(module, "TRANSLATIONS", {})
    except Exception:
        # Fallback to English if import fails
        module = importlib.import_module("Locales.enUS")
        return getattr(module, "TRANSLATIONS", {})

class Localization:
    def __init__(self, lang_code=DEFAULT_LANGUAGE):
        self.translations = load_translations(lang_code)
        self.fallback = load_translations(DEFAULT_LANGUAGE)

    def _(self, key, *args):
        text = self.translations.get(key, self.fallback.get(key, key))
        return text.format(*args) if args else text

def get_translation_completeness(lang_code):
    """Get the percentage of translations completed for a language.
    
    Args:
        lang_code: Language code (e.g., 'enUS', 'deDE')
        
    Returns:
        int: Percentage complete (0-100)
    """
    # Load reference and target translations using loader
    english = load_translations("enUS")
    target = load_translations(lang_code)
    english_keys = set(english.keys())
    lang_keys = set(target.keys())
    if not english_keys:
        return 0
    translated_count = len(lang_keys.intersection(english_keys))
    total_count = len(english_keys)
    return int((translated_count / total_count) * 100)

def get_language_display_name(lang_code):
    """Get display name for a language with completeness indicator.
    
    Args:
        lang_code: Language code (e.g., 'enUS', 'deDE')
        
    Returns:
        str: Display name with optional completeness indicator
    """
    base_name = AVAILABLE_LANGUAGES.get(lang_code, lang_code)
    if lang_code == "enUS":
        return base_name  # English is always 100%
    completeness = get_translation_completeness(lang_code)
    if completeness < 100:
        return f"{base_name} ({completeness}%)"
    else:
        return base_name

