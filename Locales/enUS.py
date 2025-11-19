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
        "folder_processed_screenshots": "Folder Cleaner ({}): Processed {} screenshot(s).",
        "folder_deleted_screenshots_folder": "Folder Cleaner ({}): Deleted empty Screenshots folder.",
        "folder_delete_screenshots_failed": "Folder Cleaner ({}): Could not delete Screenshots folder: {}",
        "orphan_processed": "Orphan Cleaner: processed {} orphan(s).",
        "addons_txt_log": "[AddOns.txt] {}: wrote {} entries, removed {}",
        "preset_applied_log": "Applied {} preset for {}",
        "preset_failed_log": "Failed to apply {} preset: {}",
        "verbose_updated_settings": "Updated {} settings:",
        "verbose_added_settings": "Added {} new settings:",
        "auto_detected_wow": "Auto-detected World of Warcraft installation: {}",
        "running_initial_hardware_scan": "Running initial hardware scan...",
        "smart_defaults_error": "Smart defaults error: {}",
        "failed_to_open_url": "Failed to open URL: {}",

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
}