"""
gui.py - Modern Tkinter User Interface for Maze Solver & Visualizer.
Provides interactive controls, canvas rendering, educational algorithm cards,
real-time statistics, and side-by-side algorithm comparison.
"""

import time
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Tuple, Dict, Any

from maze import Maze
from generator import MazeGenerator
from visualizer import MazeVisualizer
from algorithms import solve_instant
from utils import (
    COLORS, GRID_SIZES, ANIMATION_SPEEDS, ALGORITHM_INFO, MAZE_TYPES,
    format_time, WALL, EMPTY, START, END
)


class MazeGUI:
    """Main GUI Application Window for Maze Solver & Visualizer."""

    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("Maze Solver & Visualizer — Pathfinding Algorithms Visualized")
        self.root.geometry("1280x820")
        self.root.minsize(1050, 700)
        self.root.configure(bg=COLORS["bg_main"])

        # Data Models & Visualizer
        default_size = "Medium (25x25)"
        rows, cols, _ = GRID_SIZES[default_size]
        self.maze: Maze = Maze(rows, cols)
        
        # Click Mode: "wall", "start", "end"
        self.click_mode = tk.StringVar(value="wall")
        self.is_mouse_down = False
        self.mouse_draw_mode: Optional[bool] = None # True for wall, False for erase
        
        # Control Variables
        self.selected_algo = tk.StringVar(value="A* (A-Star) Algorithm")
        self.selected_size = tk.StringVar(value=default_size)
        self.selected_maze_type = tk.StringVar(value="Recursive Backtracker (DFS Maze)")
        self.selected_speed = tk.StringVar(value="Medium")

        # Setup Theme Styles
        self._configure_styles()

        # Build UI Components
        self._create_header()
        self._create_main_content()
        self._create_status_bar()

        # Generate initial maze and draw
        MazeGenerator.generate(self.maze, self.selected_maze_type.get())
        self.root.update_idletasks()
        self._on_canvas_resize(None)
        self.visualizer.draw_grid()
        self._update_algorithm_info_panel()

    def _configure_styles(self) -> None:
        """Configures ttk styles with a modern dark theme palette."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # General Frames
        self.style.configure("Dark.TFrame", background=COLORS["bg_main"])
        self.style.configure("Card.TFrame", background=COLORS["bg_card"], relief="solid", borderwidth=1)
        self.style.configure("CardInner.TFrame", background=COLORS["bg_card"])

        # Label Styles
        self.style.configure("Title.TLabel",
                             background=COLORS["bg_main"],
                             foreground=COLORS["text_primary"],
                             font=("Segoe UI", 18, "bold"))
        
        self.style.configure("Subtitle.TLabel",
                             background=COLORS["bg_main"],
                             foreground=COLORS["accent_cyan"],
                             font=("Segoe UI", 10, "italic"))

        self.style.configure("CardTitle.TLabel",
                             background=COLORS["bg_card"],
                             foreground=COLORS["accent_primary"],
                             font=("Segoe UI", 11, "bold"))

        self.style.configure("Dark.TLabel",
                             background=COLORS["bg_card"],
                             foreground=COLORS["text_primary"],
                             font=("Segoe UI", 9))

        self.style.configure("Muted.TLabel",
                             background=COLORS["bg_card"],
                             foreground=COLORS["text_secondary"],
                             font=("Segoe UI", 8))

        self.style.configure("StatKey.TLabel",
                             background=COLORS["bg_card"],
                             foreground=COLORS["text_secondary"],
                             font=("Segoe UI", 9))

        self.style.configure("StatVal.TLabel",
                             background=COLORS["bg_card"],
                             foreground=COLORS["accent_secondary"],
                             font=("Segoe UI", 10, "bold"))

        # Button Styles
        self.style.configure("Primary.TButton",
                             background=COLORS["accent_primary"],
                             foreground="#1e1e2e",
                             font=("Segoe UI", 10, "bold"),
                             padding=6)
        self.style.map("Primary.TButton",
                       background=[("active", "#d4b3ff"), ("disabled", "#44475a")])

        self.style.configure("Success.TButton",
                             background=COLORS["accent_secondary"],
                             foreground="#1e1e2e",
                             font=("Segoe UI", 10, "bold"),
                             padding=6)
        self.style.map("Success.TButton",
                       background=[("active", "#7bff9d"), ("disabled", "#44475a")])

        self.style.configure("Warning.TButton",
                             background=COLORS["accent_warning"],
                             foreground="#1e1e2e",
                             font=("Segoe UI", 9, "bold"),
                             padding=5)

        self.style.configure("Danger.TButton",
                             background=COLORS["accent_danger"],
                             foreground="#ffffff",
                             font=("Segoe UI", 9, "bold"),
                             padding=5)

        self.style.configure("Secondary.TButton",
                             background="#44475a",
                             foreground=COLORS["text_primary"],
                             font=("Segoe UI", 9),
                             padding=5)
        self.style.map("Secondary.TButton",
                       background=[("active", "#6272a4"), ("disabled", "#282a36")])

        # Radio Buttons
        self.style.configure("Dark.TRadiobutton",
                             background=COLORS["bg_card"],
                             foreground=COLORS["text_primary"],
                             font=("Segoe UI", 9))

        # Comboboxes
        self.style.configure("Dark.TCombobox",
                             fieldbackground=COLORS["bg_main"],
                             background=COLORS["bg_card"],
                             foreground=COLORS["text_primary"],
                             darkcolor=COLORS["bg_card_border"],
                             lightcolor=COLORS["bg_card_border"])

    def _create_header(self) -> None:
        """Builds top header banner with title and subtitle."""
        header_frame = ttk.Frame(self.root, style="Dark.TFrame", padding=(15, 10, 15, 5))
        header_frame.pack(fill="x", side="top")

        title_lbl = ttk.Label(header_frame, text="MAZE SOLVER & VISUALIZER", style="Title.TLabel")
        title_lbl.pack(anchor="w")

        sub_lbl = ttk.Label(header_frame, text="Pathfinding Algorithms — Visualized & Analyzed", style="Subtitle.TLabel")
        sub_lbl.pack(anchor="w")

    def _create_main_content(self) -> None:
        """Builds central content layout: Left Controls, Center Canvas, Right Info & Stats."""
        content_frame = ttk.Frame(self.root, style="Dark.TFrame", padding=(10, 5, 10, 5))
        content_frame.pack(fill="both", expand=True)

        # 1. Left Control Panel (Fixed Width)
        left_panel = ttk.Frame(content_frame, style="Dark.TFrame", width=290)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        self._build_left_controls(left_panel)

        # 2. Right Info & Stats Panel (Fixed Width)
        right_panel = ttk.Frame(content_frame, style="Dark.TFrame", width=290)
        right_panel.pack(side="right", fill="y", padx=(10, 0))
        right_panel.pack_propagate(False)
        self._build_right_panel(right_panel)

        # 3. Center Canvas Area (Dynamic Expand)
        center_panel = ttk.Frame(content_frame, style="Dark.TFrame")
        center_panel.pack(side="left", fill="both", expand=True)
        self._build_center_canvas(center_panel)

    def _build_left_controls(self, parent: ttk.Frame) -> None:
        """Constructs left control cards for Maze Config, Algorithms, and Action Buttons."""
        
        # --- CARD 1: MAZE GENERATION & CONFIG ---
        maze_card = ttk.Frame(parent, style="Card.TFrame", padding=10)
        maze_card.pack(fill="x", pady=(0, 10))

        ttk.Label(maze_card, text="⚙️ Maze Configuration", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))

        # Maze Type Dropdown
        ttk.Label(maze_card, text="Maze Type Pattern:", style="Dark.TLabel").pack(anchor="w")
        self.maze_type_cb = ttk.Combobox(maze_card,
                                         textvariable=self.selected_maze_type,
                                         values=MAZE_TYPES,
                                         state="readonly",
                                         style="Dark.TCombobox")
        self.maze_type_cb.pack(fill="x", pady=(2, 8))

        # Maze Size Dropdown
        ttk.Label(maze_card, text="Grid Size:", style="Dark.TLabel").pack(anchor="w")
        self.size_cb = ttk.Combobox(maze_card,
                                    textvariable=self.selected_size,
                                    values=list(GRID_SIZES.keys()),
                                    state="readonly",
                                    style="Dark.TCombobox")
        self.size_cb.pack(fill="x", pady=(2, 10))
        self.size_cb.bind("<<ComboboxSelected>>", self._on_size_change)

        # Maze Action Buttons
        self.btn_generate = ttk.Button(maze_card, text="🎲 Generate New Maze", style="Primary.TButton", command=self._on_generate_maze)
        self.btn_generate.pack(fill="x", pady=2)

        btn_grid_frame = ttk.Frame(maze_card, style="CardInner.TFrame")
        btn_grid_frame.pack(fill="x", pady=(4, 0))

        self.btn_clear_walls = ttk.Button(btn_grid_frame, text="🧹 Clear Walls", style="Secondary.TButton", command=self._on_clear_walls)
        self.btn_clear_walls.pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.btn_reset_search = ttk.Button(btn_grid_frame, text="🔄 Reset Path", style="Secondary.TButton", command=self._on_reset_search)
        self.btn_reset_search.pack(side="right", fill="x", expand=True, padx=(2, 0))

        # --- CARD 2: ALGORITHM & VISUALIZATION ---
        algo_card = ttk.Frame(parent, style="Card.TFrame", padding=10)
        algo_card.pack(fill="x", pady=(0, 10))

        ttk.Label(algo_card, text="🧠 Algorithm & Controls", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))

        # Algorithm Selection
        ttk.Label(algo_card, text="Pathfinding Algorithm:", style="Dark.TLabel").pack(anchor="w")
        self.algo_cb = ttk.Combobox(algo_card,
                                    textvariable=self.selected_algo,
                                    values=list(ALGORITHM_INFO.keys()),
                                    state="readonly",
                                    style="Dark.TCombobox")
        self.algo_cb.pack(fill="x", pady=(2, 8))
        self.algo_cb.bind("<<ComboboxSelected>>", lambda e: self._update_algorithm_info_panel())

        # Speed Dropdown
        ttk.Label(algo_card, text="Animation Speed:", style="Dark.TLabel").pack(anchor="w")
        self.speed_cb = ttk.Combobox(algo_card,
                                     textvariable=self.selected_speed,
                                     values=list(ANIMATION_SPEEDS.keys()),
                                     state="readonly",
                                     style="Dark.TCombobox")
        self.speed_cb.pack(fill="x", pady=(2, 10))
        self.speed_cb.bind("<<ComboboxSelected>>", self._on_speed_change)

        # Primary Run Button
        self.btn_solve = ttk.Button(algo_card, text="🚀 Visualize Algorithm", style="Success.TButton", command=self._on_start_solve)
        self.btn_solve.pack(fill="x", pady=(0, 4))

        # Execution Controls (Pause / Stop)
        ctrl_frame = ttk.Frame(algo_card, style="CardInner.TFrame")
        ctrl_frame.pack(fill="x", pady=2)

        self.btn_pause = ttk.Button(ctrl_frame, text="⏸️ Pause", style="Warning.TButton", command=self._on_toggle_pause, state="disabled")
        self.btn_pause.pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.btn_stop = ttk.Button(ctrl_frame, text="🛑 Stop", style="Danger.TButton", command=self._on_stop_solve, state="disabled")
        self.btn_stop.pack(side="right", fill="x", expand=True, padx=(2, 0))

        # Compare All Button
        self.btn_compare = ttk.Button(algo_card, text="📊 Compare All Algorithms", style="Secondary.TButton", command=self._open_comparison_dialog)
        self.btn_compare.pack(fill="x", pady=(6, 0))

        # --- CARD 3: INTERACTIVE CLICK MODE ---
        click_card = ttk.Frame(parent, style="Card.TFrame", padding=10)
        click_card.pack(fill="x")

        ttk.Label(click_card, text="🖱️ Canvas Click Tool", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 6))

        ttk.Radiobutton(click_card, text="🧱 Draw / Erase Walls (Drag)",
                        value="wall", variable=self.click_mode,
                        style="Dark.TRadiobutton").pack(anchor="w", pady=2)
        ttk.Radiobutton(click_card, text="🟢 Set Start Point (Click)",
                        value="start", variable=self.click_mode,
                        style="Dark.TRadiobutton").pack(anchor="w", pady=2)
        ttk.Radiobutton(click_card, text="🔴 Set Destination Point (Click)",
                        value="end", variable=self.click_mode,
                        style="Dark.TRadiobutton").pack(anchor="w", pady=2)

    def _build_center_canvas(self, parent: ttk.Frame) -> None:
        """Constructs the central visualizer canvas and legend bar."""
        canvas_container = ttk.Frame(parent, style="Card.TFrame", padding=2)
        canvas_container.pack(fill="both", expand=True)

        # Tkinter Canvas
        self.canvas = tk.Canvas(canvas_container,
                                bg=COLORS["grid_bg"],
                                highlightthickness=0,
                                bd=0)
        self.canvas.pack(fill="both", expand=True)

        # Instantiate Visualizer
        self.visualizer = MazeVisualizer(self.canvas, self.maze)

        # Bind Canvas Events for Resizing & Interaction
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
        self.canvas.bind("<Motion>", self._on_canvas_motion)

        # Color Legend Bar below canvas
        self._build_legend_bar(parent)

    def _build_legend_bar(self, parent: ttk.Frame) -> None:
        """Creates a modern visual color legend for all cell types."""
        legend_frame = ttk.Frame(parent, style="Dark.TFrame", padding=(0, 6, 0, 0))
        legend_frame.pack(fill="x")

        legends = [
            ("🟢 Start", COLORS["cell_start"]),
            ("🔴 Target", COLORS["cell_end"]),
            ("🧱 Wall", COLORS["cell_wall"]),
            ("⬜ Empty", COLORS["cell_empty"]),
            ("🟡 Exploring", COLORS["cell_exploring"]),
            ("🔵 Visited", COLORS["cell_visited"]),
            ("🟣 Shortest Path", COLORS["cell_path"])
        ]

        for text, color in legends:
            item = ttk.Frame(legend_frame, style="Dark.TFrame")
            item.pack(side="left", expand=True)

            box = tk.Label(item, text="   ", bg=color, width=2, height=1, relief="solid", bd=1)
            box.pack(side="left", padx=(0, 4))

            lbl = ttk.Label(item, text=text, style="Dark.TLabel")
            lbl.pack(side="left")

    def _build_right_panel(self, parent: ttk.Frame) -> None:
        """Constructs Right Panel containing Real-Time Statistics and Algorithm Educational Info."""
        
        # --- CARD 1: LIVE PERFORMANCE STATISTICS ---
        stats_card = ttk.Frame(parent, style="Card.TFrame", padding=10)
        stats_card.pack(fill="x", pady=(0, 10))

        ttk.Label(stats_card, text="📊 Performance Statistics", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))

        self.stat_algo_lbl = self._create_stat_row(stats_card, "Algorithm:", "A*")
        self.stat_status_lbl = self._create_stat_row(stats_card, "Status:", "Ready", val_color=COLORS["accent_cyan"])
        self.stat_path_lbl = self._create_stat_row(stats_card, "Path Length:", "0 cells")
        self.stat_visited_lbl = self._create_stat_row(stats_card, "Nodes Visited:", "0 cells")
        self.stat_time_lbl = self._create_stat_row(stats_card, "Execution Time:", "0.00 ms")
        self.stat_efficiency_lbl = self._create_stat_row(stats_card, "Explored Ratio:", "0.0%")

        # --- CARD 2: EDUCATIONAL ALGORITHM INFO ---
        self.info_card = ttk.Frame(parent, style="Card.TFrame", padding=10)
        self.info_card.pack(fill="both", expand=True)

        ttk.Label(self.info_card, text="📚 Algorithm Insights", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 6))

        self.info_technique = self._create_info_row(self.info_card, "Technique:")
        self.info_ds = self._create_info_row(self.info_card, "Data Structure:")
        self.info_guarantee = self._create_info_row(self.info_card, "Shortest Path:")
        self.info_time_comp = self._create_info_row(self.info_card, "Time Complexity:")
        self.info_space_comp = self._create_info_row(self.info_card, "Space Complexity:")

        ttk.Label(self.info_card, text="Description & Behavior:", style="Muted.TLabel").pack(anchor="w", pady=(8, 2))
        
        self.info_desc = tk.Text(self.info_card,
                                 wrap="word",
                                 height=7,
                                 bg=COLORS["bg_main"],
                                 fg=COLORS["text_primary"],
                                 font=("Segoe UI", 9),
                                 bd=1,
                                 relief="solid",
                                 padx=6,
                                 pady=6)
        self.info_desc.pack(fill="both", expand=True, pady=(0, 4))
        self.info_desc.configure(state="disabled")

        self.info_tip_lbl = ttk.Label(self.info_card,
                                      text="",
                                      wraplength=260,
                                      foreground=COLORS["accent_warning"],
                                      background=COLORS["bg_card"],
                                      font=("Segoe UI", 8, "italic"))
        self.info_tip_lbl.pack(anchor="w", fill="x")

    def _create_stat_row(self, parent: ttk.Frame, label_text: str, default_val: str, val_color: str = None) -> ttk.Label:
        """Helper to create a formatted label key-value row for statistics."""
        row = ttk.Frame(parent, style="CardInner.TFrame")
        row.pack(fill="x", pady=2)

        k_lbl = ttk.Label(row, text=label_text, style="StatKey.TLabel")
        k_lbl.pack(side="left")

        v_lbl = ttk.Label(row, text=default_val, style="StatVal.TLabel")
        if val_color:
            v_lbl.configure(foreground=val_color)
        v_lbl.pack(side="right")
        return v_lbl

    def _create_info_row(self, parent: ttk.Frame, label_text: str) -> ttk.Label:
        """Helper to create an educational attribute row."""
        row = ttk.Frame(parent, style="CardInner.TFrame")
        row.pack(fill="x", pady=1)

        k_lbl = ttk.Label(row, text=label_text, style="StatKey.TLabel")
        k_lbl.pack(side="left")

        v_lbl = ttk.Label(row, text="-", style="Dark.TLabel", font=("Segoe UI", 9, "bold"))
        v_lbl.pack(side="right")
        return v_lbl

    def _create_status_bar(self) -> None:
        """Creates bottom status bar for coordinates and system notices."""
        status_frame = ttk.Frame(self.root, style="Dark.TFrame", padding=(15, 3, 15, 3))
        status_frame.pack(fill="x", side="bottom")

        self.status_coords_lbl = ttk.Label(status_frame, text="Hover: Cell (row: -, col: -)", style="Muted.TLabel")
        self.status_coords_lbl.pack(side="left")

        self.status_msg_lbl = ttk.Label(status_frame, text="Ready. Select start/target or generate a maze to begin.", style="Muted.TLabel")
        self.status_msg_lbl.pack(side="right")

    # =========================================================================
    # EVENT HANDLERS & INTERACTIONS
    # =========================================================================

    def _on_canvas_resize(self, event) -> None:
        """Recalculates grid dimensions and cell sizes when the window resizes."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 50 and h > 50:
            self.visualizer.calculate_cell_size(w, h)
            self.visualizer.draw_grid()

    def _on_canvas_click(self, event) -> None:
        """Handles single mouse clicks for placing start/end or toggling walls."""
        if self.visualizer.is_running:
            return

        cell = self.visualizer.cell_at_pixel(event.x, event.y)
        if not cell:
            return

        r, c = cell
        mode = self.click_mode.get()

        if mode == "start":
            success, msg = self.maze.set_start(r, c)
            if not success:
                messagebox.showwarning("Invalid Start Position", msg, parent=self.root)
            else:
                self.visualizer.reset_visited_display()
                self.status_msg_lbl.configure(text=f"Start point placed at ({r}, {c})")

        elif mode == "end":
            success, msg = self.maze.set_end(r, c)
            if not success:
                messagebox.showwarning("Invalid Destination", msg, parent=self.root)
            else:
                self.visualizer.reset_visited_display()
                self.status_msg_lbl.configure(text=f"Destination placed at ({r}, {c})")

        elif mode == "wall":
            self.is_mouse_down = True
            current_is_wall = self.maze.is_wall(r, c)
            self.mouse_draw_mode = not current_is_wall  # If was wall, erase; if was empty, draw wall
            self.maze.set_wall_explicit(r, c, self.mouse_draw_mode)
            self.visualizer.refresh_cell(r, c)

    def _on_canvas_drag(self, event) -> None:
        """Handles mouse drag for continuous wall painting and erasing."""
        if self.visualizer.is_running or not self.is_mouse_down:
            return
        if self.click_mode.get() != "wall" or self.mouse_draw_mode is None:
            return

        cell = self.visualizer.cell_at_pixel(event.x, event.y)
        if cell:
            r, c = cell
            changed = self.maze.set_wall_explicit(r, c, self.mouse_draw_mode)
            if changed:
                self.visualizer.refresh_cell(r, c)

    def _on_canvas_release(self, event) -> None:
        """Resets mouse drag state."""
        self.is_mouse_down = False
        self.mouse_draw_mode = None

    def _on_canvas_motion(self, event) -> None:
        """Updates hover coordinate status in the bottom bar."""
        cell = self.visualizer.cell_at_pixel(event.x, event.y)
        if cell:
            r, c = cell
            cell_type_name = "Empty"
            if (r, c) == self.maze.start:
                cell_type_name = "Start Point"
            elif (r, c) == self.maze.end:
                cell_type_name = "Destination"
            elif self.maze.is_wall(r, c):
                cell_type_name = "Wall"
            self.status_coords_lbl.configure(text=f"Cell: ({r}, {c}) — {cell_type_name}")
        else:
            self.status_coords_lbl.configure(text="Hover: Outside Grid")

    def _on_size_change(self, event=None) -> None:
        """Handles maze grid resize selection."""
        self.visualizer.stop_animation()
        size_name = self.selected_size.get()
        rows, cols, _ = GRID_SIZES[size_name]
        self.maze.set_dimensions(rows, cols)
        MazeGenerator.generate(self.maze, self.selected_maze_type.get())
        self._on_canvas_resize(None)
        self._reset_stats_labels()
        self.status_msg_lbl.configure(text=f"Grid resized to {rows}x{cols}")

    def _on_speed_change(self, event=None) -> None:
        """Updates visualizer animation speed."""
        speed_name = self.selected_speed.get()
        self.visualizer.set_speed(speed_name)

    def _on_generate_maze(self) -> None:
        """Generates a new maze based on selected pattern."""
        self.visualizer.stop_animation()
        pattern = self.selected_maze_type.get()
        MazeGenerator.generate(self.maze, pattern)
        self.visualizer.draw_grid()
        self._reset_stats_labels()
        self.status_msg_lbl.configure(text=f"Generated new maze pattern: {pattern}")

    def _on_clear_walls(self) -> None:
        """Clears all walls while preserving start and destination points."""
        self.visualizer.stop_animation()
        self.maze.clear_all_walls()
        self.visualizer.draw_grid()
        self._reset_stats_labels()
        self.status_msg_lbl.configure(text="Cleared all walls. Grid is now open.")

    def _on_reset_search(self) -> None:
        """Resets visited and path visual states without affecting walls."""
        self.visualizer.stop_animation()
        self.visualizer.reset_visited_display()
        self._reset_stats_labels()
        self.status_msg_lbl.configure(text="Reset path search visualization.")

    def _update_algorithm_info_panel(self) -> None:
        """Updates the Educational Info Card based on currently selected algorithm."""
        algo_name = self.selected_algo.get()
        info = ALGORITHM_INFO.get(algo_name, {})
        if not info:
            return

        self.info_technique.configure(text=info.get("technique", "-"))
        self.info_ds.configure(text=info.get("data_structure", "-"))
        self.info_guarantee.configure(text=info.get("shortest_path", "-"))
        self.info_time_comp.configure(text=info.get("time_complexity", "-"))
        self.info_space_comp.configure(text=info.get("space_complexity", "-"))

        self.info_desc.configure(state="normal")
        self.info_desc.delete("1.0", tk.END)
        self.info_desc.insert(tk.END, info.get("description", ""))
        self.info_desc.configure(state="disabled")

        self.info_tip_lbl.configure(text="💡 Tip: " + info.get("educational_tip", ""))
        self.stat_algo_lbl.configure(text=info.get("short_name", algo_name))

    def _reset_stats_labels(self) -> None:
        """Resets statistics values to defaults."""
        self.stat_status_lbl.configure(text="Ready", foreground=COLORS["accent_cyan"])
        self.stat_path_lbl.configure(text="0 cells")
        self.stat_visited_lbl.configure(text="0 cells")
        self.stat_time_lbl.configure(text="0.00 ms")
        self.stat_efficiency_lbl.configure(text="0.0%")

    # =========================================================================
    # SOLVER EXECUTION & ANIMATION CONTROL
    # =========================================================================

    def _set_ui_solving_state(self, running: bool) -> None:
        """Enables/disables UI controls during animation execution."""
        state = "disabled" if running else "normal"
        self.btn_solve.configure(state=state)
        self.btn_generate.configure(state=state)
        self.btn_clear_walls.configure(state=state)
        self.btn_compare.configure(state=state)
        self.size_cb.configure(state=state)
        self.maze_type_cb.configure(state=state)

        # Pause and Stop are enabled only during active runs
        self.btn_pause.configure(state="normal" if running else "disabled", text="⏸️ Pause")
        self.btn_stop.configure(state="normal" if running else "disabled")

    def _on_start_solve(self) -> None:
        """Validates prerequisites and starts the solving visualization."""
        if self.visualizer.is_running:
            return

        # Validation: Check endpoints
        sr, sc = self.maze.start
        er, ec = self.maze.end
        if self.maze.is_wall(sr, sc):
            messagebox.showerror("Error", "Start point is currently a wall! Clear it before solving.", parent=self.root)
            return
        if self.maze.is_wall(er, ec):
            messagebox.showerror("Error", "Destination point is currently a wall! Clear it before solving.", parent=self.root)
            return
        if (sr, sc) == (er, ec):
            messagebox.showerror("Error", "Start point and Destination cannot be the same cell!", parent=self.root)
            return

        algo_name = self.selected_algo.get()
        self._set_ui_solving_state(True)
        self.stat_status_lbl.configure(text="Exploring...", foreground=COLORS["accent_warning"])
        self.status_msg_lbl.configure(text=f"Running {algo_name} visualization...")
        
        self.solve_start_time = time.perf_counter()

        # Start animation in Visualizer
        self.visualizer.start_animation(
            algo_name=algo_name,
            on_step=self._on_solver_step,
            on_complete=self._on_solver_complete
        )

    def _on_solver_step(self, data: Dict[str, Any]) -> None:
        """Callback triggered on each animation step to update live counters."""
        v_count = data.get("visited_count", 0)
        p_len = data.get("path_length", 0)
        self.stat_visited_lbl.configure(text=f"{v_count} cells")
        if p_len > 0:
            self.stat_path_lbl.configure(text=f"{p_len} cells")

    def _on_solver_complete(self, result: Dict[str, Any]) -> None:
        """Callback triggered when algorithm execution finishes."""
        self._set_ui_solving_state(False)
        total_time = time.perf_counter() - self.solve_start_time

        found = result.get("found", False)
        path = result.get("path", [])
        visited_count = result.get("visited_count", self.visualizer.visited_count)
        walkable_total = self.maze.count_walkable()
        ratio = (visited_count / max(1, walkable_total)) * 100

        # Benchmark pure calculation time without UI delay
        instant_res = solve_instant(self.selected_algo.get(), self.maze)
        calc_time = instant_res.get("time", 0.0)

        if found:
            self.stat_status_lbl.configure(text="Path Found! ✅", foreground=COLORS["accent_secondary"])
            self.stat_path_lbl.configure(text=f"{len(path)} cells")
            self.stat_visited_lbl.configure(text=f"{visited_count} cells")
            self.stat_time_lbl.configure(text=format_time(calc_time))
            self.stat_efficiency_lbl.configure(text=f"{ratio:.1f}% of grid")
            self.status_msg_lbl.configure(
                text=f"Solution found! Path length: {len(path)} | Explored: {visited_count} nodes | Pure Alg Time: {format_time(calc_time)}"
            )
        else:
            self.stat_status_lbl.configure(text="No Path Found ❌", foreground=COLORS["accent_danger"])
            self.stat_path_lbl.configure(text="None")
            self.stat_visited_lbl.configure(text=f"{visited_count} cells")
            self.stat_time_lbl.configure(text=format_time(calc_time))
            self.stat_efficiency_lbl.configure(text=f"{ratio:.1f}% of grid")
            self.status_msg_lbl.configure(text="No reachable path exists between Start and Destination.")
            messagebox.showinfo("Search Complete", "No valid path exists between the Start and Destination points in this maze.", parent=self.root)

    def _on_toggle_pause(self) -> None:
        """Toggles animation pause/resume."""
        if not self.visualizer.is_running:
            return
        is_running_now = self.visualizer.toggle_pause()
        if is_running_now:
            self.btn_pause.configure(text="⏸️ Pause")
            self.stat_status_lbl.configure(text="Exploring...", foreground=COLORS["accent_warning"])
            self.status_msg_lbl.configure(text="Animation resumed.")
        else:
            self.btn_pause.configure(text="▶️ Resume")
            self.stat_status_lbl.configure(text="Paused ⏸️", foreground=COLORS["accent_warning"])
            self.status_msg_lbl.configure(text="Animation paused. Click Resume to continue.")

    def _on_stop_solve(self) -> None:
        """Stops the animation immediately."""
        self.visualizer.stop_animation()
        self._set_ui_solving_state(False)
        self.stat_status_lbl.configure(text="Stopped 🛑", foreground=COLORS["accent_danger"])
        self.status_msg_lbl.configure(text="Algorithm execution was stopped by the user.")

    # =========================================================================
    # ALGORITHM COMPARISON MODAL WINDOW
    # =========================================================================

    def _open_comparison_dialog(self) -> None:
        """
        Runs BFS, DFS, Dijkstra, and A* instantly on the current maze
        and opens a comprehensive comparative analysis window.
        """
        if self.visualizer.is_running:
            messagebox.showwarning("Busy", "Please stop or wait for the current animation to finish before comparing.", parent=self.root)
            return

        sr, sc = self.maze.start
        er, ec = self.maze.end
        if self.maze.is_wall(sr, sc) or self.maze.is_wall(er, ec):
            messagebox.showerror("Error", "Start or Destination point is on a wall. Fix endpoints before comparing.", parent=self.root)
            return

        # Run benchmarks on current maze
        algos = [
            ("Breadth First Search (BFS)", "BFS"),
            ("Depth First Search (DFS)", "DFS"),
            ("Dijkstra's Algorithm", "Dijkstra"),
            ("A* (A-Star) Algorithm", "A*")
        ]

        results = []
        for full_name, short_name in algos:
            res = solve_instant(full_name, self.maze)
            results.append({
                "full_name": full_name,
                "short_name": short_name,
                "found": res.get("found", False),
                "path_length": res.get("path_length", 0),
                "visited_count": res.get("visited_count", 0),
                "time": res.get("time", 0.0),
                "is_shortest": full_name != "Depth First Search (DFS)" and res.get("found", False)
            })

        self._show_comparison_window(results)

    def _show_comparison_window(self, results: list) -> None:
        """Renders the comparison modal dialog with a styled table and takeaways."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Algorithm Performance Comparison — Benchmark Analysis")
        dialog.geometry("780x520")
        dialog.minsize(700, 450)
        dialog.configure(bg=COLORS["bg_main"])
        dialog.transient(self.root)
        dialog.grab_set()

        # Dialog Header
        top_frame = ttk.Frame(dialog, style="Dark.TFrame", padding=15)
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="📊 Algorithm Performance Benchmark", style="Title.TLabel", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ttk.Label(top_frame,
                  text=f"Benchmark executed on the exact same {self.maze.rows}x{self.maze.cols} maze with Start {self.maze.start} → End {self.maze.end}.",
                  style="Subtitle.TLabel").pack(anchor="w", pady=(2, 0))

        # Comparison Table (Treeview)
        table_frame = ttk.Frame(dialog, style="Card.TFrame", padding=10)
        table_frame.pack(fill="x", padx=15, pady=5)

        columns = ("algo", "status", "length", "visited", "time", "guaranteed")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=5)
        
        tree.heading("algo", text="Algorithm")
        tree.heading("status", text="Path Found")
        tree.heading("length", text="Path Length")
        tree.heading("visited", text="Nodes Visited")
        tree.heading("time", text="Exec Time")
        tree.heading("guaranteed", text="Shortest Path?")

        tree.column("algo", width=160, anchor="w")
        tree.column("status", width=90, anchor="center")
        tree.column("length", width=90, anchor="center")
        tree.column("visited", width=100, anchor="center")
        tree.column("time", width=100, anchor="center")
        tree.column("guaranteed", width=110, anchor="center")

        # Find best values
        valid_paths = [r["path_length"] for r in results if r["found"]]
        min_path = min(valid_paths) if valid_paths else 0
        min_visited = min(r["visited_count"] for r in results)

        for r in results:
            status_str = "Yes ✅" if r["found"] else "No ❌"
            len_str = f"{r['path_length']} cells" if r["found"] else "N/A"
            vis_str = f"{r['visited_count']} cells"
            time_str = format_time(r["time"])
            guar_str = "Optimal ✅" if r["is_shortest"] else "Not Guaranteed ⚠️"

            # Tag highlights
            if r["found"] and r["path_length"] == min_path and r["visited_count"] == min_visited:
                tag = "best"
            else:
                tag = "normal"

            tree.insert("", "end", values=(r["short_name"], status_str, len_str, vis_str, time_str, guar_str), tags=(tag,))

        tree.tag_configure("best", background="#2a3f5f")
        tree.pack(fill="x")

        # Key Findings Card
        findings_frame = ttk.Frame(dialog, style="Card.TFrame", padding=12)
        findings_frame.pack(fill="both", expand=True, padx=15, pady=10)

        ttk.Label(findings_frame, text="💡 Key Takeaways & Educational Insights", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 6))

        # Generate summary insight text
        astar_res = next((r for r in results if r["short_name"] == "A*"), None)
        bfs_res = next((r for r in results if r["short_name"] == "BFS"), None)
        dfs_res = next((r for r in results if r["short_name"] == "DFS"), None)

        insights = []
        if astar_res and bfs_res and astar_res["found"] and bfs_res["found"]:
            saved_nodes = bfs_res["visited_count"] - astar_res["visited_count"]
            if saved_nodes > 0:
                pct = (saved_nodes / bfs_res["visited_count"]) * 100
                insights.append(f"• A* evaluated {saved_nodes} fewer nodes than BFS ({pct:.1f}% reduction) thanks to its Manhattan heuristic guidance.")
            else:
                insights.append("• In tight corridors with few branches, A* and BFS explored comparable node counts.")

        if dfs_res and dfs_res["found"]:
            if dfs_res["path_length"] > min_path:
                insights.append(f"• DFS path length is {dfs_res['path_length']} cells vs {min_path} cells optimal (DFS wandered {dfs_res['path_length'] - min_path} extra steps).")
            else:
                insights.append("• DFS happened to reach the destination directly along this specific branch without severe wandering.")

        insights.append("• BFS and Dijkstra both guarantee the mathematically shortest path on unweighted grids.")
        insights.append("• A* combines Dijkstra's shortest path guarantee with heuristic prioritization for maximum efficiency.")

        insight_text = "\n".join(insights)
        
        txt_box = tk.Text(findings_frame,
                          wrap="word",
                          height=5,
                          bg=COLORS["bg_main"],
                          fg=COLORS["text_primary"],
                          font=("Segoe UI", 9),
                          bd=0,
                          padx=8,
                          pady=8)
        txt_box.pack(fill="both", expand=True)
        txt_box.insert(tk.END, insight_text)
        txt_box.configure(state="disabled")

        # Close Button
        btn_close = ttk.Button(dialog, text="Close Benchmark", style="Primary.TButton", command=dialog.destroy)
        btn_close.pack(pady=(0, 12))
