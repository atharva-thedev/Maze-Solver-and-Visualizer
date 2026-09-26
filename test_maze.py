"""
test_maze.py - Comprehensive Unit Tests for Maze Solver & Visualizer.
Tests Maze data structure, Generators, and Pathfinding Algorithms (BFS, DFS, Dijkstra, A*).
"""

import unittest
from maze import Maze
from generator import MazeGenerator
from algorithms import bfs_solve, dfs_solve, dijkstra_solve, astar_solve, solve_instant
from utils import EMPTY, WALL, START, END


class TestMazeDataStructure(unittest.TestCase):
    """Tests for the Maze class and grid operations."""

    def setUp(self):
        self.maze = Maze(15, 15)

    def test_initialization(self):
        """Verify maze dimensions and default endpoints."""
        self.assertEqual(self.maze.rows, 15)
        self.assertEqual(self.maze.cols, 15)
        self.assertEqual(self.maze.start, (1, 1))
        self.assertEqual(self.maze.end, (13, 13))
        self.assertEqual(self.maze.get_cell(1, 1), START)
        self.assertEqual(self.maze.get_cell(13, 13), END)

    def test_bounds_checking(self):
        """Check coordinate boundary validation."""
        self.assertTrue(self.maze.is_in_bounds(0, 0))
        self.assertTrue(self.maze.is_in_bounds(14, 14))
        self.assertFalse(self.maze.is_in_bounds(-1, 0))
        self.assertFalse(self.maze.is_in_bounds(0, 15))
        self.assertFalse(self.maze.is_in_bounds(15, 15))

    def test_set_start_and_end_validations(self):
        """Ensure start and end endpoints follow constraints."""
        # Cannot set out of bounds
        ok, msg = self.maze.set_start(-5, 0)
        self.assertFalse(ok)

        # Cannot set start on end
        ok, msg = self.maze.set_start(13, 13)
        self.assertFalse(ok)

        # Cannot set start on a wall
        self.maze.set_cell(5, 5, WALL)
        ok, msg = self.maze.set_start(5, 5)
        self.assertFalse(ok)

        # Valid start placement
        ok, msg = self.maze.set_start(2, 2)
        self.assertTrue(ok)
        self.assertEqual(self.maze.start, (2, 2))
        self.assertEqual(self.maze.get_cell(2, 2), START)
        self.assertEqual(self.maze.get_cell(1, 1), EMPTY)

    def test_wall_toggling(self):
        """Check wall creation, toggling, and endpoint protection."""
        # Can toggle empty to wall
        self.assertEqual(self.maze.get_cell(5, 5), EMPTY)
        self.maze.toggle_wall(5, 5)
        self.assertEqual(self.maze.get_cell(5, 5), WALL)
        self.maze.toggle_wall(5, 5)
        self.assertEqual(self.maze.get_cell(5, 5), EMPTY)

        # Cannot toggle start or end cell to wall
        self.maze.toggle_wall(self.maze.start[0], self.maze.start[1])
        self.assertEqual(self.maze.get_cell(self.maze.start[0], self.maze.start[1]), START)


class TestMazeGenerators(unittest.TestCase):
    """Tests for maze generation patterns."""

    def test_recursive_backtracker_solvability(self):
        """Recursive backtracker must produce valid walkable endpoints."""
        maze = Maze(21, 21)
        MazeGenerator.generate_recursive_backtracker(maze)
        MazeGenerator._finalize_start_end(maze)

        sr, sc = maze.start
        er, ec = maze.end
        self.assertNotEqual(maze.get_cell(sr, sc), WALL)
        self.assertNotEqual(maze.get_cell(er, ec), WALL)

        # Solve with BFS to verify solvability
        res = bfs_solve(maze)
        self.assertTrue(res["found"], "Recursive backtracker maze should be solvable.")
        self.assertGreater(res["path_length"], 0)

    def test_random_obstacles(self):
        """Random obstacle generator leaves start and end clear."""
        maze = Maze(25, 25)
        MazeGenerator.generate_random_obstacles(maze, density=0.30)
        MazeGenerator._finalize_start_end(maze)
        self.assertTrue(maze.is_walkable(maze.start[0], maze.start[1]))
        self.assertTrue(maze.is_walkable(maze.end[0], maze.end[1]))

    def test_braided_maze(self):
        """Braided maze creates solvable multiple paths."""
        maze = Maze(21, 21)
        MazeGenerator.generate_braided_maze(maze)
        MazeGenerator._finalize_start_end(maze)
        res = astar_solve(maze)
        self.assertTrue(res["found"])


