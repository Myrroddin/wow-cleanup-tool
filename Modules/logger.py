from datetime import datetime

class Logger:
    """Simple logger that keeps lines and (optionally) writes to a Tk Text widget.

    Usage:
        logger = Logger()
        logger.log("Starting")
        logger.attach_text_widget(text_widget)
        logger.clear()
    """

    def __init__(self):
        self.lines = []
        self.text_widget = None

    def attach_text_widget(self, text_widget):
        """Attach a `tk.Text` widget to mirror logs into the UI."""
        self.text_widget = text_widget
        try:
            self.text_widget.configure(state="normal")
            self.text_widget.delete("1.0", "end")
            if self.lines:
                self.text_widget.insert("end", "\n".join(self.lines) + "\n")
            self.text_widget.configure(state="disabled")
        except Exception:
            # UI may not be ready; ignore errors
            pass

    def clear(self):
        """Clear stored lines and attached text widget contents."""
        self.lines = []
        if self.text_widget:
            try:
                self.text_widget.configure(state="normal")
                self.text_widget.delete("1.0", "end")
                self.text_widget.configure(state="disabled")
            except Exception:
                pass

    def log(self, text: str):
        """Add a timestamped line to the log store and update UI when attached."""
        line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}"
        self.lines.append(line)
        if self.text_widget:
            try:
                self.text_widget.configure(state="normal")
                self.text_widget.insert("end", line + "\n")
                self.text_widget.see("end")
                self.text_widget.configure(state="disabled")
            except Exception:
                pass

    def get_lines(self):
        return list(self.lines)
