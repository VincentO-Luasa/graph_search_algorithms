import math


class Graph:
    def __init__(self, graph_dict=None, positions=None, weights=None):
        if graph_dict is None:
            graph_dict = {}
        if positions is None:
            positions = {}
        if weights is None:
            weights = {}
        self.graph = graph_dict
        self.positions = positions
        self.weights = weights

    def neighbors(self, node):
        return self.graph[node]

    def cost(self, a, b):
        return self.weights.get((a, b), 1)

    def distance(self, a, b):
        (xa, ya), (xb, yb) = self.positions[a], self.positions[b]
        return math.hypot(xa - xb, ya - yb)
