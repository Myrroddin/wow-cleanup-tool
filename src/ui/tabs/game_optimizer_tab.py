"""Game Optimizer Tab UI for WoW Cleanup Tool."""

from tkinter import ttk
from datetime import datetime
from operations.hardware_scanner import HardwareScanner


class GameOptimizerTab:
    """Game Optimizer tab for hardware detection and optimization suggestions.

    Displays system hardware information (CPU, RAM, GPU) and will eventually
    provide Config.wtf optimization recommendations based on detected hardware.
    """

    def __init__(self, parent, loc, logger=None):
        """Initialize the Game Optimizer tab.

        Args:
            parent: Parent widget
            loc: Localization instance
            logger: Logger instance (optional)
        """
        self.loc = loc
        self.logger = logger
        self.scanner = HardwareScanner()
        self.hardware_info = None

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

        # Hardware info section
        hardware_frame = ttk.LabelFrame(
            self.frame, text=self.loc._("label_hardware_info"), padding=10
        )
        hardware_frame.pack(side="top", fill="both", expand=False, pady=(0, 10))

        # Scan button
        button_frame = ttk.Frame(hardware_frame)
        button_frame.pack(side="top", anchor="w", pady=(0, 10))

        self.scan_btn = ttk.Button(
            button_frame,
            text=self.loc._("btn_scan_hardware"),
            command=self._on_scan_hardware,
        )
        self.scan_btn.pack(side="left", padx=(0, 5))

        self.refresh_btn = ttk.Button(
            button_frame,
            text=self.loc._("btn_refresh_hardware"),
            command=self._on_refresh_hardware,
            state="disabled",
        )
        self.refresh_btn.pack(side="left")

        # Hardware info display area (using grid for alignment)
        self.info_frame = ttk.Frame(hardware_frame)
        self.info_frame.pack(side="top", fill="both", expand=True)

        # Status label
        self.status_label = ttk.Label(
            hardware_frame, text=self.loc._("status_initializing"), foreground="gray"
        )
        self.status_label.pack(side="top", anchor="w", pady=(10, 0))

        # Initially display cached info if available
        self._display_hardware_info()

    def _on_scan_hardware(self):
        """Handle hardware scan button click."""
        self.status_label.config(
            text=self.loc._("status_scanning_hardware"), foreground="blue"
        )
        self.scan_btn.config(state="disabled")
        self.frame.update_idletasks()

        try:
            self.hardware_info = self.scanner.scan()
            if self.hardware_info:
                self._display_hardware_info()
                self.status_label.config(
                    text=self.loc._("status_hardware_scan_complete"), foreground="green"
                )
                self.refresh_btn.config(state="normal")

                if self.logger:
                    self.logger.log("Hardware scan completed successfully")
            else:
                self.status_label.config(
                    text=self.loc._("status_hardware_scan_failed"), foreground="red"
                )
                if self.logger:
                    self.logger.error("Hardware scan returned no results")
        except Exception as e:
            self.status_label.config(
                text=self.loc._("status_hardware_scan_failed"), foreground="red"
            )
            if self.logger:
                self.logger.error(f"Hardware scan failed: {e}")
        finally:
            self.scan_btn.config(state="normal")

    def _on_refresh_hardware(self):
        """Handle refresh button - invalidate cache and rescan."""
        # Invalidate cache
        self.scanner._cached_info = None
        if self.scanner.CACHE_FILE.exists():
            self.scanner.CACHE_FILE.unlink()

        # Rescan
        self._on_scan_hardware()

    def _display_hardware_info(self):
        """Display detected hardware information."""
        # Clear existing info
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Check if we have cached info on init
        if self.hardware_info is None:
            self.hardware_info = self.scanner._cached_info

        if self.hardware_info is None:
            no_info_label = ttk.Label(
                self.info_frame,
                text="Click 'Scan Hardware' to detect your system components",
                foreground="gray",
            )
            no_info_label.pack(side="top", anchor="w", pady=5)
            return

        info = self.hardware_info

        # Calculate cache age
        cache_age_days = (datetime.now().timestamp() - info.cache_timestamp) / (
            24 * 60 * 60
        )
        cache_age_str = ""
        if cache_age_days < 1:
            cache_age_str = self.loc._("msg_hardware_cached").format("< 1")
        else:
            cache_age_str = self.loc._("msg_hardware_cached").format(
                int(cache_age_days)
            )

        # CPU info
        cpu_frame = ttk.Frame(self.info_frame)
        cpu_frame.pack(side="top", fill="x", pady=2)

        cpu_label = ttk.Label(
            cpu_frame, text=self.loc._("label_cpu"), font=("TkDefaultFont", 9, "bold")
        )
        cpu_label.pack(side="left", padx=(0, 5))

        cpu_value = f"{info.cpu_name} - {self.loc._('msg_hardware_cores').format(info.cpu_cores)}"
        if info.cpu_freq_ghz > 0:
            cpu_value += (
                f" @ {self.loc._('msg_hardware_frequency').format(info.cpu_freq_ghz)}"
            )

        cpu_value_label = ttk.Label(cpu_frame, text=cpu_value)
        cpu_value_label.pack(side="left")

        # RAM info
        ram_frame = ttk.Frame(self.info_frame)
        ram_frame.pack(side="top", fill="x", pady=2)

        ram_label = ttk.Label(
            ram_frame, text=self.loc._("label_ram"), font=("TkDefaultFont", 9, "bold")
        )
        ram_label.pack(side="left", padx=(0, 5))

        ram_value = self.loc._("msg_hardware_memory").format(info.ram_gb)
        ram_value_label = ttk.Label(ram_frame, text=ram_value)
        ram_value_label.pack(side="left")

        # GPU info (multiple GPUs possible)
        if info.gpus:
            for idx, gpu in enumerate(info.gpus):
                gpu_frame = ttk.Frame(self.info_frame)
                gpu_frame.pack(side="top", fill="x", pady=2)

                gpu_label_text = self.loc._("label_gpu") if idx == 0 else " "
                gpu_label = ttk.Label(
                    gpu_frame, text=gpu_label_text, font=("TkDefaultFont", 9, "bold")
                )
                gpu_label.pack(side="left", padx=(0, 5))

                gpu_type = (
                    self.loc._("msg_hardware_gpu_integrated")
                    if gpu.is_integrated
                    else self.loc._("msg_hardware_gpu_dedicated")
                )
                gpu_value = f"{gpu.name}"
                if gpu.memory_mb > 0:
                    gpu_value += f" - {self.loc._('msg_hardware_memory').format(gpu.memory_mb // 1024)}"
                gpu_value += f" {gpu_type}"

                gpu_value_label = ttk.Label(gpu_frame, text=gpu_value)
                gpu_value_label.pack(side="left")

        # Cache age indicator
        cache_label = ttk.Label(
            self.info_frame,
            text=cache_age_str,
            foreground="gray",
            font=("TkDefaultFont", 8),
        )
        cache_label.pack(side="top", anchor="w", pady=(10, 0))

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
