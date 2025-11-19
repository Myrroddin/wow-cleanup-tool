TRANSLATIONS = {
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
}
