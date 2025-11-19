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
- [Contributing Translations](#contributing-translations)
  - [Translation Guidelines](#translation-guidelines)
- [Testing Translations](#testing-translations)
- [Language-Specific Notes](#language-specific-notes)
  - [Chinese - Simplified (zhCN)](#chinese---simplified-zhcn)
  - [Chinese - Traditional (zhTW)](#chinese---traditional-zhtw)
  - [French (frFR)](#french-frfr)
  - [German (deDE)](#german-dede)
  - [Italian (itIT)](#italian-itit)
  - [Korean (koKR)](#korean-kokr)
  - [Portuguese (ptBR)](#portuguese-ptbr)
  - [Russian (ruRU)](#russian-ruru)
  - [Spanish - Mexico (esMX)](#spanish---mexico-esmx)
  - [Spanish (esES)](#spanish-eses)
  - [Ukrainian (ukUA)](#ukrainian-ukua---bonus-language)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)

## Supported Languages

### Official WoW Languages

- **enUS** - English (Default)
- **deDE** - German (Deutsch)
- **esES** - Spanish - Spain (Español EU)
- **esMX** - Spanish - Mexico (Español MX)
- **frFR** - French (Français)
- **itIT** - Italian (Italiano)
- **koKR** - Korean (한국어)
- **ptBR** - Portuguese (Português)
- **ruRU** - Russian (Русский)
- **zhCN** - Chinese - Simplified (简体中文)
- **zhTW** - Chinese - Traditional (繁體中文)

### Bonus Languages

- **ukUA** - Ukrainian (Українська) - Community requested addition

## Language Detection
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

### French (frFR)

- Uses formal "vous" form for addressing the user
- Follows French spacing rules for punctuation
- All translation keys completed
- Proper use of accents and diacritics throughout

### German (deDE)

- Uses formal "Sie" form for addressing the user
- Follows German capitalization rules for nouns
- All translation keys completed
- Technical terms properly localized (e.g., "Papierkorb" for Recycle Bin)

### Italian (itIT)

- Uses formal "Lei" addressing
- Follows Italian capitalization and punctuation rules
- All translation keys completed
- Technical terms properly localized (e.g., "Cestino" for Recycle Bin)
- UI terminology consistent with Windows/macOS Italian localizations

### Korean (koKR)

- Uses polite/formal speech level (존댓말)
- Follows Korean grammar and word order
- All translation keys completed

### Portuguese (ptBR)

- Brazilian Portuguese variant
- Uses Brazilian spelling and terminology
- All translation keys completed
- Formal "você" addressing throughout

### Russian (ruRU)

- Uses formal "вы" (vy) addressing
- Follows Russian grammar and case system
- All translation keys completed
- Cyrillic script throughout
- Technical terms properly localized (e.g., "Корзина" for Recycle Bin)
- UI terminology consistent with Russian Windows/macOS localizations

### Spanish - Mexico (esMX)

- Uses Latin American Spanish terminology
- Adapted for Mexican and Latin American audiences
- All translation keys completed
- Capitalizes UI elements appropriately (e.g., "Vista Previa", "Aplicar")

### Spanish (esES)

- Uses formal "usted" form (implied) for addressing the user
- European Spanish terminology and spelling
- All translation keys completed

### Ukrainian (ukUA) - Bonus Language

- Uses formal "ви" (vy) addressing
- Follows Ukrainian grammar and case system
- All translation keys completed
- Cyrillic script throughout (Ukrainian alphabet)
- Technical terms properly localized (e.g., "Кошик" for Recycle Bin)
- UI terminology consistent with Ukrainian Windows/macOS localizations
- Added as community-requested bonus language beyond WoW's official 11 languages
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

## New in v1.0.0

- All log messages, including verbose output, are now fully localized. See new keys for verbose logging in `Locales/enUS.py` and other locale files (e.g., `verbose_updated_settings`, `verbose_added_settings`).
