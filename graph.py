from typing import Any, Iterable


# Graph edge class
class Edge:
    def __init__(self, src: Any, dest: Any, weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight

#Graph interface
class Graph:
    def outgoing_edges(self, vertex: Any) -> Iterable[Edge]:
        raise NotImplementedError()