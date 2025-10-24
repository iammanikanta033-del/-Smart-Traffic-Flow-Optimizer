# graph.py
"""
Smart Traffic Flow Optimizer - core module
Implements Graph, Edge classes and Dijkstra + A* algorithms
Pure Python, OOP, and standard library only.
Visualization is optional and handled in main.py using networkx/matplotlib.
"""

import heapq
import math
from typing import Dict, List, Tuple, Optional


class Edge:
    def __init__(self, to_node: str, distance: float, traffic_factor: float = 1.0):
        self.to_node = to_node
        self.distance = float(distance)
        self.traffic_factor = float(traffic_factor)

    def effective_weight(self) -> float:
        """Effective weight considering traffic congestion multiplier."""
        return self.distance * self.traffic_factor

    def to_tuple(self) -> Tuple[str, float, float]:
        return (self.to_node, self.distance, self.traffic_factor)


class Graph:
    def __init__(self):
        # adjacency list: node -> list of Edge objects
        self.adj: Dict[str, List[Edge]] = {}
        # optional coordinates for heuristic in A* (node -> (x,y))
        self.coords: Dict[str, Tuple[float, float]] = {}

    def add_node(self, node: str, coord: Optional[Tuple[float, float]] = None):
        if node not in self.adj:
            self.adj[node] = []
        if coord is not None:
            self.coords[node] = (float(coord[0]), float(coord[1]))

    def add_edge(self, u: str, v: str, distance: float, traffic_factor: float = 1.0, bidirectional: bool = True):
        """Add edge u->v with distance and optional traffic_factor. By default adds both directions."""
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append(Edge(v, distance, traffic_factor))
        if bidirectional:
            self.adj[v].append(Edge(u, distance, traffic_factor))

    def neighbors(self, node: str) -> List[Edge]:
        return self.adj.get(node, [])

    def _reconstruct_path(self, came_from: Dict[str, str], start: str, goal: str) -> List[str]:
        path = []
        cur = goal
        while cur != start:
            path.append(cur)
            cur = came_from.get(cur)
            if cur is None:
                return []  # unreachable
        path.append(start)
        path.reverse()
        return path

    def dijkstra(self, start: str) -> Tuple[Dict[str, float], Dict[str, str]]:
        """Returns (distances, previous_map). distances[node] = shortest effective distance from start."""
        if start not in self.adj:
            raise ValueError(f"Start node '{start}' not in graph.")
        dist: Dict[str, float] = {node: float('inf') for node in self.adj}
        dist[start] = 0.0
        prev: Dict[str, str] = {}
        pq: List[Tuple[float, str]] = [(0.0, start)]

        while pq:
            curr_d, u = heapq.heappop(pq)
            if curr_d > dist[u]:
                continue
            for edge in self.neighbors(u):
                v = edge.to_node
                w = edge.effective_weight()
                nd = curr_d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
        return dist, prev

    def shortest_path_dijkstra(self, start: str, end: str) -> Tuple[List[str], float]:
        dist, prev = self.dijkstra(start)
        if end not in dist or dist[end] == float('inf'):
            return [], float('inf')
        path = self._reconstruct_path(prev, start, end)
        return path, dist[end]

    def _heuristic(self, a: str, b: str) -> float:
        """Euclidean distance between coordinates if available; else 0."""
        if a in self.coords and b in self.coords:
            (x1, y1) = self.coords[a]
            (x2, y2) = self.coords[b]
            return math.hypot(x2 - x1, y2 - y1)
        return 0.0

    def a_star(self, start: str, goal: str) -> Tuple[List[str], float]:
        """A* search using effective_weight for edge cost and Euclidean heuristic when coords exist.
        If coords are missing, heuristic is 0 (A* reduces to Dijkstra if heuristic==0)."""
        if start not in self.adj or goal not in self.adj:
            raise ValueError("Start or goal not in graph.")

        open_set = []
        heapq.heappush(open_set, (0.0, start))
        came_from: Dict[str, str] = {}
        g_score = {node: float('inf') for node in self.adj}
        g_score[start] = 0.0
        f_score = {node: float('inf') for node in self.adj}
        f_score[start] = self._heuristic(start, goal)

        while open_set:
            curr_f, current = heapq.heappop(open_set)
            if current == goal:
                path = self._reconstruct_path(came_from, start, goal)
                return path, g_score[goal]

            for edge in self.neighbors(current):
                neighbor = edge.to_node
                tentative_g = g_score[current] + edge.effective_weight()
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return [], float('inf')  # no path

    # Utility functions
    def nodes(self) -> List[str]:
        return list(self.adj.keys())

    def edges(self) -> List[Tuple[str, str, float, float]]:
        """Return list of (u, v, distance, traffic_factor) for each adjacency entry (u->v)."""
        result = []
        for u, edges in self.adj.items():
            for e in edges:
                result.append((u, e.to_node, e.distance, e.traffic_factor))
        return result

    def load_from_edge_list(self, edge_list: List[Tuple[str, str, float, float]]):
        """Helper to populate graph from a list of (u,v,distance,traffic_factor)."""
        for u, v, d, t in edge_list:
            self.add_edge(u, v, d, t, bidirectional=True)
