import math


class Graph:
    def __init__(self, graph_dict=None, positions=None, weights=None, weighted=True):
        if graph_dict is None:
            graph_dict = {}
        if positions is None:
            positions = {}
        if weights is None:
            weights = {}
        self.graph = graph_dict
        self.positions = positions
        self.weights = weights
        # Weighted: an edge costs its weight. Unweighted: every edge costs 1.
        self.weighted = weighted
        self.heuristic_scales = {}

    def neighbors(self, node):
        return self.graph[node]

    def cost(self, a, b):
        if not self.weighted:
            return 1
        return self.weights[(a, b)]

    def distance(self, a, b):
        (xa, ya), (xb, yb) = self.positions[a], self.positions[b]
        return math.hypot(xa - xb, ya - yb)

    def heuristic(self, node, goal):
        # Straight-line distance, scaled so it never overestimates the real cost
        # (which keeps A* exact): by the smallest weight per unit of length, or,
        # when every edge costs 1, by the longest edge a single hop can cover.
        if self.weighted not in self.heuristic_scales:
            if self.weighted:
                scale = min(w / self.distance(a, b) for (a, b), w in self.weights.items())
            else:
                scale = 1 / max(self.distance(a, b) for a, b in self.weights)
            self.heuristic_scales[self.weighted] = scale
        return self.distance(node, goal) * self.heuristic_scales[self.weighted]
