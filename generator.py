"""
generator.py - Maze Generation Algorithms.
Implements Recursive Backtracking (DFS), Random Obstacles, Open Field, and Braided Mazes.
"""

import random
from typing import List, Tuple
from maze import Maze
from utils import EMPTY, WALL, START, END


class MazeGenerator:
    """Provides algorithms for generating various styles of mazes."""

    @staticmethod
    def generate(maze: Maze, maze_type: str) -> None:
        """Main dispatcher for maze generation algorithms."""
        if "Recursive Backtracker" in maze_type:
            MazeGenerator.generate_recursive_backtracker(maze)
        elif "Random Obstacles" in maze_type:
            MazeGenerator.generate_random_obstacles(maze, density=0.30)
        elif "Open Maze" in maze_type:
            MazeGenerator.generate_open_maze(maze)
        elif "Complex Braided" in maze_type:
            MazeGenerator.generate_braided_maze(maze)
        elif "Empty Grid" in maze_type:
            maze.clear_all_walls()
        else:
            MazeGenerator.generate_recursive_backtracker(maze)

        MazeGenerator._finalize_start_end(maze)

    @staticmethod
    def generate_recursive_backtracker(maze: Maze) -> None:
        """
        Generates a perfect maze using Randomized Depth-First Search (Recursive Backtracker).
        Creates intricate, solvable corridors with walls separating them.
        """
        rows, cols = maze.rows, maze.cols

        # Fill entire maze with walls
        for r in range(rows):
            for c in range(cols):
                maze.grid[r][c] = WALL

        # Start carving from (1, 1) if odd/even boundaries permit
        start_r = 1 if rows > 2 else 0
        start_c = 1 if cols > 2 else 0
        
        maze.grid[start_r][start_c] = EMPTY
        stack: List[Tuple[int, int]] = [(start_r, start_c)]
        visited = set([(start_r, start_c)])

        while stack:
            curr_r, curr_c = stack[-1]

            # 2-step neighbors (Up, Right, Down, Left)
            directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
            random.shuffle(directions)

            found_neighbor = False
            for dr, dc in directions:
                nr, nc = curr_r + dr, curr_c + dc
                if 1 <= nr < rows - 1 and 1 <= nc < cols - 1:
                    if (nr, nc) not in visited:
                        # Knock down wall between current and target
                        wall_r = curr_r + dr // 2
                        wall_c = curr_c + dc // 2
                        maze.grid[wall_r][wall_c] = EMPTY
                        maze.grid[nr][nc] = EMPTY
                        
                        visited.add((nr, nc))
                        stack.append((nr, nc))
                        found_neighbor = True
                        break

            if not found_neighbor:
                stack.pop()

    @staticmethod
    def generate_random_obstacles(maze: Maze, density: float = 0.30) -> None:
        """
        Fills the grid with randomly scattered walls at a specified density.
        Preserves safe zones around start and end cells to prevent instant blockage.
        """
        maze.clear_all_walls()
        rows, cols = maze.rows, maze.cols
        
        # Safe zone around start and end
        sr, sc = maze.start
        er, ec = maze.end
        safe_radius = 1

        for r in range(rows):
            for c in range(cols):
                # Don't place wall if in safe zone around start or end
                if abs(r - sr) <= safe_radius and abs(c - sc) <= safe_radius:
                    continue
                if abs(r - er) <= safe_radius and abs(c - ec) <= safe_radius:
                    continue

                if random.random() < density:
                    maze.grid[r][c] = WALL

    @staticmethod
    def generate_open_maze(maze: Maze) -> None:
        """
        Generates an open field maze with structured pillar clusters and obstacle blocks.
        Great for observing heuristic behavior in A* versus wide radial exploration in BFS.
        """
        maze.clear_all_walls()
        rows, cols = maze.rows, maze.cols

        # Place periodic clusters and pillars
        for r in range(2, rows - 2, 4):
            for c in range(2, cols - 2, 4):
                if random.random() < 0.75:
                    maze.grid[r][c] = WALL
                    # Randomly extend pillar into small shape
                    if r + 1 < rows - 2 and random.random() < 0.5:
                        maze.grid[r + 1][c] = WALL
                    if c + 1 < cols - 2 and random.random() < 0.5:
                        maze.grid[r][c + 1] = WALL

    @staticmethod
    def generate_braided_maze(maze: Maze) -> None:
        """
        Generates a recursive backtracker maze, then removes random dead-end walls
        to introduce multiple loops and alternative paths.
        """
        # First generate standard backtracker maze
        MazeGenerator.generate_recursive_backtracker(maze)

        rows, cols = maze.rows, maze.cols
        # Knock down ~15% of internal walls to create loops (braiding)
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                if maze.grid[r][c] == WALL:
                    # If wall has empty cells on both horizontal sides or both vertical sides
                    h_open = (maze.grid[r][c-1] == EMPTY and maze.grid[r][c+1] == EMPTY)
                    v_open = (maze.grid[r-1][c] == EMPTY and maze.grid[r+1][c] == EMPTY)
                    if (h_open or v_open) and random.random() < 0.15:
                        maze.grid[r][c] = EMPTY

    @staticmethod
    def _finalize_start_end(maze: Maze) -> None:
        """
        Ensures start and destination are in walkable positions,
        preferably top-left and bottom-right.
        """
        rows, cols = maze.rows, maze.cols
        
        # Choose start position near top-left
        start_candidates = [
            (1, 1), (1, 2), (2, 1), (2, 2), (0, 0), (1, 0), (0, 1)
        ]
        start_pos = (1, 1)
        for r, c in start_candidates:
            if maze.is_in_bounds(r, c) and maze.grid[r][c] == EMPTY:
                start_pos = (r, c)
                break
        else:
            # Force (1, 1) to be empty if valid
            if maze.is_in_bounds(1, 1):
                maze.grid[1][1] = EMPTY
                start_pos = (1, 1)

        # Choose end position near bottom-right
        end_candidates = [
            (rows - 2, cols - 2), (rows - 2, cols - 3), (rows - 3, cols - 2),
            (rows - 3, cols - 3), (rows - 1, cols - 1)
        ]
        end_pos = (rows - 2, cols - 2)
        for r, c in end_candidates:
            if maze.is_in_bounds(r, c) and maze.grid[r][c] == EMPTY and (r, c) != start_pos:
                end_pos = (r, c)
                break
        else:
            if maze.is_in_bounds(rows - 2, cols - 2) and (rows - 2, cols - 2) != start_pos:
                maze.grid[rows - 2][cols - 2] = EMPTY
                end_pos = (rows - 2, cols - 2)

        maze.start = start_pos
        maze.end = end_pos
        maze.grid[start_pos[0]][start_pos[1]] = START
        maze.grid[end_pos[0]][end_pos[1]] = END
