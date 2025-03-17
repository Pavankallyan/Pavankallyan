import sys
import heapq

# the DFS algorithm
def dfs_search(start, samples, grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    visited = set()
    stack = [(start, [])] 
    nodes_generated = 0

    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        if all(sample in visited for sample in samples):
            return path, nodes_generated, len(visited)

        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and (nr, nc) not in visited:
                stack.append(((nr, nc), path + [(dr, dc)]))
                nodes_generated += 1
    return None, nodes_generated, len(visited)

# the UCS algorithm
def ucs_search(start, samples, grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
    visited = set()
    pq = [(0, start, [])] 
    nodes_generated = 0

    while pq:
        cost, current, path = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        
        if all(sample in visited for sample in samples):
            return path, nodes_generated, len(visited)

        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and (nr, nc) not in visited:
                heapq.heappush(pq, (cost + 1, (nr, nc), path + [(dr, dc)]))
                nodes_generated += 1
    return None, nodes_generated, len(visited)


def parse_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    cols = int(lines[0].strip())
    rows = int(lines[1].strip())
    grid = [line.strip() for line in lines[2:]]

    start = None
    samples = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                start = (r, c)
            elif grid[r][c] == '*':
                samples.append((r, c))
    return grid, start, samples

# Main function
def main():
    if len(sys.argv) < 3:
        print("Usage: python3 SampleWorld.py <algorithm> <file_path>")
        return

    algorithm = sys.argv[1]
    file_path = sys.argv[2]

    grid, start, samples = parse_input(file_path)

    if not start:
        print("No starting position (@) found in the grid!")
        return
    if not samples:
        print("No samples (*) found in the grid!")
        return
    if algorithm == "dfs":
        path, nodes_generated, nodes_expanded = dfs_search(start, samples, grid)
    elif algorithm == "ucs":
        path, nodes_generated, nodes_expanded = ucs_search(start, samples, grid)
    else:
        print("Invalid algorithm! Use 'dfs' or 'ucs'.")
        return

    # Output
    if path is None:
        print("No solution found!")
    else:
        directions_map = {(-1, 0): "U", (1, 0): "D", (0, -1): "L", (0, 1): "R"}
        directions = [directions_map[step] for step in path]
        print("Action list:")
        print("\n".join(directions))
        print(f"\n{nodes_generated} nodes generated")
        print(f"{nodes_expanded} nodes expanded")

if __name__ == "__main__":
    main()