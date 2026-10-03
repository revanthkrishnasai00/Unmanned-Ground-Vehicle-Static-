Here is your documentation for the battlefield static path planning project, formatted into a clean, professional, copy-pasteable Markdown template optimized for your GitHub `README.md` file.

```markdown
# UGV Shortest-Path Planning with Static Obstacles using A*

## 1. Problem Statement
An Unmanned Ground Vehicle (UGV) must travel from a user-specified start node to a user-specified goal node on a map of a small battlefield area ($70 \times 70$ km). The obstacles are known in advance and do not move. Their density is generated randomly at three levels (Low, Medium, High). The UGV must avoid all obstacles and reach the goal by the shortest distance. The path is traced, along with the Measures of Effectiveness (MOEs).

---

## 2. Approach in Brief
* Represent the battlefield as a $70 \times 70$ grid, where 1 cell = 1 km.
* Generate random obstacles at the chosen density.
* Formulate the task as a state-space search problem.
* Solve it with **A* search**, which guarantees the shortest path.
* Print the grid with the path marked and report the MOEs.

---

## 3. Map Modelling
The grid is a list of lists. A cell is `.` (free) or `X` (obstacle).

Each cell becomes an obstacle with a probability equal to the density. The start and goal cells are always kept free.

| Level | Obstacle Density |
| :--- | :--- |
| **Low** | 10% |
| **Medium** | 20% |
| **High** | 30% |

*Because obstacles are placed randomly, every run produces a different map. A very high density can block all routes, in which case the program reports that no path was found.*

---

## 4. State-Space Formulation

| Element | Definition |
| :--- | :--- |
| **State** | `(row, column)`: the cell the UGV occupies |
| **State space** | All cells inside the $70 \times 70$ grid that are not obstacles |
| **Initial state** | The start cell entered by the user |
| **Goal state / goal test** | The goal cell entered by the user; the test is `current == goal` |
| **Actions** | Move up, down, left or right (4 directions) |
| **Transition model** | New state = current cell + move. A move is illegal if it leaves the grid or enters an obstacle |
| **Step cost** | 1 km per move |
| **Path cost $g(n)$** | Number of moves from the start, in km |
| **Solution** | A sequence of cells from start to goal. The optimal solution has the lowest path cost |

---

## 5. Algorithm: A* Search
A* repeatedly expands the state with the lowest value of:

$$f(n) = g(n) + h(n)$$

* **$g(n)$**: actual cost from the start to cell $n$.
* **$h(n)$**: estimated cost from $n$ to the goal. Here it is the Manhattan distance, $\vert{}x_1 - x_2\vert{} + \vert{}y_1 - y_2\vert{}$.

### Why the Path is Optimal
With 4-direction moves, the UGV can never reach the goal in fewer moves than the Manhattan distance, so $h$ never overestimates the true remaining cost. A heuristic with this property is admissible, and A* with an admissible heuristic always returns a shortest path.

### Pseudocode
```python
open_list = [(0, start)]
g[start] = 0
visited = {}

while open_list is not empty:
  take cell with lowest f from open_list
  if already visited:
    continue
  mark visited
  count it as an explored node

  if cell == goal:
    rebuild the path from parent links and return it

  for each free neighbour of cell:
    new_g = g[cell] + 1
    if new_g < g[neighbour]:
      g[neighbour] = new_g
      parent[neighbour] = cell
      add (new_g + h(neighbour), neighbour) to open_list

return "no path"

```

*(Note: The open list is a priority queue using `heapq`, so the lowest-$f$ cell is always found quickly. The visited set ensures each cell is expanded only once.)*

---

## 6. Code Structure (`ugv_static_simple.py`)

| Function | Purpose |
| --- | --- |
| `create_grid(size, density, start, goal)` | Builds the grid with random obstacles |
| `heuristic(current, goal)` | Manhattan distance to the goal |
| `get_neighbors(grid, current)` | Returns the legal next cells (the actions) |
| `a_star(grid, start, goal)` | Runs the search; returns the path and nodes explored |
| `count_turns(path)` | Counts changes of direction along the path |
| `print_grid(grid, path, start, goal)` | Prints the map: S start, G goal, X obstacle, * path |
| **Main program** | Reads the inputs, runs A*, prints the grid and MOEs |

---

## 7. Measures of Effectiveness (MOEs)

| MOE | Meaning |
| --- | --- |
| **Obstacles** | Number and percentage of blocked cells |
| **Path length (km)** | Number of moves in the path |
| **Shortest possible (km)** | Manhattan distance, the length with no obstacles |
| **Efficiency (%)** | Shortest possible $\div$ path length $\times$ 100. 100% means no detour |
| **Number of turns** | Changes of direction, a measure of route complexity |
| **Nodes explored** | Cells A* examined, out of all free cells; a measure of search effort |
| **Computation time (ms)** | Time taken to find the path |

---

## 8. Sample Results

*Start `(2, 3)`, goal `(66, 67)`. One run per level; obstacles are random, so other runs will differ.*

| Metric | Low | Medium | High |
| --- | --- | --- | --- |
| **Obstacles** | 9.6% | 19.8% | 29.9% |
| **Path length (km)** | 128 | 130 | 130 |
| **Shortest possible (km)** | 128 | 128 | 128 |
| **Efficiency (%)** | 100.0 | 98.5 | 98.5 |
| **Number of turns** | 27 | 37 | 48 |
| **Nodes explored** | 3,254 of 4,429 | 2,722 of 3,930 | 1,169 of 3,434 |
| **Computation time (ms)** | 7.9 | 6.4 | 3.0 |

### Observations

1. The path is the shortest possible or only 2 km longer, so the UGV barely detours even at 30% obstacles.
2. Turns increase with density ($27 \to 37 \to 48$), because the UGV has to weave around more obstacles.
3. Nodes explored fall as density rises. With more obstacles, there are fewer free cells to expand, and the search is channelled along the few open routes.
4. Computation time is only a few milliseconds, so A* easily handles a $70 \times 70$ grid.
5. At high density, some start and goal pairs may have no route, and the program prints `"Path Found: No"`.

---

## 9. How to Run

1. Install Python 3 (tick *"Add python.exe to PATH"*).
2. Run the script:
```bash
python ugv_static_simple.py

```


3. Enter the start row and column, the goal row and column (each 0 to 69), and the density choice (1, 2 or 3).
4. The grid with the path and the MOEs are printed directly in the terminal. No extra libraries are needed.

---

## 10. Assumptions and Limitations

* Obstacles are known in advance and static.
* Moves are in 4 directions only, so path length is counted in Manhattan steps. Allowing diagonal moves would shorten paths slightly.
* Every cell is 1 km and every move costs the same. There is no terrain cost or turning radius.
* Obstacles are random, so results change on every run unless a fixed random seed is set.
* The program does not check that start and goal differ, or that they were not generated as obstacles. They are always forced to be free.

```

```
