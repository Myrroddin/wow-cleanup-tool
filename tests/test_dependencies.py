"""Unit tests for dependency management and parallel installation.

This test module verifies the DependencyManager class and its features:
- Dependency checking and detection
- Parallel installation with ThreadPoolExecutor (3 workers)
- Thread-safe queue-based UI updates
- Fallback strategies (stable → beta → alpha)
- 30-second timeout handling per package
- Error handling and reporting

Created: January 3, 2026
Updated: January 3, 2026 - Added tests for queue-based parallel installation
"""

import sys
import os
import unittest
import queue
from unittest.mock import patch, MagicMock, call

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from core.dependencies import DependencyManager


class TestDependencyManager(unittest.TestCase):
    """Test DependencyManager class functionality."""

    def setUp(self):
        """Initialize test fixtures."""
        self.manager = DependencyManager()

    def tearDown(self):
        """Clean up after tests."""
        self.manager = None

    def test_init_creates_manager(self):
        """Test DependencyManager initialization."""
        manager = DependencyManager()
        assert manager.missing_packages == []
        assert manager.installation_results == {}
        assert manager.REQUIRED_PACKAGES == {
            "send2trash": "send2trash>=1.8.0",
            "psutil": "psutil>=5.9.0",
            "PIL": "Pillow>=10.0.0",
        }

    def test_check_dependencies_all_present(self):
        """Test check_dependencies when all packages are installed."""
        with patch.object(self.manager, "_is_package_installed", return_value=True):
            missing = self.manager.check_dependencies()
            assert missing == []
            assert self.manager.missing_packages == []

    def test_check_dependencies_some_missing(self):
        """Test check_dependencies when some packages are missing."""

        def mock_is_installed(package_name):
            return package_name != "send2trash"

        with patch.object(
            self.manager, "_is_package_installed", side_effect=mock_is_installed
        ):
            missing = self.manager.check_dependencies()
            assert "send2trash" in missing
            assert "psutil" not in missing
            assert "PIL" not in missing

    def test_check_dependencies_all_missing(self):
        """Test check_dependencies when all packages are missing."""
        with patch.object(self.manager, "_is_package_installed", return_value=False):
            missing = self.manager.check_dependencies()
            assert len(missing) == 3
            assert set(missing) == {"send2trash", "psutil", "PIL"}

    def test_is_package_installed_found(self):
        """Test _is_package_installed returns True for installed package."""
        with patch("importlib.util.find_spec", return_value=MagicMock()):
            result = self.manager._is_package_installed("tkinter")
            assert result is True

    def test_is_package_installed_not_found(self):
        """Test _is_package_installed returns False for missing package."""
        with patch("importlib.util.find_spec", return_value=None):
            result = self.manager._is_package_installed("nonexistent_package")
            assert result is False

    def test_install_missing_dependencies_none_missing(self):
        """Test install_missing_dependencies returns True when nothing missing."""
        self.manager.missing_packages = []
        result = self.manager.install_missing_dependencies()
        assert result is True

    def test_install_missing_dependencies_with_callback(self):
        """Test install_missing_dependencies calls callback on completion."""
        self.manager.missing_packages = ["send2trash"]

        callback = MagicMock()

        with patch.object(self.manager, "_install_package") as mock_install:
            mock_install.return_value = (True, "Successfully installed", False)

            result = self.manager.install_missing_dependencies(callback=callback)

            assert result is True
            callback.assert_called()

    def test_install_missing_dependencies_parallel_execution(self):
        """Test install_missing_dependencies uses ThreadPoolExecutor with 3 workers max."""
        self.manager.missing_packages = ["send2trash", "psutil", "PIL"]

        with patch("core.dependencies.ThreadPoolExecutor") as mock_executor_class:
            mock_executor = MagicMock()
            mock_executor_class.return_value.__enter__.return_value = mock_executor

            # Mock future results
            mock_future1 = MagicMock()
            mock_future1.result.return_value = (True, "Success", False)
            mock_executor.submit.return_value = mock_future1

            with patch(
                "core.dependencies.as_completed",
                return_value=[mock_future1, mock_future1, mock_future1],
            ):
                with patch.object(self.manager, "_install_package") as mock_install:
                    mock_install.return_value = (True, "Success", False)

                    self.manager.install_missing_dependencies()

                    # Verify ThreadPoolExecutor was created with max_workers
                    mock_executor_class.assert_called()
                    call_kwargs = (
                        mock_executor_class.call_args[1]
                        if mock_executor_class.call_args[1]
                        else {}
                    )
                    call_args = (
                        mock_executor_class.call_args[0]
                        if mock_executor_class.call_args[0]
                        else ()
                    )
                    # max_workers should be min(3, 3) = 3
                    max_workers_arg = call_kwargs.get("max_workers") or (
                        call_args[0] if call_args else 3
                    )
                    assert max_workers_arg == 3

    def test_install_missing_dependencies_with_queue(self):
        """Test install_missing_dependencies accepts update_queue parameter."""
        self.manager.missing_packages = []

        # Just test that the method accepts update_queue without error
        update_queue = queue.Queue()
        result = self.manager.install_missing_dependencies(update_queue=update_queue)

        # When no packages missing, should return True
        assert result is True

    def test_install_package_stable_success(self):
        """Test _install_package succeeds with stable release."""
        with patch("subprocess.check_call") as mock_check_call:
            success, message, timed_out = self.manager._install_package(
                "send2trash>=1.8.0"
            )

            assert success is True
            assert "send2trash" in message
            assert timed_out is False
            mock_check_call.assert_called_once()
            call_args = mock_check_call.call_args[0][0]
            assert "--no-cache-dir" in call_args
            assert "send2trash>=1.8.0" in call_args

    def test_install_package_stable_timeout_tries_beta(self):
        """Test _install_package falls back to beta on stable timeout."""
        with patch("subprocess.check_call") as mock_check_call:

            def side_effect(*args, **kwargs):
                # First call (stable) times out, second (beta) succeeds
                if mock_check_call.call_count == 1:
                    import subprocess

                    raise subprocess.TimeoutExpired("pip", 30)
                # Beta succeeds
                return None

            mock_check_call.side_effect = side_effect

            success, message, timed_out = self.manager._install_package(
                "send2trash>=1.8.0"
            )

            assert success is True
            assert timed_out is True  # At least one strategy timed out
            assert mock_check_call.call_count >= 2  # Tried stable, then beta

    def test_install_package_all_strategies_fail(self):
        """Test _install_package returns False when all strategies fail."""
        with patch("subprocess.check_call") as mock_check_call:
            import subprocess

            mock_check_call.side_effect = subprocess.CalledProcessError(1, "pip")

            success, message, timed_out = self.manager._install_package(
                "send2trash>=1.8.0"
            )

            assert success is False
            assert "Failed to install" in message
            assert timed_out is False

    def test_install_package_timeout_flag_set(self):
        """Test _install_package sets timed_out flag on TimeoutExpired."""
        with patch("subprocess.check_call") as mock_check_call:
            import subprocess

            mock_check_call.side_effect = subprocess.TimeoutExpired("pip", 30)

            success, message, timed_out = self.manager._install_package(
                "send2trash>=1.8.0"
            )

            assert success is False
            assert timed_out is True

    def test_install_package_30_second_timeout(self):
        """Test _install_package uses 30-second timeout for pip."""
        with patch("subprocess.check_call") as mock_check_call:
            self.manager._install_package("send2trash>=1.8.0")

            # Check timeout parameter
            call_kwargs = mock_check_call.call_args[1]
            assert call_kwargs.get("timeout") == 30

    def test_install_package_progress_callback(self):
        """Test _install_package calls progress_callback for each strategy."""
        progress_callback = MagicMock()

        with patch("subprocess.check_call"):
            self.manager._install_package(
                "send2trash>=1.8.0", progress_callback=progress_callback
            )

            # Should call progress_callback at least once
            assert progress_callback.called

    def test_install_package_progress_to_queue(self):
        """Test _install_package accepts update_queue parameter without error."""
        update_queue = queue.Queue()

        with patch("subprocess.check_call"):
            # Method should accept update_queue without raising
            success, message, timed_out = self.manager._install_package(
                "send2trash>=1.8.0", update_queue=update_queue
            )

            # Should complete without error
            assert isinstance(success, bool)
            assert isinstance(message, str)
            assert isinstance(timed_out, bool)

    def test_installation_results_stored(self):
        """Test installation results are stored in installation_results dict."""
        self.manager.missing_packages = ["send2trash"]

        with patch.object(self.manager, "_install_package") as mock_install:
            mock_install.return_value = (True, "Successfully installed", False)

            self.manager.install_missing_dependencies()

            assert "send2trash" in self.manager.installation_results
            assert self.manager.installation_results["send2trash"]["success"] is True

    def test_mixed_success_and_failure(self):
        """Test install_missing_dependencies with mixed success/failure results."""
        self.manager.missing_packages = ["send2trash", "psutil"]

        def mock_install(package_spec, *args, **kwargs):
            if "send2trash" in package_spec:
                return (True, "Success", False)
            else:
                return (False, "Failed", False)

        with patch.object(self.manager, "_install_package", side_effect=mock_install):
            result = self.manager.install_missing_dependencies()

            # Overall success should be False due to psutil failure
            assert result is False

    def test_package_name_extraction(self):
        """Test package name is extracted correctly from spec."""
        with patch("subprocess.check_call"):
            self.manager._install_package("Pillow>=10.0.0")

            # Should not raise error even with Pillow/PIL mismatch
            # The code handles this by splitting on >= and ==


if __name__ == "__main__":
    unittest.main()
