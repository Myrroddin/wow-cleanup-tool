"""External dependency checker and installer."""

import subprocess
import sys
import importlib.util
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import ttk


class DependencyManager:
    """Manage and install required external dependencies."""

    REQUIRED_PACKAGES = {
        "send2trash": "send2trash>=2.0.0",
        "PIL": "Pillow>=12.1.0",
        "sv_ttk": "sv-ttk>=2.6.0",
        "darkdetect": "darkdetect>=0.8.0",
        "orjson": "orjson>=3.11.0",
    }

    def __init__(self):
        self.missing_packages = []
        self.installation_results = {}

    def check_dependencies(self):
        """Check which required packages are missing.

        Returns:
            list: List of missing package names
        """
        self.missing_packages = []

        for package_name in self.REQUIRED_PACKAGES.keys():
            if not self._is_package_installed(package_name):
                self.missing_packages.append(package_name)

        return self.missing_packages

    def install_missing_dependencies(
        self, callback=None, progress_callback=None, update_queue=None
    ):
        """Install all missing dependencies in parallel with thread-safe queue updates.

        Args:
            callback: Optional callback function(package_name, success, message, timed_out)
            progress_callback: Optional callback for installation progress
            update_queue: Optional queue.Queue for thread-safe UI updates

        Returns:
            bool: True if all installations succeeded
        """
        if not self.missing_packages:
            self.check_dependencies()

        if not self.missing_packages:
            return True

        all_success = True

        # Install packages in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(
            max_workers=min(3, len(self.missing_packages))
        ) as executor:
            # Submit all installation tasks
            future_to_package = {
                executor.submit(
                    self._install_package,
                    self.REQUIRED_PACKAGES[package_name],
                    progress_callback,
                    update_queue,
                ): package_name
                for package_name in self.missing_packages
            }

            # Process results as they complete
            for future in as_completed(future_to_package):
                package_name = future_to_package[future]
                try:
                    success, message, timed_out = future.result()

                    self.installation_results[package_name] = {
                        "success": success,
                        "message": message,
                        "timed_out": timed_out,
                    }

                    if callback:
                        if update_queue:
                            update_queue.put(
                                ("complete", package_name, success, message, timed_out)
                            )
                        else:
                            callback(package_name, success, message, timed_out)

                    if not success:
                        all_success = False
                except Exception as e:
                    self.installation_results[package_name] = {
                        "success": False,
                        "message": f"Installation error: {e}",
                        "timed_out": False,
                    }
                    if callback:
                        if update_queue:
                            update_queue.put(
                                (
                                    "complete",
                                    package_name,
                                    False,
                                    f"Installation error: {e}",
                                    False,
                                )
                            )
                        else:
                            callback(
                                package_name, False, f"Installation error: {e}", False
                            )
                    all_success = False

        return all_success

    def _is_package_installed(self, package_name):
        """Check if a package is installed.

        Args:
            package_name: Name of the package

        Returns:
            bool: True if installed
        """
        spec = importlib.util.find_spec(package_name)
        return spec is not None

    def _install_package(self, package_spec, progress_callback=None, update_queue=None):
        """Install a single package using pip (stable releases only).

        Args:
            package_spec: Package specification (e.g., 'package>=1.0.0')
            progress_callback: Optional callback for progress updates
            update_queue: Optional queue for thread-safe UI updates

        Returns:
            tuple: (success, message, timed_out)
        """
        package_name = package_spec.split(">=")[0].split("==")[0]

        # Install latest stable release with version constraint
        if progress_callback:
            if update_queue:
                update_queue.put(("progress", package_name))
            else:
                progress_callback(package_name)

        try:
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--no-cache-dir",
                    package_spec,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
            return (True, f"Successfully installed {package_spec}", False)
        except subprocess.TimeoutExpired:
            return (False, f"Installation timed out for {package_spec}", True)
        except (subprocess.CalledProcessError, Exception) as e:
            return (False, f"Failed to install {package_spec}: {e}", False)


