import os
import tkinter as tk
from tkinter import ttk

try:
    from PIL import Image, ImageTk
except Exception:
    Image = ImageTk = None

def build_single_version_tab(app, tab, version_path, version_label):
    outer = ttk.Frame(tab, padding=10)
    outer.pack(fill="both", expand=True)

    # Controls row: toggles side-by-side + Process button at end
    controls = ttk.Frame(outer)
    controls.pack(fill="x")

    folder_vars = {}
    toggle_container = ttk.Frame(controls)
    toggle_container.pack(side="left", fill="x", expand=True)

    targets = {
        "Screenshots": os.path.join(version_path, "Screenshots"),
        "Logs": os.path.join(version_path, "Logs"),
        "Errors": os.path.join(version_path, "Errors"),
        "Cache": os.path.join(version_path, "Cache"),
    }

    # Store paths for later use in _process_selected_folders
    app.folder_paths[version_label] = {
        name: path for name, path in targets.items() if os.path.isdir(path)
    }

    # Master "Select/Deselect All"
    master_var = tk.BooleanVar(value=False)
    master = app.__class__.__module__  # placeholder to use ImgCheckbox from app
    # Use the same ImgCheckbox previously used in the UI
    from Modules.ui_helpers import ImgCheckbox
    master_cb = ImgCheckbox(toggle_container, "Select / Deselect All Folders", master_var, app.assets)
    master_cb.pack(side="left", padx=(0,10), pady=4)
    master_var.trace_add("write", lambda *_: app._toggle_all_folders(folder_vars))

    # Place folder toggles side-by-side (except Screenshots handled below)
    app.styled_folder_boxes = getattr(app, "styled_folder_boxes", [])
    for name, path in targets.items():
        if name == "Screenshots":
            continue
        if os.path.isdir(path):
            var = tk.BooleanVar(value=False)
            cb = ImgCheckbox(toggle_container, f"{name}", var, app.assets)
            cb.pack(side="left", padx=(0,10), pady=4)
            folder_vars[name] = (var, path, cb)
            app.styled_folder_boxes.append(cb)

    # Process button aligned right on same line
    ttk.Button(controls, text="Process Selected Folders",
               command=lambda: app._process_selected_folders(version_label, folder_vars)).pack(side="right", padx=(10,0), pady=4)

    # Screenshots panel (unchanged)
    shot_panel = ttk.LabelFrame(outer, text="Screenshots (per-file actions)", padding=8)
    shot_panel.pack(fill="both", expand=True, pady=(8, 0))

    shots_left = ttk.Frame(shot_panel); shots_left.pack(side="left", fill="both", expand=True)
    shots_right = ttk.Frame(shot_panel); shots_right.pack(side="left", fill="both", expand=True, padx=(10, 0))

    shots_canvas = tk.Canvas(shots_left)
    shots_scroll = ttk.Scrollbar(shots_left, orient="vertical", command=shots_canvas.yview)
    shots_frame = ttk.Frame(shots_canvas)
    shots_frame.bind("<Configure>", lambda e: shots_canvas.configure(scrollregion=shots_canvas.bbox("all")))
    shots_canvas.create_window((0, 0), window=shots_frame, anchor="nw")
    shots_canvas.configure(yscrollcommand=shots_scroll.set)
    shots_canvas.pack(side="left", fill="both", expand=True)
    shots_scroll.pack(side="right", fill="y")

    shots_controls = ttk.Frame(outer); shots_controls.pack(fill="x", pady=(6, 0))
    shots_select_all_var = tk.BooleanVar(value=False)
    shots_selall = ImgCheckbox(shots_controls, "Select / Deselect All Screenshot Files", shots_select_all_var, app.assets)
    shots_selall.pack(side="left")
    shots_vars = {}
    shots_select_all_var.trace_add("write", lambda *_: app._toggle_all_screenshot_files(shots_vars))

    preview_label = ttk.Label(shots_right, text="Preview", anchor="center"); preview_label.pack(anchor="n")
    preview_canvas = tk.Canvas(shots_right, width=220, height=220, highlightthickness=1)
    preview_canvas.pack(fill="both", expand=False, pady=(6, 0))
    preview_canvas._img_ref = None

    app.styled_shot_boxes = getattr(app, "styled_shot_boxes", [])
    shot_folder = targets.get("Screenshots")
    if shot_folder and os.path.isdir(shot_folder):
        files = []
        try:
            for fname in os.listdir(shot_folder):
                fp = os.path.join(shot_folder, fname)
                if os.path.isfile(fp) and fname.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tga", ".gif")):
                    files.append(fp)
        except Exception:
            files = []
        files.sort(key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0, reverse=True)
        for fp in files:
            var = tk.BooleanVar(value=False)
            cb = ImgCheckbox(shots_frame, fp, var, app.assets)
            cb.pack(anchor="w", fill="x", padx=4, pady=1)
            cb.bind("<ButtonRelease-1>", lambda e, p=fp: show_preview(app, preview_canvas, p))
            app.styled_shot_boxes.append(cb)
            shots_vars[fp] = var
    else:
        ttk.Label(shots_frame, text="Screenshots folder not found for this version.").pack(anchor="w")

    return {"folder_vars": folder_vars, "shots_vars": shots_vars, "preview_canvas": preview_canvas}

def show_preview(app, canvas: tk.Canvas, path: str):
    if not Image or not ImageTk or not path or not os.path.exists(path):
        canvas.delete("all"); canvas._img_ref = None; return
    try:
        img = Image.open(path)
        canvas.update_idletasks()
        cw = max(200, int(canvas.winfo_width()))
        ch = max(200, int(canvas.winfo_height()))
        img.thumbnail((cw, ch))
        tkimg = ImageTk.PhotoImage(img)
        canvas.delete("all")
        cx, cy = cw // 2, ch // 2
        canvas.create_image(cx, cy, image=tkimg)
        canvas._img_ref = tkimg
    except Exception:
        canvas.delete("all"); canvas._img_ref = None
