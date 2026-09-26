"""
maze.py - Maze Grid and Cell State Management.
"""

from typing import List, Tuple, Optional
from utils import EMPTY, WALL, START, END, VISITED, EXPLORING, PATH


class Maze:
    """
    Manages the 2D grid representation of the maze, cell states,
    start/end positions, and pathfinding queries.
    """

    def __init__(self, rows: int = 25, cols: int = 25):
        self.rows: int = rows
        self.cols: int = cols
        self.grid: List[List[int]] = [[EMPTY for _ in range(cols)] for _ in range(rows)]
        
        # Default start (top-left walkable) and end (bottom-right walkable)
        self.start: Tuple[int, int] = (1, 1)
        self.end: Tuple[int, int] = (rows - 2, cols - 2)
        
        # Initialize grid start and end markings
        self._ensure_default_endpoints()

    def _ensure_default_endpoints(self) -> None:
        """Sets start and end cells in the grid array safely."""
        sr, sc = self.start
        er, ec = self.end
        if self.is_in_bounds(sr, sc):
            self.grid[sr][sc] = START
        if self.is_in_bounds(er, ec):
            self.grid[er][ec] = END

    def set_dimensions(self, rows: int, cols: int) -> None:
        """Resizes the maze grid to new dimensions."""
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]
        self.start = (1, 1)
        self.end = (rows - 2, cols - 2)
        self._ensure_default_endpoints()

    def is_in_bounds(self, r: int, c: int) -> bool:
        """Check if row and column coordinates are within grid boundaries."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get_cell(self, r: int, c: int) -> int:
        """Get cell state at (r, c). Returns WALL if out of bounds."""
        if not self.is_in_bounds(r, c):
            return WALL
        return self.grid[r][c]

    def set_cell(self, r: int, c: int, cell_type: int) -> None:
        """Set cell state at (r, c)."""
        if self.is_in_bounds(r, c):
            self.grid[r][c] = cell_type

    def is_wall(self, r: int, c: int) -> bool:
        """Return True if (r, c) is a wall or out of bounds."""
        if not self.is_in_bounds(r, c):
            return True
        return self.grid[r][c] == WALL

    def is_walkable(self, r: int, c: int) -> bool:
        """Return True if (r, c) is walkable (not a wall and within bounds)."""
        if not self.is_in_bounds(r, c):
            return False
        return self.grid[r][c] != WALL

    def set_start(self, r: int, c: int) -> Tuple[bool, str]:
        """
        Sets the start position at (r, c) with validation.
        Returns (success_flag, error_or_success_message).
        """
        if not self.is_in_bounds(r, c):
            return False, "Coordinates are out of bounds."
        if (r, c) == self.end:
            return False, "Start point cannot be the same as Destination."
        if self.grid[r][c] == WALL:
            return False, "Start point cannot be placed on a wall. Clear the cell first."

        # Clear old start
        old_r, old_c = self.start
        if self.is_in_bounds(old_r, old_c) and self.grid[old_r][old_c] == START:
            self.grid[old_r][old_c] = EMPTY

        self.start = (r, c)
        self.grid[r][c] = START
        return True, "Start position updated successfully."

    def set_end(self, r: int, c: int) -> Tuple[bool, str]:
        """
        Sets the destination position at (r, c) with validation.
        Returns (success_flag, error_or_success_message).
        """
        if not self.is_in_bounds(r, c):
            return False, "Coordinates are out of bounds."
        if (r, c) == self.start:
            return False, "Destination cannot be the same as Start point."
        if self.grid[r][c] == WALL:
            return False, "Destination cannot be placed on a wall. Clear the cell first."

        # Clear old end
        old_r, old_c = self.end
        if self.is_in_bounds(old_r, old_c) and self.grid[old_r][old_c] == END:
            self.grid[old_r][old_c] = EMPTY

        self.end = (r, c)
        self.grid[r][c] = END
        return True, "Destination position updated successfully."

    def toggle_wall(self, r: int, c: int) -> bool:
        """
        Toggles wall on/off at (r, c). Cannot overwrite start or end points.
        Returns True if changed, False otherwise.
        """
        if not self.is_in_bounds(r, c):
            return False
        if (r, c) == self.start or (r, c) == self.end:
            return False
        
        if self.grid[r][c] == WALL:
            self.grid[r][c] = EMPTY
        else:
            self.grid[r][c] = WALL
        return True

    def set_wall_explicit(self, r: int, c: int, make_wall: bool) -> bool:
        """Sets wall explicitly (used for drag drawing/erasing)."""
        if not self.is_in_bounds(r, c):
            return False
        if (r, c) == self.start or (r, c) == self.end:
            return False
        
        target = WALL if make_wall else EMPTY
        if self.grid[r][c] != target:
            self.grid[r][c] = target
            return True
        return False

    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        """
        Returns orthogonal valid walkable neighbors (Up, Right, Down, Left).
        """
        # 4 directions: Up, Right, Down, Left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.is_walkable(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

    def clear_all_walls(self) -> None:
        """Removes all walls and resets visited/path states."""
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) == self.start:
                    self.grid[r][c] = START
                elif (r, c) == self.end:
                    self.grid[r][c] = END
                else:
                    self.grid[r][c] = EMPTY

    def clear_path_and_visited(self) -> None:
        """
        Clears VISITED, EXPLORING, and PATH states, preserving WALLS,
        START, and END cells.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) == self.start:
                    self.grid[r][c] = START
                elif (r, c) == self.end:
                    self.grid[r][c] = END
                elif self.grid[r][c] in (VISITED, EXPLORING, PATH):
                    self.grid[r][c] = EMPTY

    def clone(self) -> 'Maze':
        """Creates a deep copy of the current Maze instance."""
        new_maze = Maze(self.rows, self.cols)
        new_maze.grid = [row[:] for row in self.grid]
        new_maze.start = self.start
        new_maze.end = self.end
        return new_maze

    def count_walls(self) -> int:
        """Return total number of wall cells in the maze."""
        return sum(row.count(WALL) for row in self.grid)

    def count_walkable(self) -> int:
        """Return total number of walkable cells in the maze."""
        return (self.rows * self.cols) - self.count_walls()
