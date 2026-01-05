# BackgroundTask Utility Guide

## Overview

`BackgroundTask` runs I/O-heavy operations in background threads with thread-safe Tkinter UI updates. Prevents code duplication across tabs.

**See also**: [LOGGING_GUIDE.md](LOGGING_GUIDE.md) for logging within background tasks.

## Why Use It?
**Problem:** Tkinter's event loop runs on main thread; long operations freeze UI; manual threading requires careful `root.after()` usage.

**Solution:** BackgroundTask provides automatic background threading, thread-safe UI updates, built-in error handling, progress reporting, and consistent API.

## Basic Usage

### Simple Task
```python
from core.background_task import BackgroundTask

def _on_scan_files(self):
    def do_scan():
        # Background thread: I/O operations
        return scanner.scan_all_versions()
    
    def on_complete(results):
        # Main thread: UI updates
        self.tree.populate(results)
        self.logger.log(f"Found {len(results)} files")
    
    BackgroundTask.run(self.root, do_scan, on_complete, logger=self.logger)
```

### With Custom Error Handler
```python
def _on_delete_files(self):
    def do_delete():
        return [os.remove(f) for f in self.get_selected()]
    
    def on_complete(deleted):
        self.refresh_tree()
    
    def on_error(error):
        self.logger.error(f"Deletion failed: {error}")
        self.show_error_dialog(str(error))
    
    BackgroundTask.run(self.root, do_delete, on_complete, on_error=on_error)
```

### With Progress Updates
```python
def _on_optimize_game(self):
    def do_optimize(progress):
        progress("Analyzing cache...")
        cache = analyze_cache()
        progress("Cleaning temp files...")
        clean_temp()
        return cache
    
    BackgroundTask.run_with_progress(
        self.root,
        do_optimize,
        on_progress=lambda msg: self.logger.log(msg),
        on_complete=lambda r: self.logger.log("Done"),
        logger=self.logger
    )
```

## Thread Safety Rules

### ✅ Safe in Background (`do_scan`)
- File I/O, network, computation
- `logger.log()` (thread-safe)
- Return data to main thread

### ❌ Never in Background
- Tkinter widget updates (`.config()`, `.pack()`, etc.)
- Widget method calls
- UI state modification

### ✅ Safe in Callbacks (`on_complete`, `on_error`)
- Update widgets (runs on main thread)
- Populate trees, show dialogs
- Modify UI state

## Error Handling Hierarchy
1. Custom error handler: `on_error=my_handler`
2. Logger fallback: `logger=logger` (logs "Background task error: ...")
3. Re-raise on main thread (console/crash)

## Performance

**Threading Model:**
```
Main Thread → BackgroundTask (daemon thread)
  → Task → ThreadPoolExecutor (8 workers)
    → Individual operations
  → root.after(0) → Callback on main thread
```

**Worker Recommendations:**
- File scanning: 8 (optimal for SSDs)
- File deletion: 4-8 (safer writes)
- Network: 4 (avoid overwhelming servers)
- CPU-bound: `os.cpu_count()`

## Migration Example

**Before (Manual):**
```python
def _on_scan(self):
    def thread_func():
        try:
            results = do_scan()
            self.root.after(0, lambda: self.update_ui(results))
        except Exception as e:
            self.root.after(0, lambda: self.logger.error(str(e)))
    threading.Thread(target=thread_func, daemon=True).start()
```

**After (BackgroundTask):**
```python
def _on_scan(self):
    BackgroundTask.run(
        self.root, 
        lambda: scan_all(), 
        lambda r: self.update_ui(r), 
        logger=self.logger
    )
```

**Benefits:** 60% less code, no manual `root.after()`, consistent error handling.

## Best Practices
1. Keep tasks pure: Return data, don't modify UI
2. Use progress for long operations (>2s)
3. Always provide logger or error handler
4. Avoid closures capturing widgets
5. Document thread context in comments
