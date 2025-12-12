"""Single instance lock management for WoW Cleanup Tool."""

import os
import sys
import tempfile
import atexit


class SingleInstance:
    """Ensures only one instance of the application runs at a time."""

    def __init__(self, app_name="wow_cleanup_tool"):
        """Initialize single instance lock.

        Args:
            app_name: Name used for the lock file
        """
        self.app_name = app_name
        self.lock_file = os.path.join(tempfile.gettempdir(), f"{app_name}.lock")
        self.locked = False
        self.fp = None

        # Register cleanup on exit
        atexit.register(self.release)

    def acquire(self):
        """Acquire single instance lock.

        Returns:
            bool: True if lock acquired successfully, False if another instance is running
        """
        try:
            # Try to open the lock file for writing
            self.fp = open(self.lock_file, "w")

            # Platform-specific file locking
            if sys.platform == "win32":
                import msvcrt

                try:
                    msvcrt.locking(self.fp.fileno(), msvcrt.LK_NBLCK, 1)
                    self.fp.write(str(os.getpid()))
                    self.fp.flush()
                    self.locked = True
                    return True
                except (IOError, OSError):
                    # Lock is held by another process
                    self.fp.close()
                    self.fp = None
                    return False
            else:
                # Unix-like systems
                import fcntl

                try:
                    fcntl.flock(self.fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self.fp.write(str(os.getpid()))
                    self.fp.flush()
                    self.locked = True
                    return True
                except (IOError, OSError):
                    # Lock is held by another process
                    self.fp.close()
                    self.fp = None
                    return False
        except (OSError, IOError):
            return False

    def release(self):
        """Release single instance lock."""
        if not self.locked:
            return

        try:
            if self.fp:
                # Platform-specific unlock
                if sys.platform == "win32":
                    import msvcrt

                    try:
                        msvcrt.locking(self.fp.fileno(), msvcrt.LK_UNLCK, 1)
                    except (IOError, OSError):
                        pass
                else:
                    # Unix-like systems
                    import fcntl

                    try:
                        fcntl.flock(self.fp.fileno(), fcntl.LOCK_UN)
                    except (IOError, OSError):
                        pass

                self.fp.close()
                self.fp = None

            # Remove lock file
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)

            self.locked = False
        except (OSError, IOError):
            pass

    def __enter__(self):
        """Context manager entry."""
        if not self.acquire():
            sys.exit(0)  # Silently exit if another instance is running
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()
        return False
