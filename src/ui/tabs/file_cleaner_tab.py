"""File Cleaner Tab UI for WoW Cleanup Tool.

Provides UI for scanning and removing backup/old files and orphaned
AddOn SavedVariables. Supports multi-select, batch deletion, and
hierarchical display of results grouped by WoW version.

Key Features:
- Dual tabs: one for .bak/.old backup files, one for orphaned SavedVariables
- Background scanning (handled by main window via FileCleaner and OrphanScanner)
- Multi-select with "Select All/Unselect All" toggle across both trees
- File size display with human-readable formatting
- Hierarchical view: versions as collapsible parent nodes, files as children
- Delete integration: Remove Selected button triggers main window deletion handler

Threading Model:
- UI runs on main thread (Tkinter requirement)
- Scan operations run in background (see main_window.py _on_scan_files)
- Tree population happens on main thread via callbacks
- File deletion runs in background (see main_window.py _on_remove_selected)
"""

import os
import tkinter as tk
from tkinter import ttk


class FileCleanerTab:
    """UI component for scanning and managing backup/orphaned files.

    This tab provides two parallel treeview displays:
    1. Backup/Old Files: .bak and .old files found during scanning
    2. Orphaned AddOns: SavedVariables from uninstalled AddOns

    The tab is part of the main notebook and receives scan results via
    populate_backup_tree() and populate_orphan_tree() methods.
    """

    def __init__(
        self,
        parent,
        loc,
        on_scan_files,
        on_select_all_toggle,
        on_remove_selected,
        get_selected_items,
    ):
        self.frame = ttk.Frame(parent, padding=5)
        self.backup_tree = None
        self.orphan_tree = None
        self.loc = loc  # Store localization instance for use in other methods
        self._create_content(
            loc,
            on_scan_files,
            on_select_all_toggle,
            on_remove_selected,
            get_selected_items,
        )

    def _create_content(
        self,
        loc,
        on_scan_files,
        on_select_all_toggle,
        on_remove_selected,
        get_selected_items,
    ):
        """Build the tab UI: description, buttons, and dual treeviews.

        Layout:
        - Description label (explains what the tab does)
        - Button frame: Scan, Select All, Remove Selected
        - Sub-notebook with two tabs:
          * Backup & Old Files
          * Orphaned AddOn Settings
        """
        desc_label = ttk.Label(
            self.frame, text=loc._("desc_file_cleaner"), justify="left"
        )
        desc_label.pack(side="top", fill="x", pady=(0, 10))
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(side="top", fill="x", pady=(0, 10))
        scan_btn = ttk.Button(
            button_frame, text=loc._("btn_scan_files"), command=on_scan_files
        )
        scan_btn.pack(side="left", padx=(0, 10))
        select_all_btn = ttk.Button(
            button_frame,
            text=loc._("btn_select_all_toggle"),
            command=self.toggle_select_all,
        )
        select_all_btn.pack(side="left", padx=(0, 10))
        remove_btn = ttk.Button(
            button_frame,
            text=loc._("btn_remove_selected"),
            command=lambda: on_remove_selected(get_selected_items("file_cleaner")),
        )
        remove_btn.pack(side="left")

        sub_tabs = ttk.Notebook(self.frame)
        backup_tab = ttk.Frame(sub_tabs)
        orphan_tab = ttk.Frame(sub_tabs)
        sub_tabs.add(backup_tab, text=loc._("tab_backup_old_cleaner"))
        sub_tabs.add(orphan_tab, text=loc._("tab_orphaned_addons"))
        sub_tabs.pack(side="top", fill="both", expand=True)

        self.backup_tree = self._create_treeview(backup_tab, loc)

        self.orphan_tree = self._create_treeview(orphan_tab, loc)

    def _create_treeview(self, parent, loc):
        """Create a collapsible treeview for displaying scan results.

        Shows hierarchical file results grouped by WoW version,
        with file sizes and scrollable view.

        Structure:
        - Parent nodes: WoW version (e.g., "Retail (12 files)")
        - Children: Individual file paths with their sizes
        - Styling: Versions collapsed by default; users can expand as needed

        Args:
            parent: Parent frame to contain the tree
            loc: Localization instance for translating header text

        Returns:
            Configured Treeview widget
        """
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        tree = ttk.Treeview(
            tree_frame,
            columns=("size",),
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode="extended",
        )

        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)

        tree.heading("#0", text=loc._("tree_header_file_path"), anchor="w")
        tree.heading("size", text=loc._("tree_header_size"), anchor="e")
        tree.column("#0", width=400, stretch=True)
        tree.column("size", width=150, minwidth=100, stretch=True, anchor="e")

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        return tree

    def _collect_tree_items(self, tree):
        """Recursively collect all item IDs from tree (including nested children).

        Used by toggle_select_all to get all selectable items across both trees.
        Walks the tree depth-first to gather all node IDs.
        """
        if not tree:
            return []

        items = []

        def walk(node=""):
            for child in tree.get_children(node):
                items.append(child)
                walk(child)

        walk()
        return items

    def toggle_select_all(self):
        """Toggle selection state across both treeviews.

        Logic: If all items are selected, unselect all. Otherwise, select all.
        This provides a convenient "Select All / Unselect All" toggle button.

        Note: Works across both backup and orphan trees simultaneously,
        maintaining selection state independently for each.
        """
        trees = [self.backup_tree, self.orphan_tree]

        all_ids = []
        selected_ids = set()

        for tree in trees:
            if not tree:
                continue
            tree_ids = self._collect_tree_items(tree)
            all_ids.extend((tree, iid) for iid in tree_ids)
            selected_ids.update(tree.selection())

        if not all_ids:
            return

        all_selected = all(iid in selected_ids for _, iid in all_ids)

        if all_selected:
            for tree, iid in all_ids:
                tree.selection_remove(iid)
        else:
            for tree, iid in all_ids:
                tree.selection_add(iid)

    def _populate_tree(self, tree, results):
        """Populate treeview with scan results.

        Consolidated helper used by both populate_backup_tree and
        populate_orphan_tree to avoid code duplication.

        Result format:
        - Input: Dict[version_label] -> List[file_path] or List[(file_path, size_str)]
        - Output: Hierarchical tree with versions as parents, files as children

        Size handling:
        - If results include precomputed size tuples, use them directly
        - Otherwise, compute size on-the-fly (may be slow for large result sets)
        - Missing sizes display as "Unknown"

        Args:
            tree: Treeview widget to populate
            results: Dict mapping version_label -> list of file paths/tuples
        """
        if not tree:
            return

        tree.delete(*tree.get_children())

        if not results:
            return

        for version_label, files in sorted(results.items()):
            if not files:
                continue

            version_node = tree.insert(
                "",
                "end",
                text=f"{version_label} ({len(files)} {self.loc._('tree_files_count')})",
                open=False,
            )

            for file_entry in sorted(files):
                if isinstance(file_entry, (tuple, list)) and len(file_entry) >= 2:
                    file_path, size_str = file_entry[0], file_entry[1]
                else:
                    file_path = file_entry
                    try:
                        size = os.path.getsize(file_path)
                        size_str = self._format_size(size)
                    except Exception:
                        size_str = self.loc._("unknown")

                tree.insert(version_node, "end", text=file_path, values=(size_str,))

    def populate_backup_tree(self, results):
        """Populate backup/old files tree with scan results.

        Called from main_window.py after FileCleaner completes scanning.
        Displays .bak and .old files found during the scan.

        Args:
            results: Dict mapping version_label -> list of file paths
        """
        self._populate_tree(self.backup_tree, results)

    def populate_orphan_tree(self, results):
        """Populate orphaned AddOns tree with scan results.

        Called from main_window.py after OrphanScanner completes scanning.
        Displays SavedVariables from uninstalled AddOns.

        Args:
            results: Dict mapping version_label -> list of file paths
        """
        self._populate_tree(self.orphan_tree, results)

    def _format_size(self, size_bytes):
        """Format file size in human-readable format.

        Converts bytes to the largest sensible unit (B, KB, MB, GB, TB)
        for display in the size column.

        Args:
            size_bytes: File size in bytes

        Returns:
            Formatted string (e.g., "1.5 KB", "2.3 MB")
        """
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
