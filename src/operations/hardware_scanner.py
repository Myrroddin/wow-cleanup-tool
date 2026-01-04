"""Hardware detection and information gathering for WoW Cleanup Tool."""

import json
import logging
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import psutil
except ImportError:
    psutil = None

try:
    import GPUtil
except ImportError:
    GPUtil = None

logger = logging.getLogger(__name__)


@dataclass
class GPUInfo:
    """Information about a GPU."""

    name: str
    memory_mb: int
    is_integrated: bool
    vendor: str  # "NVIDIA", "AMD", "Intel", "Unknown"


@dataclass
class HardwareInfo:
    """System hardware information."""

    cpu_name: str
    cpu_cores: int
    cpu_freq_ghz: float
    ram_gb: float
    gpus: list[GPUInfo]
    cache_timestamp: float  # Unix timestamp for cache expiration

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "cpu_name": self.cpu_name,
            "cpu_cores": self.cpu_cores,
            "cpu_freq_ghz": self.cpu_freq_ghz,
            "ram_gb": self.ram_gb,
            "gpus": [asdict(gpu) for gpu in self.gpus],
            "cache_timestamp": self.cache_timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "HardwareInfo":
        """Create from dictionary (JSON deserialization)."""
        gpus = [GPUInfo(**gpu) for gpu in data.get("gpus", [])]
        return cls(
            cpu_name=data.get("cpu_name", "Unknown"),
            cpu_cores=data.get("cpu_cores", 0),
            cpu_freq_ghz=data.get("cpu_freq_ghz", 0.0),
            ram_gb=data.get("ram_gb", 0.0),
            gpus=gpus,
            cache_timestamp=data.get("cache_timestamp", 0.0),
        )

    def is_expired(self, days: int = 30) -> bool:
        """Check if cache has expired."""
        expiration_time = self.cache_timestamp + (days * 24 * 60 * 60)
        return datetime.now().timestamp() > expiration_time


