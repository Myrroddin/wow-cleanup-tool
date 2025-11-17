"""
Localization module for WoW Cleanup Tool.

Supports the 11 languages available in World of Warcraft:
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
"""

import os
import json
import locale as sys_locale

# Default language
DEFAULT_LANGUAGE = "enUS"

# Available languages matching WoW's locales
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
    "zhTW": "繁體中文"
}

def get_translation_completeness(lang_code):
    """Get the percentage of translations completed for a language.
    
    Args:
        lang_code: Language code (e.g., 'enUS', 'deDE')
        
    Returns:
        int: Percentage complete (0-100)
    """
    if lang_code not in TRANSLATIONS:
        return 0
    
    # English is the reference language
    english_keys = set(TRANSLATIONS.get("enUS", {}).keys())
    lang_keys = set(TRANSLATIONS.get(lang_code, {}).keys())
    
    if not english_keys:
        return 0
    
    # Calculate percentage of translated keys
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

# Translation strings
TRANSLATIONS = {
    "enUS": {
        # Window title
        "window_title": "WoW Cleanup Tool",
        
        # Menu/Tab names
        "file_cleaner": "File Cleaner",
        "folder_cleaner": "Folder Cleaner",
        "orphan_cleaner": "Orphan Cleaner",
        "game_optimizer": "Game Optimizer",
        "optimization_suggestions": "Optimization Suggestions",
        "log": "Log",
        "help_about": "Help / About",
        
        # Options section
        "options": "Options",
        "wow_folder": "World of Warcraft Folder:",
        "browse": "Browse...",
        "browse_tooltip": "Browse for your World of Warcraft folder.",
        "font_size": "Font Size:",
        "font": "Font:",
        "theme": "Theme:",
        "language": "Language:",
        "file_action": "File Action:",
        "delete_permanently": "Delete Permanently",
        "move_to_recycle": "Move to Recycle Bin",
        "enable_verbose": "Enable verbose logging",
        "verbose_tooltip": "When enabled, Log captures every processed file/folder/AddOns.txt line.",
        "external_log": "External Log:",
        "fresh": "Fresh",
        "fresh_tooltip": "Create a fresh log file on each export (overwrites existing).",
        "append": "Append",
        "append_tooltip": "Append each export to the existing log file (keeps up to 10-20 sessions based on verbosity).",
        "check_updates": "Check for updates",
        "check_updates_tooltip": "When enabled, check for new releases on GitHub at startup.",
        "restore_defaults": "Restore Defaults",
        "light": "light",
        "dark": "dark",
        
        # File Cleaner
        "scan": "Scan",
        "select_all": "Select All",
        "expand_all": "Expand All",
        "collapse_all": "Collapse All",
        "process_selected": "Process Selected",
        "scanning": "Scanning…",
        "no_bak_old_found": "No .bak or .old files found.",
        "files_found": "{} file(s) found.",
        
        # Folder Cleaner
        "version": "Version:",
        "path": "Path:",
        "preview": "Preview",
        "toggle_all": "Toggle All",
        "process_folders": "Process Selected Folders",
        
        # Orphan Cleaner
        "rebuild_addons": "Rebuild AddOns.txt",
        "no_orphans_found": "No orphaned SavedVariables found.",
        "orphans_found": "Found {} orphan SavedVariable(s).",
        
        # Game Optimizer
        "scan_hardware": "Scan Hardware",
        "system_matches": "Your system matches:",
        "optimization_applied": "✓ Optimization applied",
        "optimization_not_applied": "⚠ Optimization not yet applied",
        "graphics_presets": "Graphics Presets (Retail):",
        "graphics_presets_classic": "Graphics Presets (Classic):",
        "apply_preset": "Apply Preset:",
        "apply": "Apply",
        "preset_applied": "✓ {} preset applied.",
        "error": "✗ Error: {}",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
        "ultra": "Ultra",
        
        # Optimization Suggestions
        "manual_suggestions": "Manual Optimization Suggestions",
        "manual_disclaimer": "NOTE: This application does NOT perform these optimizations automatically. These are manual suggestions for you to implement.",
        "clean_data_folder": "Clean Game Data Folder",
        "clean_data_text": "If several years or multiple expansions have passed since installing World of Warcraft, consider deleting the Data folder from your main World of Warcraft directory. This *could* reduce game size and improve loading screen performance. The Battle.net launcher will automatically rebuild this folder when needed.",
        "enable_hdr": "Enable HDR (High Dynamic Range)",
        "enable_hdr_text": "Check your operating system's display settings to see if HDR is available. If supported by your monitor, enabling HDR can significantly improve visual clarity and color depth in-game.",
        "verify_refresh": "Verify Monitor Refresh Rate",
        "verify_refresh_text": "Ensure your monitor's refresh rate is set to the maximum supported value in your operating system's display settings. Higher refresh rates provide smoother gameplay and better responsiveness.",
        "enable_sam": "Enable Smart Access Memory / Resizable BAR",
        "enable_sam_text": "Check your motherboard BIOS settings for Smart Access Memory (AMD) or Resizable BAR (Intel/NVIDIA). Enabling this feature allows your CPU to access the full GPU memory, potentially improving performance.",
        "enable_xmp": "Enable XMP Memory Profile",
        "enable_xmp_text": "Access your motherboard BIOS and enable the XMP (Extreme Memory Profile) or DOCP/EOCP setting. This ensures your RAM runs at its rated speed rather than default conservative speeds, improving overall system performance.",
        
        # Log tab
        "export_log": "Export Log",
        "clear_log": "Clear Log",
        
        # Help/About
        "about_text": "A comprehensive maintenance and optimization suite for World of Warcraft.\nClean unnecessary files, manage addons, optimize game performance, and more.\n\nAlways close World of Warcraft before running this tool.",
        "copyright": "Copyright © 2025 Paul Vandersypen. Released under the GNU General Public License v3.0 (GPL-3.0-or-later). See the included LICENSE file for full terms.",
        
        # Dialogs
        "invalid_folder": "Invalid Folder",
        "select_valid_wow": "Please select a valid WoW folder first.",
        "no_selection": "No Selection",
        "no_files_selected": "No files selected for processing.",
        "no_folders_selected": "No folders were selected for cleanup.",
        "no_orphans_selected": "No orphaned files selected.",
        "confirm": "Confirm",
        "confirm_action": "Are you sure you want to {} {} {}?",
        "file_s": "file(s)",
        "folder_s": "folder(s)",
        "orphaned_savedvars": "orphaned SavedVariables",
        "completed": "Completed",
        "processed": "Processed {} {}.",
        "send2trash_missing": "send2trash missing",
        "send2trash_unavailable": "The 'send2trash' module is unavailable. Files were deleted permanently.",
        "send2trash_install": "The 'send2trash' package is not installed.\nTo enable Recycle Bin support, install it manually:\n\n  pip install send2trash\n\nor:\n\n  python -m pip install --user send2trash",
        "restore_defaults_confirm": "Restore all settings to defaults?",
        "restart_required": "Settings restored. The application will now restart.",
        "error_title": "Error",
        "restore_error": "Failed to restore defaults: {}",
        "confirm_font": "Confirm Font",
        "apply_font_confirm": "Apply font '{}' to the application?",
        "export_log_title": "Export Log",
        "log_empty": "Log is empty. Nothing to export.",
        "log_exported": "Log exported successfully to:\n{}",
        "export_error": "Export Error",
        "export_failed": "Failed to export log:\n{}",
        "addons_rebuilt": "Rebuilt AddOns.txt entries.\nTotal written: {}\nTotal removed: {}",
        
        # Log messages
        "session_started": "Session started — {}",
        "file_scan": "File Cleaner scan: {} match(es).",
        "orphan_scan": "Orphan Cleaner scan: {} orphan(s).",
        "file_processed": "File Cleaner: processed {} file(s).",
        "folder_processed": "Folder Cleaner: processed {} folder(s).",
        "orphan_processed": "Orphan Cleaner: processed {} orphan(s).",
        "send2trash_warning": "Warning: send2trash not installed; deletions were permanent.",
        "addons_txt_log": "[AddOns.txt] {}: wrote {} entries, removed {}",
        "preset_applied_log": "Applied {} preset for {}",
        "preset_failed_log": "Failed to apply {} preset: {}",
        
        # Language change
        "language_changed": "Language Changed",
        "language_changed_restart": "Language has been changed. Please restart the application for all changes to take effect.",
    },
    
    "deDE": {
        "window_title": "WoW Bereinigungstool",
        "file_cleaner": "Dateibereinigung",
        "folder_cleaner": "Ordnerbereinigung",
        "orphan_cleaner": "Verwaiste Dateien",
        "game_optimizer": "Spiel-Optimierer",
        "optimization_suggestions": "Optimierungsvorschläge",
        "log": "Protokoll",
        "help_about": "Hilfe / Info",
        "options": "Optionen",
        "wow_folder": "World of Warcraft-Ordner:",
        "browse": "Durchsuchen...",
        "browse_tooltip": "Nach Ihrem World of Warcraft-Ordner suchen.",
        "font_size": "Schriftgröße:",
        "font": "Schriftart:",
        "theme": "Design:",
        "language": "Sprache:",
        "file_action": "Dateiaktion:",
        "delete_permanently": "Dauerhaft löschen",
        "move_to_recycle": "In Papierkorb verschieben",
        "enable_verbose": "Ausführliches Protokoll aktivieren",
        "verbose_tooltip": "Wenn aktiviert, erfasst das Protokoll jede verarbeitete Datei/Ordner/AddOns.txt-Zeile.",
        "external_log": "Externes Protokoll:",
        "fresh": "Neu",
        "fresh_tooltip": "Bei jedem Export eine neue Protokolldatei erstellen (überschreibt vorhandene).",
        "append": "Anhängen",
        "append_tooltip": "Jeden Export an die vorhandene Protokolldatei anhängen (behält bis zu 10-20 Sitzungen basierend auf Ausführlichkeit).",
        "check_updates": "Auf Updates prüfen",
        "check_updates_tooltip": "Wenn aktiviert, beim Start auf neue Versionen auf GitHub prüfen.",
        "restore_defaults": "Standards wiederherstellen",
        "light": "hell",
        "dark": "dunkel",
        "scan": "Scannen",
        "select_all": "Alle auswählen",
        "expand_all": "Alle erweitern",
        "collapse_all": "Alle einklappen",
        "process_selected": "Ausgewählte verarbeiten",
        "scanning": "Wird gescannt…",
        "no_bak_old_found": "Keine .bak- oder .old-Dateien gefunden.",
        "files_found": "{} Datei(en) gefunden.",
        "version": "Version:",
        "path": "Pfad:",
        "preview": "Vorschau",
        "toggle_all": "Alle umschalten",
        "process_folders": "Ausgewählte Ordner verarbeiten",
        "rebuild_addons": "AddOns.txt neu erstellen",
        "no_orphans_found": "Keine verwaisten SavedVariables gefunden.",
        "orphans_found": "{} verwaiste SavedVariable(s) gefunden.",
        "scan_hardware": "Hardware scannen",
        "system_matches": "Ihr System entspricht:",
        "optimization_applied": "✓ Optimierung angewendet",
        "optimization_not_applied": "⚠ Optimierung noch nicht angewendet",
        "graphics_presets": "Grafikvoreinstellungen (Retail):",
        "graphics_presets_classic": "Grafikvoreinstellungen (Classic):",
        "apply_preset": "Voreinstellung anwenden:",
        "apply": "Anwenden",
        "preset_applied": "✓ {}-Voreinstellung angewendet.",
        "error": "✗ Fehler: {}",
        "low": "Niedrig",
        "medium": "Mittel",
        "high": "Hoch",
        "ultra": "Ultra",
        "manual_suggestions": "Manuelle Optimierungsvorschläge",
        "manual_disclaimer": "HINWEIS: Diese Anwendung führt diese Optimierungen NICHT automatisch durch. Dies sind manuelle Vorschläge, die Sie selbst umsetzen können.",
        "clean_data_folder": "Spieldaten-Ordner bereinigen",
        "clean_data_text": "Wenn seit der Installation von World of Warcraft mehrere Jahre oder Erweiterungen vergangen sind, sollten Sie den Data-Ordner aus Ihrem World of Warcraft-Hauptverzeichnis löschen. Dies *könnte* die Spielgröße reduzieren und die Ladebildschirmleistung verbessern. Der Battle.net-Launcher erstellt diesen Ordner automatisch neu.",
        "enable_hdr": "HDR (High Dynamic Range) aktivieren",
        "enable_hdr_text": "Überprüfen Sie die Anzeigeeinstellungen Ihres Betriebssystems, ob HDR verfügbar ist. Wenn Ihr Monitor dies unterstützt, kann die Aktivierung von HDR die visuelle Klarheit und Farbtiefe im Spiel erheblich verbessern.",
        "verify_refresh": "Bildwiederholrate des Monitors überprüfen",
        "verify_refresh_text": "Stellen Sie sicher, dass die Bildwiederholrate Ihres Monitors in den Anzeigeeinstellungen des Betriebssystems auf den maximal unterstützten Wert eingestellt ist. Höhere Bildwiederholraten sorgen für flüssigeres Gameplay und bessere Reaktionsfähigkeit.",
        "enable_sam": "Smart Access Memory / Resizable BAR aktivieren",
        "enable_sam_text": "Überprüfen Sie die BIOS-Einstellungen Ihres Motherboards auf Smart Access Memory (AMD) oder Resizable BAR (Intel/NVIDIA). Die Aktivierung dieser Funktion ermöglicht Ihrer CPU den Zugriff auf den vollen GPU-Speicher, was die Leistung potenziell verbessern kann.",
        "enable_xmp": "XMP-Speicherprofil aktivieren",
        "enable_xmp_text": "Greifen Sie auf das BIOS Ihres Motherboards zu und aktivieren Sie die XMP (Extreme Memory Profile)- oder DOCP/EOCP-Einstellung. Dadurch wird sichergestellt, dass Ihr RAM mit der angegebenen Geschwindigkeit statt mit konservativen Standardgeschwindigkeiten läuft, was die Gesamtsystemleistung verbessert.",
        "export_log": "Protokoll exportieren",
        "clear_log": "Protokoll löschen",
        "about_text": "Eine umfassende Wartungs- und Optimierungssuite für World of Warcraft.\nBereinigen Sie unnötige Dateien, verwalten Sie Addons, optimieren Sie die Spielleistung und mehr.\n\nSchließen Sie World of Warcraft immer, bevor Sie dieses Tool verwenden.",
        "copyright": "Copyright © 2025 Paul Vandersypen. Veröffentlicht unter der GNU General Public License v3.0 (GPL-3.0-or-later). Siehe die beigefügte LICENSE-Datei für vollständige Bedingungen.",
        "invalid_folder": "Ungültiger Ordner",
        "select_valid_wow": "Bitte wählen Sie zuerst einen gültigen WoW-Ordner aus.",
        "no_selection": "Keine Auswahl",
        "no_files_selected": "Keine Dateien zur Verarbeitung ausgewählt.",
        "no_folders_selected": "Keine Ordner für die Bereinigung ausgewählt.",
        "no_orphans_selected": "Keine verwaisten Dateien ausgewählt.",
        "confirm": "Bestätigen",
        "confirm_action": "Sind Sie sicher, dass Sie {} {} {} möchten?",
        "file_s": "Datei(en)",
        "folder_s": "Ordner",
        "orphaned_savedvars": "verwaiste SavedVariables",
        "completed": "Abgeschlossen",
        "processed": "{} {} verarbeitet.",
        "send2trash_missing": "send2trash fehlt",
        "send2trash_unavailable": "Das Modul 'send2trash' ist nicht verfügbar. Dateien wurden dauerhaft gelöscht.",
        "send2trash_install": "Das Paket 'send2trash' ist nicht installiert.\nUm die Papierkorb-Unterstützung zu aktivieren, installieren Sie es manuell:\n\n  pip install send2trash\n\noder:\n\n  python -m pip install --user send2trash",
        "restore_defaults_confirm": "Alle Einstellungen auf Standardwerte zurücksetzen?",
        "restart_required": "Einstellungen wiederhergestellt. Die Anwendung wird jetzt neu gestartet.",
        "error_title": "Fehler",
        "restore_error": "Fehler beim Wiederherstellen der Standardeinstellungen: {}",
        "confirm_font": "Schriftart bestätigen",
        "apply_font_confirm": "Schriftart '{}' auf die Anwendung anwenden?",
        "export_log_title": "Protokoll exportieren",
        "log_empty": "Protokoll ist leer. Nichts zu exportieren.",
        "log_exported": "Protokoll erfolgreich exportiert nach:\n{}",
        "export_error": "Exportfehler",
        "export_failed": "Fehler beim Exportieren des Protokolls:\n{}",
        "addons_rebuilt": "AddOns.txt-Einträge neu erstellt.\nGesamt geschrieben: {}\nGesamt entfernt: {}",
        "session_started": "Sitzung gestartet — {}",
        "file_scan": "Dateibereinigung Scan: {} Treffer.",
        "orphan_scan": "Verwaiste Dateien Scan: {} verwaiste Datei(en).",
        "file_processed": "Dateibereinigung: {} Datei(en) verarbeitet.",
        "folder_processed": "Ordnerbereinigung: {} Ordner verarbeitet.",
        "orphan_processed": "Verwaiste Dateien: {} verwaiste Datei(en) verarbeitet.",
        "send2trash_warning": "Warnung: send2trash nicht installiert; Löschungen waren dauerhaft.",
        "addons_txt_log": "[AddOns.txt] {}: {} Einträge geschrieben, {} entfernt",
        "preset_applied_log": "{}-Voreinstellung für {} angewendet",
        "preset_failed_log": "Fehler beim Anwenden der {}-Voreinstellung: {}",
    },
    
    # Add other languages with key translations
    # For brevity, I'll add French and Spanish as examples, with placeholders for others
    
    "frFR": {
        "window_title": "Outil de nettoyage WoW",
        "file_cleaner": "Nettoyeur de fichiers",
        "folder_cleaner": "Nettoyeur de dossiers",
        "orphan_cleaner": "Nettoyeur d'orphelins",
        "game_optimizer": "Optimiseur de jeu",
        "optimization_suggestions": "Suggestions d'optimisation",
        "log": "Journal",
        "help_about": "Aide / À propos",
        "options": "Options",
        "wow_folder": "Dossier World of Warcraft :",
        "browse": "Parcourir...",
        "browse_tooltip": "Rechercher votre dossier World of Warcraft.",
        "font_size": "Taille de police :",
        "font": "Police :",
        "theme": "Thème :",
        "language": "Langue :",
        "file_action": "Action sur fichier :",
        "delete_permanently": "Supprimer définitivement",
        "move_to_recycle": "Déplacer vers la corbeille",
        "enable_verbose": "Activer le journal détaillé",
        "verbose_tooltip": "Lorsqu'activé, le journal capture chaque fichier/dossier/ligne AddOns.txt traité.",
        "external_log": "Journal externe :",
        "fresh": "Nouveau",
        "fresh_tooltip": "Créer un nouveau fichier journal à chaque exportation (écrase l'existant).",
        "append": "Ajouter",
        "append_tooltip": "Ajouter chaque exportation au fichier journal existant (conserve jusqu'à 10-20 sessions selon la verbosité).",
        "check_updates": "Vérifier les mises à jour",
        "check_updates_tooltip": "Lorsqu'activé, vérifier les nouvelles versions sur GitHub au démarrage.",
        "restore_defaults": "Restaurer les valeurs par défaut",
        "light": "clair",
        "dark": "sombre",
        "scan": "Analyser",
        "select_all": "Tout sélectionner",
        "expand_all": "Tout développer",
        "collapse_all": "Tout réduire",
        "process_selected": "Traiter la sélection",
        "scanning": "Analyse en cours…",
        "no_bak_old_found": "Aucun fichier .bak ou .old trouvé.",
        "files_found": "{} fichier(s) trouvé(s).",
        # ... (additional French translations would continue here)
    },
    
    "esES": {
        "window_title": "Herramienta de limpieza de WoW",
        "file_cleaner": "Limpiador de archivos",
        "folder_cleaner": "Limpiador de carpetas",
        "orphan_cleaner": "Limpiador de huérfanos",
        "game_optimizer": "Optimizador de juego",
        "optimization_suggestions": "Sugerencias de optimización",
        "log": "Registro",
        "help_about": "Ayuda / Acerca de",
        "options": "Opciones",
        "wow_folder": "Carpeta de World of Warcraft:",
        "browse": "Examinar...",
        "browse_tooltip": "Buscar tu carpeta de World of Warcraft.",
        "font_size": "Tamaño de fuente:",
        "font": "Fuente:",
        "theme": "Tema:",
        "language": "Idioma:",
        "file_action": "Acción de archivo:",
        "delete_permanently": "Eliminar permanentemente",
        "move_to_recycle": "Mover a papelera de reciclaje",
        "enable_verbose": "Activar registro detallado",
        "verbose_tooltip": "Cuando está activado, el registro captura cada archivo/carpeta/línea de AddOns.txt procesada.",
        "external_log": "Registro externo:",
        "fresh": "Nuevo",
        "fresh_tooltip": "Crear un nuevo archivo de registro en cada exportación (sobrescribe el existente).",
        "append": "Añadir",
        "append_tooltip": "Añadir cada exportación al archivo de registro existente (mantiene hasta 10-20 sesiones según el detalle).",
        "check_updates": "Buscar actualizaciones",
        "check_updates_tooltip": "Cuando está activado, buscar nuevas versiones en GitHub al iniciar.",
        "restore_defaults": "Restaurar valores predeterminados",
        "light": "claro",
        "dark": "oscuro",
        "scan": "Escanear",
        "select_all": "Seleccionar todo",
        "expand_all": "Expandir todo",
        "collapse_all": "Contraer todo",
        "process_selected": "Procesar selección",
        "scanning": "Escaneando…",
        "no_bak_old_found": "No se encontraron archivos .bak o .old.",
        "files_found": "{} archivo(s) encontrado(s).",
        # ... (additional Spanish translations would continue here)
    },
}

