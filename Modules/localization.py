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
        "graphics_presets": "Graphics Presets ({}):",
        "graphics_presets_classic": "Graphics Presets ({}):",
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
        "select_font": "Select Font",
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
        
        # Additional buttons and UI elements
        "apply": "Apply",
        "cancel": "Cancel",
        "scan_bak_old": "Scan for .bak / .old Files",
        "expand_all": "Expand All",
        "collapse_all": "Collapse All",
        "select_deselect_all": "Select / Deselect All",
        "process_selected_files": "Process Selected Files",
        "scan_orphaned": "Scan for Orphaned SavedVariables",
        "process_selected_folders": "Process Selected Folders",
        "select_deselect_all_folders": "Select / Deselect All Folders",
        "select_deselect_all_screenshots": "Select / Deselect All Screenshot Files",
        "screenshots_per_file": "Screenshots (per-file actions)",
        "check_for_updates": "Check for Updates",
        
        # Game Optimizer
        "game_optimizer_title": "Game Optimizer",
        "game_optimizer_desc": "Optimizes World of Warcraft's performance based on your hardware configuration.",
        "scan_hardware": "Scan Hardware",
        "click_scan_hardware": "Click 'Scan Hardware' to detect your system's capabilities.",
        "select_valid_wow_folder": "Select a valid World of Warcraft folder in Options to enable per-version views.",
        "recommended_settings": "Recommended Settings:",
        "apply_preset_label": "Apply Preset:",
        "apply_recommended_settings": "Apply Recommended Settings",
        "scanning_cpu": "Scanning CPU...",
        "scanning_ram": "Scanning RAM... (CPU: {}C/{}T detected)",
        "scanning_gpu": "Scanning GPU... (RAM: {} GB detected)",
        
        # Startup warning
        "important_notice": "Important Notice",
        "startup_warning_text": "⚠️ Please ensure World of Warcraft is completely closed before using this tool.\n\nRunning the tool while WoW is open could interfere with the game's files.",
        "do_not_show_again": "Do not show this warning again",
        "ok": "OK",
        
        # Folder cleaner
        "select_valid_wow_folder_cleaner": "Select a valid World of Warcraft folder in Options to enable Folder Cleaner.",
        "preview_label": "Preview",
        "screenshots_not_found": "Screenshots folder not found for this version.",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "Manual Optimization Suggestions",
        "opt_sug_disclaimer": "NOTE: This application does NOT perform these optimizations automatically. These are manual suggestions for you to implement.",
        "opt_sug_clean_data_title": "Clean Game Data Folder",
        "opt_sug_clean_data_text": "If several years or multiple expansions have passed since installing World of Warcraft, consider deleting the Data folder from your main World of Warcraft directory. This *could* reduce game size and improve loading screen performance. The Battle.net launcher will automatically rebuild this folder when needed.",
        "opt_sug_clean_data_tooltip": "WHY: The Data folder accumulates temporary and cached game assets over time. Deleting it forces a fresh download of optimized files.\n\nRISK LEVEL: Safe - Battle.net will redownload needed files automatically.\n\nEXPECTED BENEFIT: Faster loading screens, reduced disk usage (potentially 10-20 GB saved).",
        "opt_sug_hdr_title": "Enable HDR (High Dynamic Range)",
        "opt_sug_hdr_text": "Check your operating system's display settings to see if HDR is available. If supported by your monitor, enabling HDR can significantly improve visual clarity and color depth in-game.",
        "opt_sug_hdr_tooltip": "WHY: HDR provides wider color gamut and better contrast, making visuals more vibrant and realistic.\n\nRISK LEVEL: Safe - Can be toggled on/off easily in OS settings.\n\nEXPECTED BENEFIT: Dramatically improved visual quality if monitor supports HDR10 or better.\n\nREQUIREMENT: HDR-capable monitor and Windows 10/11 or macOS Catalina+.",
        "opt_sug_refresh_title": "Verify Monitor Refresh Rate",
        "opt_sug_refresh_text": "Ensure your monitor's refresh rate is set to the maximum supported value in your operating system's display settings. Higher refresh rates provide smoother gameplay and better responsiveness.",
        "opt_sug_refresh_tooltip": "WHY: Many systems default to 60Hz even when monitors support 120Hz/144Hz/165Hz. This caps your frame rate unnecessarily.\n\nRISK LEVEL: Safe - No hardware risk, easily reversible.\n\nEXPECTED BENEFIT: Smoother gameplay, reduced input lag, better reaction times.\n\nHOW TO CHECK: Windows: Settings > Display > Advanced > Refresh rate\nmacOS: System Preferences > Displays",
        "opt_sug_sam_title": "Enable Smart Access Memory / Resizable BAR",
        "opt_sug_sam_text": "Check your motherboard BIOS settings for Smart Access Memory (AMD) or Resizable BAR (Intel/NVIDIA). Enabling this feature allows your CPU to access the full GPU memory, potentially improving performance.",
        "opt_sug_sam_tooltip": "WHY: Allows CPU to access entire GPU memory at once instead of small 256MB chunks, reducing bottlenecks.\n\nRISK LEVEL: Moderate - Requires BIOS changes. Document current settings first.\n\nEXPECTED BENEFIT: 5-15% FPS improvement in GPU-intensive scenarios.\n\nREQUIREMENTS:\n• AMD: Ryzen 5000+ CPU + RX 6000+ GPU\n• Intel: 10th gen+ CPU + RTX 3000+ GPU\n• BIOS update may be required",
        "opt_sug_xmp_title": "Enable XMP Memory Profile",
        "opt_sug_xmp_text": "Access your motherboard BIOS and enable the XMP (Extreme Memory Profile) or DOCP/EOCP setting. This ensures your RAM runs at its rated speed rather than default conservative speeds, improving overall system performance.",
        "opt_sug_xmp_tooltip": "WHY: RAM typically runs at 2133MHz by default even if rated for 3200MHz+. XMP enables advertised speeds.\n\nRISK LEVEL: Moderate - BIOS change. System may fail to boot if RAM is unstable (easy to reset).\n\nEXPECTED BENEFIT: 10-20% CPU performance boost, faster loading times, better 1% lows.\n\nHOW TO ENABLE: Enter BIOS (usually Del/F2 at startup) > Find XMP/DOCP setting > Enable > Save & Exit",
        
        # Help/About tab - content
        "help_version_label": "WoW Cleanup Tool {}",
        "help_about_description": "A comprehensive maintenance and optimization suite for World of Warcraft.\nClean unnecessary files, manage addons, optimize game performance, and more.\n\nAlways close World of Warcraft before running this tool.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Released under the GNU General Public License v3.0 (GPL-3.0-or-later). See the included LICENSE file for full terms.",
        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU: {} | RAM: {} | GPU: {}",
        "gpu_switch_notification": "⚠ GPU Switch: Configured to use '{}' instead of '{}'. This change optimizes performance by using your dedicated GPU for better gaming experience. This is safe and recommended.",
        "scan_tooltip_refresh": "Scanning again is not necessary unless you have changed your CPU, GPU, or RAM.\nClick to refresh the cached hardware information.",
        "scanning_ram_detected": "Scanning RAM... (CPU: {}C/{}T detected)",
        "scanning_gpu_detected": "Scanning GPU... (RAM: {} GB detected)",
        "apply_preset_label": "Apply Preset:",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "World of Warcraft Running",
        "wow_running_message": "World of Warcraft is currently running. Changes will take effect after restarting the game.\n\nDo you want to continue?",
        "permission_error_title": "Permission Error",
        "permission_error_message": "Config.wtf is read-only. Please remove the read-only attribute and try again.",
        "config_readonly_status": "✗ Config.wtf is read-only.",
        "confirm_apply_title": "Confirm Apply",
        "confirm_apply_message": "Apply {} preset to {}?\n\nThis will modify {} graphics settings in Config.wtf.\nA backup will be created automatically.\n\nMain changes:\n• Preset: {} quality settings\n• Performance: {} optimization(s)",
        "cancelled_by_user": "Cancelled by user.",
        "settings_applied_status": "✓ {} settings applied.",
        "preset_applied_status": "✓ {} preset applied.",
        "apply_error_status": "✗ Error: {}",
        
        # Preset tooltips
        "preset_tooltip_template": "{} Preset\n\nExpected Performance:\n{}\n\nClick 'Apply' below to use this preset.",
        "perf_depends_hardware": "Performance impact depends on your hardware.",
        "perf_will_vary": "Performance will vary",
        
        # Low preset performance estimates
        "low_perf_high": "Excellent performance (100+ FPS in most scenarios)",
        "low_perf_mid": "Very good performance (80-120 FPS)",
        "low_perf_low": "Good performance (60-80 FPS)",
        
        # Medium preset performance estimates
        "medium_perf_high": "Excellent performance (90-120 FPS)",
        "medium_perf_mid": "Good performance (60-90 FPS)",
        "medium_perf_low": "Moderate performance (45-60 FPS)",
        
        # High preset performance estimates
        "high_perf_high": "Very good performance (70-100 FPS)",
        "high_perf_mid": "Good performance (50-70 FPS)",
        "high_perf_low": "May struggle in raids (30-50 FPS)",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "Good performance (60-80 FPS)",
        "ultra_perf_mid": "Moderate performance (40-60 FPS)",
        "ultra_perf_low": "Low performance (20-40 FPS)",
        
        # WoW version names
        "version_retail": "Retail",
        "version_classic": "Classic",
        "version_classic_era": "Classic Era",
        "version_ptr": "PTR",
        "version_beta": "Beta",
        
        # Game Optimizer - additional strings
        "not_detected": "Not detected",
        "unknown_cpu": "Unknown CPU",
        "unknown_gpu": "Unknown",
        "not_set": "Not set",
        "hover_for_details": "Hover for details",
        
        # Orphan Cleaner - log messages
        "orphan_found_in": "[OrphanCleaner] Found orphan in {0}: {1}",
        "orphan_total_found": "[OrphanCleaner] Total orphaned SavedVariables: {0}",
        "orphan_moved_trash": "[OrphanCleaner] Moved to trash: {0}",
        "orphan_deleted": "[OrphanCleaner] Deleted: {0}",
        "orphan_error_deleting": "[OrphanCleaner] ERROR deleting {0}: {1}",
        "orphan_rebuilt_addons": "[OrphanCleaner] Rebuilt: {0}",
        "orphan_error_writing_addons": "[OrphanCleaner] ERROR writing AddOns.txt {0}: {1}",
        "orphan_error_rebuild": "[OrphanCleaner] ERROR during AddOns.txt rebuild: {0}",
        "new_setting_prefix": "[NEW] ",
        "details_colon": "Details:",
        "updated_settings": "• Updated {0} existing settings",
        "added_settings": "• Added {0} new settings",
        
        # Path Manager
        "select_wow_folder_title": "Select World of Warcraft Folder",
        "unrecognized_installation": "Unrecognized Installation",
        "folder_not_valid_continue": "The selected folder doesn't appear valid.\n\nContinue anyway?",
        "wow_folder_set": "WoW folder set: {}",
        
        # Performance
        "performance_execution_time": "[Performance] {} took {:.3f}s",
        "perf_moved_trash": "[{}] Moved to trash: {}",
        "perf_deleted": "[{}] Deleted: {}",
        "perf_error_deleting": "[{}] ERROR deleting {}: {}",
        
        "select_valid_wow_optimizer": "Select a valid World of Warcraft folder in Options to enable per-version views.",
        "select_valid_wow_folder_cleaner": "Select a valid World of Warcraft folder in Options to enable Folder Cleaner.",
        
        # Main UI - Buttons and Messages
        "apply": "Apply",
        "cancel": "Cancel",
        "export_log": "Export Log",
        "clear_log": "Clear Log",
        "confirm_font": "Confirm Font",
        "apply_font_question": "Apply font '{}' to the application?",
        "change_language": "Change Language",
        "change_language_question": "Change language from {} to {}?\n\nThe application will restart to apply the new language.",
        "language_changed": "Language Changed",
        "language_changed_restart": "Language changed to {}.\nThe application will now restart.",
        
        # Common Messages
        "invalid_folder": "Invalid Folder",
        "select_valid_wow_first": "Please select a valid WoW folder first.",
        "no_selection": "No Selection",
        "confirm": "Confirm",
        "completed": "Completed",
        "error": "Error",
        "restored": "Restored",
        
        # File Cleaner
        "no_files_selected": "No files selected for processing.",
        "found_files_count": "Found {} file(s) across versions.",
        "no_bak_old_found": "No .bak or .old files found.",
        "confirm_action_files": "Are you sure you want to {} {} file(s)?",
        "processed_files_count": "Processed {} file(s).",
        
        # Folder Cleaner
        "no_folders_selected": "No folders were selected for cleanup.",
        "confirm_action_folders": "Are you sure you want to {} {} folder(s)?",
        "processed_folders_count": "Processed {} folder(s).",
        
        # Orphan Cleaner
        "found_orphans_count": "Found {} orphan SavedVariable(s).",
        "no_orphans_found": "No orphaned SavedVariables found.",
        "no_orphans_selected": "No orphaned files selected.",
        "confirm_action_orphans": "Are you sure you want to {} {} orphaned SavedVariables?",
        "processed_orphans_count": "Processed {} orphan(s).",
        
        # Actions
        "move_to_trash": "move to Recycle Bin/Trash",
        "delete_permanently_action": "delete permanently",
        
        # send2trash Warnings
        "send2trash_missing": "send2trash missing",
        "send2trash_unavailable_files": "The 'send2trash' module is unavailable. Files were deleted permanently.",
        "send2trash_unavailable_folders": "The 'send2trash' module is unavailable. Folders were deleted permanently.",
        
        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "Rebuilt AddOns.txt entries.\nTotal written: {}\nTotal removed: {}",
        
        # Log Export
        "log_empty_nothing_export": "Log is empty. Nothing to export.",
        
        # Settings Restore
        "settings_restored_restart": "Settings restored to defaults. The application will now restart.",
        "settings_restored_manual": "Settings restored to defaults. Please restart the application manually.",
        "failed_restore_defaults": "Failed to restore defaults: {}",
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "Searches all detected WoW versions for addon SavedVariables (.lua / .lua.bak) that do not have a corresponding installed addon (Interface/AddOns). Scans Account, Realm, and Character SavedVariables folders. Processing also rebuilds AddOns.txt to match installed addons (preserving enabled/disabled where possible).",
        "orphan_description_part2": "Note: Blizzard_*.lua files are core game data and are automatically ignored for safety (but their .lua.bak backups may be removed).",
        "wtf_not_found": "WTF directory not found. Please launch the game first.",
        "unknown_preset": "Unknown preset: {}",
        "backup_failed": "Failed to create backup: {}",
        "config_write_failed": "Failed to write config: {}",
        "config_updated": "Applied {} settings to Config.wtf. ",
        "settings_updated_added": "Updated {} settings, added {} new settings.",
        "backup_saved": " Backup saved.",
        "version_path": "Version: {}\nPath: {}",
        "optimizer_launch_required": "The optimizer requires that {} has been launched at least once. Please launch World of Warcraft and proceed to the Character Select screen, then quit the game. After that, you can use the optimizer to apply graphics presets.",
        "system_matches": "Your system matches: {}",
        "optimizer_title": "Optimizer — {}",
        "recommendations_applied": "✓ Recommendations applied.",
        "applied_preset_log": "Applied {} preset for {}",
        "apply_preset_failed_log": "Failed to apply {} preset: {}",
        "hardware_scan_complete": "Hardware scan complete: cached to global settings.",
        "hardware_scan_failed": "Hardware scan failed: {}",
        "scan_error": "✗ Error: {}",
        
        # Game Validation
        "invalid_game_installation": "Invalid Game Installation",
        "game_installation_incomplete": "The World of Warcraft installation appears incomplete.\n\nPlease run the game at least once to initialize the Interface and WTF folders.\n\nAfter running the game, you can use this tool to clean up your installation.",
        
        # Startup Warning
        "user_disabled_warning": "User disabled startup warning.",
        
        # Update Checker
        "no_updates_available": "No Updates Available",
        "no_releases_published": "You are running {}.\n\nNo releases have been published yet.",
        "update_check_failed": "Update Check Failed",
        "update_check_http_error": "Could not check for updates:\n\nHTTP {}: {}",
        "update_check_network_error": "Could not check for updates:\n\n{}",
        "update_check_error": "Update Check Error",
        "update_check_exception": "An error occurred while checking for updates:\n\n{}",
        "update_available": "Update Available",
        "update_available_message": "A new version is available!\n\nCurrent: {}\nLatest: {}\n\nVisit the GitHub page to download the latest version.",
        "up_to_date": "Up to Date",
        "up_to_date_message": "You are running the latest version ({}).",
        "browser_open_error": "Could not open browser:\n\n{}",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[FileCleaner] Found file: {}",
        "file_cleaner_found": "[FileCleaner] Found: {}",
        "file_cleaner_total_found": "[FileCleaner] Total .bak/.old files found: {}",
        "file_cleaner_moved_trash": "[FileCleaner] Moved to trash: {}",
        "file_cleaner_deleted": "[FileCleaner] Deleted: {}",
        "file_cleaner_error_deleting": "[FileCleaner] ERROR deleting {}: {}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[FolderCleaner] Found: {}",
        "folder_cleaner_total": "[FolderCleaner] Total cleanable folders: {}",
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
        "graphics_presets": "Grafikvoreinstellungen ({}):",
        "graphics_presets_classic": "Grafikvoreinstellungen ({}):",
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
        "select_font": "Schriftart auswählen",
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
        "language_changed": "Sprache geändert",
        "language_changed_restart": "Die Sprache wurde geändert. Bitte starten Sie die Anwendung neu, damit alle Änderungen wirksam werden.",
        "apply": "Anwenden",
        "cancel": "Abbrechen",
        "scan_bak_old": "Nach .bak / .old-Dateien suchen",
        "expand_all": "Alle erweitern",
        "collapse_all": "Alle einklappen",
        "select_deselect_all": "Alle auswählen / Abwählen",
        "process_selected_files": "Ausgewählte Dateien verarbeiten",
        "scan_orphaned": "Nach verwaisten SavedVariables suchen",
        "process_selected_folders": "Ausgewählte Ordner verarbeiten",
        "select_deselect_all_folders": "Alle Ordner auswählen / Abwählen",
        "select_deselect_all_screenshots": "Alle Screenshot-Dateien auswählen / Abwählen",
        "screenshots_per_file": "Screenshots (Aktionen pro Datei)",
        "check_for_updates": "Auf Updates prüfen",
        "game_optimizer_title": "Spiel-Optimierer",
        "game_optimizer_desc": "Optimiert die Leistung von World of Warcraft basierend auf Ihrer Hardware-Konfiguration.",
        "scan_hardware": "Hardware scannen",
        "click_scan_hardware": "Klicken Sie auf 'Hardware scannen', um die Fähigkeiten Ihres Systems zu erkennen.",
        "select_valid_wow_folder": "Wählen Sie einen gültigen World of Warcraft-Ordner in den Optionen aus, um Versionsansichten zu aktivieren.",
        "recommended_settings": "Empfohlene Einstellungen:",
        "apply_preset_label": "Voreinstellung anwenden:",
        "apply_recommended_settings": "Empfohlene Einstellungen anwenden",
        "scanning_cpu": "CPU wird gescannt...",
        "scanning_ram": "RAM wird gescannt... (CPU: {}C/{}T erkannt)",
        "scanning_gpu": "GPU wird gescannt... (RAM: {} GB erkannt)",
        "important_notice": "Wichtiger Hinweis",
        "startup_warning_text": "⚠️ Bitte stellen Sie sicher, dass World of Warcraft vollständig geschlossen ist, bevor Sie dieses Tool verwenden.\n\nDas Ausführen des Tools während WoW geöffnet ist, könnte die Dateien des Spiels beeinträchtigen.",
        "do_not_show_again": "Diese Warnung nicht mehr anzeigen",
        "ok": "OK",
        "select_valid_wow_folder_cleaner": "Wählen Sie einen gültigen World of Warcraft-Ordner in den Optionen aus, um die Ordnerbereinigung zu aktivieren.",
        "preview_label": "Vorschau",
        "screenshots_not_found": "Screenshots-Ordner für diese Version nicht gefunden.",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "Manuelle Optimierungsvorschläge",
        "opt_sug_disclaimer": "HINWEIS: Diese Anwendung führt diese Optimierungen NICHT automatisch durch. Dies sind manuelle Vorschläge zur Umsetzung.",
        "opt_sug_clean_data_title": "Spieldaten-Ordner bereinigen",
        "opt_sug_clean_data_text": "Wenn seit der Installation von World of Warcraft mehrere Jahre oder Erweiterungen vergangen sind, sollten Sie den Data-Ordner aus Ihrem World of Warcraft-Hauptverzeichnis löschen. Dies *könnte* die Spielgröße reduzieren und die Ladebildschirmleistung verbessern. Der Battle.net-Launcher erstellt diesen Ordner automatisch neu.",
        "opt_sug_clean_data_tooltip": "WARUM: Der Data-Ordner sammelt im Laufe der Zeit temporäre und zwischengespeicherte Spiel-Assets. Das Löschen erzwingt einen frischen Download optimierter Dateien.\n\nRISIKOSTUFE: Sicher - Battle.net lädt benötigte Dateien automatisch neu herunter.\n\nERWARTETER NUTZEN: Schnellere Ladebildschirme, reduzierte Festplattennutzung (potenziell 10-20 GB gespart).",
        "opt_sug_hdr_title": "HDR (High Dynamic Range) aktivieren",
        "opt_sug_hdr_text": "Überprüfen Sie die Anzeigeeinstellungen Ihres Betriebssystems, ob HDR verfügbar ist. Wenn Ihr Monitor dies unterstützt, kann die Aktivierung von HDR die visuelle Klarheit und Farbtiefe im Spiel erheblich verbessern.",
        "opt_sug_hdr_tooltip": "WARUM: HDR bietet einen breiteren Farbraum und besseren Kontrast, was die Optik lebendiger und realistischer macht.\n\nRISIKOSTUFE: Sicher - Kann in den OS-Einstellungen einfach ein-/ausgeschaltet werden.\n\nERWARTETER NUTZEN: Dramatisch verbesserte visuelle Qualität, wenn der Monitor HDR10 oder besser unterstützt.\n\nVORAUSSETZUNG: HDR-fähiger Monitor und Windows 10/11 oder macOS Catalina+.",
        "opt_sug_refresh_title": "Bildwiederholrate des Monitors überprüfen",
        "opt_sug_refresh_text": "Stellen Sie sicher, dass die Bildwiederholrate Ihres Monitors in den Anzeigeeinstellungen auf den maximal unterstützten Wert eingestellt ist. Höhere Bildwiederholraten sorgen für flüssigeres Gameplay und bessere Reaktionsfähigkeit.",
        "opt_sug_refresh_tooltip": "WARUM: Viele Systeme verwenden standardmäßig 60Hz, obwohl Monitore 120Hz/144Hz/165Hz unterstützen. Dies begrenzt Ihre Bildrate unnötig.\n\nRISIKOSTUFE: Sicher - Kein Hardware-Risiko, leicht rückgängig zu machen.\n\nERWARTETER NUTZEN: Flüssigeres Gameplay, reduzierte Eingabeverzögerung, bessere Reaktionszeiten.\n\nSO PRÜFEN: Windows: Einstellungen > Anzeige > Erweitert > Bildwiederholrate\nmacOS: Systemeinstellungen > Bildschirme",
        "opt_sug_sam_title": "Smart Access Memory / Resizable BAR aktivieren",
        "opt_sug_sam_text": "Überprüfen Sie die BIOS-Einstellungen Ihres Motherboards auf Smart Access Memory (AMD) oder Resizable BAR (Intel/NVIDIA). Die Aktivierung ermöglicht Ihrer CPU den Zugriff auf den vollen GPU-Speicher, was die Leistung verbessern kann.",
        "opt_sug_sam_tooltip": "WARUM: Ermöglicht der CPU den Zugriff auf den gesamten GPU-Speicher auf einmal statt auf kleine 256MB-Stücke, wodurch Engpässe reduziert werden.\n\nRISIKOSTUFE: Moderat - Erfordert BIOS-Änderungen. Dokumentieren Sie zuerst die aktuellen Einstellungen.\n\nERWARTETER NUTZEN: 5-15% FPS-Verbesserung in GPU-intensiven Szenarien.\n\nVORAUSSETZUNGEN:\n• AMD: Ryzen 5000+ CPU + RX 6000+ GPU\n• Intel: 10. Gen+ CPU + RTX 3000+ GPU\n• BIOS-Update möglicherweise erforderlich",
        "opt_sug_xmp_title": "XMP-Speicherprofil aktivieren",
        "opt_sug_xmp_text": "Greifen Sie auf das BIOS Ihres Motherboards zu und aktivieren Sie die XMP (Extreme Memory Profile)- oder DOCP/EOCP-Einstellung. Dies stellt sicher, dass Ihr RAM mit der angegebenen Geschwindigkeit läuft, nicht mit konservativen Standardwerten.",
        "opt_sug_xmp_tooltip": "WARUM: RAM läuft standardmäßig mit 2133MHz, selbst wenn es für 3200MHz+ ausgelegt ist. XMP aktiviert die beworbenen Geschwindigkeiten.\n\nRISIKOSTUFE: Moderat - BIOS-Änderung. System kann beim Booten fehlschlagen, wenn RAM instabil ist (leicht zurückzusetzen).\n\nERWARTETER NUTZEN: 10-20% CPU-Leistungsschub, schnellere Ladezeiten, bessere 1%-Lows.\n\nSO AKTIVIEREN: BIOS aufrufen (meist Entf/F2 beim Start) > XMP/DOCP-Einstellung finden > Aktivieren > Speichern & Beenden",
        
        # Help/About tab - content
        "help_version_label": "WoW Bereinigungstool {}",
        "help_about_description": "Eine umfassende Wartungs- und Optimierungssuite für World of Warcraft.\nBereinigen Sie unnötige Dateien, verwalten Sie Addons, optimieren Sie die Spielleistung und mehr.\n\nSchließen Sie World of Warcraft immer, bevor Sie dieses Tool verwenden.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Veröffentlicht unter der GNU General Public License v3.0 (GPL-3.0-or-later). Siehe die beigefügte LICENSE-Datei für vollständige Bedingungen.",
        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU: {} | RAM: {} | GPU: {}",
        "gpu_switch_notification": "⚠ GPU-Wechsel: Konfiguriert zur Verwendung von '{}' anstelle von '{}'. Diese Änderung optimiert die Leistung durch Verwendung Ihrer dedizierten GPU für ein besseres Spielerlebnis. Dies ist sicher und empfohlen.",
        "scan_tooltip_refresh": "Erneutes Scannen ist nicht erforderlich, es sei denn, Sie haben CPU, GPU oder RAM geändert.\nKlicken Sie, um die zwischengespeicherten Hardware-Informationen zu aktualisieren.",
        "scanning_ram_detected": "RAM wird gescannt... (CPU: {}C/{}T erkannt)",
        "scanning_gpu_detected": "GPU wird gescannt... (RAM: {} GB erkannt)",
        "apply_preset_label": "Voreinstellung anwenden:",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "World of Warcraft läuft",
        "wow_running_message": "World of Warcraft läuft derzeit. Änderungen werden nach dem Neustart des Spiels wirksam.\n\nMöchten Sie fortfahren?",
        "permission_error_title": "Berechtigungsfehler",
        "permission_error_message": "Config.wtf ist schreibgeschützt. Bitte entfernen Sie das Schreibschutzattribut und versuchen Sie es erneut.",
        "config_readonly_status": "✗ Config.wtf ist schreibgeschützt.",
        "confirm_apply_title": "Anwendung bestätigen",
        "confirm_apply_message": "{}-Voreinstellung auf {} anwenden?\n\nDies ändert {} Grafikeinstellungen in Config.wtf.\nEin Backup wird automatisch erstellt.\n\nHauptänderungen:\n• Voreinstellung: {} Qualitätseinstellungen\n• Leistung: {} Optimierung(en)",
        "cancelled_by_user": "Vom Benutzer abgebrochen.",
        "settings_applied_status": "✓ {} Einstellungen angewendet.",
        "preset_applied_status": "✓ {}-Voreinstellung angewendet.",
        "apply_error_status": "✗ Fehler: {}",
        
        # Preset tooltips
        "preset_tooltip_template": "{}-Voreinstellung\n\nErwartete Leistung:\n{}\n\nKlicken Sie unten auf 'Anwenden', um diese Voreinstellung zu verwenden.",
        "perf_depends_hardware": "Die Leistungsauswirkung hängt von Ihrer Hardware ab.",
        "perf_will_vary": "Die Leistung variiert",
        
        # Low preset performance estimates
        "low_perf_high": "Hervorragende Leistung (100+ FPS in den meisten Szenarien)",
        "low_perf_mid": "Sehr gute Leistung (80-120 FPS)",
        "low_perf_low": "Gute Leistung (60-80 FPS)",
        
        # Medium preset performance estimates
        "medium_perf_high": "Hervorragende Leistung (90-120 FPS)",
        "medium_perf_mid": "Gute Leistung (60-90 FPS)",
        "medium_perf_low": "Moderate Leistung (45-60 FPS)",
        
        # High preset performance estimates
        "high_perf_high": "Sehr gute Leistung (70-100 FPS)",
        "high_perf_mid": "Gute Leistung (50-70 FPS)",
        "high_perf_low": "Kann in Raids schwächeln (30-50 FPS)",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "Gute Leistung (60-80 FPS)",
        "ultra_perf_mid": "Moderate Leistung (40-60 FPS)",
        "ultra_perf_low": "Niedrige Leistung (20-40 FPS)",
        
        # WoW version names
        "version_retail": "Retail",
        "version_classic": "Classic",
        "version_classic_era": "Classic Era",
        "version_ptr": "PTR",
        "version_beta": "Beta",
        
        # Game Optimizer - additional strings
        "not_detected": "Nicht erkannt",
        "unknown_cpu": "Unbekannte CPU",
        "unknown_gpu": "Unbekannt",
        "not_set": "Nicht gesetzt",
        "hover_for_details": "Für Details bewegen Sie die Maus darüber",
        
        # Orphan Cleaner - log messages
        "orphan_found_in": "[OrphanCleaner] Waise gefunden in {0}: {1}",
        "orphan_total_found": "[OrphanCleaner] Gesamt verwaiste SavedVariables: {0}",
        "orphan_moved_trash": "[OrphanCleaner] In Papierkorb verschoben: {0}",
        "orphan_deleted": "[OrphanCleaner] Gelöscht: {0}",
        "orphan_error_deleting": "[OrphanCleaner] FEHLER beim Löschen {0}: {1}",
        "orphan_rebuilt_addons": "[OrphanCleaner] Neu erstellt: {0}",
        "orphan_error_writing_addons": "[OrphanCleaner] FEHLER beim Schreiben von AddOns.txt {0}: {1}",
        "orphan_error_rebuild": "[OrphanCleaner] FEHLER während der AddOns.txt-Neuerstellung: {0}",
        "new_setting_prefix": "[NEU] ",
        "details_colon": "Details:",
        "updated_settings": "• {0} vorhandene Einstellungen aktualisiert",
        "added_settings": "• {0} neue Einstellungen hinzugefügt",
        
        # Path Manager
        "select_wow_folder_title": "World of Warcraft-Ordner auswählen",
        "unrecognized_installation": "Nicht erkannte Installation",
        "folder_not_valid_continue": "Der ausgewählte Ordner scheint ungültig zu sein.\n\nTrotzdem fortfahren?",
        "wow_folder_set": "WoW-Ordner festgelegt: {}",
        
        # Performance
        "performance_execution_time": "[Performance] {} benötigte {:.3f}s",
        "perf_moved_trash": "[{}] In Papierkorb verschoben: {}",
        "perf_deleted": "[{}] Gelöscht: {}",
        "perf_error_deleting": "[{}] FEHLER beim Löschen {}: {}",
        
        "select_valid_wow_optimizer": "Wählen Sie in den Optionen einen gültigen World of Warcraft-Ordner aus, um Versionsansichten zu aktivieren.",
        "select_valid_wow_folder_cleaner": "Wählen Sie in den Optionen einen gültigen World of Warcraft-Ordner aus, um den Ordner-Cleaner zu aktivieren.",
        
        # Main UI - Buttons and Messages
        "apply": "Anwenden",
        "cancel": "Abbrechen",
        "export_log": "Protokoll exportieren",
        "clear_log": "Protokoll löschen",
        "confirm_font": "Schriftart bestätigen",
        "apply_font_question": "Schriftart '{}' auf die Anwendung anwenden?",
        "change_language": "Sprache ändern",
        "change_language_question": "Sprache von {} auf {} ändern?\n\nDie Anwendung wird neu gestartet, um die neue Sprache anzuwenden.",
        "language_changed": "Sprache geändert",
        "language_changed_restart": "Sprache auf {} geändert.\nDie Anwendung wird jetzt neu gestartet.",
        
        # Common Messages
        "invalid_folder": "Ungültiger Ordner",
        "select_valid_wow_first": "Bitte wählen Sie zuerst einen gültigen WoW-Ordner aus.",
        "no_selection": "Keine Auswahl",
        "confirm": "Bestätigen",
        "completed": "Abgeschlossen",
        "error": "Fehler",
        "restored": "Wiederhergestellt",
        
        # File Cleaner
        "no_files_selected": "Keine Dateien zur Verarbeitung ausgewählt.",
        "found_files_count": "{} Datei(en) über Versionen gefunden.",
        "no_bak_old_found": "Keine .bak oder .old Dateien gefunden.",
        "confirm_action_files": "Sind Sie sicher, dass Sie {} {} Datei(en) möchten?",
        "processed_files_count": "{} Datei(en) verarbeitet.",
        
        # Folder Cleaner
        "no_folders_selected": "Keine Ordner zur Bereinigung ausgewählt.",
        "confirm_action_folders": "Sind Sie sicher, dass Sie {} {} Ordner möchten?",
        "processed_folders_count": "{} Ordner verarbeitet.",
        
        # Orphan Cleaner
        "found_orphans_count": "{} verwaiste SavedVariable(s) gefunden.",
        "no_orphans_found": "Keine verwaisten SavedVariables gefunden.",
        "no_orphans_selected": "Keine verwaisten Dateien ausgewählt.",
        "confirm_action_orphans": "Sind Sie sicher, dass Sie {} {} verwaiste SavedVariables möchten?",
        "processed_orphans_count": "{} Waisen verarbeitet.",
        
        # Actions
        "move_to_trash": "in den Papierkorb verschieben",
        "delete_permanently_action": "dauerhaft löschen",
        
        # send2trash Warnings
        "send2trash_missing": "send2trash fehlt",
        "send2trash_unavailable_files": "Das 'send2trash'-Modul ist nicht verfügbar. Dateien wurden dauerhaft gelöscht.",
        "send2trash_unavailable_folders": "Das 'send2trash'-Modul ist nicht verfügbar. Ordner wurden dauerhaft gelöscht.",
        
        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "AddOns.txt-Einträge neu erstellt.\nGesamt geschrieben: {}\nGesamt entfernt: {}",
        
        # Log Export
        "log_empty_nothing_export": "Protokoll ist leer. Nichts zu exportieren.",
        
        # Settings Restore
        "settings_restored_restart": "Einstellungen auf Standardwerte zurückgesetzt. Die Anwendung wird jetzt neu gestartet.",
        "settings_restored_manual": "Einstellungen auf Standardwerte zurückgesetzt. Bitte starten Sie die Anwendung manuell neu.",
        "failed_restore_defaults": "Fehler beim Zurücksetzen auf Standardwerte: {}",
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "Durchsucht alle erkannten WoW-Versionen nach Addon-SavedVariables (.lua / .lua.bak), die kein entsprechendes installiertes Addon (Interface/AddOns) haben. Scannt Account-, Realm- und Charakter-SavedVariables-Ordner. Die Verarbeitung erstellt auch AddOns.txt neu, um installierten Addons zu entsprechen (wobei aktiviert/deaktiviert nach Möglichkeit erhalten bleibt).",
        "orphan_description_part2": "Hinweis: Blizzard_*.lua-Dateien sind Kern-Spieldaten und werden aus Sicherheitsgründen automatisch ignoriert (aber ihre .lua.bak-Backups können entfernt werden).",
        "wtf_not_found": "WTF-Verzeichnis nicht gefunden. Bitte starten Sie das Spiel zuerst.",
        "unknown_preset": "Unbekannte Voreinstellung: {}",
        "backup_failed": "Backup-Erstellung fehlgeschlagen: {}",
        "config_write_failed": "Fehler beim Schreiben der Konfiguration: {}",
        "config_updated": "{}-Einstellungen auf Config.wtf angewendet. ",
        "settings_updated_added": "{} Einstellungen aktualisiert, {} neue Einstellungen hinzugefügt.",
        "backup_saved": " Backup gespeichert.",
        "version_path": "Version: {}\nPfad: {}",
        "optimizer_launch_required": "Der Optimierer erfordert, dass {} mindestens einmal gestartet wurde. Bitte starten Sie World of Warcraft und gehen Sie zum Charakterauswahlbildschirm, beenden Sie dann das Spiel. Danach können Sie den Optimierer verwenden, um Grafikvoreinstellungen anzuwenden.",
        "system_matches": "Ihr System entspricht: {}",
        "optimizer_title": "Optimierer — {}",
        "recommendations_applied": "✓ Empfehlungen angewendet.",
        "applied_preset_log": "{}-Voreinstellung für {} angewendet",
        "apply_preset_failed_log": "Fehler beim Anwenden der {}-Voreinstellung: {}",
        "hardware_scan_complete": "Hardware-Scan abgeschlossen: in globalen Einstellungen zwischengespeichert.",
        "hardware_scan_failed": "Hardware-Scan fehlgeschlagen: {}",
        "scan_error": "✗ Fehler: {}",
        
        # Game Validation
        "invalid_game_installation": "Ungültige Spielinstallation",
        "game_installation_incomplete": "Die World of Warcraft-Installation scheint unvollständig zu sein.\n\nBitte starten Sie das Spiel mindestens einmal, um die Interface- und WTF-Ordner zu initialisieren.\n\nNach dem Ausführen des Spiels können Sie dieses Tool zur Bereinigung Ihrer Installation verwenden.",
        
        # Startup Warning
        "user_disabled_warning": "Benutzer hat Startwarnung deaktiviert.",
        
        # Update Checker
        "no_updates_available": "Keine Updates verfügbar",
        "no_releases_published": "Sie verwenden {}.\n\nBisher wurden keine Versionen veröffentlicht.",
        "update_check_failed": "Update-Prüfung fehlgeschlagen",
        "update_check_http_error": "Update-Prüfung nicht möglich:\n\nHTTP {}: {}",
        "update_check_network_error": "Update-Prüfung nicht möglich:\n\n{}",
        "update_check_error": "Update-Prüfungsfehler",
        "update_check_exception": "Bei der Update-Prüfung ist ein Fehler aufgetreten:\n\n{}",
        "update_available": "Update verfügbar",
        "update_available_message": "Eine neue Version ist verfügbar!\n\nAktuell: {}\nNeueste: {}\n\nBesuchen Sie die GitHub-Seite, um die neueste Version herunterzuladen.",
        "up_to_date": "Auf dem neuesten Stand",
        "up_to_date_message": "Sie verwenden die neueste Version ({}).",
        "browser_open_error": "Browser konnte nicht geöffnet werden:\n\n{}",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[Dateibereinigung] Datei gefunden: {}",
        "file_cleaner_found": "[Dateibereinigung] Gefunden: {}",
        "file_cleaner_total_found": "[Dateibereinigung] Insgesamt .bak/.old-Dateien gefunden: {}",
        "file_cleaner_moved_trash": "[Dateibereinigung] In Papierkorb verschoben: {}",
        "file_cleaner_deleted": "[Dateibereinigung] Gelöscht: {}",
        "file_cleaner_error_deleting": "[Dateibereinigung] FEHLER beim Löschen von {}: {}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[Ordnerbereinigung] Gefunden: {}",
        "folder_cleaner_total": "[Ordnerbereinigung] Insgesamt bereinigbare Ordner: {}",
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
        "version": "Version :",
        "path": "Chemin :",
        "preview": "Aperçu",
        "toggle_all": "Tout basculer",
        "process_folders": "Traiter les dossiers sélectionnés",
        "rebuild_addons": "Reconstruire AddOns.txt",
        "no_orphans_found": "Aucune SavedVariable orpheline trouvée.",
        "orphans_found": "{} SavedVariable(s) orpheline(s) trouvée(s).",
        "scan_hardware": "Analyser le matériel",
        "system_matches": "Votre système correspond à :",
        "optimization_applied": "✓ Optimisation appliquée",
        "optimization_not_applied": "⚠ Optimisation pas encore appliquée",
        "graphics_presets": "Préréglages graphiques ({}) :",
        "graphics_presets_classic": "Préréglages graphiques ({}) :",
        "apply_preset": "Appliquer le préréglage :",
        "apply": "Appliquer",
        "preset_applied": "✓ Préréglage {} appliqué.",
        "error": "✗ Erreur : {}",
        "low": "Faible",
        "medium": "Moyen",
        "high": "Élevé",
        "ultra": "Ultra",
        "manual_suggestions": "Suggestions d'optimisation manuelles",
        "manual_disclaimer": "REMARQUE : Cette application N'effectue PAS ces optimisations automatiquement. Ce sont des suggestions manuelles que vous devez mettre en œuvre.",
        "clean_data_folder": "Nettoyer le dossier de données du jeu",
        "clean_data_text": "Si plusieurs années ou extensions se sont écoulées depuis l'installation de World of Warcraft, envisagez de supprimer le dossier Data de votre répertoire principal World of Warcraft. Cela *pourrait* réduire la taille du jeu et améliorer les performances de l'écran de chargement. Le lanceur Battle.net reconstruira automatiquement ce dossier si nécessaire.",
        "enable_hdr": "Activer HDR (High Dynamic Range)",
        "enable_hdr_text": "Vérifiez les paramètres d'affichage de votre système d'exploitation pour voir si HDR est disponible. Si votre moniteur le prend en charge, l'activation de HDR peut améliorer considérablement la clarté visuelle et la profondeur des couleurs dans le jeu.",
        "verify_refresh": "Vérifier le taux de rafraîchissement du moniteur",
        "verify_refresh_text": "Assurez-vous que le taux de rafraîchissement de votre moniteur est réglé sur la valeur maximale prise en charge dans les paramètres d'affichage de votre système d'exploitation. Des taux de rafraîchissement plus élevés offrent un gameplay plus fluide et une meilleure réactivité.",
        "enable_sam": "Activer Smart Access Memory / Resizable BAR",
        "enable_sam_text": "Vérifiez les paramètres BIOS de votre carte mère pour Smart Access Memory (AMD) ou Resizable BAR (Intel/NVIDIA). L'activation de cette fonctionnalité permet à votre CPU d'accéder à la mémoire complète du GPU, améliorant potentiellement les performances.",
        "enable_xmp": "Activer le profil mémoire XMP",
        "enable_xmp_text": "Accédez au BIOS de votre carte mère et activez le paramètre XMP (Extreme Memory Profile) ou DOCP/EOCP. Cela garantit que votre RAM fonctionne à sa vitesse nominale plutôt qu'aux vitesses conservatrices par défaut, améliorant les performances globales du système.",
        "export_log": "Exporter le journal",
        "clear_log": "Effacer le journal",
        "about_text": "Une suite complète de maintenance et d'optimisation pour World of Warcraft.\nNettoyez les fichiers inutiles, gérez les addons, optimisez les performances du jeu, et plus encore.\n\nFermez toujours World of Warcraft avant d'utiliser cet outil.",
        "copyright": "Copyright © 2025 Paul Vandersypen. Publié sous la licence publique générale GNU v3.0 (GPL-3.0-or-later). Consultez le fichier LICENSE inclus pour les conditions complètes.",
        "invalid_folder": "Dossier invalide",
        "select_valid_wow": "Veuillez d'abord sélectionner un dossier WoW valide.",
        "no_selection": "Aucune sélection",
        "no_files_selected": "Aucun fichier sélectionné pour le traitement.",
        "no_folders_selected": "Aucun dossier sélectionné pour le nettoyage.",
        "no_orphans_selected": "Aucun fichier orphelin sélectionné.",
        "confirm": "Confirmer",
        "confirm_action": "Êtes-vous sûr de vouloir {} {} {} ?",
        "file_s": "fichier(s)",
        "folder_s": "dossier(s)",
        "orphaned_savedvars": "SavedVariables orphelines",
        "completed": "Terminé",
        "processed": "{} {} traité(s).",
        "send2trash_missing": "send2trash manquant",
        "send2trash_unavailable": "Le module 'send2trash' n'est pas disponible. Les fichiers ont été supprimés définitivement.",
        "send2trash_install": "Le paquet 'send2trash' n'est pas installé.\nPour activer la prise en charge de la corbeille, installez-le manuellement :\n\n  pip install send2trash\n\nou :\n\n  python -m pip install --user send2trash",
        "restore_defaults_confirm": "Restaurer tous les paramètres par défaut ?",
        "restart_required": "Paramètres restaurés. L'application va maintenant redémarrer.",
        "error_title": "Erreur",
        "restore_error": "Échec de la restauration des valeurs par défaut : {}",
        "confirm_font": "Confirmer la police",
        "apply_font_confirm": "Appliquer la police '{}' à l'application ?",
        "select_font": "Sélectionner la police",
        "export_log_title": "Exporter le journal",
        "log_empty": "Le journal est vide. Rien à exporter.",
        "log_exported": "Journal exporté avec succès vers :\n{}",
        "export_error": "Erreur d'exportation",
        "export_failed": "Échec de l'exportation du journal :\n{}",
        "addons_rebuilt": "Entrées AddOns.txt reconstruites.\nTotal écrit : {}\nTotal supprimé : {}",
        "session_started": "Session démarrée — {}",
        "file_scan": "Analyse du nettoyeur de fichiers : {} correspondance(s).",
        "orphan_scan": "Analyse du nettoyeur d'orphelins : {} orphelin(s).",
        "file_processed": "Nettoyeur de fichiers : {} fichier(s) traité(s).",
        "folder_processed": "Nettoyeur de dossiers : {} dossier(s) traité(s).",
        "orphan_processed": "Nettoyeur d'orphelins : {} orphelin(s) traité(s).",
        "send2trash_warning": "Avertissement : send2trash non installé ; les suppressions étaient définitives.",
        "addons_txt_log": "[AddOns.txt] {} : {} entrées écrites, {} supprimées",
        "preset_applied_log": "Préréglage {} appliqué pour {}",
        "preset_failed_log": "Échec de l'application du préréglage {} : {}",
        "language_changed": "Langue modifiée",
        "language_changed_restart": "La langue a été modifiée. Veuillez redémarrer l'application pour que tous les changements prennent effet.",
        "apply": "Appliquer",
        "cancel": "Annuler",
        "scan_bak_old": "Rechercher les fichiers .bak / .old",
        "expand_all": "Tout développer",
        "collapse_all": "Tout réduire",
        "select_deselect_all": "Tout sélectionner / Désélectionner",
        "process_selected_files": "Traiter les fichiers sélectionnés",
        "scan_orphaned": "Rechercher les SavedVariables orphelines",
        "process_selected_folders": "Traiter les dossiers sélectionnés",
        "select_deselect_all_folders": "Sélectionner / Désélectionner tous les dossiers",
        "select_deselect_all_screenshots": "Sélectionner / Désélectionner toutes les captures d'écran",
        "screenshots_per_file": "Captures d'écran (actions par fichier)",
        "check_for_updates": "Vérifier les mises à jour",
        "game_optimizer_title": "Optimiseur de jeu",
        "game_optimizer_desc": "Optimise les performances de World of Warcraft en fonction de votre configuration matérielle.",
        "scan_hardware": "Analyser le matériel",
        "click_scan_hardware": "Cliquez sur 'Analyser le matériel' pour détecter les capacités de votre système.",
        "select_valid_wow_folder": "Sélectionnez un dossier World of Warcraft valide dans les options pour activer les vues par version.",
        "recommended_settings": "Paramètres recommandés :",
        "apply_preset_label": "Appliquer le préréglage :",
        "apply_recommended_settings": "Appliquer les paramètres recommandés",
        "scanning_cpu": "Analyse du CPU...",
        "scanning_ram": "Analyse de la RAM... (CPU : {}C/{}T détecté)",
        "scanning_gpu": "Analyse du GPU... (RAM : {} Go détectée)",
        "important_notice": "Avis important",
        "startup_warning_text": "⚠️ Veuillez vous assurer que World of Warcraft est complètement fermé avant d'utiliser cet outil.\n\nExécuter l'outil pendant que WoW est ouvert pourrait interférer avec les fichiers du jeu.",
        "do_not_show_again": "Ne plus afficher cet avertissement",
        "ok": "OK",
        "select_valid_wow_folder_cleaner": "Sélectionnez un dossier World of Warcraft valide dans les options pour activer le nettoyeur de dossiers.",
        "preview_label": "Aperçu",
        "screenshots_not_found": "Dossier de captures d'écran introuvable pour cette version.",
        
        # Main UI - Buttons and Messages
        "apply": "Appliquer",
        "cancel": "Annuler",
        "export_log": "Exporter le journal",
        "clear_log": "Effacer le journal",
        "confirm_font_change": "Confirmation de changement de police",
        "font_change_restart_required": "Le changement de police nécessite un redémarrage de l'application.\nVoulez-vous redémarrer maintenant ?",
        "restart": "Redémarrer",
        "later": "Plus tard",
        "confirm_language_change": "Confirmer le changement de langue",
        "language_change_restart_required": "Le changement de langue nécessite un redémarrage de l'application pour prendre effet.\n\nVoulez-vous redémarrer maintenant ?",
        "language_change_restart_message": "Veuillez redémarrer l'application pour que le changement de langue prenne effet.",
        "invalid_folder_title": "Dossier invalide",
        
        # Common Messages
        "invalid_folder_select_valid_wow": "Veuillez sélectionner un dossier World of Warcraft valide dans les options.",
        "scanning_files": "Analyse des fichiers...",
        "scanning_folders": "Analyse des dossiers...",
        "scanning_orphans": "Analyse des AddOns orphelins...",
        "no_files_selected": "Aucun fichier sélectionné",
        "no_folders_selected": "Aucun dossier sélectionné",
        "no_orphans_selected": "Aucun orphelin sélectionné",
        
        # File Cleaner
        "select_files_to_delete": "Veuillez sélectionner au moins un fichier à supprimer.",
        "confirm_delete_files_title": "Confirmer la suppression des fichiers",
        "confirm_delete_files_message": "Êtes-vous sûr de vouloir supprimer {0} fichier(s) ?",
        "files_moved_to_recycle_bin": "{0} fichier(s) déplacé(s) vers la Corbeille.",
        "files_deletion_complete": "{0} fichier(s) supprimé(s) avec succès.",
        
        # Folder Cleaner
        "select_folders_to_delete": "Veuillez sélectionner au moins un dossier à supprimer.",
        "confirm_delete_folders_title": "Confirmer la suppression des dossiers",
        "confirm_delete_folders_message": "Êtes-vous sûr de vouloir supprimer {0} dossier(s) ?",
        
        # Orphan Cleaner
        "select_orphans_to_delete": "Veuillez sélectionner au moins un AddOn orphelin à supprimer.",
        "confirm_delete_orphans_title": "Confirmer la suppression des orphelins",
        "confirm_delete_orphans_message": "Êtes-vous sûr de vouloir supprimer {0} AddOn(s) orphelin(s) ?\n\nCela supprimera également tous les fichiers SavedVariables associés.",
        "orphans_moved_to_recycle_bin": "{0} AddOn(s) orphelin(s) déplacé(s) vers la Corbeille.",
        "orphans_deletion_complete": "{0} AddOn(s) orphelin(s) supprimé(s) avec succès.",
        
        # Actions
        "folders_moved_to_recycle_bin": "{0} dossier(s) déplacé(s) vers la Corbeille.",
        "folders_deletion_complete": "{0} dossier(s) supprimé(s) avec succès.",
        
        # send2trash Warnings
        "send2trash_not_available_files": "send2trash n'est pas disponible. Les fichiers seront supprimés définitivement.",
        "send2trash_not_available_folders": "send2trash n'est pas disponible. Les dossiers seront supprimés définitivement.",
        "send2trash_not_available_orphans": "send2trash n'est pas disponible. Les AddOns orphelins seront supprimés définitivement.",
        
        # AddOns.txt Rebuild
        "addons_txt_rebuild_summary": "AddOns.txt reconstruit avec succès !\n\nAddOns trouvés : {0}\nCharactères : {1}\nFichiers de configuration : {2}",
        
        # Log Export
        "log_export_empty": "Le journal est vide. Rien à exporter.",
        
        # Settings Restore
        "settings_restored_title": "Paramètres restaurés",
        "settings_restored_to_defaults": "Paramètres restaurés aux valeurs par défaut.",
        "settings_restored_restart_required": "Paramètres restaurés aux valeurs par défaut.\nVeuillez redémarrer l'application pour que tous les changements prennent effet.",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "Suggestions d'optimisation manuelle",
        "opt_sug_disclaimer": "REMARQUE : Cette application n'effectue PAS ces optimisations automatiquement. Ce sont des suggestions manuelles que vous devez mettre en œuvre.",
        "opt_sug_clean_data_title": "Nettoyer le dossier de données du jeu",
        "opt_sug_clean_data_text": "Si plusieurs années ou extensions se sont écoulées depuis l'installation de World of Warcraft, envisagez de supprimer le dossier Data de votre répertoire principal World of Warcraft. Cela *pourrait* réduire la taille du jeu et améliorer les performances de chargement. Battle.net reconstruira automatiquement ce dossier.",
        "opt_sug_clean_data_tooltip": "POURQUOI : Le dossier Data accumule des ressources temporaires et en cache au fil du temps. Le supprimer force un téléchargement frais de fichiers optimisés.\n\nNIVEAU DE RISQUE : Sûr - Battle.net retéléchargera automatiquement les fichiers nécessaires.\n\nAVANTAGE ATTENDU : Écrans de chargement plus rapides, utilisation du disque réduite (potentiellement 10-20 Go économisés).",
        "opt_sug_hdr_title": "Activer HDR (High Dynamic Range)",
        "opt_sug_hdr_text": "Vérifiez les paramètres d'affichage de votre système d'exploitation pour voir si HDR est disponible. Si votre moniteur le prend en charge, l'activation de HDR peut améliorer considérablement la clarté visuelle et la profondeur des couleurs dans le jeu.",
        "opt_sug_hdr_tooltip": "POURQUOI : HDR offre une gamme de couleurs plus large et un meilleur contraste, rendant les visuels plus vibrants et réalistes.\n\nNIVEAU DE RISQUE : Sûr - Peut être activé/désactivé facilement dans les paramètres du système.\n\nAVANTAGE ATTENDU : Qualité visuelle considérablement améliorée si le moniteur prend en charge HDR10 ou mieux.\n\nEXIGENCE : Moniteur compatible HDR et Windows 10/11 ou macOS Catalina+.",
        "opt_sug_refresh_title": "Vérifier le taux de rafraîchissement du moniteur",
        "opt_sug_refresh_text": "Assurez-vous que le taux de rafraîchissement de votre moniteur est réglé sur la valeur maximale prise en charge dans les paramètres d'affichage. Des taux plus élevés offrent un gameplay plus fluide et une meilleure réactivité.",
        "opt_sug_refresh_tooltip": "POURQUOI : De nombreux systèmes utilisent par défaut 60Hz même si les moniteurs prennent en charge 120Hz/144Hz/165Hz. Cela limite inutilement votre fréquence d'images.\n\nNIVEAU DE RISQUE : Sûr - Aucun risque matériel, facilement réversible.\n\nAVANTAGE ATTENDU : Gameplay plus fluide, latence d'entrée réduite, meilleurs temps de réaction.\n\nCOMMENT VÉRIFIER : Windows : Paramètres > Affichage > Avancé > Taux de rafraîchissement\nmacOS : Préférences Système > Moniteurs",
        "opt_sug_sam_title": "Activer Smart Access Memory / Resizable BAR",
        "opt_sug_sam_text": "Vérifiez les paramètres BIOS de votre carte mère pour Smart Access Memory (AMD) ou Resizable BAR (Intel/NVIDIA). L'activation de cette fonctionnalité permet à votre CPU d'accéder à la mémoire complète du GPU, améliorant potentiellement les performances.",
        "opt_sug_sam_tooltip": "POURQUOI : Permet au CPU d'accéder à toute la mémoire du GPU d'un coup au lieu de petits morceaux de 256Mo, réduisant les goulots d'étranglement.\n\nNIVEAU DE RISQUE : Modéré - Nécessite des modifications du BIOS. Documentez d'abord les paramètres actuels.\n\nAVANTAGE ATTENDU : Amélioration de 5-15% des FPS dans les scénarios intensifs en GPU.\n\nEXIGENCES :\n• AMD : CPU Ryzen 5000+ + GPU RX 6000+\n• Intel : CPU 10e gen+ + GPU RTX 3000+\n• Mise à jour du BIOS peut être nécessaire",
        "opt_sug_xmp_title": "Activer le profil mémoire XMP",
        "opt_sug_xmp_text": "Accédez au BIOS de votre carte mère et activez le paramètre XMP (Extreme Memory Profile) ou DOCP/EOCP. Cela garantit que votre RAM fonctionne à sa vitesse nominale plutôt qu'aux vitesses conservatrices par défaut.",
        "opt_sug_xmp_tooltip": "POURQUOI : La RAM fonctionne généralement à 2133MHz par défaut même si elle est conçue pour 3200MHz+. XMP active les vitesses annoncées.\n\nNIVEAU DE RISQUE : Modéré - Modification du BIOS. Le système peut ne pas démarrer si la RAM est instable (facile à réinitialiser).\n\nAVANTAGE ATTENDU : Augmentation de 10-20% des performances CPU, temps de chargement plus rapides, meilleurs 1% lows.\n\nCOMMENT ACTIVER : Entrez dans le BIOS (généralement Suppr/F2 au démarrage) > Trouvez le paramètre XMP/DOCP > Activez > Enregistrez et quittez",
        
        # Help/About tab - content
        "help_version_label": "Outil de nettoyage WoW {}",
        "help_about_description": "Une suite complète de maintenance et d'optimisation pour World of Warcraft.\nNettoyez les fichiers inutiles, gérez les addons, optimisez les performances du jeu, et plus encore.\n\nFermez toujours World of Warcraft avant d'utiliser cet outil.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Publié sous la licence publique générale GNU v3.0 (GPL-3.0-or-later). Consultez le fichier LICENSE inclus pour les conditions complètes.",
        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU : {} | RAM : {} | GPU : {}",
        "gpu_switch_notification": "⚠ Changement de GPU : Configuré pour utiliser '{}' au lieu de '{}'. Ce changement optimise les performances en utilisant votre GPU dédié pour une meilleure expérience de jeu. C'est sûr et recommandé.",
        "scan_tooltip_refresh": "Une nouvelle analyse n'est pas nécessaire sauf si vous avez changé votre CPU, GPU ou RAM.\nCliquez pour actualiser les informations matérielles en cache.",
        "scanning_ram_detected": "Analyse de la RAM... (CPU : {}C/{}T détecté)",
        "scanning_gpu_detected": "Analyse du GPU... (RAM : {} Go détectée)",
        "apply_preset_label": "Appliquer le préréglage :",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "World of Warcraft en cours d'exécution",
        "wow_running_message": "World of Warcraft est actuellement en cours d'exécution. Les modifications prendront effet après le redémarrage du jeu.\n\nVoulez-vous continuer ?",
        "permission_error_title": "Erreur de permission",
        "permission_error_message": "Config.wtf est en lecture seule. Veuillez supprimer l'attribut de lecture seule et réessayer.",
        "config_readonly_status": "✗ Config.wtf est en lecture seule.",
        "confirm_apply_title": "Confirmer l'application",
        "confirm_apply_message": "Appliquer le préréglage {} à {} ?\n\nCela modifiera {} paramètres graphiques dans Config.wtf.\nUne sauvegarde sera créée automatiquement.\n\nModifications principales :\n• Préréglage : {} paramètres de qualité\n• Performance : {} optimisation(s)",
        "cancelled_by_user": "Annulé par l'utilisateur.",
        "settings_applied_status": "✓ {} paramètres appliqués.",
        "preset_applied_status": "✓ Préréglage {} appliqué.",
        "apply_error_status": "✗ Erreur : {}",
        
        # Preset tooltips
        "preset_tooltip_template": "Préréglage {}\n\nPerformance attendue :\n{}\n\nCliquez sur 'Appliquer' ci-dessous pour utiliser ce préréglage.",
        "perf_depends_hardware": "L'impact sur les performances dépend de votre matériel.",
        "perf_will_vary": "Les performances varieront",
        
        # Low preset performance estimates
        "low_perf_high": "Excellentes performances (100+ FPS dans la plupart des scénarios)",
        "low_perf_mid": "Très bonnes performances (80-120 FPS)",
        "low_perf_low": "Bonnes performances (60-80 FPS)",
        
        # Medium preset performance estimates
        "medium_perf_high": "Excellentes performances (90-120 FPS)",
        "medium_perf_mid": "Bonnes performances (60-90 FPS)",
        "medium_perf_low": "Performances modérées (45-60 FPS)",
        
        # High preset performance estimates
        "high_perf_high": "Très bonnes performances (70-100 FPS)",
        "high_perf_mid": "Bonnes performances (50-70 FPS)",
        "high_perf_low": "Peut rencontrer des difficultés en raid (30-50 FPS)",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "Bonnes performances (60-80 FPS)",
        "ultra_perf_mid": "Performances modérées (40-60 FPS)",
        "ultra_perf_low": "Faibles performances (20-40 FPS)",
        
        # WoW version names
        "version_retail": "Retail",
        "version_classic": "Classic",
        "version_classic_era": "Classic Era",
        "version_ptr": "PTR",
        "version_beta": "Bêta",
        
        # Game Optimizer - additional strings
        "not_detected": "Non détecté",
        "unknown_cpu": "CPU inconnu",
        "unknown_gpu": "Inconnu",
        "not_set": "Non défini",
        "hover_for_details": "Survolez pour plus de détails",
        
        # Orphan Cleaner - log messages
        "orphan_found_in": "[OrphanCleaner] Orphelin trouvé dans {0} : {1}",
        "orphan_total_found": "[OrphanCleaner] Total SavedVariables orphelins : {0}",
        "orphan_moved_trash": "[OrphanCleaner] Déplacé vers la corbeille : {0}",
        "orphan_deleted": "[OrphanCleaner] Supprimé : {0}",
        "orphan_error_deleting": "[OrphanCleaner] ERREUR lors de la suppression de {0} : {1}",
        "orphan_rebuilt_addons": "[OrphanCleaner] Reconstruit : {0}",
        "orphan_error_writing_addons": "[OrphanCleaner] ERREUR lors de l'écriture d'AddOns.txt {0} : {1}",
        "orphan_error_rebuild": "[OrphanCleaner] ERREUR lors de la reconstruction d'AddOns.txt : {0}",
        "new_setting_prefix": "[NOUVEAU] ",
        "details_colon": "Détails :",
        "updated_settings": "• {0} paramètres existants mis à jour",
        "added_settings": "• {0} nouveaux paramètres ajoutés",
        
        # Path Manager
        "select_wow_folder_title": "Sélectionner le dossier World of Warcraft",
        "unrecognized_installation": "Installation non reconnue",
        "folder_not_valid_continue": "Le dossier sélectionné ne semble pas valide.\n\nContinuer quand même ?",
        "wow_folder_set": "Dossier WoW défini : {}",
        
        # Performance
        "performance_execution_time": "[Performance] {} a pris {:.3f}s",
        "perf_moved_trash": "[{}] Déplacé vers la corbeille : {}",
        "perf_deleted": "[{}] Supprimé : {}",
        "perf_error_deleting": "[{}] ERREUR lors de la suppression de {} : {}",
        
        "select_valid_wow_optimizer": "Sélectionnez un dossier World of Warcraft valide dans les Options pour activer les vues par version.",
        "select_valid_wow_folder_cleaner": "Sélectionnez un dossier World of Warcraft valide dans les Options pour activer le Nettoyeur de dossiers.",
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "Recherche dans toutes les versions WoW détectées les SavedVariables d'addon (.lua / .lua.bak) qui n'ont pas d'addon installé correspondant (Interface/AddOns). Analyse les dossiers SavedVariables de compte, royaume et personnage. Le traitement reconstruit également AddOns.txt pour correspondre aux addons installés (en préservant activé/désactivé si possible).",
        "orphan_description_part2": "Remarque : Les fichiers Blizzard_*.lua sont des données de jeu principales et sont automatiquement ignorés par sécurité (mais leurs sauvegardes .lua.bak peuvent être supprimées).",
        "wtf_not_found": "Répertoire WTF introuvable. Veuillez d'abord lancer le jeu.",
        "unknown_preset": "Préréglage inconnu : {}",
        "backup_failed": "Échec de la création de la sauvegarde : {}",
        "config_write_failed": "Échec de l'écriture de la configuration : {}",
        "config_updated": "Paramètres {} appliqués à Config.wtf. ",
        "settings_updated_added": "{} paramètres mis à jour, {} nouveaux paramètres ajoutés.",
        "backup_saved": " Sauvegarde enregistrée.",
        "version_path": "Version : {}\nChemin : {}",
        "optimizer_launch_required": "L'optimiseur nécessite que {} ait été lancé au moins une fois. Veuillez lancer World of Warcraft et accéder à l'écran de sélection des personnages, puis quittez le jeu. Après cela, vous pouvez utiliser l'optimiseur pour appliquer des préréglages graphiques.",
        "system_matches": "Votre système correspond à : {}",
        "optimizer_title": "Optimiseur — {}",
        "recommendations_applied": "✓ Recommandations appliquées.",
        "applied_preset_log": "Préréglage {} appliqué pour {}",
        "apply_preset_failed_log": "Échec de l'application du préréglage {} : {}",
        "hardware_scan_complete": "Analyse matérielle terminée : mise en cache dans les paramètres globaux.",
        "hardware_scan_failed": "Échec de l'analyse matérielle : {}",
        "scan_error": "✗ Erreur : {}",
        
        # Game Validation
        "invalid_game_installation": "Installation de jeu invalide",
        "game_installation_incomplete": "L'installation de World of Warcraft semble incomplète.\n\nVeuillez lancer le jeu au moins une fois pour initialiser les dossiers Interface et WTF.\n\nAprès avoir lancé le jeu, vous pourrez utiliser cet outil pour nettoyer votre installation.",
        
        # Startup Warning
        "user_disabled_warning": "L'utilisateur a désactivé l'avertissement de démarrage.",
        
        # Update Checker
        "no_updates_available": "Aucune mise à jour disponible",
        "no_releases_published": "Vous utilisez {}.\n\nAucune version n'a encore été publiée.",
        "update_check_failed": "Échec de la vérification de mise à jour",
        "update_check_http_error": "Impossible de vérifier les mises à jour :\n\nHTTP {} : {}",
        "update_check_network_error": "Impossible de vérifier les mises à jour :\n\n{}",
        "update_check_error": "Erreur de vérification de mise à jour",
        "update_check_exception": "Une erreur s'est produite lors de la vérification des mises à jour :\n\n{}",
        "update_available": "Mise à jour disponible",
        "update_available_message": "Une nouvelle version est disponible !\n\nActuelle : {}\nDernière : {}\n\nVisitez la page GitHub pour télécharger la dernière version.",
        "up_to_date": "À jour",
        "up_to_date_message": "Vous utilisez la dernière version ({}).",
        "browser_open_error": "Impossible d'ouvrir le navigateur :\n\n{}",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[Nettoyeur de fichiers] Fichier trouvé : {}",
        "file_cleaner_found": "[Nettoyeur de fichiers] Trouvé : {}",
        "file_cleaner_total_found": "[Nettoyeur de fichiers] Total de fichiers .bak/.old trouvés : {}",
        "file_cleaner_moved_trash": "[Nettoyeur de fichiers] Déplacé vers la corbeille : {}",
        "file_cleaner_deleted": "[Nettoyeur de fichiers] Supprimé : {}",
        "file_cleaner_error_deleting": "[Nettoyeur de fichiers] ERREUR lors de la suppression de {} : {}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[Nettoyeur de dossiers] Trouvé : {}",
        "folder_cleaner_total": "[Nettoyeur de dossiers] Total de dossiers nettoyables : {}",
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
        "version": "Versión:",
        "path": "Ruta:",
        "preview": "Vista previa",
        "toggle_all": "Alternar todo",
        "process_folders": "Procesar carpetas seleccionadas",
        "rebuild_addons": "Reconstruir AddOns.txt",
        "no_orphans_found": "No se encontraron SavedVariables huérfanas.",
        "orphans_found": "{} SavedVariable(s) huérfana(s) encontrada(s).",
        "scan_hardware": "Escanear hardware",
        "system_matches": "Tu sistema coincide con:",
        "optimization_applied": "✓ Optimización aplicada",
        "optimization_not_applied": "⚠ Optimización aún no aplicada",
        "graphics_presets": "Ajustes gráficos predefinidos ({}):",
        "graphics_presets_classic": "Ajustes gráficos predefinidos ({}):",
        "apply_preset": "Aplicar ajuste predefinido:",
        "apply": "Aplicar",
        "preset_applied": "✓ Ajuste predefinido {} aplicado.",
        "error": "✗ Error: {}",
        "low": "Bajo",
        "medium": "Medio",
        "high": "Alto",
        "ultra": "Ultra",
        "manual_suggestions": "Sugerencias de optimización manual",
        "manual_disclaimer": "NOTA: Esta aplicación NO realiza estas optimizaciones automáticamente. Estas son sugerencias manuales para que las implementes.",
        "clean_data_folder": "Limpiar carpeta de datos del juego",
        "clean_data_text": "Si han pasado varios años o múltiples expansiones desde la instalación de World of Warcraft, considera eliminar la carpeta Data de tu directorio principal de World of Warcraft. Esto *podría* reducir el tamaño del juego y mejorar el rendimiento de las pantallas de carga. El lanzador de Battle.net reconstruirá automáticamente esta carpeta cuando sea necesario.",
        "enable_hdr": "Activar HDR (High Dynamic Range)",
        "enable_hdr_text": "Verifica la configuración de pantalla de tu sistema operativo para ver si HDR está disponible. Si tu monitor lo admite, activar HDR puede mejorar significativamente la claridad visual y la profundidad de color en el juego.",
        "verify_refresh": "Verificar frecuencia de actualización del monitor",
        "verify_refresh_text": "Asegúrate de que la frecuencia de actualización de tu monitor esté configurada al valor máximo admitido en la configuración de pantalla de tu sistema operativo. Frecuencias de actualización más altas proporcionan un juego más fluido y mejor capacidad de respuesta.",
        "enable_sam": "Activar Smart Access Memory / Resizable BAR",
        "enable_sam_text": "Verifica la configuración BIOS de tu placa base para Smart Access Memory (AMD) o Resizable BAR (Intel/NVIDIA). Activar esta función permite que tu CPU acceda a la memoria completa de la GPU, mejorando potencialmente el rendimiento.",
        "enable_xmp": "Activar perfil de memoria XMP",
        "enable_xmp_text": "Accede al BIOS de tu placa base y activa la configuración XMP (Extreme Memory Profile) o DOCP/EOCP. Esto asegura que tu RAM funcione a su velocidad nominal en lugar de las velocidades conservadoras predeterminadas, mejorando el rendimiento general del sistema.",
        "export_log": "Exportar registro",
        "clear_log": "Limpiar registro",
        "about_text": "Un conjunto completo de mantenimiento y optimización para World of Warcraft.\nLimpia archivos innecesarios, gestiona addons, optimiza el rendimiento del juego y más.\n\nCierra siempre World of Warcraft antes de ejecutar esta herramienta.",
        "copyright": "Copyright © 2025 Paul Vandersypen. Publicado bajo la Licencia Pública General GNU v3.0 (GPL-3.0-or-later). Consulta el archivo LICENSE incluido para conocer los términos completos.",
        "invalid_folder": "Carpeta inválida",
        "select_valid_wow": "Por favor, selecciona primero una carpeta WoW válida.",
        "no_selection": "Sin selección",
        "no_files_selected": "No se seleccionaron archivos para procesar.",
        "no_folders_selected": "No se seleccionaron carpetas para limpiar.",
        "no_orphans_selected": "No se seleccionaron archivos huérfanos.",
        "confirm": "Confirmar",
        "confirm_action": "¿Estás seguro de que quieres {} {} {}?",
        "file_s": "archivo(s)",
        "folder_s": "carpeta(s)",
        "orphaned_savedvars": "SavedVariables huérfanas",
        "completed": "Completado",
        "processed": "{} {} procesado(s).",
        "send2trash_missing": "send2trash falta",
        "send2trash_unavailable": "El módulo 'send2trash' no está disponible. Los archivos se eliminaron permanentemente.",
        "send2trash_install": "El paquete 'send2trash' no está instalado.\nPara habilitar el soporte de papelera de reciclaje, instálalo manualmente:\n\n  pip install send2trash\n\no:\n\n  python -m pip install --user send2trash",
        "restore_defaults_confirm": "¿Restaurar toda la configuración a los valores predeterminados?",
        "restart_required": "Configuración restaurada. La aplicación se reiniciará ahora.",
        "error_title": "Error",
        "restore_error": "Error al restaurar los valores predeterminados: {}",
        "confirm_font": "Confirmar fuente",
        "apply_font_confirm": "¿Aplicar la fuente '{}' a la aplicación?",
        "select_font": "Seleccionar fuente",
        "export_log_title": "Exportar registro",
        "log_empty": "El registro está vacío. Nada que exportar.",
        "log_exported": "Registro exportado con éxito a:\n{}",
        "export_error": "Error de exportación",
        "export_failed": "Error al exportar el registro:\n{}",
        "addons_rebuilt": "Entradas de AddOns.txt reconstruidas.\nTotal escrito: {}\nTotal eliminado: {}",
        "session_started": "Sesión iniciada — {}",
        "file_scan": "Escaneo del limpiador de archivos: {} coincidencia(s).",
        "orphan_scan": "Escaneo del limpiador de huérfanos: {} huérfano(s).",
        "file_processed": "Limpiador de archivos: {} archivo(s) procesado(s).",
        "folder_processed": "Limpiador de carpetas: {} carpeta(s) procesada(s).",
        "orphan_processed": "Limpiador de huérfanos: {} huérfano(s) procesado(s).",
        "send2trash_warning": "Advertencia: send2trash no instalado; las eliminaciones fueron permanentes.",
        "addons_txt_log": "[AddOns.txt] {}: {} entradas escritas, {} eliminadas",
        "preset_applied_log": "Ajuste predefinido {} aplicado para {}",
        "preset_failed_log": "Error al aplicar el ajuste predefinido {}: {}",
        "language_changed": "Idioma cambiado",
        "language_changed_restart": "El idioma ha sido cambiado. Por favor, reinicia la aplicación para que todos los cambios surtan efecto.",
        "apply": "Aplicar",
        "cancel": "Cancelar",
        "scan_bak_old": "Buscar archivos .bak / .old",
        "expand_all": "Expandir todo",
        "collapse_all": "Contraer todo",
        "select_deselect_all": "Seleccionar / Deseleccionar todo",
        "process_selected_files": "Procesar archivos seleccionados",
        "scan_orphaned": "Buscar SavedVariables huérfanas",
        "process_selected_folders": "Procesar carpetas seleccionadas",
        "select_deselect_all_folders": "Seleccionar / Deseleccionar todas las carpetas",
        "select_deselect_all_screenshots": "Seleccionar / Deseleccionar todas las capturas de pantalla",
        "screenshots_per_file": "Capturas de pantalla (acciones por archivo)",
        "check_for_updates": "Buscar actualizaciones",
        "game_optimizer_title": "Optimizador de juego",
        "game_optimizer_desc": "Optimiza el rendimiento de World of Warcraft según la configuración de tu hardware.",
        "scan_hardware": "Escanear hardware",
        "click_scan_hardware": "Haz clic en 'Escanear hardware' para detectar las capacidades de tu sistema.",
        "select_valid_wow_folder": "Selecciona una carpeta válida de World of Warcraft en Opciones para habilitar las vistas por versión.",
        "recommended_settings": "Configuración recomendada:",
        "apply_preset_label": "Aplicar ajuste predefinido:",
        "apply_recommended_settings": "Aplicar configuración recomendada",
        "scanning_cpu": "Escaneando CPU...",
        "scanning_ram": "Escaneando RAM... (CPU: {}C/{}T detectada)",
        "scanning_gpu": "Escaneando GPU... (RAM: {} GB detectada)",
        "important_notice": "Aviso importante",
        "startup_warning_text": "⚠️ Asegúrate de que World of Warcraft esté completamente cerrado antes de usar esta herramienta.\n\nEjecutar la herramienta mientras WoW está abierto podría interferir con los archivos del juego.",
        "do_not_show_again": "No mostrar este aviso de nuevo",
        "ok": "Aceptar",
        "select_valid_wow_folder_cleaner": "Selecciona una carpeta válida de World of Warcraft en Opciones para habilitar el limpiador de carpetas.",
        "preview_label": "Vista previa",
        "screenshots_not_found": "Carpeta de capturas de pantalla no encontrada para esta versión.",
        
        # Main UI - Buttons and Messages
        "apply": "Aplicar",
        "cancel": "Cancelar",
        "export_log": "Exportar registro",
        "clear_log": "Limpiar registro",
        "confirm_font_change": "Confirmación de cambio de fuente",
        "font_change_restart_required": "El cambio de fuente requiere reiniciar la aplicación.\n¿Quieres reiniciar ahora?",
        "restart": "Reiniciar",
        "later": "Más tarde",
        "confirm_language_change": "Confirmar cambio de idioma",
        "language_change_restart_required": "El cambio de idioma requiere reiniciar la aplicación para que surta efecto.\n\n¿Quieres reiniciar ahora?",
        "language_change_restart_message": "Por favor, reinicia la aplicación para que el cambio de idioma surta efecto.",
        "invalid_folder_title": "Carpeta inválida",
        
        # Common Messages
        "invalid_folder_select_valid_wow": "Por favor, selecciona una carpeta válida de World of Warcraft en Opciones.",
        "scanning_files": "Escaneando archivos...",
        "scanning_folders": "Escaneando carpetas...",
        "scanning_orphans": "Escaneando AddOns huérfanos...",
        "no_files_selected": "No se seleccionaron archivos",
        "no_folders_selected": "No se seleccionaron carpetas",
        "no_orphans_selected": "No se seleccionaron huérfanos",
        
        # File Cleaner
        "select_files_to_delete": "Por favor, selecciona al menos un archivo para eliminar.",
        "confirm_delete_files_title": "Confirmar eliminación de archivos",
        "confirm_delete_files_message": "¿Estás seguro de que quieres eliminar {0} archivo(s)?",
        "files_moved_to_recycle_bin": "{0} archivo(s) movido(s) a la Papelera de reciclaje.",
        "files_deletion_complete": "{0} archivo(s) eliminado(s) con éxito.",
        
        # Folder Cleaner
        "select_folders_to_delete": "Por favor, selecciona al menos una carpeta para eliminar.",
        "confirm_delete_folders_title": "Confirmar eliminación de carpetas",
        "confirm_delete_folders_message": "¿Estás seguro de que quieres eliminar {0} carpeta(s)?",
        
        # Orphan Cleaner
        "select_orphans_to_delete": "Por favor, selecciona al menos un AddOn huérfano para eliminar.",
        "confirm_delete_orphans_title": "Confirmar eliminación de huérfanos",
        "confirm_delete_orphans_message": "¿Estás seguro de que quieres eliminar {0} AddOn(s) huérfano(s)?\n\nEsto también eliminará todos los archivos SavedVariables asociados.",
        "orphans_moved_to_recycle_bin": "{0} AddOn(s) huérfano(s) movido(s) a la Papelera de reciclaje.",
        "orphans_deletion_complete": "{0} AddOn(s) huérfano(s) eliminado(s) con éxito.",
        
        # Actions
        "folders_moved_to_recycle_bin": "{0} carpeta(s) movida(s) a la Papelera de reciclaje.",
        "folders_deletion_complete": "{0} carpeta(s) eliminada(s) con éxito.",
        
        # send2trash Warnings
        "send2trash_not_available_files": "send2trash no está disponible. Los archivos se eliminarán permanentemente.",
        "send2trash_not_available_folders": "send2trash no está disponible. Las carpetas se eliminarán permanentemente.",
        "send2trash_not_available_orphans": "send2trash no está disponible. Los AddOns huérfanos se eliminarán permanentemente.",
        
        # AddOns.txt Rebuild
        "addons_txt_rebuild_summary": "¡AddOns.txt reconstruido con éxito!\n\nAddOns encontrados: {0}\nPersonajes: {1}\nArchivos de configuración: {2}",
        
        # Log Export
        "log_export_empty": "El registro está vacío. No hay nada que exportar.",
        
        # Settings Restore
        "settings_restored_title": "Configuración restaurada",
        "settings_restored_to_defaults": "Configuración restaurada a los valores predeterminados.",
        "settings_restored_restart_required": "Configuración restaurada a los valores predeterminados.\nPor favor, reinicia la aplicación para que todos los cambios surtan efecto.",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "Sugerencias de optimización manual",
        "opt_sug_disclaimer": "NOTA: Esta aplicación NO realiza estas optimizaciones automáticamente. Son sugerencias manuales para que las implementes.",
        "opt_sug_clean_data_title": "Limpiar carpeta de datos del juego",
        "opt_sug_clean_data_text": "Si han pasado varios años o expansiones desde la instalación de World of Warcraft, considera eliminar la carpeta Data de tu directorio principal de World of Warcraft. Esto *podría* reducir el tamaño del juego y mejorar el rendimiento de la pantalla de carga. Battle.net reconstruirá automáticamente esta carpeta.",
        "opt_sug_clean_data_tooltip": "POR QUÉ: La carpeta Data acumula recursos temporales y en caché con el tiempo. Eliminarla fuerza una descarga fresca de archivos optimizados.\n\nNIVEL DE RIESGO: Seguro - Battle.net volverá a descargar automáticamente los archivos necesarios.\n\nBENEFICIO ESPERADO: Pantallas de carga más rápidas, uso reducido del disco (potencialmente 10-20 GB ahorrados).",
        "opt_sug_hdr_title": "Activar HDR (High Dynamic Range)",
        "opt_sug_hdr_text": "Verifica la configuración de pantalla de tu sistema operativo para ver si HDR está disponible. Si tu monitor lo admite, activar HDR puede mejorar significativamente la claridad visual y la profundidad de color en el juego.",
        "opt_sug_hdr_tooltip": "POR QUÉ: HDR proporciona una gama de colores más amplia y mejor contraste, haciendo que los visuales sean más vibrantes y realistas.\n\nNIVEL DE RIESGO: Seguro - Se puede activar/desactivar fácilmente en la configuración del sistema.\n\nBENEFICIO ESPERADO: Calidad visual dramáticamente mejorada si el monitor admite HDR10 o mejor.\n\nREQUISITO: Monitor compatible con HDR y Windows 10/11 o macOS Catalina+.",
        "opt_sug_refresh_title": "Verificar frecuencia de actualización del monitor",
        "opt_sug_refresh_text": "Asegúrate de que la frecuencia de actualización de tu monitor esté configurada al valor máximo admitido en la configuración de pantalla. Frecuencias más altas proporcionan un juego más fluido y mejor capacidad de respuesta.",
        "opt_sug_refresh_tooltip": "POR QUÉ: Muchos sistemas usan 60Hz por defecto incluso cuando los monitores admiten 120Hz/144Hz/165Hz. Esto limita innecesariamente tu tasa de fotogramas.\n\nNIVEL DE RIESGO: Seguro - Sin riesgo de hardware, fácilmente reversible.\n\nBENEFICIO ESPERADO: Juego más fluido, latencia de entrada reducida, mejores tiempos de reacción.\n\nCÓMO VERIFICAR: Windows: Configuración > Pantalla > Avanzado > Frecuencia de actualización\nmacOS: Preferencias del Sistema > Pantallas",
        "opt_sug_sam_title": "Activar Smart Access Memory / Resizable BAR",
        "opt_sug_sam_text": "Verifica la configuración BIOS de tu placa base para Smart Access Memory (AMD) o Resizable BAR (Intel/NVIDIA). Activar esta función permite que tu CPU acceda a la memoria completa de la GPU, mejorando potencialmente el rendimiento.",
        "opt_sug_sam_tooltip": "POR QUÉ: Permite que la CPU acceda a toda la memoria de la GPU de una vez en lugar de pequeños fragmentos de 256MB, reduciendo cuellos de botella.\n\nNIVEL DE RIESGO: Moderado - Requiere cambios en BIOS. Documenta la configuración actual primero.\n\nBENEFICIO ESPERADO: Mejora del 5-15% en FPS en escenarios intensivos de GPU.\n\nREQUISITOS:\n• AMD: CPU Ryzen 5000+ + GPU RX 6000+\n• Intel: CPU 10ª gen+ + GPU RTX 3000+\n• Actualización de BIOS puede ser necesaria",
        "opt_sug_xmp_title": "Activar perfil de memoria XMP",
        "opt_sug_xmp_text": "Accede al BIOS de tu placa base y activa la configuración XMP (Extreme Memory Profile) o DOCP/EOCP. Esto asegura que tu RAM funcione a su velocidad nominal en lugar de velocidades conservadoras predeterminadas.",
        "opt_sug_xmp_tooltip": "POR QUÉ: La RAM normalmente funciona a 2133MHz por defecto incluso si está clasificada para 3200MHz+. XMP habilita las velocidades anunciadas.\n\nNIVEL DE RIESGO: Moderado - Cambio de BIOS. El sistema puede no arrancar si la RAM es inestable (fácil de restablecer).\n\nBENEFICIO ESPERADO: Aumento del 10-20% en rendimiento de CPU, tiempos de carga más rápidos, mejores 1% lows.\n\nCÓMO HABILITAR: Entrar al BIOS (normalmente Supr/F2 al iniciar) > Encontrar configuración XMP/DOCP > Habilitar > Guardar y salir",
        
        # Help/About tab - content
        "help_version_label": "Herramienta de limpieza de WoW {}",
        "help_about_description": "Un conjunto completo de mantenimiento y optimización para World of Warcraft.\nLimpia archivos innecesarios, gestiona addons, optimiza el rendimiento del juego y más.\n\nCierra siempre World of Warcraft antes de ejecutar esta herramienta.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Publicado bajo la Licencia Pública General GNU v3.0 (GPL-3.0-or-later). Consulta el archivo LICENSE incluido para conocer los términos completos.",
        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU: {} | RAM: {} | GPU: {}",
        "gpu_switch_notification": "⚠ Cambio de GPU: Configurado para usar '{}' en lugar de '{}'. Este cambio optimiza el rendimiento usando tu GPU dedicada para una mejor experiencia de juego. Es seguro y recomendado.",
        "scan_tooltip_refresh": "Escanear nuevamente no es necesario a menos que hayas cambiado tu CPU, GPU o RAM.\nHaz clic para actualizar la información de hardware en caché.",
        "scanning_ram_detected": "Escaneando RAM... (CPU: {}C/{}T detectada)",
        "scanning_gpu_detected": "Escaneando GPU... (RAM: {} GB detectada)",
        "apply_preset_label": "Aplicar ajuste predefinido:",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "World of Warcraft en ejecución",
        "wow_running_message": "World of Warcraft está actualmente en ejecución. Los cambios se aplicarán después de reiniciar el juego.\n\n¿Deseas continuar?",
        "permission_error_title": "Error de permisos",
        "permission_error_message": "Config.wtf está en modo de solo lectura. Por favor, elimina el atributo de solo lectura e inténtalo de nuevo.",
        "config_readonly_status": "✗ Config.wtf está en solo lectura.",
        "confirm_apply_title": "Confirmar aplicación",
        "confirm_apply_message": "¿Aplicar ajuste predefinido {} a {}?\n\nEsto modificará {} configuraciones gráficas en Config.wtf.\nSe creará una copia de seguridad automáticamente.\n\nCambios principales:\n• Ajuste: {} configuraciones de calidad\n• Rendimiento: {} optimización(es)",
        "cancelled_by_user": "Cancelado por el usuario.",
        "settings_applied_status": "✓ {} configuraciones aplicadas.",
        "preset_applied_status": "✓ Ajuste predefinido {} aplicado.",
        "apply_error_status": "✗ Error: {}",
        
        # Preset tooltips
        "preset_tooltip_template": "Ajuste predefinido {}\n\nRendimiento esperado:\n{}\n\nHaz clic en 'Aplicar' abajo para usar este ajuste.",
        "perf_depends_hardware": "El impacto en el rendimiento depende de tu hardware.",
        "perf_will_vary": "El rendimiento variará",
        
        # Low preset performance estimates
        "low_perf_high": "Excelente rendimiento (100+ FPS en la mayoría de escenarios)",
        "low_perf_mid": "Muy buen rendimiento (80-120 FPS)",
        "low_perf_low": "Buen rendimiento (60-80 FPS)",
        
        # Medium preset performance estimates
        "medium_perf_high": "Excelente rendimiento (90-120 FPS)",
        "medium_perf_mid": "Buen rendimiento (60-90 FPS)",
        "medium_perf_low": "Rendimiento moderado (45-60 FPS)",
        
        # High preset performance estimates
        "high_perf_high": "Muy buen rendimiento (70-100 FPS)",
        "high_perf_mid": "Buen rendimiento (50-70 FPS)",
        "high_perf_low": "Puede tener dificultades en bandas (30-50 FPS)",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "Buen rendimiento (60-80 FPS)",
        "ultra_perf_mid": "Rendimiento moderado (40-60 FPS)",
        "ultra_perf_low": "Bajo rendimiento (20-40 FPS)",
        
        # WoW version names
        "version_retail": "Retail",
        "version_classic": "Classic",
        "version_classic_era": "Classic Era",
        "version_ptr": "PTR",
        "version_beta": "Beta",
        
        # Game Optimizer - additional strings
        "not_detected": "No detectado",
        "unknown_cpu": "CPU desconocida",
        "unknown_gpu": "Desconocido",
        "not_set": "No establecido",
        "hover_for_details": "Pase el cursor para ver detalles",
        "new_setting_prefix": "[NUEVO] ",
        "details_colon": "Detalles:",
        "updated_settings": "• {0} configuraciones existentes actualizadas",
        "added_settings": "• {0} nuevas configuraciones añadidas",
        "select_valid_wow_optimizer": "Selecciona una carpeta válida de World of Warcraft en Opciones para habilitar las vistas por versión.",
        "wtf_not_found": "Directorio WTF no encontrado. Por favor, inicia el juego primero.",
        "unknown_preset": "Ajuste predefinido desconocido: {}",
        "backup_failed": "Error al crear copia de seguridad: {}",
        "config_write_failed": "Error al escribir configuración: {}",
        "config_updated": "Configuraciones {} aplicadas a Config.wtf. ",
        "settings_updated_added": "{} configuraciones actualizadas, {} nuevas configuraciones añadidas.",
        "backup_saved": " Copia de seguridad guardada.",
        "version_path": "Versión: {}\nRuta: {}",
        "optimizer_launch_required": "El optimizador requiere que {} haya sido iniciado al menos una vez. Por favor, inicia World of Warcraft y ve a la pantalla de selección de personajes, luego cierra el juego. Después de eso, puedes usar el optimizador para aplicar ajustes predefinidos gráficos.",
        "system_matches": "Tu sistema coincide con: {}",
        "optimizer_title": "Optimizador — {}",
        "recommendations_applied": "✓ Recomendaciones aplicadas.",
        "applied_preset_log": "Ajuste predefinido {} aplicado para {}",
        "apply_preset_failed_log": "Error al aplicar ajuste predefinido {}: {}",
        "hardware_scan_complete": "Escaneo de hardware completo: almacenado en caché en configuración global.",
        "hardware_scan_failed": "Error en escaneo de hardware: {}",
        "scan_error": "✗ Error: {}",
        
        # Game Validation
        "invalid_game_installation": "Instalación de juego no válida",
        "game_installation_incomplete": "La instalación de World of Warcraft parece incompleta.\n\nPor favor, ejecuta el juego al menos una vez para inicializar las carpetas Interface y WTF.\n\nDespués de ejecutar el juego, puedes usar esta herramienta para limpiar tu instalación.",
        
        # Startup Warning
        "user_disabled_warning": "El usuario desactivó la advertencia de inicio.",
        
        # Update Checker
        "no_updates_available": "No hay actualizaciones disponibles",
        "no_releases_published": "Estás usando {}.\n\nAún no se han publicado versiones.",
        "update_check_failed": "Verificación de actualización fallida",
        "update_check_http_error": "No se pudo verificar actualizaciones:\n\nHTTP {}: {}",
        "update_check_network_error": "No se pudo verificar actualizaciones:\n\n{}",
        "update_check_error": "Error de verificación de actualización",
        "update_check_exception": "Ocurrió un error al verificar actualizaciones:\n\n{}",
        "update_available": "Actualización disponible",
        "update_available_message": "¡Hay una nueva versión disponible!\n\nActual: {}\nÚltima: {}\n\nVisita la página de GitHub para descargar la última versión.",
        "up_to_date": "Actualizado",
        "up_to_date_message": "Estás usando la última versión ({}).",
        "browser_open_error": "No se pudo abrir el navegador:\n\n{}",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[Limpiador de archivos] Archivo encontrado: {}",
        "file_cleaner_found": "[Limpiador de archivos] Encontrado: {}",
        "file_cleaner_total_found": "[Limpiador de archivos] Total de archivos .bak/.old encontrados: {}",
        "file_cleaner_moved_trash": "[Limpiador de archivos] Movido a la papelera: {}",
        "file_cleaner_deleted": "[Limpiador de archivos] Eliminado: {}",
        "file_cleaner_error_deleting": "[Limpiador de archivos] ERROR al eliminar {}: {}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[Limpiador de carpetas] Encontrado: {}",
        "folder_cleaner_total": "[Limpiador de carpetas] Total de carpetas limpiables: {}",
        
        # Orphan Cleaner - Log messages
        "orphan_found_in": "[Limpiador de huérfanos] Encontrado huérfano en {}: {}",
        "orphan_total_found": "[Limpiador de huérfanos] Total de SavedVariables huérfanos: {}",
        "orphan_moved_trash": "[Limpiador de huérfanos] Movido a papelera: {}",
        "orphan_deleted": "[Limpiador de huérfanos] Eliminado: {}",
        "orphan_error_deleting": "[Limpiador de huérfanos] ERROR al eliminar {}: {}",
        "orphan_rebuilt_addons": "[Limpiador de huérfanos] Reconstruido: {}",
        "orphan_error_writing_addons": "[Limpiador de huérfanos] ERROR al escribir AddOns.txt {}: {}",
        "orphan_error_rebuild": "[Limpiador de huérfanos] ERROR durante la reconstrucción de AddOns.txt: {}",
        
        # Path Manager
        "select_wow_folder_title": "Seleccionar carpeta de World of Warcraft",
        "unrecognized_installation": "Instalación no reconocida",
        "folder_not_valid_continue": "La carpeta seleccionada no parece válida.\n\n¿Continuar de todos modos?",
        "wow_folder_set": "Carpeta de WoW establecida: {}",
        
        # Performance
        "performance_execution_time": "[Rendimiento] {} tardó {:.3f}s",
        "perf_moved_trash": "[{}] Movido a papelera: {}",
        "perf_deleted": "[{}] Eliminado: {}",
        "perf_error_deleting": "[{}] ERROR al eliminar {}: {}",
        
        "select_valid_wow_folder_cleaner": "Selecciona una carpeta válida de World of Warcraft en Opciones para habilitar el Limpiador de carpetas.",
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "Busca en todas las versiones de WoW detectadas las SavedVariables de addons (.lua / .lua.bak) que no tienen un addon instalado correspondiente (Interface/AddOns). Escanea las carpetas SavedVariables de cuenta, reino y personaje. El procesamiento también reconstruye AddOns.txt para que coincida con los addons instalados (preservando habilitado/deshabilitado cuando sea posible).",
        "orphan_description_part2": "Nota: Los archivos Blizzard_*.lua son datos básicos del juego y se ignoran automáticamente por seguridad (pero sus copias de seguridad .lua.bak pueden eliminarse).",
    },
    
    "esMX": {
        # Window title
        "window_title": "Herramienta de Limpieza de WoW",
        
        # Menu/Tab names
        "file_cleaner": "Limpiador de Archivos",
        "folder_cleaner": "Limpiador de Carpetas",
        "orphan_cleaner": "Limpiador de Huérfanos",
        "game_optimizer": "Optimizador de Juego",
        "optimization_suggestions": "Sugerencias de Optimización",
        "log": "Registro",
        "help_about": "Ayuda / Acerca de",
        
        # Options section
        "options": "Opciones",
        "wow_folder": "Carpeta de World of Warcraft:",
        "browse": "Explorar...",
        "browse_tooltip": "Buscar tu carpeta de World of Warcraft.",
        "font_size": "Tamaño de Fuente:",
        "font": "Fuente:",
        "theme": "Tema:",
        "language": "Idioma:",
        "file_action": "Acción de Archivo:",
        "delete_permanently": "Eliminar Permanentemente",
        "move_to_recycle": "Mover a la Papelera de Reciclaje",
        "enable_verbose": "Habilitar registro detallado",
        "verbose_tooltip": "Cuando está habilitado, el Registro captura cada archivo/carpeta/línea de AddOns.txt procesado.",
        "external_log": "Registro Externo:",
        "fresh": "Nuevo",
        "fresh_tooltip": "Crear un archivo de registro nuevo en cada exportación (sobrescribe el existente).",
        "append": "Agregar",
        "append_tooltip": "Agregar cada exportación al archivo de registro existente (mantiene hasta 10-20 sesiones según el detalle).",
        "check_updates": "Buscar actualizaciones",
        "check_updates_tooltip": "Cuando está habilitado, buscar nuevas versiones en GitHub al iniciar.",
        "restore_defaults": "Restaurar Predeterminados",
        "light": "claro",
        "dark": "oscuro",
        
        # File Cleaner
        "scan": "Escanear",
        "select_all": "Seleccionar Todo",
        "expand_all": "Expandir Todo",
        "collapse_all": "Contraer Todo",
        "process_selected": "Procesar Seleccionados",
        "scanning": "Escaneando…",
        "no_bak_old_found": "No se encontraron archivos .bak o .old.",
        "files_found": "{} archivo(s) encontrado(s).",
        
        # Folder Cleaner
        "version": "Versión:",
        "path": "Ruta:",
        "preview": "Vista Previa",
        "toggle_all": "Alternar Todo",
        "process_folders": "Procesar Carpetas Seleccionadas",
        
        # Orphan Cleaner
        "rebuild_addons": "Reconstruir AddOns.txt",
        "no_orphans_found": "No se encontraron SavedVariables huérfanos.",
        "orphans_found": "Se encontraron {} SavedVariable(s) huérfano(s).",
        
        # Game Optimizer
        "scan_hardware": "Escanear Hardware",
        "system_matches": "Tu sistema coincide con:",
        "optimization_applied": "✓ Optimización aplicada",
        "optimization_not_applied": "⚠ Optimización aún no aplicada",
        "graphics_presets": "Ajustes Predefinidos Gráficos ({}):",
        "graphics_presets_classic": "Ajustes Predefinidos Gráficos ({}):",
        "apply_preset": "Aplicar Ajuste:",
        "apply": "Aplicar",
        "preset_applied": "✓ Ajuste {} aplicado.",
        "error": "✗ Error: {}",
        "low": "Bajo",
        "medium": "Medio",
        "high": "Alto",
        "ultra": "Ultra",
        
        # Optimization Suggestions
        "manual_suggestions": "Sugerencias de Optimización Manual",
        "manual_disclaimer": "NOTA: Esta aplicación NO realiza estas optimizaciones automáticamente. Estas son sugerencias manuales para que las implementes.",
        "clean_data_folder": "Limpiar Carpeta de Datos del Juego",
        "clean_data_text": "Si han pasado varios años o múltiples expansiones desde la instalación de World of Warcraft, considera eliminar la carpeta Data de tu directorio principal de World of Warcraft. Esto *podría* reducir el tamaño del juego y mejorar el rendimiento de las pantallas de carga. El lanzador de Battle.net reconstruirá automáticamente esta carpeta cuando sea necesario.",
        "enable_hdr": "Habilitar HDR (Alto Rango Dinámico)",
        "enable_hdr_text": "Verifica la configuración de pantalla de tu sistema operativo para ver si HDR está disponible. Si tu monitor lo soporta, habilitar HDR puede mejorar significativamente la claridad visual y la profundidad de color en el juego.",
        "verify_refresh": "Verificar Tasa de Refresco del Monitor",
        "verify_refresh_text": "Asegúrate de que la tasa de refresco de tu monitor esté configurada al valor máximo soportado en la configuración de pantalla de tu sistema operativo. Tasas de refresco más altas proporcionan un juego más fluido y mejor capacidad de respuesta.",
        "enable_sam": "Habilitar Smart Access Memory / Resizable BAR",
        "enable_sam_text": "Verifica la configuración del BIOS de tu placa madre para Smart Access Memory (AMD) o Resizable BAR (Intel/NVIDIA). Habilitar esta función permite que tu CPU acceda a toda la memoria GPU, mejorando potencialmente el rendimiento.",
        "enable_xmp": "Habilitar Perfil de Memoria XMP",
        "enable_xmp_text": "Accede al BIOS de tu placa madre y habilita la configuración XMP (Extreme Memory Profile) o DOCP/EOCP. Esto asegura que tu RAM funcione a su velocidad nominal en lugar de velocidades conservadoras predeterminadas, mejorando el rendimiento general del sistema.",
        
        # Log tab
        "export_log": "Exportar Registro",
        "clear_log": "Limpiar Registro",
        
        # Help/About
        "about_text": "Un conjunto completo de mantenimiento y optimización para World of Warcraft.\nLimpia archivos innecesarios, administra addons, optimiza el rendimiento del juego y más.\n\nSiempre cierra World of Warcraft antes de usar esta herramienta.",
        "copyright": "Copyright © 2025 Paul Vandersypen. Publicado bajo la Licencia Pública General GNU v3.0 (GPL-3.0-or-later). Consulta el archivo LICENSE incluido para los términos completos.",
        
        # Dialogs
        "invalid_folder": "Carpeta Inválida",
        "select_valid_wow": "Por favor, selecciona primero una carpeta válida de WoW.",
        "no_selection": "Sin Selección",
        "no_files_selected": "No se seleccionaron archivos para procesar.",
        "no_folders_selected": "No se seleccionaron carpetas para limpiar.",
        "no_orphans_selected": "No se seleccionaron archivos huérfanos.",
        "confirm": "Confirmar",
        "confirm_action": "¿Estás seguro de que quieres {} {} {}?",
        "file_s": "archivo(s)",
        "folder_s": "carpeta(s)",
        "orphaned_savedvars": "SavedVariables huérfanos",
        "completed": "Completado",
        "processed": "Procesados {} {}.",
        "send2trash_missing": "send2trash faltante",
        "send2trash_unavailable": "El módulo 'send2trash' no está disponible. Los archivos se eliminaron permanentemente.",
        "send2trash_install": "El paquete 'send2trash' no está instalado.\nPara habilitar el soporte de Papelera de Reciclaje, instálalo manualmente:\n\n  pip install send2trash\n\no:\n\n  python -m pip install --user send2trash",
        "restore_defaults_confirm": "¿Restaurar toda la configuración a los valores predeterminados?",
        "restart_required": "Configuración restaurada. La aplicación se reiniciará ahora.",
        "error_title": "Error",
        "restore_error": "Error al restaurar predeterminados: {}",
        "confirm_font": "Confirmar Fuente",
        "apply_font_confirm": "¿Aplicar la fuente '{}' a la aplicación?",
        "select_font": "Seleccionar Fuente",
        "export_log_title": "Exportar Registro",
        "log_empty": "El registro está vacío. No hay nada que exportar.",
        "log_exported": "Registro exportado exitosamente a:\n{}",
        "export_error": "Error de Exportación",
        "export_failed": "Error al exportar el registro:\n{}",
        "addons_rebuilt": "Entradas de AddOns.txt reconstruidas.\nTotal escrito: {}\nTotal eliminado: {}",
        
        # Log messages
        "session_started": "Sesión iniciada — {}",
        "file_scan": "Escaneo del Limpiador de Archivos: {} coincidencia(s).",
        "orphan_scan": "Escaneo del Limpiador de Huérfanos: {} huérfano(s).",
        "file_processed": "Limpiador de Archivos: procesados {} archivo(s).",
        "folder_processed": "Limpiador de Carpetas: procesadas {} carpeta(s).",
        "orphan_processed": "Limpiador de Huérfanos: procesados {} huérfano(s).",
        "send2trash_warning": "Advertencia: send2trash no instalado; las eliminaciones fueron permanentes.",
        "addons_txt_log": "[AddOns.txt] {}: escribió {} entradas, eliminó {}",
        "preset_applied_log": "Aplicado ajuste {} para {}",
        "preset_failed_log": "Error al aplicar ajuste {}: {}",
        
        # Language change
        "language_changed": "Idioma Cambiado",
        "language_changed_restart": "El idioma ha sido cambiado. Por favor, reinicia la aplicación para que todos los cambios tengan efecto.",
        
        # Additional buttons and UI elements
        "apply": "Aplicar",
        "cancel": "Cancelar",
        "scan_bak_old": "Escanear Archivos .bak / .old",
        "expand_all": "Expandir Todo",
        "collapse_all": "Contraer Todo",
        "select_deselect_all": "Seleccionar / Deseleccionar Todo",
        "process_selected_files": "Procesar Archivos Seleccionados",
        "scan_orphaned": "Escanear SavedVariables Huérfanos",
        "process_selected_folders": "Procesar Carpetas Seleccionadas",
        "select_deselect_all_folders": "Seleccionar / Deseleccionar Todas las Carpetas",
        "select_deselect_all_screenshots": "Seleccionar / Deseleccionar Todas las Capturas de Pantalla",
        "screenshots_per_file": "Capturas de Pantalla (acciones por archivo)",
        "check_for_updates": "Buscar Actualizaciones",
        
        # Game Optimizer
        "game_optimizer_title": "Optimizador de Juego",
        "game_optimizer_desc": "Optimiza el rendimiento de World of Warcraft basándose en tu configuración de hardware.",
        "scan_hardware": "Escanear Hardware",
        "click_scan_hardware": "Haz clic en 'Escanear Hardware' para detectar las capacidades de tu sistema.",
        "select_valid_wow_folder": "Selecciona una carpeta válida de World of Warcraft en Opciones para habilitar las vistas por versión.",
        "recommended_settings": "Configuraciones Recomendadas:",
        "apply_preset_label": "Aplicar Ajuste:",
        "apply_recommended_settings": "Aplicar Configuraciones Recomendadas",
        "scanning_cpu": "Escaneando CPU...",
        "scanning_ram": "Escaneando RAM... (CPU: {}C/{}T detectada)",
        "scanning_gpu": "Escaneando GPU... (RAM: {} GB detectada)",
        
        # Startup warning
        "important_notice": "Aviso Importante",
        "startup_warning_text": "⚠️ Por favor, asegúrate de que World of Warcraft esté completamente cerrado antes de usar esta herramienta.\n\nEjecutar la herramienta mientras WoW está abierto podría interferir con los archivos del juego.",
        "do_not_show_again": "No mostrar esta advertencia de nuevo",
        "ok": "OK",
        
        # Folder cleaner
        "select_valid_wow_folder_cleaner": "Selecciona una carpeta válida de World of Warcraft en Opciones para habilitar el Limpiador de Carpetas.",
        "preview_label": "Vista Previa",
        "screenshots_not_found": "Carpeta de Capturas de Pantalla no encontrada para esta versión.",
        
        # Main UI - Buttons and Messages
        "apply": "Aplicar",
        "cancel": "Cancelar",
        "export_log": "Exportar Registro",
        "clear_log": "Limpiar Registro",
        "confirm_font_change": "Confirmación de Cambio de Fuente",
        "font_change_restart_required": "El cambio de fuente requiere reiniciar la aplicación.\n¿Quieres reiniciar ahora?",
        "restart": "Reiniciar",
        "later": "Más Tarde",
        "confirm_language_change": "Confirmar Cambio de Idioma",
        "language_change_restart_required": "El cambio de idioma requiere reiniciar la aplicación para que surta efecto.\n\n¿Quieres reiniciar ahora?",
        "language_change_restart_message": "Por favor, reinicia la aplicación para que el cambio de idioma surta efecto.",
        "invalid_folder_title": "Carpeta Inválida",
        
        # Common Messages
        "invalid_folder_select_valid_wow": "Por favor, selecciona una carpeta válida de World of Warcraft en Opciones.",
        "scanning_files": "Escaneando archivos...",
        "scanning_folders": "Escaneando carpetas...",
        "scanning_orphans": "Escaneando AddOns huérfanos...",
        "no_files_selected": "No se seleccionaron archivos",
        "no_folders_selected": "No se seleccionaron carpetas",
        "no_orphans_selected": "No se seleccionaron huérfanos",
        
        # File Cleaner
        "select_files_to_delete": "Por favor, selecciona al menos un archivo para eliminar.",
        "confirm_delete_files_title": "Confirmar Eliminación de Archivos",
        "confirm_delete_files_message": "¿Estás seguro de que quieres eliminar {0} archivo(s)?",
        "files_moved_to_recycle_bin": "{0} archivo(s) movido(s) a la Papelera de Reciclaje.",
        "files_deletion_complete": "{0} archivo(s) eliminado(s) con éxito.",
        
        # Folder Cleaner
        "select_folders_to_delete": "Por favor, selecciona al menos una carpeta para eliminar.",
        "confirm_delete_folders_title": "Confirmar Eliminación de Carpetas",
        "confirm_delete_folders_message": "¿Estás seguro de que quieres eliminar {0} carpeta(s)?",
        
        # Orphan Cleaner
        "select_orphans_to_delete": "Por favor, selecciona al menos un AddOn huérfano para eliminar.",
        "confirm_delete_orphans_title": "Confirmar Eliminación de Huérfanos",
        "confirm_delete_orphans_message": "¿Estás seguro de que quieres eliminar {0} AddOn(s) huérfano(s)?\n\nEsto también eliminará todos los archivos SavedVariables asociados.",
        "orphans_moved_to_recycle_bin": "{0} AddOn(s) huérfano(s) movido(s) a la Papelera de Reciclaje.",
        "orphans_deletion_complete": "{0} AddOn(s) huérfano(s) eliminado(s) con éxito.",
        
        # Actions
        "folders_moved_to_recycle_bin": "{0} carpeta(s) movida(s) a la Papelera de Reciclaje.",
        "folders_deletion_complete": "{0} carpeta(s) eliminada(s) con éxito.",
        
        # send2trash Warnings
        "send2trash_not_available_files": "send2trash no está disponible. Los archivos se eliminarán permanentemente.",
        "send2trash_not_available_folders": "send2trash no está disponible. Las carpetas se eliminarán permanentemente.",
        "send2trash_not_available_orphans": "send2trash no está disponible. Los AddOns huérfanos se eliminarán permanentemente.",
        
        # AddOns.txt Rebuild
        "addons_txt_rebuild_summary": "¡AddOns.txt reconstruido con éxito!\n\nAddOns encontrados: {0}\nPersonajes: {1}\nArchivos de configuración: {2}",
        
        # Log Export
        "log_export_empty": "El registro está vacío. No hay nada que exportar.",
        
        # Settings Restore
        "settings_restored_title": "Configuración Restaurada",
        "settings_restored_to_defaults": "Configuración restaurada a los valores predeterminados.",
        "settings_restored_restart_required": "Configuración restaurada a los valores predeterminados.\nPor favor, reinicia la aplicación para que todos los cambios surtan efecto.",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "Sugerencias de Optimización Manual",
        "opt_sug_disclaimer": "NOTA: Esta aplicación NO realiza estas optimizaciones automáticamente. Estas son sugerencias manuales para que las implementes.",
        "opt_sug_clean_data_title": "Limpiar Carpeta de Datos del Juego",
        "opt_sug_clean_data_text": "Si han pasado varios años o múltiples expansiones desde la instalación de World of Warcraft, considera eliminar la carpeta Data de tu directorio principal de World of Warcraft. Esto *podría* reducir el tamaño del juego y mejorar el rendimiento de las pantallas de carga. El lanzador de Battle.net reconstruirá automáticamente esta carpeta cuando sea necesario.",
        "opt_sug_clean_data_tooltip": "POR QUÉ: La carpeta Data acumula activos de juego temporales y en caché con el tiempo. Eliminarla fuerza una descarga fresca de archivos optimizados.\n\nNIVEL DE RIESGO: Seguro - Battle.net redescargará los archivos necesarios automáticamente.\n\nBENEFICIO ESPERADO: Pantallas de carga más rápidas, uso de disco reducido (potencialmente 10-20 GB ahorrados).",
        "opt_sug_hdr_title": "Habilitar HDR (Alto Rango Dinámico)",
        "opt_sug_hdr_text": "Verifica la configuración de pantalla de tu sistema operativo para ver si HDR está disponible. Si tu monitor lo soporta, habilitar HDR puede mejorar significativamente la claridad visual y la profundidad de color en el juego.",
        "opt_sug_hdr_tooltip": "POR QUÉ: HDR proporciona una gama de colores más amplia y mejor contraste, haciendo que las imágenes sean más vibrantes y realistas.\n\nNIVEL DE RIESGO: Seguro - Se puede activar/desactivar fácilmente en la configuración del sistema operativo.\n\nBENEFICIO ESPERADO: Calidad visual dramáticamente mejorada si el monitor soporta HDR10 o mejor.\n\nREQUISITO: Monitor compatible con HDR y Windows 10/11 o macOS Catalina+.",
        "opt_sug_refresh_title": "Verificar Tasa de Refresco del Monitor",
        "opt_sug_refresh_text": "Asegúrate de que la tasa de refresco de tu monitor esté configurada al valor máximo soportado en la configuración de pantalla de tu sistema operativo. Tasas de refresco más altas proporcionan un juego más fluido y mejor capacidad de respuesta.",
        "opt_sug_refresh_tooltip": "POR QUÉ: Muchos sistemas establecen por defecto 60Hz incluso cuando los monitores soportan 120Hz/144Hz/165Hz. Esto limita tu tasa de fotogramas innecesariamente.\n\nNIVEL DE RIESGO: Seguro - Sin riesgo de hardware, fácilmente reversible.\n\nBENEFICIO ESPERADO: Juego más fluido, latencia de entrada reducida, mejores tiempos de reacción.\n\nCÓMO VERIFICAR: Windows: Configuración > Pantalla > Avanzado > Tasa de refresco\nmacOS: Preferencias del Sistema > Pantallas",
        "opt_sug_sam_title": "Habilitar Smart Access Memory / Resizable BAR",
        "opt_sug_sam_text": "Verifica la configuración del BIOS de tu placa madre para Smart Access Memory (AMD) o Resizable BAR (Intel/NVIDIA). Habilitar esta función permite que tu CPU acceda a toda la memoria GPU, mejorando potencialmente el rendimiento.",
        "opt_sug_sam_tooltip": "POR QUÉ: Permite que la CPU acceda a toda la memoria GPU de una vez en lugar de pequeños fragmentos de 256MB, reduciendo cuellos de botella.\n\nNIVEL DE RIESGO: Moderado - Requiere cambios en el BIOS. Documenta la configuración actual primero.\n\nBENEFICIO ESPERADO: Mejora de 5-15% en FPS en escenarios intensivos de GPU.\n\nREQUISITOS:\n• AMD: CPU Ryzen 5000+ + GPU RX 6000+\n• Intel: CPU 10ª gen+ + GPU RTX 3000+\n• Puede requerir actualización del BIOS",
        "opt_sug_xmp_title": "Habilitar Perfil de Memoria XMP",
        "opt_sug_xmp_text": "Accede al BIOS de tu placa madre y habilita la configuración XMP (Extreme Memory Profile) o DOCP/EOCP. Esto asegura que tu RAM funcione a su velocidad nominal en lugar de velocidades conservadoras predeterminadas, mejorando el rendimiento general del sistema.",
        "opt_sug_xmp_tooltip": "POR QUÉ: La RAM típicamente funciona a 2133MHz por defecto incluso si está clasificada para 3200MHz+. XMP habilita las velocidades anunciadas.\n\nNIVEL DE RIESGO: Moderado - Cambio en BIOS. El sistema puede fallar al arrancar si la RAM es inestable (fácil de resetear).\n\nBENEFICIO ESPERADO: Mejora de rendimiento de CPU del 10-20%, tiempos de carga más rápidos, mejores 1% lows.\n\nCÓMO HABILITAR: Entrar al BIOS (generalmente Del/F2 al iniciar) > Encontrar configuración XMP/DOCP > Habilitar > Guardar y Salir",
        
        # Help/About tab - content
        "help_version_label": "Herramienta de Limpieza de WoW {}",
        "help_about_description": "Un conjunto completo de mantenimiento y optimización para World of Warcraft.\nLimpia archivos innecesarios, administra addons, optimiza el rendimiento del juego y más.\n\nSiempre cierra World of Warcraft antes de usar esta herramienta.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Publicado bajo la Licencia Pública General GNU v3.0 (GPL-3.0-or-later). Consulta el archivo LICENSE incluido para los términos completos.",
        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU: {} | RAM: {} | GPU: {}",
        "gpu_switch_notification": "⚠ Cambio de GPU: Configurado para usar '{}' en lugar de '{}'. Este cambio optimiza el rendimiento usando tu GPU dedicada para una mejor experiencia de juego. Es seguro y recomendado.",
        "scan_tooltip_refresh": "Escanear nuevamente no es necesario a menos que hayas cambiado tu CPU, GPU o RAM.\nHaz clic para actualizar la información de hardware en caché.",
        "scanning_ram_detected": "Escaneando RAM... (CPU: {}C/{}T detectada)",
        "scanning_gpu_detected": "Escaneando GPU... (RAM: {} GB detectada)",
        "apply_preset_label": "Aplicar Ajuste:",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "World of Warcraft en Ejecución",
        "wow_running_message": "World of Warcraft está actualmente en ejecución. Los cambios se aplicarán después de reiniciar el juego.\n\n¿Deseas continuar?",
        "permission_error_title": "Error de Permisos",
        "permission_error_message": "Config.wtf está en modo de solo lectura. Por favor, elimina el atributo de solo lectura e inténtalo de nuevo.",
        "config_readonly_status": "✗ Config.wtf está en solo lectura.",
        "confirm_apply_title": "Confirmar Aplicación",
        "confirm_apply_message": "¿Aplicar ajuste {} a {}?\n\nEsto modificará {} configuraciones gráficas en Config.wtf.\nSe creará una copia de seguridad automáticamente.\n\nCambios principales:\n• Ajuste: {} configuraciones de calidad\n• Rendimiento: {} optimización(es)",
        "cancelled_by_user": "Cancelado por el usuario.",
        "settings_applied_status": "✓ {} configuraciones aplicadas.",
        "preset_applied_status": "✓ Ajuste {} aplicado.",
        "apply_error_status": "✗ Error: {}",
        
        # Preset tooltips
        "preset_tooltip_template": "Ajuste {}\n\nRendimiento Esperado:\n{}\n\nHaz clic en 'Aplicar' abajo para usar este ajuste.",
        "perf_depends_hardware": "El impacto en el rendimiento depende de tu hardware.",
        "perf_will_vary": "El rendimiento variará",
        
        # Low preset performance estimates
        "low_perf_high": "Excelente rendimiento (100+ FPS en la mayoría de escenarios)",
        "low_perf_mid": "Muy buen rendimiento (80-120 FPS)",
        "low_perf_low": "Buen rendimiento (60-80 FPS)",
        
        # Medium preset performance estimates
        "medium_perf_high": "Excelente rendimiento (90-120 FPS)",
        "medium_perf_mid": "Buen rendimiento (60-90 FPS)",
        "medium_perf_low": "Rendimiento moderado (45-60 FPS)",
        
        # High preset performance estimates
        "high_perf_high": "Muy buen rendimiento (70-100 FPS)",
        "high_perf_mid": "Buen rendimiento (50-70 FPS)",
        "high_perf_low": "Puede tener dificultades en incursiones (30-50 FPS)",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "Buen rendimiento (60-80 FPS)",
        "ultra_perf_mid": "Rendimiento moderado (40-60 FPS)",
        "ultra_perf_low": "Bajo rendimiento (20-40 FPS)",
        
        # WoW version names
        "version_retail": "Retail",
        "version_classic": "Classic",
        "version_classic_era": "Classic Era",
        "version_ptr": "PTR",
        "version_beta": "Beta",
        
        # Game Optimizer - additional strings
        "not_detected": "No detectado",
        "unknown_cpu": "CPU desconocida",
        "unknown_gpu": "Desconocido",
        "not_set": "No establecido",
        "hover_for_details": "Pase el cursor para ver detalles",
        "new_setting_prefix": "[NUEVO] ",
        "details_colon": "Detalles:",
        "updated_settings": "• {0} configuraciones existentes actualizadas",
        "added_settings": "• {0} nuevas configuraciones añadidas",
        "select_valid_wow_optimizer": "Selecciona una carpeta válida de World of Warcraft en Opciones para habilitar las vistas por versión.",
        "wtf_not_found": "Directorio WTF no encontrado. Por favor, inicia el juego primero.",
        "unknown_preset": "Ajuste desconocido: {}",
        "backup_failed": "Error al crear copia de seguridad: {}",
        "config_write_failed": "Error al escribir configuración: {}",
        "config_updated": "Configuraciones {} aplicadas a Config.wtf. ",
        "settings_updated_added": "{} configuraciones actualizadas, {} nuevas configuraciones añadidas.",
        "backup_saved": " Copia de seguridad guardada.",
        "version_path": "Versión: {}\nRuta: {}",
        "optimizer_launch_required": "El optimizador requiere que {} haya sido iniciado al menos una vez. Por favor, inicia World of Warcraft y ve a la pantalla de selección de personajes, luego cierra el juego. Después de eso, puedes usar el optimizador para aplicar ajustes gráficos.",
        "system_matches": "Tu sistema coincide con: {}",
        "optimizer_title": "Optimizador — {}",
        "recommendations_applied": "✓ Recomendaciones aplicadas.",
        "applied_preset_log": "Aplicado ajuste {} para {}",
        "apply_preset_failed_log": "Error al aplicar ajuste {}: {}",
        "hardware_scan_complete": "Escaneo de hardware completo: almacenado en caché en configuración global.",
        "hardware_scan_failed": "Error en escaneo de hardware: {}",
        "scan_error": "✗ Error: {}",
        
        # Orphan Cleaner - Log messages
        "orphan_found_in": "[Limpiador de huérfanos] Encontrado huérfano en {}: {}",
        "orphan_total_found": "[Limpiador de huérfanos] Total de SavedVariables huérfanos: {}",
        "orphan_moved_trash": "[Limpiador de huérfanos] Movido a papelera: {}",
        "orphan_deleted": "[Limpiador de huérfanos] Eliminado: {}",
        "orphan_error_deleting": "[Limpiador de huérfanos] ERROR al eliminar {}: {}",
        "orphan_rebuilt_addons": "[Limpiador de huérfanos] Reconstruido: {}",
        "orphan_error_writing_addons": "[Limpiador de huérfanos] ERROR al escribir AddOns.txt {}: {}",
        "orphan_error_rebuild": "[Limpiador de huérfanos] ERROR durante la reconstrucción de AddOns.txt: {}",
        
        # Path Manager
        "select_wow_folder_title": "Seleccionar carpeta de World of Warcraft",
        "unrecognized_installation": "Instalación no reconocida",
        "folder_not_valid_continue": "La carpeta seleccionada no parece válida.\n\n¿Continuar de todos modos?",
        "wow_folder_set": "Carpeta de WoW establecida: {}",
        
        # Performance
        "performance_execution_time": "[Rendimiento] {} tardó {:.3f}s",
        "perf_moved_trash": "[{}] Movido a papelera: {}",
        "perf_deleted": "[{}] Eliminado: {}",
        "perf_error_deleting": "[{}] ERROR al eliminar {}: {}",
        
        "select_valid_wow_folder_cleaner": "Selecciona una carpeta válida de World of Warcraft en Opciones para habilitar el Limpiador de carpetas.",
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "Busca en todas las versiones de WoW detectadas las SavedVariables de addons (.lua / .lua.bak) que no tienen un addon instalado correspondiente (Interface/AddOns). Escanea las carpetas SavedVariables de cuenta, reino y personaje. El procesamiento también reconstruye AddOns.txt para que coincida con los addons instalados (preservando habilitado/deshabilitado cuando sea posible).",
        "orphan_description_part2": "Nota: Los archivos Blizzard_*.lua son datos básicos del juego y se ignoran automáticamente por seguridad (pero sus copias de seguridad .lua.bak pueden eliminarse).",
        
        # Game Validation
        "invalid_game_installation": "Instalación de Juego Inválida",
        "game_installation_incomplete": "La instalación de World of Warcraft parece incompleta.\n\nPor favor, ejecuta el juego al menos una vez para inicializar las carpetas Interface y WTF.\n\nDespués de ejecutar el juego, puedes usar esta herramienta para limpiar tu instalación.",
        
        # Startup Warning
        "user_disabled_warning": "El usuario deshabilitó la advertencia de inicio.",
        
        # Update Checker
        "no_updates_available": "No Hay Actualizaciones Disponibles",
        "no_releases_published": "Estás usando {}.\n\nAún no se han publicado versiones.",
        "update_check_failed": "Verificación de Actualización Fallida",
        "update_check_http_error": "No se pudo verificar actualizaciones:\n\nHTTP {}: {}",
        "update_check_network_error": "No se pudo verificar actualizaciones:\n\n{}",
        "update_check_error": "Error de Verificación de Actualización",
        "update_check_exception": "Ocurrió un error al verificar actualizaciones:\n\n{}",
        "update_available": "Actualización Disponible",
        "update_available_message": "¡Hay una nueva versión disponible!\n\nActual: {}\nÚltima: {}\n\nVisita la página de GitHub para descargar la última versión.",
        "up_to_date": "Actualizado",
        "up_to_date_message": "Estás usando la última versión ({}).",
        "browser_open_error": "No se pudo abrir el navegador:\n\n{}",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[Limpiador de Archivos] Archivo encontrado: {}",
        "file_cleaner_found": "[Limpiador de Archivos] Encontrado: {}",
        "file_cleaner_total_found": "[Limpiador de Archivos] Total de archivos .bak/.old encontrados: {}",
        "file_cleaner_moved_trash": "[Limpiador de Archivos] Movido a la papelera: {}",
        "file_cleaner_deleted": "[Limpiador de Archivos] Eliminado: {}",
        "file_cleaner_error_deleting": "[Limpiador de Archivos] ERROR al eliminar {}: {}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[Limpiador de Carpetas] Encontrado: {}",
        "folder_cleaner_total": "[Limpiador de Carpetas] Total de carpetas limpiables: {}",
    },
    
    "ptBR": {
        # Window title
        "window_title": "Ferramenta de Limpeza do WoW",
        
        # Menu/Tab names
        "file_cleaner": "Limpador de Arquivos",
        "folder_cleaner": "Limpador de Pastas",
        "orphan_cleaner": "Limpador de Órfãos",
        "game_optimizer": "Otimizador de Jogo",
        "optimization_suggestions": "Sugestões de Otimização",
        "log": "Registro",
        "help_about": "Ajuda / Sobre",
        
        # Options section
        "options": "Opções",
        "wow_folder": "Pasta do World of Warcraft:",
        "browse": "Procurar...",
        "browse_tooltip": "Procurar sua pasta do World of Warcraft.",
        "font_size": "Tamanho da Fonte:",
        "font": "Fonte:",
        "theme": "Tema:",
        "language": "Idioma:",
        "file_action": "Ação de Arquivo:",
        "delete_permanently": "Excluir Permanentemente",
        "move_to_recycle": "Mover para a Lixeira",
        "enable_verbose": "Ativar registro detalhado",
        "verbose_tooltip": "Quando ativado, o Registro captura cada arquivo/pasta/linha de AddOns.txt processado.",
        "external_log": "Registro Externo:",
        "fresh": "Novo",
        "fresh_tooltip": "Criar um novo arquivo de registro em cada exportação (sobrescreve o existente).",
        "append": "Anexar",
        "append_tooltip": "Anexar cada exportação ao arquivo de registro existente (mantém até 10-20 sessões com base na verbosidade).",
        "check_updates": "Verificar atualizações",
        "check_updates_tooltip": "Quando ativado, verificar novas versões no GitHub na inicialização.",
        "restore_defaults": "Restaurar Padrões",
        "light": "claro",
        "dark": "escuro",
        
        # File Cleaner
        "scan": "Escanear",
        "select_all": "Selecionar Tudo",
        "expand_all": "Expandir Tudo",
        "collapse_all": "Recolher Tudo",
        "process_selected": "Processar Selecionados",
        "scanning": "Escaneando…",
        "no_bak_old_found": "Nenhum arquivo .bak ou .old encontrado.",
        "files_found": "{} arquivo(s) encontrado(s).",
        
        # Folder Cleaner
        "version": "Versão:",
        "path": "Caminho:",
        "preview": "Visualizar",
        "toggle_all": "Alternar Tudo",
        "process_folders": "Processar Pastas Selecionadas",
        
        # Orphan Cleaner
        "rebuild_addons": "Reconstruir AddOns.txt",
        "no_orphans_found": "Nenhum SavedVariables órfão encontrado.",
        "orphans_found": "Encontrados {} SavedVariable(s) órfão(s).",
        
        # Game Optimizer
        "scan_hardware": "Escanear Hardware",
        "system_matches": "Seu sistema corresponde a:",
        "optimization_applied": "✓ Otimização aplicada",
        "optimization_not_applied": "⚠ Otimização ainda não aplicada",
        "graphics_presets": "Predefinições Gráficas ({}):",
        "graphics_presets_classic": "Predefinições Gráficas ({}):",
        "apply_preset": "Aplicar Predefinição:",
        "apply": "Aplicar",
        "preset_applied": "✓ Predefinição {} aplicada.",
        "error": "✗ Erro: {}",
        "low": "Baixo",
        "medium": "Médio",
        "high": "Alto",
        "ultra": "Ultra",
        
        # Optimization Suggestions
        "manual_suggestions": "Sugestões de Otimização Manual",
        "manual_disclaimer": "NOTA: Este aplicativo NÃO realiza essas otimizações automaticamente. Estas são sugestões manuais para você implementar.",
        "clean_data_folder": "Limpar Pasta de Dados do Jogo",
        "clean_data_text": "Se vários anos ou múltiplas expansões se passaram desde a instalação do World of Warcraft, considere excluir a pasta Data do seu diretório principal do World of Warcraft. Isso *pode* reduzir o tamanho do jogo e melhorar o desempenho das telas de carregamento. O Battle.net reconstruirá automaticamente esta pasta quando necessário.",
        "enable_hdr": "Ativar HDR (High Dynamic Range)",
        "enable_hdr_text": "Verifique as configurações de exibição do seu sistema operacional para ver se o HDR está disponível. Se suportado pelo seu monitor, ativar o HDR pode melhorar significativamente a clareza visual e a profundidade de cores no jogo.",
        "verify_refresh": "Verificar Taxa de Atualização do Monitor",
        "verify_refresh_text": "Certifique-se de que a taxa de atualização do seu monitor esteja definida para o valor máximo suportado nas configurações de exibição do seu sistema operacional. Taxas de atualização mais altas proporcionam jogabilidade mais suave e melhor capacidade de resposta.",
        "enable_sam": "Ativar Smart Access Memory / Resizable BAR",
        "enable_sam_text": "Verifique as configurações do BIOS da sua placa-mãe para Smart Access Memory (AMD) ou Resizable BAR (Intel/NVIDIA). Ativar este recurso permite que sua CPU acesse toda a memória da GPU, potencialmente melhorando o desempenho.",
        "enable_xmp": "Ativar Perfil de Memória XMP",
        "enable_xmp_text": "Acesse o BIOS da sua placa-mãe e ative a configuração XMP (Extreme Memory Profile) ou DOCP/EOCP. Isso garante que sua RAM funcione na velocidade nominal em vez de velocidades conservadoras padrão, melhorando o desempenho geral do sistema.",
        
        # Log tab
        "export_log": "Exportar Registro",
        "clear_log": "Limpar Registro",
        
        # Help/About
        "about_text": "Um conjunto abrangente de manutenção e otimização para World of Warcraft.\nLimpe arquivos desnecessários, gerencie addons, otimize o desempenho do jogo e muito mais.\n\nSempre feche o World of Warcraft antes de usar esta ferramenta.",
        "copyright": "Copyright © 2025 Paul Vandersypen. Lançado sob a Licença Pública Geral GNU v3.0 (GPL-3.0-or-later). Consulte o arquivo LICENSE incluído para os termos completos.",
        
        # Dialogs
        "invalid_folder": "Pasta Inválida",
        "select_valid_wow": "Por favor, selecione primeiro uma pasta válida do WoW.",
        "no_selection": "Sem Seleção",
        "no_files_selected": "Nenhum arquivo selecionado para processar.",
        "no_folders_selected": "Nenhuma pasta foi selecionada para limpeza.",
        "no_orphans_selected": "Nenhum arquivo órfão selecionado.",
        "confirm": "Confirmar",
        "confirm_action": "Tem certeza de que deseja {} {} {}?",
        "file_s": "arquivo(s)",
        "folder_s": "pasta(s)",
        "orphaned_savedvars": "SavedVariables órfãos",
        "completed": "Concluído",
        "processed": "Processados {} {}.",
        "send2trash_missing": "send2trash ausente",
        "send2trash_unavailable": "O módulo 'send2trash' não está disponível. Os arquivos foram excluídos permanentemente.",
        "send2trash_install": "O pacote 'send2trash' não está instalado.\nPara ativar o suporte à Lixeira, instale-o manualmente:\n\n  pip install send2trash\n\nou:\n\n  python -m pip install --user send2trash",
        "restore_defaults_confirm": "Restaurar todas as configurações para os padrões?",
        "restart_required": "Configurações restauradas. O aplicativo será reiniciado agora.",
        "error_title": "Erro",
        "restore_error": "Falha ao restaurar padrões: {}",
        "confirm_font": "Confirmar Fonte",
        "apply_font_confirm": "Aplicar fonte '{}' ao aplicativo?",
        "select_font": "Selecionar Fonte",
        "export_log_title": "Exportar Registro",
        "log_empty": "O registro está vazio. Nada para exportar.",
        "log_exported": "Registro exportado com sucesso para:\n{}",
        "export_error": "Erro de Exportação",
        "export_failed": "Falha ao exportar registro:\n{}",
        "addons_rebuilt": "Entradas de AddOns.txt reconstruídas.\nTotal escrito: {}\nTotal removido: {}",
        
        # Log messages
        "session_started": "Sessão iniciada — {}",
        "file_scan": "Escaneamento do Limpador de Arquivos: {} correspondência(s).",
        "orphan_scan": "Escaneamento do Limpador de Órfãos: {} órfão(s).",
        "file_processed": "Limpador de Arquivos: processados {} arquivo(s).",
        "folder_processed": "Limpador de Pastas: processadas {} pasta(s).",
        "orphan_processed": "Limpador de Órfãos: processados {} órfão(s).",
        "send2trash_warning": "Aviso: send2trash não instalado; exclusões foram permanentes.",
        "addons_txt_log": "[AddOns.txt] {}: escreveu {} entradas, removeu {}",
        "preset_applied_log": "Aplicada predefinição {} para {}",
        "preset_failed_log": "Falha ao aplicar predefinição {}: {}",
        
        # Language change
        "language_changed": "Idioma Alterado",
        "language_changed_restart": "O idioma foi alterado. Por favor, reinicie o aplicativo para que todas as alterações tenham efeito.",
        
        # Additional buttons and UI elements
        "apply": "Aplicar",
        "cancel": "Cancelar",
        "scan_bak_old": "Escanear Arquivos .bak / .old",
        "expand_all": "Expandir Tudo",
        "collapse_all": "Recolher Tudo",
        "select_deselect_all": "Selecionar / Desselecionar Tudo",
        "process_selected_files": "Processar Arquivos Selecionados",
        "scan_orphaned": "Escanear SavedVariables Órfãos",
        "process_selected_folders": "Processar Pastas Selecionadas",
        "select_deselect_all_folders": "Selecionar / Desselecionar Todas as Pastas",
        "select_deselect_all_screenshots": "Selecionar / Desselecionar Todas as Capturas de Tela",
        "screenshots_per_file": "Capturas de Tela (ações por arquivo)",
        "check_for_updates": "Verificar Atualizações",
        
        # Game Optimizer
        "game_optimizer_title": "Otimizador de Jogo",
        "game_optimizer_desc": "Otimiza o desempenho do World of Warcraft com base na sua configuração de hardware.",
        "scan_hardware": "Escanear Hardware",
        "click_scan_hardware": "Clique em 'Escanear Hardware' para detectar as capacidades do seu sistema.",
        "select_valid_wow_folder": "Selecione uma pasta válida do World of Warcraft nas Opções para ativar as visualizações por versão.",
        "recommended_settings": "Configurações Recomendadas:",
        "apply_preset_label": "Aplicar Predefinição:",
        "apply_recommended_settings": "Aplicar Configurações Recomendadas",
        "scanning_cpu": "Escaneando CPU...",
        "scanning_ram": "Escaneando RAM... (CPU: {}C/{}T detectada)",
        "scanning_gpu": "Escaneando GPU... (RAM: {} GB detectada)",
        
        # Startup warning
        "important_notice": "Aviso Importante",
        "startup_warning_text": "⚠️ Por favor, certifique-se de que o World of Warcraft esteja completamente fechado antes de usar esta ferramenta.\n\nExecutar a ferramenta enquanto o WoW está aberto pode interferir nos arquivos do jogo.",
        "do_not_show_again": "Não mostrar este aviso novamente",
        "ok": "OK",
        
        # Folder cleaner
        "select_valid_wow_folder_cleaner": "Selecione uma pasta válida do World of Warcraft nas Opções para ativar o Limpador de Pastas.",
        "preview_label": "Visualizar",
        "screenshots_not_found": "Pasta de Capturas de Tela não encontrada para esta versão.",
        
        # Main UI - Buttons and Messages
        "apply": "Aplicar",
        "cancel": "Cancelar",
        "export_log": "Exportar Registro",
        "clear_log": "Limpar Registro",
        "confirm_font_change": "Confirmação de Alteração de Fonte",
        "font_change_restart_required": "A alteração de fonte requer reiniciar o aplicativo.\nVocê deseja reiniciar agora?",
        "restart": "Reiniciar",
        "later": "Mais Tarde",
        "confirm_language_change": "Confirmar Alteração de Idioma",
        "language_change_restart_required": "A alteração de idioma requer reiniciar o aplicativo para ter efeito.\n\nVocê deseja reiniciar agora?",
        "language_change_restart_message": "Por favor, reinicie o aplicativo para que a alteração de idioma tenha efeito.",
        "invalid_folder_title": "Pasta Inválida",
        
        # Common Messages
        "invalid_folder_select_valid_wow": "Por favor, selecione uma pasta válida do World of Warcraft nas Opções.",
        "scanning_files": "Escaneando arquivos...",
        "scanning_folders": "Escaneando pastas...",
        "scanning_orphans": "Escaneando AddOns órfãos...",
        "no_files_selected": "Nenhum arquivo selecionado",
        "no_folders_selected": "Nenhuma pasta selecionada",
        "no_orphans_selected": "Nenhum órfão selecionado",
        
        # File Cleaner
        "select_files_to_delete": "Por favor, selecione pelo menos um arquivo para excluir.",
        "confirm_delete_files_title": "Confirmar Exclusão de Arquivos",
        "confirm_delete_files_message": "Você tem certeza que deseja excluir {0} arquivo(s)?",
        "files_moved_to_recycle_bin": "{0} arquivo(s) movido(s) para a Lixeira.",
        "files_deletion_complete": "{0} arquivo(s) excluído(s) com sucesso.",
        
        # Folder Cleaner
        "select_folders_to_delete": "Por favor, selecione pelo menos uma pasta para excluir.",
        "confirm_delete_folders_title": "Confirmar Exclusão de Pastas",
        "confirm_delete_folders_message": "Você tem certeza que deseja excluir {0} pasta(s)?",
        
        # Orphan Cleaner
        "select_orphans_to_delete": "Por favor, selecione pelo menos um AddOn órfão para excluir.",
        "confirm_delete_orphans_title": "Confirmar Exclusão de Órfãos",
        "confirm_delete_orphans_message": "Você tem certeza que deseja excluir {0} AddOn(s) órfão(s)?\n\nIsso também excluirá todos os arquivos SavedVariables associados.",
        "orphans_moved_to_recycle_bin": "{0} AddOn(s) órfão(s) movido(s) para a Lixeira.",
        "orphans_deletion_complete": "{0} AddOn(s) órfão(s) excluído(s) com sucesso.",
        
        # Actions
        "folders_moved_to_recycle_bin": "{0} pasta(s) movida(s) para a Lixeira.",
        "folders_deletion_complete": "{0} pasta(s) excluída(s) com sucesso.",
        
        # send2trash Warnings
        "send2trash_not_available_files": "send2trash não está disponível. Os arquivos serão excluídos permanentemente.",
        "send2trash_not_available_folders": "send2trash não está disponível. As pastas serão excluídas permanentemente.",
        "send2trash_not_available_orphans": "send2trash não está disponível. Os AddOns órfãos serão excluídos permanentemente.",
        
        # AddOns.txt Rebuild
        "addons_txt_rebuild_summary": "AddOns.txt reconstruído com sucesso!\n\nAddOns encontrados: {0}\nPersonagens: {1}\nArquivos de configuração: {2}",
        
        # Log Export
        "log_export_empty": "O registro está vazio. Não há nada para exportar.",
        
        # Settings Restore
        "settings_restored_title": "Configurações Restauradas",
        "settings_restored_to_defaults": "Configurações restauradas para os padrões.",
        "settings_restored_restart_required": "Configurações restauradas para os padrões.\nPor favor, reinicie o aplicativo para que todas as alterações tenham efeito.",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "Sugestões de Otimização Manual",
        "opt_sug_disclaimer": "NOTA: Este aplicativo NÃO realiza essas otimizações automaticamente. Estas são sugestões manuais para você implementar.",
        "opt_sug_clean_data_title": "Limpar Pasta de Dados do Jogo",
        "opt_sug_clean_data_text": "Se vários anos ou múltiplas expansões se passaram desde a instalação do World of Warcraft, considere excluir a pasta Data do seu diretório principal do World of Warcraft. Isso *pode* reduzir o tamanho do jogo e melhorar o desempenho das telas de carregamento. O Battle.net reconstruirá automaticamente esta pasta quando necessário.",
        "opt_sug_clean_data_tooltip": "POR QUE: A pasta Data acumula ativos de jogo temporários e em cache ao longo do tempo. Excluí-la força um download novo de arquivos otimizados.\n\nNÍVEL DE RISCO: Seguro - Battle.net baixará novamente os arquivos necessários automaticamente.\n\nBENEFÍCIO ESPERADO: Telas de carregamento mais rápidas, uso de disco reduzido (potencialmente 10-20 GB economizados).",
        "opt_sug_hdr_title": "Ativar HDR (High Dynamic Range)",
        "opt_sug_hdr_text": "Verifique as configurações de exibição do seu sistema operacional para ver se o HDR está disponível. Se suportado pelo seu monitor, ativar o HDR pode melhorar significativamente a clareza visual e a profundidade de cores no jogo.",
        "opt_sug_hdr_tooltip": "POR QUE: HDR fornece uma gama de cores mais ampla e melhor contraste, tornando os visuais mais vibrantes e realistas.\n\nNÍVEL DE RISCO: Seguro - Pode ser ativado/desativado facilmente nas configurações do SO.\n\nBENEFÍCIO ESPERADO: Qualidade visual drasticamente melhorada se o monitor suportar HDR10 ou melhor.\n\nREQUISITO: Monitor compatível com HDR e Windows 10/11 ou macOS Catalina+.",
        "opt_sug_refresh_title": "Verificar Taxa de Atualização do Monitor",
        "opt_sug_refresh_text": "Certifique-se de que a taxa de atualização do seu monitor esteja definida para o valor máximo suportado nas configurações de exibição do seu sistema operacional. Taxas de atualização mais altas proporcionam jogabilidade mais suave e melhor capacidade de resposta.",
        "opt_sug_refresh_tooltip": "POR QUE: Muitos sistemas usam 60Hz por padrão mesmo quando os monitores suportam 120Hz/144Hz/165Hz. Isso limita sua taxa de quadros desnecessariamente.\n\nNÍVEL DE RISCO: Seguro - Sem risco de hardware, facilmente reversível.\n\nBENEFÍCIO ESPERADO: Jogabilidade mais suave, latência de entrada reduzida, melhores tempos de reação.\n\nCOMO VERIFICAR: Windows: Configurações > Exibição > Avançado > Taxa de atualização\nmacOS: Preferências do Sistema > Monitores",
        "opt_sug_sam_title": "Ativar Smart Access Memory / Resizable BAR",
        "opt_sug_sam_text": "Verifique as configurações do BIOS da sua placa-mãe para Smart Access Memory (AMD) ou Resizable BAR (Intel/NVIDIA). Ativar este recurso permite que sua CPU acesse toda a memória da GPU, potencialmente melhorando o desempenho.",
        "opt_sug_sam_tooltip": "POR QUE: Permite que a CPU acesse toda a memória da GPU de uma vez em vez de pequenos blocos de 256MB, reduzindo gargalos.\n\nNÍVEL DE RISCO: Moderado - Requer mudanças no BIOS. Documente as configurações atuais primeiro.\n\nBENEFÍCIO ESPERADO: Melhoria de 5-15% em FPS em cenários intensivos de GPU.\n\nREQUISITOS:\n• AMD: CPU Ryzen 5000+ + GPU RX 6000+\n• Intel: CPU 10ª geração+ + GPU RTX 3000+\n• Atualização do BIOS pode ser necessária",
        "opt_sug_xmp_title": "Ativar Perfil de Memória XMP",
        "opt_sug_xmp_text": "Acesse o BIOS da sua placa-mãe e ative a configuração XMP (Extreme Memory Profile) ou DOCP/EOCP. Isso garante que sua RAM funcione na velocidade nominal em vez de velocidades conservadoras padrão, melhorando o desempenho geral do sistema.",
        "opt_sug_xmp_tooltip": "POR QUE: A RAM normalmente funciona a 2133MHz por padrão mesmo se classificada para 3200MHz+. O XMP habilita as velocidades anunciadas.\n\nNÍVEL DE RISCO: Moderado - Mudança no BIOS. O sistema pode falhar ao iniciar se a RAM estiver instável (fácil de resetar).\n\nBENEFÍCIO ESPERADO: Aumento de 10-20% no desempenho da CPU, tempos de carregamento mais rápidos, melhores 1% lows.\n\nCOMO ATIVAR: Entrar no BIOS (geralmente Del/F2 na inicialização) > Encontrar configuração XMP/DOCP > Ativar > Salvar e Sair",
        
        # Help/About tab - content
        "help_version_label": "Ferramenta de Limpeza do WoW {}",
        "help_about_description": "Um conjunto abrangente de manutenção e otimização para World of Warcraft.\nLimpe arquivos desnecessários, gerencie addons, otimize o desempenho do jogo e muito mais.\n\nSempre feche o World of Warcraft antes de usar esta ferramenta.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Lançado sob a Licença Pública Geral GNU v3.0 (GPL-3.0-or-later). Consulte o arquivo LICENSE incluído para os termos completos.",
        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU: {} | RAM: {} | GPU: {}",
        "gpu_switch_notification": "⚠ Troca de GPU: Configurado para usar '{}' em vez de '{}'. Esta mudança otimiza o desempenho usando sua GPU dedicada para uma melhor experiência de jogo. É seguro e recomendado.",
        "scan_tooltip_refresh": "Escanear novamente não é necessário a menos que você tenha mudado sua CPU, GPU ou RAM.\nClique para atualizar as informações de hardware em cache.",
        "scanning_ram_detected": "Escaneando RAM... (CPU: {}C/{}T detectada)",
        "scanning_gpu_detected": "Escaneando GPU... (RAM: {} GB detectada)",
        "apply_preset_label": "Aplicar Predefinição:",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "World of Warcraft em Execução",
        "wow_running_message": "O World of Warcraft está em execução no momento. As alterações entrarão em vigor após reiniciar o jogo.\n\nDeseja continuar?",
        "permission_error_title": "Erro de Permissão",
        "permission_error_message": "Config.wtf está somente leitura. Por favor, remova o atributo somente leitura e tente novamente.",
        "config_readonly_status": "✗ Config.wtf está somente leitura.",
        "confirm_apply_title": "Confirmar Aplicação",
        "confirm_apply_message": "Aplicar predefinição {} a {}?\n\nIsto modificará {} configurações gráficas em Config.wtf.\nUm backup será criado automaticamente.\n\nPrincipais mudanças:\n• Predefinição: {} configurações de qualidade\n• Desempenho: {} otimização(ões)",
        "cancelled_by_user": "Cancelado pelo usuário.",
        "settings_applied_status": "✓ {} configurações aplicadas.",
        "preset_applied_status": "✓ Predefinição {} aplicada.",
        "apply_error_status": "✗ Erro: {}",
        
        # Preset tooltips
        "preset_tooltip_template": "Predefinição {}\n\nDesempenho Esperado:\n{}\n\nClique em 'Aplicar' abaixo para usar esta predefinição.",
        "perf_depends_hardware": "O impacto no desempenho depende do seu hardware.",
        "perf_will_vary": "O desempenho variará",
        
        # Low preset performance estimates
        "low_perf_high": "Excelente desempenho (100+ FPS na maioria dos cenários)",
        "low_perf_mid": "Desempenho muito bom (80-120 FPS)",
        "low_perf_low": "Bom desempenho (60-80 FPS)",
        
        # Medium preset performance estimates
        "medium_perf_high": "Excelente desempenho (90-120 FPS)",
        "medium_perf_mid": "Bom desempenho (60-90 FPS)",
        "medium_perf_low": "Desempenho moderado (45-60 FPS)",
        
        # High preset performance estimates
        "high_perf_high": "Desempenho muito bom (70-100 FPS)",
        "high_perf_mid": "Bom desempenho (50-70 FPS)",
        "high_perf_low": "Pode ter dificuldades em raides (30-50 FPS)",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "Bom desempenho (60-80 FPS)",
        "ultra_perf_mid": "Desempenho moderado (40-60 FPS)",
        "ultra_perf_low": "Baixo desempenho (20-40 FPS)",
        
        # WoW version names
        "version_retail": "Retail",
        "version_classic": "Classic",
        "version_classic_era": "Classic Era",
        "version_ptr": "PTR",
        "version_beta": "Beta",
        
        # Game Optimizer - additional strings
        "not_detected": "Não detectado",
        "unknown_cpu": "CPU desconhecida",
        "unknown_gpu": "Desconhecido",
        "not_set": "Não definido",
        "hover_for_details": "Passe o mouse para ver detalhes",
        
        # Orphan Cleaner - log messages
        "orphan_found_in": "[OrphanCleaner] Órfão encontrado em {0}: {1}",
        "orphan_total_found": "[OrphanCleaner] Total de SavedVariables órfãos: {0}",
        "orphan_moved_trash": "[OrphanCleaner] Movido para a lixeira: {0}",
        "orphan_deleted": "[OrphanCleaner] Excluído: {0}",
        "orphan_error_deleting": "[OrphanCleaner] ERRO ao excluir {0}: {1}",
        "orphan_rebuilt_addons": "[OrphanCleaner] Reconstruído: {0}",
        "orphan_error_writing_addons": "[OrphanCleaner] ERRO ao escrever AddOns.txt {0}: {1}",
        "orphan_error_rebuild": "[OrphanCleaner] ERRO durante a reconstrução de AddOns.txt: {0}",
        "new_setting_prefix": "[NOVO] ",
        "details_colon": "Detalhes:",
        "updated_settings": "• {0} configurações existentes atualizadas",
        "added_settings": "• {0} novas configurações adicionadas",
        
        # Path Manager
        "select_wow_folder_title": "Selecionar pasta do World of Warcraft",
        "unrecognized_installation": "Instalação não reconhecida",
        "folder_not_valid_continue": "A pasta selecionada não parece válida.\n\nContinuar mesmo assim?",
        "wow_folder_set": "Pasta do WoW definida: {}",
        
        # Performance
        "performance_execution_time": "[Performance] {} levou {:.3f}s",
        "perf_moved_trash": "[{}] Movido para a lixeira: {}",
        "perf_deleted": "[{}] Excluído: {}",
        "perf_error_deleting": "[{}] ERRO ao excluir {}: {}",
        
        "select_valid_wow_optimizer": "Selecione uma pasta válida do World of Warcraft nas Opções para ativar as visualizações por versão.",
        "select_valid_wow_folder_cleaner": "Selecione uma pasta válida do World of Warcraft nas Opções para ativar o Limpador de pastas.",
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "Pesquisa em todas as versões do WoW detectadas por SavedVariables de addon (.lua / .lua.bak) que não têm um addon instalado correspondente (Interface/AddOns). Verifica pastas SavedVariables de conta, reino e personagem. O processamento também reconstrói AddOns.txt para corresponder aos addons instalados (preservando ativado/desativado quando possível).",
        "orphan_description_part2": "Nota: Arquivos Blizzard_*.lua são dados principais do jogo e são automaticamente ignorados por segurança (mas seus backups .lua.bak podem ser removidos).",
        "wtf_not_found": "Diretório WTF não encontrado. Por favor, inicie o jogo primeiro.",
        "unknown_preset": "Predefinição desconhecida: {}",
        "backup_failed": "Falha ao criar backup: {}",
        "config_write_failed": "Falha ao escrever configuração: {}",
        "config_updated": "Configurações {} aplicadas a Config.wtf. ",
        "settings_updated_added": "{} configurações atualizadas, {} novas configurações adicionadas.",
        "backup_saved": " Backup salvo.",
        "version_path": "Versão: {}\nCaminho: {}",
        "optimizer_launch_required": "O otimizador requer que {} tenha sido iniciado pelo menos uma vez. Por favor, inicie o World of Warcraft e vá até a tela de seleção de personagens, depois feche o jogo. Depois disso, você pode usar o otimizador para aplicar predefinições gráficas.",
        "system_matches": "Seu sistema corresponde a: {}",
        "optimizer_title": "Otimizador — {}",
        "recommendations_applied": "✓ Recomendações aplicadas.",
        "applied_preset_log": "Aplicada predefinição {} para {}",
        "apply_preset_failed_log": "Falha ao aplicar predefinição {}: {}",
        "hardware_scan_complete": "Escaneamento de hardware concluído: armazenado em cache nas configurações globais.",
        "hardware_scan_failed": "Escaneamento de hardware falhou: {}",
        "scan_error": "✗ Erro: {}",
        
        # Game Validation
        "invalid_game_installation": "Instalação de Jogo Inválida",
        "game_installation_incomplete": "A instalação do World of Warcraft parece incompleta.\n\nPor favor, execute o jogo pelo menos uma vez para inicializar as pastas Interface e WTF.\n\nApós executar o jogo, você pode usar esta ferramenta para limpar sua instalação.",
        
        # Startup Warning
        "user_disabled_warning": "Usuário desativou o aviso de inicialização.",
        
        # Update Checker
        "no_updates_available": "Nenhuma Atualização Disponível",
        "no_releases_published": "Você está usando {}.\n\nNenhuma versão foi publicada ainda.",
        "update_check_failed": "Verificação de Atualização Falhou",
        "update_check_http_error": "Não foi possível verificar atualizações:\n\nHTTP {}: {}",
        "update_check_network_error": "Não foi possível verificar atualizações:\n\n{}",
        "update_check_error": "Erro de Verificação de Atualização",
        "update_check_exception": "Ocorreu um erro ao verificar atualizações:\n\n{}",
        "update_available": "Atualização Disponível",
        "update_available_message": "Uma nova versão está disponível!\n\nAtual: {}\nÚltima: {}\n\nVisite a página do GitHub para baixar a última versão.",
        "up_to_date": "Atualizado",
        "up_to_date_message": "Você está usando a última versão ({}).",
        "browser_open_error": "Não foi possível abrir o navegador:\n\n{}",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[Limpador de Arquivos] Arquivo encontrado: {}",
        "file_cleaner_found": "[Limpador de Arquivos] Encontrado: {}",
        "file_cleaner_total_found": "[Limpador de Arquivos] Total de arquivos .bak/.old encontrados: {}",
        "file_cleaner_moved_trash": "[Limpador de Arquivos] Movido para a lixeira: {}",
        "file_cleaner_deleted": "[Limpador de Arquivos] Excluído: {}",
        "file_cleaner_error_deleting": "[Limpador de Arquivos] ERRO ao excluir {}: {}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[Limpador de Pastas] Encontrado: {}",
        "folder_cleaner_total": "[Limpador de Pastas] Total de pastas limpáveis: {}",
    },
    
    "itIT": {},  # Will use English fallback
    "ruRU": {},  # Will use English fallback
    
    "koKR": {
        # Window title
        "window_title": "WoW 정리 도구",
        
        # Menu/Tab names
        "file_cleaner": "파일 정리",
        "folder_cleaner": "폴더 정리",
        "orphan_cleaner": "고아 파일 정리",
        "game_optimizer": "게임 최적화",
        "optimization_suggestions": "최적화 제안",
        "log": "로그",
        "help_about": "도움말 / 정보",
        
        # Options section
        "options": "옵션",
        "wow_folder": "World of Warcraft 폴더:",
        "browse": "찾아보기...",
        "browse_tooltip": "World of Warcraft 폴더를 검색합니다.",
        "font_size": "글꼴 크기:",
        "font": "글꼴:",
        "theme": "테마:",
        "language": "언어:",
        "file_action": "파일 작업:",
        "delete_permanently": "영구 삭제",
        "move_to_recycle": "휴지통으로 이동",
        "enable_verbose": "상세 로그 활성화",
        "verbose_tooltip": "활성화하면 로그에 처리된 모든 파일/폴더/AddOns.txt 줄이 기록됩니다.",
        "external_log": "외부 로그:",
        "fresh": "새로 만들기",
        "fresh_tooltip": "내보낼 때마다 새 로그 파일을 생성합니다 (기존 파일 덮어쓰기).",
        "append": "추가",
        "append_tooltip": "기존 로그 파일에 각 내보내기를 추가합니다 (상세도에 따라 최대 10-20개 세션 유지).",
        "check_updates": "업데이트 확인",
        "check_updates_tooltip": "활성화하면 시작 시 GitHub에서 새 버전을 확인합니다.",
        "restore_defaults": "기본값 복원",
        "light": "밝음",
        "dark": "어두움",
        
        # File Cleaner
        "scan": "스캔",
        "select_all": "모두 선택",
        "expand_all": "모두 펼치기",
        "collapse_all": "모두 접기",
        "process_selected": "선택 항목 처리",
        "scanning": "스캔 중…",
        "no_bak_old_found": ".bak 또는 .old 파일을 찾을 수 없습니다.",
        "files_found": "{}개 파일을 찾았습니다.",
        
        # Folder Cleaner
        "version": "버전:",
        "path": "경로:",
        "preview": "미리보기",
        "toggle_all": "모두 전환",
        "process_folders": "선택한 폴더 처리",
        
        # Orphan Cleaner
        "rebuild_addons": "AddOns.txt 재구성",
        "no_orphans_found": "고아 SavedVariables를 찾을 수 없습니다.",
        "orphans_found": "{}개의 고아 SavedVariable을 찾았습니다.",
        
        # Game Optimizer
        "scan_hardware": "하드웨어 스캔",
        "system_matches": "시스템이 일치합니다:",
        "optimization_applied": "✓ 최적화 적용됨",
        "optimization_not_applied": "⚠ 최적화가 아직 적용되지 않음",
        "graphics_presets": "그래픽 사전 설정 ({}):",
        "graphics_presets_classic": "그래픽 사전 설정 ({}):",
        "apply_preset": "사전 설정 적용:",
        "apply": "적용",
        "preset_applied": "✓ {} 사전 설정이 적용되었습니다.",
        "error": "✗ 오류: {}",
        "low": "낮음",
        "medium": "보통",
        "high": "높음",
        "ultra": "울트라",
        
        # Optimization Suggestions
        "manual_suggestions": "수동 최적화 제안",
        "manual_disclaimer": "참고: 이 애플리케이션은 이러한 최적화를 자동으로 수행하지 않습니다. 직접 구현해야 하는 수동 제안입니다.",
        "clean_data_folder": "게임 데이터 폴더 정리",
        "clean_data_text": "World of Warcraft 설치 이후 여러 해 또는 여러 확장팩이 지났다면 World of Warcraft 메인 디렉토리에서 Data 폴더를 삭제하는 것을 고려하세요. 이렇게 하면 게임 크기가 줄어들고 로딩 화면 성능이 향상될 *수* 있습니다. Battle.net 런처가 필요할 때 이 폴더를 자동으로 재구성합니다.",
        "enable_hdr": "HDR(High Dynamic Range) 활성화",
        "enable_hdr_text": "운영 체제의 디스플레이 설정에서 HDR을 사용할 수 있는지 확인하세요. 모니터가 지원하는 경우 HDR을 활성화하면 게임 내 시각적 선명도와 색상 깊이가 크게 향상될 수 있습니다.",
        "verify_refresh": "모니터 재생률 확인",
        "verify_refresh_text": "운영 체제의 디스플레이 설정에서 모니터 재생률이 지원되는 최대값으로 설정되어 있는지 확인하세요. 재생률이 높을수록 더 부드러운 게임플레이와 더 나은 반응성을 제공합니다.",
        "enable_sam": "Smart Access Memory / Resizable BAR 활성화",
        "enable_sam_text": "메인보드 BIOS 설정에서 Smart Access Memory(AMD) 또는 Resizable BAR(Intel/NVIDIA)을 확인하세요. 이 기능을 활성화하면 CPU가 전체 GPU 메모리에 액세스할 수 있어 성능이 향상될 수 있습니다.",
        "enable_xmp": "XMP 메모리 프로파일 활성화",
        "enable_xmp_text": "메인보드 BIOS에 액세스하여 XMP(Extreme Memory Profile) 또는 DOCP/EOCP 설정을 활성화하세요. 이렇게 하면 RAM이 기본 보수적인 속도 대신 정격 속도로 작동하여 전체 시스템 성능이 향상됩니다.",
        
        # Log tab
        "export_log": "로그 내보내기",
        "clear_log": "로그 지우기",
        
        # Help/About
        "about_text": "World of Warcraft를 위한 포괄적인 유지 관리 및 최적화 도구 모음입니다.\n불필요한 파일을 정리하고, 애드온을 관리하고, 게임 성능을 최적화하는 등의 작업을 수행합니다.\n\n이 도구를 사용하기 전에 항상 World of Warcraft를 종료하세요.",
        "copyright": "Copyright © 2025 Paul Vandersypen. GNU General Public License v3.0(GPL-3.0-or-later)에 따라 출시되었습니다. 전체 약관은 포함된 LICENSE 파일을 참조하세요.",
        
        # Dialogs
        "invalid_folder": "잘못된 폴더",
        "select_valid_wow": "먼저 유효한 WoW 폴더를 선택하세요.",
        "no_selection": "선택 없음",
        "no_files_selected": "처리할 파일이 선택되지 않았습니다.",
        "no_folders_selected": "정리할 폴더가 선택되지 않았습니다.",
        "no_orphans_selected": "선택된 고아 파일이 없습니다.",
        "confirm": "확인",
        "confirm_action": "{} {}개를 {}하시겠습니까?",
        "file_s": "파일",
        "folder_s": "폴더",
        "orphaned_savedvars": "고아 SavedVariables",
        "completed": "완료",
        "processed": "{}개의 {}을(를) 처리했습니다.",
        "send2trash_missing": "send2trash 누락",
        "send2trash_unavailable": "'send2trash' 모듈을 사용할 수 없습니다. 파일이 영구적으로 삭제되었습니다.",
        "send2trash_install": "'send2trash' 패키지가 설치되지 않았습니다.\n휴지통 지원을 활성화하려면 수동으로 설치하세요:\n\n  pip install send2trash\n\n또는:\n\n  python -m pip install --user send2trash",
        "restore_defaults_confirm": "모든 설정을 기본값으로 복원하시겠습니까?",
        "restart_required": "설정이 복원되었습니다. 애플리케이션이 지금 다시 시작됩니다.",
        "error_title": "오류",
        "restore_error": "기본값 복원 실패: {}",
        "confirm_font": "글꼴 확인",
        "apply_font_confirm": "'{}' 글꼴을 애플리케이션에 적용하시겠습니까?",
        "select_font": "글꼴 선택",
        "export_log_title": "로그 내보내기",
        "log_empty": "로그가 비어 있습니다. 내보낼 항목이 없습니다.",
        "log_exported": "로그를 성공적으로 내보냈습니다:\n{}",
        "export_error": "내보내기 오류",
        "export_failed": "로그 내보내기 실패:\n{}",
        "addons_rebuilt": "AddOns.txt 항목이 재구성되었습니다.\n총 작성: {}\n총 제거: {}",
        
        # Log messages
        "session_started": "세션 시작됨 — {}",
        "file_scan": "파일 정리 스캔: {}개 일치.",
        "orphan_scan": "고아 파일 정리 스캔: {}개 고아 파일.",
        "file_processed": "파일 정리: {}개 파일 처리됨.",
        "folder_processed": "폴더 정리: {}개 폴더 처리됨.",
        "orphan_processed": "고아 파일 정리: {}개 고아 파일 처리됨.",
        "send2trash_warning": "경고: send2trash가 설치되지 않음; 삭제가 영구적으로 수행되었습니다.",
        "addons_txt_log": "[AddOns.txt] {}: {}개 항목 작성, {}개 제거",
        "preset_applied_log": "{} 사전 설정이 {}에 적용됨",
        "preset_failed_log": "{} 사전 설정 적용 실패: {}",
        
        # Language change
        "language_changed": "언어 변경됨",
        "language_changed_restart": "언어가 변경되었습니다. 모든 변경 사항이 적용되려면 애플리케이션을 다시 시작하세요.",
        
        # Additional buttons and UI elements
        "apply": "적용",
        "cancel": "취소",
        "scan_bak_old": ".bak / .old 파일 스캔",
        "expand_all": "모두 펼치기",
        "collapse_all": "모두 접기",
        "select_deselect_all": "모두 선택 / 선택 해제",
        "process_selected_files": "선택한 파일 처리",
        "scan_orphaned": "고아 SavedVariables 스캔",
        "process_selected_folders": "선택한 폴더 처리",
        "select_deselect_all_folders": "모든 폴더 선택 / 선택 해제",
        "select_deselect_all_screenshots": "모든 스크린샷 선택 / 선택 해제",
        "screenshots_per_file": "스크린샷 (파일당 작업)",
        "check_for_updates": "업데이트 확인",
        
        # Game Optimizer
        "game_optimizer_title": "게임 최적화",
        "game_optimizer_desc": "하드웨어 구성에 따라 World of Warcraft 성능을 최적화합니다.",
        "scan_hardware": "하드웨어 스캔",
        "click_scan_hardware": "'하드웨어 스캔'을 클릭하여 시스템 기능을 감지합니다.",
        "select_valid_wow_folder": "옵션에서 유효한 World of Warcraft 폴더를 선택하여 버전별 보기를 활성화하세요.",
        "recommended_settings": "권장 설정:",
        "apply_preset_label": "사전 설정 적용:",
        "apply_recommended_settings": "권장 설정 적용",
        "scanning_cpu": "CPU 스캔 중...",
        "scanning_ram": "RAM 스캔 중... (CPU: {}코어/{}스레드 감지됨)",
        "scanning_gpu": "GPU 스캔 중... (RAM: {} GB 감지됨)",
        
        # Startup warning
        "important_notice": "중요 공지",
        "startup_warning_text": "⚠️ 이 도구를 사용하기 전에 World of Warcraft가 완전히 종료되었는지 확인하세요.\n\nWoW가 열려 있는 동안 도구를 실행하면 게임 파일이 손상될 수 있습니다.",
        "do_not_show_again": "이 경고를 다시 표시하지 않음",
        "ok": "확인",
        
        # Folder cleaner
        "select_valid_wow_folder_cleaner": "옵션에서 유효한 World of Warcraft 폴더를 선택하여 폴더 정리를 활성화하세요.",
        "preview_label": "미리보기",
        "screenshots_not_found": "이 버전의 스크린샷 폴더를 찾을 수 없습니다.",
        
        # Main UI - Buttons and Messages
        "apply": "적용",
        "cancel": "취소",
        "export_log": "로그 내보내기",
        "clear_log": "로그 지우기",
        "confirm_font_change": "글꼴 변경 확인",
        "font_change_restart_required": "글꼴 변경은 애플리케이션을 다시 시작해야 합니다.\n지금 다시 시작하시겠습니까?",
        "restart": "다시 시작",
        "later": "나중에",
        "confirm_language_change": "언어 변경 확인",
        "language_change_restart_required": "언어 변경은 애플리케이션을 다시 시작해야 적용됩니다.\n\n지금 다시 시작하시겠습니까?",
        "language_change_restart_message": "언어 변경을 적용하려면 애플리케이션을 다시 시작하세요.",
        "invalid_folder_title": "잘못된 폴더",
        
        # Common Messages
        "invalid_folder_select_valid_wow": "옵션에서 유효한 World of Warcraft 폴더를 선택하세요.",
        "scanning_files": "파일 스캔 중...",
        "scanning_folders": "폴더 스캔 중...",
        "scanning_orphans": "고아 애드온 스캔 중...",
        "no_files_selected": "선택된 파일 없음",
        "no_folders_selected": "선택된 폴더 없음",
        "no_orphans_selected": "선택된 고아 파일 없음",
        
        # File Cleaner
        "select_files_to_delete": "삭제할 파일을 하나 이상 선택하세요.",
        "confirm_delete_files_title": "파일 삭제 확인",
        "confirm_delete_files_message": "정말로 {0}개의 파일을 삭제하시겠습니까?",
        "files_moved_to_recycle_bin": "{0}개의 파일이 휴지통으로 이동되었습니다.",
        "files_deletion_complete": "{0}개의 파일이 성공적으로 삭제되었습니다.",
        
        # Folder Cleaner
        "select_folders_to_delete": "삭제할 폴더를 하나 이상 선택하세요.",
        "confirm_delete_folders_title": "폴더 삭제 확인",
        "confirm_delete_folders_message": "정말로 {0}개의 폴더를 삭제하시겠습니까?",
        
        # Orphan Cleaner
        "select_orphans_to_delete": "삭제할 고아 애드온을 하나 이상 선택하세요.",
        "confirm_delete_orphans_title": "고아 파일 삭제 확인",
        "confirm_delete_orphans_message": "정말로 {0}개의 고아 애드온을 삭제하시겠습니까?\n\n관련된 모든 SavedVariables 파일도 함께 삭제됩니다.",
        "orphans_moved_to_recycle_bin": "{0}개의 고아 애드온이 휴지통으로 이동되었습니다.",
        "orphans_deletion_complete": "{0}개의 고아 애드온이 성공적으로 삭제되었습니다.",
        
        # Actions
        "folders_moved_to_recycle_bin": "{0}개의 폴더가 휴지통으로 이동되었습니다.",
        "folders_deletion_complete": "{0}개의 폴더가 성공적으로 삭제되었습니다.",
        
        # send2trash Warnings
        "send2trash_not_available_files": "send2trash를 사용할 수 없습니다. 파일이 영구적으로 삭제됩니다.",
        "send2trash_not_available_folders": "send2trash를 사용할 수 없습니다. 폴더가 영구적으로 삭제됩니다.",
        "send2trash_not_available_orphans": "send2trash를 사용할 수 없습니다. 고아 애드온이 영구적으로 삭제됩니다.",
        
        # AddOns.txt Rebuild
        "addons_txt_rebuild_summary": "AddOns.txt가 성공적으로 재구성되었습니다!\n\n찾은 애드온: {0}\n캐릭터: {1}\n구성 파일: {2}",
        
        # Log Export
        "log_export_empty": "로그가 비어 있습니다. 내보낼 것이 없습니다.",
        
        # Settings Restore
        "settings_restored_title": "설정 복원됨",
        "settings_restored_to_defaults": "설정이 기본값으로 복원되었습니다.",
        "settings_restored_restart_required": "설정이 기본값으로 복원되었습니다.\n모든 변경 사항을 적용하려면 애플리케이션을 다시 시작하세요.",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "수동 최적화 제안",
        "opt_sug_disclaimer": "참고: 이 애플리케이션은 이러한 최적화를 자동으로 수행하지 않습니다. 직접 구현해야 하는 수동 제안입니다.",
        "opt_sug_clean_data_title": "게임 데이터 폴더 정리",
        "opt_sug_clean_data_text": "World of Warcraft 설치 이후 여러 해 또는 여러 확장팩이 지났다면 World of Warcraft 메인 디렉토리에서 Data 폴더를 삭제하는 것을 고려하세요. 이렇게 하면 게임 크기가 줄어들고 로딩 화면 성능이 향상될 *수* 있습니다. Battle.net 런처가 필요할 때 이 폴더를 자동으로 재구성합니다.",
        "opt_sug_clean_data_tooltip": "이유: Data 폴더는 시간이 지남에 따라 임시 및 캐시된 게임 애셋을 축적합니다. 삭제하면 최적화된 파일을 새로 다운로드합니다.\n\n위험 수준: 안전함 - Battle.net이 필요한 파일을 자동으로 다시 다운로드합니다.\n\n예상 이점: 더 빠른 로딩 화면, 디스크 사용량 감소 (잠재적으로 10-20 GB 절약).",
        "opt_sug_hdr_title": "HDR(High Dynamic Range) 활성화",
        "opt_sug_hdr_text": "운영 체제의 디스플레이 설정에서 HDR을 사용할 수 있는지 확인하세요. 모니터가 지원하는 경우 HDR을 활성화하면 게임 내 시각적 선명도와 색상 깊이가 크게 향상될 수 있습니다.",
        "opt_sug_hdr_tooltip": "이유: HDR은 더 넓은 색 영역과 더 나은 대비를 제공하여 비주얼을 더 생생하고 사실적으로 만듭니다.\n\n위험 수준: 안전함 - OS 설정에서 쉽게 켜고 끌 수 있습니다.\n\n예상 이점: 모니터가 HDR10 이상을 지원하는 경우 시각적 품질이 크게 향상됩니다.\n\n요구 사항: HDR 호환 모니터 및 Windows 10/11 또는 macOS Catalina+.",
        "opt_sug_refresh_title": "모니터 재생률 확인",
        "opt_sug_refresh_text": "운영 체제의 디스플레이 설정에서 모니터 재생률이 지원되는 최대값으로 설정되어 있는지 확인하세요. 재생률이 높을수록 더 부드러운 게임플레이와 더 나은 반응성을 제공합니다.",
        "opt_sug_refresh_tooltip": "이유: 많은 시스템이 모니터가 120Hz/144Hz/165Hz를 지원하더라도 기본적으로 60Hz로 설정됩니다. 이는 프레임 레이트를 불필요하게 제한합니다.\n\n위험 수준: 안전함 - 하드웨어 위험 없음, 쉽게 되돌릴 수 있습니다.\n\n예상 이점: 더 부드러운 게임플레이, 입력 지연 감소, 더 나은 반응 시간.\n\n확인 방법: Windows: 설정 > 디스플레이 > 고급 > 재생률\nmacOS: 시스템 환경설정 > 디스플레이",
        "opt_sug_sam_title": "Smart Access Memory / Resizable BAR 활성화",
        "opt_sug_sam_text": "메인보드 BIOS 설정에서 Smart Access Memory(AMD) 또는 Resizable BAR(Intel/NVIDIA)을 확인하세요. 이 기능을 활성화하면 CPU가 전체 GPU 메모리에 액세스할 수 있어 성능이 향상될 수 있습니다.",
        "opt_sug_sam_tooltip": "이유: CPU가 256MB의 작은 청크 대신 전체 GPU 메모리에 한 번에 액세스할 수 있어 병목 현상이 줄어듭니다.\n\n위험 수준: 보통 - BIOS 변경이 필요합니다. 먼저 현재 설정을 문서화하세요.\n\n예상 이점: GPU 집약적 시나리오에서 5-15% FPS 향상.\n\n요구 사항:\n• AMD: Ryzen 5000+ CPU + RX 6000+ GPU\n• Intel: 10세대+ CPU + RTX 3000+ GPU\n• BIOS 업데이트가 필요할 수 있음",
        "opt_sug_xmp_title": "XMP 메모리 프로파일 활성화",
        "opt_sug_xmp_text": "메인보드 BIOS에 액세스하여 XMP(Extreme Memory Profile) 또는 DOCP/EOCP 설정을 활성화하세요. 이렇게 하면 RAM이 기본 보수적인 속도 대신 정격 속도로 작동하여 전체 시스템 성능이 향상됩니다.",
        "opt_sug_xmp_tooltip": "이유: RAM은 3200MHz 이상으로 평가되더라도 일반적으로 기본적으로 2133MHz로 실행됩니다. XMP는 광고된 속도를 활성화합니다.\n\n위험 수준: 보통 - BIOS 변경. RAM이 불안정하면 시스템이 부팅에 실패할 수 있습니다(쉽게 재설정 가능).\n\n예상 이점: CPU 성능 10-20% 향상, 더 빠른 로딩 시간, 더 나은 1% 최저값.\n\n활성화 방법: BIOS 진입(일반적으로 부팅 시 Del/F2) > XMP/DOCP 설정 찾기 > 활성화 > 저장 및 종료",
        
        # Help/About tab - content
        "help_version_label": "WoW 정리 도구 {}",
        "help_about_description": "World of Warcraft를 위한 포괄적인 유지 관리 및 최적화 도구 모음입니다.\n불필요한 파일을 정리하고, 애드온을 관리하고, 게임 성능을 최적화하는 등의 작업을 수행합니다.\n\n이 도구를 사용하기 전에 항상 World of Warcraft를 종료하세요.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. GNU General Public License v3.0(GPL-3.0-or-later)에 따라 출시되었습니다. 전체 약관은 포함된 LICENSE 파일을 참조하세요.",
        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU: {} | RAM: {} | GPU: {}",
        "gpu_switch_notification": "⚠ GPU 전환: 더 나은 게임 경험을 위해 전용 GPU를 사용하여 성능을 최적화하기 위해 '{}'를 사용하도록 구성되었습니다. 안전하고 권장됩니다.",
        "scan_tooltip_refresh": "CPU, GPU 또는 RAM을 변경하지 않은 경우 다시 스캔할 필요가 없습니다.\n클릭하여 캐시된 하드웨어 정보를 새로 고칩니다.",
        "scanning_ram_detected": "RAM 스캔 중... (CPU: {}코어/{}스레드 감지됨)",
        "scanning_gpu_detected": "GPU 스캔 중... (RAM: {} GB 감지됨)",
        "apply_preset_label": "사전 설정 적용:",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "World of Warcraft 실행 중",
        "wow_running_message": "World of Warcraft가 현재 실행 중입니다. 변경 사항은 게임을 다시 시작한 후 적용됩니다.\n\n계속하시겠습니까?",
        "permission_error_title": "권한 오류",
        "permission_error_message": "Config.wtf가 읽기 전용입니다. 읽기 전용 속성을 제거하고 다시 시도하세요.",
        "config_readonly_status": "✗ Config.wtf가 읽기 전용입니다.",
        "confirm_apply_title": "적용 확인",
        "confirm_apply_message": "{}에 {} 사전 설정을 적용하시겠습니까?\n\nConfig.wtf의 {}개 그래픽 설정이 수정됩니다.\n백업이 자동으로 생성됩니다.\n\n주요 변경 사항:\n• 사전 설정: {}개 품질 설정\n• 성능: {}개 최적화",
        "cancelled_by_user": "사용자가 취소했습니다.",
        "settings_applied_status": "✓ {}개 설정이 적용되었습니다.",
        "preset_applied_status": "✓ {} 사전 설정이 적용되었습니다.",
        "apply_error_status": "✗ 오류: {}",
        
        # Preset tooltips
        "preset_tooltip_template": "{} 사전 설정\n\n예상 성능:\n{}\n\n이 사전 설정을 사용하려면 아래의 '적용'을 클릭하세요.",
        "perf_depends_hardware": "성능 영향은 하드웨어에 따라 다릅니다.",
        "perf_will_vary": "성능은 다양합니다",
        
        # Low preset performance estimates
        "low_perf_high": "우수한 성능 (대부분의 시나리오에서 100+ FPS)",
        "low_perf_mid": "매우 좋은 성능 (80-120 FPS)",
        "low_perf_low": "좋은 성능 (60-80 FPS)",
        
        # Medium preset performance estimates
        "medium_perf_high": "우수한 성능 (90-120 FPS)",
        "medium_perf_mid": "좋은 성능 (60-90 FPS)",
        "medium_perf_low": "보통 성능 (45-60 FPS)",
        
        # High preset performance estimates
        "high_perf_high": "매우 좋은 성능 (70-100 FPS)",
        "high_perf_mid": "좋은 성능 (50-70 FPS)",
        "high_perf_low": "공격대에서 어려움을 겪을 수 있음 (30-50 FPS)",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "좋은 성능 (60-80 FPS)",
        "ultra_perf_mid": "보통 성능 (40-60 FPS)",
        "ultra_perf_low": "낮은 성능 (20-40 FPS)",
        
        # WoW version names
        "version_retail": "정식",
        "version_classic": "클래식",
        "version_classic_era": "클래식 에라",
        "version_ptr": "PTR",
        "version_beta": "베타",
        
        # Game Optimizer - additional strings
        "not_detected": "감지되지 않음",
        "unknown_cpu": "알 수 없는 CPU",
        "unknown_gpu": "알 수 없음",
        "not_set": "설정되지 않음",
        "hover_for_details": "자세한 내용을 보려면 마우스를 올려놓으세요",
        
        # Orphan Cleaner - log messages
        "orphan_found_in": "[OrphanCleaner] {0}에서 고아 파일 발견: {1}",
        "orphan_total_found": "[OrphanCleaner] 총 고아 SavedVariables: {0}",
        "orphan_moved_trash": "[OrphanCleaner] 휴지통으로 이동됨: {0}",
        "orphan_deleted": "[OrphanCleaner] 삭제됨: {0}",
        "orphan_error_deleting": "[OrphanCleaner] {0} 삭제 중 오류: {1}",
        "orphan_rebuilt_addons": "[OrphanCleaner] 재구성됨: {0}",
        "orphan_error_writing_addons": "[OrphanCleaner] AddOns.txt {0} 쓰기 오류: {1}",
        "orphan_error_rebuild": "[OrphanCleaner] AddOns.txt 재구성 중 오류: {0}",
        "new_setting_prefix": "[새로운 항목] ",
        "details_colon": "세부 정보:",
        "updated_settings": "• 기존 설정 {0}개 업데이트됨",
        "added_settings": "• 새 설정 {0}개 추가됨",
        
        # Path Manager
        "select_wow_folder_title": "World of Warcraft 폴더 선택",
        "unrecognized_installation": "인식되지 않은 설치",
        "folder_not_valid_continue": "선택한 폴더가 유효하지 않은 것 같습니다.\n\n그래도 계속하시겠습니까?",
        "wow_folder_set": "WoW 폴더 설정됨: {}",
        
        # Performance
        "performance_execution_time": "[성능] {}이(가) {:.3f}초 걸림",
        "perf_moved_trash": "[{}] 휴지통으로 이동됨: {}",
        "perf_deleted": "[{}] 삭제됨: {}",
        "perf_error_deleting": "[{}] {} 삭제 중 오류: {}",
        
        "select_valid_wow_optimizer": "옵션에서 유효한 World of Warcraft 폴더를 선택하여 버전별 보기를 활성화하세요.",
        "select_valid_wow_folder_cleaner": "옵션에서 유효한 World of Warcraft 폴더를 선택하여 폴더 클리너를 활성화하세요.",
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "감지된 모든 WoW 버전에서 해당 설치된 애드온(Interface/AddOns)이 없는 애드온 SavedVariables(.lua / .lua.bak)를 검색합니다. 계정, 서버 및 캐릭터 SavedVariables 폴더를 검사합니다. 처리 시 설치된 애드온과 일치하도록 AddOns.txt를 재구성합니다(가능한 경우 활성화/비활성화 상태 유지).",
        "orphan_description_part2": "참고: Blizzard_*.lua 파일은 핵심 게임 데이터이며 안전을 위해 자동으로 무시됩니다(.lua.bak 백업은 제거될 수 있음).",
        "wtf_not_found": "WTF 디렉토리를 찾을 수 없습니다. 먼저 게임을 시작하세요.",
        "unknown_preset": "알 수 없는 사전 설정: {}",
        "backup_failed": "백업 생성 실패: {}",
        "config_write_failed": "구성 쓰기 실패: {}",
        "config_updated": "Config.wtf에 {}개 설정이 적용되었습니다. ",
        "settings_updated_added": "{}개 설정이 업데이트되고 {}개의 새 설정이 추가되었습니다.",
        "backup_saved": " 백업이 저장되었습니다.",
        "version_path": "버전: {}\n경로: {}",
        "optimizer_launch_required": "최적화 도구를 사용하려면 {}을(를) 한 번 이상 시작해야 합니다. World of Warcraft를 시작하여 캐릭터 선택 화면으로 이동한 다음 게임을 종료하세요. 그 후 최적화 도구를 사용하여 그래픽 사전 설정을 적용할 수 있습니다.",
        "system_matches": "시스템이 일치합니다: {}",
        "optimizer_title": "최적화 — {}",
        "recommendations_applied": "✓ 권장 사항이 적용되었습니다.",
        "applied_preset_log": "{} 사전 설정이 {}에 적용됨",
        "apply_preset_failed_log": "{} 사전 설정 적용 실패: {}",
        "hardware_scan_complete": "하드웨어 스캔 완료: 전역 설정에 캐시됨.",
        "hardware_scan_failed": "하드웨어 스캔 실패: {}",
        "scan_error": "✗ 오류: {}",
        
        # Game Validation
        "invalid_game_installation": "잘못된 게임 설치",
        "game_installation_incomplete": "World of Warcraft 설치가 불완전한 것으로 보입니다.\n\nInterface 및 WTF 폴더를 초기화하려면 게임을 최소 한 번 실행하세요.\n\n게임을 실행한 후 이 도구를 사용하여 설치를 정리할 수 있습니다.",
        
        # Startup Warning
        "user_disabled_warning": "사용자가 시작 경고를 비활성화했습니다.",
        
        # Update Checker
        "no_updates_available": "업데이트 없음",
        "no_releases_published": "{}을(를) 사용 중입니다.\n\n아직 배포된 버전이 없습니다.",
        "update_check_failed": "업데이트 확인 실패",
        "update_check_http_error": "업데이트를 확인할 수 없습니다:\n\nHTTP {}: {}",
        "update_check_network_error": "업데이트를 확인할 수 없습니다:\n\n{}",
        "update_check_error": "업데이트 확인 오류",
        "update_check_exception": "업데이트 확인 중 오류가 발생했습니다:\n\n{}",
        "update_available": "업데이트 사용 가능",
        "update_available_message": "새 버전을 사용할 수 있습니다!\n\n현재: {}\n최신: {}\n\nGitHub 페이지를 방문하여 최신 버전을 다운로드하세요.",
        "up_to_date": "최신 버전",
        "up_to_date_message": "최신 버전({})을 사용 중입니다.",
        "browser_open_error": "브라우저를 열 수 없습니다:\n\n{}",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[파일 정리] 파일을 찾았습니다: {}",
        "file_cleaner_found": "[파일 정리] 찾음: {}",
        "file_cleaner_total_found": "[파일 정리] 총 .bak/.old 파일 발견: {}",
        "file_cleaner_moved_trash": "[파일 정리] 휴지통으로 이동: {}",
        "file_cleaner_deleted": "[파일 정리] 삭제됨: {}",
        "file_cleaner_error_deleting": "[파일 정리] {} 삭제 중 오류: {}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[폴더 정리] 찾음: {}",
        "folder_cleaner_total": "[폴더 정리] 총 정리 가능한 폴더: {}",
    },
    
    "zhCN": {},  # Will use English fallback
    "zhTW": {},  # Will use English fallback
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
