from collections import deque

def shortest_path(start, goal, game_map):
    
    rows, cols = game_map.shape
    visited = set()
    queue = deque([(start, 0)])  

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:

        (x, y), dist = queue.popleft()

        if (x, y) == tuple(goal):
            return dist

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                if game_map[nx][ny] != 2:  
                    queue.append(((nx, ny), dist + 1))
    return 0