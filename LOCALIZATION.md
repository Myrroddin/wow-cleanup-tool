# Localization Guide

The WoW Cleanup Tool supports localization in all 11 languages available in World of Warcraft, plus Ukrainian as a bonus language.

## Table of Contents

- [Supported Languages](#supported-languages)
  - [Official WoW Languages](#official-wow-languages)
  - [Bonus Languages](#bonus-languages)
- [Language Detection](#language-detection)
- [Adding or Updating Translations](#adding-or-updating-translations)
  - [File Location](#file-location)
  - [Translation Structure](#translation-structure)
  - [Using Translations in Code](#using-translations-in-code)
  - [Adding New Translation Keys](#adding-new-translation-keys)
  - [Translation Key Guidelines](#translation-key-guidelines)
- [Current Translation Status](#current-translation-status)
  - [Recent Updates (November 2025)](#recent-updates-november-2025)
  - [Fully Translated (12 languages)](#fully-translated-7-languages)
- [Contributing Translations](#contributing-translations)
  - [Translation Guidelines](#translation-guidelines)
- [Testing Translations](#testing-translations)
- [Language-Specific Notes](#language-specific-notes)
  - [German (deDE)](#german-dede)
  - [French (frFR)](#french-frfr)
  - [Spanish (esES)](#spanish-eses)
  - [Spanish - Mexico (esMX)](#spanish---mexico-esmx)
  - [Portuguese (ptBR)](#portuguese-ptbr)
  - [Korean (koKR)](#korean-kokr)
  - [Italian (itIT)](#italian-itit)
  - [Russian (ruRU)](#russian-ruru)
  - [Ukrainian (ukUA)](#ukrainian-ukua---bonus-language)
  - [Chinese - Simplified (zhCN)](#chinese---simplified-zhcn)
  - [Chinese - Traditional (zhTW)](#chinese---traditional-zhtw)
  - [Spanish](#spanish)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)

## Supported Languages

### Official WoW Languages

- **enUS** - English (Default)
- **deDE** - German (Deutsch)
- **frFR** - French (Français)
- **esES** - Spanish - Spain (Español EU)
- **esMX** - Spanish - Mexico (Español MX)
- **ptBR** - Portuguese (Português)
- **itIT** - Italian (Italiano)
- **ruRU** - Russian (Русский)
- **koKR** - Korean (한국어)
- **zhCN** - Chinese - Simplified (简体中文)
- **zhTW** - Chinese - Traditional (繁體中文)

### Bonus Languages

- **ukUA** - Ukrainian (Українська) - Community requested addition

## Language Detection

The application automatically detects your system language on first launch and sets the interface language accordingly. You can manually change the language using the Language dropdown in the Options section.

## Adding or Updating Translations

### File Location

All translations are stored in: `Modules/localization.py`

### Translation Structure

Translations are organized in the `TRANSLATIONS` dictionary with the following structure:

```python
TRANSLATIONS = {
    "enUS": {
        "key": "English text",
        # ...
    },
    "deDE": {
        "key": "German text",
        # ...
    },
    # ... other languages
}
```

### Using Translations in Code

To use a localized string in the application code:

```python
from Modules import localization

# Get translated text
text = localization._("key")

# Get translated text with formatting
text = localization._("key", arg1, arg2)
```

### Adding New Translation Keys

1. Add the key to all language dictionaries in `TRANSLATIONS`
2. Start with the English (`enUS`) translation
3. Add translations for other languages
4. If a translation is not available, it will fallback to English

### Translation Key Guidelines

- Use lowercase with underscores: `window_title`, `file_cleaner`
- Keep keys descriptive and consistent
- Group related keys together
- Use placeholders (`{}`) for dynamic content

## Current Translation Status

### Recent Updates (November 2025)

The localization system has been significantly expanded with comprehensive translations across all major user-facing components:

- ✅ All message boxes and dialog boxes fully localized
- ✅ Main UI buttons and labels (Apply, Cancel, Export Log, Clear Log, etc.)
- ✅ File/Folder/Orphan Cleaner complete with status messages
- ✅ Game Optimizer dialogs and confirmation messages
- ✅ Optimization Suggestions tab with 6 manual optimization tips (including Reinstall WoW)
- ✅ Settings restoration and language change dialogs
- ✅ Error messages and warnings (send2trash, invalid folders, etc.)
- ✅ AddOns.txt rebuild summaries
- ✅ Log export messages

### Fully Translated (12 languages)

All core languages are now 100% complete with comprehensive translations:

- **English (enUS)** - 100% complete (~262 keys)
- **German (deDE)** - 100% complete (~262 keys)
- **French (frFR)** - 100% complete (~262 keys)
- **Spanish - Spain (esES)** - 100% complete (~262 keys)
- **Spanish - Mexico (esMX)** - 100% complete (~262 keys)
- **Portuguese - Brazil (ptBR)** - 100% complete (~262 keys)
- **Korean (koKR)** - 100% complete (~262 keys)
- **Chinese - Simplified (zhCN)** - 100% complete (~262 keys)
- **Chinese - Traditional (zhTW)** - 100% complete (~262 keys)
- **Italian (itIT)** - 100% complete (~262 keys)
- **Russian (ruRU)** - 100% complete (~262 keys)
- **Ukrainian (ukUA)** - 100% complete (~262 keys) - Bonus language

**All 12 languages are now fully translated!** 🎉

**Recent additions:**
- `opt_sug_reinstall_title` - "Reinstall WoW (Clean Install)" title
- `opt_sug_reinstall_text` - Brief explanation of the clean reinstall process
- `opt_sug_reinstall_tooltip` - Detailed why/risk/benefit/how-to guide for clean reinstalls

## Contributing Translations

We welcome contributions for missing translations! To contribute:

1. Fork the repository
2. Edit `Modules/localization.py`
3. Add or update translations for your language
4. Test the translations in the application
5. Submit a pull request

### Translation Guidelines

- Keep the same meaning as the English original
- Use terminology consistent with World of Warcraft in your language
- Consider UI space constraints (keep translations reasonably short)
- Use native language names for language selection (already implemented)
- Preserve formatting placeholders (`{}`) and special characters (`\n`)

## Testing Translations

1. Open the application
2. Go to Options → Language
3. Select your language from the dropdown
4. Restart the application to see all changes
5. Verify all UI elements display correctly

## Language-Specific Notes

### German (deDE)

- Uses formal "Sie" form for addressing the user
- Follows German capitalization rules for nouns
- All translation keys completed
- Technical terms properly localized (e.g., "Papierkorb" for Recycle Bin)

### French (frFR)

- Uses formal "vous" form for addressing the user
- Follows French spacing rules for punctuation
- All translation keys completed
- Proper use of accents and diacritics throughout

### Spanish (esES)

- Uses formal "usted" form (implied) for addressing the user
- European Spanish terminology and spelling
- All translation keys completed

### Spanish - Mexico (esMX)

- Uses Latin American Spanish terminology
- Adapted for Mexican and Latin American audiences
- All translation keys completed
- Capitalizes UI elements appropriately (e.g., "Vista Previa", "Aplicar")

### Portuguese (ptBR)

- Brazilian Portuguese variant
- Uses Brazilian spelling and terminology
- All translation keys completed
- Formal "você" addressing throughout

### Korean (koKR)

- Uses polite/formal speech level (존댓말)
- Follows Korean grammar and word order
- All translation keys completed

### Italian (itIT)

- Uses formal "Lei" addressing
- Follows Italian capitalization and punctuation rules
- All translation keys completed
- Technical terms properly localized (e.g., "Cestino" for Recycle Bin)
- UI terminology consistent with Windows/macOS Italian localizations

### Russian (ruRU)

- Uses formal "вы" (vy) addressing
- Follows Russian grammar and case system
- All translation keys completed
- Cyrillic script throughout
- Technical terms properly localized (e.g., "Корзина" for Recycle Bin)
- UI terminology consistent with Russian Windows/macOS localizations

### Ukrainian (ukUA) - Bonus Language

- Uses formal "ви" (vy) addressing
- Follows Ukrainian grammar and case system
- All translation keys completed
- Cyrillic script throughout (Ukrainian alphabet)
- Technical terms properly localized (e.g., "Кошик" for Recycle Bin)
- UI terminology consistent with Ukrainian Windows/macOS localizations
- Added as community-requested bonus language beyond WoW's official 11 languages

### Chinese - Simplified (zhCN)

- Used in mainland China
- Uses Simplified Chinese characters (简体中文)
- All translation keys completed
- Uses "魔兽世界" for World of Warcraft
- Follows mainland China terminology and conventions

### Chinese - Traditional (zhTW)

- Used in Taiwan, Hong Kong, and Macau
- Uses Traditional Chinese characters (繁體中文)
- All translation keys completed
- Uses "魔獸世界" for World of Warcraft
- Follows Taiwan/Hong Kong terminology and conventions

### Spanish

- **esES** - European Spanish
- **esMX** - Latin American Spanish (primarily Mexican variant)

## Known Limitations

- Language change triggers a confirmation dialog and automatically restarts the application
- Font rendering quality may vary by language (especially CJK and Cyrillic languages)
- Some translations may need refinement based on community feedback

## Future Improvements

- [ ] Add right-to-left (RTL) support if needed for potential future languages (Arabic, Hebrew)
- [ ] Improve dynamic UI resizing for different text lengths across languages
- [ ] Add translation validation tools to ensure consistency
- [ ] Create translation memory for maintaining consistency across updates
- [ ] Consider community translation contributions via Crowdin or similar platform
- [ ] Add context-aware tooltips for translators
- [ ] Implement automated translation completeness checks
