import tkinter as tk
from tkinter import ttk
from Modules import localization
from Modules.themes import THEMES

def show_startup_warning(root, settings, save_settings_fn, logger=None):
    """Show the startup warning popup.

    Parameters:
        root: Tk root window
        settings: dict-like settings object (modified in-place)
        save_settings_fn: callable(settings) -> None to persist settings
        logger: optional logger with .log(str) method
    """
    _ = localization.get_text
    if settings.get("hide_warning", False):
        return

    # Get current theme
    theme = settings.get("theme", "light")
    theme_data = THEMES.get(theme, THEMES["light"])

    popup = tk.Toplevel(root)
    popup.title(_("important_notice"))
    popup.resizable(False, False)
    popup.configure(bg=theme_data["bg"])
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
        text=_("startup_warning_text"),
        wraplength=pw - 24, justify="left"
    ).pack(pady=(0, 12))

    never_show_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(frm, text=_("do_not_show_again"), variable=never_show_var).pack(anchor="w")

    def _dismiss():
        if never_show_var.get():
            try:
                settings["hide_warning"] = True
                save_settings_fn(settings)
                if logger:
                    try: logger.log(_("user_disabled_warning"))
                    except Exception: pass
            except Exception:
                pass
        popup.destroy()

    ttk.Button(frm, text=_("ok"), command=_dismiss).pack(pady=(12, 0))
