import random
import heapq
import time

SIZE = 70          # 70 x 70 km battlefield, 1 cell = 1 km


def create_grid(size, density, start, goal):
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            if (i, j) == start or (i, j) == goal:
                row.append(".")
            elif random.random() < density:
                row.append("X")
            else:
                row.append(".")
        grid.append(row)
    return grid


def heuristic(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def get_neighbors(grid, current):
    x, y = current
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] != "X":
                neighbors.append((nx, ny))
    return neighbors


def a_star(grid, start, goal):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    g_cost = {start: 0}
    parent = {start: None}
    visited = set()
    nodes_explored = 0

    while priority_queue:
        f, current = heapq.heappop(priority_queue)

        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, nodes_explored

        for neighbor in get_neighbors(grid, current):
            new_g = g_cost[current] + 1
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                f = new_g + heuristic(neighbor, goal)
                parent[neighbor] = current
                heapq.heappush(priority_queue, (f, neighbor))

    return None, nodes_explored


def count_turns(path):
    turns = 0
    for i in range(1, len(path) - 1):
        d1 = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
        d2 = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1])
        if d1 != d2:
            turns += 1
    return turns


def print_grid(grid, path, start, goal):
    path_set = set(path) if path else set()
    for i in range(len(grid)):
        row = ""
        for j in range(len(grid[0])):
            if (i, j) == start:
                row += "S "
            elif (i, j) == goal:
                row += "G "
            elif (i, j) in path_set:
                row += "* "
            else:
                row += grid[i][j] + " "
        print(row)


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

print("UGV A* PATH FINDING - STATIC OBSTACLES")

print("\nEnter Start Position")
start = (int(input("Start row (0-69): ")), int(input("Start column (0-69): ")))

print("\nEnter Goal Position")
goal = (int(input("Goal row (0-69): ")), int(input("Goal column (0-69): ")))

for p in (start, goal):
    if not (0 <= p[0] < SIZE and 0 <= p[1] < SIZE):
        print("Position must be between 0 and", SIZE - 1)
        exit()

print("\nSelect Obstacle Density")
print("1. Low (10%)")
print("2. Medium (20%)")
print("3. High (30%)")
choice = input("Enter your choice (1/2/3): ")

if choice == "1":
    density_name, density = "Low", 0.10
elif choice == "2":
    density_name, density = "Medium", 0.20
elif choice == "3":
    density_name, density = "High", 0.30
else:
    print("Invalid choice.")
    exit()

grid = create_grid(SIZE, density, start, goal)

begin = time.time()
path, nodes_explored = a_star(grid, start, goal)
run_time = (time.time() - begin) * 1000

obstacles = sum(row.count("X") for row in grid)

print("\n")
print("=" * 50)
print("UGV BATTLEFIELD (70 x 70 km)")
print("Obstacle Density:", density_name)
print("S=start  G=goal  X=obstacle  *=path")
print("=" * 50)
print()
print_grid(grid, path, start, goal)

print("\n")
print("=" * 50)
print("MEASURES OF EFFECTIVENESS")
print("=" * 50)
print("Obstacles          :", obstacles, "cells (%.1f %%)" % (100 * obstacles / SIZE ** 2))

if path:
    path_length = len(path) - 1
    manhattan = heuristic(start, goal)
    print("Path Found         : Yes")
    print("Path Length        :", path_length, "km")
    print("Shortest Possible  :", manhattan, "km (no obstacles)")
    print("Efficiency         : %.1f %%" % (100 * manhattan / path_length))
    print("Number of Turns    :", count_turns(path))
    print("Nodes Explored     :", nodes_explored, "of", SIZE ** 2 - obstacles)
    print("Computation Time   : %.2f ms" % run_time)
    print("\nPath:")
    print(path)
else:
    print("Path Found         : No")
    print("Nodes Explored     :", nodes_explored)