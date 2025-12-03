# Graph edge class
class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

# Graph interface
class Graph:
    def outgoing_edges(self, vertex):
        raise NotImplementedError()
