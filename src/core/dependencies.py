"""External dependency checker and installer."""
import subprocess
import sys
import importlib.util
from tkinter import ttk


class DependencyManager:
    """Manage and install required external dependencies."""
    
    REQUIRED_PACKAGES = {
        'send2trash': 'send2trash>=1.8.0',
        'psutil': 'psutil>=5.9.0',
        'PIL': 'Pillow>=10.0.0',
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
    
    def install_missing_dependencies(self, callback=None, progress_callback=None):
        """Install all missing dependencies.
        
        Args:
            callback: Optional callback function(package_name, success, message, timed_out)
            progress_callback: Optional callback for installation progress
            
        Returns:
            bool: True if all installations succeeded
        """
        if not self.missing_packages:
            self.check_dependencies()
        
        if not self.missing_packages:
            return True
        
        all_success = True
        
        for package_name in self.missing_packages:
            package_spec = self.REQUIRED_PACKAGES[package_name]
            success, message, timed_out = self._install_package(package_spec, progress_callback)
            
            self.installation_results[package_name] = {
                'success': success,
                'message': message,
                'timed_out': timed_out
            }
            
            if callback:
                callback(package_name, success, message, timed_out)
            
            if not success:
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
    
    def _install_package(self, package_spec, progress_callback=None):
        """Install a single package using pip with fallback strategy.
        
        Tries to install in this order:
        1. Latest stable release
        2. Latest beta/rc version (--pre flag)
        3. Latest alpha version (--pre flag with upgrade)
        
        Args:
            package_spec: Package specification (e.g., 'package>=1.0.0')
            progress_callback: Optional callback for progress updates
            
        Returns:
            tuple: (success, message, timed_out)
        """
        package_name = package_spec.split('>=')[0].split('==')[0]
        timed_out = False
        
        # Strategy 1: Try stable release with version constraint
        if progress_callback:
            progress_callback('stable', package_name)
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', package_spec],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=60
            )
            return (True, f"Successfully installed {package_spec}", False)
        except subprocess.TimeoutExpired:
            timed_out = True
        except subprocess.CalledProcessError:
            pass
        
        # Strategy 2: Try latest pre-release (beta/rc)
        if progress_callback:
            progress_callback('beta', package_name)
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', '--pre', package_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=60
            )
            return (True, f"Successfully installed {package_name} (pre-release)", timed_out)
        except subprocess.TimeoutExpired:
            timed_out = True
        except subprocess.CalledProcessError:
            pass
        
        # Strategy 3: Try latest alpha with upgrade flag
        if progress_callback:
            progress_callback('alpha', package_name)
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', '--pre', '--upgrade', package_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=60
            )
            return (True, f"Successfully installed {package_name} (alpha)", timed_out)
        except subprocess.TimeoutExpired:
            timed_out = True
        except (subprocess.CalledProcessError, Exception) as e:
            return (False, f"Failed to install {package_spec}: {e}", timed_out)
        
        return (False, f"Failed to install {package_spec}", timed_out)
    
    def get_installation_summary(self):
        """Get summary of installation results.
        
        Returns:
            dict: Summary with success/failure counts and details
        """
        if not self.installation_results:
            return {
                'total': 0,
                'successful': 0,
                'failed': 0,
                'details': {}
            }
        
        successful = sum(1 for r in self.installation_results.values() if r['success'])
        failed = len(self.installation_results) - successful
        
        return {
            'total': len(self.installation_results),
            'successful': successful,
            'failed': failed,
            'details': self.installation_results.copy()
        }


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
        from core.themes import THEMES
        
        settings = load_settings()
        loc = Localization(settings.get('language', 'en_us'))
        theme_name = settings.get('theme', 'light')
        theme = THEMES[theme_name]
    except Exception:
        # Fallback to English if localization fails
        class FallbackLoc:
            def _(self, key): return key
        loc = FallbackLoc()
        theme = THEMES['light']
    
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
        progress_window.configure(bg=theme['bg'])
        
        # Center window
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (200 // 2)
        progress_window.geometry(f"450x200+{x}+{y}")
        
        # Apply theme to ttk widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=theme['frame_bg'])
        style.configure('TLabel', background=theme['frame_bg'], foreground=theme['fg'])
        
        # Configure themed progress bar
        style.configure('Themed.Horizontal.TProgressbar',
                       troughcolor=theme['entry_bg'],
                       background=theme['select_bg'],
                       bordercolor=theme['button_bg'],
                       lightcolor=theme['select_bg'],
                       darkcolor=theme['select_bg'])
        
        content = ttk.Frame(progress_window, padding=20)
        content.pack(fill='both', expand=True)
        
        status_label = ttk.Label(content, text=loc._("status_initializing"), 
                               font=('TkDefaultFont', 10), wraplength=410)
        status_label.pack(pady=(0, 10))
        
        # Overall progress bar
        overall_progress = ttk.Progressbar(content, mode='determinate', 
                                          style='Themed.Horizontal.TProgressbar',
                                          length=400)
        overall_progress.pack(pady=(0, 15))
        
        detail_label = ttk.Label(content, text="", 
                               font=('TkDefaultFont', 9), wraplength=410)
        detail_label.pack(pady=(0, 10))
        
        # Current package progress bar
        package_progress = ttk.Progressbar(content, mode='indeterminate',
                                          style='Themed.Horizontal.TProgressbar',
                                          length=400)
        package_progress.pack(pady=(0, 10))
        
        had_timeout = False
        total_packages = len(missing)
        current_package_index = 0
        
        def progress_callback(stage, package):
            stage_names = {
                'stable': loc._("version_stable"),
                'beta': loc._("version_beta"),
                'alpha': loc._("version_alpha")
            }
            detail_label.config(text=loc._("dep_trying_stage").format(
                stage_names.get(stage, stage), package))
            # Start indeterminate animation for current package
            package_progress.start(10)
            progress_window.update()
        
        def install_callback(package, success, message, timed_out):
            nonlocal had_timeout, current_package_index
            if timed_out:
                had_timeout = True
            
            # Stop package progress animation
            package_progress.stop()
            
            status = "✓" if success else "✗"
            status_label.config(text=f"{status} {package}")
            if timed_out:
                detail_label.config(text=loc._("dep_taking_longer"))
            
            # Update overall progress
            current_package_index += 1
            overall_progress['value'] = (current_package_index / total_packages) * 100
            
            progress_window.update()
        
        status_label.config(text=loc._("dep_installing_count").format(len(missing)))
        overall_progress['maximum'] = 100
        overall_progress['value'] = 0
        progress_window.update()
        
        success = manager.install_missing_dependencies(
            callback=install_callback,
            progress_callback=progress_callback
        )
        
        progress_window.destroy()
        
        if not success:
            messagebox.showerror(
                loc._("dep_install_failed"),
                loc._("dep_install_failed_msg")
            )
            root.destroy()
            return False
        
        if had_timeout:
            messagebox.showinfo(
                loc._("dep_install_complete"),
                loc._("dep_install_complete_msg")
            )
        
        root.destroy()
        return True
        
    except ImportError:
        # Fallback if tkinter not available
        success = manager.install_missing_dependencies()
        return success
