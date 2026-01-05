"""Folder Cleaner Tab UI for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk

from core.themes import get_theme_colors
from ui.widgets.tooltip import Tooltip
from ui.dialogs.screenshot_viewer import ScreenshotViewer


class FolderCleanerTab:
    def __init__(
        self,
        parent,
        loc,
        on_scan_folders,
        on_select_all_toggle,
        on_remove_screenshots,
        on_remove_selected,
        get_selected_items,
        game_versions,
        settings=None,
        font_size=12,
    ):
        self.frame = ttk.Frame(parent, padding=5)
        self.loc = loc  # Store localization instance for use in other methods
        self.game_versions = game_versions  # List of GameVersion objects
        self.settings = settings  # Store settings for theme/font access
        self.font_size = font_size
        self.on_remove_screenshots = on_remove_screenshots
        self.sub_tabs = None  # Store sub-tabs notebook reference
        self.version_frames = {}  # Store frame for each game version
        self.folder_checkboxes = (
            {}
        )  # Store checkboxes: {game_version: {folder_type: (var, checkbox)}}
        self.cache_tooltips = {}  # Store active cache tooltips by flavor_dir
        self._select_all_tooltip = None  # Tooltip reference for select-all button
        self.screenshot_trees = {}
        self.screenshot_previews = {}
        self.screenshot_images = {}
        self.screenshot_item_paths = {}
        self.screenshot_toggle_buttons = {}
        self.screenshot_remove_buttons = {}
        self.screenshot_cache = (
            {}
        )  # Cache for loaded screenshots: {file_path: PhotoImage}
        self._configure_timer = None  # Debounce timer for configure events
        self._preview_timers = {}  # Debounce timers per flavor for screenshot preview
        self._style_configured = False
        self._create_content(
            loc,
            on_scan_folders,
            on_select_all_toggle,
            on_remove_selected,
            get_selected_items,
        )

    def _create_content(
        self,
        loc,
        on_scan_folders,
        on_select_all_toggle,
        on_remove_selected,
        get_selected_items,
    ):
        """Build the tab UI: description, buttons, and folder scanning interface.

        Layout:
        - Description label (explains what the tab does)
        - Button frame: Scan Folders, Select All, Remove Selected
        - Sub-notebook with tabs for each detected game version
        """
        self.desc_label = ttk.Label(
            self.frame,
            text=loc._("desc_folder_cleaner"),
            justify="left",
        )
        self.desc_label.pack(side="top", fill="x", pady=(0, 10))
        # Bind to configure event with debouncing to reduce flicker
        self.desc_label.bind("<Configure>", self._debounced_update_wraplength)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(side="top", fill="x", pady=(0, 10))

        scan_btn = ttk.Button(
            button_frame, text=loc._("btn_scan_folders"), command=on_scan_folders
        )
        scan_btn.pack(side="left", padx=(0, 10))

        select_all_btn = ttk.Button(
            button_frame,
            text=loc._("btn_select_all_toggle"),
            command=on_select_all_toggle,
        )
        select_all_btn.pack(side="left", padx=(0, 10))
        self._add_select_all_tooltip(select_all_btn)

        remove_btn = ttk.Button(
            button_frame,
            text=loc._("btn_remove_selected"),
            command=lambda: on_remove_selected(get_selected_items("folder_cleaner")),
        )
        remove_btn.pack(side="left")

        # Create sub-notebook with tabs for each game version
        if self.game_versions:
            self.sub_tabs = ttk.Notebook(self.frame)
            for game_version in self.game_versions:
                version_tab = ttk.Frame(self.sub_tabs)
                self.version_frames[game_version.flavor_dir] = version_tab
                self.folder_checkboxes[game_version.flavor_dir] = {}
                self.screenshot_remove_buttons[game_version.flavor_dir] = None
                self.sub_tabs.add(version_tab, text=game_version.display_name)
            self.sub_tabs.pack(side="top", fill="both", expand=True)

    def display_scan_results(self, results, screenshot_files=None):
        """Display scan results with checkboxes for each found folder.

        Args:
            results: Dict mapping flavor_dir to dict of {folder_type: folder_path}
                    Example: {'_retail_': {'errors': 'path/to/Errors', 'cache': 'path/to/Cache'}}
            screenshot_files: Optional dict mapping flavor_dir to list of screenshot file paths
        """
        # Folder display order: errors, logs, screenshots, cache (cache always last)
        folder_order = ["errors", "logs", "screenshots", "cache"]

        screenshot_files = screenshot_files or {}

        # Always clear all frames so stale results are removed between scans
        for flavor_dir, frame in self.version_frames.items():
            for widget in frame.winfo_children():
                widget.destroy()

            self.folder_checkboxes[flavor_dir] = {}
            self.screenshot_trees[flavor_dir] = None
            self.screenshot_previews[flavor_dir] = None
            self.screenshot_images[flavor_dir] = None
            self.screenshot_item_paths[flavor_dir] = {}

        # Clear screenshot cache to free memory
        self.screenshot_cache.clear()
        self.screenshot_toggle_buttons = {}
        self.screenshot_remove_buttons = {}

        for flavor_dir, folders in results.items():
            if flavor_dir not in self.version_frames:
                continue

            frame = self.version_frames[flavor_dir]

            # Create horizontal container for checkboxes
            checkbox_frame = ttk.Frame(frame)
            checkbox_frame.pack(side="top", anchor="w", pady=5)

            has_screenshots = "screenshots" in folders

            # Display folders horizontally in specified order
            for folder_type in folder_order:
                if folder_type not in folders:
                    continue

                folder_path = folders[folder_type]

                # Create checkbox for this folder
                var = tk.BooleanVar(value=False)  # Default unselected
                folder_display_name = self.loc._(f"folder_{folder_type}")

                cb = ttk.Checkbutton(
                    checkbox_frame, text=folder_display_name, variable=var
                )
                cb.pack(side="left", padx=(0, 15))

                # Add tooltip for cache folder warning
                if folder_type == "cache" and self.settings:
                    self._add_cache_tooltip(cb, flavor_dir)

                # Store reference
                self.folder_checkboxes[flavor_dir][folder_type] = (var, cb, folder_path)

            screenshot_toggle_btn = None
            remove_shots_btn = None
            if has_screenshots:
                screenshot_toggle_btn = ttk.Button(
                    checkbox_frame,
                    text=self.loc._("btn_select_all_screenshots"),
                    command=lambda fd=flavor_dir: self._toggle_screenshot_selection(fd),
                )
                screenshot_toggle_btn.pack(side="left", padx=(0, 15))

                remove_shots_btn = ttk.Button(
                    checkbox_frame,
                    text=self.loc._("btn_remove_selected_screenshots"),
                    command=lambda fd=flavor_dir: self._on_remove_screenshots_click(fd),
                )
                remove_shots_btn.pack(side="left", padx=(0, 15))

            self.screenshot_toggle_buttons[flavor_dir] = screenshot_toggle_btn
            self.screenshot_remove_buttons[flavor_dir] = remove_shots_btn

            # Build screenshots tree/preview when the folder exists
            if has_screenshots:
                files = screenshot_files.get(flavor_dir, [])
                self._build_screenshot_view(
                    flavor_dir, frame, folders["screenshots"], files
                )
                self._update_screenshot_toggle_label(flavor_dir)

    def _add_cache_tooltip(self, widget, flavor_dir):
        """Add theme-aware tooltip to cache checkbox."""

        def show_tooltip(event):
            theme_name = self.settings.get("theme", "system")
            theme = get_theme_colors(theme_name)

            tooltip = Tooltip(
                widget,
                self.loc._("tooltip_cache_warning"),
                theme,
                wraplength=320,
            )
            tooltip.show()
            self.cache_tooltips[flavor_dir] = tooltip

        def hide_tooltip(event):
            if flavor_dir in self.cache_tooltips:
                self.cache_tooltips[flavor_dir].hide()
                del self.cache_tooltips[flavor_dir]

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def _add_select_all_tooltip(self, widget):
        """Add theme-aware tooltip to select-all button (folder cleaner only)."""
        if not self.settings:
            return

        def show_tooltip(event):
            theme_name = self.settings.get("theme", "system")
            theme = get_theme_colors(theme_name)

            tooltip = Tooltip(
                widget,
                self.loc._("tooltip_select_all_cache_manual"),
                theme,
                wraplength=320,
            )
            tooltip.show()
            self._select_all_tooltip = tooltip

        def hide_tooltip(event):
            if self._select_all_tooltip:
                self._select_all_tooltip.hide()
                self._select_all_tooltip = None

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def _update_wraplength(self, event=None):
        """Update wraplength based on actual widget width."""
        if hasattr(self, "desc_label"):
            # Get actual widget width, subtract padding for margins
            width = self.desc_label.winfo_width()
            if width > 1:  # Ensure widget is actually rendered
                self.desc_label.configure(wraplength=max(width - 20, 100))

    def _debounced_update_wraplength(self, event=None):
        """Debounce wraplength updates to reduce flicker during resize."""
        # Cancel existing timer if any
        if self._configure_timer:
            self.frame.after_cancel(self._configure_timer)
        # Schedule update after 50ms of no resize events
        self._configure_timer = self.frame.after(50, self._update_wraplength)

    def refresh_wraplength(self, font_size):
        """Update description label wraplength when font size changes."""
        self.font_size = font_size
        # Trigger a wraplength update based on current width
        self._update_wraplength()

    def toggle_select_all(self):
        """Toggle selection of all folders except cache (which must be manual).

        Determine if any non-cache folder is unchecked; if so, select them all.
        Otherwise, unselect all non-cache folders. Cache stays untouched.
        """

        any_unselected = False

        for flavor_dir, folders_dict in self.folder_checkboxes.items():
            for folder_type, (var, _, _) in folders_dict.items():
                if folder_type != "cache" and not var.get():
                    any_unselected = True
                    break
            if any_unselected:
                break

        # Set all non-cache folders to the new state
        new_state = any_unselected
        for flavor_dir, folders_dict in self.folder_checkboxes.items():
            for folder_type, (var, _, _) in folders_dict.items():
                if folder_type != "cache":
                    var.set(new_state)

    def _collect_tree_items(self, tree):
        """Recursively collect item IDs from a treeview."""
        if not tree:
            return []

        items = []

        def walk(node=""):
            for child in tree.get_children(node):
                items.append(child)
                walk(child)

        walk()
        return items

    def _update_screenshot_toggle_label(self, flavor_dir):
        """Update screenshot toggle text and disabled state based on selection."""
        button = self.screenshot_toggle_buttons.get(flavor_dir)
        tree = self.screenshot_trees.get(flavor_dir)

        if not button or not tree or not getattr(button, "state", None):
            return

        item_ids = self._collect_tree_items(tree)

        if not item_ids:
            button.state(["disabled"])
            button.configure(text=self.loc._("btn_select_all_screenshots"))
            return

        button.state(["!disabled"])

        selected_ids = set(tree.selection())
        all_selected = all(iid in selected_ids for iid in item_ids)

        new_text = (
            "btn_unselect_all_screenshots"
            if all_selected
            else "btn_select_all_screenshots"
        )
        button.configure(text=self.loc._(new_text))

    def _get_selected_screenshots(self, flavor_dir):
        tree = self.screenshot_trees.get(flavor_dir)
        if not tree:
            return []

        selected = []
        for iid in tree.selection():
            path = self.screenshot_item_paths.get(flavor_dir, {}).get(iid)
            if path:
                selected.append(path)
        return list(dict.fromkeys(selected))

    def _on_remove_screenshots_click(self, flavor_dir):
        """Invoke removal callback with selected screenshots for a flavor."""
        if not self.on_remove_screenshots:
            return

        folder_entry = self.folder_checkboxes.get(flavor_dir, {}).get("screenshots")
        folder_path = folder_entry[2] if folder_entry else None
        selected_files = self._get_selected_screenshots(flavor_dir)

        self.on_remove_screenshots(flavor_dir, folder_path, selected_files)

    def _toggle_screenshot_selection(self, flavor_dir):
        """Toggle select all/unselect all screenshots for a given flavor."""
        tree = self.screenshot_trees.get(flavor_dir)
        if not tree:
            return

        item_ids = self._collect_tree_items(tree)
        if not item_ids:
            self._update_screenshot_toggle_label(flavor_dir)
            return

        selected_ids = set(tree.selection())
        all_selected = all(iid in selected_ids for iid in item_ids)

        if all_selected:
            for iid in item_ids:
                tree.selection_remove(iid)
        else:
            for iid in item_ids:
                tree.selection_add(iid)

        # Keep preview and button text in sync with selection
        self._on_screenshot_selected(flavor_dir)
        self._update_screenshot_toggle_label(flavor_dir)

    def get_selected_folders(self):
        """Get list of selected folder paths (excludes unselected folders).

        Returns:
            List of folder paths that are selected, across all game versions
        """
        selected_folders = []
        for flavor_dir, folders_dict in self.folder_checkboxes.items():
            for folder_type, (var, _, folder_path) in folders_dict.items():
                if var.get():  # Only include if checked
                    selected_folders.append(folder_path)
        return selected_folders

    def _build_screenshot_view(self, flavor_dir, parent_frame, screenshots_path, files):
        """Create the screenshot tree and preview panel for a game version."""
        if not self._style_configured:
            style = ttk.Style()
            style.configure("Fixed.Treeview", font=("TkFixedFont", 10))
            style.configure("Fixed.Treeview.Heading", font=("TkFixedFont", 10, "bold"))
            self._style_configured = True

        container = ttk.Frame(parent_frame)
        container.pack(fill="both", expand=True, pady=(10, 0))

        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=0)
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=1)

        # Tree frame with scrollbars
        tree_frame = ttk.Frame(container)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        tree = ttk.Treeview(
            tree_frame,
            columns=(),
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode="extended",
        )

        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)

        tree.heading("#0", text=self.loc._("tree_header_file_path"), anchor="w")
        tree.column("#0", width=500, stretch=True)

        tree.configure(style="Fixed.Treeview")

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Populate tree with screenshot files (relative names for readability)
        self.screenshot_item_paths[flavor_dir] = {}
        for idx, file_path in enumerate(files):
            rel_name = self._relative_path_for_display(file_path, screenshots_path)
            item_id = f"shot_{idx}"
            tree.insert("", "end", iid=item_id, text=rel_name)
            self.screenshot_item_paths[flavor_dir][item_id] = file_path

        tree.bind(
            "<<TreeviewSelect>>",
            lambda event, fd=flavor_dir: self._on_screenshot_selected(fd),
        )

        # Create right panel frame for instructions and preview
        right_panel = ttk.Frame(container)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Add instruction label at the top with dynamic wraplength
        instruction_label = ttk.Label(
            right_panel,
            text=self.loc._("desc_screenshot_interaction"),
            justify="left",
        )
        instruction_label.pack(side="top", fill="x", pady=(0, 10))
        # Bind to update wraplength based on panel width with debouncing
        instruction_label.bind(
            "<Configure>",
            lambda e, lbl=instruction_label: self._update_instruction_wraplength(
                e, lbl
            ),
        )

        # Preview canvas starts at 200x200, resizes dynamically per image aspect ratio
        # Wrapped in a frame to allow centering within the available space
        preview_frame = ttk.Frame(right_panel)
        preview_frame.pack(side="top", fill="both", expand=True)

        preview_canvas = tk.Canvas(
            preview_frame,
            width=200,
            height=200,
            highlightthickness=1,
            highlightbackground="#ccc",
        )
        # Center the canvas horizontally using pack with side="top" anchor
        preview_canvas.pack(anchor="n", pady=(0, 0))

        # Bind click to open screenshot viewer
        preview_canvas.bind(
            "<Button-1>",
            lambda event, fd=flavor_dir: self._on_preview_click(fd),
        )

        self.screenshot_trees[flavor_dir] = tree
        self.screenshot_previews[flavor_dir] = preview_canvas
        self.screenshot_images[flavor_dir] = None

    def _relative_path_for_display(self, file_path, root_path):
        """Return a display-friendly path relative to the screenshots root."""
        import os

        try:
            return os.path.relpath(file_path, root_path)
        except Exception:
            return os.path.basename(file_path)

    def _update_instruction_wraplength(self, event, label):
        """Update instruction label wraplength based on panel width."""
        if event.width > 1:
            label.configure(wraplength=max(event.width - 20, 100))

    def _on_screenshot_selected(self, flavor_dir):
        tree = self.screenshot_trees.get(flavor_dir)
        if not tree:
            return

        selection = tree.selection()
        if not selection:
            self._clear_preview(flavor_dir)
            self._update_screenshot_toggle_label(flavor_dir)
            return

        item_id = selection[0]
        file_path = self.screenshot_item_paths.get(flavor_dir, {}).get(item_id)
        if file_path:
            if flavor_dir in self._preview_timers:
                self.frame.after_cancel(self._preview_timers[flavor_dir])

            def render():
                self._show_screenshot(flavor_dir, file_path)

            self._preview_timers[flavor_dir] = self.frame.after(50, render)

        self._update_screenshot_toggle_label(flavor_dir)

    def _clear_preview(self, flavor_dir):
        canvas = self.screenshot_previews.get(flavor_dir)
        if not canvas:
            return
        canvas.delete("all")
        self.screenshot_images[flavor_dir] = None

    def _on_preview_click(self, flavor_dir):
        """Handle click on preview canvas to open screenshot viewer."""
        # Get the currently selected screenshot path
        tree = self.screenshot_trees.get(flavor_dir)
        if not tree:
            return

        selection = tree.selection()
        if not selection:
            return

        item_id = selection[0]
        file_path = self.screenshot_item_paths.get(flavor_dir, {}).get(item_id)
        if not file_path:
            return

        # Get theme and settings
        theme_name = self.settings.get("theme", "system") if self.settings else "system"

        # Show screenshot viewer dialog
        viewer = ScreenshotViewer(
            self.frame, self.loc, theme_name, self.settings, file_path
        )
        viewer.show()

    def _show_screenshot(self, flavor_dir, file_path):
        """Render the selected screenshot, scaling canvas height to match aspect ratio."""
        canvas = self.screenshot_previews.get(flavor_dir)
        if not canvas:
            return

        try:
            from PIL import Image, ImageTk
        except Exception:
            self._clear_preview(flavor_dir)
            return

        # Check cache first for performance
        if file_path in self.screenshot_cache:
            photo = self.screenshot_cache[file_path]
            # Cached image already has correct dimensions
            new_width = photo.width()
            new_height = photo.height()
        else:
            try:
                img = Image.open(file_path)
            except Exception:
                self._clear_preview(flavor_dir)
                return

            # Calculate thumbnail size (preserves aspect ratio)
            original_width, original_height = img.size
            max_width = 200
            aspect_ratio = original_height / original_width
            new_width = min(original_width, max_width)
            new_height = int(new_width * aspect_ratio)

            # Use thumbnail() instead of resize() - more efficient, modifies in-place
            img.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            # Cache the resized image
            self.screenshot_cache[file_path] = photo

        # Resize canvas to match scaled image
        canvas.config(width=new_width, height=new_height)
        canvas.delete("all")
        canvas.create_image(new_width // 2, new_height // 2, image=photo)
        self.screenshot_images[flavor_dir] = photo
