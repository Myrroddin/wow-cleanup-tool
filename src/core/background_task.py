"""Background task executor for thread-safe UI operations.

December 30, 2025: Utility class to standardize background threading across tabs.
Ensures Tkinter UI remains responsive during I/O-heavy operations while maintaining
thread-safe updates via root.after().
"""

import threading
from typing import Callable, Optional, Any


class BackgroundTask:
    """Execute long-running operations in background threads with safe UI updates.

    December 30, 2025: Designed to prevent UI freezing during file scanning,
    deletion, and other I/O-heavy operations while ensuring all Tkinter widget
    updates occur on the main thread.

    Example usage:
        def do_scan():
            results = scanner.scan_versions(versions)
            return results

        def on_complete(results):
            self.tree.populate(results)
            logger.log("Scan complete")

        BackgroundTask.run(root, do_scan, on_complete, logger)
    """

    @staticmethod
    def run(
        root,
        task: Callable[[], Any],
        on_complete: Optional[Callable[[Any], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        logger=None,
    ):
        """Execute task in background thread with thread-safe callbacks.

        December 30, 2025: Main entry point for background operations. Task runs
        in daemon thread; callbacks execute on main thread via root.after().

        Args:
            root: Tkinter root window (required for thread-safe UI updates)
            task: Callable to execute in background (should return results)
            on_complete: Optional callback for successful completion (receives task result)
            on_error: Optional callback for errors (receives Exception)
            logger: Optional logger for default error handling

        Thread Safety:
            - task() runs in background daemon thread
            - on_complete() and on_error() run on main thread
            - Safe to update Tkinter widgets in callbacks
        """

        def thread_wrapper():
            """Background thread wrapper with exception handling."""
            try:
                # December 30, 2025: Execute task in background thread
                result = task()

                # December 30, 2025: Schedule completion callback on main thread
                if on_complete:
                    root.after(0, lambda: on_complete(result))

            except Exception as e:
                # December 30, 2025: Handle errors on main thread
                if on_error:
                    root.after(0, lambda: on_error(e))
                elif logger:
                    # Default error logging if no custom handler
                    root.after(0, lambda: logger.error(f"Background task error: {e}"))
                else:
                    # Fallback: re-raise on main thread for visibility
                    root.after(0, lambda: (_ for _ in ()).throw(e))

        # December 30, 2025: Start daemon thread (auto-terminates with app)
        thread = threading.Thread(target=thread_wrapper, daemon=True)
        thread.start()

    @staticmethod
    def run_with_progress(
        root,
        task: Callable[[Callable[[str], None]], Any],
        on_progress: Callable[[str], None],
        on_complete: Optional[Callable[[Any], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        logger=None,
    ):
        """Execute task with progress updates.

        December 30, 2025: Extended version supporting progress callbacks for
        long-running operations that report status updates.

        Args:
            root: Tkinter root window
            task: Callable accepting progress callback, returns results
            on_progress: Callback for progress updates (receives status string)
            on_complete: Optional callback for successful completion
            on_error: Optional callback for errors
            logger: Optional logger for default error handling

        Example:
            def do_scan(progress_callback):
                progress_callback("Scanning version 1...")
                results1 = scan_v1()
                progress_callback("Scanning version 2...")
                results2 = scan_v2()
                return [results1, results2]

            BackgroundTask.run_with_progress(
                root, do_scan, lambda msg: logger.log(msg), on_complete, logger
            )
        """

        def progress_wrapper(message: str):
            """Thread-safe progress callback."""
            root.after(0, lambda: on_progress(message))

        def thread_wrapper():
            """Background thread wrapper with progress support."""
            try:
                # December 30, 2025: Pass thread-safe progress callback to task
                result = task(progress_wrapper)

                # December 30, 2025: Schedule completion on main thread
                if on_complete:
                    root.after(0, lambda: on_complete(result))

            except Exception as e:
                # December 30, 2025: Handle errors on main thread
                if on_error:
                    root.after(0, lambda: on_error(e))
                elif logger:
                    root.after(0, lambda: logger.error(f"Background task error: {e}"))
                else:
                    root.after(0, lambda: (_ for _ in ()).throw(e))

        # December 30, 2025: Start daemon thread
        thread = threading.Thread(target=thread_wrapper, daemon=True)
        thread.start()
