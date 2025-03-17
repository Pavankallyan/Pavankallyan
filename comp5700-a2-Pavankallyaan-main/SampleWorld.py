import sys
import heapq
from collections import deque

def parse_input(file_path):
    lines = []
    if file_path == "-":
        lines = sys.stdin.read().splitlines()
    else:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    cols = int(lines[0].strip())
    rows = int(lines[1].strip())
    grid = [list(line.strip()) for line in lines[2:rows+2]]
    start = None
    samples = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                start = (r, c)
            elif grid[r][c] == '*':
                samples.append((r, c))
    return grid, start, samples

def dfs_search(start, samples, grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    stack = [(start, frozenset(), [])]
    visited = set()
    nodes_generated = 0
    nodes_expanded = 0

    while stack:
        (r, c), collected, path = stack.pop()
        nodes_expanded += 1
        if (r, c, collected) in visited:
            continue
        visited.add((r, c, collected))

        if collected == frozenset(samples):
            return path, nodes_generated, nodes_expanded

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                new_collected = set(collected)
                if (nr, nc) in samples and (nr, nc) not in collected:
                    new_collected.add((nr, nc))
                new_collected = frozenset(new_collected)
                if (nr, nc, new_collected) not in visited:
                    stack.append(((nr, nc), new_collected, path + [(dr, dc)]))
                    nodes_generated += 1
    return None, nodes_generated, nodes_expanded

def ucs_search(start, samples, grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    heap = [(0, start, frozenset(), [])]
    visited = dict()
    nodes_generated = 0
    nodes_expanded = 0

    while heap:
        cost, (r, c), collected, path = heapq.heappop(heap)
        nodes_expanded += 1
        if collected == frozenset(samples):
            return path, nodes_generated, nodes_expanded
        if (r, c, collected) in visited and visited[(r, c, collected)] <= cost:
            continue
        visited[(r, c, collected)] = cost

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                new_cost = cost + 1
                new_collected = set(collected)
                if (nr, nc) in samples and (nr, nc) not in collected:
                    new_collected.add((nr, nc))
                new_collected = frozenset(new_collected)
                if (nr, nc, new_collected) not in visited or new_cost < visited.get((nr, nc, new_collected), float('inf')):
                    heapq.heappush(heap, (new_cost, (nr, nc), new_collected, path + [(dr, dc)]))
                    nodes_generated += 1
    return None, nodes_generated, nodes_expanded

def dls(start, samples, grid, depth, nodes_generated):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    stack = [(start, frozenset(), [], 0)]
    visited = set()

    while stack:
        (r, c), collected, path, current_depth = stack.pop()
        if current_depth > depth:
            continue
        if (r, c, collected) in visited:
            continue
        visited.add((r, c, collected))

        if collected == frozenset(samples):
            return path, nodes_generated + len(stack), len(visited)

        if current_depth == depth:
            continue

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                new_collected = set(collected)
                if (nr, nc) in samples and (nr, nc) not in collected:
                    new_collected.add((nr, nc))
                new_collected = frozenset(new_collected)
                stack.append(((nr, nc), new_collected, path + [(dr, dc)], current_depth + 1))
                nodes_generated += 1
    return None, nodes_generated, len(visited)

def ids_search(start, samples, grid):
    depth = 0
    total_generated = 0
    total_expanded = 0
    while True:
        result, generated, expanded = dls(start, samples, grid, depth, total_generated)
        total_generated = generated
        total_expanded += expanded
        if result is not None:
            return result, total_generated, total_expanded
        depth += 1

def heuristic(node, samples_collected, samples, heuristic_type):
    remaining = [s for s in samples if s not in samples_collected]
    if not remaining:
        return 0
    min_dist = float('inf')
    r, c = node
    for (sr, sc) in remaining:
        if heuristic_type == 'h1':
            dist = abs(r - sr) + abs(c - sc)
        elif heuristic_type == 'h2':
            dist = max(abs(r - sr), abs(c - sc))
        else:
            dist = 0
        if dist < min_dist:
            min_dist = dist
    return min_dist

def astar_search(start, samples, grid, heuristic_type):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    heap = []
    initial_collected = frozenset()
    heapq.heappush(heap, (0, 0, start, initial_collected, []))
    visited = dict()
    nodes_generated = 1
    nodes_expanded = 0

    while heap:
        f_cost, g_cost, (r, c), collected, path = heapq.heappop(heap)
        nodes_expanded += 1
        if collected == frozenset(samples):
            return path, nodes_generated, nodes_expanded
        if (r, c, collected) in visited and visited[(r, c, collected)] <= g_cost:
            continue
        visited[(r, c, collected)] = g_cost

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                new_g = g_cost + 1
                new_collected = set(collected)
                if (nr, nc) in samples and (nr, nc) not in collected:
                    new_collected.add((nr, nc))
                new_collected = frozenset(new_collected)
                h_val = heuristic((nr, nc), new_collected, samples, heuristic_type)
                f_val = new_g + h_val
                if (nr, nc, new_collected) not in visited or new_g < visited.get((nr, nc, new_collected), float('inf')):
                    heapq.heappush(heap, (f_val, new_g, (nr, nc), new_collected, path + [(dr, dc)]))
                    nodes_generated += 1
    return None, nodes_generated, nodes_expanded

def main():
    if len(sys.argv) < 2:
        print("Usage: python SampleWorld.py <algorithm> [heuristic] < input_file")
        return
    algorithm = sys.argv[1]
    heuristic_type = sys.argv[2] if len(sys.argv) > 2 and algorithm == 'astar' else None
    grid, start, samples = parse_input("-")
    samples = frozenset(samples)

    # Handle initial sample collection at start position
    collected = set()
    actions = []
    if start in samples:
        actions.append('S')
        collected.add(start)

    if algorithm == 'dfs':
        path, generated, expanded = dfs_search(start, samples, grid)
    elif algorithm == 'ucs':
        path, generated, expanded = ucs_search(start, samples, grid)
    elif algorithm == 'ids':
        path, generated, expanded = ids_search(start, samples, grid)
    elif algorithm == 'astar':
        if heuristic_type not in ['h0', 'h1', 'h2']:
            print("Invalid heuristic for A*. Use h0, h1, or h2.")
            return
        path, generated, expanded = astar_search(start, samples, grid, heuristic_type)
    else:
        print("Invalid algorithm. Choose dfs, ucs, ids, or astar.")
        return

    if path is None:
        print("No solution found.")
    else:
        current_pos = start
        # Process each move to build actions
        for move in path:
            dr, dc = move
            current_pos = (current_pos[0] + dr, current_pos[1] + dc)
            # Append movement action
            actions.append('U' if dr == -1 else 'D' if dr == 1 else 'L' if dc == -1 else 'R')
            # Check for sample collection
            if current_pos in samples and current_pos not in collected:
                actions.append('S')
                collected.add(current_pos)
        # Print to terminal
        print('\n'.join(actions))
        print(f"{generated} nodes generated")
        print(f"{expanded} nodes expanded")

if __name__ == "__main__":
    main()