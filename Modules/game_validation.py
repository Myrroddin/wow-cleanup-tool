import os
import tkinter as tk
from tkinter import ttk, messagebox

def is_game_version_valid(version_path):
    """Check if a game version path contains required folders (Interface, WTF).

    Returns:
        bool: True if both Interface and WTF folders exist, False otherwise.
    """
    if not version_path or not os.path.isdir(version_path):
        return False
    interface_path = os.path.join(version_path, "Interface")
    wtf_path = os.path.join(version_path, "WTF")
    return os.path.isdir(interface_path) and os.path.isdir(wtf_path)

def show_game_validation_warning(root):
    """Show a popup warning that the game needs to be run at least once.

    Parameters:
        root: Tk root window for the warning popup.
    """
    messagebox.showwarning(
        "Invalid Game Installation",
        "The World of Warcraft installation appears incomplete.\n\n"
        "Please run the game at least once to initialize the Interface and WTF folders.\n\n"
        "After running the game, you can use this tool to clean up your installation."
    )
