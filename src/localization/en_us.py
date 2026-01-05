"""English (US) translations for WoW Cleanup Tool."""

TRANSLATIONS = {
    "btn_browse": "Browse...",
    "btn_bug_report": "Bug Report",
    "btn_clear_log": "Clear Session Log",
    "btn_clear_persistent_log": "Delete Log File",
    "btn_copy_log": "Copy Log to Clipboard",
    "btn_ok": "OK",
    "btn_open_log_folder": "Open Log Folder",
    "btn_remove_selected": "Remove Selected",
    "btn_remove_selected_screenshots": "Remove Selected Screenshots",
    "btn_reset_settings": "Reset Settings",
    "btn_scan_files": "Scan Files",
    "btn_scan_folders": "Scan Folders",
    "btn_scan_hardware": "Scan Hardware",
    "btn_select_all_screenshots": "Select All Screenshots",
    "btn_select_all_toggle": "Select All / Unselect All",
    "btn_unselect_all_screenshots": "Unselect All Screenshots",
    "cache_age_date_format": "%Y-%m-%d",
    "cache_age_days": "{} days old",
    "cache_age_months": "{} months old",
    "cache_age_under_day": "<1 day old",
    "cache_age_years": "{} years old",
    "dep_install_complete": "Installation Complete",
    "dep_install_complete_msg": (
        "Dependencies were successfully installed, but some packages\n"
        "took longer than expected.\n\n"
        "The application is now ready to use."
    ),
    "dep_install_failed": "Installation Failed",
    "dep_install_failed_msg": (
        "Failed to install required dependencies.\n\n"
        "The application cannot run without these packages.\n\n"
        "Please install manually:\n"
        "pip install send2trash Pillow sv-ttk darkdetect orjson psutil GPUtil py-cpuinfo"
    ),
    "dep_installing_parallel": "Installing {} packages in parallel...",
    "dep_installing_single": "Installing {}...",
    "dep_taking_longer": "Installation is taking longer than expected...",
    "desc_developer_log": (
        "Technical log for debugging, errors, and warnings. These entries may be "
        "requested when reporting bugs."
    ),
    "desc_file_cleaner": (
        "Find and remove unnecessary files. Some files may return when "
        "the game recreates them, which is expected."
    ),
    "desc_folder_cleaner": (
        "Find and remove unnecessary folders. Some folders may return when "
        "the game recreates them, which is expected."
    ),
    "desc_game_optimizer": (
        "Optimize your World of Warcraft Config.wtf files to enhance CPU and GPU performance."
    ),
    "desc_screenshot_interaction": (
        "Click a screenshot in the list to preview it. Click the preview to open it in a larger popup. "
        "Press Escape or click outside the popup to close."
    ),
    "desc_user_log": (
        "Activity log showing what the application is doing. For warnings and errors, "
        "see the Developer Log tab."
    ),
    "error_prefix": "Error",
    "folder_cache": "Cache",
    "folder_errors": "Errors",
    "folder_logs": "Logs",
    "folder_screenshots": "Screenshots",
    "game_version_classic": "Classic",
    "game_version_classic_era": "Classic Era",
    "game_version_modifier_beta": "Beta",
    "game_version_modifier_ptr": "PTR",
    "game_version_retail": "Retail",
    "invalid_wow_path": "Invalid WoW installation path.",
    "label_append_log": "Append Log (Persistent)",
    "label_cpu": "CPU:",
    "label_delete_mode": "Delete Mode:",
    "label_detected_installations": "Detected Installations:",
    "label_font": "Font",
    "label_font_size": "Font Size",
    "label_gpu": "GPU:",
    "label_log_timestamps": "Log Timestamps",
    "label_ram": "RAM:",
    "label_theme": "Theme",
    "label_verbose_logging": "Verbose Logging",
    "label_wow_installation_path": "WoW Installation Path:",
    "license_accept": "Accept",
    "license_decline": "Decline",
    "msg_click_scan_hardware": "Click 'Scan Hardware' to detect your system",
    "msg_hardware_cores": "{} cores",
    "msg_hardware_frequency": "{} GHz",
    "msg_hardware_gpu_dedicated": "(Dedicated)",
    "msg_hardware_gpu_integrated": "(Integrated)",
    "msg_hardware_memory": "{} GB",
    "msg_hardware_ram_speed": "@ {} MHz",
    "msg_gpu_unsupported": "Your graphics card is not supported for optimization. World of Warcraft may not run on your system. Optimization features have been disabled.",
    "msg_license_instructions": (
        "Please read and accept the license agreement to continue using WoW Cleanup Tool."
    ),
    "msg_log_empty": "Log is empty.",
    "msg_multiple_installations": (
        "Multiple World of Warcraft installations detected. "
        "Only one installation should exist on your system."
    ),
    "msg_multiple_installations_instructions": (
        "Please choose one installation to use, or move/uninstall the others. "
        "The application will now exit."
    ),
    "msg_multiple_installations_see_dev_log": (
        "Multiple WoW installations detected. See the Developer Log for details."
    ),
    "msg_wow_close_warning": (
        "Please close World of Warcraft before running this tool to avoid file conflicts."
    ),
    "option_delete_mode_permanent": "Delete Permanently",
    "option_delete_mode_trash": "Move to Trash",
    "option_dont_show_again": "Don't show this again",
    "option_theme_dark": "Dark",
    "option_theme_light": "Light",
    "option_theme_system": "System",
    "press_enter_to_exit": "Press Enter to exit...",
    "select_wow_folder": "Select World of Warcraft Folder",
    "status_hardware_scan_complete": "Hardware scan complete",
    "status_hardware_scan_failed": "Hardware scan failed",
    "status_initializing": "Initializing...",
    "status_log_deleted": "Log Deleted",
    "status_no_hardware_detected": "No hardware detected (psutil not available)",
    "status_optimized": "{} Optimized",
    "status_scanning_hardware": "Scanning hardware...",
    "status_using_gpu": "Using: {}",
    "system_default_font": "System Default",
    "tab_backup_old_cleaner": "Backup & Old Files",
    "tab_developer": "Developer Log",
    "tab_disabled_tooltip": (
        "This feature requires a valid WoW installation path. "
        "Please use the Browse button to select your World of Warcraft folder."
    ),
    "tab_file_cleaner": "File Cleaner",
    "tab_folder_cleaner": "Folder Cleaner",
    "tab_game_optimizer": "Game Optimizer",
    "tab_game_optimizer_disabled": "This tab is disabled because your graphics card is not supported for optimization.",
    "tab_log": "User Log",
    "tab_optimization_suggestions": "Optimization Suggestions",
    "tab_orphaned_addons": "Orphaned AddOn Settings",
    "title_backup_warning": "Important: Backup Your Data",
    "title_dependencies": "Installing Dependencies",
    "title_license": "License Agreement",
    "title_main_window": "WoW Cleanup Tool",
    "title_multiple_installations": "Multiple WoW Installations Detected",
    "tooltip_browse_wow_folder": "Choose your main WoW folder (not a subfolder).",
    "tooltip_cache_warning": (
        "NOT RECOMMENDED: Removing the Cache folder may cause temporary performance issues. "
        "The game will rebuild it automatically. Only remove if experiencing problems."
    ),
    "tooltip_clear_log": "Clear the current session log.",
    "tooltip_clear_persistent_log": (
        "Clear the persistent user log file (only available in append mode)."
    ),
    "tooltip_language_menu": "Select application language",
    "tooltip_log_timestamps": "User Log and Developer Log",
    "tooltip_scan_hardware": "(Cached {})",
    "tooltip_select_all_cache_manual": (
        "Cache must be selected manually. This toggle only affects Errors, Logs, "
        "and Screenshots."
    ),
    "tooltip_user_log_only": "User Log Only",
    "tree_files_count": "files",
    "tree_header_file_path": "File Path",
    "tree_header_size": "Size",
    "unknown": "Unknown",
    "user_log_normal_addons_txt_cleaned": "[{}]: removed {} line(s) from AddOns.txt",
    "user_log_normal_app_failure": (
        "The application failed to start. Please see the Developer Log for details."
    ),
    "user_log_normal_app_started": "Application started successfully!",
    "user_log_normal_gpu_configured": "[{}]: Set gxAdapter to '{}' in Config.wtf",
    "user_log_normal_gpu_unsupported": "Unsupported GPU detected. Game Optimizer tab disabled.",
    "user_log_normal_hardware_detected": "Hardware detected and cached.",
    "user_log_normal_hardware_scan_failed": (
        "Hardware scan failed. See Developer Log for details."
    ),
    "user_log_normal_no_game_versions": "No WoW game versions detected.",
    "user_log_normal_removed_files": "[{}]: removed {} file(s).",
    "user_log_normal_removed_folder": "[{}]: removed {} folder",
    "user_log_normal_wow_detected": "WoW installation detected.",
    "user_log_normal_wow_validated": "WoW installation validated.",
    "user_log_verbose_addons_txt_cleaned": "[{}]: removed {} from AddOns.txt",
    "user_log_verbose_detected_cpu": "Detected CPU: {} - {} cores @ {} GHz",
    "user_log_verbose_detected_cpu_no_freq": "Detected CPU: {} - {} cores",
    "user_log_verbose_detected_gpu": "Detected GPU: {} {}",
    "user_log_verbose_detected_ram": "Detected RAM: {} GB @ {} MHz",
    "user_log_verbose_detected_ram_no_speed": "Detected RAM: {} GB",
    "user_log_verbose_removed_file": "[{}]: removed {}",
    "user_log_verbose_wow_detected": "WoW installation detected at: {}",
    "user_log_verbose_wow_validated": (
        "WoW installation validated. Found {} game version(s)"
    ),
    "warning": "Warning",
    "warning_icon": "⚠",
}