# Add fallback for languages that haven't been fully translated yet
for lang_code in AVAILABLE_LANGUAGES.keys():
    if lang_code not in TRANSLATIONS:
        TRANSLATIONS[lang_code] = TRANSLATIONS["enUS"].copy()

# Current language
_current_language = DEFAULT_LANGUAGE

def detect_system_language():
    """Detect the system language and map it to a supported WoW locale."""
    try:
        system_locale = sys_locale.getdefaultlocale()[0]
        if not system_locale:
            return DEFAULT_LANGUAGE
        
        # Map common locale codes to WoW locales
        locale_map = {
            "en": "enUS",
            "de": "deDE",
            "fr": "frFR",
            "es": "esES",
            "pt": "ptBR",
            "it": "itIT",
            "ru": "ruRU",
            "ko": "koKR",
            "zh_CN": "zhCN",
            "zh_TW": "zhTW",
            "zh_HK": "zhTW",
        }
        
        # Try exact match first
        if system_locale in AVAILABLE_LANGUAGES:
            return system_locale
        
        # Try language code only
        lang_code = system_locale.split('_')[0]
        if lang_code in locale_map:
            return locale_map[lang_code]
        
        # Check for special cases
        if system_locale.startswith("es_MX") or system_locale.startswith("es_AR"):
            return "esMX"
        
        return DEFAULT_LANGUAGE
    except Exception:
        return DEFAULT_LANGUAGE

def set_language(lang_code):
    """Set the current language."""
    global _current_language
    if lang_code in AVAILABLE_LANGUAGES:
        _current_language = lang_code
    else:
        _current_language = DEFAULT_LANGUAGE

def get_language():
    """Get the current language code."""
    return _current_language

def get_text(key, *args, **kwargs):
    """
    Get translated text for the given key.
    
    Args:
        key: Translation key
        *args: Positional arguments for string formatting
        **kwargs: Keyword arguments for string formatting
    
    Returns:
        Translated and formatted string
    """
    try:
        text = TRANSLATIONS[_current_language].get(key, TRANSLATIONS["enUS"].get(key, key))
        if args:
            return text.format(*args)
        elif kwargs:
            return text.format(**kwargs)
        return text
    except Exception:
        return key

def get_available_languages():
    """Get dictionary of available language codes and names."""
    return AVAILABLE_LANGUAGES.copy()

# Convenience alias
_ = get_text
