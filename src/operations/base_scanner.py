"""
Base scanner class for all cleanup operations.

Provides common functionality for scanning WoW installations,
including parallel processing and progress reporting.
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Optional, Callable, Any


class BaseScanner:
    """Base class for all WoW cleanup scanners.

    Provides:
    - Parallel scanning across multiple WoW versions
    - Progress callback support
    - Consistent error handling
    - os.scandir-based directory traversal
    """

    def __init__(
        self,
        max_workers: int = 8,
        logger: Optional[Any] = None,
        loc: Optional[Any] = None,
    ):
        """Initialize scanner.

        Args:
            max_workers: Maximum parallel workers (default 8 for SSDs)
            logger: Optional logger with .error() and .debug() methods
            loc: Optional localization instance with ._() method
        """
        self.max_workers = max_workers
        self.logger = logger
        self.loc = loc

    def scan_versions(
        self,
        versions: List[Tuple[str, str]],
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, List[str]]:
        """Scan multiple WoW versions in parallel.

        Args:
            versions: List of (version_path, version_label) tuples
            progress_callback: Optional callback(current, total, label)

        Returns:
            Dict mapping version_label -> list of found items
        """
        results = {}

        if not versions:
            return results

        # Limit workers to number of versions, cap at max_workers
        workers = min(len(versions), self.max_workers)

        try:
            with ThreadPoolExecutor(max_workers=workers) as executor:
                # Submit all scan tasks
                future_map = {
                    executor.submit(self._scan_version, vpath): vlabel
                    for vpath, vlabel in versions
                }

                # Collect results as they complete
                completed = 0
                total = len(versions)

                for future in as_completed(future_map):
                    vlabel = future_map[future]
                    completed += 1

                    if progress_callback:
                        progress_callback(completed, total, vlabel)

                    try:
                        items = future.result()
                        if items:
                            results[vlabel] = items
                    except Exception as e:
                        # Log error but continue with other versions
                        if self.logger and hasattr(self, "loc") and self.loc:
                            self.logger.error(
                                self.loc._("error_scanning_version").format(vlabel, e)
                            )
                        elif self.logger:
                            self.logger.error(f"Error scanning {vlabel}: {e}")
                        continue

        except Exception as e:
            # Fallback to single-threaded on executor failure
            if self.logger and hasattr(self, "loc") and self.loc:
                self.logger.error(self.loc._("error_threadpool_fallback").format(e))
            elif self.logger:
                self.logger.error(
                    f"ThreadPoolExecutor failed, falling back to single-threaded: {e}"
                )
            for vpath, vlabel in versions:
                try:
                    items = self._scan_version(vpath)
                    if items:
                        results[vlabel] = items
                except Exception:
                    continue

        return results

    def _scan_version(self, version_path: str) -> List[str]:
        """Scan a single WoW version. Override in subclasses.

        Args:
            version_path: Path to WoW version directory

        Returns:
            List of found item paths
        """
        raise NotImplementedError("Subclasses must implement _scan_version")

    def _scan_directory_recursive(
        self, start_dir: str, filter_func: Callable[[os.DirEntry], bool]
    ) -> List[str]:
        """Recursively scan directory with os.scandir.

        Args:
            start_dir: Starting directory path
            filter_func: Function(DirEntry) -> bool to filter entries

        Returns:
            List of matching file paths
        """
        results = []

        def _scan_dir(path):
            try:
                with os.scandir(path) as entries:
                    for entry in entries:
                        try:
                            if entry.is_file(follow_symlinks=False):
                                if filter_func(entry):
                                    results.append(entry.path)
                            elif entry.is_dir(follow_symlinks=False):
                                _scan_dir(entry.path)
                        except (OSError, PermissionError):
                            # Skip inaccessible entries
                            continue
            except (OSError, PermissionError):
                # Skip inaccessible directories
                pass

        _scan_dir(start_dir)
        return results

    def _has_populated_directory(self, dir_path: str) -> bool:
        """Check if directory has entries without loading all names.

        Args:
            dir_path: Path to directory

        Returns:
            bool: True if directory has at least one entry
        """
        try:
            with os.scandir(dir_path) as it:
                return next(it, None) is not None
        except (OSError, PermissionError):
            return False


""