class TestPathfindingAlgorithms(unittest.TestCase):
    """Tests for BFS, DFS, Dijkstra, and A* pathfinding correctness."""

    def test_open_grid_shortest_path(self):
        """On an open 10x10 grid from (0,0) to (4,4), Manhattan distance is 8 -> path length 9."""
        maze = Maze(10, 10)
        maze.clear_all_walls()
        maze.set_start(0, 0)
        maze.set_end(4, 4)

        bfs_res = bfs_solve(maze)
        dijkstra_res = dijkstra_solve(maze)
        astar_res = astar_solve(maze)
        dfs_res = dfs_solve(maze)

        # BFS, Dijkstra, and A* MUST guarantee identical optimal path length
        expected_len = 9  # 8 steps + starting node = 9 cells
        self.assertTrue(bfs_res["found"])
        self.assertEqual(bfs_res["path_length"], expected_len)
        self.assertEqual(dijkstra_res["path_length"], expected_len)
        self.assertEqual(astar_res["path_length"], expected_len)

        # DFS should also find a path (length may or may not be optimal)
        self.assertTrue(dfs_res["found"])
        self.assertGreaterEqual(dfs_res["path_length"], expected_len)

        # A* should visit fewer or equal nodes than BFS in open grid
        self.assertLessEqual(astar_res["visited_count"], bfs_res["visited_count"])

    def test_unsolvable_maze(self):
        """When the destination is completely surrounded by walls, algorithms report not found."""
        maze = Maze(11, 11)
        maze.clear_all_walls()
        maze.set_start(1, 1)
        maze.set_end(5, 5)

        # Wall in (5, 5) on all 4 sides
        maze.set_cell(4, 5, WALL)
        maze.set_cell(6, 5, WALL)
        maze.set_cell(5, 4, WALL)
        maze.set_cell(5, 6, WALL)

        for algo_name in ["BFS", "DFS", "Dijkstra", "A*"]:
            res = solve_instant(algo_name, maze)
            self.assertFalse(res["found"], f"{algo_name} should report no path in walled-in maze")
            self.assertEqual(res["path"], [])
            self.assertEqual(res["path_length"], 0)

    def test_start_adjacent_to_end(self):
        """When start is immediately next to end, path length is exactly 2."""
        maze = Maze(10, 10)
        maze.clear_all_walls()
        maze.set_start(2, 2)
        maze.set_end(2, 3)

        for algo_name in ["BFS", "DFS", "Dijkstra", "A*"]:
            res = solve_instant(algo_name, maze)
            self.assertTrue(res["found"])
            self.assertEqual(res["path_length"], 2, f"{algo_name} failed on adjacent cells")
            self.assertEqual(res["path"], [(2, 2), (2, 3)])

    def test_start_equals_end(self):
        """When start and end are identical, path length is 1."""
        maze = Maze(5, 5)
        maze.start = (2, 2)
        maze.end = (2, 2)

        for algo_name in ["BFS", "DFS", "Dijkstra", "A*"]:
            res = solve_instant(algo_name, maze)
            self.assertTrue(res["found"])
            self.assertEqual(res["path_length"], 1)
            self.assertEqual(res["path"], [(2, 2)])

    def test_large_maze_performance(self):
        """Test on large 45x45 maze to ensure fast execution (< 0.1s)."""
        maze = Maze(45, 45)
        MazeGenerator.generate_recursive_backtracker(maze)
        MazeGenerator._finalize_start_end(maze)

        for algo_name in ["BFS", "Dijkstra", "A*"]:
            res = solve_instant(algo_name, maze)
            self.assertTrue(res["found"])
            self.assertLess(res["time"], 0.1, f"{algo_name} took too long ({res['time']}s) on large maze")


if __name__ == "__main__":
    unittest.main()
