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

### Fully Translated

- **English (enUS)** - 100% complete
- **German (deDE)** - Main UI elements translated

### Partially Translated

- **French (frFR)** - Basic UI elements
- **Spanish (esES)** - Basic UI elements

### Pending Translation

The following languages currently fallback to English and need translations:

- Spanish - Mexico (esMX)
- Portuguese (ptBR)
- Italian (itIT)
- Russian (ruRU)
- Korean (koKR)
- Chinese - Simplified (zhCN)
- Chinese - Traditional (zhTW)

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

### Chinese

- **zhCN** - Simplified Chinese (used in mainland China)
- **zhTW** - Traditional Chinese (used in Taiwan, Hong Kong, Macau)

### Spanish

- **esES** - European Spanish
- **esMX** - Latin American Spanish (primarily Mexican variant)

## Known Limitations

- Language change requires application restart for full effect
- Some dynamically generated messages may not be localized
- Font rendering quality may vary by language (especially CJK languages)

## Future Improvements

- [ ] Complete translations for all 11 languages
- [ ] Add right-to-left (RTL) support if needed
- [ ] Improve dynamic UI resizing for different text lengths
- [ ] Add translation validation tools
- [ ] Create translation memory for consistency
