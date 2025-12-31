# BackgroundTask Utility Usage Guide

## Overview

`BackgroundTask` is a standardized utility for running I/O-heavy operations in background threads while maintaining thread-safe Tkinter UI updates.

**December 30, 2025**: Created to prevent code duplication across File Cleaner, Folder Cleaner, and Game Optimizer tabs.

## Why BackgroundTask?

### The Problem
- Tkinter's event loop runs on the main thread
- Long-running operations (file scanning, deletion) freeze the UI
- Direct threading requires careful `root.after()` usage for UI updates
- Code duplication across multiple tabs

### The Solution
BackgroundTask provides:
- ✅ Automatic background threading
- ✅ Thread-safe UI updates via `root.after()`
- ✅ Built-in error handling
- ✅ Optional progress reporting
- ✅ Consistent API across all tabs

## Basic Usage

### Simple Background Task

```python
from core.background_task import BackgroundTask

def _on_scan_files(self):
    """Scan files without freezing UI."""
    
    def do_scan():
        """Runs in background thread - do I/O here."""
        results = scanner.scan_all_versions()
        return results
    
    def on_complete(results):
        """Runs on main thread - safe to update UI."""
        self.tree.populate(results)
        self.logger.log(f"Found {len(results)} files")
    
    # Execute task in background
    BackgroundTask.run(
        self.root,
        do_scan,
        on_complete,
        logger=self.logger
    )
```

### With Custom Error Handling

```python
def _on_delete_files(self):
    """Delete files with custom error handling."""
    
    def do_delete():
        """Background: Delete selected files."""
        deleted = []
        for file in self.get_selected():
            os.remove(file)
            deleted.append(file)
        return deleted
    
    def on_complete(deleted):
        """Main thread: Update UI."""
        self.refresh_tree()
        self.logger.log(f"Deleted {len(deleted)} files")
    
    def on_error(error):
        """Main thread: Handle errors."""
        self.logger.error(f"Deletion failed: {error}")
        self.show_error_dialog(str(error))
    
    BackgroundTask.run(
        self.root,
        do_delete,
        on_complete,
        on_error=on_error
    )
```

### With Progress Updates

```python
from core.background_task import BackgroundTask

def _on_optimize_game(self):
    """Optimize game settings with progress reporting."""
    
    def do_optimize(progress):
        """Background: Optimize with progress callbacks."""
        progress("Analyzing cache...")
        cache_size = analyze_cache()
        
        progress("Cleaning temp files...")
        clean_temp()
        
        progress("Optimizing config...")
        optimize_config()
        
        return {"cache": cache_size, "status": "complete"}
    
    def on_complete(results):
        """Main thread: Show results."""
        self.logger.log(f"Optimization complete: {results}")
    
    # progress_callback runs on main thread automatically
    BackgroundTask.run_with_progress(
        self.root,
        do_optimize,
        on_progress=lambda msg: self.logger.log(msg),
        on_complete=on_complete,
        logger=self.logger
    )
```

## Current Implementation

### File Cleaner Tab
**Location**: `src/ui/main_window.py::_on_scan_files()`

```python
def _on_scan_files(self):
    def do_scan():
        # Background: Scan files using ThreadPoolExecutor (8 workers)
        backup_results = file_cleaner.scan_versions(versions)
        orphan_results = orphan_scanner.scan_versions(versions)
        return (backup_results, orphan_results)
    
    def on_complete(results):
        # Main thread: Update treeviews
        backup_results, orphan_results = results
        self.file_cleaner_tab.populate_backup_tree(backup_results)
        self.file_cleaner_tab.populate_orphan_tree(orphan_results)
    
    BackgroundTask.run(self.root, do_scan, on_complete, logger=self.logger)
```

## Future Usage Examples

### Folder Cleaner Tab (To Be Implemented)

```python
def _on_clean_folders(self):
    """Clean cache/screenshots/etc folders."""
    
    def do_clean():
        cleaner = FolderCleaner(logger=self.logger)
        results = cleaner.clean_all(
            cache=self.cache_checkbox.get(),
            screenshots=self.screenshots_checkbox.get(),
            logs=self.logs_checkbox.get()
        )
        return results
    
    def on_complete(results):
        self.stats_label.config(text=f"Freed {results['size_mb']} MB")
        self.logger.log(f"Cleaned {results['files']} files")
    
    BackgroundTask.run(self.root, do_clean, on_complete, logger=self.logger)
```

### Game Optimizer Tab (To Be Implemented)

