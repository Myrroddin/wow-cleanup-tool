"""User Log Tab UI for WoW Cleanup Tool."""

import tkinter as tk
from tkinter import ttk


class LogTab:
    def __init__(self, parent, loc, log_controls, append_log_var=None, font_size=12):
        # Reduce top padding to align description closer to tab header
        self.frame = ttk.Frame(parent, padding=(0, 5, 5, 5))
        self.append_log_var = append_log_var
        self.original_btn_style = None  # Store original button configuration
        self.font_size = font_size
        self._configure_timer = None  # Debounce timer for configure events
        self._create_content(loc, log_controls)

        # Set up trace to update delete button state when append mode changes
        if self.append_log_var:
            self.append_log_var.trace_add(
                "write", lambda *args: self._update_delete_button_state()
            )
            self._update_delete_button_state()  # Set initial state

    def _create_content(self, loc, log_controls):
        # Description label with dynamic wraplength based on widget width
        self.desc_label = ttk.Label(
            self.frame,
            text=loc._("desc_user_log"),
            justify="left",
        )
        self.desc_label.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        # Bind to configure event with debouncing to reduce flicker
        self.desc_label.bind("<Configure>", self._debounced_update_wraplength)

        # Controls row - buttons in container frame
        controls = ttk.Frame(self.frame)
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        clear_btn = ttk.Button(
            controls, text=loc._("btn_clear_log"), command=log_controls["clear"]
        )
        clear_btn.grid(row=0, column=0, padx=(0, 8))

        # Add tooltip to clear button
        from ui.widgets.tooltip import Tooltip
        from core.themes import THEMES

        def setup_clear_tooltip():
            def on_enter(e):
                theme_name = self.settings.get("theme", "light")
                theme = THEMES.get(theme_name, THEMES["light"])
                t = Tooltip(
                    clear_btn,
                    loc._("tooltip_clear_log"),
                    theme,
                    self.settings.get("font_family", "TkDefaultFont"),
                    int(self.settings.get("font_size", 12)),
                )
                t.show()
                clear_btn._tip = t

            def on_leave(e):
                if hasattr(clear_btn, "_tip"):
                    clear_btn._tip.hide()

            clear_btn.bind("<Enter>", on_enter)
            clear_btn.bind("<Leave>", on_leave)

        setup_clear_tooltip()

        self.delete_btn = ttk.Button(
            controls,
            text=loc._("btn_clear_persistent_log"),
            command=log_controls["delete"],
        )
        self.delete_btn.grid(row=0, column=1, padx=(0, 8))

        # Add tooltip to delete button
        def setup_delete_tooltip():
            def on_enter(e):
                theme_name = self.settings.get("theme", "light")
                theme = THEMES.get(theme_name, THEMES["light"])
                t = Tooltip(
                    self.delete_btn,
                    loc._("tooltip_clear_persistent_log"),
                    theme,
                    self.settings.get("font_family", "TkDefaultFont"),
                    int(self.settings.get("font_size", 12)),
                )
                t.show()
                self.delete_btn._tip = t

            def on_leave(e):
                if hasattr(self.delete_btn, "_tip"):
                    self.delete_btn._tip.hide()

            self.delete_btn.bind("<Enter>", on_enter)
            self.delete_btn.bind("<Leave>", on_leave)

        setup_delete_tooltip()

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
        # Calculate height based on font size (18 rows at 12pt → 1.5x scaling)
        text_height = int(18 * (self.font_size / 12))
        self.log_text = tk.Text(
            self.frame, wrap="word", height=text_height, width=80, state="disabled"
        )
        self.log_text.grid(row=2, column=0, sticky="nsew")

        # Configure expansion
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def _update_wraplength(self, event=None):
        """Update wraplength based on actual widget width."""
        if hasattr(self, "desc_label"):
            # Get actual widget width, subtract padding for margins
            width = self.desc_label.winfo_width()
            if width > 1:  # Ensure widget is actually rendered
                self.desc_label.configure(wraplength=max(width - 20, 100))

    def _debounced_update_wraplength(self, event=None):
        """Debounce wraplength updates to reduce flicker during resize."""
        # Cancel existing timer if any
        if self._configure_timer:
            self.frame.after_cancel(self._configure_timer)
        # Schedule update after 50ms of no resize events
        self._configure_timer = self.frame.after(50, self._update_wraplength)

    def refresh_wraplength(self, font_size):
        """Update description label wraplength when font size changes."""
        self.font_size = font_size
        # Trigger a wraplength update based on current width
        self._update_wraplength()

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
