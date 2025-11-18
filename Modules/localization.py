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
    "zhTW": "繁體中文",
    "ukUA": "Українська"
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
        "process_selected_screenshots": "Process Selected Screenshots",
        "no_screenshots_selected": "No screenshots selected.",
        "confirm_action_screenshots": "{} {} screenshot file(s)?",
        "processed_screenshots_count": "Processed {} screenshot(s).",
        "screenshots_per_file": "Screenshots (per-file actions)",
        "folder_screenshots": "Screenshots",
        "folder_logs": "Logs",
        "folder_errors": "Errors",
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
        "preview_hint": "(Click image to enlarge • Click again or press Esc to close)",
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
        "opt_sug_reinstall_title": "Reinstall WoW (Clean Install)",
        "opt_sug_reinstall_text": "Back up your AddOns and WTF folders, uninstall all WoW versions via Battle.net, reinstall, then restore your backups. This removes accumulated legacy files and obsolete data from years of patches.",
        "opt_sug_reinstall_tooltip": "WHY: Years of updates leave behind obsolete files, deprecated assets, and fragmented data that slow loading and waste space.\n\nRISK LEVEL: Low - Your settings/addons are preserved in WTF/AddOns folders.\n\nEXPECTED BENEFIT: Faster loading times, reduced disk usage (5-15 GB saved), improved stability.\n\nHOW TO: 1) Back up Interface\\AddOns and WTF folders\n2) Uninstall via Battle.net\n3) Reinstall WoW\n4) Copy backed up folders back",
        
        # Help/About tab - content
        "help_version_label": "WoW Cleanup Tool {}",
        "help_about_description": "A comprehensive maintenance and optimization suite for World of Warcraft.\nClean unnecessary files, manage addons, optimize game performance, and more.\n\nAlways close World of Warcraft before running this tool.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Released under the GNU General Public License v3.0 (GPL-3.0-or-later). See the included LICENSE file for full terms.",
        "support_patreon": "Support on Patreon",
        "donate_paypal": "Donate via PayPal",
        "github_repository": "GitHub Repository",
        "github_issues": "Report Issues",
        
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
        "update_message": "A new version is available!\n\nCurrent: {}\nLatest: {}\n\nWould you like to download it now?",
        "up_to_date": "Up to Date",
        "up_to_date_message": "You are running the latest version ({}).",
        "browser_open_error": "Could not open browser:\n\n{}",
        "download_update": "Download Update",
        "view_release": "View Release",
        "later": "Later",
        "downloading_update": "Downloading Update",
        "downloading_update_file": "Downloading update file...",
        "download_failed": "Download Failed",
        "download_failed_message": "Failed to download update:\n\n{}",
        "update_ready": "Update Ready",
        "update_downloaded_message": "Update downloaded successfully!\n\nFile: {}\n\nWould you like to install it now?",
        "install_now": "Install Now",
        "install_later": "Install Later",
        "update_location": "Downloaded to: {}",
        "failed_to_fetch_release": "Failed to fetch release information from GitHub.",
        "no_download_available": "No downloadable files found for this release.",
        "install_update": "Install Update",
        "please_run_installer": "The download location has been opened.\n\nPlease run the installer to update the application.",
        "update_saved_message": "Update saved to:\n\n{}\n\nYou can install it later.",
        
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
        "processed": "{} {} verarbeitet.",        "restore_defaults_confirm": "Alle Einstellungen auf Standardwerte zurücksetzen?",
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
        "process_selected_screenshots": "Ausgewählte Screenshots verarbeiten",
        "no_screenshots_selected": "Keine Screenshots ausgewählt.",
        "confirm_action_screenshots": "{} {} Screenshot-Datei(en)?",
        "processed_screenshots_count": "{} Screenshot(s) verarbeitet.",
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
        "preview_hint": "(Bild anklicken zum Vergrößern • Erneut klicken oder Esc drücken zum Schließen)",
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
        "opt_sug_reinstall_title": "WoW neu installieren (Neuinstallation)",
        "opt_sug_reinstall_text": "Sichern Sie Ihre AddOns- und WTF-Ordner, deinstallieren Sie alle WoW-Versionen über Battle.net, installieren Sie neu und stellen Sie Ihre Backups wieder her. Dies entfernt angesammelte Legacy-Dateien und veraltete Daten aus jahrelangen Patches.",
        "opt_sug_reinstall_tooltip": "WARUM: Jahre von Updates hinterlassen veraltete Dateien, veraltete Assets und fragmentierte Daten, die das Laden verlangsamen und Speicherplatz verschwenden.\n\nRISIKOSTUFE: Niedrig - Ihre Einstellungen/Addons bleiben in WTF/AddOns-Ordnern erhalten.\n\nERWARTETER NUTZEN: Schnellere Ladezeiten, reduzierte Festplattennutzung (5-15 GB gespart), verbesserte Stabilität.\n\nSO AKTIVIEREN: 1) Interface\\AddOns und WTF sichern\n2) Über Battle.net deinstallieren\n3) WoW neu installieren\n4) Gesicherte Ordner zurückkopieren",
        
        # Help/About tab - content
        "help_version_label": "WoW Bereinigungstool {}",
        "help_about_description": "Eine umfassende Wartungs- und Optimierungssuite für World of Warcraft.\nBereinigen Sie unnötige Dateien, verwalten Sie Addons, optimieren Sie die Spielleistung und mehr.\n\nSchließen Sie World of Warcraft immer, bevor Sie dieses Tool verwenden.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Veröffentlicht unter der GNU General Public License v3.0 (GPL-3.0-or-later). Siehe die beigefügte LICENSE-Datei für vollständige Bedingungen.",
        "support_patreon": "Auf Patreon unterstützen",
        "donate_paypal": "Via PayPal spenden",
        "github_repository": "GitHub-Repository",
        "github_issues": "Probleme melden",
        
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
        "update_message": "Eine neue Version ist verfügbar!\n\nAktuell: {}\nNeueste: {}\n\nMöchten Sie es jetzt herunterladen?",
        "up_to_date": "Auf dem neuesten Stand",
        "up_to_date_message": "Sie verwenden die neueste Version ({}).",
        "browser_open_error": "Browser konnte nicht geöffnet werden:\n\n{}",
        "download_update": "Update herunterladen",
        "view_release": "Version anzeigen",
        "later": "Später",
        "downloading_update": "Update wird heruntergeladen",
        "downloading_update_file": "Update-Datei wird heruntergeladen...",
        "download_failed": "Download fehlgeschlagen",
        "download_failed_message": "Update konnte nicht heruntergeladen werden:\n\n{}",
        "update_ready": "Update bereit",
        "update_downloaded_message": "Update erfolgreich heruntergeladen!\n\nDatei: {}\n\nMöchten Sie es jetzt installieren?",
        "install_now": "Jetzt installieren",
        "install_later": "Später installieren",
        "update_location": "Heruntergeladen nach: {}",
        "failed_to_fetch_release": "Release-Informationen konnten nicht von GitHub abgerufen werden.",
        "no_download_available": "Keine herunterladbaren Dateien für diese Version gefunden.",
        "install_update": "Update installieren",
        "please_run_installer": "Der Download-Speicherort wurde geöffnet.\n\nBitte führen Sie das Installationsprogramm aus, um die Anwendung zu aktualisieren.",
        "update_saved_message": "Update gespeichert unter:\n\n{}\n\nSie können es später installieren.",
        
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
        "processed": "{} {} traité(s).",        "restore_defaults_confirm": "Restaurer tous les paramètres par défaut ?",
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
        "orphan_processed": "Nettoyeur d'orphelins : {} orphelin(s) traité(s).",        "addons_txt_log": "[AddOns.txt] {} : {} entrées écrites, {} supprimées",
        "preset_applied_log": "Préréglage {} appliqué pour {}",
        "preset_failed_log": "Échec de l'application du préréglage {} : {}",
        "change_language": "Changer la langue",
        "change_language_question": "Changer la langue de {} à {} ?\n\nL'application va redémarrer pour appliquer la nouvelle langue.",
        "language_changed": "Langue modifiée",
        "language_changed_restart": "Langue modifiée en {}.\nL'application va maintenant redémarrer.",
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
        "process_selected_screenshots": "Traiter les captures d'écran sélectionnées",
        "no_screenshots_selected": "Aucune capture d'écran sélectionnée.",
        "confirm_action_screenshots": "{} {} fichier(s) de capture d'écran ?",
        "processed_screenshots_count": "{} capture(s) d'écran traitée(s).",
        "screenshots_per_file": "Captures d'écran (actions par fichier)",
        "folder_screenshots": "Captures d'écran",
        "folder_logs": "Journaux",
        "folder_errors": "Erreurs",
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
        "preview_hint": "(Cliquez sur l'image pour agrandir • Cliquez à nouveau ou appuyez sur Échap pour fermer)",
        "screenshots_not_found": "Dossier de captures d'écran introuvable pour cette version.",
        
        # Main UI - Buttons and Messages
        "apply": "Appliquer",
        "cancel": "Annuler",
        "export_log": "Exporter le journal",
        "clear_log": "Effacer le journal",
        
        # Common Messages
        "no_files_selected": "Aucun fichier sélectionné",
        "no_folders_selected": "Aucun dossier sélectionné",
        "no_orphans_selected": "Aucun orphelin sélectionné",

        # Common Messages
        "apply_font_question": "Appliquer la police '{}' à l'application ?",
        "select_valid_wow_first": "Veuillez d'abord sélectionner un dossier WoW valide.",
        "restored": "Restauré",

        # File Cleaner
        "found_files_count": "Trouvé {} fichier(s) sur toutes les versions.",
        "confirm_action_files": "Êtes-vous sûr de vouloir {} {} fichier(s) ?",
        "processed_files_count": "Traité {} fichier(s).",

        # Folder Cleaner
        "confirm_action_folders": "Êtes-vous sûr de vouloir {} {} dossier(s) ?",
        "processed_folders_count": "Traité {} dossier(s).",

        # Orphan Cleaner
        "found_orphans_count": "Trouvé {} SavedVariable(s) orphelin(s).",
        "confirm_action_orphans": "Êtes-vous sûr de vouloir {} {} SavedVariables orphelins ?",
        "processed_orphans_count": "Traité {} orphelin(s).",

        # Actions
        "move_to_trash": "déplacer vers la corbeille",
        "delete_permanently_action": "supprimer définitivement",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "Entrées AddOns.txt reconstruites.\nTotal écrit : {}\nTotal supprimé : {}",

        # Log Export
        "log_empty_nothing_export": "Le journal est vide. Rien à exporter.",

        # Settings Restore
        "settings_restored_restart": "Paramètres restaurés par défaut. L'application va maintenant redémarrer.",
        "settings_restored_manual": "Paramètres restaurés par défaut. Veuillez redémarrer l'application manuellement.",
        "failed_restore_defaults": "Échec de la restauration des paramètres par défaut : {}",
        
        # File Cleaner
        
        # Folder Cleaner
        
        # Orphan Cleaner
        
        # Actions
        
        # AddOns.txt Rebuild
        
        # Log Export
        
        # Settings Restore
        
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
        "opt_sug_reinstall_title": "Réinstaller WoW (Installation propre)",
        "opt_sug_reinstall_text": "Sauvegardez vos dossiers AddOns et WTF, désinstallez toutes les versions de WoW via Battle.net, réinstallez, puis restaurez vos sauvegardes. Cela supprime les fichiers hérités accumulés et les données obsolètes des années de correctifs.",
        "opt_sug_reinstall_tooltip": "POURQUOI : Des années de mises à jour laissent des fichiers obsolètes, des ressources dépréciées et des données fragmentées qui ralentissent le chargement et gaspillent l'espace.\n\nNIVEAU DE RISQUE : Faible - Vos paramètres/addons sont préservés dans les dossiers WTF/AddOns.\n\nAVANTAGE ATTENDU : Temps de chargement plus rapides, utilisation réduite du disque (5-15 Go économisés), stabilité améliorée.\n\nCOMMENT FAIRE : 1) Sauvegarder Interface\\AddOns et WTF\n2) Désinstaller via Battle.net\n3) Réinstaller WoW\n4) Copier les dossiers sauvegardés",
        
        # Help/About tab - content
        "help_version_label": "Outil de nettoyage WoW {}",
        "help_about_description": "Une suite complète de maintenance et d'optimisation pour World of Warcraft.\nNettoyez les fichiers inutiles, gérez les addons, optimisez les performances du jeu, et plus encore.\n\nFermez toujours World of Warcraft avant d'utiliser cet outil.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Publié sous la licence publique générale GNU v3.0 (GPL-3.0-or-later). Consultez le fichier LICENSE inclus pour les conditions complètes.",
        "support_patreon": "Soutenir sur Patreon",
        "donate_paypal": "Faire un don via PayPal",
        "github_repository": "Dépôt GitHub",
        "github_issues": "Signaler des problèmes",
        
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
        "update_message": "Une nouvelle version est disponible !\n\nActuelle : {}\nDernière : {}\n\nVoulez-vous la télécharger maintenant ?",
        "up_to_date": "À jour",
        "up_to_date_message": "Vous utilisez la dernière version ({}).",
        "browser_open_error": "Impossible d'ouvrir le navigateur :\n\n{}",
        "download_update": "Télécharger la mise à jour",
        "view_release": "Voir la version",
        "later": "Plus tard",
        "downloading_update": "Téléchargement de la mise à jour",
        "downloading_update_file": "Téléchargement du fichier de mise à jour...",
        "download_failed": "Échec du téléchargement",
        "download_failed_message": "Échec du téléchargement de la mise à jour :\n\n{}",
        "update_ready": "Mise à jour prête",
        "update_downloaded_message": "Mise à jour téléchargée avec succès !\n\nFichier : {}\n\nVoulez-vous l'installer maintenant ?",
        "install_now": "Installer maintenant",
        "install_later": "Installer plus tard",
        "update_location": "Téléchargé dans : {}",
        "failed_to_fetch_release": "Impossible de récupérer les informations de version depuis GitHub.",
        "no_download_available": "Aucun fichier téléchargeable trouvé pour cette version.",
        "install_update": "Installer la mise à jour",
        "please_run_installer": "L'emplacement de téléchargement a été ouvert.\n\nVeuillez exécuter le programme d'installation pour mettre à jour l'application.",
        "update_saved_message": "Mise à jour enregistrée dans :\n\n{}\n\nVous pouvez l'installer plus tard.",
        
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
        "processed": "{} {} procesado(s).",        "restore_defaults_confirm": "¿Restaurar toda la configuración a los valores predeterminados?",
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
        "orphan_processed": "Limpiador de huérfanos: {} huérfano(s) procesado(s).",        "addons_txt_log": "[AddOns.txt] {}: {} entradas escritas, {} eliminadas",
        "preset_applied_log": "Ajuste predefinido {} aplicado para {}",
        "preset_failed_log": "Error al aplicar el ajuste predefinido {}: {}",
        "change_language": "Cambiar idioma",
        "change_language_question": "¿Cambiar idioma de {} a {}?\n\nLa aplicación se reiniciará para aplicar el nuevo idioma.",
        "language_changed": "Idioma cambiado",
        "language_changed_restart": "Idioma cambiado a {}.\nLa aplicación se reiniciará ahora.",
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
        "process_selected_screenshots": "Procesar capturas de pantalla seleccionadas",
        "no_screenshots_selected": "No hay capturas de pantalla seleccionadas.",
        "confirm_action_screenshots": "¿{} {} archivo(s) de captura de pantalla?",
        "processed_screenshots_count": "{} captura(s) de pantalla procesada(s).",
        "screenshots_per_file": "Capturas de pantalla (acciones por archivo)",
        "folder_screenshots": "Capturas de pantalla",
        "folder_logs": "Registros",
        "folder_errors": "Errores",
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
        "preview_hint": "(Haz clic en la imagen para ampliar • Haz clic de nuevo o pulsa Esc para cerrar)",
        "screenshots_not_found": "Carpeta de capturas de pantalla no encontrada para esta versión.",
        
        # Main UI - Buttons and Messages
        "apply": "Aplicar",
        "cancel": "Cancelar",
        "export_log": "Exportar registro",
        "clear_log": "Limpiar registro",
        
        # Common Messages
        "no_files_selected": "No se seleccionaron archivos",
        "no_folders_selected": "No se seleccionaron carpetas",
        "no_orphans_selected": "No se seleccionaron huérfanos",

        # Common Messages
        "apply_font_question": "¿Aplicar fuente '{}' a la aplicación?",
        "select_valid_wow_first": "Por favor, selecciona primero una carpeta WoW válida.",
        "restored": "Restaurado",

        # File Cleaner
        "found_files_count": "Encontrado {} archivo(s) en todas las versiones.",
        "confirm_action_files": "¿Estás seguro de que quieres {} {} archivo(s)?",
        "processed_files_count": "Procesado {} archivo(s).",

        # Folder Cleaner
        "confirm_action_folders": "¿Estás seguro de que quieres {} {} carpeta(s)?",
        "processed_folders_count": "Procesado {} carpeta(s).",

        # Orphan Cleaner
        "found_orphans_count": "Encontrado {} SavedVariable(s) huérfano(s).",
        "confirm_action_orphans": "¿Estás seguro de que quieres {} {} SavedVariables huérfanos?",
        "processed_orphans_count": "Procesado {} huérfano(s).",

        # Actions
        "move_to_trash": "mover a la papelera",
        "delete_permanently_action": "eliminar permanentemente",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "Entradas de AddOns.txt reconstruidas.\nTotal escrito: {}\nTotal eliminado: {}",

        # Log Export
        "log_empty_nothing_export": "El registro está vacío. Nada que exportar.",

        # Settings Restore
        "settings_restored_restart": "Configuración restaurada a valores predeterminados. La aplicación se reiniciará ahora.",
        "settings_restored_manual": "Configuración restaurada a valores predeterminados. Por favor, reinicia la aplicación manualmente.",
        "failed_restore_defaults": "Error al restaurar valores predeterminados: {}",
        
        # File Cleaner
        
        # Folder Cleaner
        
        # Orphan Cleaner
        
        # Actions
        
        # AddOns.txt Rebuild
        
        # Log Export
        
        # Settings Restore
        
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
        "opt_sug_reinstall_title": "Reinstalar WoW (Instalación limpia)",
        "opt_sug_reinstall_text": "Haz copia de seguridad de tus carpetas AddOns y WTF, desinstala todas las versiones de WoW a través de Battle.net, reinstala y luego restaura tus copias de seguridad. Esto elimina archivos heredados acumulados y datos obsoletos de años de parches.",
        "opt_sug_reinstall_tooltip": "POR QUÉ: Años de actualizaciones dejan archivos obsoletos, recursos deprecados y datos fragmentados que ralentizan la carga y desperdician espacio.\n\nNIVEL DE RIESGO: Bajo - Tus configuraciones/addons se conservan en carpetas WTF/AddOns.\n\nBENEFICIO ESPERADO: Tiempos de carga más rápidos, uso de disco reducido (5-15 GB ahorrados), estabilidad mejorada.\n\nCÓMO HACERLO: 1) Respaldar Interface\\AddOns y WTF\n2) Desinstalar vía Battle.net\n3) Reinstalar WoW\n4) Copiar carpetas respaldadas",
        
        # Help/About tab - content
        "help_version_label": "Herramienta de limpieza de WoW {}",
        "help_about_description": "Un conjunto completo de mantenimiento y optimización para World of Warcraft.\nLimpia archivos innecesarios, gestiona addons, optimiza el rendimiento del juego y más.\n\nCierra siempre World of Warcraft antes de ejecutar esta herramienta.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Publicado bajo la Licencia Pública General GNU v3.0 (GPL-3.0-or-later). Consulta el archivo LICENSE incluido para conocer los términos completos.",
        "support_patreon": "Apoyar en Patreon",
        "donate_paypal": "Donar vía PayPal",
        "github_repository": "Repositorio de GitHub",
        "github_issues": "Reportar problemas",

        
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
        "update_message": "¡Hay una nueva versión disponible!\n\nActual: {}\nÚltima: {}\n\n¿Quieres descargarla ahora?",
        "up_to_date": "Actualizado",
        "up_to_date_message": "Estás usando la última versión ({}).",
        "browser_open_error": "No se pudo abrir el navegador:\n\n{}",
        "download_update": "Descargar actualización",
        "view_release": "Ver versión",
        "later": "Más tarde",
        "downloading_update": "Descargando actualización",
        "downloading_update_file": "Descargando archivo de actualización...",
        "download_failed": "Descarga fallida",
        "download_failed_message": "Error al descargar la actualización:\n\n{}",
        "update_ready": "Actualización lista",
        "update_downloaded_message": "¡Actualización descargada correctamente!\n\nArchivo: {}\n\n¿Quieres instalarla ahora?",
        "install_now": "Instalar ahora",
        "install_later": "Instalar más tarde",
        "update_location": "Descargado en: {}",
        "failed_to_fetch_release": "Error al obtener información de versión desde GitHub.",
        "no_download_available": "No se encontraron archivos descargables para esta versión.",
        "install_update": "Instalar actualización",
        "please_run_installer": "Se ha abierto la ubicación de descarga.\n\nEjecuta el instalador para actualizar la aplicación.",
        "update_saved_message": "Actualización guardada en:\n\n{}\n\nPuedes instalarla más tarde.",
        
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
        "processed": "Procesados {} {}.",        "restore_defaults_confirm": "¿Restaurar toda la configuración a los valores predeterminados?",
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
        "orphan_processed": "Limpiador de Huérfanos: procesados {} huérfano(s).",        "addons_txt_log": "[AddOns.txt] {}: escribió {} entradas, eliminó {}",
        "preset_applied_log": "Aplicado ajuste {} para {}",
        "preset_failed_log": "Error al aplicar ajuste {}: {}",
        "change_language": "Cambiar Idioma",
        "change_language_question": "¿Cambiar idioma de {} a {}?\n\nLa aplicación se reiniciará para aplicar el nuevo idioma.",
        "language_changed": "Idioma Cambiado",
        "language_changed_restart": "Idioma cambiado a {}.\nLa aplicación se reiniciará ahora.",
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
        "process_selected_screenshots": "Procesar Capturas de Pantalla Seleccionadas",
        "no_screenshots_selected": "No hay capturas de pantalla seleccionadas.",
        "confirm_action_screenshots": "¿{} {} archivo(s) de captura de pantalla?",
        "processed_screenshots_count": "{} captura(s) de pantalla procesada(s).",
        "screenshots_per_file": "Capturas de Pantalla (acciones por archivo)",
        "folder_screenshots": "Capturas de Pantalla",
        "folder_logs": "Registros",
        "folder_errors": "Errores",
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
        "preview_hint": "(Haz clic en la imagen para ampliar • Haz clic de nuevo o presiona Esc para cerrar)",
        "screenshots_not_found": "Carpeta de Capturas de Pantalla no encontrada para esta versión.",
        
        # Main UI - Buttons and Messages
        "apply": "Aplicar",
        "cancel": "Cancelar",
        "export_log": "Exportar Registro",
        "clear_log": "Limpiar Registro",
        
        # Common Messages
        "no_files_selected": "No se seleccionaron archivos",
        "no_folders_selected": "No se seleccionaron carpetas",
        "no_orphans_selected": "No se seleccionaron huérfanos",

        # Common Messages
        "apply_font_question": "¿Aplicar fuente '{}' a la aplicación?",
        "select_valid_wow_first": "Por favor, selecciona primero una carpeta WoW válida.",
        "restored": "Restaurado",

        # File Cleaner
        "found_files_count": "Encontrado {} archivo(s) en todas las versiones.",
        "confirm_action_files": "¿Estás seguro de que quieres {} {} archivo(s)?",
        "processed_files_count": "Procesado {} archivo(s).",

        # Folder Cleaner
        "confirm_action_folders": "¿Estás seguro de que quieres {} {} carpeta(s)?",
        "processed_folders_count": "Procesado {} carpeta(s).",

        # Orphan Cleaner
        "found_orphans_count": "Encontrado {} SavedVariable(s) huérfano(s).",
        "confirm_action_orphans": "¿Estás seguro de que quieres {} {} SavedVariables huérfanos?",
        "processed_orphans_count": "Procesado {} huérfano(s).",

        # Actions
        "move_to_trash": "mover a la papelera",
        "delete_permanently_action": "eliminar permanentemente",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "Entradas de AddOns.txt reconstruidas.\nTotal escrito: {}\nTotal eliminado: {}",

        # Log Export
        "log_empty_nothing_export": "El registro está vacío. Nada que exportar.",

        # Settings Restore
        "settings_restored_restart": "Configuración restaurada a valores predeterminados. La aplicación se reiniciará ahora.",
        "settings_restored_manual": "Configuración restaurada a valores predeterminados. Por favor, reinicia la aplicación manualmente.",
        "failed_restore_defaults": "Error al restaurar valores predeterminados: {}",
        
        # File Cleaner
        
        # Folder Cleaner
        
        # Orphan Cleaner
        
        # Actions
        
        # AddOns.txt Rebuild
        
        # Log Export
        
        # Settings Restore
        
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
        "opt_sug_reinstall_title": "Reinstalar WoW (Instalación Limpia)",
        "opt_sug_reinstall_text": "Respalda tus carpetas AddOns y WTF, desinstala todas las versiones de WoW a través de Battle.net, reinstala y luego restaura tus respaldos. Esto elimina archivos heredados acumulados y datos obsoletos de años de parches.",
        "opt_sug_reinstall_tooltip": "POR QUÉ: Años de actualizaciones dejan archivos obsoletos, recursos deprecados y datos fragmentados que ralentizan la carga y desperdician espacio.\n\nNIVEL DE RIESGO: Bajo - Tus configuraciones/addons se conservan en carpetas WTF/AddOns.\n\nBENEFICIO ESPERADO: Tiempos de carga más rápidos, uso de disco reducido (5-15 GB ahorrados), estabilidad mejorada.\n\nCÓMO HACERLO: 1) Respaldar Interface\\AddOns y WTF\n2) Desinstalar vía Battle.net\n3) Reinstalar WoW\n4) Copiar carpetas respaldadas",
        
        # Help/About tab - content
        "help_version_label": "Herramienta de Limpieza de WoW {}",
        "help_about_description": "Un conjunto completo de mantenimiento y optimización para World of Warcraft.\nLimpia archivos innecesarios, administra addons, optimiza el rendimiento del juego y más.\n\nSiempre cierra World of Warcraft antes de usar esta herramienta.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Publicado bajo la Licencia Pública General GNU v3.0 (GPL-3.0-or-later). Consulta el archivo LICENSE incluido para los términos completos.",
        "support_patreon": "Apoyar en Patreon",
        "donate_paypal": "Donar vía PayPal",
        "github_repository": "Repositorio de GitHub",
        "github_issues": "Reportar problemas",

        
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
        "update_message": "¡Hay una nueva versión disponible!\n\nActual: {}\nÚltima: {}\n\n¿Quieres descargarla ahora?",
        "up_to_date": "Actualizado",
        "up_to_date_message": "Estás usando la última versión ({}).",
        "browser_open_error": "No se pudo abrir el navegador:\n\n{}",
        "download_update": "Descargar Actualización",
        "view_release": "Ver Versión",
        "later": "Más Tarde",
        "downloading_update": "Descargando Actualización",
        "downloading_update_file": "Descargando archivo de actualización...",
        "download_failed": "Descarga Fallida",
        "download_failed_message": "Error al descargar la actualización:\n\n{}",
        "update_ready": "Actualización Lista",
        "update_downloaded_message": "¡Actualización descargada correctamente!\n\nArchivo: {}\n\n¿Quieres instalarla ahora?",
        "install_now": "Instalar Ahora",
        "install_later": "Instalar Más Tarde",
        "update_location": "Descargado en: {}",
        "failed_to_fetch_release": "Error al obtener información de versión desde GitHub.",
        "no_download_available": "No se encontraron archivos descargables para esta versión.",
        "install_update": "Instalar Actualización",
        "please_run_installer": "Se ha abierto la ubicación de descarga.\n\nEjecuta el instalador para actualizar la aplicación.",
        "update_saved_message": "Actualización guardada en:\n\n{}\n\nPuedes instalarla más tarde.",
        
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
        "processed": "Processados {} {}.",        "restore_defaults_confirm": "Restaurar todas as configurações para os padrões?",
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
        "orphan_processed": "Limpador de Órfãos: processados {} órfão(s).",        "addons_txt_log": "[AddOns.txt] {}: escreveu {} entradas, removeu {}",
        "preset_applied_log": "Aplicada predefinição {} para {}",
        "preset_failed_log": "Falha ao aplicar predefinição {}: {}",
        "change_language": "Alterar Idioma",
        "change_language_question": "Alterar idioma de {} para {}?\n\nO aplicativo será reiniciado para aplicar o novo idioma.",
        "language_changed": "Idioma Alterado",
        "language_changed_restart": "Idioma alterado para {}.\nO aplicativo será reiniciado agora.",
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
        "process_selected_screenshots": "Processar Capturas de Tela Selecionadas",
        "no_screenshots_selected": "Nenhuma captura de tela selecionada.",
        "confirm_action_screenshots": "{} {} arquivo(s) de captura de tela?",
        "processed_screenshots_count": "{} captura(s) de tela processada(s).",
        "screenshots_per_file": "Capturas de Tela (ações por arquivo)",
        "folder_screenshots": "Capturas de Tela",
        "folder_logs": "Registros",
        "folder_errors": "Erros",
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
        "preview_hint": "(Clique na imagem para ampliar • Clique novamente ou pressione Esc para fechar)",
        "screenshots_not_found": "Pasta de Capturas de Tela não encontrada para esta versão.",
        
        # Main UI - Buttons and Messages
        "apply": "Aplicar",
        "cancel": "Cancelar",
        "export_log": "Exportar Registro",
        "clear_log": "Limpar Registro",
        
        # Common Messages
        "no_files_selected": "Nenhum arquivo selecionado",
        "no_folders_selected": "Nenhuma pasta selecionada",
        "no_orphans_selected": "Nenhum órfão selecionado",

        # Common Messages
        "apply_font_question": "Aplicar fonte '{}' ao aplicativo?",
        "select_valid_wow_first": "Por favor, selecione primeiro uma pasta WoW válida.",
        "restored": "Restaurado",

        # File Cleaner
        "found_files_count": "Encontrado {} arquivo(s) em todas as versões.",
        "confirm_action_files": "Tem certeza que deseja {} {} arquivo(s)?",
        "processed_files_count": "Processado {} arquivo(s).",

        # Folder Cleaner
        "confirm_action_folders": "Tem certeza que deseja {} {} pasta(s)?",
        "processed_folders_count": "Processado {} pasta(s).",

        # Orphan Cleaner
        "found_orphans_count": "Encontrado {} SavedVariable(s) órfão(s).",
        "confirm_action_orphans": "Tem certeza que deseja {} {} SavedVariables órfãos?",
        "processed_orphans_count": "Processado {} órfão(s).",

        # Actions
        "move_to_trash": "mover para lixeira",
        "delete_permanently_action": "excluir permanentemente",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "Entradas de AddOns.txt reconstruídas.\nTotal escrito: {}\nTotal removido: {}",

        # Log Export
        "log_empty_nothing_export": "O registro está vazio. Nada para exportar.",

        # Settings Restore
        "settings_restored_restart": "Configurações restauradas para padrões. O aplicativo será reiniciado agora.",
        "settings_restored_manual": "Configurações restauradas para padrões. Por favor, reinicie o aplicativo manualmente.",
        "failed_restore_defaults": "Falha ao restaurar padrões: {}",
        
        # File Cleaner
        
        # Folder Cleaner
        
        # Orphan Cleaner
        
        # Actions
        
        # AddOns.txt Rebuild
        
        # Log Export
        
        # Settings Restore
        
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
        "opt_sug_reinstall_title": "Reinstalar WoW (Instalação Limpa)",
        "opt_sug_reinstall_text": "Faça backup das suas pastas AddOns e WTF, desinstale todas as versões do WoW via Battle.net, reinstale e restaure seus backups. Isso remove arquivos legados acumulados e dados obsoletos de anos de patches.",
        "opt_sug_reinstall_tooltip": "POR QUE: Anos de atualizações deixam arquivos obsoletos, assets depreciados e dados fragmentados que desaceleram o carregamento e desperdiçam espaço.\n\nNÍVEL DE RISCO: Baixo - Suas configurações/addons são preservados nas pastas WTF/AddOns.\n\nBENEFÍCIO ESPERADO: Tempos de carregamento mais rápidos, uso de disco reduzido (5-15 GB economizados), estabilidade melhorada.\n\nCOMO FAZER: 1) Backup de Interface\\AddOns e WTF\n2) Desinstalar via Battle.net\n3) Reinstalar WoW\n4) Copiar pastas do backup",
        
        # Help/About tab - content
        "help_version_label": "Ferramenta de Limpeza do WoW {}",
        "help_about_description": "Um conjunto abrangente de manutenção e otimização para World of Warcraft.\nLimpe arquivos desnecessários, gerencie addons, otimize o desempenho do jogo e muito mais.\n\nSempre feche o World of Warcraft antes de usar esta ferramenta.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Lançado sob a Licença Pública Geral GNU v3.0 (GPL-3.0-or-later). Consulte o arquivo LICENSE incluído para os termos completos.",
        "support_patreon": "Apoiar no Patreon",
        "donate_paypal": "Doar via PayPal",
        "github_repository": "Repositório do GitHub",
        "github_issues": "Relatar problemas",

        
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
        "update_message": "Uma nova versão está disponível!\n\nAtual: {}\nÚltima: {}\n\nDeseja baixá-la agora?",
        "up_to_date": "Atualizado",
        "up_to_date_message": "Você está usando a última versão ({}).",
        "browser_open_error": "Não foi possível abrir o navegador:\n\n{}",
        "download_update": "Baixar Atualização",
        "view_release": "Ver Versão",
        "later": "Mais Tarde",
        "downloading_update": "Baixando Atualização",
        "downloading_update_file": "Baixando arquivo de atualização...",
        "download_failed": "Falha no Download",
        "download_failed_message": "Falha ao baixar a atualização:\n\n{}",
        "update_ready": "Atualização Pronta",
        "update_downloaded_message": "Atualização baixada com sucesso!\n\nArquivo: {}\n\nDeseja instalá-la agora?",
        "install_now": "Instalar Agora",
        "install_later": "Instalar Mais Tarde",
        "update_location": "Baixado em: {}",
        "failed_to_fetch_release": "Falha ao obter informações de versão do GitHub.",
        "no_download_available": "Nenhum arquivo disponível para download nesta versão.",
        "install_update": "Instalar Atualização",
        "please_run_installer": "O local de download foi aberto.\n\nExecute o instalador para atualizar o aplicativo.",
        "update_saved_message": "Atualização salva em:\n\n{}\n\nVocê pode instalá-la mais tarde.",
        
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
    
    "itIT": {
        # Window title
        "window_title": "Strumento di Pulizia WoW",
        
        # Menu/Tab names
        "file_cleaner": "Pulizia File",
        "folder_cleaner": "Pulizia Cartelle",
        "orphan_cleaner": "Pulizia Orfani",
        "game_optimizer": "Ottimizzazione Gioco",
        "optimization_suggestions": "Suggerimenti di Ottimizzazione",
        "log": "Registro",
        "help_about": "Aiuto/Info",
        
        # Options section
        "options": "Opzioni",
        "wow_folder": "Cartella WoW:",
        "browse": "Sfoglia...",
        "browse_tooltip": "Sfoglia la cartella di World of Warcraft.",
        "font_size": "Dimensione carattere:",
        "font": "Carattere:",
        "theme": "Tema:",
        "language": "Lingua:",
        "file_action": "Azione file:",
        "delete_permanently": "Elimina definitivamente",
        "move_to_recycle": "Sposta nel Cestino",
        "enable_verbose": "Abilita registro dettagliato",
        "verbose_tooltip": "Quando abilitato, il registro registra ogni file/cartella/riga di AddOns.txt elaborati.",
        "external_log": "Registro esterno:",
        "fresh": "Nuovo",
        "fresh_tooltip": "Crea un nuovo file di registro ad ogni esportazione (sovrascrive quello esistente).",
        "append": "Aggiungi",
        "append_tooltip": "Aggiunge ogni esportazione al file di registro esistente (mantiene 10-20 sessioni a seconda della verbosità).",
        "check_updates": "Verifica aggiornamenti",
        "check_updates_tooltip": "Quando abilitato, controlla le nuove versioni su GitHub all'avvio.",
        "restore_defaults": "Ripristina predefiniti",
        "light": "Chiaro",
        "dark": "Scuro",
        
        # File Cleaner
        "scan": "Scansiona",
        "select_all": "Seleziona tutto",
        "expand_all": "Espandi tutto",
        "collapse_all": "Comprimi tutto",
        "process_selected": "Elabora selezionati",
        "scanning": "Scansione in corso…",
        "no_bak_old_found": "Nessun file .bak o .old trovato.",
        "files_found": "{} file trovati.",
        
        # Folder Cleaner
        "version": "Versione:",
        "path": "Percorso:",
        "preview": "Anteprima",
        "toggle_all": "Commuta tutti",
        "process_folders": "Elabora cartelle selezionate",
        
        # Orphan Cleaner
        "rebuild_addons": "Ricostruisci AddOns.txt",
        "no_orphans_found": "Nessun SavedVariables orfano trovato.",
        "orphans_found": "{} SavedVariable orfani trovati.",
        
        # Game Optimizer
        "scan_hardware": "Scansiona hardware",
        "system_matches": "Il tuo sistema corrisponde a:",
        "optimization_applied": "✓ Ottimizzazione applicata",
        "optimization_not_applied": "⚠ Ottimizzazione non ancora applicata",
        "graphics_presets": "Preset grafici ({}):",
        "graphics_presets_classic": "Preset grafici ({}):",
        "apply_preset": "Applica preset:",
        "apply": "Applica",
        "preset_applied": "✓ Preset {} applicato.",
        "error": "✗ Errore: {}",
        "low": "Basso",
        "medium": "Medio",
        "high": "Alto",
        "ultra": "Ultra",
        
        # Optimization Suggestions
        "manual_suggestions": "Suggerimenti di Ottimizzazione Manuale",
        "manual_disclaimer": "Nota: questa applicazione NON esegue automaticamente queste ottimizzazioni. Questi sono suggerimenti che devi implementare manualmente.",
        "clean_data_folder": "Pulisci la cartella Data del gioco",
        "clean_data_text": "Se sono passati alcuni anni o diverse espansioni da quando hai installato WoW, considera di eliminare la cartella Data nella directory principale di World of Warcraft. Questo *potrebbe* ridurre la dimensione del gioco e migliorare le prestazioni dello schermo di caricamento. Il launcher Battle.net ricostruirà automaticamente questa cartella quando necessario.",
        "enable_hdr": "Abilita HDR (High Dynamic Range)",
        "enable_hdr_text": "Controlla le impostazioni di visualizzazione del sistema operativo per vedere se HDR è disponibile. Se il tuo monitor lo supporta, abilitare HDR può migliorare significativamente la chiarezza visiva e la profondità del colore nel gioco.",
        "verify_refresh": "Verifica la frequenza di aggiornamento del monitor",
        "verify_refresh_text": "Assicurati che la frequenza di aggiornamento del monitor sia impostata al massimo supportato nelle impostazioni di visualizzazione del sistema operativo. Frequenze più elevate forniscono un'esperienza di gioco più fluida e una migliore reattività.",
        "enable_sam": "Abilita Smart Access Memory/Resizable BAR",
        "enable_sam_text": "Controlla le impostazioni del BIOS della scheda madre per Smart Access Memory (AMD) o Resizable BAR (Intel/NVIDIA). L'abilitazione consente alla CPU di accedere all'intera memoria GPU, migliorando potenzialmente le prestazioni.",
        "enable_xmp": "Abilita profili memoria XMP",
        "enable_xmp_text": "Accedi al BIOS della scheda madre e abilita XMP (Extreme Memory Profile) o le impostazioni DOCP/EOCP. Questo assicura che la RAM funzioni alla sua velocità nominale invece della velocità predefinita conservativa, migliorando le prestazioni complessive del sistema.",
        
        # Log tab
        "export_log": "Esporta registro",
        "clear_log": "Cancella registro",
        
        # Help/About
        "about_text": "Suite completa di manutenzione e ottimizzazione per World of Warcraft.\nPulisci file non necessari, gestisci addon, ottimizza le prestazioni di gioco e altro.\n\nChiudi sempre World of Warcraft prima di eseguire questo strumento.",
        "copyright": "Copyright © 2025 Paul Vandersypen. Rilasciato sotto i termini della GNU General Public License v3.0 (GPL-3.0-or-later). Consulta il file LICENSE allegato per i termini completi.",
        
        # Dialogs
        "invalid_folder": "Cartella non valida",
        "select_valid_wow": "Seleziona prima una cartella WoW valida.",
        "no_selection": "Nessuna selezione",
        "no_files_selected": "Nessun file selezionato da elaborare.",
        "no_folders_selected": "Nessuna cartella selezionata da pulire.",
        "no_orphans_selected": "Nessun orfano selezionato.",
        "confirm": "Conferma",
        "confirm_action": "Sei sicuro di voler {} {} {}?",
        "file_s": " file",
        "folder_s": " cartelle",
        "orphaned_savedvars": " SavedVariables orfani",
        "completed": "Completato",
        "processed": "{} {} elaborati.",        "restore_defaults_confirm": "Ripristinare tutte le impostazioni ai valori predefiniti?",
        "restart_required": "Impostazioni ripristinate. L'applicazione verrà ora riavviata.",
        "error_title": "Errore",
        "restore_error": "Ripristino predefiniti fallito: {}",
        "confirm_font": "Conferma carattere",
        "apply_font_confirm": "Applicare il carattere '{}' all'applicazione?",
        "select_font": "Seleziona carattere",
        "export_log_title": "Esporta registro",
        "log_empty": "Il registro è vuoto. Niente da esportare.",
        "log_exported": "Registro esportato con successo in:\n{}",
        "export_error": "Errore esportazione",
        "export_failed": "Esportazione registro fallita:\n{}",
        "addons_rebuilt": "Voci AddOns.txt ricostruite.\nTotale scritte: {}\nTotale rimosse: {}",
        
        # Log messages
        "session_started": "Sessione avviata — {}",
        "file_scan": "Scansione pulizia file: {} corrispondenze.",
        "orphan_scan": "Scansione pulizia orfani: {} orfani.",
        "file_processed": "Pulizia file: {} file elaborati.",
        "folder_processed": "Pulizia cartelle: {} cartelle elaborate.",
        "orphan_processed": "Pulizia orfani: {} orfani elaborati.",        "addons_txt_log": "[AddOns.txt] {}: {} voci scritte, {} rimosse",
        "preset_applied_log": "Preset {} applicato per {}",
        "preset_failed_log": "Applicazione preset {} fallita: {}",
        "change_language": "Cambia lingua",
        "change_language_question": "Cambiare lingua da {} a {}?\n\nL\'applicazione verrà riavviata per applicare la nuova lingua.",
        "language_changed": "Lingua cambiata",
        "language_changed_restart": "Lingua cambiata in {}.\nL\'applicazione verrà ora riavviata.",
        "apply": "Applica",
        "cancel": "Annulla",
        "scan_bak_old": "Scansiona file .bak / .old",
        "expand_all": "Espandi tutto",
        "collapse_all": "Comprimi tutto",
        "select_deselect_all": "Seleziona/Deseleziona tutto",
        "process_selected_files": "Elabora file selezionati",
        "scan_orphaned": "Scansiona SavedVariables orfani",
        "process_selected_folders": "Elabora cartelle selezionate",
        "select_deselect_all_folders": "Seleziona/Deseleziona tutte le cartelle",
        "select_deselect_all_screenshots": "Seleziona/Deseleziona tutti gli screenshot",
        "process_selected_screenshots": "Elabora Screenshot Selezionati",
        "no_screenshots_selected": "Nessuno screenshot selezionato.",
        "confirm_action_screenshots": "{} {} file di screenshot?",
        "processed_screenshots_count": "{} screenshot elaborati.",
        "screenshots_per_file": "Screenshot (per azione file)",
        "folder_screenshots": "Screenshot",
        "folder_logs": "Registri",
        "folder_errors": "Errori",
        "check_for_updates": "Verifica aggiornamenti",
        
        # Game Optimizer
        "game_optimizer_title": "Ottimizzatore Gioco",
        "game_optimizer_desc": "Ottimizza le prestazioni di World of Warcraft in base alla tua configurazione hardware.",
        "scan_hardware": "Scansiona hardware",
        "click_scan_hardware": "Clicca 'Scansiona hardware' per rilevare le capacità del tuo sistema.",
        "select_valid_wow_folder": "Seleziona una cartella WoW valida nelle Opzioni per abilitare le visualizzazioni per versione.",
        "recommended_settings": "Impostazioni consigliate:",
        "apply_preset_label": "Applica preset:",
        "apply_recommended_settings": "Applica impostazioni consigliate",
        "scanning_cpu": "Scansione CPU in corso...",
        "scanning_ram": "Scansione RAM in corso... (CPU rilevata: {} core/{} thread)",
        "scanning_gpu": "Scansione GPU in corso... (RAM rilevata: {} GB)",
        
        # Startup warning
        "important_notice": "Avviso importante",
        "startup_warning_text": "⚠️ Prima di usare questo strumento, assicurati che World of Warcraft sia completamente chiuso.\n\nEseguire lo strumento mentre WoW è aperto potrebbe interferire con i file di gioco.",
        "do_not_show_again": "Non mostrare più questo avviso",
        "ok": "OK",
        
        # Folder cleaner
        "select_valid_wow_folder_cleaner": "Seleziona una cartella WoW valida nelle Opzioni per abilitare il Pulitore Cartelle.",
        "preview_label": "Anteprima",
        "preview_hint": "(Clicca sull'immagine per ingrandire • Clicca di nuovo o premi Esc per chiudere)",
        "screenshots_not_found": "Cartella Screenshot non trovata per questa versione.",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "Suggerimenti di Ottimizzazione Manuale",
        "opt_sug_disclaimer": "Nota: questa applicazione NON esegue automaticamente queste ottimizzazioni. Questi sono suggerimenti che devi implementare manualmente.",
        "opt_sug_clean_data_title": "Pulisci la cartella Data del gioco",
        "opt_sug_clean_data_text": "Se sono passati alcuni anni o diverse espansioni da quando hai installato WoW, considera di eliminare la cartella Data nella directory principale di World of Warcraft. Questo *potrebbe* ridurre la dimensione del gioco e migliorare le prestazioni dello schermo di caricamento. Il launcher Battle.net ricostruirà automaticamente questa cartella quando necessario.",
        "opt_sug_clean_data_tooltip": "Motivo: La cartella Data accumula risorse di gioco temporanee e in cache nel tempo. Eliminarla forza un nuovo download di file ottimizzati.\n\nLivello di rischio: Sicuro - Battle.net scaricherà automaticamente i file necessari.\n\nBenefici attesi: Schermate di caricamento più veloci, ridotto utilizzo disco (potenziale risparmio 10-20 GB).",
        "opt_sug_hdr_title": "Abilita HDR (High Dynamic Range)",
        "opt_sug_hdr_text": "Controlla le impostazioni di visualizzazione del sistema operativo per vedere se HDR è disponibile. Se il tuo monitor lo supporta, abilitare HDR può migliorare significativamente la chiarezza visiva e la profondità del colore nel gioco.",
        "opt_sug_hdr_tooltip": "Motivo: HDR offre una gamma di colori più ampia e un migliore contrasto, rendendo gli effetti visivi più vividi e realistici.\n\nLivello di rischio: Sicuro - facilmente attivabile/disattivabile nelle impostazioni OS.\n\nBenefici attesi: Miglioramento significativo della qualità visiva se il monitor supporta HDR10 o superiore.\n\nRequisiti: Monitor compatibile HDR e Windows 10/11 o macOS Catalina+.",
        "opt_sug_refresh_title": "Verifica la frequenza di aggiornamento del monitor",
        "opt_sug_refresh_text": "Assicurati che la frequenza di aggiornamento del monitor sia impostata al massimo supportato nelle impostazioni di visualizzazione del sistema operativo. Frequenze più elevate forniscono un'esperienza di gioco più fluida e una migliore reattività.",
        "opt_sug_refresh_tooltip": "Motivo: Molti sistemi impostano di default 60Hz anche se i monitor supportano 120Hz/144Hz/165Hz. Questo limita inutilmente la frequenza dei fotogrammi.\n\nLivello di rischio: Sicuro - nessun rischio hardware, facile da ripristinare.\n\nBenefici attesi: Gameplay più fluido, riduzione latenza input, miglior tempo di risposta.\n\nCome verificare: Windows: Impostazioni > Display > Avanzate > Frequenza di aggiornamento\nmacOS: Preferenze di Sistema > Monitor",
        "opt_sug_sam_title": "Abilita Smart Access Memory/Resizable BAR",
        "opt_sug_sam_text": "Controlla le impostazioni del BIOS della scheda madre per Smart Access Memory (AMD) o Resizable BAR (Intel/NVIDIA). L'abilitazione consente alla CPU di accedere all'intera memoria GPU, migliorando potenzialmente le prestazioni.",
        "opt_sug_sam_tooltip": "Motivo: Consente alla CPU di accedere all'intera memoria GPU in una volta, invece di piccoli blocchi da 256MB, riducendo i colli di bottiglia.\n\nLivello di rischio: Moderato - richiede modifiche al BIOS. Annota prima le impostazioni attuali.\n\nBenefici attesi: Aumento FPS 5-15% in scene intensive GPU.\n\nRequisiti:\n• AMD: CPU Ryzen 5000+ + GPU RX 6000+\n• Intel: CPU 10a gen+ + GPU RTX 3000+\n• Potrebbe richiedere aggiornamento BIOS",
        "opt_sug_xmp_title": "Abilita profili memoria XMP",
        "opt_sug_xmp_text": "Accedi al BIOS della scheda madre e abilita XMP (Extreme Memory Profile) o le impostazioni DOCP/EOCP. Questo assicura che la RAM funzioni alla sua velocità nominale invece della velocità predefinita conservativa, migliorando le prestazioni complessive del sistema.",
        "opt_sug_xmp_tooltip": "Motivo: La RAM spesso funziona a 2133MHz di default anche se è valutata per 3200MHz+. XMP abilita le velocità pubblicizzate.\n\nLivello di rischio: Moderato - modifica BIOS. Il sistema potrebbe non avviarsi se la RAM è instabile (facile da resettare).\n\nBenefici attesi: Aumento prestazioni CPU 10-20%, caricamenti più veloci, migliori 1% low.\n\nCome abilitare: Accedi al BIOS (di solito Canc/F2 all'avvio) > Trova impostazioni XMP/DOCP > Abilita > Salva ed esci",
        "opt_sug_reinstall_title": "Reinstalla WoW (Installazione pulita)",
        "opt_sug_reinstall_text": "Fai il backup delle cartelle AddOns e WTF, disinstalla tutte le versioni di WoW tramite Battle.net, reinstalla e ripristina i backup. Questo rimuove file legacy accumulati e dati obsoleti da anni di patch.",
        "opt_sug_reinstall_tooltip": "Motivo: Anni di aggiornamenti lasciano file obsoleti, risorse deprecate e dati frammentati che rallentano il caricamento e sprecano spazio.\n\nLivello di rischio: Basso - Le impostazioni/addon sono preservati nelle cartelle WTF/AddOns.\n\nBenefici attesi: Caricamenti più veloci, uso disco ridotto (5-15 GB risparmiati), stabilità migliorata.\n\nCome fare: 1) Backup di Interface\\AddOns e WTF\n2) Disinstalla tramite Battle.net\n3) Reinstalla WoW\n4) Copia le cartelle di backup",
        
        # Help/About tab - content
        "help_version_label": "Strumento di Pulizia WoW {}",
        "help_about_description": "Suite completa di manutenzione e ottimizzazione per World of Warcraft.\nPulisci file non necessari, gestisci addon, ottimizza le prestazioni di gioco e altro.\n\nChiudi sempre World of Warcraft prima di eseguire questo strumento.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Rilasciato sotto i termini della GNU General Public License v3.0 (GPL-3.0-or-later). Consulta il file LICENSE allegato per i termini completi.",
        "support_patreon": "Supporta su Patreon",
        "donate_paypal": "Dona tramite PayPal",
        "github_repository": "Repository GitHub",
        "github_issues": "Segnala problemi",

        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU: {} | RAM: {} | GPU: {}",
        "gpu_switch_notification": "⚠ Cambio GPU: Impostato per usare '{}' invece di '{}'. Questa modifica ottimizza le prestazioni utilizzando la tua GPU dedicata per una migliore esperienza di gioco. È sicuro e consigliato.",
        "scan_tooltip_refresh": "Non è necessario scansionare di nuovo a meno che non hai modificato CPU, GPU o RAM.\nClicca per aggiornare le informazioni hardware nella cache.",
        "scanning_ram_detected": "Scansione RAM in corso... (CPU rilevata: {} core/{} thread)",
        "scanning_gpu_detected": "Scansione GPU in corso... (RAM rilevata: {} GB)",
        "apply_preset_label": "Applica preset:",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "WoW in esecuzione",
        "wow_running_message": "World of Warcraft è attualmente in esecuzione. Le modifiche avranno effetto dopo il riavvio del gioco.\n\nVuoi continuare?",
        "permission_error_title": "Errore permessi",
        "permission_error_message": "Config.wtf è in sola lettura. Rimuovi l'attributo di sola lettura e riprova.",
        "config_readonly_status": "✗ Config.wtf è in sola lettura.",
        "confirm_apply_title": "Conferma applicazione",
        "confirm_apply_message": "Applicare il preset {} a {}?\n\nQuesto modificherà {} impostazioni grafiche in Config.wtf.\nVerrà creato automaticamente un backup.\n\nModifiche principali:\n• Preset: Impostazioni qualità {}\n• Prestazioni: {} ottimizzazioni",
        "cancelled_by_user": "Annullato dall'utente.",
        "settings_applied_status": "✓ {} impostazioni applicate.",
        "preset_applied_status": "✓ Preset {} applicato.",
        "apply_error_status": "✗ Errore: {}",
        
        # Preset tooltips
        "preset_tooltip_template": "Preset {}\n\nPrestazioni attese:\n{}\n\nClicca 'Applica' qui sotto per usare questo preset.",
        "perf_depends_hardware": "L'impatto sulle prestazioni dipende dal tuo hardware.",
        "perf_will_vary": "Le prestazioni varieranno",
        
        # Low preset performance estimates
        "low_perf_high": "Prestazioni eccellenti (100+ FPS nella maggior parte degli scenari)",
        "low_perf_mid": "Prestazioni molto buone (80-120 FPS)",
        "low_perf_low": "Buone prestazioni (60-80 FPS)",
        
        # Medium preset performance estimates
        "medium_perf_high": "Prestazioni eccellenti (90-120 FPS)",
        "medium_perf_mid": "Buone prestazioni (60-90 FPS)",
        "medium_perf_low": "Prestazioni moderate (45-60 FPS)",
        
        # High preset performance estimates
        "high_perf_high": "Prestazioni molto buone (70-100 FPS)",
        "high_perf_mid": "Buone prestazioni (50-70 FPS)",
        "high_perf_low": "Potrebbe avere difficoltà in raid (30-50 FPS)",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "Buone prestazioni (60-80 FPS)",
        "ultra_perf_mid": "Prestazioni moderate (40-60 FPS)",
        "ultra_perf_low": "Prestazioni inferiori (20-40 FPS)",
        
        # WoW version names
        "version_retail": "Retail",
        "version_classic": "Classic",
        "version_classic_era": "Classic Era",
        "version_ptr": "PTR",
        "version_beta": "Beta",
        
        # Game Optimizer - additional strings
        "not_detected": "Non rilevato",
        "unknown_cpu": "CPU sconosciuta",
        "unknown_gpu": "Sconosciuta",
        "not_set": "Non impostato",
        "hover_for_details": "Passa sopra per i dettagli",
        
        # Orphan Cleaner - log messages
        "orphan_found_in": "[Pulizia Orfani] Trovato orfano in {0}: {1}",
        "orphan_total_found": "[Pulizia Orfani] Totale SavedVariables orfani: {0}",
        "orphan_moved_trash": "[Pulizia Orfani] Spostato nel cestino: {0}",
        "orphan_deleted": "[Pulizia Orfani] Eliminato: {0}",
        "orphan_error_deleting": "[Pulizia Orfani] Errore eliminazione {0}: {1}",
        "orphan_rebuilt_addons": "[Pulizia Orfani] Ricostruito: {0}",
        "orphan_error_writing_addons": "[Pulizia Orfani] Errore scrittura AddOns.txt {0}: {1}",
        "orphan_error_rebuild": "[Pulizia Orfani] Errore durante ricostruzione AddOns.txt: {0}",
        "new_setting_prefix": "[Nuovo] ",
        "details_colon": "Dettagli:",
        "updated_settings": "• Aggiornate {} impostazioni esistenti",
        "added_settings": "• Aggiunte {} nuove impostazioni",
        
        # Path Manager
        "select_wow_folder_title": "Seleziona cartella WoW",
        "unrecognized_installation": "Installazione non riconosciuta",
        "folder_not_valid_continue": "La cartella selezionata sembra non valida.\n\nVuoi continuare comunque?",
        "wow_folder_set": "Cartella WoW impostata: {}",
        
        # Performance
        "performance_execution_time": "[Prestazioni] {} ha richiesto {:.3f} secondi",
        "perf_moved_trash": "[{}] Spostato nel cestino: {}",
        "perf_deleted": "[{}] Eliminato: {}",
        "perf_error_deleting": "[{}] Errore eliminazione {}: {}",
        
        "select_valid_wow_optimizer": "Seleziona una cartella WoW valida nelle Opzioni per abilitare le visualizzazioni per versione.",
        "select_valid_wow_folder_cleaner": "Seleziona una cartella WoW valida nelle Opzioni per abilitare il Pulitore Cartelle.",
        
        # Main UI - Buttons and Messages
        "apply": "Applica",
        "cancel": "Annulla",
        "export_log": "Esporta registro",
        "clear_log": "Cancella registro",
        
        # Common Messages
        "no_files_selected": "Nessun file selezionato",
        "no_folders_selected": "Nessuna cartella selezionata",
        "no_orphans_selected": "Nessun orfano selezionato",

        # Common Messages
        "apply_font_question": "Applicare il carattere '{}' all'applicazione?",
        "select_valid_wow_first": "Si prega di selezionare prima una cartella WoW valida.",
        "restored": "Ripristinato",

        # File Cleaner
        "found_files_count": "Trovato {} file in tutte le versioni.",
        "confirm_action_files": "Sei sicuro di voler {} {} file?",
        "processed_files_count": "Elaborato {} file.",

        # Folder Cleaner
        "confirm_action_folders": "Sei sicuro di voler {} {} cartelle?",
        "processed_folders_count": "Elaborato {} cartelle.",

        # Orphan Cleaner
        "found_orphans_count": "Trovato {} SavedVariable orfano/i.",
        "confirm_action_orphans": "Sei sicuro di voler {} {} SavedVariables orfani?",
        "processed_orphans_count": "Elaborato {} orfano/i.",

        # Actions
        "move_to_trash": "spostare nel cestino",
        "delete_permanently_action": "eliminare permanentemente",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "Voci AddOns.txt ricostruite.\nTotale scritto: {}\nTotale rimosso: {}",

        # Log Export
        "log_empty_nothing_export": "Il registro è vuoto. Niente da esportare.",

        # Settings Restore
        "settings_restored_restart": "Impostazioni ripristinate ai valori predefiniti. L'applicazione verrà riavviata ora.",
        "settings_restored_manual": "Impostazioni ripristinate ai valori predefiniti. Si prega di riavviare l'applicazione manualmente.",
        "failed_restore_defaults": "Impossibile ripristinare i valori predefiniti: {}",
        
        # File Cleaner
        
        # Folder Cleaner
        
        # Orphan Cleaner
        
        # Actions
        
        # AddOns.txt Rebuild
        
        # Log Export
        
        # Settings Restore
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "Cerca SavedVariables di addon (.lua / .lua.bak) senza addon installato corrispondente (Interface/AddOns) in tutte le versioni WoW rilevate. Scansiona cartelle SavedVariables di account, server e personaggi. L'elaborazione ricostruisce anche AddOns.txt per corrispondere agli addon installati (preservando lo stato abilitato/disabilitato quando possibile).",
        "orphan_description_part2": "Nota: I file Blizzard_*.lua sono dati del gioco core e vengono automaticamente ignorati per sicurezza (ma i loro backup .lua.bak potrebbero essere eliminati).",
        "wtf_not_found": "Directory WTF non trovata. Avvia prima il gioco.",
        "unknown_preset": "Preset sconosciuto: {}",
        "backup_failed": "Creazione backup fallita: {}",
        "config_write_failed": "Scrittura configurazione fallita: {}",
        "config_updated": "{} impostazioni applicate a Config.wtf.",
        "settings_updated_added": "{} impostazioni aggiornate, {} nuove impostazioni aggiunte.",
        "backup_saved": " Backup salvato.",
        "version_path": "Versione: {}\nPercorso: {}",
        "optimizer_launch_required": "L'ottimizzatore richiede che {} sia stato avviato almeno una volta. Avvia WoW e raggiungi la schermata di selezione personaggio, poi esci dal gioco. Dopo di che, potrai usare l'ottimizzatore per applicare i preset grafici.",
        "system_matches": "Il tuo sistema corrisponde a: {}",
        "optimizer_title": "Ottimizzatore — {}",
        "recommendations_applied": "✓ Impostazioni consigliate applicate.",
        "applied_preset_log": "Preset {} applicato per {}",
        "apply_preset_failed_log": "Applicazione preset {} fallita: {}",
        "hardware_scan_complete": "Scansione hardware completata: salvato nelle impostazioni globali.",
        "hardware_scan_failed": "Scansione hardware fallita: {}",
        "scan_error": "✗ Errore: {}",
        
        # Game Validation
        "invalid_game_installation": "Installazione gioco non valida",
        "game_installation_incomplete": "L'installazione di World of Warcraft sembra incompleta.\n\nEsegui il gioco almeno una volta per inizializzare le cartelle Interface e WTF.\n\nDopo aver eseguito il gioco, potrai usare questo strumento per pulire la tua installazione.",
        
        # Startup Warning
        "user_disabled_warning": "L'utente ha disabilitato l'avviso di avvio.",
        
        # Update Checker
        "no_updates_available": "Nessun aggiornamento disponibile",
        "no_releases_published": "Stai eseguendo {}.\n\nNessuna release pubblicata ancora.",
        "update_check_failed": "Verifica aggiornamento fallita",
        "update_check_http_error": "Impossibile verificare aggiornamenti:\n\nHTTP {}: {}",
        "update_check_network_error": "Impossibile verificare aggiornamenti:\n\n{}",
        "update_check_error": "Errore verifica aggiornamento",
        "update_check_exception": "Errore durante verifica aggiornamenti:\n\n{}",
        "update_available": "Aggiornamento disponibile",
        "update_message": "È disponibile una nuova versione!\n\nVersione attuale: {}\nUltima versione: {}\n\nVuoi scaricarla ora?",
        "up_to_date": "Aggiornato",
        "up_to_date_message": "Stai eseguendo l'ultima versione ({}).",
        "browser_open_error": "Impossibile aprire il browser:\n\n{}",
        "download_update": "Scarica aggiornamento",
        "view_release": "Visualizza versione",
        "later": "Più tardi",
        "downloading_update": "Download aggiornamento",
        "downloading_update_file": "Download del file di aggiornamento...",
        "download_failed": "Download fallito",
        "download_failed_message": "Impossibile scaricare l'aggiornamento:\n\n{}",
        "update_ready": "Aggiornamento pronto",
        "update_downloaded_message": "Aggiornamento scaricato con successo!\n\nFile: {}\n\nVuoi installarlo ora?",
        "install_now": "Installa ora",
        "install_later": "Installa più tardi",
        "update_location": "Scaricato in: {}",
        "failed_to_fetch_release": "Impossibile recuperare le informazioni sulla versione da GitHub.",
        "no_download_available": "Nessun file scaricabile trovato per questa versione.",
        "install_update": "Installa aggiornamento",
        "please_run_installer": "La posizione di download è stata aperta.\n\nEsegui il programma di installazione per aggiornare l'applicazione.",
        "update_saved_message": "Aggiornamento salvato in:\n\n{}\n\nPuoi installarlo più tardi.",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[Pulizia File] Trovato file: {}",
        "file_cleaner_found": "[Pulizia File] Trovato: {}",
        "file_cleaner_total_found": "[Pulizia File] Totale file .bak/.old trovati: {}",
        "file_cleaner_moved_trash": "[Pulizia File] Spostato nel cestino: {}",
        "file_cleaner_deleted": "[Pulizia File] Eliminato: {}",
        "file_cleaner_error_deleting": "[Pulizia File] Errore eliminazione {}: {}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[Pulizia Cartelle] Trovato: {}",
        "folder_cleaner_total": "[Pulizia Cartelle] Totale cartelle pulibili: {}",
    },
    "ruRU": {
        # Window title
        "window_title": "Утилита Очистки WoW",
        
        # Menu/Tab names
        "file_cleaner": "Очистка Файлов",
        "folder_cleaner": "Очистка Папок",
        "orphan_cleaner": "Очистка Сирот",
        "game_optimizer": "Оптимизация Игры",
        "optimization_suggestions": "Советы по Оптимизации",
        "log": "Журнал",
        "help_about": "Справка/О программе",
        
        # Options section
        "options": "Параметры",
        "wow_folder": "Папка WoW:",
        "browse": "Обзор...",
        "browse_tooltip": "Выберите папку World of Warcraft.",
        "font_size": "Размер шрифта:",
        "font": "Шрифт:",
        "theme": "Тема:",
        "language": "Язык:",
        "file_action": "Действие с файлами:",
        "delete_permanently": "Удалить навсегда",
        "move_to_recycle": "Переместить в Корзину",
        "enable_verbose": "Подробный журнал",
        "verbose_tooltip": "При включении журнал записывает каждый обработанный файл/папку/строку AddOns.txt.",
        "external_log": "Внешний журнал:",
        "fresh": "Новый",
        "fresh_tooltip": "Создавать новый файл журнала при каждом экспорте (перезаписывает существующий).",
        "append": "Добавить",
        "append_tooltip": "Добавлять каждый экспорт к существующему файлу журнала (сохраняет 10-20 сеансов в зависимости от подробности).",
        "check_updates": "Проверять обновления",
        "check_updates_tooltip": "При включении проверяет наличие новых версий на GitHub при запуске.",
        "restore_defaults": "Восстановить настройки",
        "light": "Светлая",
        "dark": "Тёмная",
        
        # File Cleaner
        "scan": "Сканировать",
        "select_all": "Выбрать всё",
        "expand_all": "Развернуть всё",
        "collapse_all": "Свернуть всё",
        "process_selected": "Обработать выбранное",
        "scanning": "Сканирование…",
        "no_bak_old_found": "Файлы .bak или .old не найдены.",
        "files_found": "Найдено файлов: {}.",
        
        # Folder Cleaner
        "version": "Версия:",
        "path": "Путь:",
        "preview": "Предпросмотр",
        "toggle_all": "Переключить всё",
        "process_folders": "Обработать выбранные папки",
        
        # Orphan Cleaner
        "rebuild_addons": "Перестроить AddOns.txt",
        "no_orphans_found": "Осиротевших SavedVariables не найдено.",
        "orphans_found": "Найдено {} осиротевших SavedVariables.",
        
        # Game Optimizer
        "scan_hardware": "Сканировать оборудование",
        "system_matches": "Ваша система соответствует:",
        "optimization_applied": "✓ Оптимизация применена",
        "optimization_not_applied": "⚠ Оптимизация ещё не применена",
        "graphics_presets": "Графические пресеты ({}):",
        "graphics_presets_classic": "Графические пресеты ({}):",
        "apply_preset": "Применить пресет:",
        "apply": "Применить",
        "preset_applied": "✓ Пресет {} применён.",
        "error": "✗ Ошибка: {}",
        "low": "Низкие",
        "medium": "Средние",
        "high": "Высокие",
        "ultra": "Ультра",
        
        # Optimization Suggestions
        "manual_suggestions": "Рекомендации по Ручной Оптимизации",
        "manual_disclaimer": "Примечание: это приложение НЕ выполняет эти оптимизации автоматически. Это рекомендации, которые вы должны реализовать вручную.",
        "clean_data_folder": "Очистить папку Data игры",
        "clean_data_text": "Если прошло несколько лет или дополнений с момента установки WoW, рассмотрите возможность удаления папки Data в главном каталоге World of Warcraft. Это *может* уменьшить размер игры и улучшить производительность экрана загрузки. Лаунчер Battle.net автоматически восстановит эту папку при необходимости.",
        "enable_hdr": "Включить HDR (расширенный динамический диапазон)",
        "enable_hdr_text": "Проверьте настройки дисплея операционной системы, доступен ли HDR. Если ваш монитор поддерживает его, включение HDR может значительно улучшить визуальную чёткость и глубину цвета в игре.",
        "verify_refresh": "Проверьте частоту обновления монитора",
        "verify_refresh_text": "Убедитесь, что частота обновления монитора установлена на максимально поддерживаемую в настройках дисплея операционной системы. Более высокая частота обеспечивает более плавный игровой процесс и лучшую отзывчивость.",
        "enable_sam": "Включить Smart Access Memory/Resizable BAR",
        "enable_sam_text": "Проверьте настройки BIOS материнской платы на наличие Smart Access Memory (AMD) или Resizable BAR (Intel/NVIDIA). Включение позволяет процессору получать доступ ко всей памяти GPU, потенциально улучшая производительность.",
        "enable_xmp": "Включить профили памяти XMP",
        "enable_xmp_text": "Войдите в BIOS материнской платы и включите XMP (Extreme Memory Profile) или настройки DOCP/EOCP. Это гарантирует, что ваша оперативная память работает на номинальной скорости вместо консервативной скорости по умолчанию, улучшая общую производительность системы.",
        
        # Log tab
        "export_log": "Экспортировать журнал",
        "clear_log": "Очистить журнал",
        
        # Help/About
        "about_text": "Комплексный набор инструментов для обслуживания и оптимизации World of Warcraft.\nОчищайте ненужные файлы, управляйте аддонами, оптимизируйте производительность игры и многое другое.\n\nВсегда закрывайте World of Warcraft перед запуском этой утилиты.",
        "copyright": "Авторские права © 2025 Paul Vandersypen. Выпущено на условиях GNU General Public License v3.0 (GPL-3.0-or-later). Полные условия см. в прилагаемом файле LICENSE.",
        
        # Dialogs
        "invalid_folder": "Недействительная папка",
        "select_valid_wow": "Пожалуйста, сначала выберите действительную папку WoW.",
        "no_selection": "Нет выбора",
        "no_files_selected": "Файлы для обработки не выбраны.",
        "no_folders_selected": "Папки для очистки не выбраны.",
        "no_orphans_selected": "Осиротевшие файлы не выбраны.",
        "confirm": "Подтверждение",
        "confirm_action": "Вы уверены, что хотите {} {} {}?",
        "file_s": " файл(ов)",
        "folder_s": " папок(и)",
        "orphaned_savedvars": " осиротевших SavedVariables",
        "completed": "Завершено",
        "processed": "Обработано {} {}.",        "restore_defaults_confirm": "Восстановить все настройки по умолчанию?",
        "restart_required": "Настройки восстановлены. Приложение будет перезапущено.",
        "error_title": "Ошибка",
        "restore_error": "Не удалось восстановить настройки по умолчанию: {}",
        "confirm_font": "Подтвердить шрифт",
        "apply_font_confirm": "Применить шрифт '{}' к приложению?",
        "select_font": "Выбрать шрифт",
        "export_log_title": "Экспорт журнала",
        "log_empty": "Журнал пуст. Нечего экспортировать.",
        "log_exported": "Журнал успешно экспортирован в:\n{}",
        "export_error": "Ошибка экспорта",
        "export_failed": "Не удалось экспортировать журнал:\n{}",
        "addons_rebuilt": "Записи AddOns.txt перестроены.\nВсего записано: {}\nВсего удалено: {}",
        
        # Log messages
        "session_started": "Сеанс начат — {}",
        "file_scan": "Сканирование очистки файлов: {} совпадений.",
        "orphan_scan": "Сканирование очистки сирот: {} сирот.",
        "file_processed": "Очистка файлов: обработано {} файлов.",
        "folder_processed": "Очистка папок: обработано {} папок.",
        "orphan_processed": "Очистка сирот: обработано {} сирот.",        "addons_txt_log": "[AddOns.txt] {}: записано {}, удалено {}",
        "preset_applied_log": "Пресет {} применён для {}",
        "preset_failed_log": "Не удалось применить пресет {}: {}",
        "change_language": "Изменить язык",
        "change_language_question": "Изменить язык с {} на {}?\n\nПриложение будет перезапущено для применения нового языка.",
        "language_changed": "Язык изменён",
        "language_changed_restart": "Язык изменён на {}.\nПриложение будет перезапущено.",
        
        # Additional buttons and UI elements
        "apply": "Применить",
        "cancel": "Отмена",
        "scan_bak_old": "Сканировать файлы .bak / .old",
        "expand_all": "Развернуть всё",
        "collapse_all": "Свернуть всё",
        "select_deselect_all": "Выбрать/Снять выбор со всех",
        "process_selected_files": "Обработать выбранные файлы",
        "scan_orphaned": "Сканировать осиротевшие SavedVariables",
        "process_selected_folders": "Обработать выбранные папки",
        "select_deselect_all_folders": "Выбрать/Снять выбор со всех папок",
        "select_deselect_all_screenshots": "Выбрать/Снять выбор со всех скриншотов",
        "process_selected_screenshots": "Обработать выбранные скриншоты",
        "no_screenshots_selected": "Скриншоты не выбраны.",
        "confirm_action_screenshots": "{} {} файл(ов) скриншотов?",
        "processed_screenshots_count": "Обработано {} скриншот(ов).",
        "screenshots_per_file": "Скриншоты (для действия с файлами)",
        "folder_screenshots": "Скриншоты",
        "folder_logs": "Журналы",
        "folder_errors": "Ошибки",
        "check_for_updates": "Проверить обновления",
        
        # Game Optimizer
        "game_optimizer_title": "Оптимизатор Игры",
        "game_optimizer_desc": "Оптимизируйте производительность World of Warcraft на основе вашей аппаратной конфигурации.",
        "scan_hardware": "Сканировать оборудование",
        "click_scan_hardware": "Нажмите 'Сканировать оборудование', чтобы определить возможности вашей системы.",
        "select_valid_wow_folder": "Выберите действительную папку WoW в Параметрах, чтобы включить просмотр по версиям.",
        "recommended_settings": "Рекомендуемые настройки:",
        "apply_preset_label": "Применить пресет:",
        "apply_recommended_settings": "Применить рекомендуемые настройки",
        "scanning_cpu": "Сканирование процессора...",
        "scanning_ram": "Сканирование ОЗУ... (обнаружен процессор: {} ядер/{} потоков)",
        "scanning_gpu": "Сканирование видеокарты... (обнаружено ОЗУ: {} ГБ)",
        
        # Startup warning
        "important_notice": "Важное уведомление",
        "startup_warning_text": "⚠️ Перед использованием этой утилиты убедитесь, что World of Warcraft полностью закрыт.\n\nЗапуск утилиты при открытом WoW может помешать работе файлов игры.",
        "do_not_show_again": "Больше не показывать это предупреждение",
        "ok": "ОК",
        
        # Folder cleaner
        "select_valid_wow_folder_cleaner": "Выберите действительную папку WoW в Параметрах, чтобы включить Очистку Папок.",
        "preview_label": "Предпросмотр",
        "preview_hint": "(Нажмите на изображение для увеличения • Нажмите снова или нажмите Esc для закрытия)",
        "screenshots_not_found": "Папка Screenshots не найдена для этой версии.",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "Рекомендации по Ручной Оптимизации",
        "opt_sug_disclaimer": "Примечание: это приложение НЕ выполняет эти оптимизации автоматически. Это рекомендации, которые вы должны реализовать вручную.",
        "opt_sug_clean_data_title": "Очистить папку Data игры",
        "opt_sug_clean_data_text": "Если прошло несколько лет или дополнений с момента установки WoW, рассмотрите возможность удаления папки Data в главном каталоге World of Warcraft. Это *может* уменьшить размер игры и улучшить производительность экрана загрузки. Лаунчер Battle.net автоматически восстановит эту папку при необходимости.",
        "opt_sug_clean_data_tooltip": "Причина: Папка Data со временем накапливает временные и кэшированные игровые ресурсы. Её удаление заставляет загрузить оптимизированные файлы заново.\n\nУровень риска: Безопасно - Battle.net автоматически загрузит необходимые файлы.\n\nОжидаемые преимущества: Более быстрая загрузка экранов, меньшее использование диска (потенциальная экономия 10-20 ГБ).",
        "opt_sug_hdr_title": "Включить HDR (расширенный динамический диапазон)",
        "opt_sug_hdr_text": "Проверьте настройки дисплея операционной системы, доступен ли HDR. Если ваш монитор поддерживает его, включение HDR может значительно улучшить визуальную чёткость и глубину цвета в игре.",
        "opt_sug_hdr_tooltip": "Причина: HDR обеспечивает более широкую цветовую гамму и лучшую контрастность, делая визуальные эффекты более яркими и реалистичными.\n\nУровень риска: Безопасно - легко включается/выключается в настройках ОС.\n\nОжидаемые преимущества: Значительное улучшение визуального качества, если монитор поддерживает HDR10 или выше.\n\nТребования: Монитор с поддержкой HDR и Windows 10/11 или macOS Catalina+.",
        "opt_sug_refresh_title": "Проверьте частоту обновления монитора",
        "opt_sug_refresh_text": "Убедитесь, что частота обновления монитора установлена на максимально поддерживаемую в настройках дисплея операционной системы. Более высокая частота обеспечивает более плавный игровой процесс и лучшую отзывчивость.",
        "opt_sug_refresh_tooltip": "Причина: Многие системы по умолчанию устанавливают 60 Гц, даже если мониторы поддерживают 120 Гц/144 Гц/165 Гц. Это без необходимости ограничивает частоту кадров.\n\nУровень риска: Безопасно - нет риска для оборудования, легко вернуть.\n\nОжидаемые преимущества: Более плавный игровой процесс, меньшая задержка ввода, лучшее время отклика.\n\nКак проверить: Windows: Параметры > Дисплей > Дополнительно > Частота обновления\nmacOS: Системные настройки > Мониторы",
        "opt_sug_sam_title": "Включить Smart Access Memory/Resizable BAR",
        "opt_sug_sam_text": "Проверьте настройки BIOS материнской платы на наличие Smart Access Memory (AMD) или Resizable BAR (Intel/NVIDIA). Включение позволяет процессору получать доступ ко всей памяти GPU, потенциально улучшая производительность.",
        "opt_sug_sam_tooltip": "Причина: Позволяет процессору получать доступ ко всей памяти GPU за раз, вместо небольших блоков по 256 МБ, уменьшая узкие места.\n\nУровень риска: Средний - требует изменения BIOS. Сначала запишите текущие настройки.\n\nОжидаемые преимущества: Увеличение FPS на 5-15% в GPU-интенсивных сценах.\n\nТребования:\n• AMD: Процессор Ryzen 5000+ + видеокарта RX 6000+\n• Intel: Процессор 10-го поколения+ + видеокарта RTX 3000+\n• Может потребоваться обновление BIOS",
        "opt_sug_xmp_title": "Включить профили памяти XMP",
        "opt_sug_xmp_text": "Войдите в BIOS материнской платы и включите XMP (Extreme Memory Profile) или настройки DOCP/EOCP. Это гарантирует, что ваша оперативная память работает на номинальной скорости вместо консервативной скорости по умолчанию, улучшая общую производительность системы.",
        "opt_sug_xmp_tooltip": "Причина: ОЗУ часто работает на частоте 2133 МГц по умолчанию, даже если рассчитана на 3200 МГц+. XMP включает заявленные скорости.\n\nУровень риска: Средний - изменение BIOS. Система может не загрузиться, если ОЗУ нестабильна (легко сбросить).\n\nОжидаемые преимущества: Увеличение производительности процессора на 10-20%, более быстрая загрузка, лучшие 1% минимумы.\n\nКак включить: Войдите в BIOS (обычно Del/F2 при загрузке) > Найдите настройки XMP/DOCP > Включите > Сохраните и выйдите",
        "opt_sug_reinstall_title": "Переустановить WoW (Чистая установка)",
        "opt_sug_reinstall_text": "Создайте резервные копии папок AddOns и WTF, удалите все версии WoW через Battle.net, переустановите и восстановите резервные копии. Это удаляет накопленные устаревшие файлы и устаревшие данные за годы патчей.",
        "opt_sug_reinstall_tooltip": "Причина: Годы обновлений оставляют устаревшие файлы, устаревшие ресурсы и фрагментированные данные, которые замедляют загрузку и тратят место.\n\nУровень риска: Низкий - Ваши настройки/аддоны сохраняются в папках WTF/AddOns.\n\nОжидаемые преимущества: Более быстрая загрузка, меньше используемого дискового пространства (5-15 ГБ сэкономлено), улучшенная стабильность.\n\nКак сделать: 1) Резервное копирование Interface\\AddOns и WTF\n2) Удалить через Battle.net\n3) Переустановить WoW\n4) Скопировать резервные папки",
        
        # Help/About tab - content
        "help_version_label": "Утилита Очистки WoW {}",
        "help_about_description": "Комплексный набор инструментов для обслуживания и оптимизации World of Warcraft.\nОчищайте ненужные файлы, управляйте аддонами, оптимизируйте производительность игры и многое другое.\n\nВсегда закрывайте World of Warcraft перед запуском этой утилиты.",
        "help_copyright": "Авторские права © 2025 Paul Vandersypen. Выпущено на условиях GNU General Public License v3.0 (GPL-3.0-or-later). Полные условия см. в прилагаемом файле LICENSE.",
        "support_patreon": "Поддержать на Patreon",
        "donate_paypal": "Пожертвовать через PayPal",
        "github_repository": "Репозиторий GitHub",
        "github_issues": "Сообщить о проблеме",

        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ Процессор: {} | ОЗУ: {} | Видеокарта: {}",
        "gpu_switch_notification": "⚠ Переключение видеокарты: Настроено использование '{}' вместо '{}'. Это изменение оптимизирует производительность, используя вашу дискретную видеокарту для лучшего игрового опыта. Это безопасно и рекомендуется.",
        "scan_tooltip_refresh": "Не нужно сканировать снова, если вы не меняли процессор, видеокарту или ОЗУ.\nНажмите, чтобы обновить кэшированную информацию об оборудовании.",
        "scanning_ram_detected": "Сканирование ОЗУ... (обнаружен процессор: {} ядер/{} потоков)",
        "scanning_gpu_detected": "Сканирование видеокарты... (обнаружено ОЗУ: {} ГБ)",
        "apply_preset_label": "Применить пресет:",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "WoW запущен",
        "wow_running_message": "World of Warcraft в настоящее время запущен. Изменения вступят в силу после перезапуска игры.\n\nПродолжить?",
        "permission_error_title": "Ошибка прав доступа",
        "permission_error_message": "Config.wtf доступен только для чтения. Удалите атрибут только для чтения и повторите попытку.",
        "config_readonly_status": "✗ Config.wtf доступен только для чтения.",
        "confirm_apply_title": "Подтвердить применение",
        "confirm_apply_message": "Применить пресет {} к {}?\n\nЭто изменит {} графических настроек в Config.wtf.\nРезервная копия будет создана автоматически.\n\nОсновные изменения:\n• Пресет: Настройки качества {}\n• Производительность: {} оптимизаций",
        "cancelled_by_user": "Отменено пользователем.",
        "settings_applied_status": "✓ Применено {} настроек.",
        "preset_applied_status": "✓ Пресет {} применён.",
        "apply_error_status": "✗ Ошибка: {}",
        
        # Preset tooltips
        "preset_tooltip_template": "Пресет {}\n\nОжидаемая производительность:\n{}\n\nНажмите 'Применить' ниже, чтобы использовать этот пресет.",
        "perf_depends_hardware": "Влияние на производительность зависит от вашего оборудования.",
        "perf_will_vary": "Производительность будет варьироваться",
        
        # Low preset performance estimates
        "low_perf_high": "Отличная производительность (100+ FPS в большинстве сценариев)",
        "low_perf_mid": "Очень хорошая производительность (80-120 FPS)",
        "low_perf_low": "Хорошая производительность (60-80 FPS)",
        
        # Medium preset performance estimates
        "medium_perf_high": "Отличная производительность (90-120 FPS)",
        "medium_perf_mid": "Хорошая производительность (60-90 FPS)",
        "medium_perf_low": "Умеренная производительность (45-60 FPS)",
        
        # High preset performance estimates
        "high_perf_high": "Очень хорошая производительность (70-100 FPS)",
        "high_perf_mid": "Хорошая производительность (50-70 FPS)",
        "high_perf_low": "Могут быть трудности в рейдах (30-50 FPS)",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "Хорошая производительность (60-80 FPS)",
        "ultra_perf_mid": "Умеренная производительность (40-60 FPS)",
        "ultra_perf_low": "Низкая производительность (20-40 FPS)",
        
        # WoW version names
        "version_retail": "Retail",
        "version_classic": "Classic",
        "version_classic_era": "Classic Era",
        "version_ptr": "PTR",
        "version_beta": "Beta",
        
        # Game Optimizer - additional strings
        "not_detected": "Не обнаружено",
        "unknown_cpu": "Неизвестный процессор",
        "unknown_gpu": "Неизвестная",
        "not_set": "Не установлено",
        "hover_for_details": "Наведите для подробностей",
        
        # Orphan Cleaner - log messages
        "orphan_found_in": "[Очистка Сирот] Найден сирота в {0}: {1}",
        "orphan_total_found": "[Очистка Сирот] Всего осиротевших SavedVariables: {0}",
        "orphan_moved_trash": "[Очистка Сирот] Перемещено в корзину: {0}",
        "orphan_deleted": "[Очистка Сирот] Удалено: {0}",
        "orphan_error_deleting": "[Очистка Сирот] Ошибка удаления {0}: {1}",
        "orphan_rebuilt_addons": "[Очистка Сирот] Перестроено: {0}",
        "orphan_error_writing_addons": "[Очистка Сирот] Ошибка записи AddOns.txt {0}: {1}",
        "orphan_error_rebuild": "[Очистка Сирот] Ошибка при перестроении AddOns.txt: {0}",
        "new_setting_prefix": "[Новое] ",
        "details_colon": "Подробности:",
        "updated_settings": "• Обновлено {} существующих настроек",
        "added_settings": "• Добавлено {} новых настроек",
        
        # Path Manager
        "select_wow_folder_title": "Выбор папки WoW",
        "unrecognized_installation": "Нераспознанная установка",
        "folder_not_valid_continue": "Выбранная папка не является действительной.\n\nВсё равно продолжить?",
        "wow_folder_set": "Папка WoW установлена: {}",
        
        # Performance
        "performance_execution_time": "[Производительность] {} заняло {:.3f} секунд",
        "perf_moved_trash": "[{}] Перемещено в корзину: {}",
        "perf_deleted": "[{}] Удалено: {}",
        "perf_error_deleting": "[{}] Ошибка удаления {}: {}",
        
        "select_valid_wow_optimizer": "Выберите действительную папку WoW в Параметрах, чтобы включить просмотр по версиям.",
        "select_valid_wow_folder_cleaner": "Выберите действительную папку WoW в Параметрах, чтобы включить Очистку Папок.",
        
        # Main UI - Buttons and Messages
        "apply": "Применить",
        "cancel": "Отмена",
        "export_log": "Экспортировать журнал",
        "clear_log": "Очистить журнал",
        
        # Common Messages
        "no_files_selected": "Файлы не выбраны",
        "no_folders_selected": "Папки не выбраны",
        "no_orphans_selected": "Осиротевшие файлы не выбраны",

        # Common Messages
        "apply_font_question": "Применить шрифт '{}' к приложению?",
        "select_valid_wow_first": "Пожалуйста, сначала выберите действительную папку WoW.",
        "restored": "Восстановлено",

        # File Cleaner
        "found_files_count": "Найдено {} файл(ов) во всех версиях.",
        "confirm_action_files": "Вы уверены, что хотите {} {} файл(ов)?",
        "processed_files_count": "Обработано {} файл(ов).",

        # Folder Cleaner
        "confirm_action_folders": "Вы уверены, что хотите {} {} папок?",
        "processed_folders_count": "Обработано {} папок.",

        # Orphan Cleaner
        "found_orphans_count": "Найдено {} сирот SavedVariable.",
        "confirm_action_orphans": "Вы уверены, что хотите {} {} сирот SavedVariables?",
        "processed_orphans_count": "Обработано {} сирот.",

        # Actions
        "move_to_trash": "переместить в корзину",
        "delete_permanently_action": "удалить навсегда",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "Записи AddOns.txt восстановлены.\nВсего записано: {}\nВсего удалено: {}",

        # Log Export
        "log_empty_nothing_export": "Журнал пуст. Нечего экспортировать.",

        # Settings Restore
        "settings_restored_restart": "Настройки восстановлены по умолчанию. Приложение будет перезапущено.",
        "settings_restored_manual": "Настройки восстановлены по умолчанию. Пожалуйста, перезапустите приложение вручную.",
        "failed_restore_defaults": "Не удалось восстановить значения по умолчанию: {}",
        
        # File Cleaner
        
        # Folder Cleaner
        
        # Orphan Cleaner
        
        # Actions
        
        # AddOns.txt Rebuild
        
        # Log Export
        
        # Settings Restore
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "Поиск SavedVariables аддонов (.lua / .lua.bak) без соответствующего установленного аддона (Interface/AddOns) во всех обнаруженных версиях WoW. Сканирует папки SavedVariables учётных записей, серверов и персонажей. Обработка также перестраивает AddOns.txt в соответствии с установленными аддонами (по возможности сохраняя состояние включено/отключено).",
        "orphan_description_part2": "Примечание: Файлы Blizzard_*.lua являются основными данными игры и автоматически игнорируются для безопасности (но их резервные копии .lua.bak могут быть удалены).",
        "wtf_not_found": "Каталог WTF не найден. Сначала запустите игру.",
        "unknown_preset": "Неизвестный пресет: {}",
        "backup_failed": "Не удалось создать резервную копию: {}",
        "config_write_failed": "Не удалось записать конфигурацию: {}",
        "config_updated": "Применено {} настроек к Config.wtf.",
        "settings_updated_added": "Обновлено {} настроек, добавлено {} новых настроек.",
        "backup_saved": " Резервная копия сохранена.",
        "version_path": "Версия: {}\nПуть: {}",
        "optimizer_launch_required": "Оптимизатор требует, чтобы {} был запущен хотя бы один раз. Запустите WoW и дойдите до экрана выбора персонажа, затем выйдите из игры. После этого вы сможете использовать оптимизатор для применения графических пресетов.",
        "system_matches": "Ваша система соответствует: {}",
        "optimizer_title": "Оптимизатор — {}",
        "recommendations_applied": "✓ Рекомендуемые настройки применены.",
        "applied_preset_log": "Пресет {} применён для {}",
        "apply_preset_failed_log": "Не удалось применить пресет {}: {}",
        "hardware_scan_complete": "Сканирование оборудования завершено: сохранено в глобальных настройках.",
        "hardware_scan_failed": "Не удалось выполнить сканирование оборудования: {}",
        "scan_error": "✗ Ошибка: {}",
        
        # Game Validation
        "invalid_game_installation": "Недействительная установка игры",
        "game_installation_incomplete": "Установка World of Warcraft кажется неполной.\n\nЗапустите игру хотя бы один раз, чтобы инициализировать папки Interface и WTF.\n\nПосле запуска игры вы сможете использовать эту утилиту для очистки установки.",
        
        # Startup Warning
        "user_disabled_warning": "Пользователь отключил предупреждение при запуске.",
        
        # Update Checker
        "no_updates_available": "Обновления недоступны",
        "no_releases_published": "Вы используете {}.\n\nНикаких релизов ещё не опубликовано.",
        "update_check_failed": "Не удалось проверить обновления",
        "update_check_http_error": "Не удалось проверить обновления:\n\nHTTP {}: {}",
        "update_check_network_error": "Не удалось проверить обновления:\n\n{}",
        "update_check_error": "Ошибка проверки обновлений",
        "update_check_exception": "Ошибка при проверке обновлений:\n\n{}",
        "update_available": "Доступно обновление",
        "update_message": "Доступна новая версия!\n\nТекущая версия: {}\nПоследняя версия: {}\n\nХотите загрузить ее сейчас?",
        "up_to_date": "Актуальная версия",
        "up_to_date_message": "Вы используете последнюю версию ({}).",
        "browser_open_error": "Не удалось открыть браузер:\n\n{}",
        "download_update": "Загрузить обновление",
        "view_release": "Посмотреть релиз",
        "later": "Позже",
        "downloading_update": "Загрузка обновления",
        "downloading_update_file": "Загрузка файла обновления...",
        "download_failed": "Ошибка загрузки",
        "download_failed_message": "Не удалось загрузить обновление:\n\n{}",
        "update_ready": "Обновление готово",
        "update_downloaded_message": "Обновление успешно загружено!\n\nФайл: {}\n\nХотите установить его сейчас?",
        "install_now": "Установить сейчас",
        "install_later": "Установить позже",
        "update_location": "Загружено в: {}",
        "failed_to_fetch_release": "Не удалось получить информацию о релизе из GitHub.",
        "no_download_available": "Файлы для загрузки не найдены для этого релиза.",
        "install_update": "Установить обновление",
        "please_run_installer": "Папка загрузки открыта.\n\nЗапустите установщик для обновления приложения.",
        "update_saved_message": "Обновление сохранено в:\n\n{}\n\nВы можете установить его позже.",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[Очистка Файлов] Найден файл: {}",
        "file_cleaner_found": "[Очистка Файлов] Найдено: {}",
        "file_cleaner_total_found": "[Очистка Файлов] Всего найдено файлов .bak/.old: {}",
        "file_cleaner_moved_trash": "[Очистка Файлов] Перемещено в корзину: {}",
        "file_cleaner_deleted": "[Очистка Файлов] Удалено: {}",
        "file_cleaner_error_deleting": "[Очистка Файлов] Ошибка удаления {}: {}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[Очистка Папок] Найдено: {}",
        "folder_cleaner_total": "[Очистка Папок] Всего папок, доступных для очистки: {}",
    },
    
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
        "processed": "{}개의 {}을(를) 처리했습니다.",        "restore_defaults_confirm": "모든 설정을 기본값으로 복원하시겠습니까?",
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
        "orphan_processed": "고아 파일 정리: {}개 고아 파일 처리됨.",        "addons_txt_log": "[AddOns.txt] {}: {}개 항목 작성, {}개 제거",
        "preset_applied_log": "{} 사전 설정이 {}에 적용됨",
        "preset_failed_log": "{} 사전 설정 적용 실패: {}",
        "change_language": "언어 변경",
        "change_language_question": "언어를 {}에서 {}(으)로 변경하시겠습니까?\n\n새 언어를 적용하기 위해 애플리케이션이 다시 시작됩니다.",
        "language_changed": "언어 변경됨",
        "language_changed_restart": "언어가 {}(으)로 변경되었습니다.\n애플리케이션이 지금 다시 시작됩니다.",
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
        "process_selected_screenshots": "선택한 스크린샷 처리",
        "no_screenshots_selected": "선택한 스크린샷이 없습니다.",
        "confirm_action_screenshots": "{} {} 스크린샷 파일?",
        "processed_screenshots_count": "{} 스크린샷 처리됨.",
        "screenshots_per_file": "스크린샷 (파일당 작업)",
        "folder_screenshots": "스크린샷",
        "folder_logs": "로그",
        "folder_errors": "오류",
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
        "preview_hint": "(이미지를 클릭하여 확대 • 다시 클릭하거나 Esc를 눌러 닫기)",
        "screenshots_not_found": "이 버전의 스크린샷 폴더를 찾을 수 없습니다.",
        
        # Main UI - Buttons and Messages
        "apply": "적용",
        "cancel": "취소",
        "export_log": "로그 내보내기",
        "clear_log": "로그 지우기",
        
        # Common Messages
        "no_files_selected": "선택된 파일 없음",
        "no_folders_selected": "선택된 폴더 없음",
        "no_orphans_selected": "선택된 고아 파일 없음",

        # Common Messages
        "apply_font_question": "애플리케이션에 '{}' 글꼴을 적용하시겠습니까?",
        "select_valid_wow_first": "먼저 유효한 WoW 폴더를 선택하세요.",
        "restored": "복원됨",

        # File Cleaner
        "found_files_count": "모든 버전에서 {}개 파일을 찾았습니다.",
        "confirm_action_files": "{}개 파일을 {}하시겠습니까?",
        "processed_files_count": "{}개 파일을 처리했습니다.",

        # Folder Cleaner
        "confirm_action_folders": "{}개 폴더를 {}하시겠습니까?",
        "processed_folders_count": "{}개 폴더를 처리했습니다.",

        # Orphan Cleaner
        "found_orphans_count": "{}개 고아 SavedVariable을 찾았습니다.",
        "confirm_action_orphans": "{}개 고아 SavedVariables를 {}하시겠습니까?",
        "processed_orphans_count": "{}개 고아를 처리했습니다.",

        # Actions
        "move_to_trash": "휴지통으로 이동",
        "delete_permanently_action": "영구 삭제",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "AddOns.txt 항목이 재구성되었습니다.\n총 작성: {}\n총 제거: {}",

        # Log Export
        "log_empty_nothing_export": "로그가 비어 있습니다. 내보낼 것이 없습니다.",

        # Settings Restore
        "settings_restored_restart": "설정이 기본값으로 복원되었습니다. 애플리케이션이 이제 다시 시작됩니다.",
        "settings_restored_manual": "설정이 기본값으로 복원되었습니다. 애플리케이션을 수동으로 다시 시작하세요.",
        "failed_restore_defaults": "기본값 복원 실패: {}",
        
        # File Cleaner
        
        # Folder Cleaner
        
        # Orphan Cleaner
        
        # Actions
        
        # AddOns.txt Rebuild
        
        # Log Export
        
        # Settings Restore
        
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
        "opt_sug_reinstall_title": "WoW 재설치 (클린 설치)",
        "opt_sug_reinstall_text": "AddOns 및 WTF 폴더를 백업하고, Battle.net을 통해 모든 WoW 버전을 제거한 후 재설치하고 백업을 복원하세요. 이렇게 하면 수년간의 패치로 누적된 레거시 파일과 오래된 데이터가 제거됩니다.",
        "opt_sug_reinstall_tooltip": "이유: 수년간의 업데이트로 오래된 파일, 사용 중단된 애셋, 조각난 데이터가 남아 로딩 속도를 늦추고 공간을 낭비합니다.\n\n위험 수준: 낮음 - 설정/애드온은 WTF/AddOns 폴더에 보존됩니다.\n\n예상 이점: 더 빠른 로딩 시간, 디스크 사용량 감소(5-15 GB 절약), 향상된 안정성.\n\n방법: 1) Interface\\AddOns 및 WTF 백업\n2) Battle.net을 통해 제거\n3) WoW 재설치\n4) 백업한 폴더 복사",
        
        # Help/About tab - content
        "help_version_label": "WoW 정리 도구 {}",
        "help_about_description": "World of Warcraft를 위한 포괄적인 유지 관리 및 최적화 도구 모음입니다.\n불필요한 파일을 정리하고, 애드온을 관리하고, 게임 성능을 최적화하는 등의 작업을 수행합니다.\n\n이 도구를 사용하기 전에 항상 World of Warcraft를 종료하세요.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. GNU General Public License v3.0(GPL-3.0-or-later)에 따라 출시되었습니다. 전체 약관은 포함된 LICENSE 파일을 참조하세요.",
        "support_patreon": "Patreon에서 후원하기",
        "donate_paypal": "PayPal로 기부하기",
        "github_repository": "GitHub 저장소",
        "github_issues": "문제 보고",

        
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
        "update_message": "새 버전을 사용할 수 있습니다!\n\n현재: {}\n최신: {}\n\n지금 다운로드하시겠습니까?",
        "up_to_date": "최신 버전",
        "up_to_date_message": "최신 버전({})을 사용 중입니다.",
        "browser_open_error": "브라우저를 열 수 없습니다:\n\n{}",
        "download_update": "업데이트 다운로드",
        "view_release": "릴리스 보기",
        "later": "나중에",
        "downloading_update": "업데이트 다운로드 중",
        "downloading_update_file": "업데이트 파일을 다운로드하는 중...",
        "download_failed": "다운로드 실패",
        "download_failed_message": "업데이트 다운로드에 실패했습니다:\n\n{}",
        "update_ready": "업데이트 준비 완료",
        "update_downloaded_message": "업데이트를 성공적으로 다운로드했습니다!\n\n파일: {}\n\n지금 설치하시겠습니까?",
        "install_now": "지금 설치",
        "install_later": "나중에 설치",
        "update_location": "다운로드 위치: {}",
        "failed_to_fetch_release": "GitHub에서 릴리스 정보를 가져오지 못했습니다.",
        "no_download_available": "이 릴리스에서 다운로드할 수 있는 파일을 찾을 수 없습니다.",
        "install_update": "업데이트 설치",
        "please_run_installer": "다운로드 위치가 열렸습니다.\n\n설치 프로그램을 실행하여 애플리케이션을 업데이트하십시오.",
        "update_saved_message": "업데이트가 다음 위치에 저장되었습니다:\n\n{}\n\n나중에 설치할 수 있습니다.",
        
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
    
    "zhCN": {
        # Window title
        "window_title": "魔兽世界清理工具",
        
        # Menu/Tab names
        "file_cleaner": "文件清理",
        "folder_cleaner": "文件夹清理",
        "orphan_cleaner": "孤立文件清理",
        "game_optimizer": "游戏优化",
        "optimization_suggestions": "优化建议",
        "log": "日志",
        "help_about": "帮助/关于",
        
        # Options section
        "options": "选项",
        "wow_folder": "魔兽世界文件夹：",
        "browse": "浏览...",
        "browse_tooltip": "浏览您的魔兽世界文件夹。",
        "font_size": "字体大小：",
        "font": "字体：",
        "theme": "主题：",
        "language": "语言：",
        "file_action": "文件操作：",
        "delete_permanently": "永久删除",
        "move_to_recycle": "移至回收站",
        "enable_verbose": "启用详细日志",
        "verbose_tooltip": "启用后，日志将记录每个处理的文件/文件夹/AddOns.txt行。",
        "external_log": "外部日志：",
        "fresh": "新建",
        "fresh_tooltip": "每次导出时创建新的日志文件（覆盖现有文件）。",
        "append": "追加",
        "append_tooltip": "将每次导出追加到现有日志文件（根据详细程度保留10-20个会话）。",
        "check_updates": "检查更新",
        "check_updates_tooltip": "启用后，将在启动时检查GitHub上的新版本。",
        "restore_defaults": "恢复默认设置",
        "light": "浅色",
        "dark": "深色",
        
        # File Cleaner
        "scan": "扫描",
        "select_all": "全选",
        "expand_all": "全部展开",
        "collapse_all": "全部折叠",
        "process_selected": "处理选中项",
        "scanning": "扫描中…",
        "no_bak_old_found": "未找到.bak或.old文件。",
        "files_found": "找到{}个文件。",
        
        # Folder Cleaner
        "version": "版本：",
        "path": "路径：",
        "preview": "预览",
        "toggle_all": "全部切换",
        "process_folders": "处理选中的文件夹",
        
        # Orphan Cleaner
        "rebuild_addons": "重建AddOns.txt",
        "no_orphans_found": "未找到孤立的SavedVariables。",
        "orphans_found": "找到{}个孤立的SavedVariable。",
        
        # Game Optimizer
        "scan_hardware": "扫描硬件",
        "system_matches": "您的系统匹配：",
        "optimization_applied": "✓ 已应用优化",
        "optimization_not_applied": "⚠ 尚未应用优化",
        "graphics_presets": "图形预设（{}）：",
        "graphics_presets_classic": "图形预设（{}）：",
        "apply_preset": "应用预设：",
        "apply": "应用",
        "preset_applied": "✓ 已应用{}预设。",
        "error": "✗ 错误：{}",
        "low": "低",
        "medium": "中",
        "high": "高",
        "ultra": "极致",
        
        # Optimization Suggestions
        "manual_suggestions": "手动优化建议",
        "manual_disclaimer": "注意：此应用程序不会自动执行这些优化。这些是您需要手动实施的建议。",
        "clean_data_folder": "清理游戏数据文件夹",
        "clean_data_text": "如果安装魔兽世界后已经过了几年或多个资料片，请考虑删除魔兽世界主目录中的Data文件夹。这*可能*会减小游戏大小并提高加载屏幕性能。Battle.net启动器会在需要时自动重建此文件夹。",
        "enable_hdr": "启用HDR（高动态范围）",
        "enable_hdr_text": "检查操作系统的显示设置以查看HDR是否可用。如果您的显示器支持，启用HDR可以显著提高游戏内的视觉清晰度和色彩深度。",
        "verify_refresh": "验证显示器刷新率",
        "verify_refresh_text": "确保在操作系统的显示设置中将显示器的刷新率设置为支持的最大值。更高的刷新率可提供更流畅的游戏体验和更好的响应性。",
        "enable_sam": "启用智能访问内存/可调整大小的BAR",
        "enable_sam_text": "检查主板BIOS设置中的智能访问内存（AMD）或可调整大小的BAR（Intel/NVIDIA）。启用此功能可让CPU访问完整的GPU内存，可能会提高性能。",
        "enable_xmp": "启用XMP内存配置文件",
        "enable_xmp_text": "访问主板BIOS并启用XMP（极限内存配置文件）或DOCP/EOCP设置。这可确保您的内存以其额定速度而非默认的保守速度运行，从而提高整体系统性能。",
        
        # Log tab
        "export_log": "导出日志",
        "clear_log": "清除日志",
        
        # Help/About
        "about_text": "魔兽世界的综合维护和优化套件。\n清理不必要的文件，管理插件，优化游戏性能等。\n\n运行此工具前请务必关闭魔兽世界。",
        "copyright": "版权所有 © 2025 Paul Vandersypen。根据GNU通用公共许可证v3.0（GPL-3.0-or-later）发布。有关完整条款，请参阅随附的LICENSE文件。",
        
        # Dialogs
        "invalid_folder": "无效的文件夹",
        "select_valid_wow": "请先选择有效的魔兽世界文件夹。",
        "no_selection": "未选择",
        "no_files_selected": "未选择要处理的文件。",
        "no_folders_selected": "未选择要清理的文件夹。",
        "no_orphans_selected": "未选择孤立文件。",
        "confirm": "确认",
        "confirm_action": "确定要{}{}{}吗？",
        "file_s": "个文件",
        "folder_s": "个文件夹",
        "orphaned_savedvars": "个孤立的SavedVariables",
        "completed": "已完成",
        "processed": "已处理{}{}。",        "restore_defaults_confirm": "将所有设置恢复为默认值？",
        "restart_required": "设置已恢复。应用程序现在将重新启动。",
        "error_title": "错误",
        "restore_error": "恢复默认设置失败：{}",
        "confirm_font": "确认字体",
        "apply_font_confirm": "将字体'{}'应用到应用程序？",
        "select_font": "选择字体",
        "export_log_title": "导出日志",
        "log_empty": "日志为空。没有可导出的内容。",
        "log_exported": "日志已成功导出到：\n{}",
        "export_error": "导出错误",
        "export_failed": "导出日志失败：\n{}",
        "addons_rebuilt": "已重建AddOns.txt条目。\n总共写入：{}\n总共删除：{}",
        
        # Log messages
        "session_started": "会话已开始 — {}",
        "file_scan": "文件清理扫描：{}个匹配项。",
        "orphan_scan": "孤立文件清理扫描：{}个孤立文件。",
        "file_processed": "文件清理：已处理{}个文件。",
        "folder_processed": "文件夹清理：已处理{}个文件夹。",
        "orphan_processed": "孤立文件清理：已处理{}个孤立文件。",        "addons_txt_log": "[AddOns.txt] {}：写入{}个条目，删除{}个",
        "preset_applied_log": "已为{}应用{}预设",
        "preset_failed_log": "应用{}预设失败：{}",
        "change_language": "更改语言",
        "change_language_question": "将语言从 {} 更改为 {}？\n\n应用程序将重新启动以应用新语言。",
        "language_changed": "语言已更改",
        "language_changed_restart": "语言已更改为 {}。\n应用程序现在将重新启动。",
        "apply": "应用",
        "cancel": "取消",
        "scan_bak_old": "扫描.bak / .old文件",
        "expand_all": "全部展开",
        "collapse_all": "全部折叠",
        "select_deselect_all": "全选/取消全选",
        "process_selected_files": "处理选中的文件",
        "scan_orphaned": "扫描孤立的SavedVariables",
        "process_selected_folders": "处理选中的文件夹",
        "select_deselect_all_folders": "全选/取消全选所有文件夹",
        "select_deselect_all_screenshots": "全选/取消全选所有截图文件",
        "process_selected_screenshots": "处理选定的截图",
        "no_screenshots_selected": "未选择截图。",
        "confirm_action_screenshots": "{}{}个截图文件？",
        "processed_screenshots_count": "已处理{}个截图。",
        "screenshots_per_file": "截图（按文件操作）",
        "folder_screenshots": "截图",
        "folder_logs": "日志",
        "folder_errors": "错误",
        "check_for_updates": "检查更新",
        
        # Game Optimizer
        "game_optimizer_title": "游戏优化器",
        "game_optimizer_desc": "根据您的硬件配置优化魔兽世界的性能。",
        "scan_hardware": "扫描硬件",
        "click_scan_hardware": "点击'扫描硬件'以检测您系统的功能。",
        "select_valid_wow_folder": "在选项中选择有效的魔兽世界文件夹以启用按版本视图。",
        "recommended_settings": "推荐设置：",
        "apply_preset_label": "应用预设：",
        "apply_recommended_settings": "应用推荐设置",
        "scanning_cpu": "正在扫描CPU...",
        "scanning_ram": "正在扫描内存...（已检测到CPU：{}核/{}线程）",
        "scanning_gpu": "正在扫描GPU...（已检测到内存：{} GB）",
        
        # Startup warning
        "important_notice": "重要提示",
        "startup_warning_text": "⚠️ 在使用此工具之前，请确保魔兽世界已完全关闭。\n\n在魔兽世界打开时运行该工具可能会干扰游戏文件。",
        "do_not_show_again": "不再显示此警告",
        "ok": "确定",
        
        # Folder cleaner
        "select_valid_wow_folder_cleaner": "在选项中选择有效的魔兽世界文件夹以启用文件夹清理器。",
        "preview_label": "预览",
        "preview_hint": "(点击图片放大 • 再次点击或按 Esc 关闭)",
        "screenshots_not_found": "未找到此版本的截图文件夹。",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "手动优化建议",
        "opt_sug_disclaimer": "注意：此应用程序不会自动执行这些优化。这些是您需要手动实施的建议。",
        "opt_sug_clean_data_title": "清理游戏数据文件夹",
        "opt_sug_clean_data_text": "如果安装魔兽世界后已经过了几年或多个资料片，请考虑删除魔兽世界主目录中的Data文件夹。这*可能*会减小游戏大小并提高加载屏幕性能。Battle.net启动器会在需要时自动重建此文件夹。",
        "opt_sug_clean_data_tooltip": "原因：Data文件夹会随着时间的推移累积临时和缓存的游戏资源。删除它会强制重新下载优化的文件。\n\n风险级别：安全 - Battle.net将自动重新下载所需文件。\n\n预期收益：更快的加载屏幕，减少磁盘使用量（可能节省10-20 GB）。",
        "opt_sug_hdr_title": "启用HDR（高动态范围）",
        "opt_sug_hdr_text": "检查操作系统的显示设置以查看HDR是否可用。如果您的显示器支持，启用HDR可以显著提高游戏内的视觉清晰度和色彩深度。",
        "opt_sug_hdr_tooltip": "原因：HDR提供更广的色域和更好的对比度，使视觉效果更加生动和逼真。\n\n风险级别：安全 - 可在操作系统设置中轻松开关。\n\n预期收益：如果显示器支持HDR10或更高版本，视觉质量会显著提升。\n\n要求：支持HDR的显示器和Windows 10/11或macOS Catalina+。",
        "opt_sug_refresh_title": "验证显示器刷新率",
        "opt_sug_refresh_text": "确保在操作系统的显示设置中将显示器的刷新率设置为支持的最大值。更高的刷新率可提供更流畅的游戏体验和更好的响应性。",
        "opt_sug_refresh_tooltip": "原因：即使显示器支持120Hz/144Hz/165Hz，许多系统默认为60Hz。这会不必要地限制帧率。\n\n风险级别：安全 - 无硬件风险，易于恢复。\n\n预期收益：更流畅的游戏体验，减少输入延迟，更好的反应时间。\n\n如何检查：Windows：设置 > 显示 > 高级 > 刷新率\nmacOS：系统偏好设置 > 显示器",
        "opt_sug_sam_title": "启用智能访问内存/可调整大小的BAR",
        "opt_sug_sam_text": "检查主板BIOS设置中的智能访问内存（AMD）或可调整大小的BAR（Intel/NVIDIA）。启用此功能可让CPU访问完整的GPU内存，可能会提高性能。",
        "opt_sug_sam_tooltip": "原因：允许CPU一次访问整个GPU内存，而不是小的256MB块，减少瓶颈。\n\n风险级别：中等 - 需要更改BIOS。首先记录当前设置。\n\n预期收益：在GPU密集型场景中提升5-15%的FPS。\n\n要求：\n• AMD：Ryzen 5000+ CPU + RX 6000+ GPU\n• Intel：第10代+ CPU + RTX 3000+ GPU\n• 可能需要BIOS更新",
        "opt_sug_xmp_title": "启用XMP内存配置文件",
        "opt_sug_xmp_text": "访问主板BIOS并启用XMP（极限内存配置文件）或DOCP/EOCP设置。这可确保您的内存以其额定速度而非默认的保守速度运行,从而提高整体系统性能。",
        "opt_sug_xmp_tooltip": "原因：内存通常默认以2133MHz运行，即使额定为3200MHz+。XMP启用广告速度。\n\n风险级别：中等 - BIOS更改。如果内存不稳定，系统可能无法启动（易于重置）。\n\n预期收益：CPU性能提升10-20%，加载时间更快，更好的1%低点。\n\n如何启用：进入BIOS（启动时通常按Del/F2） > 找到XMP/DOCP设置 > 启用 > 保存并退出",
        "opt_sug_reinstall_title": "重新安装WoW（干净安装）",
        "opt_sug_reinstall_text": "备份您的AddOns和WTF文件夹，通过Battle.net卸载所有WoW版本，重新安装，然后恢复您的备份。这将删除多年补丁累积的旧文件和过时数据。",
        "opt_sug_reinstall_tooltip": "原因：多年的更新会留下过时的文件、弃用的资源和碎片化数据，导致加载速度变慢并浪费空间。\n\n风险级别：低 - 您的设置/插件保存在WTF/AddOns文件夹中。\n\n预期收益：更快的加载时间，减少磁盘使用量（节省5-15 GB），提高稳定性。\n\n操作方法：1) 备份Interface\\AddOns和WTF\n2) 通过Battle.net卸载\n3) 重新安装WoW\n4) 复制备份的文件夹",
        
        # Help/About tab - content
        "help_version_label": "魔兽世界清理工具 {}",
        "help_about_description": "魔兽世界的综合维护和优化套件。\n清理不必要的文件，管理插件，优化游戏性能等。\n\n运行此工具前请务必关闭魔兽世界。",
        "help_copyright": "版权所有 © 2025 Paul Vandersypen。根据GNU通用公共许可证v3.0（GPL-3.0-or-later）发布。有关完整条款，请参阅随附的LICENSE文件。",
        "support_patreon": "在 Patreon 上支持",
        "donate_paypal": "通过 PayPal 捐赠",
        "github_repository": "GitHub仓库",
        "github_issues": "报告问题",

        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU：{} | 内存：{} | GPU：{}",
        "gpu_switch_notification": "⚠ GPU切换：配置为使用'{}'而不是'{}'。此更改通过使用您的独立GPU来优化性能，以获得更好的游戏体验。这是安全且推荐的。",
        "scan_tooltip_refresh": "除非您更改了CPU、GPU或内存，否则无需再次扫描。\n点击刷新缓存的硬件信息。",
        "scanning_ram_detected": "正在扫描内存...（已检测到CPU：{}核/{}线程）",
        "scanning_gpu_detected": "正在扫描GPU...（已检测到内存：{} GB）",
        "apply_preset_label": "应用预设：",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "魔兽世界正在运行",
        "wow_running_message": "魔兽世界当前正在运行。更改将在重新启动游戏后生效。\n\n是否要继续？",
        "permission_error_title": "权限错误",
        "permission_error_message": "Config.wtf是只读的。请删除只读属性，然后重试。",
        "config_readonly_status": "✗ Config.wtf是只读的。",
        "confirm_apply_title": "确认应用",
        "confirm_apply_message": "将{}预设应用到{}？\n\n这将修改Config.wtf中的{}个图形设置。\n将自动创建备份。\n\n主要更改：\n• 预设：{}质量设置\n• 性能：{}个优化",
        "cancelled_by_user": "用户取消。",
        "settings_applied_status": "✓ 已应用{}设置。",
        "preset_applied_status": "✓ 已应用{}预设。",
        "apply_error_status": "✗ 错误：{}",
        
        # Preset tooltips
        "preset_tooltip_template": "{}预设\n\n预期性能：\n{}\n\n点击下方的'应用'以使用此预设。",
        "perf_depends_hardware": "性能影响取决于您的硬件。",
        "perf_will_vary": "性能会有所不同",
        
        # Low preset performance estimates
        "low_perf_high": "出色的性能（大多数场景100+ FPS）",
        "low_perf_mid": "非常好的性能（80-120 FPS）",
        "low_perf_low": "良好的性能（60-80 FPS）",
        
        # Medium preset performance estimates
        "medium_perf_high": "出色的性能（90-120 FPS）",
        "medium_perf_mid": "良好的性能（60-90 FPS）",
        "medium_perf_low": "中等性能（45-60 FPS）",
        
        # High preset performance estimates
        "high_perf_high": "非常好的性能（70-100 FPS）",
        "high_perf_mid": "良好的性能（50-70 FPS）",
        "high_perf_low": "在团队副本中可能吃力（30-50 FPS）",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "良好的性能（60-80 FPS）",
        "ultra_perf_mid": "中等性能（40-60 FPS）",
        "ultra_perf_low": "较低性能（20-40 FPS）",
        
        # WoW version names
        "version_retail": "正式服",
        "version_classic": "怀旧服",
        "version_classic_era": "经典旧世",
        "version_ptr": "测试服",
        "version_beta": "测试服",
        
        # Game Optimizer - additional strings
        "not_detected": "未检测到",
        "unknown_cpu": "未知CPU",
        "unknown_gpu": "未知",
        "not_set": "未设置",
        "hover_for_details": "悬停查看详情",
        
        # Orphan Cleaner - log messages
        "orphan_found_in": "[孤立文件清理] 在{0}中发现孤立文件：{1}",
        "orphan_total_found": "[孤立文件清理] 孤立的SavedVariables总数：{0}",
        "orphan_moved_trash": "[孤立文件清理] 已移至回收站：{0}",
        "orphan_deleted": "[孤立文件清理] 已删除：{0}",
        "orphan_error_deleting": "[孤立文件清理] 删除{0}时出错：{1}",
        "orphan_rebuilt_addons": "[孤立文件清理] 已重建：{0}",
        "orphan_error_writing_addons": "[孤立文件清理] 写入AddOns.txt {0}时出错：{1}",
        "orphan_error_rebuild": "[孤立文件清理] AddOns.txt重建期间出错：{0}",
        "new_setting_prefix": "[新] ",
        "details_colon": "详情：",
        "updated_settings": "• 更新了{0}个现有设置",
        "added_settings": "• 添加了{0}个新设置",
        
        # Path Manager
        "select_wow_folder_title": "选择魔兽世界文件夹",
        "unrecognized_installation": "无法识别的安装",
        "folder_not_valid_continue": "所选文件夹似乎无效。\n\n仍要继续吗？",
        "wow_folder_set": "魔兽世界文件夹已设置：{}",
        
        # Performance
        "performance_execution_time": "[性能] {}耗时{:.3f}秒",
        "perf_moved_trash": "[{}] 已移至回收站：{}",
        "perf_deleted": "[{}] 已删除：{}",
        "perf_error_deleting": "[{}] 删除{}时出错：{}",
        
        "select_valid_wow_optimizer": "在选项中选择有效的魔兽世界文件夹以启用按版本视图。",
        "select_valid_wow_folder_cleaner": "在选项中选择有效的魔兽世界文件夹以启用文件夹清理器。",
        
        # Main UI - Buttons and Messages
        "apply": "应用",
        "cancel": "取消",
        "export_log": "导出日志",
        "clear_log": "清除日志",
        
        # Common Messages
        "no_files_selected": "未选择文件",
        "no_folders_selected": "未选择文件夹",
        "no_orphans_selected": "未选择孤立文件",

        # Common Messages
        "apply_font_question": "将字体'{}'应用于应用程序？",
        "select_valid_wow_first": "请先选择有效的WoW文件夹。",
        "restored": "已恢复",

        # File Cleaner
        "found_files_count": "在所有版本中找到{}个文件。",
        "confirm_action_files": "您确定要{}{}个文件吗？",
        "processed_files_count": "已处理{}个文件。",

        # Folder Cleaner
        "confirm_action_folders": "您确定要{}{}个文件夹吗？",
        "processed_folders_count": "已处理{}个文件夹。",

        # Orphan Cleaner
        "found_orphans_count": "找到{}个孤立SavedVariable。",
        "confirm_action_orphans": "您确定要{}{}个孤立SavedVariables吗？",
        "processed_orphans_count": "已处理{}个孤立项。",

        # Actions
        "move_to_trash": "移至回收站",
        "delete_permanently_action": "永久删除",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "已重建AddOns.txt条目。\n总共写入：{}\n总共删除：{}",

        # Log Export
        "log_empty_nothing_export": "日志为空。没有可导出的内容。",

        # Settings Restore
        "settings_restored_restart": "设置已恢复为默认值。应用程序现在将重新启动。",
        "settings_restored_manual": "设置已恢复为默认值。请手动重新启动应用程序。",
        "failed_restore_defaults": "恢复默认值失败：{}",
        
        # File Cleaner
        
        # Folder Cleaner
        
        # Orphan Cleaner
        
        # Actions
        
        # AddOns.txt Rebuild
        
        # Log Export
        
        # Settings Restore
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "在所有检测到的魔兽世界版本中搜索没有相应已安装插件（Interface/AddOns）的插件SavedVariables（.lua / .lua.bak）。扫描账户、服务器和角色SavedVariables文件夹。处理还会重建AddOns.txt以匹配已安装的插件（尽可能保留启用/禁用状态）。",
        "orphan_description_part2": "注意：Blizzard_*.lua文件是核心游戏数据，为安全起见会自动忽略（但其.lua.bak备份可能会被删除）。",
        "wtf_not_found": "未找到WTF目录。请先启动游戏。",
        "unknown_preset": "未知预设：{}",
        "backup_failed": "创建备份失败：{}",
        "config_write_failed": "写入配置失败：{}",
        "config_updated": "已将{}个设置应用到Config.wtf。",
        "settings_updated_added": "更新了{}个设置，添加了{}个新设置。",
        "backup_saved": " 备份已保存。",
        "version_path": "版本：{}\n路径：{}",
        "optimizer_launch_required": "优化器要求至少启动过一次{}。请启动魔兽世界并进入角色选择屏幕，然后退出游戏。之后，您可以使用优化器应用图形预设。",
        "system_matches": "您的系统匹配：{}",
        "optimizer_title": "优化器 — {}",
        "recommendations_applied": "✓ 已应用推荐设置。",
        "applied_preset_log": "已为{}应用{}预设",
        "apply_preset_failed_log": "应用{}预设失败：{}",
        "hardware_scan_complete": "硬件扫描完成：已缓存到全局设置。",
        "hardware_scan_failed": "硬件扫描失败：{}",
        "scan_error": "✗ 错误：{}",
        
        # Game Validation
        "invalid_game_installation": "无效的游戏安装",
        "game_installation_incomplete": "魔兽世界安装似乎不完整。\n\n请至少运行一次游戏以初始化Interface和WTF文件夹。\n\n运行游戏后，您可以使用此工具清理您的安装。",
        
        # Startup Warning
        "user_disabled_warning": "用户已禁用启动警告。",
        
        # Update Checker
        "no_updates_available": "无可用更新",
        "no_releases_published": "您正在运行{}。\n\n尚未发布任何版本。",
        "update_check_failed": "更新检查失败",
        "update_check_http_error": "无法检查更新：\n\nHTTP {}：{}",
        "update_check_network_error": "无法检查更新：\n\n{}",
        "update_check_error": "更新检查错误",
        "update_check_exception": "检查更新时发生错误：\n\n{}",
        "update_available": "有可用更新",
        "update_message": "有新版本可用！\n\n当前版本：{}\n最新版本：{}\n\n您要现在下载吗？",
        "up_to_date": "已是最新版本",
        "up_to_date_message": "您正在运行最新版本（{}）。",
        "browser_open_error": "无法打开浏览器：\n\n{}",
        "download_update": "下载更新",
        "view_release": "查看发布",
        "later": "稍后",
        "downloading_update": "正在下载更新",
        "downloading_update_file": "正在下载更新文件...",
        "download_failed": "下载失败",
        "download_failed_message": "下载更新失败：\n\n{}",
        "update_ready": "更新就绪",
        "update_downloaded_message": "更新下载成功！\n\n文件：{}\n\n您要现在安装吗？",
        "install_now": "现在安装",
        "install_later": "稍后安装",
        "update_location": "下载位置：{}",
        "failed_to_fetch_release": "无法从GitHub获取发布信息。",
        "no_download_available": "未找到此版本的可下载文件。",
        "install_update": "安装更新",
        "please_run_installer": "下载位置已打开。\n\n请运行安装程序以更新应用程序。",
        "update_saved_message": "更新已保存到：\n\n{}\n\n您可以稍后安装。",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[文件清理] 找到文件：{}",
        "file_cleaner_found": "[文件清理] 找到：{}",
        "file_cleaner_total_found": "[文件清理] 找到的.bak/.old文件总数：{}",
        "file_cleaner_moved_trash": "[文件清理] 已移至回收站：{}",
        "file_cleaner_deleted": "[文件清理] 已删除：{}",
        "file_cleaner_error_deleting": "[文件清理] 删除{}时出错：{}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[文件夹清理] 找到：{}",
        "folder_cleaner_total": "[文件夹清理] 可清理的文件夹总数：{}",
    },
    "zhTW": {
        # Window title
        "window_title": "魔獸世界清理工具",
        
        # Menu/Tab names
        "file_cleaner": "檔案清理",
        "folder_cleaner": "資料夾清理",
        "orphan_cleaner": "孤立檔案清理",
        "game_optimizer": "遊戲最佳化",
        "optimization_suggestions": "最佳化建議",
        "log": "日誌",
        "help_about": "說明/關於",
        
        # Options section
        "options": "選項",
        "wow_folder": "魔獸世界資料夾：",
        "browse": "瀏覽...",
        "browse_tooltip": "瀏覽您的魔獸世界資料夾。",
        "font_size": "字型大小：",
        "font": "字型：",
        "theme": "主題：",
        "language": "語言：",
        "file_action": "檔案操作：",
        "delete_permanently": "永久刪除",
        "move_to_recycle": "移至資源回收筒",
        "enable_verbose": "啟用詳細日誌",
        "verbose_tooltip": "啟用後，日誌將記錄每個處理的檔案/資料夾/AddOns.txt行。",
        "external_log": "外部日誌：",
        "fresh": "新建",
        "fresh_tooltip": "每次匯出時建立新的日誌檔案（覆蓋現有檔案）。",
        "append": "附加",
        "append_tooltip": "將每次匯出附加到現有日誌檔案（根據詳細程度保留10-20個工作階段）。",
        "check_updates": "檢查更新",
        "check_updates_tooltip": "啟用後，將在啟動時檢查GitHub上的新版本。",
        "restore_defaults": "還原預設值",
        "light": "淺色",
        "dark": "深色",
        
        # File Cleaner
        "scan": "掃描",
        "select_all": "全選",
        "expand_all": "全部展開",
        "collapse_all": "全部摺疊",
        "process_selected": "處理選取項目",
        "scanning": "掃描中…",
        "no_bak_old_found": "未找到.bak或.old檔案。",
        "files_found": "找到{}個檔案。",
        
        # Folder Cleaner
        "version": "版本：",
        "path": "路徑：",
        "preview": "預覽",
        "toggle_all": "全部切換",
        "process_folders": "處理選取的資料夾",
        
        # Orphan Cleaner
        "rebuild_addons": "重建AddOns.txt",
        "no_orphans_found": "未找到孤立的SavedVariables。",
        "orphans_found": "找到{}個孤立的SavedVariable。",
        
        # Game Optimizer
        "scan_hardware": "掃描硬體",
        "system_matches": "您的系統符合：",
        "optimization_applied": "✓ 已套用最佳化",
        "optimization_not_applied": "⚠ 尚未套用最佳化",
        "graphics_presets": "圖形預設（{}）：",
        "graphics_presets_classic": "圖形預設（{}）：",
        "apply_preset": "套用預設：",
        "apply": "套用",
        "preset_applied": "✓ 已套用{}預設。",
        "error": "✗ 錯誤：{}",
        "low": "低",
        "medium": "中",
        "high": "高",
        "ultra": "極致",
        
        # Optimization Suggestions
        "manual_suggestions": "手動最佳化建議",
        "manual_disclaimer": "注意：此應用程式不會自動執行這些最佳化。這些是您需要手動實施的建議。",
        "clean_data_folder": "清理遊戲資料資料夾",
        "clean_data_text": "如果安裝魔獸世界後已經過了幾年或多個資料片，請考慮刪除魔獸世界主目錄中的Data資料夾。這*可能*會減小遊戲大小並提高載入畫面效能。Battle.net啟動器會在需要時自動重建此資料夾。",
        "enable_hdr": "啟用HDR（高動態範圍）",
        "enable_hdr_text": "檢查作業系統的顯示設定以查看HDR是否可用。如果您的顯示器支援，啟用HDR可以顯著提高遊戲內的視覺清晰度和色彩深度。",
        "verify_refresh": "驗證顯示器更新率",
        "verify_refresh_text": "確保在作業系統的顯示設定中將顯示器的更新率設定為支援的最大值。更高的更新率可提供更流暢的遊戲體驗和更好的反應性。",
        "enable_sam": "啟用智慧存取記憶體/可調整大小的BAR",
        "enable_sam_text": "檢查主機板BIOS設定中的智慧存取記憶體（AMD）或可調整大小的BAR（Intel/NVIDIA）。啟用此功能可讓CPU存取完整的GPU記憶體，可能會提高效能。",
        "enable_xmp": "啟用XMP記憶體設定檔",
        "enable_xmp_text": "存取主機板BIOS並啟用XMP（極限記憶體設定檔）或DOCP/EOCP設定。這可確保您的記憶體以其額定速度而非預設的保守速度執行，從而提高整體系統效能。",
        
        # Log tab
        "export_log": "匯出日誌",
        "clear_log": "清除日誌",
        
        # Help/About
        "about_text": "魔獸世界的綜合維護和最佳化套件。\n清理不必要的檔案，管理插件，最佳化遊戲效能等。\n\n執行此工具前請務必關閉魔獸世界。",
        "copyright": "版權所有 © 2025 Paul Vandersypen。根據GNU通用公共授權條款v3.0（GPL-3.0-or-later）發布。有關完整條款，請參閱隨附的LICENSE檔案。",
        
        # Dialogs
        "invalid_folder": "無效的資料夾",
        "select_valid_wow": "請先選擇有效的魔獸世界資料夾。",
        "no_selection": "未選擇",
        "no_files_selected": "未選擇要處理的檔案。",
        "no_folders_selected": "未選擇要清理的資料夾。",
        "no_orphans_selected": "未選擇孤立檔案。",
        "confirm": "確認",
        "confirm_action": "確定要{}{}{}嗎？",
        "file_s": "個檔案",
        "folder_s": "個資料夾",
        "orphaned_savedvars": "個孤立的SavedVariables",
        "completed": "已完成",
        "processed": "已處理{}{}。",        "restore_defaults_confirm": "將所有設定還原為預設值？",
        "restart_required": "設定已還原。應用程式現在將重新啟動。",
        "error_title": "錯誤",
        "restore_error": "還原預設值失敗：{}",
        "confirm_font": "確認字型",
        "apply_font_confirm": "將字型'{}'套用到應用程式？",
        "select_font": "選擇字型",
        "export_log_title": "匯出日誌",
        "log_empty": "日誌為空。沒有可匯出的內容。",
        "log_exported": "日誌已成功匯出到：\n{}",
        "export_error": "匯出錯誤",
        "export_failed": "匯出日誌失敗：\n{}",
        "addons_rebuilt": "已重建AddOns.txt項目。\n總共寫入：{}\n總共刪除：{}",
        
        # Log messages
        "session_started": "工作階段已開始 — {}",
        "file_scan": "檔案清理掃描：{}個符合項目。",
        "orphan_scan": "孤立檔案清理掃描：{}個孤立檔案。",
        "file_processed": "檔案清理：已處理{}個檔案。",
        "folder_processed": "資料夾清理：已處理{}個資料夾。",
        "orphan_processed": "孤立檔案清理：已處理{}個孤立檔案。",        "addons_txt_log": "[AddOns.txt] {}：寫入{}個項目，刪除{}個",
        "preset_applied_log": "已為{}套用{}預設",
        "preset_failed_log": "套用{}預設失敗：{}",
        "change_language": "變更語言",
        "change_language_question": "將語言從 {} 變更為 {}？\n\n應用程式將重新啟動以套用新語言。",
        "language_changed": "語言已變更",
        "language_changed_restart": "語言已變更為 {}。\n應用程式現在將重新啟動。",
        "apply": "套用",
        "cancel": "取消",
        "scan_bak_old": "掃描.bak / .old檔案",
        "expand_all": "全部展開",
        "collapse_all": "全部摺疊",
        "select_deselect_all": "全選/取消全選",
        "process_selected_files": "處理選取的檔案",
        "scan_orphaned": "掃描孤立的SavedVariables",
        "process_selected_folders": "處理選取的資料夾",
        "select_deselect_all_folders": "全選/取消全選所有資料夾",
        "select_deselect_all_screenshots": "全選/取消全選所有螢幕截圖檔案",
        "process_selected_screenshots": "處理選定的螢幕截圖",
        "no_screenshots_selected": "未選擇螢幕截圖。",
        "confirm_action_screenshots": "{}{}個螢幕截圖檔案？",
        "processed_screenshots_count": "已處理{}個螢幕截圖。",
        "screenshots_per_file": "螢幕截圖（按檔案操作）",
        "folder_screenshots": "螢幕截圖",
        "folder_logs": "日誌",
        "folder_errors": "錯誤",
        "check_for_updates": "檢查更新",
        
        # Game Optimizer
        "game_optimizer_title": "遊戲最佳化器",
        "game_optimizer_desc": "根據您的硬體配置最佳化魔獸世界的效能。",
        "scan_hardware": "掃描硬體",
        "click_scan_hardware": "點擊「掃描硬體」以偵測您系統的功能。",
        "select_valid_wow_folder": "在選項中選擇有效的魔獸世界資料夾以啟用按版本檢視。",
        "recommended_settings": "建議設定：",
        "apply_preset_label": "套用預設：",
        "apply_recommended_settings": "套用建議設定",
        "scanning_cpu": "正在掃描CPU...",
        "scanning_ram": "正在掃描記憶體...（已偵測到CPU：{}核心/{}執行緒）",
        "scanning_gpu": "正在掃描GPU...（已偵測到記憶體：{} GB）",
        
        # Startup warning
        "important_notice": "重要提示",
        "startup_warning_text": "⚠️ 在使用此工具之前，請確保魔獸世界已完全關閉。\n\n在魔獸世界開啟時執行該工具可能會干擾遊戲檔案。",
        "do_not_show_again": "不再顯示此警告",
        "ok": "確定",
        
        # Folder cleaner
        "select_valid_wow_folder_cleaner": "在選項中選擇有效的魔獸世界資料夾以啟用資料夾清理器。",
        "preview_label": "預覽",
        "preview_hint": "(點擊圖片放大 • 再次點擊或按 Esc 關閉)",
        "screenshots_not_found": "未找到此版本的螢幕截圖資料夾。",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "手動最佳化建議",
        "opt_sug_disclaimer": "注意：此應用程式不會自動執行這些最佳化。這些是您需要手動實施的建議。",
        "opt_sug_clean_data_title": "清理遊戲資料資料夾",
        "opt_sug_clean_data_text": "如果安裝魔獸世界後已經過了幾年或多個資料片，請考慮刪除魔獸世界主目錄中的Data資料夾。這*可能*會減小遊戲大小並提高載入畫面效能。Battle.net啟動器會在需要時自動重建此資料夾。",
        "opt_sug_clean_data_tooltip": "原因：Data資料夾會隨著時間的推移累積暫存和快取的遊戲資源。刪除它會強制重新下載最佳化的檔案。\n\n風險等級：安全 - Battle.net將自動重新下載所需檔案。\n\n預期收益：更快的載入畫面，減少磁碟使用量（可能節省10-20 GB）。",
        "opt_sug_hdr_title": "啟用HDR（高動態範圍）",
        "opt_sug_hdr_text": "檢查作業系統的顯示設定以查看HDR是否可用。如果您的顯示器支援，啟用HDR可以顯著提高遊戲內的視覺清晰度和色彩深度。",
        "opt_sug_hdr_tooltip": "原因：HDR提供更廣的色域和更好的對比度，使視覺效果更加生動和逼真。\n\n風險等級：安全 - 可在作業系統設定中輕鬆開關。\n\n預期收益：如果顯示器支援HDR10或更高版本，視覺品質會顯著提升。\n\n要求：支援HDR的顯示器和Windows 10/11或macOS Catalina+。",
        "opt_sug_refresh_title": "驗證顯示器更新率",
        "opt_sug_refresh_text": "確保在作業系統的顯示設定中將顯示器的更新率設定為支援的最大值。更高的更新率可提供更流暢的遊戲體驗和更好的反應性。",
        "opt_sug_refresh_tooltip": "原因：即使顯示器支援120Hz/144Hz/165Hz，許多系統預設為60Hz。這會不必要地限制畫面更新率。\n\n風險等級：安全 - 無硬體風險，易於恢復。\n\n預期收益：更流暢的遊戲體驗，減少輸入延遲，更好的反應時間。\n\n如何檢查：Windows：設定 > 顯示 > 進階 > 更新率\nmacOS：系統偏好設定 > 顯示器",
        "opt_sug_sam_title": "啟用智慧存取記憶體/可調整大小的BAR",
        "opt_sug_sam_text": "檢查主機板BIOS設定中的智慧存取記憶體（AMD）或可調整大小的BAR（Intel/NVIDIA）。啟用此功能可讓CPU存取完整的GPU記憶體，可能會提高效能。",
        "opt_sug_sam_tooltip": "原因：允許CPU一次存取整個GPU記憶體，而不是小的256MB區塊，減少瓶頸。\n\n風險等級：中等 - 需要變更BIOS。首先記錄目前設定。\n\n預期收益：在GPU密集型場景中提升5-15%的FPS。\n\n要求：\n• AMD：Ryzen 5000+ CPU + RX 6000+ GPU\n• Intel：第10代+ CPU + RTX 3000+ GPU\n• 可能需要BIOS更新",
        "opt_sug_xmp_title": "啟用XMP記憶體設定檔",
        "opt_sug_xmp_text": "存取主機板BIOS並啟用XMP（極限記憶體設定檔）或DOCP/EOCP設定。這可確保您的記憶體以其額定速度而非預設的保守速度執行，從而提高整體系統效能。",
        "opt_sug_xmp_tooltip": "原因：記憶體通常預設以2133MHz執行，即使額定為3200MHz+。XMP啟用廣告速度。\n\n風險等級：中等 - BIOS變更。如果記憶體不穩定，系統可能無法啟動（易於重設）。\n\n預期收益：CPU效能提升10-20%，載入時間更快，更好的1%低點。\n\n如何啟用：進入BIOS（啟動時通常按Del/F2） > 找到XMP/DOCP設定 > 啟用 > 儲存並離開",
        "opt_sug_reinstall_title": "重新安裝WoW（乾淨安裝）",
        "opt_sug_reinstall_text": "備份您的AddOns和WTF資料夾，透過Battle.net解除安裝所有WoW版本，重新安裝，然後還原您的備份。這將移除多年修補程式累積的舊檔案和過時資料。",
        "opt_sug_reinstall_tooltip": "原因：多年的更新會留下過時的檔案、棄用的資源和碎片化資料，導致載入速度變慢並浪費空間。\n\n風險等級：低 - 您的設定/插件保存在WTF/AddOns資料夾中。\n\n預期收益：更快的載入時間，減少磁碟使用量（節省5-15 GB），提高穩定性。\n\n操作方法：1) 備份Interface\\AddOns和WTF\n2) 透過Battle.net解除安裝\n3) 重新安裝WoW\n4) 複製備份的資料夾",
        
        # Help/About tab - content
        "help_version_label": "魔獸世界清理工具 {}",
        "help_about_description": "魔獸世界的綜合維護和最佳化套件。\n清理不必要的檔案，管理插件，最佳化遊戲效能等。\n\n執行此工具前請務必關閉魔獸世界。",
        "help_copyright": "版權所有 © 2025 Paul Vandersypen。根據GNU通用公共授權條款v3.0（GPL-3.0-or-later）發布。有關完整條款，請參閱隨附的LICENSE檔案。",
        "support_patreon": "在 Patreon 上支持",
        "donate_paypal": "透過 PayPal 捐款",
        "github_repository": "GitHub儲存庫",
        "github_issues": "回報問題",

        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU：{} | 記憶體：{} | GPU：{}",
        "gpu_switch_notification": "⚠ GPU切換：設定為使用'{}'而不是'{}'。此變更透過使用您的獨立GPU來最佳化效能，以獲得更好的遊戲體驗。這是安全且建議的。",
        "scan_tooltip_refresh": "除非您變更了CPU、GPU或記憶體，否則無需再次掃描。\n點擊重新整理快取的硬體資訊。",
        "scanning_ram_detected": "正在掃描記憶體...（已偵測到CPU：{}核心/{}執行緒）",
        "scanning_gpu_detected": "正在掃描GPU...（已偵測到記憶體：{} GB）",
        "apply_preset_label": "套用預設：",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "魔獸世界正在執行",
        "wow_running_message": "魔獸世界目前正在執行。變更將在重新啟動遊戲後生效。\n\n是否要繼續？",
        "permission_error_title": "權限錯誤",
        "permission_error_message": "Config.wtf是唯讀的。請移除唯讀屬性，然後重試。",
        "config_readonly_status": "✗ Config.wtf是唯讀的。",
        "confirm_apply_title": "確認套用",
        "confirm_apply_message": "將{}預設套用到{}？\n\n這將修改Config.wtf中的{}個圖形設定。\n將自動建立備份。\n\n主要變更：\n• 預設：{}品質設定\n• 效能：{}個最佳化",
        "cancelled_by_user": "使用者取消。",
        "settings_applied_status": "✓ 已套用{}設定。",
        "preset_applied_status": "✓ 已套用{}預設。",
        "apply_error_status": "✗ 錯誤：{}",
        
        # Preset tooltips
        "preset_tooltip_template": "{}預設\n\n預期效能：\n{}\n\n點擊下方的'套用'以使用此預設。",
        "perf_depends_hardware": "效能影響取決於您的硬體。",
        "perf_will_vary": "效能會有所不同",
        
        # Low preset performance estimates
        "low_perf_high": "出色的效能（大多數場景100+ FPS）",
        "low_perf_mid": "非常好的效能（80-120 FPS）",
        "low_perf_low": "良好的效能（60-80 FPS）",
        
        # Medium preset performance estimates
        "medium_perf_high": "出色的效能（90-120 FPS）",
        "medium_perf_mid": "良好的效能（60-90 FPS）",
        "medium_perf_low": "中等效能（45-60 FPS）",
        
        # High preset performance estimates
        "high_perf_high": "非常好的效能（70-100 FPS）",
        "high_perf_mid": "良好的效能（50-70 FPS）",
        "high_perf_low": "在團隊副本中可能吃力（30-50 FPS）",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "良好的效能（60-80 FPS）",
        "ultra_perf_mid": "中等效能（40-60 FPS）",
        "ultra_perf_low": "較低效能（20-40 FPS）",
        
        # WoW version names
        "version_retail": "正式伺服器",
        "version_classic": "懷舊伺服器",
        "version_classic_era": "經典舊世",
        "version_ptr": "測試伺服器",
        "version_beta": "測試伺服器",
        
        # Game Optimizer - additional strings
        "not_detected": "未偵測到",
        "unknown_cpu": "未知CPU",
        "unknown_gpu": "未知",
        "not_set": "未設定",
        "hover_for_details": "懸停檢視詳情",
        
        # Orphan Cleaner - log messages
        "orphan_found_in": "[孤立檔案清理] 在{0}中發現孤立檔案：{1}",
        "orphan_total_found": "[孤立檔案清理] 孤立的SavedVariables總數：{0}",
        "orphan_moved_trash": "[孤立檔案清理] 已移至資源回收筒：{0}",
        "orphan_deleted": "[孤立檔案清理] 已刪除：{0}",
        "orphan_error_deleting": "[孤立檔案清理] 刪除{0}時發生錯誤：{1}",
        "orphan_rebuilt_addons": "[孤立檔案清理] 已重建：{0}",
        "orphan_error_writing_addons": "[孤立檔案清理] 寫入AddOns.txt {0}時發生錯誤：{1}",
        "orphan_error_rebuild": "[孤立檔案清理] AddOns.txt重建期間發生錯誤：{0}",
        "new_setting_prefix": "[新] ",
        "details_colon": "詳情：",
        "updated_settings": "• 更新了{0}個現有設定",
        "added_settings": "• 新增了{0}個新設定",
        
        # Path Manager
        "select_wow_folder_title": "選擇魔獸世界資料夾",
        "unrecognized_installation": "無法識別的安裝",
        "folder_not_valid_continue": "所選資料夾似乎無效。\n\n仍要繼續嗎？",
        "wow_folder_set": "魔獸世界資料夾已設定：{}",
        
        # Performance
        "performance_execution_time": "[效能] {}耗時{:.3f}秒",
        "perf_moved_trash": "[{}] 已移至資源回收筒：{}",
        "perf_deleted": "[{}] 已刪除：{}",
        "perf_error_deleting": "[{}] 刪除{}時發生錯誤：{}",
        
        "select_valid_wow_optimizer": "在選項中選擇有效的魔獸世界資料夾以啟用按版本檢視。",
        "select_valid_wow_folder_cleaner": "在選項中選擇有效的魔獸世界資料夾以啟用資料夾清理器。",
        
        # Main UI - Buttons and Messages
        "apply": "套用",
        "cancel": "取消",
        "export_log": "匯出日誌",
        "clear_log": "清除日誌",
        
        # Common Messages
        "no_files_selected": "未選擇檔案",
        "no_folders_selected": "未選擇資料夾",
        "no_orphans_selected": "未選擇孤立檔案",

        # Common Messages
        "apply_font_question": "將字體「{}」應用於應用程式？",
        "select_valid_wow_first": "請先選擇有效的WoW資料夾。",
        "restored": "已還原",

        # File Cleaner
        "found_files_count": "在所有版本中找到{}個檔案。",
        "confirm_action_files": "您確定要{}{}個檔案嗎？",
        "processed_files_count": "已處理{}個檔案。",

        # Folder Cleaner
        "confirm_action_folders": "您確定要{}{}個資料夾嗎？",
        "processed_folders_count": "已處理{}個資料夾。",

        # Orphan Cleaner
        "found_orphans_count": "找到{}個孤立SavedVariable。",
        "confirm_action_orphans": "您確定要{}{}個孤立SavedVariables嗎？",
        "processed_orphans_count": "已處理{}個孤立項。",

        # Actions
        "move_to_trash": "移至資源回收筒",
        "delete_permanently_action": "永久刪除",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "已重建AddOns.txt條目。\n總共寫入：{}\n總共刪除：{}",

        # Log Export
        "log_empty_nothing_export": "日誌為空。沒有可匯出的內容。",

        # Settings Restore
        "settings_restored_restart": "設定已還原為預設值。應用程式現在將重新啟動。",
        "settings_restored_manual": "設定已還原為預設值。請手動重新啟動應用程式。",
        "failed_restore_defaults": "還原預設值失敗：{}",
        
        # File Cleaner
        
        # Folder Cleaner
        
        # Orphan Cleaner
        
        # Actions
        
        # AddOns.txt Rebuild
        
        # Log Export
        
        # Settings Restore
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "在所有偵測到的魔獸世界版本中搜尋沒有相應已安裝插件（Interface/AddOns）的插件SavedVariables（.lua / .lua.bak）。掃描帳號、伺服器和角色SavedVariables資料夾。處理還會重建AddOns.txt以符合已安裝的插件（盡可能保留啟用/停用狀態）。",
        "orphan_description_part2": "注意：Blizzard_*.lua檔案是核心遊戲資料，為安全起見會自動忽略（但其.lua.bak備份可能會被刪除）。",
        "wtf_not_found": "未找到WTF目錄。請先啟動遊戲。",
        "unknown_preset": "未知預設：{}",
        "backup_failed": "建立備份失敗：{}",
        "config_write_failed": "寫入設定失敗：{}",
        "config_updated": "已將{}個設定套用到Config.wtf。",
        "settings_updated_added": "更新了{}個設定，新增了{}個新設定。",
        "backup_saved": " 備份已儲存。",
        "version_path": "版本：{}\n路徑：{}",
        "optimizer_launch_required": "最佳化器要求至少啟動過一次{}。請啟動魔獸世界並進入角色選擇畫面，然後結束遊戲。之後，您可以使用最佳化器套用圖形預設。",
        "system_matches": "您的系統符合：{}",
        "optimizer_title": "最佳化器 — {}",
        "recommendations_applied": "✓ 已套用建議設定。",
        "applied_preset_log": "已為{}套用{}預設",
        "apply_preset_failed_log": "套用{}預設失敗：{}",
        "hardware_scan_complete": "硬體掃描完成：已快取到全域設定。",
        "hardware_scan_failed": "硬體掃描失敗：{}",
        "scan_error": "✗ 錯誤：{}",
        
        # Game Validation
        "invalid_game_installation": "無效的遊戲安裝",
        "game_installation_incomplete": "魔獸世界安裝似乎不完整。\n\n請至少執行一次遊戲以初始化Interface和WTF資料夾。\n\n執行遊戲後，您可以使用此工具清理您的安裝。",
        
        # Startup Warning
        "user_disabled_warning": "使用者已停用啟動警告。",
        
        # Update Checker
        "no_updates_available": "無可用更新",
        "no_releases_published": "您正在執行{}。\n\n尚未發布任何版本。",
        "update_check_failed": "更新檢查失敗",
        "update_check_http_error": "無法檢查更新：\n\nHTTP {}：{}",
        "update_check_network_error": "無法檢查更新：\n\n{}",
        "update_check_error": "更新檢查錯誤",
        "update_check_exception": "檢查更新時發生錯誤：\n\n{}",
        "update_available": "有可用更新",
        "update_message": "有新版本可用！\n\n目前版本：{}\n最新版本：{}\n\n您要現在下載嗎？",
        "up_to_date": "已是最新版本",
        "up_to_date_message": "您正在執行最新版本（{}）。",
        "browser_open_error": "無法開啟瀏覽器：\n\n{}",
        "download_update": "下載更新",
        "view_release": "檢視發布",
        "later": "稍後",
        "downloading_update": "正在下載更新",
        "downloading_update_file": "正在下載更新檔案...",
        "download_failed": "下載失敗",
        "download_failed_message": "下載更新失敗：\n\n{}",
        "update_ready": "更新就緒",
        "update_downloaded_message": "更新下載成功！\n\n檔案：{}\n\n您要現在安裝嗎？",
        "install_now": "現在安裝",
        "install_later": "稍後安裝",
        "update_location": "下載位置：{}",
        "failed_to_fetch_release": "無法從GitHub取得發布資訊。",
        "no_download_available": "未找到此版本的可下載檔案。",
        "install_update": "安裝更新",
        "please_run_installer": "下載位置已開啟。\n\n請執行安裝程式以更新應用程式。",
        "update_saved_message": "更新已儲存到：\n\n{}\n\n您可以稍後安裝。",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[檔案清理] 找到檔案：{}",
        "file_cleaner_found": "[檔案清理] 找到：{}",
        "file_cleaner_total_found": "[檔案清理] 找到的.bak/.old檔案總數：{}",
        "file_cleaner_moved_trash": "[檔案清理] 已移至資源回收筒：{}",
        "file_cleaner_deleted": "[檔案清理] 已刪除：{}",
        "file_cleaner_error_deleting": "[檔案清理] 刪除{}時發生錯誤：{}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[資料夾清理] 找到：{}",
        "folder_cleaner_total": "[資料夾清理] 可清理的資料夾總數：{}",
    },
    "ukUA": {
        # Window title
        "window_title": "Утиліта Очищення WoW",
        
        # Menu/Tab names
        "file_cleaner": "Очищення Файлів",
        "folder_cleaner": "Очищення Папок",
        "orphan_cleaner": "Очищення Сиріт",
        "game_optimizer": "Оптимізація Гри",
        "optimization_suggestions": "Поради з Оптимізації",
        "log": "Журнал",
        "help_about": "Довідка/Про програму",
        
        # Options section
        "options": "Параметри",
        "wow_folder": "Папка WoW:",
        "browse": "Огляд...",
        "browse_tooltip": "Оберіть папку World of Warcraft.",
        "font_size": "Розмір шрифту:",
        "font": "Шрифт:",
        "theme": "Тема:",
        "language": "Мова:",
        "file_action": "Дія з файлами:",
        "delete_permanently": "Видалити назавжди",
        "move_to_recycle": "Перемістити до Кошика",
        "enable_verbose": "Детальний журнал",
        "verbose_tooltip": "Якщо увімкнено, журнал записує кожен оброблений файл/папку/рядок AddOns.txt.",
        "external_log": "Зовнішній журнал:",
        "fresh": "Новий",
        "fresh_tooltip": "Створювати новий файл журналу при кожному експорті (перезаписує існуючий).",
        "append": "Додати",
        "append_tooltip": "Додавати кожен експорт до існуючого файлу журналу (зберігає 10-20 сеансів залежно від деталізації).",
        "check_updates": "Перевіряти оновлення",
        "check_updates_tooltip": "Якщо увімкнено, перевіряє наявність нових версій на GitHub при запуску.",
        "restore_defaults": "Відновити налаштування",
        "light": "Світла",
        "dark": "Темна",
        
        # File Cleaner
        "scan": "Сканувати",
        "select_all": "Вибрати все",
        "expand_all": "Розгорнути все",
        "collapse_all": "Згорнути все",
        "process_selected": "Обробити вибране",
        "scanning": "Сканування…",
        "no_bak_old_found": "Файли .bak або .old не знайдено.",
        "files_found": "Знайдено файлів: {}.",
        
        # Folder Cleaner
        "version": "Версія:",
        "path": "Шлях:",
        "preview": "Попередній перегляд",
        "toggle_all": "Перемкнути все",
        "process_folders": "Обробити вибрані папки",
        
        # Orphan Cleaner
        "rebuild_addons": "Перебудувати AddOns.txt",
        "no_orphans_found": "Осиротілих SavedVariables не знайдено.",
        "orphans_found": "Знайдено {} осиротілих SavedVariables.",
        
        # Game Optimizer
        "scan_hardware": "Сканувати обладнання",
        "system_matches": "Ваша система відповідає:",
        "optimization_applied": "✓ Оптимізацію застосовано",
        "optimization_not_applied": "⚠ Оптимізацію ще не застосовано",
        "graphics_presets": "Графічні пресети ({}):",
        "graphics_presets_classic": "Графічні пресети ({}):",
        "apply_preset": "Застосувати пресет:",
        "apply": "Застосувати",
        "preset_applied": "✓ Пресет {} застосовано.",
        "error": "✗ Помилка: {}",
        "low": "Низькі",
        "medium": "Середні",
        "high": "Високі",
        "ultra": "Ультра",
        
        # Optimization Suggestions
        "manual_suggestions": "Рекомендації з Ручної Оптимізації",
        "manual_disclaimer": "Примітка: ця програма НЕ виконує ці оптимізації автоматично. Це рекомендації, які ви маєте реалізувати вручну.",
        "clean_data_folder": "Очистити папку Data гри",
        "clean_data_text": "Якщо минуло кілька років або доповнень з моменту встановлення WoW, розгляньте можливість видалення папки Data у головному каталозі World of Warcraft. Це *може* зменшити розмір гри та покращити продуктивність екрана завантаження. Лаунчер Battle.net автоматично відновить цю папку за потреби.",
        "enable_hdr": "Увімкнути HDR (розширений динамічний діапазон)",
        "enable_hdr_text": "Перевірте налаштування дисплея операційної системи, чи доступний HDR. Якщо ваш монітор підтримує його, увімкнення HDR може значно покращити візуальну чіткість та глибину кольору в грі.",
        "verify_refresh": "Перевірте частоту оновлення монітора",
        "verify_refresh_text": "Переконайтеся, що частота оновлення монітора встановлена на максимально підтримувану в налаштуваннях дисплея операційної системи. Вища частота забезпечує плавніший ігровий процес та кращу чуйність.",
        "enable_sam": "Увімкнути Smart Access Memory/Resizable BAR",
        "enable_sam_text": "Перевірте налаштування BIOS материнської плати на наявність Smart Access Memory (AMD) або Resizable BAR (Intel/NVIDIA). Увімкнення дозволяє процесору отримувати доступ до всієї пам'яті GPU, потенційно покращуючи продуктивність.",
        "enable_xmp": "Увімкнути профілі пам'яті XMP",
        "enable_xmp_text": "Увійдіть до BIOS материнської плати та увімкніть XMP (Extreme Memory Profile) або налаштування DOCP/EOCP. Це гарантує, що ваша оперативна пам'ять працює на номінальній швидкості замість консервативної швидкості за замовчуванням, покращуючи загальну продуктивність системи.",
        
        # Log tab
        "export_log": "Експортувати журнал",
        "clear_log": "Очистити журнал",
        
        # Help/About
        "about_text": "Комплексний набір інструментів для обслуговування та оптимізації World of Warcraft.\nОчищайте непотрібні файли, керуйте аддонами, оптимізуйте продуктивність гри тощо.\n\nЗавжди закривайте World of Warcraft перед запуском цієї утиліти.",
        "copyright": "Авторські права © 2025 Paul Vandersypen. Випущено на умовах GNU General Public License v3.0 (GPL-3.0-or-later). Повні умови див. у доданому файлі LICENSE.",
        
        # Dialogs
        "invalid_folder": "Недійсна папка",
        "select_valid_wow": "Будь ласка, спочатку оберіть дійсну папку WoW.",
        "no_selection": "Немає вибору",
        "no_files_selected": "Файли для обробки не вибрано.",
        "no_folders_selected": "Папки для очищення не вибрано.",
        "no_orphans_selected": "Осиротілі файли не вибрано.",
        "confirm": "Підтвердження",
        "confirm_action": "Ви впевнені, що хочете {} {} {}?",
        "file_s": " файл(ів)",
        "folder_s": " папок(и)",
        "orphaned_savedvars": " осиротілих SavedVariables",
        "completed": "Завершено",
        "processed": "Оброблено {} {}.",        "restore_defaults_confirm": "Відновити всі налаштування за замовчуванням?",
        "restart_required": "Налаштування відновлено. Програму буде перезапущено.",
        "error_title": "Помилка",
        "restore_error": "Не вдалося відновити налаштування за замовчуванням: {}",
        "confirm_font": "Підтвердити шрифт",
        "apply_font_confirm": "Застосувати шрифт '{}' до програми?",
        "select_font": "Обрати шрифт",
        "export_log_title": "Експорт журналу",
        "log_empty": "Журнал порожній. Нема чого експортувати.",
        "log_exported": "Журнал успішно експортовано до:\n{}",
        "export_error": "Помилка експорту",
        "export_failed": "Не вдалося експортувати журнал:\n{}",
        "addons_rebuilt": "Записи AddOns.txt перебудовано.\nВсього записано: {}\nВсього видалено: {}",
        
        # Log messages
        "session_started": "Сеанс розпочато — {}",
        "file_scan": "Сканування очищення файлів: {} збігів.",
        "orphan_scan": "Сканування очищення сиріт: {} сиріт.",
        "file_processed": "Очищення файлів: оброблено {} файлів.",
        "folder_processed": "Очищення папок: оброблено {} папок.",
        "orphan_processed": "Очищення сиріт: оброблено {} сиріт.",        "addons_txt_log": "[AddOns.txt] {}: записано {}, видалено {}",
        "preset_applied_log": "Пресет {} застосовано для {}",
        "preset_failed_log": "Не вдалося застосувати пресет {}: {}",
        "change_language": "Змінити мову",
        "change_language_question": "Змінити мову з {} на {}?\n\nПрограма буде перезапущена для застосування нової мови.",
        "language_changed": "Мову змінено",
        "language_changed_restart": "Мову змінено на {}.\nПрограма буде перезапущена.",
        
        # Additional buttons and UI elements
        "apply": "Застосувати",
        "cancel": "Скасувати",
        "scan_bak_old": "Сканувати файли .bak / .old",
        "expand_all": "Розгорнути все",
        "collapse_all": "Згорнути все",
        "select_deselect_all": "Вибрати/Скасувати вибір всіх",
        "process_selected_files": "Обробити вибрані файли",
        "scan_orphaned": "Сканувати осиротілі SavedVariables",
        "process_selected_folders": "Обробити вибрані папки",
        "select_deselect_all_folders": "Вибрати/Скасувати вибір всіх папок",
        "select_deselect_all_screenshots": "Вибрати/Скасувати вибір всіх скріншотів",
        "process_selected_screenshots": "Обробити вибрані скріншоти",
        "no_screenshots_selected": "Скріншоти не вибрано.",
        "confirm_action_screenshots": "{} {} файл(ів) скріншотів?",
        "processed_screenshots_count": "Оброблено {} скріншот(ів).",
        "screenshots_per_file": "Скріншоти (для дії з файлами)",
        "folder_screenshots": "Скріншоти",
        "folder_logs": "Журнали",
        "folder_errors": "Помилки",
        "check_for_updates": "Перевірити оновлення",
        
        # Game Optimizer
        "game_optimizer_title": "Оптимізатор Гри",
        "game_optimizer_desc": "Оптимізуйте продуктивність World of Warcraft на основі вашої апаратної конфігурації.",
        "scan_hardware": "Сканувати обладнання",
        "click_scan_hardware": "Натисніть 'Сканувати обладнання', щоб визначити можливості вашої системи.",
        "select_valid_wow_folder": "Оберіть дійсну папку WoW у Параметрах, щоб увімкнути перегляд за версіями.",
        "recommended_settings": "Рекомендовані налаштування:",
        "apply_preset_label": "Застосувати пресет:",
        "apply_recommended_settings": "Застосувати рекомендовані налаштування",
        "scanning_cpu": "Сканування процесора...",
        "scanning_ram": "Сканування ОЗП... (виявлено процесор: {} ядер/{} потоків)",
        "scanning_gpu": "Сканування відеокарти... (виявлено ОЗП: {} ГБ)",
        
        # Startup warning
        "important_notice": "Важливе повідомлення",
        "startup_warning_text": "⚠️ Перед використанням цієї утиліти переконайтеся, що World of Warcraft повністю закрито.\n\nЗапуск утиліти при відкритому WoW може завадити роботі файлів гри.",
        "do_not_show_again": "Більше не показувати це попередження",
        "ok": "Гаразд",
        
        # Folder cleaner
        "select_valid_wow_folder_cleaner": "Оберіть дійсну папку WoW у Параметрах, щоб увімкнути Очищення Папок.",
        "preview_label": "Попередній перегляд",
        "preview_hint": "(Клацніть на зображення для збільшення • Клацніть знову або натисніть Esc для закриття)",
        "screenshots_not_found": "Папку Screenshots не знайдено для цієї версії.",
        
        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "Рекомендації з Ручної Оптимізації",
        "opt_sug_disclaimer": "Примітка: ця програма НЕ виконує ці оптимізації автоматично. Це рекомендації, які ви маєте реалізувати вручну.",
        "opt_sug_clean_data_title": "Очистити папку Data гри",
        "opt_sug_clean_data_text": "Якщо минуло кілька років або доповнень з моменту встановлення WoW, розгляньте можливість видалення папки Data у головному каталозі World of Warcraft. Це *може* зменшити розмір гри та покращити продуктивність екрана завантаження. Лаунчер Battle.net автоматично відновить цю папку за потреби.",
        "opt_sug_clean_data_tooltip": "Причина: Папка Data з часом накопичує тимчасові та кешовані ігрові ресурси. Її видалення примушує завантажити оптимізовані файли знову.\n\nРівень ризику: Безпечно - Battle.net автоматично завантажить необхідні файли.\n\nОчікувані переваги: Швидше завантаження екранів, менше використання диска (потенційна економія 10-20 ГБ).",
        "opt_sug_hdr_title": "Увімкнути HDR (розширений динамічний діапазон)",
        "opt_sug_hdr_text": "Перевірте налаштування дисплея операційної системи, чи доступний HDR. Якщо ваш монітор підтримує його, увімкнення HDR може значно покращити візуальну чіткість та глибину кольору в грі.",
        "opt_sug_hdr_tooltip": "Причина: HDR забезпечує ширшу колірну гаму та кращу контрастність, роблячи візуальні ефекти яскравішими та реалістичнішими.\n\nРівень ризику: Безпечно - легко вмикається/вимикається в налаштуваннях ОС.\n\nОчікувані переваги: Значне покращення візуальної якості, якщо монітор підтримує HDR10 або вище.\n\nВимоги: Монітор з підтримкою HDR та Windows 10/11 або macOS Catalina+.",
        "opt_sug_refresh_title": "Перевірте частоту оновлення монітора",
        "opt_sug_refresh_text": "Переконайтеся, що частота оновлення монітора встановлена на максимально підтримувану в налаштуваннях дисплея операційної системи. Вища частота забезпечує плавніший ігровий процес та кращу чуйність.",
        "opt_sug_refresh_tooltip": "Причина: Багато систем за замовчуванням встановлюють 60 Гц, навіть якщо монітори підтримують 120 Гц/144 Гц/165 Гц. Це без потреби обмежує частоту кадрів.\n\nРівень ризику: Безпечно - немає ризику для обладнання, легко повернути.\n\nОчікувані переваги: Плавніший ігровий процес, менша затримка вводу, кращий час відгуку.\n\nЯк перевірити: Windows: Параметри > Дисплей > Додатково > Частота оновлення\nmacOS: Системні налаштування > Монітори",
        "opt_sug_sam_title": "Увімкнути Smart Access Memory/Resizable BAR",
        "opt_sug_sam_text": "Перевірте налаштування BIOS материнської плати на наявність Smart Access Memory (AMD) або Resizable BAR (Intel/NVIDIA). Увімкнення дозволяє процесору отримувати доступ до всієї пам'яті GPU, потенційно покращуючи продуктивність.",
        "opt_sug_sam_tooltip": "Причина: Дозволяє процесору отримувати доступ до всієї пам'яті GPU за раз, замість невеликих блоків по 256 МБ, зменшуючи вузькі місця.\n\nРівень ризику: Помірний - вимагає зміни BIOS. Спочатку запишіть поточні налаштування.\n\nОчікувані переваги: Збільшення FPS на 5-15% у GPU-інтенсивних сценах.\n\nВимоги:\n• AMD: Процесор Ryzen 5000+ + відеокарта RX 6000+\n• Intel: Процесор 10-го покоління+ + відеокарта RTX 3000+\n• Може знадобитися оновлення BIOS",
        "opt_sug_xmp_title": "Увімкнути профілі пам'яті XMP",
        "opt_sug_xmp_text": "Увійдіть до BIOS материнської плати та увімкніть XMP (Extreme Memory Profile) або налаштування DOCP/EOCP. Це гарантує, що ваша оперативна пам'ять працює на номінальній швидкості замість консервативної швидкості за замовчуванням, покращуючи загальну продуктивність системи.",
        "opt_sug_xmp_tooltip": "Причина: ОЗП часто працює на частоті 2133 МГц за замовчуванням, навіть якщо розрахована на 3200 МГц+. XMP вмикає заявлені швидкості.\n\nРівень ризику: Помірний - зміна BIOS. Система може не завантажитися, якщо ОЗП нестабільна (легко скинути).\n\nОчікувані переваги: Збільшення продуктивності процесора на 10-20%, швидше завантаження, кращі 1% мінімуми.\n\nЯк увімкнути: Увійдіть до BIOS (зазвичай Del/F2 при завантаженні) > Знайдіть налаштування XMP/DOCP > Увімкніть > Збережіть та вийдіть",
        "opt_sug_reinstall_title": "Перевстановити WoW (Чиста установка)",
        "opt_sug_reinstall_text": "Створіть резервні копії папок AddOns та WTF, видаліть усі версії WoW через Battle.net, перевстановіть і відновіть резервні копії. Це видаляє накопичені застарілі файли та застарілі дані за роки патчів.",
        "opt_sug_reinstall_tooltip": "Причина: Роки оновлень залишають застарілі файли, застарілі ресурси та фрагментовані дані, які сповільнюють завантаження та витрачають місце.\n\nРівень ризику: Низький - Ваші налаштування/аддони зберігаються в папках WTF/AddOns.\n\nОчікувані переваги: Швидше завантаження, менше використаного дискового простору (5-15 ГБ заощаджено), покращена стабільність.\n\nЯк зробити: 1) Резервне копіювання Interface\\AddOns та WTF\n2) Видалити через Battle.net\n3) Перевстановити WoW\n4) Скопіювати резервні папки",
        
        # Help/About tab - content
        "help_version_label": "Утиліта Очищення WoW {}",
        "help_about_description": "Комплексний набір інструментів для обслуговування та оптимізації World of Warcraft.\nОчищайте непотрібні файли, керуйте аддонами, оптимізуйте продуктивність гри тощо.\n\nЗавжди закривайте World of Warcraft перед запуском цієї утиліти.",
        "help_copyright": "Авторські права © 2025 Paul Vandersypen. Випущено на умовах GNU General Public License v3.0 (GPL-3.0-or-later). Повні умови див. у доданому файлі LICENSE.",
        "support_patreon": "Підтримати на Patreon",
        "donate_paypal": "Пожертвувати через PayPal",
        "github_repository": "Репозиторій GitHub",
        "github_issues": "Повідомити про проблему",

        
        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ Процесор: {} | ОЗП: {} | Відеокарта: {}",
        "gpu_switch_notification": "⚠ Перемикання відеокарти: Налаштовано використання '{}' замість '{}'. Ця зміна оптимізує продуктивність, використовуючи вашу дискретну відеокарту для кращого ігрового досвіду. Це безпечно та рекомендовано.",
        "scan_tooltip_refresh": "Не потрібно сканувати знову, якщо ви не змінювали процесор, відеокарту або ОЗП.\nНатисніть, щоб оновити кешовану інформацію про обладнання.",
        "scanning_ram_detected": "Сканування ОЗП... (виявлено процесор: {} ядер/{} потоків)",
        "scanning_gpu_detected": "Сканування відеокарти... (виявлено ОЗП: {} ГБ)",
        "apply_preset_label": "Застосувати пресет:",
        
        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "WoW запущено",
        "wow_running_message": "World of Warcraft наразі запущено. Зміни наберуть чинності після перезапуску гри.\n\nПродовжити?",
        "permission_error_title": "Помилка прав доступу",
        "permission_error_message": "Config.wtf доступний лише для читання. Видаліть атрибут лише для читання та повторіть спробу.",
        "config_readonly_status": "✗ Config.wtf доступний лише для читання.",
        "confirm_apply_title": "Підтвердити застосування",
        "confirm_apply_message": "Застосувати пресет {} до {}?\n\nЦе змінить {} графічних налаштувань у Config.wtf.\nРезервну копію буде створено автоматично.\n\nОсновні зміни:\n• Пресет: Налаштування якості {}\n• Продуктивність: {} оптимізацій",
        "cancelled_by_user": "Скасовано користувачем.",
        "settings_applied_status": "✓ Застосовано {} налаштувань.",
        "preset_applied_status": "✓ Пресет {} застосовано.",
        "apply_error_status": "✗ Помилка: {}",
        
        # Preset tooltips
        "preset_tooltip_template": "Пресет {}\n\nОчікувана продуктивність:\n{}\n\nНатисніть 'Застосувати' нижче, щоб використати цей пресет.",
        "perf_depends_hardware": "Вплив на продуктивність залежить від вашого обладнання.",
        "perf_will_vary": "Продуктивність варіюватиметься",
        
        # Low preset performance estimates
        "low_perf_high": "Чудова продуктивність (100+ FPS у більшості сценаріїв)",
        "low_perf_mid": "Дуже гарна продуктивність (80-120 FPS)",
        "low_perf_low": "Гарна продуктивність (60-80 FPS)",
        
        # Medium preset performance estimates
        "medium_perf_high": "Чудова продуктивність (90-120 FPS)",
        "medium_perf_mid": "Гарна продуктивність (60-90 FPS)",
        "medium_perf_low": "Помірна продуктивність (45-60 FPS)",
        
        # High preset performance estimates
        "high_perf_high": "Дуже гарна продуктивність (70-100 FPS)",
        "high_perf_mid": "Гарна продуктивність (50-70 FPS)",
        "high_perf_low": "Можуть бути труднощі в рейдах (30-50 FPS)",
        
        # Ultra preset performance estimates
        "ultra_perf_high": "Гарна продуктивність (60-80 FPS)",
        "ultra_perf_mid": "Помірна продуктивність (40-60 FPS)",
        "ultra_perf_low": "Низька продуктивність (20-40 FPS)",
        
        # WoW version names
        "version_retail": "Retail",
        "version_classic": "Classic",
        "version_classic_era": "Classic Era",
        "version_ptr": "PTR",
        "version_beta": "Beta",
        
        # Game Optimizer - additional strings
        "not_detected": "Не виявлено",
        "unknown_cpu": "Невідомий процесор",
        "unknown_gpu": "Невідома",
        "not_set": "Не встановлено",
        "hover_for_details": "Наведіть для подробиць",
        
        # Orphan Cleaner - log messages
        "orphan_found_in": "[Очищення Сиріт] Знайдено сироту в {0}: {1}",
        "orphan_total_found": "[Очищення Сиріт] Всього осиротілих SavedVariables: {0}",
        "orphan_moved_trash": "[Очищення Сиріт] Переміщено до кошика: {0}",
        "orphan_deleted": "[Очищення Сиріт] Видалено: {0}",
        "orphan_error_deleting": "[Очищення Сиріт] Помилка видалення {0}: {1}",
        "orphan_rebuilt_addons": "[Очищення Сиріт] Перебудовано: {0}",
        "orphan_error_writing_addons": "[Очищення Сиріт] Помилка запису AddOns.txt {0}: {1}",
        "orphan_error_rebuild": "[Очищення Сиріт] Помилка при перебудові AddOns.txt: {0}",
        "new_setting_prefix": "[Нове] ",
        "details_colon": "Подробиці:",
        "updated_settings": "• Оновлено {} існуючих налаштувань",
        "added_settings": "• Додано {} нових налаштувань",
        
        # Path Manager
        "select_wow_folder_title": "Вибір папки WoW",
        "unrecognized_installation": "Нерозпізнане встановлення",
        "folder_not_valid_continue": "Обрана папка не є дійсною.\n\nВсе одно продовжити?",
        "wow_folder_set": "Папку WoW встановлено: {}",
        
        # Performance
        "performance_execution_time": "[Продуктивність] {} зайняло {:.3f} секунд",
        "perf_moved_trash": "[{}] Переміщено до кошика: {}",
        "perf_deleted": "[{}] Видалено: {}",
        "perf_error_deleting": "[{}] Помилка видалення {}: {}",
        
        "select_valid_wow_optimizer": "Оберіть дійсну папку WoW у Параметрах, щоб увімкнути перегляд за версіями.",
        "select_valid_wow_folder_cleaner": "Оберіть дійсну папку WoW у Параметрах, щоб увімкнути Очищення Папок.",
        
        # Main UI - Buttons and Messages
        "apply": "Застосувати",
        "cancel": "Скасувати",
        "export_log": "Експортувати журнал",
        "clear_log": "Очистити журнал",
        
        # Common Messages
        "no_files_selected": "Файли не вибрано",
        "no_folders_selected": "Папки не вибрано",
        "no_orphans_selected": "Осиротілі файли не вибрано",

        # Common Messages
        "apply_font_question": "Застосувати шрифт '{}' до програми?",
        "select_valid_wow_first": "Будь ласка, спочатку виберіть дійсну папку WoW.",
        "restored": "Відновлено",

        # File Cleaner
        "found_files_count": "Знайдено {} файл(ів) у всіх версіях.",
        "confirm_action_files": "Ви впевнені, що хочете {} {} файл(ів)?",
        "processed_files_count": "Оброблено {} файл(ів).",

        # Folder Cleaner
        "confirm_action_folders": "Ви впевнені, що хочете {} {} папок?",
        "processed_folders_count": "Оброблено {} папок.",

        # Orphan Cleaner
        "found_orphans_count": "Знайдено {} сиріт SavedVariable.",
        "confirm_action_orphans": "Ви впевнені, що хочете {} {} сиріт SavedVariables?",
        "processed_orphans_count": "Оброблено {} сиріт.",

        # Actions
        "move_to_trash": "перемістити у кошик",
        "delete_permanently_action": "видалити назавжди",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "Записи AddOns.txt відновлено.\nВсього записано: {}\nВсього видалено: {}",

        # Log Export
        "log_empty_nothing_export": "Журнал порожній. Нічого експортувати.",

        # Settings Restore
        "settings_restored_restart": "Налаштування відновлено до значень за замовчуванням. Програма буде перезапущена.",
        "settings_restored_manual": "Налаштування відновлено до значень за замовчуванням. Будь ласка, перезапустіть програму вручну.",
        "failed_restore_defaults": "Не вдалося відновити значення за замовчуванням: {}",
        
        # File Cleaner
        
        # Folder Cleaner
        
        # Orphan Cleaner
        
        # Actions
        
        # AddOns.txt Rebuild
        
        # Log Export
        
        # Settings Restore
        
        # Orphan Cleaner Tab
        "orphan_description_part1": "Пошук SavedVariables аддонів (.lua / .lua.bak) без відповідного встановленого аддона (Interface/AddOns) у всіх виявлених версіях WoW. Сканує папки SavedVariables облікових записів, серверів та персонажів. Обробка також перебудовує AddOns.txt відповідно до встановлених аддонів (по можливості зберігаючи стан увімкнено/вимкнено).",
        "orphan_description_part2": "Примітка: Файли Blizzard_*.lua є основними даними гри та автоматично ігноруються для безпеки (але їхні резервні копії .lua.bak можуть бути видалені).",
        "wtf_not_found": "Каталог WTF не знайдено. Спочатку запустіть гру.",
        "unknown_preset": "Невідомий пресет: {}",
        "backup_failed": "Не вдалося створити резервну копію: {}",
        "config_write_failed": "Не вдалося записати конфігурацію: {}",
        "config_updated": "Застосовано {} налаштувань до Config.wtf.",
        "settings_updated_added": "Оновлено {} налаштувань, додано {} нових налаштувань.",
        "backup_saved": " Резервну копію збережено.",
        "version_path": "Версія: {}\nШлях: {}",
        "optimizer_launch_required": "Оптимізатор вимагає, щоб {} було запущено принаймні один раз. Запустіть WoW і дійдіть до екрана вибору персонажа, потім вийдіть з гри. Після цього ви зможете використовувати оптимізатор для застосування графічних пресетів.",
        "system_matches": "Ваша система відповідає: {}",
        "optimizer_title": "Оптимізатор — {}",
        "recommendations_applied": "✓ Рекомендовані налаштування застосовано.",
        "applied_preset_log": "Пресет {} застосовано для {}",
        "apply_preset_failed_log": "Не вдалося застосувати пресет {}: {}",
        "hardware_scan_complete": "Сканування обладнання завершено: збережено в глобальних налаштуваннях.",
        "hardware_scan_failed": "Не вдалося виконати сканування обладнання: {}",
        "scan_error": "✗ Помилка: {}",
        
        # Game Validation
        "invalid_game_installation": "Недійсне встановлення гри",
        "game_installation_incomplete": "Встановлення World of Warcraft здається неповним.\n\nЗапустіть гру принаймні один раз, щоб ініціалізувати папки Interface та WTF.\n\nПісля запуску гри ви зможете використовувати цю утиліту для очищення встановлення.",
        
        # Startup Warning
        "user_disabled_warning": "Користувач вимкнув попередження при запуску.",
        
        # Update Checker
        "no_updates_available": "Оновлення недоступні",
        "no_releases_published": "Ви використовуєте {}.\n\nЖодних релізів ще не опубліковано.",
        "update_check_failed": "Не вдалося перевірити оновлення",
        "update_check_http_error": "Не вдалося перевірити оновлення:\n\nHTTP {}: {}",
        "update_check_network_error": "Не вдалося перевірити оновлення:\n\n{}",
        "update_check_error": "Помилка перевірки оновлень",
        "update_check_exception": "Помилка при перевірці оновлень:\n\n{}",
        "update_available": "Доступне оновлення",
        "update_message": "Доступна нова версія!\n\nПоточна версія: {}\nОстання версія: {}\n\nБажаєте завантажити її зараз?",
        "up_to_date": "Актуальна версія",
        "up_to_date_message": "Ви використовуєте останню версію ({}).",
        "browser_open_error": "Не вдалося відкрити браузер:\n\n{}",
        "download_update": "Завантажити оновлення",
        "view_release": "Переглянути реліз",
        "later": "Пізніше",
        "downloading_update": "Завантаження оновлення",
        "downloading_update_file": "Завантаження файлу оновлення...",
        "download_failed": "Помилка завантаження",
        "download_failed_message": "Не вдалося завантажити оновлення:\n\n{}",
        "update_ready": "Оновлення готове",
        "update_downloaded_message": "Оновлення успішно завантажено!\n\nФайл: {}\n\nБажаєте встановити його зараз?",
        "install_now": "Встановити зараз",
        "install_later": "Встановити пізніше",
        "update_location": "Завантажено до: {}",
        "failed_to_fetch_release": "Не вдалося отримати інформацію про реліз з GitHub.",
        "no_download_available": "Файли для завантаження не знайдено для цього релізу.",
        "install_update": "Встановити оновлення",
        "please_run_installer": "Папку завантаження відкрито.\n\nЗапустіть інсталятор для оновлення застосунку.",
        "update_saved_message": "Оновлення збережено в:\n\n{}\n\nВи можете встановити його пізніше.",
        
        # File Cleaner - Log messages
        "file_cleaner_found_file": "[Очищення Файлів] Знайдено файл: {}",
        "file_cleaner_found": "[Очищення Файлів] Знайдено: {}",
        "file_cleaner_total_found": "[Очищення Файлів] Всього знайдено файлів .bak/.old: {}",
        "file_cleaner_moved_trash": "[Очищення Файлів] Переміщено до кошика: {}",
        "file_cleaner_deleted": "[Очищення Файлів] Видалено: {}",
        "file_cleaner_error_deleting": "[Очищення Файлів] Помилка видалення {}: {}",
        
        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[Очищення Папок] Знайдено: {}",
        "folder_cleaner_total": "[Очищення Папок] Всього папок, доступних для очищення: {}",
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
