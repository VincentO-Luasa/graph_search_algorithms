import math
import random
import time

import networkx as nx
import matplotlib.pyplot as plt
from graph import Graph
from search_algorithms import a_star, bfs, bidirectional, dfs, dijkstra, greedy

algorithms = {
    "Breadth-First Search": bfs,
    "Depth-First Search": dfs,
    "Dijkstra": dijkstra,
    "A*": a_star,
    "Greedy Best-First Search": greedy,
    "Bidirectional Search": bidirectional,
}

descriptions = {
    "Breadth-First Search": "Explores in rings, like a ripple spreading from the start. "
    "It is guaranteed to find the path with the *fewest hops*, but ignores how long each "
    "edge is, so that path is not always the cheapest.",
    "Depth-First Search": "Dives down one branch as far as it can before backtracking. "
    "Simple and memory-light, but its path is rarely the shortest.",
    "Dijkstra": "Always expands the unexplored node that is cheapest to reach, so it is "
    "guaranteed to find the path with the *lowest total cost*.",
    "A*": "Dijkstra with a sense of direction: it favours nodes that lie towards the goal, "
    "finding the same cheapest path while exploring less. Its straight-line guess never "
    "overestimates, which is what keeps it exact.",
    "Greedy Best-First Search": "Always jumps to the node that *looks* closest to the goal "
    "and ignores the distance already travelled. Very fast, but easily lured into detours: "
    "its path is often not the cheapest.",
    "Bidirectional Search": "Launches two breadth-first waves, one from each end (green from "
    "the start, violet from the goal), layer by layer, and stops when they meet. Like BFS it "
    "guarantees the *fewest hops*, while two small circles usually cover less ground than one big one.",
}


def generate_graph(node_number, seed):
    # Random points in a square, each linked to its 3 nearest neighbours.
    # Every edge weighs its length, so the graph has cycles and
    # shortcuts for the cost-aware algorithms to find.
    rng = random.Random(seed)
    side = math.sqrt(node_number) * 10
    min_distance = 10 * 0.62
    positions = {}
    tries = 0
    while len(positions) < node_number and tries < node_number * 60:
        tries += 1
        p = (rng.uniform(0, side), rng.uniform(0, side))
        if all(math.dist(p, q) > min_distance for q in positions.values()):
            positions[len(positions)] = p

    graph = Graph({node: [] for node in positions}, positions)
    G = nx.Graph()
    G.add_nodes_from(positions)
    for node in positions:
        closest = sorted(
            (other for other in positions if other != node),
            key=lambda other: graph.distance(node, other),
        )
        for other in closest[:3]:
            G.add_edge(node, other)

    # Join disconnected pieces with their shortest possible link
    components = [list(c) for c in nx.connected_components(G)]
    while len(components) > 1:
        a, b = min(
            ((a, b) for a in components[0] for c in components[1:] for b in c),
            key=lambda pair: graph.distance(*pair),
        )
        G.add_edge(a, b)
        components = [list(c) for c in nx.connected_components(G)]

    for a, b in G.edges:
        weight = max(1, round(graph.distance(a, b)))
        graph.graph[a].append(b)
        graph.graph[b].append(a)
        graph.weights[(a, b)] = weight
        graph.weights[(b, a)] = weight

    # Shuffle neighbour order so DFS wanders instead of sweeping
    for node in graph.graph:
        rng.shuffle(graph.graph[node])
    return graph


def default_endpoints(graph):
    # Leftmost and rightmost nodes, so the search has to cross the graph
    start = min(graph.positions, key=lambda node: graph.positions[node][0])
    goal = max(graph.positions, key=lambda node: graph.positions[node][0])
    return start, goal


def graph_search(algorithm, graph, start, goal):
    result = algorithms[algorithm](graph, start, goal)
    # Only bidirectional search explores from the goal too
    if len(result) == 2:
        return result + (set(),)
    return result


def path_cost(graph, path):
    return sum(graph.cost(a, b) for a, b in zip(path, path[1:]))


def plot_graph(graph, color_map, plot_holder, path=None):
    G = nx.Graph(graph.graph)
    pos = graph.positions
    node_size = max(120, 500 * 20 / len(G))
    fig, ax = plt.subplots(figsize=(8, 8))
    nx.draw(
        G,
        pos,
        ax=ax,
        node_size=node_size,
        node_color=[color_map[node] for node in G],
        edge_color="lightgray",
        with_labels=True,
        font_size=8,
    )
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges, edge_color="orange", width=4)
        if graph.weighted:
            edge_labels = {(a, b): graph.cost(a, b) for a, b in path_edges}
            nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels, font_color="darkorange")
    plot_holder.pyplot(fig)
    plt.close(fig)


def endpoint_colors(graph, start, goal, color="lightgray"):
    color_map = {node: color for node in graph.graph}
    color_map[start] = "royalblue"
    color_map[goal] = "tomato"
    return color_map


def run_visualization(algorithm, graph, plot_holder, start, goal, step_duration=0.5):
    visited, path, from_goal = graph_search(algorithm, graph, start, goal)
    n = len(visited)
    for i in range(n):
        color_map = endpoint_colors(graph, start, goal)
        for node in visited[:i]:
            if node not in (start, goal):
                color_map[node] = "plum" if node in from_goal else "lightgreen"
        color_map[visited[i]] = "cyan"
        plot_graph(graph, color_map, plot_holder)
        time.sleep(step_duration)
    color_map = endpoint_colors(graph, start, goal)
    for node in visited:
        if node not in (start, goal):
            if node in path:
                color_map[node] = "gold"
            else:
                color_map[node] = "plum" if node in from_goal else "lightgreen"
    plot_graph(graph, color_map, plot_holder, path)
    return visited, path
