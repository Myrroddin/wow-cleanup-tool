TRANSLATIONS = {
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
}
