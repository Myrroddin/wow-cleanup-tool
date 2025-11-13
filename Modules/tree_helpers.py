import os


def build_checkbox_images(app):
    """Populate `app.chk_unchecked` and `app.chk_checked` using app.assets."""
    try:
        app.chk_unchecked = app.assets.checkbox(False)
        app.chk_checked = app.assets.checkbox(True)
    except Exception:
        app.chk_unchecked = None
        app.chk_checked = None

def file_tree_add_parent(app, label):
    pid = app.file_tree.insert("", "end", text=f"  {label}", open=False)
    app.tree_checks[pid] = False
    file_tree_set_icon(app, pid)
    return pid

def file_tree_add_child_file(app, parent_id, path):
    basename = os.path.basename(path)
    iid = app.file_tree.insert(parent_id, "end", text=f"  {basename}", open=False)
    app.tree_checks[iid] = False
    app.tree_paths[iid] = path
    file_tree_set_icon(app, iid)
    return iid

def file_tree_set_icon(app, iid):
    if getattr(app, "chk_unchecked", None):
        img = app.chk_checked if app.tree_checks.get(iid, False) else app.chk_unchecked
        try:
            app.file_tree.item(iid, image=img)
        except Exception:
            pass
    else:
        checked = app.tree_checks.get(iid, False)
        try:
            text = app.file_tree.item(iid, "text")
        except Exception:
            text = ""
        prefix = "[x]" if checked else "[ ]"
        try:
            if not text.strip().startswith("["):
                app.file_tree.item(iid, text=f"{prefix} {text.strip()}")
            else:
                app.file_tree.item(iid, text=f"{prefix} {text.strip()[3:].strip()}")
        except Exception:
            pass

def on_file_tree_click(app, event):
    elem = app.file_tree.identify("element", event.x, event.y)
    if elem in ("Treeitem.indicator", "treeitem.indicator", "indicator"):
        return
    iid = app.file_tree.identify_row(event.y)
    if not iid:
        return
    # toggling selection
    if iid not in getattr(app, "tree_paths", {}):
        new_state = not app.tree_checks.get(iid, False)
        app.tree_checks[iid] = new_state
        for child in app.file_tree.get_children(iid):
            app.tree_checks[child] = new_state
            file_tree_set_icon(app, child)
        file_tree_set_icon(app, iid)
    else:
        app.tree_checks[iid] = not app.tree_checks.get(iid, False)
        file_tree_set_icon(app, iid)
    return "break"

def tree_toggle_all(app):
    new_state = app.tree_select_all_var.get()
    for iid in app.file_tree.get_children(""):
        app.tree_checks[iid] = new_state
        file_tree_set_icon(app, iid)
        for child in app.file_tree.get_children(iid):
            app.tree_checks[child] = new_state
            file_tree_set_icon(app, child)

def tree_expand_all(app):
    for iid in app.file_tree.get_children(""):
        app.file_tree.item(iid, open=True)

def tree_collapse_all(app):
    for iid in app.file_tree.get_children(""):
        app.file_tree.item(iid, open=False)

def orphan_tree_add_parent(app, label):
    pid = app.orphan_tree.insert("", "end", text=f"  {label}", open=False)
    app.orphan_checks[pid] = False
    orphan_tree_set_icon(app, pid)
    return pid

def orphan_tree_add_child_file(app, parent_id, path):
    basename = os.path.basename(path)
    iid = app.orphan_tree.insert(parent_id, "end", text=f"  {basename}", open=False)
    app.orphan_checks[iid] = False
    app.orphan_paths[iid] = path
    orphan_tree_set_icon(app, iid)
    return iid

def orphan_tree_set_icon(app, iid):
    if getattr(app, "chk_unchecked", None):
        img = app.chk_checked if app.orphan_checks.get(iid, False) else app.chk_unchecked
        try:
            app.orphan_tree.item(iid, image=img)
        except Exception:
            pass
    else:
        checked = app.orphan_checks.get(iid, False)
        try:
            text = app.orphan_tree.item(iid, "text")
        except Exception:
            text = ""
        prefix = "[x]" if checked else "[ ]"
        try:
            if not text.strip().startswith("["):
                app.orphan_tree.item(iid, text=f"{prefix} {text.strip()}")
            else:
                app.orphan_tree.item(iid, text=f"{prefix} {text.strip()[3:].strip()}")
        except Exception:
            pass

def on_orphan_tree_click(app, event):
    elem = app.orphan_tree.identify("element", event.x, event.y)
    if elem in ("Treeitem.indicator", "treeitem.indicator", "indicator"):
        return
    iid = app.orphan_tree.identify_row(event.y)
    if not iid:
        return
    if iid not in getattr(app, "orphan_paths", {}):
        new_state = not app.orphan_checks.get(iid, False)
        app.orphan_checks[iid] = new_state
        for child in app.orphan_tree.get_children(iid):
            app.orphan_checks[child] = new_state
            orphan_tree_set_icon(app, child)
        orphan_tree_set_icon(app, iid)
    else:
        app.orphan_checks[iid] = not app.orphan_checks.get(iid, False)
        orphan_tree_set_icon(app, iid)
    return "break"

def orphan_tree_toggle_all(app):
    new_state = app.orphan_select_all_var.get()
    for iid in app.orphan_tree.get_children(""):
        app.orphan_checks[iid] = new_state
        orphan_tree_set_icon(app, iid)
        for child in app.orphan_tree.get_children(iid):
            app.orphan_checks[child] = new_state
            orphan_tree_set_icon(app, child)

def orphan_tree_expand_all(app):
    if hasattr(app, "orphan_tree"):
        for iid in app.orphan_tree.get_children(""):
            app.orphan_tree.item(iid, open=True)

def orphan_tree_collapse_all(app):
    if hasattr(app, "orphan_tree"):
        for iid in app.orphan_tree.get_children(""):
            app.orphan_tree.item(iid, open=False)