class HardwareScanner:
    """Scans and caches system hardware information."""

    CACHE_FILE = Path.home() / ".wow_cleanup_tool" / "hardware_cache.json"

    def __init__(self):
        """Initialize the hardware scanner."""
        self._cached_info: Optional[HardwareInfo] = None
        self._load_cache()

    def _load_cache(self) -> None:
        """Load cached hardware information from disk if valid."""
        if self.CACHE_FILE.exists():
            try:
                with open(self.CACHE_FILE, "r") as f:
                    data = json.load(f)
                    info = HardwareInfo.from_dict(data)
                    # Check if cache is still valid (30 day TTL)
                    if not info.is_expired(days=30):
                        self._cached_info = info
                        logger.debug("Loaded valid hardware info from cache")
                    else:
                        logger.debug(
                            "Hardware cache expired, will refresh on next scan"
                        )
                        self.CACHE_FILE.unlink(missing_ok=True)
            except Exception as e:
                logger.warning(f"Failed to load hardware cache: {e}")
                self._cached_info = None

    def _save_cache(self, info: HardwareInfo) -> None:
        """Save hardware information to cache."""
        try:
            self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(self.CACHE_FILE, "w") as f:
                json.dump(info.to_dict(), f, indent=2)
            logger.debug("Saved hardware info to cache")
        except Exception as e:
            logger.warning(f"Failed to save hardware cache: {e}")

    def scan(self) -> Optional[HardwareInfo]:
        """
        Scan system hardware in parallel. Returns cached results if available.

        Uses ThreadPoolExecutor to run CPU, RAM, and GPU detection concurrently,
        reducing total scan time significantly.

        Returns:
            HardwareInfo object or None if scan fails.
        """
        if self._cached_info is not None:
            return self._cached_info

        try:
            if psutil is None:
                logger.error("psutil not available for hardware scanning")
                return None

            # Run detection tasks in parallel for faster scanning
            with ThreadPoolExecutor(max_workers=3) as executor:
                cpu_future = executor.submit(self._get_cpu_name)
                ram_future = executor.submit(self._get_ram_info)
                gpu_future = executor.submit(self._get_gpu_info)

                cpu_name = cpu_future.result(timeout=10)
                ram_gb = ram_future.result(timeout=5)
                gpus = gpu_future.result(timeout=15)

            cpu_cores = psutil.cpu_count(logical=False) or 1
            cpu_freq = psutil.cpu_freq()
            cpu_freq_ghz = (cpu_freq.max / 1000.0) if cpu_freq else 0.0

            info = HardwareInfo(
                cpu_name=cpu_name,
                cpu_cores=cpu_cores,
                cpu_freq_ghz=round(cpu_freq_ghz, 2),
                ram_gb=ram_gb,
                gpus=gpus,
                cache_timestamp=datetime.now().timestamp(),
            )

            self._cached_info = info
            self._save_cache(info)
            logger.debug(f"Hardware scan completed: {info}")
            return info

        except Exception as e:
            logger.error(f"Hardware scan failed: {e}", exc_info=True)
            return None

    def _get_cpu_name(self) -> str:
        """Get human-readable CPU name with fallback chain."""
        try:
            # Try cpuinfo if available (most reliable)
            try:
                import cpuinfo

                cpu_info = cpuinfo.get_cpu_info()
                brand = cpu_info.get("brand_raw", "")
                if brand:
                    return self._clean_cpu_name(brand)
            except ImportError:
                pass

            # Fallback: Windows WMI
            if sys.platform == "win32":
                return self._get_cpu_name_windows()

            # Fallback: /proc/cpuinfo on Linux
            if sys.platform.startswith("linux"):
                return self._get_cpu_name_linux()

            return "Unknown CPU"

        except Exception as e:
            logger.warning(f"Failed to get CPU name: {e}")
            return "Unknown CPU"

    def _get_ram_info(self) -> float:
        """Get total RAM in GB."""
        try:
            if psutil is None:
                return 0.0
            ram_bytes = psutil.virtual_memory().total
            return round(ram_bytes / (1024**3), 2)
        except Exception as e:
            logger.warning(f"Failed to get RAM info: {e}")
            return 0.0

    def _clean_cpu_name(self, name: str) -> str:
        """Clean up CPU name by removing extra whitespace and qualifiers."""
        # Remove redundant descriptions like (R), (TM), multiple spaces
        name = re.sub(r"\(R\)|\(TM\)", "", name)
        name = re.sub(r"\s+", " ", name)
        return name.strip()

    def _get_cpu_name_windows(self) -> str:
        """Get CPU name from Windows WMI using PowerShell."""
        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name",
                ],
                capture_output=True,
                text=True,
                timeout=5,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                ),
            )
            if result.returncode == 0:
                cpu_name = result.stdout.strip()
                if cpu_name:
                    return self._clean_cpu_name(cpu_name)
        except Exception as e:
            logger.debug(f"PowerShell CPU query failed: {e}")
        return "Unknown CPU"

    def _get_cpu_name_linux(self) -> str:
        """Get CPU name from Linux /proc/cpuinfo."""
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if line.startswith("model name"):
                        cpu_name = line.split(":", 1)[1].strip()
                        return self._clean_cpu_name(cpu_name)
        except Exception as e:
            logger.debug(f"Linux CPU query failed: {e}")
        return "Unknown CPU"

    def _get_gpu_info(self) -> list[GPUInfo]:
        """Get information about installed GPUs with fallback chain.

        Tries multiple detection methods in order of preference:
        1. GPUtil (best for NVIDIA, cross-platform)
        2. Windows WMI
        3. Linux lspci
        """
        gpus = []

        # Try GPUtil first (most reliable for NVIDIA and modern GPUs)
        if GPUtil is not None:
            try:
                gpu_list = GPUtil.getGPUs()
                for gpu in gpu_list:
                    gpu_info = self._parse_gpu_info(gpu.name, int(gpu.memoryTotal))
                    gpus.append(gpu_info)
                if gpus:
                    logger.debug(f"Detected {len(gpus)} GPU(s) using GPUtil")
                    return gpus
            except Exception as e:
                logger.debug(f"GPUtil detection failed: {e}")

        # Fallback to platform-specific methods
        if sys.platform == "win32":
            gpus.extend(self._get_gpu_info_windows())
        elif sys.platform.startswith("linux"):
            gpus.extend(self._get_gpu_info_linux())

        logger.debug(f"Found {len(gpus)} GPU(s) total")
        return gpus

    def _get_gpu_info_windows(self) -> list[GPUInfo]:
        """Get GPU info from Windows WMI using PowerShell."""
        gpus = []
        try:
            # Use PowerShell Get-CimInstance (more reliable than wmic)
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "Get-CimInstance Win32_VideoController | "
                    "Select-Object Name, AdapterRAM | "
                    'ForEach-Object { "Name=$($_.Name)"; "AdapterRAM=$($_.AdapterRAM)"; "" }',
                ],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                ),
            )

            if result.returncode == 0:
                gpu_blocks = result.stdout.split("\n\n")
                for block in gpu_blocks:
                    if not block.strip():
                        continue

                    gpu_name = None
                    gpu_memory_mb = 0

                    for line in block.split("\n"):
                        if line.startswith("Name="):
                            gpu_name = line.replace("Name=", "").strip()
                        elif line.startswith("AdapterRAM="):
                            try:
                                memory_bytes = int(
                                    line.replace("AdapterRAM=", "").strip()
                                )
                                gpu_memory_mb = memory_bytes // (1024 * 1024)
                            except ValueError:
                                pass

                    if gpu_name and gpu_name.lower() != "unknown":
                        gpu_info = self._parse_gpu_info(gpu_name, gpu_memory_mb)
                        gpus.append(gpu_info)

        except Exception as e:
            logger.warning(f"Windows GPU detection failed: {e}")

        return gpus

    def _get_gpu_info_linux(self) -> list[GPUInfo]:
        """Get GPU info from Linux lspci and glxinfo."""
        gpus = []

        try:
            # Try lspci for all GPUs
            result = subprocess.run(
                ["lspci"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if "VGA compatible controller:" in line or "3D controller:" in line:
                        # Extract GPU name
                        gpu_name = (
                            line.split(": ", 1)[-1].strip() if ": " in line else ""
                        )
                        if gpu_name:
                            gpu_info = self._parse_gpu_info(gpu_name, 0)
                            gpus.append(gpu_info)

        except Exception as e:
            logger.warning(f"Linux GPU detection failed: {e}")

        return gpus

    def _parse_gpu_info(self, gpu_name: str, memory_mb: int) -> GPUInfo:
        """Parse GPU name and return GPUInfo object."""
        gpu_name_lower = gpu_name.lower()
        is_integrated = False
        vendor = "Unknown"

        # Determine vendor
        if "nvidia" in gpu_name_lower:
            vendor = "NVIDIA"
        elif "amd" in gpu_name_lower or "radeon" in gpu_name_lower:
            vendor = "AMD"
        elif "intel" in gpu_name_lower:
            vendor = "Intel"
            is_integrated = True

        # Check if integrated (Intel UHD, Intel Iris, AMD Vega integrated, etc.)
        integrated_keywords = [
            "integrated",
            "uhd",
            "iris",
            "xe",
            "radeon graphics",
            "vega",
        ]
        if any(kw in gpu_name_lower for kw in integrated_keywords):
            is_integrated = True

        # Clean up name for display (remove extra qualifiers)
        clean_name = self._clean_gpu_name(gpu_name)

        return GPUInfo(
            name=clean_name,
            memory_mb=memory_mb,
            is_integrated=is_integrated,
            vendor=vendor,
        )

    def _clean_gpu_name(self, name: str) -> str:
        """Clean up GPU name for display."""
        # Remove [AMD/ATI], (R), (TM), and reduce multiple spaces
        name = re.sub(r"\[AMD/ATI\]|\(R\)|\(TM\)", "", name)
        name = re.sub(r"\s+", " ", name)
        return name.strip()
