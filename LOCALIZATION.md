# Localization Guide

The WoW Cleanup Tool supports localization in all 11 languages available in World of Warcraft.

## Supported Languages

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
- ✅ Settings restoration and language change dialogs
- ✅ Error messages and warnings (send2trash, invalid folders, etc.)
- ✅ AddOns.txt rebuild summaries
- ✅ Log export messages

### Fully Translated (7 languages)

All core languages are now 100% complete with comprehensive translations:

- **English (enUS)** - 100% complete (~253 keys)
- **German (deDE)** - 100% complete (~253 keys)
- **French (frFR)** - 100% complete (~253 keys)
- **Spanish - Spain (esES)** - 100% complete (~253 keys)
- **Spanish - Mexico (esMX)** - 100% complete (~253 keys)
- **Portuguese - Brazil (ptBR)** - 100% complete (~253 keys)
- **Korean (koKR)** - 100% complete (~253 keys)

### Using English Fallback (4 languages)

The following languages are configured to automatically use English translations until native translations are provided:

- **Italian (itIT)** - 0% (uses English)
- **Russian (ruRU)** - 0% (uses English)
- **Chinese - Simplified (zhCN)** - 0% (uses English)
- **Chinese - Traditional (zhTW)** - 0% (uses English)

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
- All 211 translation keys completed

### Chinese

- **zhCN** - Simplified Chinese (used in mainland China)
- **zhTW** - Traditional Chinese (used in Taiwan, Hong Kong, Macau)

### Spanish

- **esES** - European Spanish
- **esMX** - Latin American Spanish (primarily Mexican variant)

## Known Limitations

- Language change triggers a confirmation dialog and automatically restarts the application
- Font rendering quality may vary by language (especially CJK languages)
- Languages using English fallback will show 100% English text until translated

## Future Improvements

- [ ] Complete native translations for remaining 4 languages (itIT, ruRU, zhCN, zhTW)
- [ ] Add right-to-left (RTL) support if needed for potential future languages
- [ ] Improve dynamic UI resizing for different text lengths across languages
- [ ] Add translation validation tools to ensure consistency
- [ ] Create translation memory for maintaining consistency across updates
- [ ] Consider community translation contributions via Crowdin or similar platform
- [ ] Add context-aware tooltips for translators
- [ ] Implement automated translation completeness checks
