"""Utility functions for log controls (copy, clear, delete, open folder) for user and developer logs."""

import tkinter as tk
from tkinter import messagebox
import os
import sys
import subprocess
from core.settings import get_user_log_file
from pathlib import Path

# User log controls


def clear_user_log(log_text, logger=None):
    """Clear the user log display and optionally delete the file.

    Args:
        log_text: The text widget to clear
        logger: WoWLogger instance to check append mode

    Behavior:
        - Append mode OFF: Clears display AND deletes log file (session-only log)
        - Append mode ON: Clears display only (preserves persistent log file)
    """
    if log_text:
        log_text.configure(state="normal")
        log_text.delete("1.0", "end")
        log_text.configure(state="disabled")

    # If append mode is OFF, delete the log file (it's session-only)
    if logger and hasattr(logger, "_append_mode") and not logger._append_mode:
        log_file = get_user_log_file()
        if log_file.exists():
            try:
                log_file.unlink()
            except Exception:
                pass  # Silent fail - file might be locked


def copy_user_log(root, log_text, loc):
    user_log = log_text.get("1.0", "end-1c")
    if user_log:
        root.clipboard_clear()
        root.clipboard_append(user_log)
        messagebox.showinfo(loc._("btn_copy_log"), loc._("btn_copy_log"))


def open_log_folder():
    """Open the folder containing log files in the system file manager."""
    log_folder = get_user_log_file().parent

    # Ensure folder exists
    log_folder.mkdir(parents=True, exist_ok=True)

    try:
        if sys.platform == "win32":
            os.startfile(log_folder)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(log_folder)])
        else:
            subprocess.run(["xdg-open", str(log_folder)])
    except Exception:
        pass


def delete_user_log(settings, loc):
    log_file = get_user_log_file()
    if not log_file.exists():
        return
    try:
        delete_mode = settings.get("delete_mode", "trash")
        if delete_mode == "trash":
            from send2trash import send2trash

            send2trash(str(log_file))
        else:
            log_file.unlink()
        messagebox.showinfo(loc._("status_log_deleted"), "Log file deleted.")
    except Exception as e:
        messagebox.showerror(loc._("error_prefix"), str(e))


# Developer log controls


def clear_dev_log(dev_text):
    if dev_text:
        dev_text.configure(state="normal")
        dev_text.delete("1.0", "end")
        dev_text.configure(state="disabled")


def copy_dev_log(root, logger, loc):
    dev_log = logger.get_dev_log()
    if dev_log:
        root.clipboard_clear()
        root.clipboard_append(dev_log)
        messagebox.showinfo(loc._("btn_copy_log"), loc._("btn_copy_log"))
