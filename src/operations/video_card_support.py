"""Supported video card reference for WoW Classic/Classic Era (Windows).

Source: Blizzard Support Article ID 248472 (World of Warcraft Classic Supported Video Cards).
This module captures the supported GPU series and minimum required GPUs so the
optimizer can gate features or warn users with unsupported hardware.
"""

import re

# Minimum required GPUs (Windows, Classic / Classic Era)
CLASSIC_WINDOWS_MINIMUM_GPUS = {
    "nvidia": "GeForce GT 440 (1 GB)",
    "amd": "Radeon HD 5670 (1 GB)",
    "intel": "Intel HD Graphics 4000 (45W TDP with 4 GB system RAM)",
}

# Minimum required GPUs (Windows, Retail)
RETAIL_WINDOWS_MINIMUM_GPUS = {
    "nvidia": "GeForce GTX 760 (2 GB)",
    "amd": "Radeon RX 560 (2 GB)",
    "intel": "Intel UHD Graphics 630 (45W TDP with 8 GB system RAM)",
}

# Supported GPU series (Windows, Classic / Classic Era)
CLASSIC_WINDOWS_SUPPORTED_SERIES = {
    "nvidia": [
        "GeForce GTX 400 Series",
        "GeForce GTX 500 Series",
        "GeForce GTX 600 Series",
        "GeForce GTX 700 Series",
        "GeForce GTX 800M Series",
        "GeForce GTX 900 Series",
        "GeForce GTX 10 Series",
        "Volta Series",
        "GeForce GTX 16 Series",
        "GeForce RTX 20 Series",
        "GeForce RTX 30 Series",
        "GeForce RTX 40 Series",
        "GeForce RTX 50 Series",
        "NVIDIA Titan",
        "NVIDIA Quadro",
        "NVIDIA RTX A",
    ],
    "amd": [
        "Radeon HD 5000 Series",
        "Radeon HD 6000 Series",
        "Radeon HD 7000 Series",
        "Radeon HD 8000 Series",
        "Radeon R5/R7/R9 200 Series",
        "Radeon R5/R7/R9 300 Series",
        "Radeon R9 Fury/Nano Series",
        "Radeon Pro Duo",
        "Radeon RX 400 Series",
        "Radeon RX 500 Series",
        "Radeon RX Vega Series",
        "Radeon VII Series",
        "Radeon RX 5000 Series",
        "Radeon RX 6000 Series",
        "Radeon RX 7000 Series",
        "Radeon RX 9000 Series",
        "Radeon PRO",
    ],
    "intel": [
        "Intel HD Graphics 4000",
        "Intel HD Graphics 4200/4400/4600",
        "Intel HD Graphics 5000 Series",
        "Intel HD Graphics 6000 Series",
        "Intel HD Graphics 500 Series",
        "Intel HD Graphics 600 Series",
        "Intel UHD Graphics 600 Series",
        "Intel UHD Graphics 700 Series",
        "Intel UHD Graphics 800 Series",
        "Intel Iris Plus",
        "Intel Iris Xe",
        "Intel Arc",
        "Arc A-Series",
        "Arc B-Series",
    ],
}

# Supported GPU series (Windows, Retail)
RETAIL_WINDOWS_SUPPORTED_SERIES = {
    "nvidia": [
        "GeForce GTX 760",
        "GeForce GTX 800M Series",
        "GeForce GTX 900 Series",
        "GeForce GTX 10 Series",
        "Volta Series",
        "GeForce GTX 16 Series",
        "GeForce RTX 20 Series",
        "GeForce RTX 30 Series",
        "GeForce RTX 40 Series",
        "GeForce RTX 50 Series",
        "NVIDIA Titan",
        "NVIDIA Quadro",
        "NVIDIA RTX A",
    ],
    "amd": [
        "Radeon RX 560",
        "Radeon RX Vega Series",
        "Radeon VII Series",
        "Radeon RX 5000 Series",
        "Radeon RX 6000 Series",
        "Radeon RX 7000 Series",
        "Radeon RX 9000 Series",
        "Radeon PRO",
    ],
    "intel": [
        "Intel UHD Graphics 630",
        "Intel UHD Graphics 700 Series",
        "Intel UHD Graphics 800 Series",
        "Intel Iris Plus Graphics",
        "Intel Iris Xe Graphics",
        "Intel Arc",
        "Arc A-Series",
        "Arc B-Series",
    ],
}

