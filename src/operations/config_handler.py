"""Config.wtf file handler for World of Warcraft optimization.

This module provides utilities to read, modify, and write WoW Config.wtf files,
managing CVars (Console Variables) used for game configuration.
"""

from pathlib import Path
from typing import Any


def read_config(config_path: Path) -> dict[str, str]:
    """Read a Config.wtf file and parse all CVars.

    Args:
        config_path: Path to Config.wtf file

    Returns:
        Dictionary mapping CVar names to their values (as strings)
    """
    cvars = {}
    if not config_path.exists():
        return cvars

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("SET "):
                    # Parse: SET cvarName "value"
                    parts = line[4:].split(None, 1)  # Split after "SET "
                    if len(parts) == 2:
                        cvar_name = parts[0]
                        value = parts[1]
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        cvars[cvar_name] = value
    except Exception:
        # If we can't read the file, return empty dict
        pass

    return cvars


def write_config(config_path: Path, cvars: dict[str, Any]) -> bool:
    """Write CVars to a Config.wtf file.

    Args:
        config_path: Path to Config.wtf file
        cvars: Dictionary of CVar names to values

    Returns:
        True if successful, False otherwise
    """
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            for cvar_name, value in sorted(cvars.items()):
                # Format based on value type
                if isinstance(value, str):
                    f.write(f'SET {cvar_name} "{value}"\n')
                elif isinstance(value, (int, float)):
                    f.write(f'SET {cvar_name} "{value}"\n')
                else:
                    f.write(f'SET {cvar_name} "{str(value)}"\n')
        return True
    except Exception:
        return False


def update_cvar(config_path: Path, cvar_name: str, value: Any) -> bool:
    """Update a single CVar in a Config.wtf file.

    Reads the file, updates the CVar, and writes it back.
    Creates the CVar if it doesn't exist.

    Args:
        config_path: Path to Config.wtf file
        cvar_name: Name of the CVar to update
        value: New value for the CVar

    Returns:
        True if successful, False otherwise
    """
    cvars = read_config(config_path)
    cvars[cvar_name] = value
    return write_config(config_path, cvars)


def get_cvar(config_path: Path, cvar_name: str) -> str | None:
    """Get the value of a specific CVar from a Config.wtf file.

    Args:
        config_path: Path to Config.wtf file
        cvar_name: Name of the CVar to retrieve

    Returns:
        CVar value as string, or None if not found
    """
    cvars = read_config(config_path)
    return cvars.get(cvar_name)


def clean_gpu_name(gpu_name: str) -> str:
    """Remove manufacturer prefix from GPU name for gxAdapter CVar.

    WoW's gxAdapter expects GPU names without manufacturer prefixes.

    Examples:
        "NVIDIA GeForce RTX 2080 Super" -> "GeForce RTX 2080 Super"
        "AMD Radeon RX 7900 XTX" -> "Radeon RX 7900 XTX"
        "Intel Arc A770" -> "Arc A770"
        "Apple M3 Max" -> "M3 Max"

    Args:
        gpu_name: Full GPU name from hardware detection

    Returns:
        GPU name with manufacturer prefix removed
    """
    # List of manufacturer prefixes to strip (case-insensitive)
    prefixes = ["NVIDIA ", "AMD ", "Intel ", "Apple "]

    for prefix in prefixes:
        if gpu_name.startswith(prefix):
            return gpu_name[len(prefix) :]

    return gpu_name


def select_best_gpu(gpus: list) -> str | None:
    """Select the best GPU for gaming from a list of detected GPUs.

    Prefers dedicated GPUs over integrated. If multiple dedicated GPUs exist,
    returns the first one (hardware scanner typically lists most powerful first).

    Args:
        gpus: List of GPU objects with 'name' and 'is_integrated' attributes

    Returns:
        Cleaned GPU name suitable for gxAdapter, or None if no GPUs
    """
    if not gpus:
        return None

    # First, try to find a dedicated GPU
    for gpu in gpus:
        if not gpu.is_integrated:
            return clean_gpu_name(gpu.name)

    # If no dedicated GPU found, use the first GPU (likely integrated)
    return clean_gpu_name(gpus[0].name)
