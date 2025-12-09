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
    def __init__(self, master, tree_data, **kwargs):
        super().__init__(master, **kwargs)
        self.tree_data = tree_data  # Root TreeNode
        self.node_positions = {}    # Map node to (x, y, width, height)
        self.selected_nodes = set()
        self.bind('<Button-1>', self._on_click)
        self._redraw()

    def _redraw(self):
        self.delete('all')
        self.node_positions.clear()
        self._draw_node(self.tree_data, 10, 10, 0)

    def _draw_node(self, node, x, y, depth):
        expander = None
        if node.children:
            expander = '[-]' if node.expanded else '[+]'
        # Unicode checkbox
        checkbox = '☑' if node.selected else '☐'
        label = f'{expander} {checkbox} {node.label}' if expander else f'{checkbox} {node.label}'
        color = 'blue' if node.selected else 'black'
        text_id = self.create_text(x + depth*20, y, anchor='nw', text=label, fill=color, font=('TkDefaultFont', 10))
        bbox = self.bbox(text_id)
        self.node_positions[text_id] = (node, bbox)
        y += 20
        if node.expanded:
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
                    node.expanded = not node.expanded
                    self._redraw()
                    return
            # If clicked on checkbox (roughly first 20px after expander)
            checkbox_area = (bbox[0]+30, bbox[1], bbox[0]+50, bbox[3])
            if checkbox_area[0] <= event.x <= checkbox_area[2]:
                # If group, toggle all children
                if node.is_group:
                    new_state = not node.selected
                    node.selected = new_state
                    for child in node.children:
                        child.selected = new_state
                else:
                    node.selected = not node.selected
                self._redraw()
                return
            # If clicked on label, toggle selection
            node.selected = not node.selected
            self._redraw()

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
    # Build sample tree
    tree = TreeNode('Game Versions', [
        TreeNode('Retail', [TreeNode('file1.bak'), TreeNode('file2.old')]),
        TreeNode('Classic', [TreeNode('file3.bak')]),
    ], expanded=True)
    canvas = SaplingCanvas(root, tree, width=400, height=300, bg='white')
    canvas.pack(fill='both', expand=True)
    root.mainloop()
