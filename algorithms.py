"""
algorithms.py - Pathfinding Algorithms Implementation.
Includes BFS, DFS, Dijkstra, and A* with step-by-step visualization generators
and instant benchmark solving methods.
"""

import time
import heapq
from collections import deque
from typing import Dict, List, Tuple, Optional, Generator, Any
from maze import Maze
from utils import manhattan_distance


def reconstruct_path(parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]],
                     start: Tuple[int, int],
                     end: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Reconstructs the path from start to end by tracing back parent pointers.
    Returns list of (row, col) coordinates from start to end inclusive.
    """
    if end not in parent:
        return []
    
    path = []
    curr: Optional[Tuple[int, int]] = end
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path.reverse()
    return path if path and path[0] == start else []


# =====================================================================
# 1. BREADTH FIRST SEARCH (BFS)
# =====================================================================

def bfs_generator(maze: Maze) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
    """
    Breadth First Search (BFS) generator for step-by-step animation.
    Uses FIFO Queue (collections.deque) for level-by-level exploration.
    Guarantees shortest path on unweighted grids.
    """
    start_time = time.perf_counter()
    start = maze.start
    end = maze.end

    if start == end:
        elapsed = time.perf_counter() - start_time
        return {"found": True, "path": [start], "visited_count": 1, "time": elapsed}

    queue: deque = deque([start])
    visited = {start}
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    visited_order: List[Tuple[int, int]] = [start]

    found = False

    while queue:
        curr = queue.popleft()

        yield {"type": "exploring", "cell": curr}

        if curr == end:
            found = True
            break

        for neighbor in maze.get_neighbors(curr[0], curr[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = curr
                visited_order.append(neighbor)
                queue.append(neighbor)
                yield {"type": "visited", "cell": neighbor}

    elapsed = time.perf_counter() - start_time
    path = reconstruct_path(parent, start, end) if found else []

    if found and path:
        yield {"type": "path_start", "path": path}
        for p_cell in path:
            yield {"type": "path_step", "cell": p_cell}

    return {
        "found": found,
        "path": path,
        "path_length": len(path),
        "visited_count": len(visited_order),
        "time": elapsed
    }


def bfs_solve(maze: Maze) -> Dict[str, Any]:
    """Instant BFS solver without generator overhead for benchmarks."""
    start_time = time.perf_counter()
    start = maze.start
    end = maze.end

    if start == end:
        return {"found": True, "path": [start], "path_length": 1, "visited_count": 1, "time": time.perf_counter() - start_time}

    queue = deque([start])
    visited = {start}
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    visited_count = 1
    found = False

    while queue:
        curr = queue.popleft()
        if curr == end:
            found = True
            break

        for neighbor in maze.get_neighbors(curr[0], curr[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = curr
                visited_count += 1
                queue.append(neighbor)

    elapsed = time.perf_counter() - start_time
    path = reconstruct_path(parent, start, end) if found else []
    return {
        "found": found,
        "path": path,
        "path_length": len(path),
        "visited_count": visited_count,
        "time": elapsed
    }


# =====================================================================
# 2. DEPTH FIRST SEARCH (DFS)
# =====================================================================

def dfs_generator(maze: Maze) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
    """
    Depth First Search (DFS) generator for step-by-step animation.
    Uses LIFO Stack to explore deeply along corridors before backtracking.
    Does NOT guarantee the shortest path.
    """
    start_time = time.perf_counter()
    start = maze.start
    end = maze.end

    if start == end:
        elapsed = time.perf_counter() - start_time
        return {"found": True, "path": [start], "visited_count": 1, "time": elapsed}

    stack: List[Tuple[int, int]] = [start]
    visited = set()
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    visited_order: List[Tuple[int, int]] = []
    found = False

    while stack:
        curr = stack.pop()

        if curr in visited:
            continue

        visited.add(curr)
        visited_order.append(curr)

        yield {"type": "exploring", "cell": curr}
        yield {"type": "visited", "cell": curr}

        if curr == end:
            found = True
            break

        # Reverse neighbor order so exploration pushes in standard order
        for neighbor in reversed(maze.get_neighbors(curr[0], curr[1])):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = curr
                stack.append(neighbor)

    elapsed = time.perf_counter() - start_time
    path = reconstruct_path(parent, start, end) if found else []

    if found and path:
        yield {"type": "path_start", "path": path}
        for p_cell in path:
            yield {"type": "path_step", "cell": p_cell}

    return {
        "found": found,
        "path": path,
        "path_length": len(path),
        "visited_count": len(visited_order),
        "time": elapsed
    }


def dfs_solve(maze: Maze) -> Dict[str, Any]:
    """Instant DFS solver for benchmarks."""
    start_time = time.perf_counter()
    start = maze.start
    end = maze.end

    if start == end:
        return {"found": True, "path": [start], "path_length": 1, "visited_count": 1, "time": time.perf_counter() - start_time}

    stack = [start]
    visited = set()
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    visited_count = 0
    found = False

    while stack:
        curr = stack.pop()
        if curr in visited:
            continue

        visited.add(curr)
        visited_count += 1

        if curr == end:
            found = True
            break

        for neighbor in reversed(maze.get_neighbors(curr[0], curr[1])):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = curr
                stack.append(neighbor)

    elapsed = time.perf_counter() - start_time
    path = reconstruct_path(parent, start, end) if found else []
    return {
        "found": found,
        "path": path,
        "path_length": len(path),
        "visited_count": visited_count,
        "time": elapsed
    }


# =====================================================================
# 3. DIJKSTRA'S ALGORITHM
# =====================================================================

def dijkstra_generator(maze: Maze) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
    """
    Dijkstra's Algorithm generator for step-by-step animation.
    Uses Min-Heap Priority Queue (heapq) to always expand the cheapest known node.
    Guarantees shortest path.
    """
    start_time = time.perf_counter()
    start = maze.start
    end = maze.end

    if start == end:
        elapsed = time.perf_counter() - start_time
        return {"found": True, "path": [start], "visited_count": 1, "time": elapsed}

    # Priority queue stores tuples: (distance, insertion_counter, (row, col))
    counter = 0
    pq: List[Tuple[float, int, Tuple[int, int]]] = [(0, counter, start)]
    distances: Dict[Tuple[int, int], float] = {start: 0}
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    visited = set()
    visited_order: List[Tuple[int, int]] = []
    found = False

    while pq:
        dist, _, curr = heapq.heappop(pq)

        if curr in visited:
            continue

        visited.add(curr)
        visited_order.append(curr)

        yield {"type": "exploring", "cell": curr}
        yield {"type": "visited", "cell": curr}

        if curr == end:
            found = True
            break

        for neighbor in maze.get_neighbors(curr[0], curr[1]):
            if neighbor in visited:
                continue

            new_dist = dist + 1  # Uniform weight = 1
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                parent[neighbor] = curr
                counter += 1
                heapq.heappush(pq, (new_dist, counter, neighbor))

    elapsed = time.perf_counter() - start_time
    path = reconstruct_path(parent, start, end) if found else []

    if found and path:
        yield {"type": "path_start", "path": path}
        for p_cell in path:
            yield {"type": "path_step", "cell": p_cell}

    return {
        "found": found,
        "path": path,
        "path_length": len(path),
        "visited_count": len(visited_order),
        "time": elapsed
    }


def dijkstra_solve(maze: Maze) -> Dict[str, Any]:
    """Instant Dijkstra solver for benchmarks."""
    start_time = time.perf_counter()
    start = maze.start
    end = maze.end

    if start == end:
        return {"found": True, "path": [start], "path_length": 1, "visited_count": 1, "time": time.perf_counter() - start_time}

    counter = 0
    pq = [(0, counter, start)]
    distances = {start: 0}
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    visited = set()
    visited_count = 0
    found = False

    while pq:
        dist, _, curr = heapq.heappop(pq)
        if curr in visited:
            continue

        visited.add(curr)
        visited_count += 1

        if curr == end:
            found = True
            break

        for neighbor in maze.get_neighbors(curr[0], curr[1]):
            if neighbor in visited:
                continue

            new_dist = dist + 1
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                parent[neighbor] = curr
                counter += 1
                heapq.heappush(pq, (new_dist, counter, neighbor))

    elapsed = time.perf_counter() - start_time
    path = reconstruct_path(parent, start, end) if found else []
    return {
        "found": found,
        "path": path,
        "path_length": len(path),
        "visited_count": visited_count,
        "time": elapsed
    }


# =====================================================================
# 4. A* (A-STAR) ALGORITHM
# =====================================================================

def astar_generator(maze: Maze) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
    """
    A* Algorithm generator for step-by-step animation.
    Uses Min-Heap Priority Queue with f(n) = g(n) + h(n) where h(n) is Manhattan distance.
    Guarantees shortest path while minimizing visited nodes.
    """
    start_time = time.perf_counter()
    start = maze.start
    end = maze.end

    if start == end:
        elapsed = time.perf_counter() - start_time
        return {"found": True, "path": [start], "visited_count": 1, "time": elapsed}

    counter = 0
    g_score: Dict[Tuple[int, int], float] = {start: 0}
    h_start = manhattan_distance(start, end)
    f_score: Dict[Tuple[int, int], float] = {start: h_start}

    # Heap contains: (f_score, h_score, tie_counter, cell)
    pq: List[Tuple[float, float, int, Tuple[int, int]]] = [(h_start, h_start, counter, start)]
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    visited = set()
    visited_order: List[Tuple[int, int]] = []
    found = False

    while pq:
        f, h, _, curr = heapq.heappop(pq)

        if curr in visited:
            continue

        visited.add(curr)
        visited_order.append(curr)

        yield {"type": "exploring", "cell": curr}
        yield {"type": "visited", "cell": curr}

        if curr == end:
            found = True
            break

        curr_g = g_score[curr]
        for neighbor in maze.get_neighbors(curr[0], curr[1]):
            if neighbor in visited:
                continue

            tentative_g = curr_g + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                h_neighbor = manhattan_distance(neighbor, end)
                neighbor_f = tentative_g + h_neighbor
                f_score[neighbor] = neighbor_f
                parent[neighbor] = curr
                counter += 1
                heapq.heappush(pq, (neighbor_f, h_neighbor, counter, neighbor))

    elapsed = time.perf_counter() - start_time
    path = reconstruct_path(parent, start, end) if found else []

    if found and path:
        yield {"type": "path_start", "path": path}
        for p_cell in path:
            yield {"type": "path_step", "cell": p_cell}

    return {
        "found": found,
        "path": path,
        "path_length": len(path),
        "visited_count": len(visited_order),
        "time": elapsed
    }


def astar_solve(maze: Maze) -> Dict[str, Any]:
    """Instant A* solver for benchmarks."""
    start_time = time.perf_counter()
    start = maze.start
    end = maze.end

    if start == end:
        return {"found": True, "path": [start], "path_length": 1, "visited_count": 1, "time": time.perf_counter() - start_time}

    counter = 0
    g_score = {start: 0}
    h_start = manhattan_distance(start, end)
    pq = [(h_start, h_start, counter, start)]
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    visited = set()
    visited_count = 0
    found = False

    while pq:
        f, h, _, curr = heapq.heappop(pq)
        if curr in visited:
            continue

        visited.add(curr)
        visited_count += 1

        if curr == end:
            found = True
            break

        curr_g = g_score[curr]
        for neighbor in maze.get_neighbors(curr[0], curr[1]):
            if neighbor in visited:
                continue

            tentative_g = curr_g + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                h_neighbor = manhattan_distance(neighbor, end)
                parent[neighbor] = curr
                counter += 1
                heapq.heappush(pq, (tentative_g + h_neighbor, h_neighbor, counter, neighbor))

    elapsed = time.perf_counter() - start_time
    path = reconstruct_path(parent, start, end) if found else []
    return {
        "found": found,
        "path": path,
        "path_length": len(path),
        "visited_count": visited_count,
        "time": elapsed
    }


# =====================================================================
# DISPATCHER METHODS
# =====================================================================

def get_algorithm_generator(algo_name: str, maze: Maze):
    """Returns the step-by-step generator for the requested algorithm."""
    if "BFS" in algo_name or "Breadth" in algo_name:
        return bfs_generator(maze)
    elif "DFS" in algo_name or "Depth" in algo_name:
        return dfs_generator(maze)
    elif "Dijkstra" in algo_name:
        return dijkstra_generator(maze)
    elif "A*" in algo_name or "A-Star" in algo_name:
        return astar_generator(maze)
    else:
        return bfs_generator(maze)


def solve_instant(algo_name: str, maze: Maze) -> Dict[str, Any]:
    """Executes the specified algorithm instantly and returns performance stats."""
    if "BFS" in algo_name or "Breadth" in algo_name:
        return bfs_solve(maze)
    elif "DFS" in algo_name or "Depth" in algo_name:
        return dfs_solve(maze)
    elif "Dijkstra" in algo_name:
        return dijkstra_solve(maze)
    elif "A*" in algo_name or "A-Star" in algo_name:
        return astar_solve(maze)
    else:
        return bfs_solve(maze)