def check_and_install_dependencies():
    """Check and install dependencies with UI feedback on timeout.

    Returns:
        bool: True if all dependencies are available
    """
    manager = DependencyManager()
    missing = manager.check_dependencies()

    if not missing:
        return True

    # Load localization and settings before showing UI
    try:
        from localization import Localization
        from core.settings import load_settings
        from core.themes import get_theme_colors, THEMES, resolve_system_theme

        settings = load_settings()
        loc = Localization(settings.get("language", "en_us"))
        theme_name = settings.get("theme", "system")
        theme = get_theme_colors(theme_name)
    except Exception:
        # Fallback to English if localization fails
        class FallbackLoc:
            def _(self, key):
                return key

        loc = FallbackLoc()
        try:
            theme = THEMES[resolve_system_theme()]
        except Exception:
            # Minimal light-ish fallback if theme data unavailable
            theme = {
                "bg": "#f0f0f0",
                "frame_bg": "#f0f0f0",
                "fg": "#000000",
                "select_bg": "#0078d7",
                "select_fg": "#ffffff",
            }

    # Show progress UI during installation
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()

        # Create progress window
        progress_window = tk.Toplevel(root)
        progress_window.title(loc._("title_dependencies"))
        progress_window.geometry("450x200")
        progress_window.resizable(False, False)
        progress_window.transient(root)
        progress_window.grab_set()

        # Apply theme colors
        progress_window.configure(bg=theme["bg"])

        # Center window
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (200 // 2)
        progress_window.geometry(f"450x200+{x}+{y}")

        # Apply theme to ttk widgets
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=theme["frame_bg"])
        style.configure("TLabel", background=theme["frame_bg"], foreground=theme["fg"])

        # Configure themed progress bar
        style.configure(
            "Themed.Horizontal.TProgressbar",
            troughcolor=theme["entry_bg"],
            background=theme["select_bg"],
            bordercolor=theme["button_bg"],
            lightcolor=theme["select_bg"],
            darkcolor=theme["select_bg"],
        )

        content = ttk.Frame(progress_window, padding=20)
        content.pack(fill="both", expand=True)

        status_label = ttk.Label(
            content,
            text=loc._("status_initializing"),
            font=("TkDefaultFont", 10),
            wraplength=410,
        )
        status_label.pack(pady=(0, 10))

        # Overall progress bar
        overall_progress = ttk.Progressbar(
            content,
            mode="determinate",
            style="Themed.Horizontal.TProgressbar",
            length=400,
        )
        overall_progress.pack(pady=(0, 15))

        detail_label = ttk.Label(
            content, text="", font=("TkDefaultFont", 9), wraplength=410
        )
        detail_label.pack(pady=(0, 10))

        # Current package progress bar
        package_progress = ttk.Progressbar(
            content,
            mode="indeterminate",
            style="Themed.Horizontal.TProgressbar",
            length=400,
        )
        package_progress.pack(pady=(0, 10))

        had_timeout = False
        total_packages = len(missing)
        current_package_index = 0
        installation_complete = False
        installation_success = False

        # Create queue for thread-safe communication
        update_queue = queue.Queue()

        # Track active packages for parallel progress display
        active_packages = set()

        def process_queue():
            """Process queue messages on main thread (thread-safe UI updates)."""
            nonlocal had_timeout, current_package_index, installation_complete, installation_success

            try:
                while True:
                    msg = update_queue.get_nowait()
                    msg_type = msg[0]

                    if msg_type == "progress":
                        # Format: ("progress", package_name)
                        package = msg[1]
                        active_packages.add(package)
                        # Show all active packages
                        if len(active_packages) == 1:
                            detail_label.config(
                                text=loc._("dep_installing_single").format(package)
                            )
                        else:
                            detail_label.config(
                                text=loc._("dep_installing_parallel").format(
                                    len(active_packages)
                                )
                            )
                        package_progress.start(10)

                    elif msg_type == "complete":
                        # Format: ("complete", package, success, message, timed_out)
                        package, success, message, timed_out = msg[1:]
                        if package in active_packages:
                            active_packages.remove(package)

                        if timed_out:
                            had_timeout = True

                        package_progress.stop()
                        status = "✓" if success else "✗"
                        status_label.config(text=f"{status} {package}")
                        if timed_out:
                            detail_label.config(text=loc._("dep_taking_longer"))

                        current_package_index += 1
                        overall_progress["value"] = (
                            current_package_index / total_packages
                        ) * 100

                    elif msg_type == "done":
                        # Installation thread finished
                        installation_complete = True
                        installation_success = msg[1]

            except queue.Empty:
                pass

            # Continue polling if not complete
            if not installation_complete:
                progress_window.after(50, process_queue)

        def run_installation():
            """Run installation in background, signal completion via queue."""
            success = manager.install_missing_dependencies(
                callback=lambda *args: None,  # Handled via queue
                progress_callback=lambda *args: None,  # Handled via queue
                update_queue=update_queue,
            )
            update_queue.put(("done", success))

        # Start queue polling
        progress_window.after(50, process_queue)

        # Start installation in background thread
        import threading

        install_thread = threading.Thread(target=run_installation, daemon=True)
        install_thread.start()

        # Wait for installation to complete
        while not installation_complete:
            progress_window.update()
            root.update()

        progress_window.destroy()

        if not installation_success:
            messagebox.showerror(
                loc._("dep_install_failed"), loc._("dep_install_failed_msg")
            )
            root.destroy()
            return False

        if had_timeout:
            messagebox.showinfo(
                loc._("dep_install_complete"), loc._("dep_install_complete_msg")
            )

        root.destroy()
        return True

    except ImportError:
        # Fallback if tkinter not available
        success = manager.install_missing_dependencies()
        return success
