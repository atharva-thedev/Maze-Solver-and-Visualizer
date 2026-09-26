"""
utils.py - Constants, configuration, and helper functions for Maze Solver & Visualizer.
"""

from typing import Tuple, List, Dict, Any

# Grid Cell States
EMPTY = 0
WALL = 1
START = 2
END = 3
VISITED = 4
EXPLORING = 5
PATH = 6
FRONTIER = 7

# Cell Dimensions & Presets
GRID_SIZES: Dict[str, Tuple[int, int, int]] = {
    "Small (15x15)": (15, 15, 36),
    "Medium (25x25)": (25, 25, 22),
    "Large (35x35)": (35, 35, 16),
    "Extra Large (45x45)": (45, 45, 12),
}

# Animation Speed Delays (in milliseconds)
ANIMATION_SPEEDS: Dict[str, int] = {
    "Slow": 50,
    "Medium": 20,
    "Fast": 5,
    "Ultra Fast": 1,
}

# Color Palette - Modern Sleek Theme
COLORS: Dict[str, str] = {
    # Theme Backgrounds & Accents
    "bg_main": "#1e1e2e",         # Dark Slate
    "bg_card": "#282a36",         # Slightly lighter card background
    "bg_card_border": "#44475a",  # Card border accent
    "text_primary": "#f8f8f2",    # Crisp white
    "text_secondary": "#6272a4",  # Slate blue-grey
    "accent_primary": "#bd93f9",  # Purple
    "accent_secondary": "#50fa7b",# Green
    "accent_warning": "#ffb86c",  # Orange
    "accent_danger": "#ff5555",   # Red
    "accent_cyan": "#8be9fd",     # Cyan

    # Canvas & Maze Grid Colors
    "grid_bg": "#181825",         # Canvas background
    "grid_line": "#313244",       # Subtle grid line
    "cell_empty": "#f8f9fa",      # White/Off-white for walkable path
    "cell_wall": "#21222c",       # Dark slate wall
    "cell_start": "#50fa7b",      # Vibrant Green
    "cell_end": "#ff5555",        # Vibrant Coral Red
    "cell_exploring": "#ffb86c",  # Glowing Orange/Amber
    "cell_visited": "#8be9fd",    # Bright Cyan/Sky Blue
    "cell_visited_deep": "#6272a4", # Secondary visited shade
    "cell_path": "#bd93f9",       # Neon Purple
    "cell_path_border": "#ff79c6",# Pink highlight
}

# Educational Algorithm Information
ALGORITHM_INFO: Dict[str, Dict[str, Any]] = {
    "Breadth First Search (BFS)": {
        "short_name": "BFS",
        "technique": "Level-by-level Frontier Expansion",
        "data_structure": "FIFO Queue (collections.deque)",
        "shortest_path": "Yes (Guaranteed for unweighted grids)",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "description": (
            "Breadth First Search explores all neighbor nodes at the present depth level "
            "before moving on to nodes at the next depth level. Because every step in an "
            "unweighted maze has uniform cost (1 step), BFS is guaranteed to find the "
            "shortest path from the start to the destination."
        ),
        "educational_tip": (
            "Notice how BFS expands radially like a growing circle/wavefront until it hits the target. "
            "It visits more nodes than A* because it has no sense of direction."
        )
    },
    "Depth First Search (DFS)": {
        "short_name": "DFS",
        "technique": "Deep Exploration & Backtracking",
        "data_structure": "LIFO Stack / Recursion",
        "shortest_path": "No (Finds *a* path, rarely the shortest)",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "description": (
            "Depth First Search dives as deep as possible along each branch before backtracking. "
            "It follows a single corridor until reaching a dead end, then backtracks to explore "
            "alternative corridors. It does NOT guarantee the shortest path."
        ),
        "educational_tip": (
            "Notice the long, winding path DFS takes! It might wander across the entire maze "
            "even if the destination was only 1 step away in the other direction."
        )
    },
    "Dijkstra's Algorithm": {
        "short_name": "Dijkstra",
        "technique": "Greedy Lowest-Cost Expansion",
        "data_structure": "Min-Heap Priority Queue (heapq)",
        "shortest_path": "Yes (Guaranteed optimal)",
        "time_complexity": "O((V + E) log V)",
        "space_complexity": "O(V)",
        "description": (
            "Dijkstra's Algorithm finds the shortest path between nodes by maintaining a priority queue "
            "of distances. In an unweighted maze where all edge weights are equal (1.0), Dijkstra behaves "
            "similarly to BFS, expanding outward uniformly based on total accumulated distance."
        ),
        "educational_tip": (
            "Dijkstra is the foundation of modern routing. On unweighted mazes, it explores identically "
            "to BFS, but supports weighted terrains (e.g. mud, mountains) seamlessly."
        )
    },
    "A* (A-Star) Algorithm": {
        "short_name": "A*",
        "technique": "Heuristic Informed Best-First Search",
        "data_structure": "Min-Heap Priority Queue (heapq)",
        "shortest_path": "Yes (Admissible Manhattan Heuristic)",
        "time_complexity": "O((V + E) log V) worst-case",
        "space_complexity": "O(V)",
        "description": (
            "A* evaluates nodes using f(n) = g(n) + h(n), where g(n) is the exact cost from start to node n, "
            "and h(n) is the heuristic estimate from n to destination (Manhattan distance). "
            "Because Manhattan distance is admissible (never overestimates true grid cost), A* is guaranteed "
            "to return the optimal shortest path while exploring significantly fewer nodes than Dijkstra or BFS."
        ),
        "educational_tip": (
            "Watch how A* directs its exploration beam straight toward the red destination cell, "
            "drastically reducing wasted node evaluations compared to BFS/Dijkstra!"
        )
    }
}

# Maze Generation Types
MAZE_TYPES: List[str] = [
    "Recursive Backtracker (DFS Maze)",
    "Random Obstacles (30% density)",
    "Open Maze (Sparse Obstacles)",
    "Complex Braided Maze",
    "Empty Grid (Free Draw)",
]


def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculate Manhattan distance between two (row, col) points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidean_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """Calculate Euclidean distance between two (row, col) points."""
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def format_time(seconds: float) -> str:
    """Format execution time into readable string (s or ms)."""
    if seconds < 0.001:
        return f"{seconds * 1000 * 1000:.1f} µs"
    elif seconds < 1.0:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds:.4f} s"
