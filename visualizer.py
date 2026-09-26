"""
visualizer.py - Canvas Renderer and Animation Controller.
Controls step-by-step visual animation using Tkinter after() scheduling.
"""

from typing import List, Tuple, Optional, Callable, Dict, Any
import tkinter as tk
from maze import Maze
from algorithms import get_algorithm_generator
from utils import (
    EMPTY, WALL, START, END, VISITED, EXPLORING, PATH,
    COLORS, ANIMATION_SPEEDS
)


class MazeVisualizer:
    """
    Manages Canvas drawing, cell color updates, and non-blocking
    step-by-step algorithm animation via Tkinter after().
    """

    def __init__(self, canvas: tk.Canvas, maze: Maze):
        self.canvas: tk.Canvas = canvas
        self.maze: Maze = maze

        # Matrix of Canvas Rectangle IDs for fast itemconfig updates
        self.rect_ids: List[List[Optional[int]]] = []
        
        # Dimensions
        self.cell_size: int = 22
        self.offset_x: int = 10
        self.offset_y: int = 10

        # Animation State
        self.generator = None
        self.is_running: bool = False
        self.is_paused: bool = False
        self.delay_ms: int = ANIMATION_SPEEDS["Medium"]
        self.after_id: Optional[str] = None

        # Statistics & Callbacks
        self.step_count: int = 0
        self.visited_count: int = 0
        self.path_length: int = 0
        self.on_step_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        self.on_complete_callback: Optional[Callable[[Dict[str, Any]], None]] = None

    def calculate_cell_size(self, canvas_width: int, canvas_height: int) -> None:
        """Dynamically computes the cell size to fit nicely within the canvas."""
        margin = 20
        avail_w = max(100, canvas_width - margin * 2)
        avail_h = max(100, canvas_height - margin * 2)

        size_w = avail_w // self.maze.cols
        size_h = avail_h // self.maze.rows
        self.cell_size = max(8, min(size_w, size_h, 40))

        # Center the grid in the canvas
        grid_w = self.maze.cols * self.cell_size
        grid_h = self.maze.rows * self.cell_size
        self.offset_x = max(margin, (canvas_width - grid_w) // 2)
        self.offset_y = max(margin, (canvas_height - grid_h) // 2)

    def draw_grid(self) -> None:
        """Initializes and renders the complete maze on the Canvas."""
        self.stop_animation()
        self.canvas.delete("all")
        self.rect_ids = [[None for _ in range(self.maze.cols)] for _ in range(self.maze.rows)]

        cell_size = self.cell_size
        off_x = self.offset_x
        off_y = self.offset_y

        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                x1 = off_x + c * cell_size
                y1 = off_y + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                fill_color = self.get_cell_color(r, c)
                border_color = COLORS["grid_line"]

                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill_color,
                    outline=border_color,
                    width=1
                )
                self.rect_ids[r][c] = rect_id

        self.draw_start_end_markers()

    def get_cell_color(self, r: int, c: int) -> str:
        """Maps cell state to its corresponding theme hex color."""
        cell_val = self.maze.get_cell(r, c)
        if (r, c) == self.maze.start:
            return COLORS["cell_start"]
        elif (r, c) == self.maze.end:
            return COLORS["cell_end"]
        elif cell_val == WALL:
            return COLORS["cell_wall"]
        elif cell_val == EXPLORING:
            return COLORS["cell_exploring"]
        elif cell_val == VISITED:
            return COLORS["cell_visited"]
        elif cell_val == PATH:
            return COLORS["cell_path"]
        else:
            return COLORS["cell_empty"]

    def update_cell_color(self, r: int, c: int, color: Optional[str] = None) -> None:
        """Updates the fill color of a single cell quickly using its canvas ID."""
        if not self.maze.is_in_bounds(r, c):
            return
        if not self.rect_ids or r >= len(self.rect_ids) or c >= len(self.rect_ids[0]):
            return

        rect_id = self.rect_ids[r][c]
        if rect_id is not None:
            if color is None:
                color = self.get_cell_color(r, c)
            self.canvas.itemconfig(rect_id, fill=color)

    def draw_start_end_markers(self) -> None:
        """Ensures Start and End cells are colored correctly."""
        sr, sc = self.maze.start
        er, ec = self.maze.end
        self.update_cell_color(sr, sc, COLORS["cell_start"])
        self.update_cell_color(er, ec, COLORS["cell_end"])

    def refresh_cell(self, r: int, c: int) -> None:
        """Redraws a single cell according to current maze state."""
        self.update_cell_color(r, c, self.get_cell_color(r, c))

    def reset_visited_display(self) -> None:
        """Clears visited and path visual colors from canvas without destroying walls."""
        self.stop_animation()
        self.maze.clear_path_and_visited()
        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                self.update_cell_color(r, c, self.get_cell_color(r, c))
        self.draw_start_end_markers()

    def cell_at_pixel(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Converts canvas pixel coordinates (x, y) to grid (row, col)."""
        c = (x - self.offset_x) // self.cell_size
        r = (y - self.offset_y) // self.cell_size
        if self.maze.is_in_bounds(r, c):
            return (r, c)
        return None

    def start_animation(self,
                        algo_name: str,
                        on_step: Optional[Callable[[Dict[str, Any]], None]] = None,
                        on_complete: Optional[Callable[[Dict[str, Any]], None]] = None) -> None:
        """Starts solving animation using the selected algorithm."""
        self.stop_animation()
        self.reset_visited_display()

        self.on_step_callback = on_step
        self.on_complete_callback = on_complete
        self.generator = get_algorithm_generator(algo_name, self.maze)

        self.is_running = True
        self.is_paused = False
        self.step_count = 0
        self.visited_count = 0
        self.path_length = 0

        self._schedule_next_step()

    def _schedule_next_step(self) -> None:
        """Schedules the next animation step using Tkinter after()."""
        if not self.is_running or self.is_paused:
            return

        # For ultra fast / instant steps, process a small batch per tick to keep 60fps
        batch_size = 1 if self.delay_ms > 10 else (5 if self.delay_ms > 2 else 20)
        
        finished = False
        for _ in range(batch_size):
            if not self.is_running or self.is_paused:
                break
            finished = self._step_internal()
            if finished:
                break

        if not finished and self.is_running and not self.is_paused:
            self.after_id = self.canvas.after(self.delay_ms, self._schedule_next_step)

    def _step_internal(self) -> bool:
        """Executes a single step from the generator. Returns True if generator finished."""
        if self.generator is None:
            return True

        try:
            event = next(self.generator)
            self.step_count += 1
            event_type = event.get("type")

            if event_type == "exploring":
                r, c = event["cell"]
                if (r, c) != self.maze.start and (r, c) != self.maze.end:
                    self.update_cell_color(r, c, COLORS["cell_exploring"])
                self.maze.set_cell(r, c, EXPLORING)

            elif event_type == "visited":
                r, c = event["cell"]
                if (r, c) != self.maze.start and (r, c) != self.maze.end:
                    self.update_cell_color(r, c, COLORS["cell_visited"])
                self.maze.set_cell(r, c, VISITED)
                self.visited_count += 1

            elif event_type == "path_step":
                r, c = event["cell"]
                if (r, c) != self.maze.start and (r, c) != self.maze.end:
                    self.update_cell_color(r, c, COLORS["cell_path"])
                self.maze.set_cell(r, c, PATH)
                self.path_length += 1

            if self.on_step_callback:
                self.on_step_callback({
                    "visited_count": self.visited_count,
                    "path_length": self.path_length,
                    "event": event
                })

            return False

        except StopIteration as e:
            # Generator completed
            result = e.value or {}
            self.is_running = False
            self.draw_start_end_markers()

            if self.on_complete_callback:
                self.on_complete_callback(result)
            return True

    def pause_animation(self) -> None:
        """Pauses the currently running animation."""
        self.is_paused = True
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None

    def resume_animation(self) -> None:
        """Resumes a paused animation."""
        if self.is_running and self.is_paused:
            self.is_paused = False
            self._schedule_next_step()

    def toggle_pause(self) -> bool:
        """Toggles between pause and resume. Returns True if now running, False if paused."""
        if self.is_paused:
            self.resume_animation()
            return True
        else:
            self.pause_animation()
            return False

    def stop_animation(self) -> None:
        """Stops and cancels any running animation."""
        self.is_running = False
        self.is_paused = False
        if self.after_id:
            try:
                self.canvas.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None
        self.generator = None

    def set_speed(self, speed_name: str) -> None:
        """Sets the animation delay in milliseconds."""
        self.delay_ms = ANIMATION_SPEEDS.get(speed_name, 20)
