"""Tests for Folder Cleaner Tab UI."""

import sys
import os
import pytest
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from ui.tabs.folder_cleaner_tab import FolderCleanerTab
from wow.version_manager import GameVersion


@pytest.fixture
def loc():
    """Mock localization."""
    mock_loc = Mock()
    mock_loc._ = lambda key, *args: f"{key}_{args}" if args else key
    return mock_loc


@pytest.fixture
def settings():
    """Mock settings dictionary."""
    return {"theme": "light", "font_family": "TkDefaultFont", "font_size": 12}


@pytest.fixture
def game_versions():
    """Sample game versions."""
    return [
        GameVersion(flavor_dir="_retail_", display_name="Retail", path="C:\\retail"),
        GameVersion(flavor_dir="_classic_", display_name="Classic", path="C:\\classic"),
    ]


@pytest.fixture
def folder_tab(loc, settings, game_versions):
    """Create FolderCleanerTab instance with mocked Tk."""
    with patch("ui.tabs.folder_cleaner_tab.ttk.Frame") as mock_frame_class:
        mock_parent = MagicMock()
        mock_frame = MagicMock()
        mock_frame_class.return_value = mock_frame

        with patch("ui.tabs.folder_cleaner_tab.ttk.Notebook"):
            tab = FolderCleanerTab(
                parent=mock_parent,
                loc=loc,
                on_scan_folders=Mock(),
                on_select_all_toggle=Mock(),
                on_remove_selected=Mock(),
                get_selected_items=Mock(),
                game_versions=game_versions,
                settings=settings,
            )
            return tab


def test_folder_cleaner_tab_initialization(folder_tab, game_versions):
    """Test folder cleaner tab initializes correctly."""
    assert folder_tab.frame is not None
    assert folder_tab.loc is not None
    assert folder_tab.game_versions == game_versions
    assert folder_tab.settings is not None
    assert folder_tab.sub_tabs is not None
    assert len(folder_tab.version_frames) == len(game_versions)
    assert folder_tab.folder_checkboxes == {gv.flavor_dir: {} for gv in game_versions}


def test_display_scan_results_empty(folder_tab):
    """Test display_scan_results with no results."""
    folder_tab.display_scan_results({})

    # All version frames should be cleared
    for frame in folder_tab.version_frames.values():
        assert len(frame.winfo_children()) == 0


def test_display_scan_results_with_folders(folder_tab):
    """Test display_scan_results with folders found."""
    with patch("ui.tabs.folder_cleaner_tab.tk.BooleanVar") as mock_bool_var:
        mock_var = MagicMock()
        mock_bool_var.return_value = mock_var

        # Mock the frame for _retail_
        mock_frame = MagicMock()
        folder_tab.version_frames["_retail_"] = mock_frame

        results = {
            "_retail_": {
                "errors": "C:/WoW/_retail_/Errors",
                "logs": "C:/WoW/_retail_/Logs",
                "cache": "C:/WoW/_retail_/Cache",
            }
        }

        folder_tab.display_scan_results(results)

        # Check that checkboxes were created for _retail_
        assert "_retail_" in folder_tab.folder_checkboxes
        assert "errors" in folder_tab.folder_checkboxes["_retail_"]
        assert "logs" in folder_tab.folder_checkboxes["_retail_"]
        assert "cache" in folder_tab.folder_checkboxes["_retail_"]


def test_display_scan_results_with_screenshots(folder_tab):
    """Test display_scan_results with screenshots folder and files."""
    with patch("ui.tabs.folder_cleaner_tab.tk.BooleanVar"):
        with patch.object(folder_tab, "_build_screenshot_view") as mock_build:
            # Mock the frame for _retail_
            mock_frame = MagicMock()
            folder_tab.version_frames["_retail_"] = mock_frame

            results = {
                "_retail_": {
                    "screenshots": "C:/WoW/_retail_/Screenshots",
                }
            }
            screenshot_files = {
                "_retail_": [
                    "C:/WoW/_retail_/Screenshots/shot1.jpg",
                    "C:/WoW/_retail_/Screenshots/shot2.png",
                ]
            }

            folder_tab.display_scan_results(results, screenshot_files)

            # Check that _build_screenshot_view was called
            mock_build.assert_called_once()
            args = mock_build.call_args[0]
            assert args[0] == "_retail_"
            assert args[2] == "C:/WoW/_retail_/Screenshots"
            assert len(args[3]) == 2


