"""Main window UI creation for WoW Cleanup Tool.

This module contains the MainWindowBuilder class which constructs the entire
main application window including all tabs, controls, and UI elements.

Structure:
- MainWindowBuilder class: Builds the main window with 6 tabs
- Helper methods for tooltips, font refresh, and UI updates
- Integration with theme system, settings, and logging
"""

import os
import tkinter as tk
from tkinter import ttk
import webbrowser

from ui.widgets.tooltip import Tooltip
from ui.log_controls import (
    clear_user_log,
    copy_user_log,
    delete_user_log,
    clear_dev_log,
    copy_dev_log,
    open_log_folder,
)
from ui.tabs.file_cleaner_tab import FileCleanerTab
from ui.tabs.folder_cleaner_tab import FolderCleanerTab
from ui.tabs.game_optimizer_tab import GameOptimizerTab
from ui.tabs.log_tab import LogTab
from ui.tabs.developer_tab import DeveloperTab
from wow.version_manager import GameVersion


class MainWindowBuilder:
    """Builds and manages the main application window.

    This class is responsible for creating the entire UI structure including:
    - Notebook with 6 tabs (File Cleaner, Folder Cleaner, Game Optimizer, Log, Developer)
    - Top control bar with WoW path selection and theme toggle
    - Settings persistence for window geometry, theme, fonts
    - Integration with logging system for real-time log display
    - Game version tracking for multi-flavor operations
    """

    def _show_tooltip(self, widget, text):
        """Display a themed tooltip near the specified widget."""
        try:
            from core.themes import THEMES

            # Clear any existing hover tooltip first
            self._hide_tooltip()

            theme_name = self.settings.get("theme", "light")
            theme = THEMES.get(theme_name, THEMES["light"])
            font_family = self.settings.get("font_family", "TkDefaultFont")
            font_size = int(self.settings.get("font_size", 12))

            tooltip = Tooltip(
                widget, text, theme, font_family, font_size, wraplength=320
            )
            tooltip.show()
            self._active_tooltip = tooltip
        except Exception:
            # Fail silently if tooltips cannot be shown (e.g., during headless tests)
            pass

    def _hide_tooltip(self):
        """Hide the currently displayed hover tooltip (if any)."""
        if getattr(self, "_active_tooltip", None):
            try:
                self._active_tooltip.hide()
            except Exception:
                pass
            self._active_tooltip = None

    def refresh_all_widget_fonts(self):
        """Force refresh of all widget fonts and styles after font/size change.

        This method is called when user changes font family or size in settings.
        It re-applies the current theme to ensure all widgets (including tooltips,
        buttons, labels, etc.) reflect the new font configuration.

        Process:
        1. Loads current font and theme settings
        2. Re-applies theme to update ttk styles
        3. Updates all standard widget types
        4. Refreshes custom elements like bug report icon

        Added: Initial implementation
        Updated: December 28, 2025 - Added bug icon refresh

        Args:
            None

        Returns:
            None
        """
        import sys
        from core.themes import THEMES

        font_family = self.settings.get("font_family", "TkDefaultFont")
        font_size = int(self.settings.get("font_size", 12))
        theme_name = self.settings.get("theme", "light")
        theme_colors = THEMES.get(theme_name, THEMES["light"])
        # ...removed debug print...
        # Re-apply theme to root (updates ttk styles)
        from core.themes import apply_theme

        apply_theme(self.root, theme_name, font_family, font_size)
        # ...removed debug print...
        # Update ttk styles for all major widget types
        Tooltip.refresh_all_visible_tooltips(theme_colors, font_family, font_size)
        style = ttk.Style()
        widget_types = [
            "TLabel",
            "TButton",
            "TEntry",
            "TCombobox",
            "TCheckbutton",
            "TRadiobutton",
            "Treeview",
            "TNotebook",
            "TFrame",
            "Labelframe",
            "TMenubutton",
            "TScrollbar",
        ]

        # Refresh bug icon if it exists
        self._refresh_bug_icon(font_size)

        # Only font/style update logic should be here. All widget creation and layout must be in build().
        pass

    def _refresh_bug_icon(self, font_size):
        """Refresh the bug icon to match current font size."""
        try:
            from PIL import Image, ImageTk
            from pathlib import Path

            # Determine icon size based on font size
            icon_size = max(16, font_size + 6)

            # Load and resize the bug icon
            icon_path = (
                Path(__file__).parent.parent.parent / "assets" / "icons" / "bug_16.png"
            )
            if icon_path.exists():
                bug_icon = Image.open(icon_path)
                bug_icon = bug_icon.resize(
                    (icon_size, icon_size), Image.Resampling.LANCZOS
                )
                self.bug_icon_photo = ImageTk.PhotoImage(bug_icon)
        except Exception:
            # Silently fail if icon refresh is not possible
            pass

    def add_font_controls(self, parent, on_font_family_changed, on_font_size_changed):
        """Add font family and size controls to the given parent widget."""
        # Font Label
        font_label = ttk.Label(parent, text=self.loc._("label_font"), style="TLabel")
        font_label.grid(row=0, column=4, padx=(8, 0))
        # Font Family Combobox
        system_default_label = self.loc._("system_default_font")
        font_list = self.font_utils.get_available_fonts(system_default_label)
        # Map settings value to UI label
        saved_font = self.settings.get("font_family", "TkDefaultFont")
        if saved_font == "TkDefaultFont":
            initial_font_label = system_default_label
        else:
            initial_font_label = saved_font
        self.font_family_var = tk.StringVar(value=initial_font_label)
        font_combo = ttk.Combobox(
            parent,
            textvariable=self.font_family_var,
            values=font_list,
            state="readonly",
            width=18,
        )
        font_combo.grid(row=0, column=5, padx=(8, 0))
        font_combo.bind("<<ComboboxSelected>>", on_font_family_changed)
        self.font_combo = font_combo
        # Font Size Label
        font_size_label = ttk.Label(
            parent, text=self.loc._("label_font_size"), style="TLabel"
        )
        font_size_label.grid(row=0, column=6, padx=(4, 0))
        # Font Size Combobox
        font_sizes = self.font_utils.get_font_sizes()
        saved_size = str(self.settings.get("font_size", 12))
        self.font_size_var = tk.StringVar(value=saved_size)
        font_size_combo = ttk.Combobox(
            parent,
            textvariable=self.font_size_var,
            values=font_sizes,
            state="readonly",
            width=4,
        )
        font_size_combo.grid(row=0, column=7, padx=(4, 0))
        font_size_combo.bind("<<ComboboxSelected>>", on_font_size_changed)
        self.font_size_combo = font_size_combo
        return font_combo, font_size_combo

    def add_theme_toggle(self, parent, command):
        """Add a toggle theme button to the given parent widget."""
        btn = ttk.Button(
            parent,
            text=self.loc._("btn_toggle_theme"),
            command=command,
            style="TButton",
        )
        btn.grid(row=0, column=3, padx=(8, 0))
        # No tooltip for theme toggle button
        return btn

    def __init__(self, *args, **kwargs):
        def show_tooltip(event):
            """Show tooltip when hovering over a disabled tab."""
            if (
                not hasattr(self, "_tab_tooltip_bindings")
                or not self._tab_tooltip_bindings
            ):
                return
            try:
                elem = self.tabbar.identify(event.x, event.y)
                if elem and hasattr(self.tabbar, "index"):
                    tab_idx = self.tabbar.index(f"@{event.x},{event.y}")
                    if tab_idx in self._tab_tooltip_bindings:
                        if (
                            self._current_tooltip_tab == tab_idx
                            and self._tooltip_window
                        ):
                            return
                        tooltip_text = self._tab_tooltip_bindings[tab_idx]
                        if self._tooltip_window:
                            self._tooltip_window.destroy()
                        from core.themes import THEMES

                        current_theme = self.settings.get("theme", "dark")
                        theme_colors = THEMES.get(current_theme, THEMES["dark"])
                        self._tooltip_window = tk.Toplevel(self.tabbar)
                        self._tooltip_window.wm_overrideredirect(True)
                        self._tooltip_window.wm_geometry(
                            f"+{event.x_root + 10}+{event.y_root + 10}"
                        )
                        label = tk.Label(
                            self._tooltip_window,
                            text=tooltip_text,
                            background=theme_colors.get("tooltip_bg", "#ffffe0"),
                            foreground=theme_colors.get("tooltip_fg", "#000000"),
                            relief="solid",
                            borderwidth=1,
                            font=("TkDefaultFont", 9),
                            padx=8,
                            pady=5,
                            wraplength=300,
                            justify="left",
                        )
                        label.pack()
                        self._current_tooltip_tab = tab_idx
                    else:
                        hide_tooltip(None)
            except Exception:
                pass

        def hide_tooltip(event):
            if self._tooltip_window:
                self._tooltip_window.destroy()
                self._tooltip_window = None
                self._current_tooltip_tab = None

        self.tabbar.bind("<Motion>", show_tooltip)
        self.tabbar.bind("<Leave>", hide_tooltip)
        font_size_label.grid(row=0, column=6, padx=(4, 0))
        # Font Size Combobox
        font_sizes = self.font_utils.get_font_sizes()
        self.font_size_var = tk.StringVar(value=str(self.settings.get("font_size", 12)))
        font_size_combo = ttk.Combobox(
            parent,
            textvariable=self.font_size_var,
            values=font_sizes,
            state="readonly",
            width=4,
        )
        font_size_combo.grid(row=0, column=7, padx=(4, 0))
        font_size_combo.bind("<<ComboboxSelected>>", on_font_size_changed)
        # Store references for controller
        self.font_size_combo = font_size_combo
        return font_combo, font_size_combo

    # add_browse_button is now implemented in build(); stub removed.

    def _on_scan_files(self):
        """Scan for backup/old files and orphaned SavedVariables.

        December 30, 2025: Uses BackgroundTask utility for thread-safe scanning.
        Prevents UI freezing while maintaining safe Tkinter widget updates.

        Note: WoW path validation happens on app startup. Feature tabs (including
        File Cleaner) are disabled if no valid path is found, so this method
        is only callable when a valid WoW installation exists.
        """
        from core.background_task import BackgroundTask

        def do_scan():
            """Background task: Scan all WoW versions for files."""
            from operations.file_cleaner import FileCleaner
            from operations.orphan_scanner import OrphanScanner
            from wow.path_manager import PathManager

            def _format_size(size_bytes: int) -> str:
                """Format file size into human-readable string."""
                for unit in ["B", "KB", "MB", "GB"]:
                    if size_bytes < 1024.0:
                        return f"{size_bytes:.1f} {unit}"
                    size_bytes /= 1024.0
                return f"{size_bytes:.1f} TB"

            def _attach_sizes(results):
                """Attach precomputed size strings to scan results."""
                sized_results = {}
                for version_label, files in results.items():
                    sized_files = []
                    for file_path in files:
                        try:
                            size = os.path.getsize(file_path)
                            size_str = _format_size(size)
                        except Exception:
                            size_str = "Unknown"
                        sized_files.append((file_path, size_str))
                    sized_results[version_label] = sized_files
                return sized_results

            # December 30, 2025: Initialize parallel scanners
            # 8 workers optimal for SSDs; automatically reduced for fewer versions
            file_cleaner = FileCleaner(max_workers=8, logger=self.logger, loc=self.loc)
            orphan_scanner = OrphanScanner(
                max_workers=8, logger=self.logger, loc=self.loc
            )

            # December 30, 2025: Detect installed WoW versions
            wow_path = self.settings.get("wow_path")
            path_manager = PathManager(self.loc)
            flavors = path_manager.detect_flavors(wow_path)

            if not flavors:
                self.logger.log(self.loc._("user_log_normal_no_game_versions"))
                return None

            # December 30, 2025: Build version list for parallel scanning
            versions = []
            for flavor_dir in flavors:
                flavor_path = os.path.join(wow_path, flavor_dir)
                version_label = path_manager.get_flavor_display_name(flavor_dir)
                versions.append((flavor_path, version_label))

            # December 30, 2025: Scan for backup/old files
            backup_results = file_cleaner.scan_versions(versions)
            backup_results = _attach_sizes(backup_results)

            # December 30, 2025: Scan for orphaned SavedVariables
            orphan_results = orphan_scanner.scan_versions(versions)
            orphan_results = _attach_sizes(orphan_results)

            return (backup_results, orphan_results)

        def on_complete(results):
            """Main thread callback: Update UI with scan results."""
            if not results:
                return

            backup_results, orphan_results = results

            # December 30, 2025: Update treeviews on main thread (thread-safe)
            if hasattr(self, "file_cleaner_tab"):
                self.file_cleaner_tab.populate_backup_tree(backup_results)
                self.file_cleaner_tab.populate_orphan_tree(orphan_results)

        # December 30, 2025: Execute in background with BackgroundTask utility
        BackgroundTask.run(self.root, do_scan, on_complete, logger=self.logger)

    def _on_remove_selected(self, selected_items):
        # Defensive: ensure selected_items is a list
        if isinstance(selected_items, str):
            self.logger.error(
                f"Bug: _on_remove_selected received string instead of list: {selected_items}"
            )
            return

        if not selected_items:
            return

        from core.background_task import BackgroundTask
        from operations.file_operations import (
            delete_files_batch,
            clean_addons_txt_for_orphans,
        )

        delete_mode = self.delete_mode_var.get()
        selected_paths = list(dict.fromkeys(selected_items))  # preserve order, dedupe

        def _build_version_and_tree_lookup():
            """Build lookup for version labels and which tree each file belongs to."""

            lookup = {}
            tree_lookup = {}
            for tree in (
                getattr(self.file_cleaner_tab, "backup_tree", None),
                getattr(self.file_cleaner_tab, "orphan_tree", None),
            ):
                if not tree:
                    continue

                tree_name = (
                    "orphan" if tree == self.file_cleaner_tab.orphan_tree else "backup"
                )

                for version_node in tree.get_children(""):
                    version_text = tree.item(version_node, "text") or ""
                    version_label = version_text.rsplit(" (", 1)[0].strip()
                    for child in tree.get_children(version_node):
                        path = tree.item(child, "text")
                        if path:
                            lookup[path] = version_label
                            tree_lookup[path] = tree_name

            return lookup, tree_lookup

        version_lookup, tree_lookup = _build_version_and_tree_lookup()

        def _get_version_path_from_file(file_path):
            """Extract WoW version path from a SavedVariables file path.

            Example: C:\\WoW\\_retail_\\WTF\\... -> C:\\WoW\\_retail_
            """

            from wow.path_manager import PathManager

            for flavor_dir in PathManager.WOW_FLAVORS.keys():
                if flavor_dir in file_path:
                    idx = file_path.find(flavor_dir)
                    if idx != -1:
                        end_idx = idx + len(flavor_dir)
                        return file_path[:end_idx]
            return None

        def do_delete():
            """Background deletion honoring user delete mode."""
            processed, _, _, processed_paths = delete_files_batch(
                selected_paths,
                delete_mode=delete_mode,
                logger=self.logger,
                loc=self.loc,
            )

            addons_txt_results = {}
            if processed_paths:
                orphan_files_by_version = {}
                for path in processed_paths:
                    if tree_lookup.get(path) != "orphan":
                        continue

                    version_path = _get_version_path_from_file(path)
                    if version_path:
                        orphan_files_by_version.setdefault(version_path, []).append(
                            path
                        )

                for version_path, orphan_files in orphan_files_by_version.items():
                    cleaned = clean_addons_txt_for_orphans(
                        orphan_files, version_path, self.logger, self.loc
                    )
                    if cleaned:
                        addons_txt_results[version_path] = cleaned

            return processed_paths, addons_txt_results

        def on_complete(result):
            """Main thread: remove deleted items from treeviews and log results."""

            if not hasattr(self, "file_cleaner_tab") or result is None:
                return

            processed_paths, addons_txt_results = result
            if processed_paths is None:
                return

            if processed_paths:
                version_buckets = {}
                for path in processed_paths:
                    version_label = version_lookup.get(path, self.loc._("unknown"))
                    version_buckets.setdefault(version_label, []).append(path)

                for version_label, paths in version_buckets.items():
                    if self.logger._verbose:
                        for path in paths:
                            self.logger.verbose(
                                self.loc._("user_log_verbose_removed_file").format(
                                    version_label, path
                                )
                            )
                    else:
                        self.logger.log(
                            self.loc._("user_log_normal_removed_files").format(
                                version_label, len(paths)
                            )
                        )

            if addons_txt_results:
                from wow.path_manager import PathManager

                path_manager = PathManager(self.loc)
                for version_path, cleaned_files in addons_txt_results.items():
                    version_label = self.loc._("unknown")
                    for flavor_dir in PathManager.WOW_FLAVORS.keys():
                        if version_path.endswith(flavor_dir):
                            version_label = path_manager.get_flavor_display_name(
                                flavor_dir
                            )
                            break

                    total_lines = sum(cleaned_files.values())
                    if self.logger._verbose:
                        for addons_txt_path, removed_count in cleaned_files.items():
                            self.logger.verbose(
                                self.loc._(
                                    "user_log_verbose_addons_txt_cleaned"
                                ).format(version_label, f"{removed_count} addon(s)")
                            )
                    else:
                        self.logger.log(
                            self.loc._("user_log_normal_addons_txt_cleaned").format(
                                version_label, total_lines
                            )
                        )

            removed = set(processed_paths or [])
            for tree in (
                self.file_cleaner_tab.backup_tree,
                self.file_cleaner_tab.orphan_tree,
            ):
                if not tree:
                    continue
                for parent in list(tree.get_children("")):
                    for child in list(tree.get_children(parent)):
                        item_text = tree.item(child, "text")
                        if item_text in removed:
                            tree.delete(child)
                    if not tree.get_children(parent):
                        tree.delete(parent)

        BackgroundTask.run(self.root, do_delete, on_complete, logger=self.logger)

    def get_selected_items(self, context):
        if context == "file_cleaner":
            if not hasattr(self, "file_cleaner_tab"):
                return []
            trees = [
                self.file_cleaner_tab.backup_tree,
                self.file_cleaner_tab.orphan_tree,
            ]
            selected_paths = []
            for tree in trees:
                if not tree:
                    continue
                for iid in tree.selection():
                    # Ignore parent nodes (version headers)
                    if tree.get_children(iid):
                        continue
                    item_text = tree.item(iid, "text")
                    if item_text:
                        selected_paths.append(item_text)
            # Deduplicate while preserving selection order
            return list(dict.fromkeys(selected_paths))
        elif context == "folder_cleaner":
            if not hasattr(self, "folder_cleaner_tab"):
                return []
            return self.folder_cleaner_tab.get_selected_folders()
        return []

    def _on_remove_selected_folders(self, selected_folders):
        """Remove selected folders based on delete mode setting.

        Args:
            selected_folders: List of folder paths to remove
        """
        if not selected_folders:
            return

        from core.background_task import BackgroundTask
        import shutil
        import os

        delete_mode = self.delete_mode_var.get()

        def do_remove():
            """Background task: Remove selected folders."""
            removed_folders = []

            for folder_path in selected_folders:
                try:
                    if delete_mode == "trash":
                        # Move to trash
                        from send2trash import send2trash

                        send2trash(folder_path)
                    else:
                        # Permanent delete
                        shutil.rmtree(folder_path)
                    removed_folders.append(folder_path)

                    # Log with game version and folder name
                    from wow.path_manager import PathManager

                    path_manager = PathManager(self.loc)

                    # Find which game version this folder belongs to
                    game_version_label = self.loc._("unknown")
                    for game_version in self.game_versions:
                        if game_version.flavor_dir in folder_path:
                            game_version_label = game_version.display_name
                            break

                    # Extract folder name from path
                    folder_name = os.path.basename(folder_path.rstrip(os.sep))

                    # Log the removal (always logs regardless of verbose setting)
                    self.logger.log(
                        self.loc._(
                            "user_log_normal_removed_folder",
                            game_version_label,
                            folder_name,
                        )
                    )
                except Exception as e:
                    self.logger.error(f"Failed to remove {folder_path}: {str(e)}")

            return removed_folders

        def on_complete(removed_folders):
            """Main thread callback: Update UI and clear selections."""
            if removed_folders:
                # Clear checkboxes for removed folders
                for (
                    flavor_dir,
                    folders_dict,
                ) in self.folder_cleaner_tab.folder_checkboxes.items():
                    for folder_type, (var, _, folder_path) in folders_dict.items():
                        if folder_path in removed_folders:
                            var.set(False)

        BackgroundTask.run(self.root, do_remove, on_complete, logger=self.logger)

        # Deduplicate while preserving selection order
        return list(dict.fromkeys(selected_paths))

    def _on_scan_folders(self):
        """Scan for cleanable folders and screenshots content.

        Displays found folders in the folder cleaner tab with checkboxes and,
        when a Screenshots folder exists, lists its files for preview.
        Cache folder is always displayed last if found.
        """
        from core.background_task import BackgroundTask

        def do_scan():
            """Background task: Scan all WoW versions for cleanable folders.

            January 3, 2026: Optimized with os.scandir for 2-3x faster screenshot enumeration.
            Uses scandir instead of listdir to avoid loading all names into memory.
            """
            import os
            from wow.path_manager import PathManager

            wow_path = self.settings.get("wow_path")
            path_manager = PathManager(self.loc)
            flavors = path_manager.detect_flavors(wow_path)

            if not flavors:
                self.logger.log(self.loc._("user_log_normal_no_game_versions"))
                return None

            # Folders to scan for (in display order, cache always last)
            folder_types = ["Errors", "Logs", "Screenshots", "Cache"]

            results = {}
            screenshot_files = {}
            allowed_image_exts = {
                ".png",
                ".jpg",
                ".jpeg",
                ".bmp",
                ".gif",
                ".tga",
                ".tiff",
            }

            for flavor_dir in flavors:
                flavor_path = os.path.join(wow_path, flavor_dir)
                found_folders = {}

                for folder_type in folder_types:
                    folder_path = os.path.join(flavor_path, folder_type)
                    # Use try/except instead of exists check (EAFP pattern - faster)
                    try:
                        # January 3, 2026: Use scandir for folder existence check
                        with os.scandir(folder_path) as entries:
                            # Verify it's actually a directory by successfully opening it
                            found_folders[folder_type.lower()] = folder_path

                            if folder_type == "Screenshots":
                                files = []
                                # January 3, 2026: scandir is 2-3x faster than listdir
                                # and doesn't load all filenames into memory at once
                                for entry in entries:
                                    try:
                                        if not entry.is_file(follow_symlinks=False):
                                            continue
                                        _, ext = os.path.splitext(entry.name)
                                        if ext.lower() not in allowed_image_exts:
                                            continue
                                        files.append(entry.path)
                                    except (OSError, PermissionError):
                                        continue

                                screenshot_files[flavor_dir] = sorted(files)
                    except (OSError, PermissionError, FileNotFoundError):
                        # Folder doesn't exist or isn't accessible
                        continue

                if found_folders:
                    results[flavor_dir] = found_folders

            return {"folders": results, "screenshots": screenshot_files}

        def on_complete(results):
            """Main thread callback: Update UI with scan results."""
            if results and hasattr(self, "folder_cleaner_tab"):
                folder_results = results.get("folders", {})
                screenshot_results = results.get("screenshots", {})
                self.folder_cleaner_tab.display_scan_results(
                    folder_results, screenshot_results
                )

        # Execute in background with BackgroundTask utility
        BackgroundTask.run(self.root, do_scan, on_complete, logger=self.logger)

    def __init__(self, root, loc, settings, logger, font_utils):
        """Initialize the main window builder.
        Args:
            root: Tkinter root window
            loc: Localization instance
            settings: Settings dictionary
            logger: Logger instance
            font_utils: Font utilities module
        """
        self.root = root
        self.loc = loc
        self.settings = settings
        self.logger = logger
        self.font_utils = font_utils
        # self.log_text = None
        # self.dev_text = None
        # self.notebook = None
        # self.feature_tab_indices = []
        self.font_family_var = None
        self.font_combo = None
        self.font_size_var = None
        self.log_text = None
        self.dev_text = None
        self.dev_tab_index = None
        self.dev_badge_label = None
        self._active_tooltip = None
        self.wow_path_var = None
        self.path_entry = None
        self.bug_icon_photo = None  # Store reference to bug icon PhotoImage
        self.file_cleaner_tab = None  # Store reference for scan results
        self.folder_cleaner_tab = None  # Store reference for folder scan results
        # Store detected game versions (as GameVersion objects)
        # These are populated during WoW path validation and used by tabs
        self.game_versions: list[GameVersion] = []

        # Track feature tab indices for enable/disable
        self.feature_tab_indices = []

    def build(self, theme_toggle_callback=None):
        # from ui.custom_tabbar import CustomTabBar  # Already imported at top

        """Build and return the main window UI components.
        Returns:
            dict: Dictionary containing references to key UI components
        """
        import sys

        # Initialize font StringVars early
        system_default_label = self.loc._("system_default_font")
        current_font = self.settings.get("font_family", "TkDefaultFont")
        if current_font == "TkDefaultFont":
            self.font_family_var = tk.StringVar(value=system_default_label)
        else:
            self.font_family_var = tk.StringVar(value=current_font)
        self.font_size_var = tk.StringVar(value=str(self.settings.get("font_size", 12)))

        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.rowconfigure(0, weight=0)  # Title
        main_frame.rowconfigure(1, weight=0)  # WoW path
        main_frame.rowconfigure(2, weight=0)  # Delete mode row does not expand
        main_frame.rowconfigure(3, weight=0)  # Tab bar does not expand
        main_frame.rowconfigure(4, weight=1)  # Tab content expands vertically
        main_frame.columnconfigure(0, weight=1)  # Ensure tab bar expands horizontally
        self.main_frame = main_frame

        # Initialize delete mode StringVar
        self.delete_mode_var = tk.StringVar(
            value=self.settings.get("delete_mode", "trash")
        )

        # Initialize verbose logging BooleanVar
        self.verbose_var = tk.BooleanVar(
            value=self.settings.get("verbose_logging", True)
        )

        # Initialize append log BooleanVar (needed before tab creation)
        self.append_log_var = tk.BooleanVar(
            value=self.settings.get("append_log", False)
        )

        # Initialize game versions early (needed before tab creation)
        from wow.path_manager import PathManager

        path_manager = PathManager(self.loc)
        detected_path = path_manager.detect_wow_path()
        valid = (
            path_manager.validate_wow_path(detected_path) if detected_path else False
        )
        if valid and detected_path:
            _, self.game_versions = path_manager.validate_installation(detected_path)
        else:
            self.game_versions = []

        # (Debug prints for wow_path_label must only appear after assignment)
        self._create_tabbed_log_area(main_frame, row=3)

        # Initialize language StringVar with display name
        self.language_var = tk.StringVar(value="English (US)")

        # (Debug prints for detected_path and valid must only appear after assignment)
        # Main frame already created above
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # --- Main Title ---
        title_label = ttk.Label(
            main_frame,
            text=self.loc._("title_main_window"),
            anchor="center",
            style="Title.TLabel",
        )
        title_label.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)
        # --- End Main Title ---

        # WoW path field will be row=1

        # --- WoW Path Field, Browse Button, and Language Dropdown ---
        from wow.path_manager import PathManager

        wow_path_frame = ttk.Frame(main_frame)
        wow_path_frame.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        # Ensure wow_path_frame expands horizontally
        main_frame.columnconfigure(0, weight=1)
        for i in range(8):
            wow_path_frame.columnconfigure(i, weight=0)

        wow_path_label = ttk.Label(
            wow_path_frame, text=self.loc._("label_wow_installation_path")
        )
        wow_path_label.grid(row=0, column=0, sticky="w", padx=(0, 12))

        # Use the already-detected WoW path from earlier in build()
        wow_path_value = detected_path if valid else ""

        self.wow_path_var = tk.StringVar(value=wow_path_value)
        self.path_entry = ttk.Entry(
            wow_path_frame, textvariable=self.wow_path_var, width=24
        )
        self.path_entry.grid(row=0, column=1, sticky="w", padx=(0, 12))
        self.root.update_idletasks()

        # Browse button
        def on_browse():
            import tkinter.filedialog as filedialog

            folder = filedialog.askdirectory(title=self.loc._("select_wow_folder"))
            if folder:
                self.wow_path_var.set(folder)

        browse_btn = ttk.Button(
            wow_path_frame, text=self.loc._("btn_browse"), command=on_browse
        )
        browse_btn.grid(row=0, column=2, sticky="w", padx=(0, 12))
        browse_btn_ttp = self.loc._("tooltip_browse_wow_folder")
        browse_btn.bind(
            "<Enter>", lambda e: self._show_tooltip(browse_btn, browse_btn_ttp)
        )
        browse_btn.bind("<Leave>", lambda e: self._hide_tooltip())

        # Language dropdown (English always first, others sorted alphabetically, native names)
        language_options = [
            ("English (US)", "en_us"),
            ("Deutsch", "de_de"),
            ("Français", "fr_fr"),
            ("Italiano", "it_it"),
            ("Русский", "ru_ru"),
            ("繁體中文", "zh_tw"),
            ("简体中文", "zh_cn"),
            ("Português (Brasil)", "pt_br"),
            ("Español (EU)", "es_es"),
            ("Español (Latinoamérica)", "es_mx"),
            ("Українська", "uk_ua"),
            ("한국어", "ko_kr"),
        ]
        # Sort all except English alphabetically by display name
        english = language_options[0]
        other_langs = sorted(language_options[1:], key=lambda x: x[0].lower())
        language_options = [english] + other_langs
        language_names = [name for name, code in language_options]
        self.language_options = language_options
        self.language_var = tk.StringVar(value=language_names[0])
        language_combo = ttk.Combobox(
            wow_path_frame,
            textvariable=self.language_var,
            values=language_names,
            state="readonly",
            width=20,
        )
        language_combo.grid(row=0, column=3, sticky="w", padx=(0, 12))
        self.language_combo = language_combo

        # Theme toggle button (column 4)
        theme_btn = ttk.Button(
            wow_path_frame,
            text=self.loc._("btn_toggle_theme"),
            command=theme_toggle_callback,
            style="TButton",
        )
        theme_btn.grid(row=0, column=4, padx=(0, 12))

        # Font label (column 5)
        font_label = ttk.Label(
            wow_path_frame, text=self.loc._("label_font"), style="TLabel"
        )
        font_label.grid(row=0, column=5, padx=(0, 12))

        # Font family combobox (column 6)
        system_default_label = self.loc._("system_default_font")
        font_list = self.font_utils.get_available_fonts(system_default_label)
        saved_font = self.settings.get("font_family", "TkDefaultFont")
        initial_font_label = (
            system_default_label if saved_font == "TkDefaultFont" else saved_font
        )
        self.font_family_var = tk.StringVar(value=initial_font_label)
        font_combo = ttk.Combobox(
            wow_path_frame,
            textvariable=self.font_family_var,
            values=font_list,
            state="readonly",
            width=18,
        )
        font_combo.grid(row=0, column=6, padx=(0, 12))
        self.font_combo = font_combo

        # Font size label (column 7)
        font_size_label = ttk.Label(
            wow_path_frame, text=self.loc._("label_font_size"), style="TLabel"
        )
        font_size_label.grid(row=0, column=7, padx=(0, 12))

        # Font size combobox (column 8)
        font_sizes = self.font_utils.get_font_sizes()
        saved_size = str(self.settings.get("font_size", 12))
        self.font_size_var = tk.StringVar(value=saved_size)
        font_size_combo = ttk.Combobox(
            wow_path_frame,
            textvariable=self.font_size_var,
            values=font_sizes,
            state="readonly",
            width=4,
        )
        font_size_combo.grid(
            row=0, column=8, padx=(0, 0)
        )  # Last widget: no right padding
        self.font_size_combo = font_size_combo
        language_combo_ttp = self.loc._("tooltip_language_menu")
        language_combo.bind(
            "<Enter>", lambda e: self._show_tooltip(language_combo, language_combo_ttp)
        )
        language_combo.bind("<Leave>", lambda e: self._hide_tooltip())

        # Debug prints for wow path row widgets (after all widgets are created)
        # ...debug prints removed...

        # Dynamically set minimum window width to fit all widgets in the WoW path row (including paddings)
        total_width = 0
        paddings = [(0, 12), (0, 12), (0, 12), (0, 0)]
        for widget, pad in zip(
            [wow_path_label, self.path_entry, browse_btn, language_combo], paddings
        ):
            widget.update_idletasks()
            total_width += widget.winfo_reqwidth() + sum(pad)
        # Add a little extra for spacing
        min_width = total_width + 20
        self.root.minsize(min_width, self.root.winfo_height())
        # ...debug prints removed...

        # --- UI Layout ---
        # Add row for delete mode selection (Move to Trash / Delete Permanently)
        delete_mode_frame = ttk.Frame(main_frame)
        delete_mode_frame.grid(row=2, column=0, sticky="w", pady=(0, 6), padx=(0, 0))
        for i in range(5):
            delete_mode_frame.columnconfigure(i, weight=0)
        delete_mode_label = ttk.Label(
            delete_mode_frame, text=self.loc._("label_delete_mode")
        )
        delete_mode_label.grid(row=0, column=0, padx=(0, 12), sticky="w")
        trash_rb = ttk.Radiobutton(
            delete_mode_frame,
            text=self.loc._("option_delete_mode_trash"),
            value="trash",
            variable=self.delete_mode_var,
        )
        trash_rb.grid(row=0, column=1, padx=(0, 12), sticky="w")
        permanent_rb = ttk.Radiobutton(
            delete_mode_frame,
            text=self.loc._("option_delete_mode_permanent"),
            value="permanent",
            variable=self.delete_mode_var,
        )
        permanent_rb.grid(row=0, column=2, padx=(0, 12), sticky="w")

        # Add verbose logging checkbox to delete mode row (default on)
        verbose_cb = ttk.Checkbutton(
            delete_mode_frame,
            text=self.loc._("label_verbose_logging"),
            variable=self.verbose_var,
        )
        verbose_cb.grid(row=0, column=3, padx=(0, 12), sticky="w")
        # Add tooltip to verbose logging checkbox
        verbose_cb_ttp = self.loc._("tooltip_user_log_only")
        verbose_cb.bind(
            "<Enter>", lambda e: self._show_tooltip(verbose_cb, verbose_cb_ttp)
        )
        verbose_cb.bind("<Leave>", lambda e: self._hide_tooltip())

        # Add chat timestamps checkbox to delete mode row (default on)
        self.chat_timestamps_var = tk.BooleanVar(
            value=self.settings.get("chat_timestamps", True)
        )

        def on_chat_timestamps_toggle():
            # Update log formatter dynamically
            if hasattr(self.logger, "set_timestamps_enabled"):
                self.logger.set_timestamps_enabled(self.chat_timestamps_var.get())

        chat_timestamps_cb = ttk.Checkbutton(
            delete_mode_frame,
            text=self.loc._("label_log_timestamps"),
            variable=self.chat_timestamps_var,
            command=on_chat_timestamps_toggle,
        )
        chat_timestamps_cb.grid(row=0, column=5, padx=(0, 12), sticky="w")
        chat_timestamps_cb_ttp = self.loc._("tooltip_log_timestamps")
        chat_timestamps_cb.bind(
            "<Enter>",
            lambda e: self._show_tooltip(chat_timestamps_cb, chat_timestamps_cb_ttp),
        )
        chat_timestamps_cb.bind("<Leave>", lambda e: self._hide_tooltip())

        # Add append log checkbox to delete mode row (default off)
        append_log_cb = ttk.Checkbutton(
            delete_mode_frame,
            text=self.loc._("label_append_log"),
            variable=self.append_log_var,
        )
        append_log_cb.grid(row=0, column=4, padx=(0, 12), sticky="w")
        # Add tooltip to append log checkbox
        append_log_cb_ttp = self.loc._("tooltip_user_log_only")
        append_log_cb.bind(
            "<Enter>", lambda e: self._show_tooltip(append_log_cb, append_log_cb_ttp)
        )
        append_log_cb.bind("<Leave>", lambda e: self._hide_tooltip())

        # Add reset settings button (now column 6, no right padding)
        def on_reset_settings():
            from core.settings import get_default_settings, save_settings
            from core.themes import apply_theme
            import tkinter.messagebox as messagebox

            defaults = get_default_settings()
            # Preserve current WoW path if present in the UI
            wow_path = self.wow_path_var.get() if self.wow_path_var else None
            if wow_path:
                defaults["wow_path"] = wow_path

            # Persist defaults immediately
            save_settings(defaults)

            # Update in-memory settings
            self.settings.clear()
            self.settings.update(defaults)

            # Apply theme/fonts from defaults
            theme_name = self.settings.get("theme", "light")
            font_family = self.settings.get("font_family", "TkDefaultFont")
            font_size = int(self.settings.get("font_size", 12))
            apply_theme(self.root, theme_name, font_family, font_size)

            # Update UI-bound variables
            system_default_label = self.loc._("system_default_font")
            self.font_family_var.set(
                system_default_label if font_family == "TkDefaultFont" else font_family
            )
            self.font_size_var.set(str(font_size))
            self.delete_mode_var.set(self.settings.get("delete_mode", "trash"))
            self.verbose_var.set(self.settings.get("verbose_logging", True))
            self.append_log_var.set(self.settings.get("append_log", False))
            self.chat_timestamps_var.set(self.settings.get("chat_timestamps", True))
            self.language_var.set("English (US)")

            # Refresh widgets for new font/theme
            self.refresh_all_widget_fonts()

            # Resize window to fit default content
            try:
                from ui.geometry import resize_to_content

                # 2025-12-30: Use shared helper so reset matches other resize paths
                resize_to_content(self.root, 480, 320)
            except Exception:
                pass

            messagebox.showinfo(
                self.loc._("btn_reset_settings"),
                self.loc._("btn_reset_settings") + " applied.",
            )

        # Add reset settings button (column 6, with consistent padding)
        reset_btn = ttk.Button(
            delete_mode_frame,
            text=self.loc._("btn_reset_settings"),
            command=on_reset_settings,
            style="TButton",
        )
        reset_btn.grid(row=0, column=6, padx=(0, 12), sticky="w")

        # Add bug report button (column 7, with emoji icon)
        # Added: December 28, 2025
        # Opens GitHub issues page in default browser when clicked
        def on_bug_report():
            """Open GitHub issues page for bug reports.

            Launches the default web browser to the project's GitHub issues page
            where users can submit bug reports, feature requests, or view existing issues.

            Args:
                None

            Returns:
                None
            """
            import webbrowser

            webbrowser.open_new("https://github.com/Myrroddin/wow-cleanup-tool/issues")

        # Use ttk.Button with emoji icon (🐞) which is simple, reliable, and scales with font
        # The emoji approach was chosen over PNG icons for:
        # - Automatic scaling with font size changes
        # - No PhotoImage management complexity
        # - Cross-platform compatibility
        # - Accessibility (screen readers can read emoji)
        bug_btn = ttk.Button(
            delete_mode_frame,
            text="🐞 " + self.loc._("btn_bug_report"),  # Localized text from en_us.py
            command=on_bug_report,
            style="TButton",
        )

        bug_btn.grid(row=0, column=7, padx=(0, 0), sticky="w")
        self.root.update_idletasks()

        # Build UI sections
        path_frame = wow_path_frame

        # --- Create the tabbed log area (feature tabs) ---
        self._create_tabbed_log_area(main_frame, row=3)

        # After building, force font/theme refresh to apply persisted settings
        self.refresh_all_widget_fonts()
        # Return references to important widgets
        return {
            "main_frame": self.main_frame,
            "path_frame": wow_path_frame,
            "wow_path_var": self.wow_path_var,
            "path_entry": self.path_entry,
            "font_family_var": self.font_family_var,
            "font_size_var": self.font_size_var,
            "font_combo": getattr(self, "font_combo", None),
            "font_size_combo": getattr(self, "font_size_combo", None),
            "append_log_var": self.append_log_var,
            "language_var": self.language_var,
            "language_combo": getattr(self, "language_combo", None),
            "language_options": getattr(self, "language_options", []),
            "delete_mode_var": self.delete_mode_var,
            "verbose_var": self.verbose_var,
            "reset_button": reset_btn,
            "log_text": getattr(self, "log_text", None),
            "dev_text": getattr(self, "dev_text", None),
        }

    # _create_title is now implemented in build(); stub removed.

    def _create_tabbed_log_area(self, parent, row=2):
        from ui.text_widget_handler import TextWidgetHandler
        import logging
        from core.themes import THEMES

        # Tab definitions
        tabs = [
            ("file_cleaner", self.loc._("tab_file_cleaner")),
            ("folder_cleaner", self.loc._("tab_folder_cleaner")),
            ("game_optimizer", self.loc._("tab_game_optimizer")),
            ("log", self.loc._("tab_log")),
            ("developer", self.loc._("tab_developer")),
        ]
        self.tab_frames = {}
        self.notebook = ttk.Notebook(parent)
        self.dev_tab_index = None
        for idx, (tab_id, tab_label) in enumerate(tabs):
            frame = ttk.Frame(self.notebook, padding=5)
            # Unify tab padding: small horizontal spacing, no vertical padding
            self.notebook.add(frame, text=tab_label, padding=(8, 0))
            self.tab_frames[tab_id] = frame
            if tab_id == "developer":
                self.dev_tab_index = idx
        self.notebook.grid(row=row, column=0, sticky="nsew", pady=6)

        # File Cleaner Tab (with child notebook)
        file_cleaner_tab = FileCleanerTab(
            self.tab_frames["file_cleaner"],
            self.loc,
            self._on_scan_files,
            getattr(self, "_on_select_all_toggle", lambda items: None),
            self._on_remove_selected,
            self.get_selected_items,
        )
        file_cleaner_tab.frame.pack(fill="both", expand=True)
        self.file_cleaner_tab = file_cleaner_tab

        # Folder Cleaner Tab
        folder_cleaner_tab = FolderCleanerTab(
            self.tab_frames["folder_cleaner"],
            self.loc,
            on_scan_folders=self._on_scan_folders,
            on_select_all_toggle=lambda: folder_cleaner_tab.toggle_select_all(),
            on_remove_selected=self._on_remove_selected_folders,
            get_selected_items=lambda context: [],  # Placeholder (not used for folder cleaner)
            game_versions=self.game_versions,
            settings=self.settings,
        )
        folder_cleaner_tab.frame.pack(fill="both", expand=True)
        self.folder_cleaner_tab = folder_cleaner_tab  # Store reference

        # Game Optimizer Tab
        game_optimizer_tab = GameOptimizerTab(
            self.tab_frames["game_optimizer"], self.loc
        )
        game_optimizer_tab.frame.pack(fill="both", expand=True)

        # Log Tab
        log_tab = LogTab(
            self.tab_frames["log"],
            self.loc,
            log_controls={
                "clear": lambda: clear_user_log(self.log_text, self.logger),
                "copy": lambda: copy_user_log(self.root, self.log_text, self.loc),
                "open_folder": lambda: open_log_folder(),
                "delete": lambda: delete_user_log(self.settings, self.loc),
            },
            append_log_var=self.append_log_var,
            font_size=self.settings.get("font_size", 12),
        )
        log_tab.frame.pack(fill="both", expand=True)
        # Store reference to log text widget for later access
        self.log_text = log_tab.log_text

        # Attach logger to user log text widget
        # CRITICAL FIX: December 28, 2025
        # This attachment must happen AFTER the tab is created and the widget exists
        # The attach_text_widget method now:
        # 1. Loads existing log content directly from disk file
        # 2. Creates the TextWidgetHandler for real-time updates
        # 3. Adds handler to logger for future messages
        # Previous bug: Stub method was shadowing this, preventing attachment
        self.logger.attach_text_widget(self.log_text)

        # Load previous user log if append mode is enabled
        if self.settings.get("append_log", False):
            from core.settings import load_user_log

            previous_log = load_user_log()
            if previous_log:
                # Find the log_text widget in the log tab
                for child in self.tab_frames["log"].winfo_children():
                    if isinstance(child, tk.Text):
                        child.configure(state="normal")
                        child.insert("1.0", previous_log + "\n")
                        child.configure(state="disabled")
                        break

        # Developer Tab
        developer_tab = DeveloperTab(
            self.tab_frames["developer"],
            self.loc,
            log_controls={
                "clear": lambda: clear_dev_log(self.dev_text),
                "copy": lambda: copy_dev_log(self.root, self.logger, self.loc),
                "open_folder": lambda: open_log_folder(),
            },
            font_size=self.settings.get("font_size", 12),
        )
        developer_tab.frame.pack(fill="both", expand=True)
        # Store reference to developer log text widget for later access
        self.dev_text = developer_tab.log_text

        # Attach logger to developer log text widget
        # CRITICAL FIX: December 28, 2025
        # Similar to user log attachment above, this must happen after widget creation
        # The attach_dev_text_widget method:
        # 1. Loads existing dev log content from disk (dev_log.txt)
        # 2. Creates TextWidgetHandler for debug/warning/error messages
        # 3. Configures handler to show all log levels (DEBUG and above)
        self.logger.attach_dev_text_widget(self.dev_text)

    # Log control methods are now imported from ui.log_controls

    # Tab UI creation is now handled by separate tab classes in ui.tabs

    def _update_error_badge(self, count):
        """Update error badge on developer tab.

        Args:
            count: Number of errors
        """
        if count > 0:
            self.dev_badge_label.config(text=f"🔴 {count}")
            # Update tab text to include badge
            self.notebook.tab(
                self.dev_tab_index, text=f"{self.loc._('tab_developer')} 🔴 {count}"
            )
        else:
            self.dev_badge_label.config(text="")
            self.notebook.tab(self.dev_tab_index, text=self.loc._("tab_developer"))

    def refresh_dev_log_colors(self):
        """Refresh developer log color tags when theme changes."""
        # Dev log colors are handled by the logger; no special widget-level configuration needed
        pass

    def _setup_tab_tooltip_handler(self):
        """Set up tooltip display for disabled tabs."""
        self._tooltip_window = None
        self._current_tooltip_tab = None

        def show_tooltip(event):
            """Show tooltip when hovering over a disabled tab."""
            if (
                not hasattr(self, "_tab_tooltip_bindings")
                or not self._tab_tooltip_bindings
            ):
                return

            # Identify which tab is under the cursor
            try:
                elem = self.notebook.identify(event.x, event.y)
                if elem and hasattr(self.notebook, "index"):
                    # elem format: "tab@x,y" or similar - try to extract tab index
                    tab_idx = self.notebook.index(f"@{event.x},{event.y}")

                    # Only show tooltip if tab is in bindings (disabled tabs only)
                    if tab_idx in self._tab_tooltip_bindings:
                        # Don't recreate if already showing for this tab
                        if (
                            self._current_tooltip_tab == tab_idx
                            and self._tooltip_window
                        ):
                            return

                        tooltip_text = self._tab_tooltip_bindings[tab_idx]

                        # Destroy existing tooltip
                        if self._tooltip_window:
                            self._tooltip_window.destroy()

                        # Get current theme colors
                        from core.themes import THEMES

                        current_theme = self.settings.get("theme", "dark")
                        theme_colors = THEMES.get(current_theme, THEMES["dark"])

                        # Create tooltip window
                        self._tooltip_window = tk.Toplevel(self.notebook)
                        self._tooltip_window.wm_overrideredirect(True)
                        self._tooltip_window.wm_geometry(
                            f"+{event.x_root + 10}+{event.y_root + 10}"
                        )

                        # Create label with word wrapping (max width ~300px)
                        self._tooltip_window.configure(
                            bg=theme_colors.get("tooltip_bg", "#ffffe0")
                        )
                        label = tk.Label(
                            self._tooltip_window,
                            text=tooltip_text,
                            background=theme_colors.get("tooltip_bg", "#ffffe0"),
                            foreground=theme_colors.get("tooltip_fg", "#000000"),
                            relief="solid",
                            borderwidth=1,
                            font=("TkDefaultFont", 9),
                            padx=8,
                            pady=5,
                            wraplength=300,
                            justify="left",
                        )
                        label.pack()
                        self._current_tooltip_tab = tab_idx
                    else:
                        # Not hovering over a disabled tab, hide tooltip
                        hide_tooltip(None)
            except Exception:
                pass

        def hide_tooltip(event):
            """Hide tooltip when cursor leaves."""
            if self._tooltip_window:
                self._tooltip_window.destroy()
                self._tooltip_window = None
                self._current_tooltip_tab = None

        # Bind hover events to notebook
        self.notebook.bind("<Motion>", show_tooltip)
        self.notebook.bind("<Leave>", hide_tooltip)

    def set_feature_tabs_enabled(self, enabled):
        """Enable or disable feature tabs based on WoW path validity.

        Args:
            enabled: True to enable tabs, False to disable
        """
        state = "normal" if enabled else "disabled"
        if not hasattr(self, "_tab_tooltip_bindings"):
            self._tab_tooltip_bindings = {}
        for tab_idx in self.feature_tab_indices:
            self.tabbar.tab(tab_idx, state=state)
            if enabled:
                if tab_idx in self._tab_tooltip_bindings:
                    del self._tab_tooltip_bindings[tab_idx]
            else:
                self._tab_tooltip_bindings[tab_idx] = self.loc._("tab_disabled_tooltip")
        if hasattr(self, "_tooltip_window") and self._tooltip_window:
            self._tooltip_window.destroy()
            self._tooltip_window = None
            self._current_tooltip_tab = None
