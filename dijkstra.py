from graph import Edge, Graph
import numpy as np
from typing import Any, Dict, List, Iterable, Tuple
import heapq


class DijkstraShortestPathFinder:
    def shortest_paths_tree(self, graph: Graph, start: Any, end: Any) -> Dict[Any, Edge]:
        parent_edge: Dict[Any, Edge] = {}
        dist: Dict[Any, float] = {}
        INF = float('inf')
        heap = []
        counter = 0

        dist[start] = 0.0
        heapq.heappush(heap, (0.0, counter, start))
        counter += 1

        while heap:
            d, _, u = heapq.heappop(heap)
            if d != dist.get(u, INF):
                continue
            if u == end:
                break
            for edge in graph.outgoing_edges(u):
                v = edge.dest
                w = edge.weight
                newd = d + w
                if newd < dist.get(v, INF):
                    dist[v] = newd
                    parent_edge[v] = edge
                    heapq.heappush(heap, (newd, counter, v))
                    counter += 1
        return parent_edge

    def extract_shortest_path(self, spt: Dict[Any, Edge], start: Any, end: Any) -> List[Edge]:
        if end not in spt and end != start:
            return []
        path_rev: List[Edge] = []
        cur = end
        while cur != start:
            if cur not in spt:
                return []
            edge = spt[cur]
            path_rev.append(edge)
            cur = edge.src
        path_rev.reverse()
        return path_rev

    def find_shortest_path(self, graph: Graph, start: Any, end: Any) -> List[Edge]:
        spt = self.shortest_paths_tree(graph, start, end)
        return self.extract_shortest_path(spt, start, end)

# Energy grid graph for seams
class EnergyGridGraph(Graph):
    def __init__(self, energy: np.ndarray, vertical: bool = True):
        assert energy.ndim == 2
        self.energy = energy.astype(float)
        self.H, self.W = energy.shape
        self.vertical = vertical
        self.SOURCE = ("<SOURCE>", "S")
        self.SINK = ("<SINK>", "T")

    def outgoing_edges(self, vertex: Any) -> Iterable[Edge]:
        if vertex == self.SOURCE:
            if self.vertical:
                for x in range(self.W):
                    yield Edge(self.SOURCE, (x, 0), float(self.energy[0, x]))
            else:
                for y in range(self.H):
                    yield Edge(self.SOURCE, (0, y), float(self.energy[y, 0]))
            return
        if vertex == self.SINK:
            return
        x, y = vertex
        if self.vertical:
            if y == self.H - 1:
                yield Edge((x, y), self.SINK, 0.0)
                return
            ny = y + 1
            for nx in range(x - 1, x + 2):
                if 0 <= nx < self.W:
                    yield Edge((x, y), (nx, ny), float(self.energy[ny, nx]))
        else:
            if x == self.W - 1:
                yield Edge((x, y), self.SINK, 0.0)
                return
            nx = x + 1
            for ny in range(y - 1, y + 2):
                if 0 <= ny < self.H:
                    yield Edge((x, y), (nx, ny), float(self.energy[ny, nx]))


# Dijkstra seam finder
class DijkstraMethod:
    def __init__(self):
        self.path_finder = DijkstraShortestPathFinder()

    def find_vertical_seam(self, energy: np.ndarray) -> List[int]:
        graph = EnergyGridGraph(energy, vertical=True)
        s, t = graph.SOURCE, graph.SINK
        edges = self.path_finder.find_shortest_path(graph, s, t)
        verts: List[Tuple[int, int]] = []
        for e in edges:
            if e.dest == graph.SINK:
                break
            if e.dest != graph.SOURCE:
                verts.append(e.dest)
        seam = [-1] * energy.shape[0]
        for (x, y) in verts:
            seam[y] = x
        return seam

    def find_horizontal_seam(self, energy: np.ndarray) -> List[int]:
        transposed = energy.T.copy()
        seam_in_transposed = self.find_vertical_seam(transposed)
        return seam_in_transposed