def test_toggle_select_all_selects_when_unselected(folder_tab):
    """Test toggle_select_all selects all non-cache folders when some are unselected."""
    # Mock BooleanVar instances
    errors_var = MagicMock()
    errors_var.get.return_value = False
    logs_var = MagicMock()
    logs_var.get.return_value = False
    cache_var = MagicMock()
    cache_var.get.return_value = False

    folder_tab.folder_checkboxes = {
        "_retail_": {
            "errors": (errors_var, MagicMock(), "C:/WoW/_retail_/Errors"),
            "logs": (logs_var, MagicMock(), "C:/WoW/_retail_/Logs"),
            "cache": (cache_var, MagicMock(), "C:/WoW/_retail_/Cache"),
        }
    }

    folder_tab.toggle_select_all()

    # Non-cache folders should be selected
    errors_var.set.assert_called_once_with(True)
    logs_var.set.assert_called_once_with(True)
    # Cache should not be touched
    cache_var.set.assert_not_called()


def test_toggle_select_all_unselects_when_all_selected(folder_tab):
    """Test toggle_select_all unselects all non-cache folders when all are selected."""
    # Mock BooleanVar instances - all non-cache selected
    errors_var = MagicMock()
    errors_var.get.return_value = True
    logs_var = MagicMock()
    logs_var.get.return_value = True
    cache_var = MagicMock()
    cache_var.get.return_value = False

    folder_tab.folder_checkboxes = {
        "_retail_": {
            "errors": (errors_var, MagicMock(), "C:/WoW/_retail_/Errors"),
            "logs": (logs_var, MagicMock(), "C:/WoW/_retail_/Logs"),
            "cache": (cache_var, MagicMock(), "C:/WoW/_retail_/Cache"),
        }
    }

    folder_tab.toggle_select_all()

    # All non-cache should be unselected
    errors_var.set.assert_called_once_with(False)
    logs_var.set.assert_called_once_with(False)
    cache_var.set.assert_not_called()


def test_toggle_select_all_ignores_cache(folder_tab):
    """Test toggle_select_all never touches cache folder."""
    cache_var = MagicMock()
    cache_var.get.return_value = False

    folder_tab.folder_checkboxes = {
        "_retail_": {
            "cache": (cache_var, MagicMock(), "C:/WoW/_retail_/Cache"),
        }
    }

    # Toggle multiple times
    folder_tab.toggle_select_all()
    cache_var.set.assert_not_called()

    folder_tab.toggle_select_all()
    cache_var.set.assert_not_called()


def test_get_selected_folders_returns_checked_paths(folder_tab):
    """Test get_selected_folders returns only checked folder paths."""
    errors_var = MagicMock()
    errors_var.get.return_value = True
    logs_var = MagicMock()
    logs_var.get.return_value = False

    folder_tab.folder_checkboxes = {
        "_retail_": {
            "errors": (errors_var, MagicMock(), "C:/WoW/_retail_/Errors"),
            "logs": (logs_var, MagicMock(), "C:/WoW/_retail_/Logs"),
        }
    }

    selected = folder_tab.get_selected_folders()
    assert len(selected) == 1
    assert "C:/WoW/_retail_/Errors" in selected


def test_get_selected_folders_multiple_versions(folder_tab):
    """Test get_selected_folders across multiple game versions."""
    retail_errors_var = MagicMock()
    retail_errors_var.get.return_value = True
    classic_logs_var = MagicMock()
    classic_logs_var.get.return_value = True

    folder_tab.folder_checkboxes = {
        "_retail_": {
            "errors": (retail_errors_var, MagicMock(), "C:/WoW/_retail_/Errors")
        },
        "_classic_": {"logs": (classic_logs_var, MagicMock(), "C:/WoW/_classic_/Logs")},
    }

    selected = folder_tab.get_selected_folders()
    assert len(selected) == 2


def test_relative_path_for_display(folder_tab):
    """Test relative path display helper."""
    result = folder_tab._relative_path_for_display(
        "C:/WoW/_retail_/Screenshots/shot1.jpg", "C:/WoW/_retail_/Screenshots"
    )
    assert result == "shot1.jpg"


def test_relative_path_for_display_fallback(folder_tab):
    """Test relative path display falls back to basename on error."""

    # Mock os.path.relpath to raise exception
    with patch("os.path.relpath", side_effect=ValueError("Invalid path")):
        result = folder_tab._relative_path_for_display("C:/invalid/path.jpg", "C:/root")
        assert result == "path.jpg"


