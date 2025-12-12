"""
Localization module for WoW Cleanup Tool.

Supports 12 languages matching World of Warcraft locales plus Ukrainian:
- English (en_us) - enUS
- German (de_de) - deDE
- French (fr_fr) - frFR
- Spanish - Spain (es_es) - esES
- Spanish - Mexico (es_mx) - esMX
- Portuguese - Brazil (pt_br) - ptBR
- Italian (it_it) - itIT
- Russian (ru_ru) - ruRU
- Korean (ko_kr) - koKR
- Chinese - Simplified (zh_cn) - zhCN
- Chinese - Traditional (zh_tw) - zhTW
- Ukrainian (uk_ua) - ukUA

Usage:
    from localization import Localization

    loc = Localization("de_de")
    translated_text = loc._("title_main_window")  # Window titles use title_ prefix
    button_text = loc._("btn_browse")              # Buttons use btn_ prefix
    label_text = loc._("label_font_size")          # UI labels use label_ prefix

Key Naming Conventions:
    - btn_*: Button labels
    - label_*: UI field labels
    - status_*: Status messages
    - msg_*: Dialog messages
    - title_*: Window/dialog titles
    - tab_*: Tab names
    - option_*: Checkbox/radio options
    - version_*: Version types
    - dep_*: Dependency-related
    - error_*: Error messages
    - file_*: File dialog filters
    - log_*: Log-related actions
    - wow_*: WoW-specific messages
"""

import importlib
from typing import Dict, Optional

DEFAULT_LANGUAGE: str = "en_us"

AVAILABLE_LANGUAGES: Dict[str, str] = {
    "en_us": "English",
    "de_de": "Deutsch",
    "fr_fr": "Français",
    "es_es": "Español (EU)",
    "es_mx": "Español (MX)",
    "pt_br": "Português",
    "it_it": "Italiano",
    "ru_ru": "Русский",
    "ko_kr": "한국어",
    "zh_cn": "简体中文",
    "zh_tw": "繁體中文",
    "uk_ua": "Українська",
}


def load_translations(lang_code: str) -> Dict[str, str]:
    """Load translation dictionary for a given language code.

    Args:
        lang_code: Language code (e.g., 'en_us', 'de_de')

    Returns:
        dict: Translation dictionary
    """
    try:
        module = importlib.import_module(f"localization.{lang_code}")
        return getattr(module, "TRANSLATIONS", {})
    except Exception:
        # Fallback to English if import fails
        module = importlib.import_module("localization.en_us")
        return getattr(module, "TRANSLATIONS", {})


class Localization:
    """Localization handler for multi-language support."""

    def __init__(self, lang_code: str = DEFAULT_LANGUAGE) -> None:
        """Initialize localization with a specific language.

        Args:
            lang_code: Language code (default: en_us)
        """
        self.translations: Dict[str, str] = load_translations(lang_code)
        self.fallback: Dict[str, str] = load_translations(DEFAULT_LANGUAGE)

    def _(self, key: str, *args: any) -> str:
        """Get translated text for a key.

        Args:
            key: Translation key
            *args: Optional format arguments

        Returns:
            str: Translated text
        """
        text = self.translations.get(key, self.fallback.get(key, key))
        return text.format(*args) if args else text


def get_translation_completeness(lang_code: str) -> int:
    """Get the percentage of translations completed for a language.

    Args:
        lang_code: Language code (e.g., 'en_us', 'de_de')

    Returns:
        int: Percentage complete (0-100)
    """
    english = load_translations("en_us")
    target = load_translations(lang_code)
    english_keys = set(english.keys())
    lang_keys = set(target.keys())
    if not english_keys:
        return 0
    translated_count = len(lang_keys.intersection(english_keys))
    total_count = len(english_keys)
    return int((translated_count / total_count) * 100)


def get_language_display_name(lang_code: str) -> str:
    """Get display name for a language with completeness indicator.

    Args:
        lang_code: Language code (e.g., 'en_us', 'de_de')

    Returns:
        str: Display name with optional completeness indicator
    """
    base_name = AVAILABLE_LANGUAGES.get(lang_code, lang_code)
    if lang_code == "en_us":
        return base_name  # English is always 100%
    completeness = get_translation_completeness(lang_code)
    if completeness < 100:
        return f"{base_name} ({completeness}%)"
    else:
        return base_name


# Create a default global localization instance for module-level usage
_default_loc: Localization = Localization(DEFAULT_LANGUAGE)


def _(key: str, *args: any) -> str:
    """Global translation function using default localization instance.

    This is a convenience function for modules that don't have access to
    the app's localization instance.

    Args:
        key: Translation key
        *args: Optional format arguments

    Returns:
        str: Translated text
    """
    return _default_loc._(key, *args)