# Supported GPUs (macOS, Classic / Classic Era)
CLASSIC_MAC_SUPPORTED_GPUS = {
    "nvidia": [
        "GeForce GT 640M",
        "GeForce GT 650M",
        "GeForce GT 660M",
        "GeForce GTX 675MX",
        "GeForce GTX 680MX",
        "GeForce GT 750M",
        "GeForce GT 755M",
        "GeForce GTX 775M",
        "GeForce GTX 780M",
    ],
    "amd": [
        "Radeon R9 M290",
        "Radeon R9 M290X",
        "Radeon R9 M370X",
        "Radeon R9 M380",
        "Radeon R9 M390",
        "Radeon R9 M395",
        "Radeon RX 470",
        "Radeon RX 480",
        "Radeon Pro 555",
        "Radeon Pro 560",
        "Radeon RX 560",
        "Radeon Pro 570",
        "Radeon RX 570",
        "Radeon Pro 575",
        "Radeon Pro 580",
        "Radeon RX 580",
        "Radeon Pro WX 7100",
        "Radeon RX Vega 56",
        "Radeon RX Vega 64",
        "Vega Frontier Edition Air",
        "Radeon Pro WX 9100",
    ],
    "intel": [
        "Intel HD Graphics 4000",
        "Intel HD Graphics 5000",
        "Intel Iris Graphics 5100",
        "Intel Iris Pro Graphics 5200",
        "Intel HD Graphics 5300",
        "Intel HD Graphics 6000",
        "Intel Iris Graphics 6100",
        "Intel Iris Pro Graphics 6200",
        "Intel HD Graphics 515",
        "Intel Iris Graphics 540",
        "Intel Iris Graphics 550",
        "Intel Iris Pro Graphics 640",
        "Intel Iris Pro Graphics 650",
    ],
    "apple": [
        "M1",
        "M1 Pro",
        "M1 Max",
        "M1 Ultra",
        "M2",
        "M2 Pro",
        "M2 Max",
        "M2 Ultra",
        "M3",
        "M3 Pro",
        "M3 Max",
    ],
}

# Supported GPUs (macOS, Retail)
RETAIL_MAC_SUPPORTED_GPUS = {
    "nvidia": [
        "GeForce GTX 750M",
        "GeForce GT 755M",
        "GeForce GTX 775M",
        "GeForce GTX 780M",
    ],
    "amd": [
        "Radeon R9 M290",
        "Radeon R9 M290X",
        "Radeon R9 M370X",
        "Radeon R9 M380",
        "Radeon R9 M390",
        "Radeon R9 M395",
        "Radeon Pro 450",
        "Radeon Pro 455",
        "Radeon RX 470",
        "Radeon RX 480",
        "Radeon Pro 555",
        "Radeon Pro 560",
        "Radeon RX 560",
        "Radeon Pro 570",
        "Radeon RX 570",
        "Radeon Pro 575",
        "Radeon Pro 580",
        "Radeon RX 580",
        "Radeon Pro WX 7100",
        "Radeon RX Vega 56",
        "Radeon RX Vega 64",
        "Vega Frontier Edition Air",
        "Radeon Pro WX 9100",
    ],
    "intel": [
        "Intel UHD Graphics 630",
        "Intel Iris Plus Graphics 640",
        "Intel Iris Plus Graphics 650",
    ],
    "apple": [
        "M1",
        "M1 Pro",
        "M1 Max",
        "M1 Ultra",
        "M2",
        "M2 Pro",
        "M2 Max",
        "M2 Ultra",
        "M3",
        "M3 Pro",
        "M3 Max",
    ],
}


