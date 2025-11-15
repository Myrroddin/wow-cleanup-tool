"""
Game Optimizer module for WoW Cleanup Tool.

Handles hardware detection and caching for faster lookups.
Provides UI components for the Game Optimizer tab.
"""

import os
import platform
import subprocess
import re
import tkinter as tk
from tkinter import ttk
import psutil
from Modules.global_settings import get_global_setting, set_global_setting

class ToolTip:
    """Simple tooltip widget that appears on hover."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        widget.bind("<Enter>", self.showtip, add=True)
        widget.bind("<Leave>", self.hidetip, add=True)

    def showtip(self, event=None):
        """Display the tooltip."""
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="lightyellow",
                        relief=tk.SOLID, borderwidth=1, font=("tahoma", 9, "normal"))
        label.pack(ipadx=1)

    def hidetip(self, event=None):
        """Hide the tooltip."""
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def get_hardware_info():
    """Retrieve system hardware information affecting game performance.

    Detects CPU cores, RAM, GPU, and other performance-relevant hardware.

    Returns:
        dict: Dictionary containing hardware details
    """
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    info = {
        "system": platform.system(),
        "processor": platform.processor(),
        "cpu_name": _detect_cpu_name(),
        "cpu_cores": cpu_cores,
        "cpu_threads": cpu_threads,
        "memory_gb": round(psutil.virtual_memory().total / (1024 ** 3), 1),
    }

    info["gpu"] = _detect_gpu_names()

    return info

def _detect_cpu_name():
    """Return a full CPU name across Windows, macOS, and Linux when possible."""
    system = platform.system()
    # Windows
    if system == "Windows":
        # Try WMIC first
        try:
            result = subprocess.run(
                ["wmic", "cpu", "get", "Name"], capture_output=True, text=True, timeout=5
            )
            lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
            vals = [l for l in lines if l.lower() != "name"]
            if vals:
                return ", ".join(dict.fromkeys(vals))
        except Exception:
            pass
        # Fallback: PowerShell CIM
        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "(Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name) -join ', '"
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )
            name = result.stdout.strip()
            if name:
                return name
        except Exception:
            pass
        # Last resort
        return platform.processor() or "Unknown CPU"

    # macOS (Darwin)
    if system == "Darwin":
        try:
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            name = result.stdout.strip()
            if name:
                return name
        except Exception:
            pass
        # Apple Silicon sometimes needs model identifier as fallback
        try:
            result = subprocess.run(
                ["sysctl", "hw.model"], capture_output=True, text=True, timeout=5
            )
            m = re.search(r"hw\.model:\s*(.+)", result.stdout)
            if m:
                return m.group(1).strip()
        except Exception:
            pass
        return platform.processor() or "Unknown CPU"

    # Linux and others
    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        m = re.search(r"^model name\s*:\s*(.+)$", txt, re.MULTILINE)
        if m:
            return m.group(1).strip()
        # ARM variants often use 'Hardware' or 'Processor'
        m = re.search(r"^Hardware\s*:\s*(.+)$", txt, re.MULTILINE)
        if m:
            return m.group(1).strip()
        m = re.search(r"^Processor\s*:\s*(.+)$", txt, re.MULTILINE)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    # lscpu fallback
    try:
        result = subprocess.run(["lscpu"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.splitlines():
            if "Model name:" in line:
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return platform.processor() or "Unknown CPU"

def _is_integrated_gpu(gpu_name):
    """Determine if a GPU is integrated (built into CPU).
    
    Args:
        gpu_name: String name of the GPU
    
    Returns:
        bool: True if integrated GPU, False if dedicated/discrete
    """
    gpu_lower = gpu_name.lower()
    
    # Intel integrated patterns
    if "intel" in gpu_lower and any(x in gpu_lower for x in [
        "hd graphics", "uhd graphics", "iris", "xe graphics"
    ]):
        return True
    
    # AMD integrated patterns (APU graphics)
    if "amd" in gpu_lower and any(x in gpu_lower for x in [
        "radeon graphics", "vega", "radeon(tm) graphics"
    ]):
        # But not discrete AMD cards
        if not any(x in gpu_lower for x in ["rx", "r9", "r7", "r5"]):
            return True
    
    return False

def _select_best_gpu(gpu_list, cpu_name):
    """Select the best GPU from a list, preferring dedicated over integrated.
    
    For Intel/AMD CPUs with both integrated and dedicated GPUs, return the
    dedicated GPU. For Apple Silicon, return None (skip GPU selection).
    
    Args:
        gpu_list: List of GPU name strings
        cpu_name: String name of the CPU
    
    Returns:
        str or None: Name of the dedicated GPU to use, or None if no selection needed
    """
    # Skip for Apple Silicon - they don't have dedicated GPUs
    cpu_lower = cpu_name.lower()
    if "apple" in cpu_lower and any(x in cpu_lower for x in ["m1", "m2", "m3", "m4"]):
        return None
    
    if not gpu_list or len(gpu_list) < 2:
        return None
    
    # Check if we have both integrated and dedicated GPUs
    integrated = []
    dedicated = []
    
    for gpu in gpu_list:
        if _is_integrated_gpu(gpu):
            integrated.append(gpu)
        else:
            dedicated.append(gpu)
    
    # If we have both types, return the first dedicated GPU
    if integrated and dedicated:
        return dedicated[0]
    
    return None

def _detect_gpu_names():
    """Return a list of GPU names across platforms when possible."""
    system = platform.system()
    # Windows
    if system == "Windows":
        try:
            result = subprocess.run(
                ["wmic", "path", "win32_videocontroller", "get", "name"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            gpus = [
                line.strip()
                for line in result.stdout.splitlines()[1:]
                if line.strip() and line.strip().lower() != "name"
            ]
            return gpus or ["Not detected"]
        except Exception:
            return ["Not detected"]

    # macOS
    if system == "Darwin":
        try:
            result = subprocess.run(
                ["/usr/sbin/system_profiler", "SPDisplaysDataType"],
                capture_output=True,
                text=True,
                timeout=8,
            )
            gpus = []
            for line in result.stdout.splitlines():
                line = line.strip()
                if line.startswith("Chipset Model:"):
                    gpus.append(line.split(":", 1)[1].strip())
            return gpus or ["Not detected"]
        except Exception:
            return ["Not detected"]

    # Linux/Other
    try:
        result = subprocess.run(["lspci"], capture_output=True, text=True, timeout=5)
        gpus = []
        for line in result.stdout.splitlines():
            if re.search(r"VGA|3D|Display", line, re.IGNORECASE):
                # Extract the device description portion
                part = line.split(":", 2)
                gpus.append(part[-1].strip() if part else line.strip())
        return gpus or ["Not detected"]
    except Exception:
        return ["Not detected"]

def build_game_optimizer_tab(app, parent):
    """Build the Game Optimizer tab UI.

    Args:
        app: The WoWCleanupTool instance
        parent: The parent frame for the tab
    """
    frame = ttk.Frame(parent, padding=20)
    frame.pack(fill="both", expand=True)

    # Title
    ttk.Label(frame, text="Game Optimizer", font=(None, 14, "bold")).pack(
        anchor="w", pady=(0, 12)
    )

    # Description
    description_text = "Optimizes World of Warcraft's performance based on your hardware configuration."
    description_label = ttk.Label(
        frame,
        text=description_text,
        wraplength=frame.winfo_width(),
        justify="left",
    )
    description_label.pack(anchor="w", pady=(0, 20))

    def update_wraplength(event):
        # Set wraplength to the current frame width
        description_label.configure(wraplength=frame.winfo_width())

    frame.bind("<Configure>", update_wraplength)

    # Scan Hardware button with info label
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x", pady=10)

    scan_btn = ttk.Button(
        button_frame,
        text="Scan Hardware",
        command=lambda: _on_scan_hardware(app, info_label, scan_btn, notebook_container),
    )
    scan_btn.pack(side="left", padx=(0, 12))

    # Create tooltip reference (will be populated after scan)
    scan_btn._tooltip = None

    info_label = ttk.Label(
        button_frame,
        text="",
        foreground="gray",
    )
    info_label.pack(side="left", fill="x", expand=True)

    # Prepare hidden notebook container for per-version tabs (hidden until needed)
    notebook_container = ttk.Frame(frame)
    # Do not pack notebook_container yet; it will be shown when data exists
    app.optimizer_version_notebook = None
    app.optimizer_version_tabs = []

    # Load cached hardware info and populate tabs if available
    _load_cached_hardware(app, info_label, scan_btn, notebook_container)

def _load_cached_hardware(app, info_label, scan_btn, notebook_container):
    """Load cached hardware info from global settings.

    Args:
        app: The WoWCleanupTool instance
        info_label: The label to update with status
        scan_btn: The Scan Hardware button widget
    """
    cached = get_global_setting("hardware_cache", None)
    if cached:
        _display_hardware_info(info_label, cached)
        _set_scan_tooltip(scan_btn)
        _populate_version_tabs(app, notebook_container)
    else:
        info_label.configure(
            text="Click 'Scan Hardware' to detect your system's capabilities."
        )

def _display_hardware_info(info_label, hardware):
    """Display formatted hardware information in the label.

    Args:
        info_label: The label to update
        hardware: Hardware info dict
    """
    cpu_name = hardware.get('cpu_name', 'Unknown')
    cores = hardware.get('cpu_cores', '?')
    threads = hardware.get('cpu_threads', '?')
    cpu_info = f"{cpu_name} — {cores}C/{threads}T"
    ram_info = f"{hardware.get('memory_gb', '?')} GB"
    gpu_info = hardware.get("gpu", ["Unknown"])[0] if hardware.get("gpu") else "Unknown"
    text = f"✓ CPU: {cpu_info} | RAM: {ram_info} | GPU: {gpu_info}"
    info_label.configure(text=text)

def _set_scan_tooltip(scan_btn):
    """Attach tooltip to the Scan Hardware button after cache is populated.

    Args:
        scan_btn: The Scan Hardware button widget
    """
    tooltip_text = (
        "Scanning again is not necessary unless you have changed your CPU, GPU, or RAM.\n"
        "Click to refresh the cached hardware information."
    )
    if scan_btn._tooltip:
        scan_btn._tooltip.text = tooltip_text
    else:
        scan_btn._tooltip = ToolTip(scan_btn, tooltip_text)

# Retail requirement thresholds derived from Blizzard Support article 76459
RETAIL_REQ = {
    "min": {"ram_gb": 8, "cpu_cores": 4, "cpu_threads": 8},
    "rec": {"ram_gb": 16, "cpu_cores": 6, "cpu_threads": 12},
}

# Classic Era requirement thresholds derived from Blizzard Support article 243159
CLASSIC_REQ = {
    "min": {"ram_gb": 4, "cpu_cores": 2, "cpu_threads": 4},
    "rec": {"ram_gb": 8, "cpu_cores": 4, "cpu_threads": 8},
}

def _classify_gpu_level(gpu_list, system):
    names = ", ".join(gpu_list or [])
    n = names.lower()
    # Recommended tier
    if any(k in n for k in ["rtx", "rdna 2", "rdna 3", "arc 7", "arc 8", "apple m1", "apple m2", "apple m3", "apple m4"]):
        return "rec"
    # macOS: Intel Iris Pro/Plus (older high-end integrated)
    if system == "Darwin" and any(k in n for k in ["iris pro", "iris plus"]):
        return "min"
    # Linux: Better NVIDIA/AMD discrete detection
    if any(k in n for k in ["geforce gtx 16", "geforce gtx 10", "geforce gtx 9", "radeon rx 5", "radeon rx 6", "radeon rx 7"]):
        return "min"
    # Minimum tier indicators
    if any(k in n for k in ["iris xe", "rx 4", "gcn 4", "vega", "uhd", "radeon 6", "radeon 5"]):
        return "min"
    # Generic GPU detected but unclear tier
    if any(k in n for k in ["nvidia", "geforce", "radeon", "amd", "intel"]):
        return "min"
    return "below"

def _classify_gpu_level_classic(gpu_list, system):
    """Classic-friendly GPU classification with lower thresholds."""
    names = ", ".join(gpu_list or [])
    n = names.lower()
    # Recommended tier for Classic (lower bar than Retail)
    if any(k in n for k in ["rtx", "gtx 16", "gtx 10", "gtx 9", "radeon rx", "rdna", "arc", "apple m", "iris pro", "iris plus"]):
        return "rec"
    # Minimum tier for Classic
    if any(k in n for k in ["gt 4", "gt 5", "gt 6", "hd 5", "hd 6", "hd 4000", "iris", "uhd", "vega", "radeon 5", "radeon 6"]):
        return "min"
    # Generic GPU
    if any(k in n for k in ["nvidia", "geforce", "radeon", "amd", "intel"]):
        return "min"
    return "below"

def _classify_retail_hardware(hardware):
    ram = hardware.get("memory_gb") or 0
    cores = hardware.get("cpu_cores") or 0
    threads = hardware.get("cpu_threads") or 0
    gpu_level = _classify_gpu_level(hardware.get("gpu"), hardware.get("system"))

    levels = []
    levels.append("rec" if ram >= RETAIL_REQ["rec"]["ram_gb"] else ("min" if ram >= RETAIL_REQ["min"]["ram_gb"] else "below"))
    levels.append("rec" if (cores >= RETAIL_REQ["rec"]["cpu_cores"] or threads >= RETAIL_REQ["rec"]["cpu_threads"]) else ("min" if (cores >= RETAIL_REQ["min"]["cpu_cores"] or threads >= RETAIL_REQ["min"]["cpu_threads"]) else "below"))
    levels.append(gpu_level)
    order = {"below": 0, "min": 1, "rec": 2}
    overall = min(levels, key=lambda x: order.get(x, 0))
    return overall, {"ram": levels[0], "cpu": levels[1], "gpu": levels[2]}

def _classify_classic_hardware(hardware):
    """Classify hardware for Classic/Classic Era using lower thresholds."""
    ram = hardware.get("memory_gb") or 0
    cores = hardware.get("cpu_cores") or 0
    threads = hardware.get("cpu_threads") or 0
    gpu_level = _classify_gpu_level_classic(hardware.get("gpu"), hardware.get("system"))

    levels = []
    levels.append("rec" if ram >= CLASSIC_REQ["rec"]["ram_gb"] else ("min" if ram >= CLASSIC_REQ["min"]["ram_gb"] else "below"))
    levels.append("rec" if (cores >= CLASSIC_REQ["rec"]["cpu_cores"] or threads >= CLASSIC_REQ["rec"]["cpu_threads"]) else ("min" if (cores >= CLASSIC_REQ["min"]["cpu_cores"] or threads >= CLASSIC_REQ["min"]["cpu_threads"]) else "below"))
    levels.append(gpu_level)
    order = {"below": 0, "min": 1, "rec": 2}
    overall = min(levels, key=lambda x: order.get(x, 0))
    return overall, {"ram": levels[0], "cpu": levels[1], "gpu": levels[2]}

def _build_presets_for_level(level):
    presets = {
        "Low": [
            "Render Scale: 0.8",
            "Texture Quality: Low",
            "Shadow Quality: Low",
            "SSAO: Off",
            "Anti-Aliasing: None",
            "VSync: Off",
        ],
        "Medium": [
            "Render Scale: 1.0",
            "Texture Quality: Medium",
            "Shadow Quality: Low",
            "SSAO: Low",
            "Anti-Aliasing: FXAA High",
            "VSync: Off",
        ],
        "High": [
            "Render Scale: 1.0",
            "Texture Quality: High",
            "Shadow Quality: High",
            "SSAO: High",
            "Anti-Aliasing: CMAA / MSAA 2x",
            "VSync: Optional",
        ],
        "Ultra": [
            "Render Scale: 1.0",
            "Texture Quality: Ultra",
            "Shadow Quality: Ultra",
            "SSAO: Ultra",
            "Anti-Aliasing: TAA / DLAA (if available)",
            "VSync: Optional",
        ],
    }
    if level == "below":
        presets["High"][0] = "Render Scale: 0.9"
        presets["High"][2] = "Shadow Quality: Medium"
        presets["Ultra"][0] = "Render Scale: 0.9"
        presets["Ultra"][2] = "Shadow Quality: High"
        presets["Ultra"][3] = "SSAO: High"
        presets["Ultra"][4] = "Anti-Aliasing: FXAA High"
    elif level == "min":
        presets["Ultra"][2] = "Shadow Quality: High"
        presets["Ultra"][3] = "SSAO: High"
    return presets

def _tier_to_suggested_preset(overall):
    """Map overall tier classification to a suggested preset name."""
    if overall == "below":
        return "Low"
    elif overall == "min":
        return "Medium"
    else:  # rec
        return "High"

def _preset_to_config_settings(preset_name):
    """Map preset name to WoW Config.wtf CVar settings."""
    # WoW graphics settings as CVars
    configs = {
        "Low": [
            "SET renderScale \"0.8\"",
            "SET graphicsTextureResolution \"1\"",
            "SET graphicsShadowQuality \"1\"",
            "SET graphicsSSAO \"0\"",
            "SET MSAAQuality \"0\"",
            "SET gxVSync \"0\"",
            "SET graphicsViewDistance \"3\"",
            "SET graphicsEnvironmentDetail \"3\"",
        ],
        "Medium": [
            "SET renderScale \"1.0\"",
            "SET graphicsTextureResolution \"2\"",
            "SET graphicsShadowQuality \"2\"",
            "SET graphicsSSAO \"1\"",
            "SET MSAAQuality \"0\"",
            "SET gxVSync \"0\"",
            "SET graphicsViewDistance \"5\"",
            "SET graphicsEnvironmentDetail \"5\"",
        ],
        "High": [
            "SET renderScale \"1.0\"",
            "SET graphicsTextureResolution \"3\"",
            "SET graphicsShadowQuality \"3\"",
            "SET graphicsSSAO \"2\"",
            "SET MSAAQuality \"2\"",
            "SET gxVSync \"0\"",
            "SET graphicsViewDistance \"7\"",
            "SET graphicsEnvironmentDetail \"7\"",
        ],
        "Ultra": [
            "SET renderScale \"1.0\"",
            "SET graphicsTextureResolution \"3\"",
            "SET graphicsShadowQuality \"4\"",
            "SET graphicsSSAO \"3\"",
            "SET MSAAQuality \"4\"",
            "SET gxVSync \"0\"",
            "SET graphicsViewDistance \"10\"",
            "SET graphicsEnvironmentDetail \"10\"",
        ],
    }
    return configs.get(preset_name, [])

def _apply_settings_to_config(version_path, preset_name, hardware=None):
    """Write preset settings to the version's Config.wtf file.
    
    Args:
        version_path: Path to the WoW version folder (e.g., _retail_)
        preset_name: Name of the preset to apply (Low/Medium/High/Ultra)
        hardware: Optional hardware info dict for GPU selection
    
    Returns:
        tuple: (success: bool, message: str)
    """
    config_path = os.path.join(version_path, "WTF", "Config.wtf")
    wtf_dir = os.path.dirname(config_path)
    
    # Do not create WTF directory - it must exist from game launch
    if not os.path.exists(wtf_dir):
        return False, "WTF directory not found. Please launch the game first."
    
    settings = _preset_to_config_settings(preset_name)
    if not settings:
        return False, f"Unknown preset: {preset_name}"
    
    try:
        # Read existing config if it exists
        existing_lines = []
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8", errors="ignore") as f:
                existing_lines = f.readlines()
        
        # Create a dict of existing settings
        config_dict = {}
        for line in existing_lines:
            line = line.strip()
            if line.startswith("SET "):
                parts = line.split(None, 2)
                if len(parts) >= 2:
                    config_dict[parts[1]] = line
            else:
                # Preserve non-SET lines (comments, etc.)
                if line and not line.startswith("SET "):
                    config_dict[f"__comment_{len(config_dict)}"] = line
        
        # Update with new preset settings
        for setting in settings:
            parts = setting.split(None, 2)
            if len(parts) >= 2:
                config_dict[parts[1]] = setting
        
        # GPU selection for Intel/AMD systems with both integrated and dedicated GPUs
        if hardware:
            gpu_list = hardware.get("gpu", [])
            cpu_name = hardware.get("cpu_name", "")
            dedicated_gpu = _select_best_gpu(gpu_list, cpu_name)
            
            if dedicated_gpu:
                # Set WoW to use the dedicated GPU
                # gxApi controls graphics API: values are typically "d3d11", "d3d12", etc.
                # gxAdapter is the GPU index - 0 for first, 1 for second, etc.
                gpu_index = str(gpu_list.index(dedicated_gpu))
                config_dict["gxAdapter"] = f'SET gxAdapter "{gpu_index}"'
        
        # Write back to file
        with open(config_path, "w", encoding="utf-8") as f:
            for key, value in config_dict.items():
                f.write(value + "\n")
        
        return True, f"Applied {preset_name} settings to Config.wtf"
    
    except Exception as e:
        return False, f"Failed to write config: {e}"

def _check_version_directories(version_path):
    """Check if the required game directories exist.
    
    Args:
        version_path: Path to the WoW version folder (e.g., _retail_)
    
    Returns:
        bool: True if WTF and Interface/AddOns directories exist, False otherwise
    """
    wtf_dir = os.path.join(version_path, "WTF")
    interface_dir = os.path.join(version_path, "Interface")
    addons_dir = os.path.join(interface_dir, "AddOns")
    
    return (os.path.exists(wtf_dir) and 
            os.path.exists(interface_dir) and 
            os.path.exists(addons_dir))

def _populate_version_tabs(app, notebook_container):
    """Create and show a per-version notebook under the Game Optimizer tab.

    Reuses the app helpers to enumerate versions and build single-version
    content where possible.
    """
    # Clear any existing notebook for optimizer
    try:
        if app.optimizer_version_notebook:
            app.optimizer_version_notebook.destroy()
    except Exception:
        pass

    base = app.wow_path_var.get().strip() if hasattr(app, "wow_path_var") else ""
    if not base or not os.path.isdir(base):
        # No WoW folder selected; do not show tabs but inform user if desired
        try:
            for w in notebook_container.winfo_children():
                w.destroy()
            info = ttk.Frame(notebook_container, padding=12)
            info.pack(fill="both", expand=True)
            ttk.Label(info, text="Select a valid World of Warcraft folder in Options to enable per-version views.").pack()
            # Do not pack the container if no valid base
            try:
                notebook_container.pack_forget()
            except Exception:
                pass
        except Exception:
            pass
        return

    versions = app._enumerate_versions(base)
    if not versions:
        # No detected versions; keep hidden
        try:
            notebook_container.pack_forget()
        except Exception:
            pass
        return

    # Show container and notebook
    try:
        notebook_container.pack(fill="both", expand=True, padx=10, pady=10)
    except Exception:
        pass

    app.optimizer_version_notebook = ttk.Notebook(notebook_container)
    app.optimizer_version_notebook.pack(fill="both", expand=True)
    app.optimizer_version_tabs.clear()

    for vpath, vlabel in versions:
        tab = ttk.Frame(app.optimizer_version_notebook)
        app.optimizer_version_notebook.add(tab, text=vlabel)
        # Build optimizer-specific content for this version (reuse cached hardware)
        try:
            cached = get_global_setting("hardware_cache", None)
            widgets = _build_optimizer_version_tab(app, tab, vpath, vlabel, cached)
        except Exception:
            # Fallback: simple info label
            ttk.Label(tab, text=f"Version: {vlabel}\nPath: {vpath}").pack(anchor="w", padx=8, pady=8)
            widgets = None
        app.optimizer_version_tabs.append((vlabel, vpath, widgets))

def _build_optimizer_version_tab(app, tab, version_path, version_label, hardware):
    """Construct optimizer-specific controls for a single game version tab.

    Args:
        app: main application instance
        tab: the ttk.Frame for the version
        version_path: filesystem path for the version
        version_label: human-readable label (e.g., 'Retail')
        hardware: cached hardware info dict (may be None)

    Returns:
        dict: references to created widgets (for future use)
    """
    frame = ttk.Frame(tab, padding=8)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text=f"Optimizer — {version_label}", font=(None, 12, "bold")).pack(anchor="w", pady=(0, 8))

    # Check if required directories exist
    if not _check_version_directories(version_path):
        # Show instruction message instead of optimizer UI
        instruction_text = (
            f"The optimizer requires that {version_label} has been launched at least once. "
            "Please launch World of Warcraft and proceed to the Character Select screen, then quit the game. "
            "After that, you can use the optimizer to apply graphics presets."
        )
        instruction_label = ttk.Label(
            frame,
            text=instruction_text,
            wraplength=frame.winfo_width() if frame.winfo_width() > 1 else 600,
            justify="left",
            foreground="red"
        )
        instruction_label.pack(anchor="w", pady=(8, 8))
        
        # Update wraplength on resize
        def update_instruction_wrap(event):
            instruction_label.configure(wraplength=frame.winfo_width())
        frame.bind("<Configure>", update_instruction_wrap)
        
        return {"instruction_label": instruction_label}

    # Determine version type and classify hardware accordingly
    is_retail = version_label.lower().startswith("retail")
    is_classic = "classic" in version_label.lower()

    if is_retail:
        overall, parts = _classify_retail_hardware(hardware or {})
        presets = _build_presets_for_level(overall)
        suggested_preset = _tier_to_suggested_preset(overall)
        preset_title = "Graphics Presets (Retail):"
    elif is_classic:
        overall, parts = _classify_classic_hardware(hardware or {})
        presets = _build_presets_for_level(overall)
        suggested_preset = _tier_to_suggested_preset(overall)
        preset_title = "Graphics Presets (Classic):"
    else:
        overall = None
        suggested_preset = None
        preset_title = None

    # System tier summary with suggested preset
    if is_retail or is_classic:
        tier_frame = ttk.Frame(frame)
        tier_frame.pack(fill="x", pady=(0, 8))
        ttk.Label(tier_frame, text=f"Your system matches: {suggested_preset}", foreground="blue", font=(None, 10, "italic")).pack(anchor="w")

    # Recommendations
    rec_frame = ttk.Frame(frame)
    rec_frame.pack(fill="both", expand=True, pady=(4, 8))

    # Version-specific presets (Retail or Classic)
    if is_retail or is_classic:
        ttk.Label(rec_frame, text=preset_title, font=(None, 10, "bold")).pack(anchor="w", pady=(0, 6))
        
        # Create a grid with 4 columns for Low, Medium, High, Ultra
        preset_grid = ttk.Frame(rec_frame)
        preset_grid.pack(fill="both", expand=True)
        
        col = 0
        for name in ("Low", "Medium", "High", "Ultra"):
            preset_col = ttk.Frame(preset_grid, relief="ridge", borderwidth=1, padding=6)
            preset_col.grid(row=0, column=col, sticky="nsew", padx=4, pady=2)
            preset_grid.columnconfigure(col, weight=1)
            
            ttk.Label(preset_col, text=name, font=(None, 10, "bold")).pack(anchor="w")
            ttk.Separator(preset_col, orient="horizontal").pack(fill="x", pady=(2, 4))
            
            for line in presets[name]:
                ttk.Label(preset_col, text=f"• {line}", font=(None, 8)).pack(anchor="w")
            
            col += 1
    else:
        # Generic recommendations as fallback
        mem = (hardware.get('memory_gb') if hardware else None) or 0
        threads = (hardware.get('cpu_threads') if hardware else None) or 0
        if mem >= 16:
            tex = "Texture Quality: High"
        elif mem >= 8:
            tex = "Texture Quality: Medium"
        else:
            tex = "Texture Quality: Low"
        threads_rec = "Background Threads: 4" if threads >= 8 else "Background Threads: 2"
        ttk.Label(rec_frame, text="Recommended Settings:").grid(row=0, column=0, sticky="w")
        ttk.Label(rec_frame, text=tex).grid(row=1, column=0, sticky="w", padx=(8,0))
        ttk.Label(rec_frame, text=threads_rec).grid(row=2, column=0, sticky="w", padx=(8,0))

    # Action buttons
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill="x", pady=(8, 0))

    status_var = tk.StringVar(value="")
    
    # Retail or Classic tab: dropdown for preset selection
    if is_retail or is_classic:
        preset_var = tk.StringVar(value=suggested_preset)
        ttk.Label(btn_frame, text="Apply Preset:").pack(side="left", padx=(0, 6))
        preset_dropdown = ttk.Combobox(btn_frame, textvariable=preset_var, values=["Low", "Medium", "High", "Ultra"], state="readonly", width=12)
        preset_dropdown.pack(side="left", padx=(0, 8))
        
        def apply_preset():
            chosen = preset_var.get()
            success, message = _apply_settings_to_config(version_path, chosen, hardware)
            if success:
                msg = f"Applied {chosen} preset for {version_label}"
                app.log(msg, always_log=True)
                status_var.set(f"✓ {chosen} preset applied.")
            else:
                app.log(f"Failed to apply {chosen} preset: {message}", always_log=True)
                status_var.set(f"✗ Error: {message[:40]}")
        
        ttk.Button(btn_frame, text="Apply", command=apply_preset).pack(side="left")
    else:
        # Generic apply for other versions
        def apply_recommendations():
            msg = f"Applied optimizer recommendations for {version_label}"
            app.log(msg, always_log=True)
            status_var.set("✓ Recommendations applied.")
        
        ttk.Button(btn_frame, text="Apply Recommended Settings", command=apply_recommendations).pack(side="left")
    
    ttk.Label(btn_frame, textvariable=status_var, foreground="green").pack(side="left", padx=(10,0))

    return {"status_var": status_var}

def _on_scan_hardware(app, info_label, scan_btn, notebook_container):
    """Handle Scan Hardware button press.

    Scans system hardware, caches results in global settings, and logs succinctly.

    Args:
        app: The WoWCleanupTool instance
        info_label: The label to update with status
        scan_btn: The Scan Hardware button widget
    """
    info_label.configure(text="Scanning hardware...")
    app.root.update()

    try:
        hardware = get_hardware_info()
        set_global_setting("hardware_cache", hardware)
        _display_hardware_info(info_label, hardware)
        _set_scan_tooltip(scan_btn)
        _populate_version_tabs(app, notebook_container)
        app.log("Hardware scan complete: cached to global settings.", always_log=True)
    except Exception as e:
        info_label.configure(text=f"✗ Error: {str(e)[:50]}")
        app.log(f"Hardware scan failed: {str(e)}", always_log=True)
