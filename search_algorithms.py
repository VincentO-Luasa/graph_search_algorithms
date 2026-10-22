def build_path(parents, start, goal):
    if goal not in parents:
        return []
    path = [goal]
    while path[-1] != start:
        path.append(parents[path[-1]])
    return path[::-1]


def dfs(graph, start, goal):
    visited = []
    parents = {start: None}

    def explore(node):
        visited.append(node)
        if node == goal:
            return True
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                parents[neighbor] = node
                if explore(neighbor):
                    return True
        return False

    explore(start)
    return visited, build_path(parents, start, goal)


def bfs(graph, start, goal):
    queue = [start]
    visited = []
    parents = {start: None}
    while len(queue) > 0:
        current = queue.pop(0)
        visited.append(current)
        if current == goal:
            break
        for neighbor in graph.neighbors(current):
            if neighbor not in parents:
                parents[neighbor] = current
                queue.append(neighbor)
    return visited, build_path(parents, start, goal)