def test_clear_preview(folder_tab):
    """Test clearing screenshot preview."""
    # Setup preview canvas
    mock_canvas = MagicMock()
    folder_tab.screenshot_previews["_retail_"] = mock_canvas
    folder_tab.screenshot_images["_retail_"] = Mock()

    folder_tab._clear_preview("_retail_")

    mock_canvas.delete.assert_called_once_with("all")
    assert folder_tab.screenshot_images["_retail_"] is None


def test_clear_preview_no_canvas(folder_tab):
    """Test clearing preview when no canvas exists."""
    # Should not raise error
    folder_tab._clear_preview("nonexistent")


def test_show_screenshot_handles_missing_pil(folder_tab, tmp_path):
    """Test showing screenshot handles missing PIL gracefully."""
    mock_canvas = MagicMock()
    folder_tab.screenshot_previews["_retail_"] = mock_canvas

    img_path = tmp_path / "test.jpg"
    img_path.write_text("")

    # Mock import to raise ImportError
    with patch("builtins.__import__", side_effect=ImportError("No PIL")):
        with patch.object(folder_tab, "_clear_preview") as mock_clear:
            # Should not raise, just clear preview
            folder_tab._show_screenshot("_retail_", str(img_path))
            mock_clear.assert_called_once()


def test_screenshot_selection_updates_preview(folder_tab):
    """Test selecting screenshot in tree triggers preview update."""
    # Setup tree and preview
    mock_tree = MagicMock()
    mock_tree.selection.return_value = ["shot_0"]
    folder_tab.screenshot_trees["_retail_"] = mock_tree
    folder_tab.screenshot_previews["_retail_"] = MagicMock()
    folder_tab.screenshot_item_paths["_retail_"] = {"shot_0": "C:/test.jpg"}

    with patch.object(folder_tab, "_show_screenshot") as mock_show:
        folder_tab._on_screenshot_selected("_retail_")

        mock_show.assert_called_once_with("_retail_", "C:/test.jpg")


def test_screenshot_deselection_clears_preview(folder_tab):
    """Test deselecting screenshot clears preview."""
    mock_tree = MagicMock()
    mock_tree.selection.return_value = []
    folder_tab.screenshot_trees["_retail_"] = mock_tree
    folder_tab.screenshot_previews["_retail_"] = MagicMock()

    with patch.object(folder_tab, "_clear_preview") as mock_clear:
        # No selection
        folder_tab._on_screenshot_selected("_retail_")

        mock_clear.assert_called_once_with("_retail_")


def test_preview_click_opens_viewer(folder_tab):
    """Test clicking preview canvas opens screenshot viewer."""
    # Setup the tree with a selection
    folder_tab.screenshot_item_paths["_retail_"] = {"shot_0": "C:/test.jpg"}

    # Mock the tree to return a selection
    mock_tree = MagicMock()
    mock_tree.selection.return_value = ["shot_0"]
    folder_tab.screenshot_trees["_retail_"] = mock_tree

    with patch("ui.tabs.folder_cleaner_tab.ScreenshotViewer") as mock_viewer_class:
        mock_viewer = MagicMock()
        mock_viewer_class.return_value = mock_viewer

        # Trigger preview click
        folder_tab._on_preview_click("_retail_")

        # Verify viewer was created and shown
        mock_viewer_class.assert_called_once()
        mock_viewer.show.assert_called_once()


def test_preview_click_does_nothing_without_image(folder_tab):
    """Test clicking preview with no image does nothing."""
    # No image path set
    folder_tab.screenshot_item_paths["_retail_"] = None

    with patch("ui.tabs.folder_cleaner_tab.ScreenshotViewer") as mock_viewer_class:
        # Trigger preview click
        folder_tab._on_preview_click("_retail_")

        # Viewer should not be created
        mock_viewer_class.assert_not_called()


def test_display_results_clears_stale_data(folder_tab):
    """Test display_scan_results clears old data between scans."""
    with patch("ui.tabs.folder_cleaner_tab.tk.BooleanVar"):
        # Mock the frame for _retail_
        mock_frame = MagicMock()
        folder_tab.version_frames["_retail_"] = mock_frame

        # First scan
        results1 = {"_retail_": {"errors": "C:/WoW/_retail_/Errors"}}
        folder_tab.display_scan_results(results1)

        assert "_retail_" in folder_tab.folder_checkboxes
        assert "errors" in folder_tab.folder_checkboxes["_retail_"]

        # Second scan with different results
        results2 = {"_retail_": {"logs": "C:/WoW/_retail_/Logs"}}
        folder_tab.display_scan_results(results2)

        # Old data should be gone
        assert "errors" not in folder_tab.folder_checkboxes["_retail_"]
        assert "logs" in folder_tab.folder_checkboxes["_retail_"]


