"""
UI refresh and rebuild module for WoW Cleanup Tool.

Handles theme-aware widget refreshing, asset rebuilding, and UI state synchronization.
Centralizes all logic for updating UI elements after theme or asset changes.
"""

def refresh_styled_checkables(app):
    """Refresh all styled checkbox and radio widgets after theme or asset changes.
    
    This updates ImgCheckbox and ImgRadio widgets to use new theme assets.
    
    Args:
        app: The WoWCleanupTool instance
    """
    if hasattr(app, "rb_delete"):
        app.rb_delete.assets = app.assets; app.rb_delete._sync_image()
    if hasattr(app, "rb_trash"):
        app.rb_trash.assets = app.assets; app.rb_trash._sync_image()
    if hasattr(app, "styled_folder_boxes"):
        for cb in app.styled_folder_boxes:
            cb.assets = app.assets; cb._sync_image()
    if hasattr(app, "styled_shot_boxes"):
        for cb in app.styled_shot_boxes:
            cb.assets = app.assets; cb._sync_image()
    if hasattr(app, "_build_checkbox_images"):
        app._build_checkbox_images()
        if hasattr(app, "file_tree"):
            for iid in list(getattr(app, "tree_checks", {}).keys()):
                app._tree_set_icon(iid)
        if hasattr(app, "orphan_tree"):
            for iid in list(getattr(app, "orphan_checks", {}).keys()):
                app._orphan_tree_set_icon(iid)

def reload_all_custom_checkboxes(app):
    """Replace checkbox images in all treeviews after theme change.
    
    Args:
        app: The WoWCleanupTool instance
    """
    # File Cleaner
    if hasattr(app, "tree_checks") and hasattr(app, "file_tree"):
        for iid, var in app.tree_checks.items():
            img = app.chk_checked if var.get() else app.chk_unchecked
            app.file_tree.item(iid, image=img)

    # Orphan Cleaner
    if hasattr(app, "orphan_checks") and hasattr(app, "orphan_tree"):
        for iid, var in app.orphan_checks.items():
            img = app.chk_checked if var.get() else app.chk_unchecked
            app.orphan_tree.item(iid, image=img)

    # Folder cleaner uses per-version custom widgets, no TreeView

def rebuild_assets(app):
    """Rebuild image assets based on current theme and platform.
    
    Args:
        app: The WoWCleanupTool instance
    """
    import platform
    from Modules.ui_helpers import ImgAssets
    osname = platform.system()
    dark = (app.theme_var.get() == "dark")
    app.assets = ImgAssets(osname=osname, dark=dark)

def set_options_border(app, show_dark_border: bool):
    """Update the Options frame border color based on theme.
    
    Args:
        app: The WoWCleanupTool instance
        show_dark_border: True for dark theme, False for light
    """
    if hasattr(app, "options_border"):
        try:
            app.options_border.configure(bg="#b0b0b0" if show_dark_border else app.root.cget("bg"))
        except Exception:
            pass
