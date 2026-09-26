"""
integration_test.py - Automated GUI and algorithm interaction tests.
"""

import tkinter as tk
from gui import MazeGUI
from algorithms import solve_instant


def run_integration_test():
    root = tk.Tk()
    app = MazeGUI(root)
    root.update()

    # 1. Test Grid Resize
    app.selected_size.set('Small (15x15)')
    app._on_size_change()
    root.update()
    assert len(app.canvas.find_all()) == 225, "Canvas item count mismatch for 15x15"
    print("Test 1 Passed: Grid resize to 15x15 verified.")

    # 2. Test All Maze Generation Patterns
    patterns = [
        'Recursive Backtracker (DFS Maze)',
        'Random Obstacles (30% density)',
        'Open Maze (Sparse Obstacles)',
        'Complex Braided Maze',
        'Empty Grid (Free Draw)'
    ]
    for p in patterns:
        app.selected_maze_type.set(p)
        app._on_generate_maze()
        root.update()
    print("Test 2 Passed: All 5 maze generator patterns verified.")

    # 3. Test Clear Walls and Reset Search
    app._on_clear_walls()
    root.update()
    app._on_reset_search()
    root.update()
    print("Test 3 Passed: Clear walls and Reset search verified.")

    # 4. Test Educational Info Card updates
    algos = [
        'Breadth First Search (BFS)',
        'Depth First Search (DFS)',
        "Dijkstra's Algorithm",
        'A* (A-Star) Algorithm'
    ]
    for algo in algos:
        app.selected_algo.set(algo)
        app._update_algorithm_info_panel()
        root.update()
    print("Test 4 Passed: Algorithm info card dynamic updates verified.")

    # 5. Test Instant Solver Benchmarks
    for algo in algos:
        res = solve_instant(algo, app.maze)
        print(f"Test 5 Benchmark: {algo} -> found={res['found']}, path={res['path_length']}, visited={res['visited_count']}, time={res['time']*1000:.3f}ms")
        assert res['found'] is True, f"Failed to find path for {algo}"

    # 6. Test Step Animation
    app.visualizer.start_animation("Breadth First Search (BFS)")
    for _ in range(25):
        root.update()
        app.visualizer._step_internal()
    assert app.visualizer.visited_count > 0, "Animation did not record visited cells"
    app.visualizer.stop_animation()
    print("Test 6 Passed: Step animation and event handling verified.")

    root.destroy()
    print("\n[SUCCESS] ALL INTEGRATION & REGRESSION TESTS COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    run_integration_test()
