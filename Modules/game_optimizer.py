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
from concurrent.futures import ThreadPoolExecutor
import psutil
from Modules.global_settings import get_global_setting, set_global_setting
from Modules.ui_helpers import Tooltip
from Modules import localization

def get_hardware_info():
    """Retrieve system hardware information affecting game performance.

    Detects CPU cores, RAM, GPU, and other performance-relevant hardware.
    CPU and GPU detection run in parallel for faster results.

    Returns:
        dict: Dictionary containing hardware details
    """
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    
    # Run CPU and GPU detection in parallel (both are I/O-bound subprocess calls)
    with ThreadPoolExecutor(max_workers=2) as executor:
        cpu_future = executor.submit(_detect_cpu_name)
        gpu_future = executor.submit(_detect_gpu_names)
        cpu_name = cpu_future.result()
        gpu_list = gpu_future.result()
    
    # Check if GPU was switched from integrated to discrete
    selected_gpu, original_gpu = _select_best_gpu(gpu_list, cpu_name)
    
    info = {
        "system": platform.system(),
        "processor": platform.processor(),
        "cpu_name": cpu_name,
        "cpu_cores": cpu_cores,
        "cpu_threads": cpu_threads,
        "memory_gb": round(psutil.virtual_memory().total / (1024 ** 3), 1),
        "gpu": gpu_list,
        "gpu_selected": selected_gpu,
        "gpu_original": original_gpu,
    }

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
        return platform.processor() or localization._("unknown_cpu")

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
        return platform.processor() or localization._("unknown_cpu")

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
    return platform.processor() or localization._("unknown_cpu")

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
        "radeon graphics", "vega", "radeon(tm) graphics", "radeon™ graphics"
    ]):
        # But not discrete AMD cards (RX series, older R9/R7/R5 series)
        if not any(x in gpu_lower for x in ["rx ", "r9 ", "r7 ", "r5 ", "rx4", "rx5", "rx6", "rx7"]):
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
        tuple: (selected_gpu, original_gpu) where selected_gpu is the GPU to use,
               original_gpu is the first GPU in the list (usually integrated),
               or (None, None) if no selection needed
    """
    # Skip for Apple Silicon - they don't have dedicated GPUs
    cpu_lower = cpu_name.lower()
    if "apple" in cpu_lower and any(x in cpu_lower for x in ["m1", "m2", "m3", "m4"]):
        return None, None
    
    if not gpu_list or len(gpu_list) < 2:
        return None, None
    
    # Check if we have both integrated and dedicated GPUs
    integrated = []
    dedicated = []
    
    for gpu in gpu_list:
        if _is_integrated_gpu(gpu):
            integrated.append(gpu)
        else:
            dedicated.append(gpu)
    
    # If we have both types, return the first dedicated GPU and the first integrated
    if integrated and dedicated:
        return dedicated[0], integrated[0]
    
    return None, None

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
            return gpus or [localization._("not_detected")]
        except Exception:
            return [localization._("not_detected")]

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
            return gpus or [localization._("not_detected")]
        except Exception:
            return [localization._("not_detected")]

    # Linux/Other
    try:
        result = subprocess.run(["lspci"], capture_output=True, text=True, timeout=5)
        gpus = []
        for line in result.stdout.splitlines():
            if re.search(r"VGA|3D|Display", line, re.IGNORECASE):
                # Extract the device description portion
                part = line.split(":", 2)
                gpus.append(part[-1].strip() if part else line.strip())
        return gpus or [localization._("not_detected")]
    except Exception:
        return [localization._("not_detected")]

def build_game_optimizer_tab(app, parent):
    """Build the Game Optimizer tab UI.

    Args:
        app: The WoWCleanupTool instance
        parent: The parent frame for the tab
    """
    frame = ttk.Frame(parent, padding=20)
    frame.pack(fill="both", expand=True)

    # Title
    ttk.Label(frame, text=localization._("game_optimizer_title"), font=(None, 14, "bold")).pack(
        anchor="w", pady=(0, 12)
    )

    # Description
    description_text = localization._("game_optimizer_desc")
    description_label = ttk.Label(
        frame,
        text=description_text,
        wraplength=max(200, frame.winfo_width() - 40),
        justify="left",
    )
    description_label.pack(anchor="w", pady=(0, 20))

    def update_wraplength(event):
        # Set wraplength with margin to prevent text cutoff
        description_label.configure(wraplength=max(200, frame.winfo_width() - 40))

    frame.bind("<Configure>", update_wraplength)

    # Scan Hardware button with info label
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x", pady=10)

    scan_btn = ttk.Button(
        button_frame,
        text=localization._("scan_hardware"),
        command=lambda: _on_scan_hardware(app, info_label, gpu_switch_label, scan_btn, notebook_container),
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

    # GPU switch notification label (shown when GPU is switched)
    gpu_switch_label = ttk.Label(
        frame,
        text="",
        foreground="blue",
        wraplength=max(200, frame.winfo_width() - 40),
        justify="left",
    )
    gpu_switch_label.pack(anchor="w", pady=(0, 10))
    
    # Update wraplength on resize
    def update_gpu_switch_wraplength(event):
        gpu_switch_label.configure(wraplength=max(200, frame.winfo_width() - 40))
    frame.bind("<Configure>", update_gpu_switch_wraplength, add="+")

    # Prepare hidden notebook container for per-version tabs (hidden until needed)
    notebook_container = ttk.Frame(frame)
    # Do not pack notebook_container yet; it will be shown when data exists
    app.optimizer_version_notebook = None
    app.optimizer_version_tabs = []

    # Load cached hardware info and populate tabs if available
    _load_cached_hardware(app, info_label, gpu_switch_label, scan_btn, notebook_container)

def _load_cached_hardware(app, info_label, gpu_switch_label, scan_btn, notebook_container):
    """Load cached hardware info from global settings.

    Args:
        app: The WoWCleanupTool instance
        info_label: The label to update with status
        gpu_switch_label: The label to display GPU switch notification
        scan_btn: The Scan Hardware button widget
    """
    cached = get_global_setting("hardware_cache", None)
    if cached:
        _display_hardware_info(info_label, cached)
        _display_gpu_switch_info(gpu_switch_label, cached)
        _set_scan_tooltip(scan_btn)
        _populate_version_tabs(app, notebook_container)
    else:
        info_label.configure(
            text=localization._("click_scan_hardware")
        )

def _display_hardware_info(info_label, hardware):
    """Display formatted hardware information in the label.

    Args:
        info_label: The label to update
        hardware: Hardware info dict
    """
    cpu_name = hardware.get('cpu_name', localization._("unknown_gpu"))
    cores = hardware.get('cpu_cores', '?')
    threads = hardware.get('cpu_threads', '?')
    cpu_info = f"{cpu_name} — {cores}C/{threads}T"
    ram_info = f"{hardware.get('memory_gb', '?')} GB"
    gpu_info = hardware.get("gpu", [localization._("unknown_gpu")])[0] if hardware.get("gpu") else localization._("unknown_gpu")
    text = localization._("hardware_detected").format(cpu_info, ram_info, gpu_info)
    info_label.configure(text=text)

def _display_gpu_switch_info(gpu_switch_label, hardware):
    """Display GPU switch notification if applicable.
    
    Args:
        gpu_switch_label: The label to update with GPU switch info
        hardware: Hardware info dict
    """
    gpu_selected = hardware.get("gpu_selected")
    gpu_original = hardware.get("gpu_original")
    
    if gpu_selected and gpu_original:
        text = localization._("gpu_switch_notification").format(gpu_selected, gpu_original)
        gpu_switch_label.configure(text=text)
    else:
        gpu_switch_label.configure(text="")

def _set_scan_tooltip(scan_btn):
    """Attach tooltip to the Scan Hardware button after cache is populated.

    Args:
        scan_btn: The Scan Hardware button widget
    """
    tooltip_text = localization._("scan_tooltip_refresh")
    if scan_btn._tooltip:
        scan_btn._tooltip.text = tooltip_text
    else:
        scan_btn._tooltip = Tooltip(scan_btn, tooltip_text)

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

def _read_current_config(version_path):
    """Read current Config.wtf and return dict of setting name -> value.
    
    Args:
        version_path: Path to the WoW version folder
        
    Returns:
        dict: Mapping of setting names to their current values
    """
    config_path = os.path.join(version_path, "WTF", "Config.wtf")
    config_dict = {}
    
    if not os.path.exists(config_path):
        return config_dict
    
    try:
        with open(config_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("SET "):
                    parts = line.split(None, 2)
                    if len(parts) >= 3:
                        setting_name = parts[1]
                        # Extract value, removing quotes
                        value = parts[2].strip('"')
                        config_dict[setting_name] = value
    except Exception:
        pass
    
    return config_dict

def _get_recommended_performance_settings(hardware):
    """Get recommended performance settings based on hardware that may not be in presets.
    
    Args:
        hardware: Hardware info dict
        
    Returns:
        list: List of recommended CVar settings for performance
    """
    recommendations = []
    
    if not hardware:
        return recommendations
    
    threads = hardware.get('cpu_threads', 0)
    cores = hardware.get('cpu_cores', 0)
    ram_gb = hardware.get('memory_gb', 0)
    
    # Threaded optimization
    if threads >= 12:
        recommendations.append('SET processAffinityMask "255"')  # Use all cores
        recommendations.append('SET graphicsMultisampleMode "4"')  # Better quality
    elif threads >= 8:
        recommendations.append('SET processAffinityMask "15"')  # Use 4 cores
    
    # Physics and multithreading
    if cores >= 6:
        recommendations.append('SET physicsInteractionLimit "60"')  # More physics objects
    
    # Spell density based on GPU tier (if available)
    gpu_list = hardware.get('gpu', [])
    if gpu_list:
        # High-end GPUs: full spell effects
        recommendations.append('SET spellClutter "160"')  # Full spell density
        recommendations.append('SET particleDensity "100"')  # Max particles
    
    # Network and cache settings
    recommendations.append('SET M2Faster "1"')  # Faster model loading
    recommendations.append('SET textureFilteringMode "5"')  # Trilinear filtering
    
    return recommendations

def _create_config_backup(config_path):
    """Create a timestamped backup of Config.wtf file.
    
    Args:
        config_path: Path to the Config.wtf file
        
    Returns:
        tuple: (success: bool, backup_path: str or None)
    """
    if not os.path.exists(config_path):
        return True, None
    
    try:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = f"{config_path}.backup.{timestamp}"
        
        # Copy the file
        import shutil
        shutil.copy2(config_path, backup_path)
        
        # Clean up old backups (keep only last 5)
        backup_dir = os.path.dirname(config_path)
        backup_files = sorted(
            [f for f in os.listdir(backup_dir) if f.startswith("Config.wtf.backup.")],
            reverse=True
        )
        for old_backup in backup_files[5:]:
            try:
                os.remove(os.path.join(backup_dir, old_backup))
            except Exception:
                pass
        
        return True, backup_path
    except Exception as e:
        return False, str(e)

def _check_wow_running():
    """Check if World of Warcraft is currently running.
    
    Returns:
        bool: True if WoW is running, False otherwise
    """
    try:
        import psutil
        wow_processes = ["Wow.exe", "WowClassic.exe", "World of Warcraft.exe", "Wow-64.exe"]
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] in wow_processes:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
    except Exception:
        return False

def _save_optimization_history(version_path, version_label, preset_name, changes):
    """Save optimization change to history file.
    
    Args:
        version_path: Path to the WoW version folder
        version_label: Version label (e.g., 'Retail')
        preset_name: Preset that was applied
        changes: Dict with 'updated' and 'added' lists
    """
    try:
        import datetime
        import json
        
        history_file = os.path.join(version_path, "WTF", "optimization_history.json")
        
        # Load existing history
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                pass
        
        # Add new entry
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "version": version_label,
            "preset": preset_name,
            "updated": len(changes.get("updated", [])),
            "added": len(changes.get("added", [])),
            "total": len(changes.get("updated", [])) + len(changes.get("added", []))
        }
        history.append(entry)
        
        # Keep only last 20 entries
        history = history[-20:]
        
        # Save history
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass

def _get_optimization_history(version_path):
    """Load optimization history from file.
    
    Args:
        version_path: Path to the WoW version folder
        
    Returns:
        list: List of history entries
    """
    try:
        import json
        history_file = os.path.join(version_path, "WTF", "optimization_history.json")
        if os.path.exists(history_file):
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []

def _get_preset_performance_estimate(preset_name, hardware):
    """Estimate performance impact of a preset.
    
    Args:
        preset_name: Name of the preset (Low/Medium/High/Ultra)
        hardware: Hardware info dict
        
    Returns:
        str: Performance impact description
    """
    if not hardware:
        return localization._("perf_depends_hardware")
    
    # Classify hardware
    ram = hardware.get("memory_gb", 0)
    threads = hardware.get("cpu_threads", 0)
    gpu_list = hardware.get("gpu", [])
    gpu_name = ", ".join(gpu_list).lower()
    
    # Determine if hardware is high-end
    is_high_end = threads >= 12 and ram >= 16 and any(k in gpu_name for k in ["rtx", "rdna 3", "rdna 2"])
    is_mid_range = threads >= 8 and ram >= 12
    
    # Map preset names to translation key prefixes
    preset_key = preset_name.lower()
    tier = "high" if is_high_end else ("mid" if is_mid_range else "low")
    
    # Build translation key: {preset}_perf_{tier}
    translation_key = f"{preset_key}_perf_{tier}"
    return localization._(translation_key)

def _apply_settings_to_config(version_path, preset_name, hardware=None):
    """Write preset settings to the version's Config.wtf file.
    
    Args:
        version_path: Path to the WoW version folder (e.g., _retail_)
        preset_name: Name of the preset to apply (Low/Medium/High/Ultra)
        hardware: Optional hardware info dict for GPU selection
    
    Returns:
        tuple: (success: bool, message: str, changes_summary: dict or None)
    """
    config_path = os.path.join(version_path, "WTF", "Config.wtf")
    wtf_dir = os.path.dirname(config_path)
    
    # Do not create WTF directory - it must exist from game launch
    if not os.path.exists(wtf_dir):
        return False, localization._("wtf_not_found"), None
    
    settings = _preset_to_config_settings(preset_name)
    if not settings:
        return False, localization._("unknown_preset").format(preset_name), None
    
    # Create backup before making changes
    backup_success, backup_info = _create_config_backup(config_path)
    if not backup_success:
        return False, localization._("backup_failed").format(backup_info), None
    
    try:
        # Track changes for summary
        changes_made = {"updated": [], "added": []}
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
                setting_name = parts[1]
                if setting_name in config_dict:
                    changes_made["updated"].append(setting_name)
                else:
                    changes_made["added"].append(setting_name)
                config_dict[setting_name] = setting
        
        # Add recommended performance settings
        if hardware:
            recommended_settings = _get_recommended_performance_settings(hardware)
            for setting in recommended_settings:
                parts = setting.split(None, 2)
                if len(parts) >= 2:
                    setting_name = parts[1]
                    if setting_name not in config_dict:
                        changes_made["added"].append(setting_name)
                    config_dict[setting_name] = setting
        
        # GPU selection for Intel/AMD systems with both integrated and dedicated GPUs
        if hardware:
            gpu_list = hardware.get("gpu", [])
            cpu_name = hardware.get("cpu_name", "")
            dedicated_gpu, _ = _select_best_gpu(gpu_list, cpu_name)
            
            # Only set adapter on Windows builds
            if dedicated_gpu and platform.system() == "Windows":
                gpu_index = str(gpu_list.index(dedicated_gpu))
                config_dict["gxAdapter"] = f'SET gxAdapter "{gpu_index}"'
        
        # Write back to file
        with open(config_path, "w", encoding="utf-8") as f:
            for key, value in config_dict.items():
                f.write(value + "\n")
        
        # Build summary message
        summary_msg = localization._("config_updated").format(preset_name)
        summary_msg += localization._("settings_updated_added").format(len(changes_made['updated']), len(changes_made['added']))
        if backup_info:
            summary_msg += localization._("backup_saved")
        
        return True, summary_msg, changes_made
    
    except Exception as e:
        return False, localization._("config_write_failed").format(e), None

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
            ttk.Label(info, text=localization._("select_valid_wow_optimizer")).pack()
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
            ttk.Label(tab, text=localization._("version_path").format(vlabel, vpath)).pack(anchor="w", padx=8, pady=8)
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

    ttk.Label(frame, text=localization._("optimizer_title").format(version_label), font=(None, 12, "bold")).pack(anchor="w", pady=(0, 8))

    # Check if required directories exist
    if not _check_version_directories(version_path):
        # Show instruction message instead of optimizer UI
        instruction_text = localization._("optimizer_launch_required").format(version_label)
        instruction_label = ttk.Label(
            frame,
            text=instruction_text,
            wraplength=max(200, (frame.winfo_width() - 40) if frame.winfo_width() > 1 else 560),
            justify="left",
            foreground="red"
        )
        instruction_label.pack(anchor="w", pady=(8, 8))
        
        # Update wraplength on resize with margin to prevent text cutoff
        def update_instruction_wrap(event):
            instruction_label.configure(wraplength=max(200, frame.winfo_width() - 40))
        frame.bind("<Configure>", update_instruction_wrap)
        
        return {"instruction_label": instruction_label}

    # Determine version type and classify hardware accordingly
    is_retail = version_label.lower().startswith("retail")
    is_classic = "classic" in version_label.lower()
    # If both integrated and dedicated GPUs are present (Intel/AMD), select dedicated BEFORE classification
    classification_hw = (hardware or {}).copy() if hardware else {}
    try:
        if hardware:
            gpu_list = hardware.get("gpu", [])
            cpu_name = hardware.get("cpu_name", "")
            chosen_dedicated, _ = _select_best_gpu(gpu_list, cpu_name)
            if chosen_dedicated:
                # Use only the dedicated GPU for tier calculations
                classification_hw["gpu"] = [chosen_dedicated]
    except Exception:
        pass

    if is_retail:
        overall, parts = _classify_retail_hardware(classification_hw)
        presets = _build_presets_for_level(overall)
        suggested_preset = _tier_to_suggested_preset(overall)
        preset_title = localization._("graphics_presets").format(localization._("version_retail"))
    elif is_classic:
        overall, parts = _classify_classic_hardware(classification_hw)
        presets = _build_presets_for_level(overall)
        suggested_preset = _tier_to_suggested_preset(overall)
        preset_title = localization._("graphics_presets_classic").format(localization._("version_classic"))
    else:
        overall = None
        suggested_preset = None
        preset_title = None

    # Read current config values once for all comparisons
    current_config = _read_current_config(version_path) if (is_retail or is_classic) else {}
    
    # Get recommended performance settings once for all uses
    recommended_perf_settings = _get_recommended_performance_settings(hardware) if (is_retail or is_classic) else []

    # System tier summary with suggested preset
    if is_retail or is_classic:
        tier_frame = ttk.Frame(frame)
        tier_frame.pack(fill="x", pady=(0, 8))
        
        # Create horizontal layout for system match and optimization status
        status_line = ttk.Frame(tier_frame)
        status_line.pack(anchor="w")
        
        ttk.Label(status_line, text=localization._("system_matches").format(localization._(suggested_preset.lower())), foreground="blue", font=(None, 10, "italic")).pack(side="left")
        
        # Helper function to check optimization status
        def check_optimization_status():
            """Check if all optimizations are applied and return status text and color."""
            current_cfg = _read_current_config(version_path)
            suggested_settings = _preset_to_config_settings(suggested_preset)
            
            # Combine preset settings and recommended performance settings
            all_settings = suggested_settings + recommended_perf_settings
            
            # Check if ALL settings match current config
            matches = 0
            total_settings = len(all_settings)
            for setting in all_settings:
                if setting.startswith("SET "):
                    parts = setting.split(None, 2)
                    if len(parts) >= 3:
                        setting_name = parts[1]
                        expected_value = parts[2].strip('"')
                        current_value = current_cfg.get(setting_name, "")
                        if current_value == expected_value:
                            matches += 1
            
            is_optimized = matches == total_settings and total_settings > 0
            status_text = localization._("optimization_applied") if is_optimized else localization._("optimization_not_applied")
            status_color = "green" if is_optimized else "orange"
            return status_text, status_color
        
        # Initial optimization status check
        optimization_status, status_color = check_optimization_status()
        optimization_status_var = tk.StringVar(value=optimization_status)
        optimization_status_label = ttk.Label(status_line, textvariable=optimization_status_var, foreground=status_color, font=(None, 9))
        optimization_status_label.pack(side="left", padx=(10, 0))

    # Action buttons - pack at bottom FIRST to reserve space
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(side="bottom", fill="x", pady=(8, 0))

    status_var = tk.StringVar(value="")

    # Create scrollable content area for recommendations (pack after button to fill remaining space)
    content_canvas = tk.Canvas(frame, borderwidth=0, highlightthickness=0)
    content_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=content_canvas.yview)
    content_canvas.configure(yscrollcommand=content_scrollbar.set)
    
    # Recommendations frame inside canvas
    rec_frame = ttk.Frame(content_canvas)
    content_canvas_window = content_canvas.create_window((0, 0), window=rec_frame, anchor="nw")
    
    def _on_rec_frame_configure(event):
        content_canvas.configure(scrollregion=content_canvas.bbox("all"))
    
    def _on_canvas_configure(event):
        content_canvas.itemconfig(content_canvas_window, width=event.width)
    
    rec_frame.bind("<Configure>", _on_rec_frame_configure)
    content_canvas.bind("<Configure>", _on_canvas_configure)
    
    # Pack canvas with scrollbar
    content_canvas.pack(side="left", fill="both", expand=True, pady=(4, 8))
    content_scrollbar.pack(side="right", fill="y", pady=(4, 8))

    # Version-specific presets (Retail or Classic)
    if is_retail or is_classic:
        ttk.Label(rec_frame, text=preset_title, font=(None, 10, "bold")).pack(anchor="w", pady=(0, 6))
        
        # Note: current_config and recommended_perf_settings already read earlier
        
        # Create a grid with 4 columns for Low, Medium, High, Ultra
        preset_grid = ttk.Frame(rec_frame)
        preset_grid.pack(fill="both", expand=True)
        
        # Helper to create tooltip text for a preset setting
        def create_setting_tooltip(preset_name, display_line):
            """Create tooltip showing current value vs new value for a setting."""
            # Get the CVar settings for this preset
            cvar_settings = _preset_to_config_settings(preset_name)
            
            # Find matching CVar for this display line
            tooltip_parts = []
            for cvar in cvar_settings:
                # Extract setting name and new value from CVar
                if cvar.startswith("SET "):
                    parts = cvar.split(None, 2)
                    if len(parts) >= 3:
                        setting_name = parts[1]
                        new_value = parts[2].strip('"')
                        
                        # Match display line to setting (rough match)
                        if ("renderScale" in setting_name and "Render Scale" in display_line) or \
                           ("TextureResolution" in setting_name and "Texture Quality" in display_line) or \
                           ("ShadowQuality" in setting_name and "Shadow Quality" in display_line) or \
                           ("SSAO" in setting_name and "SSAO" in display_line) or \
                           ("MSAAQuality" in setting_name and "Anti-Aliasing" in display_line) or \
                           ("VSync" in setting_name and "VSync" in display_line) or \
                           ("ViewDistance" in setting_name and "View Distance" in display_line) or \
                           ("EnvironmentDetail" in setting_name and "Environment" in display_line):
                            
                            current_value = current_config.get(setting_name, localization._("not_set"))
                            tooltip_parts.append(f"{setting_name}:\nCurrent: {current_value}\nNew: {new_value}")
            
            return "\n\n".join(tooltip_parts) if tooltip_parts else localization._("hover_for_details")
        
        # Helper to create tooltip for recommended performance settings
        def create_perf_setting_tooltip(setting):
            """Create tooltip for recommended performance settings."""
            if setting.startswith("SET "):
                parts = setting.split(None, 2)
                if len(parts) >= 3:
                    setting_name = parts[1]
                    new_value = parts[2].strip('"')
                    current_value = current_config.get(setting_name, localization._("not_set"))
                    
                    tooltip_text = f"{setting_name}:\nCurrent: {current_value}\nRecommended: {new_value}"
                    if setting_name not in current_config:
                        tooltip_text += "\n\nThis setting is not currently in your Config.wtf.\nAdding it will improve performance."
                    return tooltip_text
            return localization._("hover_for_details")
        
        col = 0
        for name in ("Low", "Medium", "High", "Ultra"):
            preset_col = ttk.Frame(preset_grid, relief="ridge", borderwidth=1, padding=6)
            preset_col.grid(row=0, column=col, sticky="nsew", padx=4, pady=2)
            preset_grid.columnconfigure(col, weight=1)
            
            preset_header = ttk.Label(preset_col, text=localization._(name.lower()), font=(None, 10, "bold"))
            preset_header.pack(anchor="w")
            
            # Add performance estimate tooltip to preset header
            from Modules.ui_helpers import Tooltip
            perf_estimate = _get_preset_performance_estimate(name, hardware)
            preset_tooltip = localization._("preset_tooltip_template").format(
                localization._(name.lower()), perf_estimate
            )
            Tooltip(preset_header, preset_tooltip)
            
            ttk.Separator(preset_col, orient="horizontal").pack(fill="x", pady=(2, 4))
            
            # Add preset lines
            for line in presets[name]:
                lbl = ttk.Label(preset_col, text=f"• {line}", font=(None, 8))
                lbl.pack(anchor="w")
                # Add tooltip with current vs new values
                from Modules.ui_helpers import Tooltip
                Tooltip(lbl, create_setting_tooltip(name, line))
            
            # Add recommended performance settings to each column
            if recommended_perf_settings:
                ttk.Separator(preset_col, orient="horizontal").pack(fill="x", pady=(6, 4))
                for setting in recommended_perf_settings:
                    # Extract setting name and value
                    if setting.startswith("SET "):
                        parts = setting.split(None, 2)
                        if len(parts) >= 3:
                            setting_name = parts[1]
                            new_value = parts[2].strip('"')
                            is_new = setting_name not in current_config
                            prefix = localization._("new_setting_prefix") if is_new else ""
                            
                            lbl = ttk.Label(preset_col, text=f"{prefix}• {setting_name} = {new_value}", 
                                          font=(None, 8), foreground="green" if is_new else "black")
                            lbl.pack(anchor="w")
                            
                            Tooltip(lbl, create_perf_setting_tooltip(setting))
            
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
        ttk.Label(rec_frame, text=localization._("recommended_settings")).grid(row=0, column=0, sticky="w")
        ttk.Label(rec_frame, text=tex).grid(row=1, column=0, sticky="w", padx=(8,0))
        ttk.Label(rec_frame, text=threads_rec).grid(row=2, column=0, sticky="w", padx=(8,0))

    # Populate action buttons (btn_frame already created and packed at bottom)
    
    # Retail or Classic tab: dropdown for preset selection
    if is_retail or is_classic:
        # Translate suggested preset for display
        suggested_preset_translated = localization._(suggested_preset.lower()) if suggested_preset else ""
        preset_var = tk.StringVar(value=suggested_preset_translated)
        ttk.Label(btn_frame, text=localization._("apply_preset_label")).pack(side="left", padx=(0, 6))
        preset_values = [localization._("low"), localization._("medium"), localization._("high"), localization._("ultra")]
        preset_dropdown = ttk.Combobox(btn_frame, textvariable=preset_var, values=preset_values, state="readonly", width=12)
        preset_dropdown.pack(side="left", padx=(0, 8))
        
        def apply_preset():
            from tkinter import messagebox
            # Convert translated display value back to English internal value
            chosen_display = preset_var.get()
            # Reverse lookup to get English preset name
            preset_map = {
                localization._("low"): "Low",
                localization._("medium"): "Medium",
                localization._("high"): "High",
                localization._("ultra"): "Ultra"
            }
            chosen = preset_map.get(chosen_display, chosen_display)  # fallback to display value if not found
            
            # Validation: Check if WoW is running
            if _check_wow_running():
                proceed = messagebox.askyesno(
                    localization._("wow_running_title"),
                    localization._("wow_running_message"),
                    icon='warning'
                )
                if not proceed:
                    status_var.set(localization._("cancelled_by_user"))
                    return
            
            # Validation: Check file permissions
            config_path = os.path.join(version_path, "WTF", "Config.wtf")
            if os.path.exists(config_path):
                try:
                    if not os.access(config_path, os.W_OK):
                        messagebox.showerror(
                            localization._("permission_error_title"),
                            localization._("permission_error_message")
                        )
                        status_var.set(localization._("config_readonly_status"))
                        return
                except Exception:
                    pass
            
            # Show confirmation dialog with summary
            preset_settings = _preset_to_config_settings(chosen)
            perf_settings = _get_recommended_performance_settings(hardware) if hardware else []
            total_changes = len(preset_settings) + len(perf_settings)
            
            confirm_msg = localization._("confirm_apply_message").format(
                chosen, version_label, total_changes, chosen, len(perf_settings)
            )
            
            proceed = messagebox.askyesno(localization._("confirm_apply_title"), confirm_msg, icon='question')
            if not proceed:
                status_var.set(localization._("cancelled_by_user"))
                return
            
            # Apply settings
            success, message, changes = _apply_settings_to_config(version_path, chosen, hardware)
            if success:
                # Log with details
                msg = localization._("applied_preset_log").format(chosen, version_label)
                app.log(msg, always_log=True)
                
                # Show detailed results
                if changes:
                    result_msg = f"✓ {message}\n\n"
                    result_msg += f"{localization._("details_colon")}\n"
                    result_msg += f"{localization._("updated_settings").format(len(changes['updated']))}\n"
                    result_msg += f"{localization._("added_settings").format(len(changes['added']))}"
                    status_var.set(localization._("settings_applied_status").format(len(changes['updated'])+len(changes['added'])))
                else:
                    status_var.set(localization._("preset_applied_status").format(chosen))
                
                # Update optimization status feedback
                new_status, new_color = check_optimization_status()
                optimization_status_var.set(f"  —  {new_status}")
                optimization_status_label.configure(foreground=new_color)
                
                # Save change to history
                _save_optimization_history(version_path, version_label, chosen, changes)
            else:
                app.log(localization._("apply_preset_failed_log").format(chosen, message), always_log=True)
                status_var.set(localization._("apply_error_status").format(message[:40]))
        
        ttk.Button(btn_frame, text=localization._("apply"), command=apply_preset).pack(side="left")
    else:
        # Generic apply for other versions
        def apply_recommendations():
            msg = localization._("applied_preset_log").format(localization._("recommended_settings"), version_label)
            app.log(msg, always_log=True)
            status_var.set(localization._("recommendations_applied"))
        
        ttk.Button(btn_frame, text=localization._("apply_recommended_settings"), command=apply_recommendations).pack(side="left")
    
    ttk.Label(btn_frame, textvariable=status_var, foreground="green").pack(side="left", padx=(10,0))

    return {"status_var": status_var}

def _on_scan_hardware(app, info_label, gpu_switch_label, scan_btn, notebook_container):
    """Handle Scan Hardware button press.

    Scans system hardware, caches results in global settings, and logs succinctly.

    Args:
        app: The WoWCleanupTool instance
        info_label: The label to update with status
        gpu_switch_label: The label to display GPU switch notification
        scan_btn: The Scan Hardware button widget
    """
    # Show progress feedback
    info_label.configure(text=localization._("scanning_cpu"))
    gpu_switch_label.configure(text="")
    app.root.update()

    try:
        # Detect CPU with progress update
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_threads = psutil.cpu_count(logical=True)
        cpu_name = _detect_cpu_name()
        
        info_label.configure(text=localization._("scanning_ram_detected").format(cpu_cores, cpu_threads))
        app.root.update()
        
        # Detect RAM
        memory_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)
        
        info_label.configure(text=localization._("scanning_gpu_detected").format(memory_gb))
        app.root.update()
        
        # Detect GPU
        gpu_list = _detect_gpu_names()
        selected_gpu, original_gpu = _select_best_gpu(gpu_list, cpu_name)
        
        hardware = {
            "system": platform.system(),
            "processor": platform.processor(),
            "cpu_name": cpu_name,
            "cpu_cores": cpu_cores,
            "cpu_threads": cpu_threads,
            "memory_gb": memory_gb,
            "gpu": gpu_list,
            "gpu_selected": selected_gpu,
            "gpu_original": original_gpu,
        }
        
        set_global_setting("hardware_cache", hardware)
        _display_hardware_info(info_label, hardware)
        _display_gpu_switch_info(gpu_switch_label, hardware)
        _set_scan_tooltip(scan_btn)
        _populate_version_tabs(app, notebook_container)
        app.log(localization._("hardware_scan_complete"), always_log=True)
    except Exception as e:
        info_label.configure(text=localization._("scan_error").format(str(e)[:50]))
        app.log(localization._("hardware_scan_failed").format(str(e)), always_log=True)