```python
def _on_optimize(self):
    """Optimize game performance settings."""
    
    def do_optimize(progress):
        optimizer = GameOptimizer(logger=self.logger)
        
        progress("Detecting hardware...")
        specs = optimizer.detect_hardware()
        
        progress("Calculating optimal settings...")
        settings = optimizer.calculate_settings(specs)
        
        progress("Applying configuration...")
        optimizer.apply_settings(settings)
        
        return settings
    
    def on_complete(settings):
        self.settings_display.update(settings)
        self.logger.log("Optimization complete")
    
    BackgroundTask.run_with_progress(
        self.root,
        do_optimize,
        on_progress=lambda msg: self.progress_label.config(text=msg),
        on_complete=on_complete,
        logger=self.logger
    )
```

## Thread Safety Rules

### ✅ Safe in Background Task (`do_scan` function)
- File I/O (reading, writing, deleting)
- Network requests
- Heavy computation
- Calling `logger.log()` (logger is thread-safe)
- Returning data to main thread

### ❌ Unsafe in Background Task
- **NEVER** update Tkinter widgets directly
- **NEVER** call widget methods (`.config()`, `.pack()`, etc.)
- **NEVER** modify UI state

### ✅ Safe in Callbacks (`on_complete`, `on_error`)
- Update Tkinter widgets (runs on main thread)
- Populate treeviews
- Show dialogs
- Call `logger.log()`
- Modify UI state

## Error Handling Hierarchy

1. **Custom error handler** (highest priority)
   ```python
   BackgroundTask.run(root, task, on_complete, on_error=my_handler)
   ```

2. **Logger fallback**
   ```python
   BackgroundTask.run(root, task, on_complete, logger=logger)
   # Logs: "Background task error: <exception>"
   ```

3. **Re-raise on main thread** (if no handler/logger)
   - Error will appear in console/crash reporter

## Performance Notes

### Current Threading Model
```
Main Thread (Tkinter event loop)
  └─> BackgroundTask.run() starts daemon thread
       └─> Task function executes
            └─> ThreadPoolExecutor (8 workers) for parallel I/O
                 └─> Individual file operations
       └─> Completion callback scheduled via root.after(0)
            └─> UI updates on main thread
```

### Worker Count Recommendations
- **File scanning**: 8 workers (optimal for SSDs)
- **File deletion**: 4-8 workers (safer for write operations)
- **Network operations**: 4 workers (avoid overwhelming servers)
- **CPU-bound tasks**: `os.cpu_count()` workers

### Memory Considerations
- Background task returns data, not widgets
- Large result sets (>10k items) should be paginated
- Progress callbacks minimize memory for status updates

## Migration Guide

### Before (Manual Threading)
```python
def _on_scan(self):
    import threading
    
    def thread_func():
        try:
            results = do_scan()
            self.root.after(0, lambda: self.update_ui(results))
        except Exception as e:
            self.root.after(0, lambda: self.logger.error(str(e)))
    
    thread = threading.Thread(target=thread_func, daemon=True)
    thread.start()
```

### After (BackgroundTask)
```python
def _on_scan(self):
    def do_scan():
        return scan_all()
    
    def on_complete(results):
        self.update_ui(results)
    
    BackgroundTask.run(self.root, do_scan, on_complete, logger=self.logger)
```

**Benefits**:
- 60% less code
- No manual `root.after()` management
- Consistent error handling
- Easier to test and maintain

## Testing Considerations

### Mock Background Tasks
```python
# In tests, you can mock BackgroundTask.run to execute synchronously
with patch('core.background_task.BackgroundTask.run') as mock_run:
    def sync_run(root, task, on_complete, **kwargs):
        result = task()
        if on_complete:
            on_complete(result)
    
    mock_run.side_effect = sync_run
    
    # Now test UI code without threading complexity
    tab._on_scan_files()
```

## Best Practices

1. **Keep tasks pure**: Return data, don't modify UI
2. **Use progress for long operations**: Users want feedback
3. **Handle errors gracefully**: Always provide logger or error handler
4. **Avoid closures capturing widgets**: Pass data, not references
5. **Document thread context**: Comment which thread each function runs on

## December 30, 2025 Status

**Implemented**:
- ✅ BackgroundTask utility class
- ✅ File Cleaner tab scanning (refactored to use BackgroundTask)

**Pending**:
- ⏳ File deletion (`_on_remove_selected`)
- ⏳ Folder Cleaner tab operations
- ⏳ Game Optimizer tab operations

All future I/O operations should use BackgroundTask for consistency.
