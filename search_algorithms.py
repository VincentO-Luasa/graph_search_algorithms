import heapq


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


def dijkstra(graph, start, goal):
    heap = [(0, start)]
    costs = {start: 0}
    parents = {start: None}
    visited = []
    while len(heap) > 0:
        cost, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.append(current)
        if current == goal:
            break
        for neighbor in graph.neighbors(current):
            new_cost = cost + graph.cost(current, neighbor)
            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parents[neighbor] = current
                heapq.heappush(heap, (new_cost, neighbor))
    return visited, build_path(parents, start, goal)


def a_star(graph, start, goal):
    # Dijkstra, ordered by cost so far + estimated cost to the goal
    scale = graph.heuristic_scale()
    heap = [(graph.heuristic(start, goal, scale), start)]
    costs = {start: 0}
    parents = {start: None}
    visited = []
    while len(heap) > 0:
        _, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.append(current)
        if current == goal:
            break
        for neighbor in graph.neighbors(current):
            new_cost = costs[current] + graph.cost(current, neighbor)
            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parents[neighbor] = current
                heapq.heappush(heap, (new_cost + graph.heuristic(neighbor, goal, scale), neighbor))
    return visited, build_path(parents, start, goal)


def greedy(graph, start, goal):
    # Always expand the node that looks closest to the goal, ignoring the cost so far
    heap = [(graph.distance(start, goal), start)]
    parents = {start: None}
    visited = []
    while len(heap) > 0:
        _, current = heapq.heappop(heap)
        visited.append(current)
        if current == goal:
            break
        for neighbor in graph.neighbors(current):
            if neighbor not in parents:
                parents[neighbor] = current
                heapq.heappush(heap, (graph.distance(neighbor, goal), neighbor))
    return visited, build_path(parents, start, goal)


def bidirectional(graph, start, goal):
    # Two BFS waves, one from each end, expanding the smaller frontier one
    # whole layer at a time. When they touch, keep the best meeting over the
    # entire layer: stopping at the first contact can miss the fewest hops.
    if start == goal:
        return [start], [start], set()
    hops = {"start": {start: 0}, "goal": {goal: 0}}
    parents = {"start": {start: None}, "goal": {goal: None}}
    frontiers = {"start": [start], "goal": [goal]}
    visited = []
    from_goal = set()
    best = None
    while best is None and frontiers["start"] and frontiers["goal"]:
        side = "start" if len(frontiers["start"]) <= len(frontiers["goal"]) else "goal"
        other = "goal" if side == "start" else "start"
        next_frontier = []
        for current in frontiers[side]:
            visited.append(current)
            if side == "goal":
                from_goal.add(current)
            for neighbor in graph.neighbors(current):
                if neighbor in hops[other]:
                    length = hops[side][current] + 1 + hops[other][neighbor]
                    if best is None or length < best[2]:
                        best = (current, neighbor, length) if side == "start" else (neighbor, current, length)
                if neighbor not in hops[side]:
                    hops[side][neighbor] = hops[side][current] + 1
                    parents[side][neighbor] = current
                    next_frontier.append(neighbor)
        frontiers[side] = next_frontier

    if best is None:
        return visited, [], from_goal
    # a is reached from the start, b from the goal, and a-b is an edge
    a, b, _ = best
    path = build_path(parents["start"], start, a) + build_path(parents["goal"], goal, b)[::-1]
    return visited, path, from_goal