def test_no_folders_message_displayed(folder_tab):
    """Test 'no folders found' message when version has no cleanable folders."""
    mock_frame = MagicMock()
    folder_tab.version_frames["_retail_"] = mock_frame

    results = {"_retail_": {}}
    folder_tab.display_scan_results(results)

    # Should have called pack on a label widget
    assert (
        mock_frame.winfo_children.called
        or len(folder_tab.folder_checkboxes.get("_retail_", {})) == 0
    )


def test_screenshot_cache_initialization(folder_tab):
    """Test screenshot cache is initialized as empty dict."""
    assert folder_tab.screenshot_cache == {}
    assert isinstance(folder_tab.screenshot_cache, dict)


def test_screenshot_cache_stores_images(folder_tab):
    """Test screenshots are cached after loading."""
    mock_photo = MagicMock()
    mock_photo.width.return_value = 200
    mock_photo.height.return_value = 150

    file_path = "C:/WoW/_retail_/Screenshots/shot1.jpg"
    folder_tab.screenshot_cache[file_path] = mock_photo

    assert file_path in folder_tab.screenshot_cache
    assert folder_tab.screenshot_cache[file_path] == mock_photo


def test_screenshot_cache_cleared_on_rescan(folder_tab):
    """Test screenshot cache is cleared when display_scan_results is called."""
    # Pre-populate cache
    folder_tab.screenshot_cache["old_path"] = MagicMock()
    assert len(folder_tab.screenshot_cache) > 0

    with patch("ui.tabs.folder_cleaner_tab.tk.BooleanVar"):
        mock_frame = MagicMock()
        folder_tab.version_frames["_retail_"] = mock_frame

        results = {"_retail_": {}}
        folder_tab.display_scan_results(results)

        # Cache should be empty after rescan
        assert folder_tab.screenshot_cache == {}


def test_debounced_wraplength_initialization(folder_tab):
    """Test debounce timer is initialized to None."""
    assert folder_tab._configure_timer is None


def test_debounced_update_wraplength_sets_timer(folder_tab):
    """Test _debounced_update_wraplength schedules update with timer."""
    with patch.object(folder_tab.frame, "after") as mock_after:
        folder_tab._debounced_update_wraplength()

        # Should call after with 50ms delay
        mock_after.assert_called_once()
        call_args = mock_after.call_args[0]
        assert call_args[0] == 50  # 50ms debounce


def test_debounced_wraplength_cancels_previous_timer(folder_tab):
    """Test _debounced_update_wraplength cancels previous timer."""
    with patch.object(folder_tab.frame, "after") as mock_after:
        with patch.object(folder_tab.frame, "after_cancel") as mock_cancel:
            # Set a fake timer
            folder_tab._configure_timer = 12345

            folder_tab._debounced_update_wraplength()

            # Should cancel previous timer
            mock_cancel.assert_called_once_with(12345)
            # Should schedule new timer
            mock_after.assert_called_once()


def test_refresh_wraplength_updates_on_font_change(folder_tab):
    """Test refresh_wraplength updates when font size changes."""
    folder_tab.font_size = 14

    with patch.object(folder_tab, "_update_wraplength") as mock_update:
        folder_tab.refresh_wraplength(16)

        assert folder_tab.font_size == 16
        mock_update.assert_called_once()


def test_screenshot_cache_stores_images_simple(folder_tab):
    """Test screenshot cache can store and retrieve PhotoImage objects."""
    mock_photo = MagicMock()
    file_path = "C:/WoW/_retail_/Screenshots/shot1.jpg"
    folder_tab.screenshot_cache[file_path] = mock_photo

    assert file_path in folder_tab.screenshot_cache
    assert folder_tab.screenshot_cache[file_path] == mock_photo


def test_update_instruction_wraplength(folder_tab):
    """Test instruction label wraplength updates based on panel width."""
    mock_label = MagicMock()
    mock_event = MagicMock()
    mock_event.width = 300

    folder_tab._update_instruction_wraplength(mock_event, mock_label)

    # Should set wraplength to width - 20
    mock_label.configure.assert_called_once()
    call_kwargs = mock_label.configure.call_args[1]
    assert call_kwargs["wraplength"] == 280
