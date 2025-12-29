"""User Log Tab UI for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk


class LogTab:
    def __init__(self, parent, loc, log_controls, append_log_var=None):
        # Reduce top padding to align description closer to tab header
        self.frame = ttk.Frame(parent, padding=(0, 5, 5, 5))
        self.append_log_var = append_log_var
        self.original_btn_style = None  # Store original button configuration
        self._create_content(loc, log_controls)

        # Set up trace to update delete button state when append mode changes
        if self.append_log_var:
            self.append_log_var.trace_add(
                "write", lambda *args: self._update_delete_button_state()
            )
            self._update_delete_button_state()  # Set initial state

    def _create_content(self, loc, log_controls):
        # Description label
        desc_label = ttk.Label(
            self.frame,
            text=loc._("desc_user_log"),
            justify="left",
            wraplength=600,
        )
        desc_label.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        # Controls row - buttons in container frame
        controls = ttk.Frame(self.frame)
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        clear_btn = ttk.Button(
            controls, text=loc._("btn_clear_log"), command=log_controls["clear"]
        )
        clear_btn.grid(row=0, column=0, padx=(0, 8))

        self.delete_btn = ttk.Button(
            controls,
            text=loc._("btn_clear_persistent_log"),
            command=log_controls["delete"],
        )
        self.delete_btn.grid(row=0, column=1, padx=(0, 8))

        # Create overlay using ttk.Label with custom style for dimming
        # This will be placed exactly over the button when disabled
        style = ttk.Style()
        bg = style.lookup("TFrame", "background")
        style.configure(
            "DimmedOverlay.TLabel",
            foreground="#888888",  # Dim gray text
            background=bg,
            anchor="center",
        )

        self.delete_btn_overlay = ttk.Label(
            controls,
            text=loc._("btn_clear_persistent_log"),
            style="DimmedOverlay.TLabel",
            cursor="arrow",
        )

        open_folder_btn = ttk.Button(
            controls,
            text=loc._("btn_open_log_folder"),
            command=log_controls["open_folder"],
        )
        open_folder_btn.grid(row=0, column=2, padx=(0, 8))

        copy_btn = ttk.Button(
            controls, text=loc._("btn_copy_log"), command=log_controls["copy"]
        )
        copy_btn.grid(row=0, column=3)

        # Log display area
        self.log_text = tk.Text(
            self.frame, wrap="word", height=18, width=80, state="disabled"
        )
        self.log_text.grid(row=2, column=0, sticky="nsew")

        # Configure expansion
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def _update_delete_button_state(self):
        """Enable or disable the delete button based on append mode.

        Delete button is only enabled when append mode is ON (persistent logging).
        When append mode is OFF, the button is disabled and shown with dim overlay.
        """
        if self.append_log_var and self.delete_btn:
            if self.append_log_var.get():
                # Enabled: show normal button, hide overlay
                self.delete_btn.config(state="normal")
                self.delete_btn_overlay.place_forget()
            else:
                # Disabled: disable button and show overlay positioned exactly over it
                self.delete_btn.config(state="disabled")
                # Position overlay exactly over the button using place()
                # This ensures perfect geometry matching
                self.delete_btn_overlay.place(
                    in_=self.delete_btn, x=0, y=0, relwidth=1.0, relheight=1.0
                )
