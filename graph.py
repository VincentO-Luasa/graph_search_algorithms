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

    def neighbors(self, node):
        return self.graph[node]

    def cost(self, a, b):
        if not self.weighted:
            return 1
        return self.weights[(a, b)]

    def distance(self, a, b):
        (xa, ya), (xb, yb) = self.positions[a], self.positions[b]
        return math.hypot(xa - xb, ya - yb)

    def heuristic_scale(self):
        # Scale for the straight-line distance so it never overestimates the real
        # cost (which keeps A* exact): the smallest cost per unit of length over
        # all edges. When every edge costs 1, that is 1 / the longest edge.
        # Zero-length edges are skipped: they cannot make the estimate too high.
        ratios = [
            self.cost(a, b) / self.distance(a, b)
            for a in self.graph
            for b in self.neighbors(a)
            if self.distance(a, b) > 0
        ]
        return min(ratios, default=0)

    def heuristic(self, node, goal, scale=None):
        if scale is None:
            scale = self.heuristic_scale()
        return self.distance(node, goal) * scale
