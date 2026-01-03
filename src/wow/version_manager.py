"""Game version representation and management.

Provides a unified way to represent WoW game versions (flavors) throughout
the application. This eliminates the need to pass tuples and provides a
single source of truth for version information.
"""

from typing import List, Optional


class GameVersion:
    """Represents a single World of Warcraft game version (flavor).

    Encapsulates all information needed to identify and work with a specific
    WoW version (Retail, Classic, Classic Era, etc.).

    Attributes:
        flavor_dir: Directory name for this version (e.g., "_retail_", "_classic_")
        display_name: Localized display name for UI (e.g., "Retail", "Classic")
        path: Full filesystem path to this version's directory
    """

    def __init__(self, flavor_dir: str, display_name: str, path: str):
        """Initialize a game version.

        Args:
            flavor_dir: Folder name for this WoW version (e.g., "_retail_")
            display_name: User-friendly name for UI display (localized)
            path: Full path to the version directory on disk
        """
        self.flavor_dir = flavor_dir
        self.display_name = display_name
        self.path = path

    def __repr__(self) -> str:
        """Return string representation for debugging."""
        return f"GameVersion({self.flavor_dir}, {self.display_name})"

    def __eq__(self, other) -> bool:
        """Compare versions by flavor_dir."""
        if isinstance(other, GameVersion):
            return self.flavor_dir == other.flavor_dir
        return False

    def __hash__(self) -> int:
        """Allow use in sets and as dict keys."""
        return hash(self.flavor_dir)

    @staticmethod
    def from_tuple(flavor_dir: str, display_name: str, path: str = "") -> "GameVersion":
        """Create GameVersion from individual components.

        Args:
            flavor_dir: Folder name for this version
            display_name: Display name for UI
            path: Full path to version directory (optional)

        Returns:
            GameVersion: New instance
        """
        return GameVersion(flavor_dir, display_name, path)

    def to_tuple(self) -> tuple:
        """Convert to tuple format for backward compatibility.

        Returns:
            tuple: (flavor_dir, display_name)
        """
        return (self.flavor_dir, self.display_name)
