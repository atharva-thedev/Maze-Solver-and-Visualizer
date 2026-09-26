"""
main.py - Application Entry Point for Maze Solver & Visualizer.
College-level Python Project for Pathfinding Algorithm Visualization.
"""

import sys
import tkinter as tk
from gui import MazeGUI


def main():
    """Initializes the Tkinter root window and launches the application."""
    root = tk.Tk()

    # Enable High DPI scaling on Windows if supported
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = MazeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
