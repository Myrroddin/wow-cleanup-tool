"""Utility functions for log controls (copy, save, clear, delete) for user and developer logs."""

import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from core.settings import get_user_log_file
from pathlib import Path

# User log controls


def clear_user_log(log_text):
    if log_text:
        log_text.configure(state="normal")
        log_text.delete("1.0", "end")
        log_text.configure(state="disabled")


def copy_user_log(root, log_text, loc):
    user_log = log_text.get("1.0", "end-1c")
    if user_log:
        root.clipboard_clear()
        root.clipboard_append(user_log)
        messagebox.showinfo(loc._("btn_copy_log"), loc._("log_copied"))


def save_user_log(log_text, loc):
    default_name = f"wow_cleanup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            (loc._("file_text_files"), "*.txt"),
            (loc._("file_all_files"), "*.*"),
        ],
        initialfile=default_name,
    )
    if file_path:
        try:
            user_log = log_text.get("1.0", "end-1c")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(user_log)
            messagebox.showinfo(
                loc._("btn_save_log"), loc._("btn_log_saved").format(file_path)
            )
        except Exception as e:
            messagebox.showerror(loc._("error_prefix"), str(e))


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
        messagebox.showinfo(loc._("log_delete"), loc._("status_log_deleted"))
    except Exception as e:
        messagebox.showerror(
            loc._("error_prefix"), loc._("log_delete_error").format(str(e))
        )


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
        messagebox.showinfo(loc._("btn_copy_log"), loc._("status_log_copied"))


def save_dev_log(logger, loc):
    default_name = f"wow_cleanup_dev_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            (loc._("file_text_files"), "*.txt"),
            (loc._("file_all_files"), "*.*"),
        ],
        initialfile=default_name,
    )
    if file_path:
        try:
            dev_log = logger.get_dev_log()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(dev_log)
            messagebox.showinfo(
                loc._("btn_save_log"), loc._("btn_log_saved").format(file_path)
            )
        except Exception as e:
            messagebox.showerror(loc._("error_prefix"), str(e))
