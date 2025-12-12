"""
SaplingCanvas: Custom tree widget using tk.Canvas for full control over expanders, selection, and layout.
"""

import tkinter as tk


class TreeNode:
    def __init__(self, label, children=None, expanded=False):
        self.label = label
        self.children = children if children else []
        self.expanded = expanded
        self.selected = False
        self.is_group = bool(children)


class SaplingCanvas(tk.Canvas):
    def __init__(
        self,
        master,
        tree_data,
        expand_all_on_root_click=False,
        on_select=None,
        on_expand=None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.tree_data = tree_data  # Root TreeNode
        self.expand_all_on_root_click = bool(expand_all_on_root_click)
        self.on_select = on_select
        self.on_expand = on_expand
        self.node_positions = {}  # Map node to (x, y, width, height)
        self.selected_nodes = set()
        self.debug_font = ("Consolas", 10)
        self.bind("<Button-1>", self._on_click)
        self._redraw()

    def expand_node(self, node):
        node.expanded = True
        self._redraw()
        if self.on_expand:
            self.on_expand(node)

    def collapse_node(self, node):
        node.expanded = False
        self._redraw()
        if self.on_expand:
            self.on_expand(node)

    def get_selected_nodes(self):
        selected = []

        def _collect(node):
            if node.selected:
                selected.append(node)
            for child in node.children:
                _collect(child)

        _collect(self.tree_data)
        return selected

    def _redraw(self):
        self.delete("all")
        self.node_positions.clear()
        self._draw_node(self.tree_data, 10, 10, 0)

    def _draw_node(self, node, x, y, depth):
        # Only triangle style
        expander_str = ""
        checkbox = "☑" if node.selected else "☐"
        connector = "    " * depth
        if node.children:
            expander_str = "▼" if node.expanded else "▶"
            label = f"{connector}{expander_str} {checkbox} {node.label}"
        else:
            label = f"{connector}{checkbox} {node.label}"
        color = "blue" if node.selected else "black"
        text_id = self.create_text(
            x, y, anchor="nw", text=label, fill=color, font=self.debug_font
        )
        bbox = self.bbox(text_id)
        self.node_positions[text_id] = (node, bbox)
        y += 20
        if node.expanded and node.children:
            for child in node.children:
                y = self._draw_node(child, x, y, depth + 1)
        return y

    def _on_click(self, event):
        clicked = None
        clicked_bbox = None
        for text_id, (node, bbox) in self.node_positions.items():
            if bbox and bbox[0] <= event.x <= bbox[2] and bbox[1] <= event.y <= bbox[3]:
                clicked = (node, text_id)
                clicked_bbox = bbox
                break
        if clicked and clicked_bbox:
            node, text_id = clicked
            bbox = clicked_bbox
            # If clicked on expander
            if node.children:
                expander_area = (bbox[0], bbox[1], bbox[0] + 30, bbox[3])
                if expander_area[0] <= event.x <= expander_area[2]:
                    # If root node and expand_all_on_root_click is True
                    if node is self.tree_data and self.expand_all_on_root_click:
                        new_state = not node.expanded
                        node.expanded = new_state
                        for child in node.children:
                            self._set_expanded_recursive(child, new_state)
                        if self.on_expand:
                            self.on_expand(node)
                    else:
                        node.expanded = not node.expanded
                        if self.on_expand:
                            self.on_expand(node)
                    self._redraw()
                    return
            # If clicked on checkbox (roughly first 20px after expander)
            checkbox_area = (bbox[0] + 30, bbox[1], bbox[0] + 50, bbox[3])
            if checkbox_area[0] <= event.x <= checkbox_area[2]:
                # If group, toggle all children
                if node.is_group:
                    new_state = not node.selected

                    def _set_selected_recursive(n, state):
                        n.selected = state
                        for c in n.children:
                            _set_selected_recursive(c, state)

                    _set_selected_recursive(node, new_state)
                else:
                    node.selected = not node.selected
                self._redraw()
                if self.on_select:
                    self.on_select(node)
                return
            # If clicked on label, toggle selection
            node.selected = not node.selected
            self._redraw()
            if self.on_select:
                self.on_select(node)

    def _set_expanded_recursive(self, node, expanded):
        node.expanded = expanded
        for child in node.children:
            self._set_expanded_recursive(child, expanded)

    def select_all(self):
        def _select_recursive(node):
            node.selected = True
            for child in node.children:
                _select_recursive(child)

        _select_recursive(self.tree_data)
        self._redraw()

    def unselect_all(self):
        def _unselect_recursive(node):
            node.selected = False
            for child in node.children:
                _unselect_recursive(child)

        _unselect_recursive(self.tree_data)
        self._redraw()

    def build_tree(self, scan_results):
        if not scan_results:
            return TreeNode("No .bak/.old files found", [])
        root = TreeNode("Game Versions", expanded=True)
        for flavor, files in scan_results.items():
            flavor_node = TreeNode(flavor, expanded=True)
            for f in files:
                flavor_node.children.append(TreeNode(f))
            root.children.append(flavor_node)
        return root
