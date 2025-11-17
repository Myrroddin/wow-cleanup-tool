import tkinter as tk
from tkinter import ttk

def show_startup_warning(root, settings, save_settings_fn, logger=None):
    """Show the startup warning popup.

    Parameters:
        root: Tk root window
        settings: dict-like settings object (modified in-place)
        save_settings_fn: callable(settings) -> None to persist settings
        logger: optional logger with .log(str) method
    """
    if settings.get("hide_warning", False):
        return

    popup = tk.Toplevel(root)
    popup.title("Important Notice")
    popup.resizable(False, False)
    pw, ph = 460, 210
    root.update_idletasks()
    try:
        mw = root.winfo_width(); mh = root.winfo_height()
        mx = root.winfo_x(); my = root.winfo_y()
        px = mx + (mw // 2) - (pw // 2); py = my + (mh // 2) - (ph // 2)
    except Exception:
        sw = root.winfo_screenwidth(); sh = root.winfo_screenheight()
        px = (sw // 2) - (pw // 2); py = (sh // 2) - (ph // 2)
    popup.geometry(f"{pw}x{ph}+{px}+{py}")
    popup.transient(root); popup.grab_set()

    frm = ttk.Frame(popup, padding=12); frm.pack(fill="both", expand=True)
    ttk.Label(
        frm,
        text=("⚠️ Please ensure World of Warcraft is completely closed before using this tool.\n\n"
              "Running the tool while WoW is open could interfere with the game's files."),
        wraplength=pw - 48, justify="left"
    ).pack(pady=(0, 12))

    never_show_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(frm, text="Do not show this warning again", variable=never_show_var).pack(anchor="w")

    def _dismiss():
        if never_show_var.get():
            try:
                settings["hide_warning"] = True
                save_settings_fn(settings)
                if logger:
                    try: logger.log("User disabled startup warning.")
                    except Exception: pass
            except Exception:
                pass
        popup.destroy()

    ttk.Button(frm, text="OK", command=_dismiss).pack(pady=(12, 0))