def _extract_gpu_series(gpu_name: str) -> list[str]:
    """Extract GPU series identifiers from GPU name.

    Handles variations like:
    - "GeForce RTX 2080 Super" → ["rtx 20", "geforce rtx 20"]
    - "Radeon 9070 XT" → ["9000", "rx 9000"]
    - "Radeon RX 6700 XT" → ["rx 6000", "6000"]
    - "Intel Arc A770" → ["arc a", "a"]

    Args:
        gpu_name: GPU name to extract series from

    Returns:
        List of series identifiers to check
    """
    gpu_lower = gpu_name.lower()
    series_patterns = []

    # Add the full name for backward compatibility
    series_patterns.append(gpu_lower)

    # NVIDIA patterns
    if "geforce" in gpu_lower or "nvidia" in gpu_lower:
        # RTX 20, RTX 30, RTX 40, RTX 50, etc.
        rtx_match = re.search(r"rtx\s*(\d)(\d)", gpu_lower)
        if rtx_match:
            decade = rtx_match.group(1) + rtx_match.group(2)
            series_patterns.append(f"rtx {decade}")
            series_patterns.append(f"geforce rtx {decade}")

        # GTX patterns (GTX 1080, GTX 960, etc.)
        gtx_match = re.search(r"gtx\s*(\d)(\d{2})", gpu_lower)
        if gtx_match:
            decade = gtx_match.group(1) + "0"
            series_patterns.append(f"gtx {decade}")

        # Add manufacturer prefix variations
        if "titan" in gpu_lower:
            series_patterns.append("titan")
        if "quadro" in gpu_lower:
            series_patterns.append("quadro")
        if "rtx a" in gpu_lower or "rtxa" in gpu_lower:
            series_patterns.append("rtx a")

    # AMD patterns
    if "radeon" in gpu_lower or "amd" in gpu_lower:
        # RX 6000, RX 7000, RX 9000 series (e.g., "RX 6700 XT" or "9070 XT")
        rx_match = re.search(r"(?:rx\s*)?(\d)(\d{3})", gpu_lower)
        if rx_match:
            decade = rx_match.group(1) + "000"
            series_patterns.append(f"rx {decade}")
            series_patterns.append(f"radeon rx {decade}")
            series_patterns.append(f"{decade}")  # Match just "9000"

        # R9/R7/R5 patterns for older cards
        old_match = re.search(r"r([579])\s*(\d{3})", gpu_lower)
        if old_match:
            series_patterns.append(f"r{old_match.group(1)}")

        # Add manufacturer-specific patterns
        if "pro" in gpu_lower:
            series_patterns.append("pro")
        if "fury" in gpu_lower:
            series_patterns.append("fury")
        if "nano" in gpu_lower:
            series_patterns.append("nano")
        if "vega" in gpu_lower:
            series_patterns.append("vega")

    # Intel patterns
    if "intel" in gpu_lower or "arc" in gpu_lower:
        # Arc A-Series or Arc B-Series
        arc_match = re.search(r"arc\s*([ab])", gpu_lower)
        if arc_match:
            series_patterns.append(f"arc {arc_match.group(1)}")
            series_patterns.append(f"arc {arc_match.group(1)}-series")

        # Intel UHD/HD Graphics series
        uhd_match = re.search(r"u?hd\s*graphics\s*(\d{3,4})", gpu_lower)
        if uhd_match:
            series_patterns.append(f"uhd graphics {uhd_match.group(1)}")
            series_patterns.append(f"hd graphics {uhd_match.group(1)}")

        # Intel Iris patterns
        if "iris" in gpu_lower:
            series_patterns.append("iris")
            if "xe" in gpu_lower:
                series_patterns.append("iris xe")

    return series_patterns


def is_gpu_supported(gpu_name: str, game_version: str = "retail") -> bool:
    """Check if a GPU is supported for the given game version.

    Uses smart pattern matching to handle GPU name variations.

    Args:
        gpu_name: Full or partial GPU name (e.g., "GeForce RTX 2080 Super", "Radeon 9070 XT")
        game_version: "retail" or "classic" (defaults to "retail")

    Returns:
        True if GPU is supported, False if unsupported or unknown
    """
    if not gpu_name or not gpu_name.strip():
        return False

    # Select appropriate supported series based on game version and OS
    # For now, assuming Windows (primary platform)
    if game_version.lower() in ("classic", "classic_era"):
        supported_series = CLASSIC_WINDOWS_SUPPORTED_SERIES
    else:
        supported_series = RETAIL_WINDOWS_SUPPORTED_SERIES

    # Extract potential series identifiers from GPU name
    series_patterns = _extract_gpu_series(gpu_name)

    # Check each extracted pattern against supported series
    for pattern in series_patterns:
        for manufacturer, series_list in supported_series.items():
            for series in series_list:
                # Case-insensitive substring match
                if pattern in series.lower():
                    return True

    return False
