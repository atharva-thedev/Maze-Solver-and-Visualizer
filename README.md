# 🧩 Maze Solver & Visualizer — Python College Project

An interactive desktop application built in pure Python and Tkinter that generates intricate mazes, solves them in real-time using classic pathfinding algorithms (**BFS, DFS, Dijkstra, A\***), animates the exploration step-by-step, and delivers deep educational insights and performance benchmarks.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [Technologies Used](#-technologies-used)
4. [Pathfinding Algorithms](#-pathfinding-algorithms)
   - [Breadth First Search (BFS)](#1-breadth-first-search-bfs)
   - [Depth First Search (DFS)](#2-depth-first-search-dfs)
   - [Dijkstra's Algorithm](#3-dijkstras-algorithm)
   - [A* (A-Star) Algorithm](#4-a-a-star-algorithm)
5. [Complexity Analysis & Comparison](#-complexity-analysis--comparison)
6. [Maze Generation Algorithms](#-maze-generation-algorithms)
7. [GUI Design & Color Palette](#-gui-design--color-palette)
8. [Project Architecture](#-project-architecture)
9. [Installation & Requirements](#-installation--requirements)
10. [How to Run](#-how-to-run)
11. [How to Use (Interactive Guide)](#-how-to-use-interactive-guide)
12. [Unit Testing & Verification](#-unit-testing--verification)
13. [Future Improvements](#-future-improvements)
14. [Learning Outcomes](#-learning-outcomes)

---

## 🎯 Project Overview

In computer science, pathfinding is a core problem with direct applications in robotics, GPS navigation, AI game development, and network routing.

This project offers an intuitive, visually stunning visualizer built **strictly with Python 3 and Tkinter**, allowing students and educators to:
- Visually observe how different graph traversal and shortest-path algorithms navigate corridors and dead ends.
- Understand the practical differences between unguided level-by-level search (BFS/Dijkstra) and heuristic-informed search (A*).
- Benchmark all algorithms simultaneously on the identical maze topology.

---

## ✨ Key Features

- **Pure Python & Tkinter Desktop GUI**: No web frameworks, no Electron, no external pip dependencies.
- **4 Pathfinding Algorithms Implemented From Scratch**:
  - Breadth First Search (BFS)
  - Depth First Search (DFS)
  - Dijkstra's Algorithm
  - A* (A-Star) with Manhattan Distance Heuristic
- **4 Procedural Maze Generators**:
  - Recursive Backtracker (Randomized DFS Maze — perfect corridors)
  - Random Obstacles (with density tuning)
  - Open Maze (Pillar & cluster obstacles)
  - Complex Braided Maze (Multiple loops and alternative paths)
  - Freehand Drawing Mode (Custom walls)
- **Fluid, Non-Blocking Animation**:
  - Implemented using Tkinter's `root.after()` event loop scheduling.
  - Controls to **Start**, **Pause / Resume**, **Stop**, and **Change Speed** in real-time.
- **Side-by-Side Algorithm Benchmark & Comparison**:
  - Compare BFS, DFS, Dijkstra, and A* on the exact same maze.
  - Displays metrics for Path Length, Nodes Visited, Calculation Time ($\mu$s/ms), and Shortest Path guarantee.
- **Interactive Mouse Drawing**:
  - Click to place custom **Start** (🟢) and **Destination** (🔴) points.
  - Drag to paint and erase walls interactively.
- **Dynamic Educational Information Card**:
  - Real-time display of Time Complexity, Space Complexity, Data Structures, and Algorithmic Insights when an algorithm is selected.
- **Live Statistics Panel**:
  - Real-time counter of explored nodes, path length, execution time, and grid exploration ratio.
- **High-DPI Scaling & Resizable Canvas**:
  - Automatically calculates grid dimensions and centers cells dynamically upon resizing.

---

## 🛠️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3.8+** | Core programming language |
| **Tkinter / ttk** | Native desktop graphical user interface |
| **`collections.deque`** | High-performance $O(1)$ FIFO queue for BFS |
| **`heapq`** | Min-Heap priority queue for Dijkstra and A* |
| **`time.perf_counter`** | Sub-millisecond execution benchmarking |
| **`unittest`** | Automated testing suite |

---

## 🧠 Pathfinding Algorithms

### 1. Breadth First Search (BFS)
- **Technique**: Level-by-level frontier expansion.
- **Data Structure**: FIFO Queue (`collections.deque`).
- **Shortest Path**: **Yes** (Guaranteed for unweighted uniform grids).
- **Time Complexity**: $O(V + E)$
- **Space Complexity**: $O(V)$
- **How it Works**: Explores all neighbors at depth $d$ before proceeding to depth $d+1$. It radiates outward in a growing diamond/circle until the destination is reached.

### 2. Depth First Search (DFS)
- **Technique**: Deep branch exploration with backtracking.
- **Data Structure**: LIFO Stack / Recursion.
- **Shortest Path**: **No** (Finds *a* path, often long and winding).
- **Time Complexity**: $O(V + E)$
- **Space Complexity**: $O(V)$
- **How it Works**: Explores as far as possible along each branch before backtracking at dead ends. Great for maze generation, but poor for shortest-path routing.

### 3. Dijkstra's Algorithm
- **Technique**: Greedy lowest-cost node expansion.
- **Data Structure**: Min-Heap Priority Queue (`heapq`).
- **Shortest Path**: **Yes** (Guaranteed optimal).
- **Time Complexity**: $O((V + E) \log V)$
- **Space Complexity**: $O(V)$
- **How it Works**: Maintains a priority queue sorted by cumulative distance $g(n)$ from the start node. On uniform cost mazes (cost = 1 per step), it expands radially similarly to BFS.

### 4. A* (A-Star) Algorithm
- **Technique**: Heuristic-guided best-first search.
- **Data Structure**: Min-Heap Priority Queue (`heapq`).
- **Heuristic Function**: Manhattan Distance:
  $$h(n) = |r_n - r_{end}| + |c_n - c_{end}|$$
- **Evaluation Function**:
  $$f(n) = g(n) + h(n)$$
- **Shortest Path**: **Yes** (Because Manhattan distance is admissible on 4-directional grids, $h(n) \le h^*(n)$).
- **Time Complexity**: $O((V + E) \log V)$ worst-case; practically much faster.
- **Space Complexity**: $O(V)$
- **Why A* outperforms Dijkstra**: By factoring in distance to the target, A* aims its exploration beam directly toward the destination, reducing wasted node evaluations.

---

## 📊 Complexity Analysis & Comparison

| Algorithm | Data Structure | Time Complexity | Space Complexity | Shortest Path? | Heuristic? |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **BFS** | FIFO Queue | $O(V + E)$ | $O(V)$ | ✅ Yes | ❌ No |
| **DFS** | LIFO Stack | $O(V + E)$ | $O(V)$ | ❌ No | ❌ No |
| **Dijkstra** | Min-Heap Priority Queue | $O((V + E) \log V)$ | $O(V)$ | ✅ Yes | ❌ No |
| **A\*** | Min-Heap Priority Queue | $O((V + E) \log V)$ | $O(V)$ | ✅ Yes | ✅ Manhattan |

*Where $V = \text{Rows} \times \text{Cols}$ (number of cells) and $E \le 4V$ (walkable orthogonal edges).*

---

## 🌀 Maze Generation Algorithms

1. **Recursive Backtracker (DFS Maze)**:
   Carves corridors through a grid filled with walls by stepping 2 cells at a time with randomized direction order and stack backtracking. Produces intricate, winding, perfect mazes with zero loops and guaranteed solvability.
2. **Random Obstacles**:
   Spreads walls randomly across the grid at a controlled density (30%), preserving safe zones around start and end points.
3. **Open Field (Sparse Pillars)**:
   Creates open areas with pillar clusters to visually demonstrate the directional focus of A* vs the circular spread of BFS.
4. **Braided Maze**:
   Generates a recursive backtracker maze and knocks down ~15% of dead-end walls to introduce multiple loops and alternative routes.

---

## 🎨 GUI Design & Color Palette

The interface is built with a modern dark theme:

| Cell Type | Visual Color | Meaning |
| :--- | :--- | :--- |
| **Start Point** | `🟢 #50fa7b` (Vibrant Green) | Origin of search |
| **Destination** | `🔴 #ff5555` (Coral Red) | Target destination |
| **Wall** | `🧱 #21222c` (Dark Slate) | Impassable barrier |
| **Empty** | `⬜ #f8f9fa` (Crisp Off-White) | Walkable corridor |
| **Currently Exploring** | `🟡 #ffb86c` (Glowing Amber) | Node currently popped from frontier |
| **Visited Nodes** | `🔵 #8be9fd` (Sky Blue) | Explored cells |
| **Shortest Path** | `🟣 #bd93f9` (Neon Purple) | Final reconstructed solution path |

---

## 📂 Project Architecture

```text
Maze-Solver-Visualizer/
│
├── main.py             # Application entry point & High-DPI setup
├── gui.py              # Tkinter user interface, controls, and layout
├── maze.py             # Maze 2D grid model, cell states, bounds & queries
├── algorithms.py       # BFS, DFS, Dijkstra, and A* solvers & generators
├── generator.py        # Procedural maze generators (DFS, Random, Open, Braided)
├── visualizer.py       # Canvas rendering & non-blocking after() animation
├── utils.py            # Color palette, presets, algorithm metadata & math helpers
├── test_maze.py        # Comprehensive automated unit test suite
├── requirements.txt    # Standard library documentation (Zero external dependencies)
└── README.md           # Comprehensive project documentation
```

---

## 📥 Installation & Requirements

### Requirements
- **Python 3.8 or higher**
- Tkinter (included with standard Python installers on Windows and macOS)

*On Linux (Ubuntu/Debian), if Tkinter is not pre-installed:*
```bash
sudo apt-get install python3-tk
```

---

## 🚀 How to Run

1. Clone or navigate to the project directory:
   ```bash
   cd "path/to/Maze-Solver-Visualizer"
   ```

2. Run the application directly:
   ```bash
   python main.py
   ```

---

## 🎮 How to Use (Interactive Guide)

1. **Choose a Maze Type & Size**:
   - Select your preferred grid size (Small 15x15, Medium 25x25, Large 35x35, Extra Large 45x45).
   - Select a maze pattern from the dropdown and click **"🎲 Generate New Maze"**.
2. **Customize Start & Destination (Optional)**:
   - Select the **"🟢 Set Start Point"** radio button and click any empty cell.
   - Select the **"🔴 Set Destination Point"** radio button and click another empty cell.
3. **Draw / Erase Custom Walls (Optional)**:
   - Select the **"🧱 Draw / Erase Walls"** tool and click or drag across the grid.
4. **Select an Algorithm & Speed**:
   - Choose BFS, DFS, Dijkstra, or A*.
   - Review the **Algorithm Insights** card on the right for time complexity and behavior.
   - Pick your desired animation speed (Slow, Medium, Fast, Ultra Fast).
5. **Start Visualization**:
   - Click **"🚀 Visualize Algorithm"**.
   - Watch the animated search and final purple path reconstruction.
   - Use **"⏸️ Pause / Resume"** or **"🛑 Stop"** anytime.
6. **Compare All Algorithms**:
   - Click **"📊 Compare All Algorithms"** to see a side-by-side performance benchmark table showing path length, nodes visited, and exact run times for all 4 algorithms on the same maze!

---

## 🧪 Unit Testing & Verification

Run the automated test suite with:

```bash
python -m unittest test_maze.py -v
```

### Test Coverage Highlights:
- Grid bounds checking, endpoint setting, wall toggling.
- Procedural generation solvability tests.
- Mathematical path optimality: Verifies BFS, Dijkstra, and A* yield identical shortest path lengths on open grids.
- Edge cases: Unsolvable maze (completely walled in), Start adjacent to End, Start equals End, Large 45x45 grid performance.

---

## 🔮 Future Improvements

- **Weighted Terrains**: Support for mud/water tiles with higher movement costs ($c > 1$) to further highlight Dijkstra vs BFS differences.
- **Diagonal Movement**: Optional 8-directional traversal with Euclidean distance heuristics ($h(n) = \sqrt{\Delta r^2 + \Delta c^2}$).
- **Bidirectional Search**: Bidirectional BFS and Bidirectional A* exploring simultaneously from Start and End.
- **Maze Export / Import**: Save and load custom maze layouts to JSON or text format.

---

## 🎓 Learning Outcomes

- **Data Structure Selection**: Understanding the practical differences between FIFO Queues, LIFO Stacks, and Min-Heap Priority Queues in pathfinding.
- **Heuristic Search**: Demonstrating how an admissible heuristic (Manhattan distance) directs search without compromising path optimality.
- **GUI Programming**: Mastering non-blocking asynchronous event scheduling (`root.after()`) in desktop graphical applications.
- **Modular Software Engineering**: Designing decoupled, clean Python modules separating presentation (`gui.py`), animation (`visualizer.py`), domain logic (`maze.py`), and algorithms (`algorithms.py`).
