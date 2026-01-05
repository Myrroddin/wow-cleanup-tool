"""Game Optimizer Tab UI for WoW Cleanup Tool."""

from datetime import datetime
from pathlib import Path
from tkinter import ttk

from core.themes import get_theme_colors
from operations.config_handler import select_best_gpu, update_cvar
from operations.hardware_scanner import HardwareScanner
from operations.video_card_support import is_gpu_supported
from ui.dialogs import show_gpu_unsupported_warning
from ui.widgets.tooltip import Tooltip


class GameOptimizerTab:
    """Game Optimizer tab for hardware detection and optimization suggestions.

    Displays system hardware information (CPU, RAM, GPU) and will eventually
    provide Config.wtf optimization recommendations based on detected hardware.
    """

    def __init__(self, parent, loc, logger=None, settings=None, game_versions=None):
        """Initialize the Game Optimizer tab.

        Args:
            parent: Parent widget
            loc: Localization instance
            logger: Logger instance (optional)
        """
        self.loc = loc
        self.logger = logger
        self.scanner = HardwareScanner()
        self.settings = settings or {}
        self.hardware_info = None
        self.game_versions = game_versions or []
        self.version_tabs = None
        self.version_frames = {}
        self.optimization_status_labels = {}
        self.gpu_status_labels = {}
        self.parent_notebook = parent  # Store parent for tab disabling

        self.frame = ttk.Frame(parent, padding=10)
        self._create_content()

    def _create_content(self):
        """Create the Game Optimizer tab content."""
        # Description label
        self.desc_label = ttk.Label(
            self.frame,
            text=self.loc._("desc_game_optimizer"),
            justify="left",
        )
        self.desc_label.pack(side="top", fill="x", pady=(0, 10))
        # Bind to configure event with debouncing to reduce flicker
        self.desc_label.bind("<Configure>", self._debounced_update_wraplength)

        # Horizontal container for button and hardware info
        controls_frame = ttk.Frame(self.frame)
        controls_frame.pack(side="top", fill="x", pady=(0, 10))

        # Scan button on left
        self.scan_btn = ttk.Button(
            controls_frame,
            text=self.loc._("btn_scan_hardware"),
            command=self._on_scan_hardware,
        )
        self.scan_btn.pack(side="left", padx=(0, 20))

        # Tooltip showing cache age on hover
        def show_scan_tooltip(event):
            theme_name = self.settings.get("theme", "system")
            theme = get_theme_colors(theme_name)

            cached = self.hardware_info or self.scanner._cached_info
            tooltip_text = self._format_cache_age(cached)

            tooltip = Tooltip(
                self.scan_btn,
                tooltip_text,
                theme,
                wraplength=260,
            )
            tooltip.show()
            self.scan_btn._tooltip = tooltip

        def hide_scan_tooltip(event):
            if getattr(self.scan_btn, "_tooltip", None):
                self.scan_btn._tooltip.hide()
                self.scan_btn._tooltip = None

        self.scan_btn.bind("<Enter>", show_scan_tooltip)
        self.scan_btn.bind("<Leave>", hide_scan_tooltip)

        # Hardware info display area on right
        self.info_frame = ttk.Frame(controls_frame)
        self.info_frame.pack(side="left", fill="x", expand=True)

        # Status label
        self.status_label = ttk.Label(
            self.frame,
            text=self.loc._("status_initializing"),
            foreground="gray",
            font=self._get_font(),
        )
        self.status_label.pack(side="top", anchor="w", pady=(10, 0))

        # Game version tabs (below scan controls)
        if self.game_versions:
            self.version_tabs = ttk.Notebook(self.frame)
            for game_version in self.game_versions:
                version_tab = ttk.Frame(self.version_tabs)
                self.version_frames[game_version.flavor_dir] = version_tab
                self.version_tabs.add(version_tab, text=game_version.display_name)
                status_label = ttk.Label(
                    version_tab,
                    text=self.loc._("status_optimized").format("❌"),
                    font=self._get_font("bold"),
                    foreground="red",
                )
                status_label.grid(row=0, column=0, sticky="w", padx=(4, 0), pady=(4, 6))
                self.optimization_status_labels[game_version.flavor_dir] = status_label

                gpu_status_label = ttk.Label(
                    version_tab,
                    text=self.loc._("status_using_gpu").format("—"),
                    font=self._get_font(),
                    foreground="gray",
                )
                gpu_status_label.grid(
                    row=0, column=1, sticky="w", padx=(10, 0), pady=(4, 6)
                )
                self.gpu_status_labels[game_version.flavor_dir] = gpu_status_label
            self.version_tabs.pack(side="top", fill="x", pady=(10, 10))

        # Initially display cached info if available
        self._display_hardware_info()

    def _on_scan_hardware(self):
        """Handle hardware scan button click - always refreshes cache."""
        # Invalidate cache to force fresh scan
        self.scanner._cached_info = None
        if self.scanner.CACHE_FILE.exists():
            self.scanner.CACHE_FILE.unlink()

        self.status_label.config(
            text=self.loc._("status_scanning_hardware"), foreground="blue"
        )
        self.scan_btn.config(state="disabled")
        self.frame.update_idletasks()

        try:
            self.hardware_info = self.scanner.scan()
            if self.hardware_info:
                self._display_hardware_info()
                try:
                    self.status_label.config(
                        text=self.loc._("status_hardware_scan_complete"),
                        foreground="green",
                    )
                except Exception:
                    pass  # Widget may have been destroyed if GPU unsupported

                # Log hardware detection
                if self.logger:
                    info = self.hardware_info

                    # Check if verbose logging is enabled
                    if hasattr(self.logger, "_verbose") and self.logger._verbose:
                        # Verbose mode: log detailed hardware info
                        # CPU
                        if info.cpu_freq_ghz > 0:
                            self.logger.verbose(
                                self.loc._("user_log_verbose_detected_cpu").format(
                                    info.cpu_name, info.cpu_cores, info.cpu_freq_ghz
                                )
                            )
                        else:
                            self.logger.verbose(
                                self.loc._(
                                    "user_log_verbose_detected_cpu_no_freq"
                                ).format(info.cpu_name, info.cpu_cores)
                            )

                        # RAM
                        if info.ram_speed_mhz > 0:
                            self.logger.verbose(
                                self.loc._("user_log_verbose_detected_ram").format(
                                    info.ram_gb, info.ram_speed_mhz
                                )
                            )
                        else:
                            self.logger.verbose(
                                self.loc._(
                                    "user_log_verbose_detected_ram_no_speed"
                                ).format(info.ram_gb)
                            )

                        # GPU(s)
                        for gpu in info.gpus:
                            gpu_type = (
                                self.loc._("msg_hardware_gpu_integrated")
                                if gpu.is_integrated
                                else self.loc._("msg_hardware_gpu_dedicated")
                            )
                            self.logger.verbose(
                                self.loc._("user_log_verbose_detected_gpu").format(
                                    gpu.name, gpu_type
                                )
                            )
                    else:
                        # Non-verbose mode: log normal summary
                        self.logger.log(self.loc._("user_log_normal_hardware_detected"))
            else:
                try:
                    self.status_label.config(
                        text=self.loc._("status_hardware_scan_failed"), foreground="red"
                    )
                except Exception:
                    pass  # Widget may have been destroyed
                if self.logger:
                    self.logger.log(self.loc._("user_log_normal_hardware_scan_failed"))
                    self.logger.error(
                        "Hardware scan returned no results. This typically means psutil is not installed "
                        "or there was an error accessing system information. Check that psutil is installed: "
                        "pip install psutil"
                    )
        except Exception as e:
            try:
                self.status_label.config(
                    text=self.loc._("status_hardware_scan_failed"), foreground="red"
                )
            except Exception:
                pass  # Widget may have been destroyed
            if self.logger:
                self.logger.log(self.loc._("user_log_normal_hardware_scan_failed"))
                self.logger.error(
                    f"Hardware scan encountered an exception: {e}. "
                    f"This may be caused by missing dependencies (psutil, GPUtil, py-cpuinfo) "
                    f"or permission issues accessing system information. "
                    f"Try reinstalling dependencies: pip install psutil GPUtil py-cpuinfo"
                )
        finally:
            try:
                self.scan_btn.config(state="normal")
            except Exception:
                pass  # Widget may have been destroyed

    def _display_hardware_info(self):
        """Display detected hardware information as a vertical list."""
        # Clear existing info
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Check if we have cached info on init
        if self.hardware_info is None:
            self.hardware_info = self.scanner._cached_info

        if self.hardware_info is None:
            no_info_label = ttk.Label(
                self.info_frame,
                text=self.loc._("msg_click_scan_hardware"),
                foreground="gray",
                font=self._get_font(),
            )
            no_info_label.pack(side="top", anchor="w", pady=(0, 5))
            self.status_label.config(
                text=self.loc._("status_initializing"), foreground="gray"
            )
            return

        info = self.hardware_info

        # Update status to indicate cached data is loaded
        self.status_label.config(
            text=self.loc._("status_hardware_scan_complete"), foreground="green"
        )

        # CPU info
        cpu_frame = ttk.Frame(self.info_frame)
        cpu_frame.pack(side="top", anchor="w", pady=(0, 5))

        cpu_label_bold = ttk.Label(
            cpu_frame,
            text=f"• {self.loc._('label_cpu')}",
            font=self._get_font("bold"),
        )
        cpu_label_bold.pack(side="left")

        cpu_value = f"{info.cpu_name} - {self.loc._('msg_hardware_cores').format(info.cpu_cores)}"
        if info.cpu_freq_ghz > 0:
            cpu_value += (
                f" @ {self.loc._('msg_hardware_frequency').format(info.cpu_freq_ghz)}"
            )

        cpu_label_normal = ttk.Label(
            cpu_frame, text=f" {cpu_value}", font=self._get_font()
        )
        cpu_label_normal.pack(side="left")

        # RAM info
        ram_frame = ttk.Frame(self.info_frame)
        ram_frame.pack(side="top", anchor="w", pady=(0, 5))

        ram_label_bold = ttk.Label(
            ram_frame,
            text=f"• {self.loc._('label_ram')}",
            font=self._get_font("bold"),
        )
        ram_label_bold.pack(side="left")

        ram_value = f"{self.loc._('msg_hardware_memory').format(info.ram_gb)}"
        if info.ram_speed_mhz > 0:
            ram_value += (
                f" {self.loc._('msg_hardware_ram_speed').format(info.ram_speed_mhz)}"
            )

        ram_label_normal = ttk.Label(
            ram_frame, text=f" {ram_value}", font=self._get_font()
        )
        ram_label_normal.pack(side="left")

        # GPU info (multiple GPUs possible)
        if info.gpus:
            for idx, gpu in enumerate(info.gpus):
                gpu_frame = ttk.Frame(self.info_frame)
                gpu_frame.pack(side="top", anchor="w", pady=(0, 5))

                gpu_label_bold = ttk.Label(
                    gpu_frame,
                    text=f"• {self.loc._('label_gpu')}",
                    font=self._get_font("bold"),
                )
                gpu_label_bold.pack(side="left")

                gpu_type = (
                    self.loc._("msg_hardware_gpu_integrated")
                    if gpu.is_integrated
                    else self.loc._("msg_hardware_gpu_dedicated")
                )
                gpu_value = f"{gpu.name} {gpu_type}"

                gpu_label_normal = ttk.Label(
                    gpu_frame, text=f" {gpu_value}", font=self._get_font()
                )
                gpu_label_normal.pack(side="left")

        # Configure GPU in Config.wtf after hardware info is displayed
        # This runs both when loading from cache and after fresh scan
        self._on_hardware_loaded()

    def _on_hardware_loaded(self):
        """Called after hardware info is loaded or scanned.

        Configures GPU in Config.wtf files.
        """
        self._configure_gpu()

    def _configure_gpu(self):
        """Configure gxAdapter CVar in all game version Config.wtf files.

        Shows a theme-aware warning dialog if the GPU is unsupported and disables
        the Game Optimizer tab.
        """
        if not self.hardware_info or not self.hardware_info.gpus:
            return

        # Select the best GPU (dedicated preferred)
        gpu_name = select_best_gpu(self.hardware_info.gpus)
        if not gpu_name:
            return

        # Check if GPU is supported (use first game version's flavor for check)
        game_flavor = (
            self.game_versions[0].flavor_dir if self.game_versions else "retail"
        )
        if not is_gpu_supported(gpu_name, game_flavor):
            # GPU is unsupported - show theme-aware warning dialog
            self._show_unsupported_gpu_warning(gpu_name)
            return

        # GPU is supported - update each game version's Config.wtf
        for game_version in self.game_versions:
            config_path = Path(game_version.path) / "WTF" / "Config.wtf"
            try:
                success = update_cvar(config_path, "gxAdapter", gpu_name)
                if success:
                    # Update the GPU status label for this version
                    if game_version.flavor_dir in self.gpu_status_labels:
                        self.gpu_status_labels[game_version.flavor_dir].config(
                            text=self.loc._("status_using_gpu").format(gpu_name),
                            foreground="green",
                        )
                    # Log the change
                    if self.logger:
                        self.logger.log(
                            self.loc._("user_log_normal_gpu_configured").format(
                                game_version.display_name, gpu_name
                            )
                        )
            except Exception as e:
                if self.logger:
                    self.logger.error(
                        f"Failed to update gxAdapter for {game_version.display_name}: {e}"
                    )

    def _show_unsupported_gpu_warning(self, gpu_name: str):
        """Show a theme-aware warning dialog for unsupported GPU.

        Disables the Game Optimizer tab and shows a disabled message.

        Args:
            gpu_name: Name of the unsupported GPU
        """
        # Show themed warning dialog
        theme_name = self.settings.get("theme", "system")
        show_gpu_unsupported_warning(
            self.frame.winfo_toplevel(), self.loc, theme_name, self.settings
        )

        # Disable the Game Optimizer tab
        self._disable_tab_with_message()

        # Log the unsupported GPU
        if self.logger:
            self.logger.log(self.loc._("user_log_normal_gpu_unsupported"))

    def _disable_tab_with_message(self):
        """Disable the Game Optimizer tab and show explanation message."""
        # Find the notebook and this tab's index
        try:
            # Clear the current frame content
            for widget in self.frame.winfo_children():
                widget.destroy()

            # Show disabled message
            disabled_label = ttk.Label(
                self.frame,
                text=self.loc._("tab_game_optimizer_disabled"),
                justify="center",
                font=self._get_font(),
            )
            disabled_label.pack(expand=True, fill="both", padx=20, pady=20)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to disable Game Optimizer tab: {e}")

    def _format_cache_age(self, info):
        """Format cache age as date plus a long-lived relative string."""
        if not info or not getattr(info, "cache_timestamp", None):
            return self.loc._("tooltip_scan_hardware").format(self.loc._("unknown"))

        cache_dt = datetime.fromtimestamp(info.cache_timestamp)
        age_seconds = max(0, datetime.now().timestamp() - info.cache_timestamp)
        age_days = age_seconds / (24 * 60 * 60)

        if age_days < 1:
            age_text = self.loc._("cache_age_under_day")
        elif age_days < 60:
            age_text = self.loc._("cache_age_days").format(int(age_days))
        elif age_days < 365:
            months = max(1, round(age_days / 30))
            age_text = self.loc._("cache_age_months").format(months)
        else:
            years = max(1, round(age_days / 365))
            age_text = self.loc._("cache_age_years").format(years)

        date_format = self.loc._("cache_age_date_format")
        try:
            date_text = cache_dt.strftime(date_format)
        except Exception:
            date_text = cache_dt.strftime("%Y-%m-%d")
        return self.loc._("tooltip_scan_hardware").format(f"{date_text} • {age_text}")

    def _debounced_update_wraplength(self, event=None):
        """Update wraplength for description label with debouncing."""
        if hasattr(self, "_configure_timer"):
            self.frame.after_cancel(self._configure_timer)

        def update():
            self._update_wraplength()

        self._configure_timer = self.frame.after(50, update)

    def _update_wraplength(self, event=None):
        """Update description label wraplength based on current width."""
        if hasattr(self, "desc_label"):
            width = self.desc_label.winfo_width()
            if width > 1:
                self.desc_label.config(wraplength=width - 20)

    def _get_font(self, weight=None):
        """Return a font tuple respecting user-configured family and size."""
        family = self.settings.get("font_family", "TkDefaultFont")
        size = int(self.settings.get("font_size", 12))
        if weight:
            return (family, size, weight)
        return (family, size)
