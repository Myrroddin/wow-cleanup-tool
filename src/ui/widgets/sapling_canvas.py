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
    def __init__(self, master, style, tree_data, expand_all_on_root_click=False,
                 on_select=None, on_expand=None, **kwargs):
        import sys
        super().__init__(master, **kwargs)
        self.style = style.lower() if isinstance(style, str) else 'triangle'
        self.tree_data = tree_data  # Root TreeNode
        self.expand_all_on_root_click = bool(expand_all_on_root_click)
        self.on_select = on_select
        self.on_expand = on_expand
        self.node_positions = {}    # Map node to (x, y, width, height)
        self.selected_nodes = set()
        self.bind('<Button-1>', self._on_click)
        # Debug print for font and canvas width
        font = ('Consolas', 10)  # Switch to monospaced font for clarity
        self.debug_font = font
        print(f"[DEBUG] Canvas width: {self['width']}", file=sys.stderr)
        print(f"[DEBUG] Using font: {font}", file=sys.stderr)
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
        self.delete('all')
        self.node_positions.clear()
        self._draw_node(self.tree_data, 10, 10, 0)

    def _draw_node(self, node, x, y, depth):
        import sys
        # Debug print for tracing indentation and label composition
        # Expander style
        expander_str = ''
        checkbox = '☑' if node.selected else '☐'
        connector = ''
        if self.style == 'box':
            connector = '    ' * depth
            print(f"[DEBUG] Connector for '{node.label}': '{connector}'", file=sys.stderr)
            if node.children:
                expander_str = '[-]' if node.expanded else '[+]'
                print(f"[BOX DEBUG] Connector for '{node.label}': '{connector}'", file=sys.stderr)
            # Ensure files (leaf nodes) are also indented
        elif self.style == 'triangle':
            connector = '    ' * depth
            if node.children:
                expander_str = '▼' if node.expanded else '▶'
        elif self.style == 'simple' and depth > 0:
            connector = '|   ' * (depth-1) + '|-- '
            if node.children:
                expander_str = '-' if node.expanded else '+'
        # Always set label for every node
        if node.children:
            label = f'{connector}{expander_str} {checkbox} {node.label}'
        else:
            label = f'{connector}{checkbox} {node.label}'
        color = 'blue' if node.selected else 'black'
        text_id = self.create_text(x, y, anchor='nw', text=label, fill=color, font=self.debug_font)
        bbox = self.bbox(text_id)
        self.node_positions[text_id] = (node, bbox)
        y += 20
        if node.expanded and node.children:
            for child in node.children:
                y = self._draw_node(child, x, y, depth+1)
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
                expander_area = (bbox[0], bbox[1], bbox[0]+30, bbox[3])
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
            checkbox_area = (bbox[0]+30, bbox[1], bbox[0]+50, bbox[3])
            if checkbox_area[0] <= event.x <= checkbox_area[2]:
                # If group, toggle all children
                if node.is_group:
                    new_state = not node.selected
                    def _set_selected_recursive(n, state):
                        n.selected = state
                        for c in n.children:
                            _set_selected_recursive(c, state)
                    _set_selected_recursive(node, new_state)
                    # Debug print: confirm selected state for all descendants
                    def _print_selected(n, depth=0):
                        import sys
                        print(f"[DEBUG] {'  '*depth}{n.label}: selected={n.selected}", file=sys.stderr)
                        for c in n.children:
                            _print_selected(c, depth+1)
                    _print_selected(node)
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
        import logging
        logger = logging.getLogger("SaplingCanvas")
        logger.debug(f"[DEBUG] build_tree called with scan_results: {scan_results}")
        if not scan_results:
            logger.debug("[DEBUG] No .bak/.old files found in scan_results.")
            return TreeNode('No .bak/.old files found', [])
        root = TreeNode('Game Versions', expanded=True)
        for flavor, files in scan_results.items():
            logger.debug(f"[DEBUG] Adding flavor '{flavor}' with files: {files}")
            flavor_node = TreeNode(flavor, expanded=True)
            for f in files:
                flavor_node.children.append(TreeNode(f))
            root.children.append(flavor_node)
        return root
# Example usage (for testing):
if __name__ == '__main__':
    root = tk.Tk()
    root.title('SaplingCanvas Demo')
    # Build deeply nested sample tree
    tree = TreeNode('Game Versions', [
        TreeNode('Retail', [
            TreeNode('file1.bak'),
            TreeNode('file2.old'),
            TreeNode('Nested', [
                TreeNode('Deeper', [
                    TreeNode('file3.bak'),
                    TreeNode('file4.old'),
                ], expanded=True),
                TreeNode('file5.bak'),
            ], expanded=True),
        ], expanded=True),
        TreeNode('Classic', [
            TreeNode('file6.bak'),
            TreeNode('file7.old'),
        ], expanded=True),
    ], expanded=True)

    # Show all styles in separate windows
    for style in ['triangle', 'box', 'simple']:
        win = tk.Toplevel() if style != 'triangle' else root
        win.title(f'SaplingCanvas Demo - {style.capitalize()} Style')
        # Demo: triangle style with expand_all_on_root_click True, others False
        expand_all = True if style == 'triangle' else False
        canvas = SaplingCanvas(win, style, tree, expand_all_on_root_click=expand_all, width=400, height=300, bg='white')
        canvas.pack(fill='both', expand=True)
    root.mainloop()
