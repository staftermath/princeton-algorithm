"""
This file implement princeton algorithm part 2 week2 course code: Minimum spanning tree
"""
from collections import defaultdict
from week1.percolation import UnionFind


def is_edge(f):
    def new_f(*args, **kwargs):
        if not isinstance(args[1], Edge):
            raise NotImplementedError("Cannot compare to class object other than Edge")
        return f(*args, **kwargs)
    return new_f


class Edge(object):

    def __init__(self, v, w, weight):
        """

        Args:
            v (int):
            w (int):
            weight (float):
        """
        self._v = v
        self._w = w
        self._weight = weight

    @property
    def v(self):
        return self._v

    @property
    def w(self):
        return self._w

    @property
    def weight(self):
        return self._weight

    def either(self):
        return self.v

    def other(self, v):
        if self.v == v:
            return self.w
        elif self.w == v:
            return self.v
        else:
            raise ValueError("{} is not one of the endpoint".format(v))

    @is_edge
    def __eq__(self, other):
        return self.weight == other.weight

    @is_edge
    def __gt__(self, other):
        return self.weight > other.weight

    @is_edge
    def __lt__(self, other):
        return self.weight < other.weight

    @is_edge
    def __ge__(self, other):
        return self.weight >= other.weight

    @is_edge
    def __le__(self, other):
        return self.weight <= other.weight

    def __str__(self):
        return "{} -> {} ({})".format(self.v, self.w, self.weight)

    def __hash__(self):
        return hash(str(self))


class EdgeWeightedGraph(object):

    def __init__(self, v):
        """
        Args:
            v (int):
        """
        self._v = v
        self._e = 0
        self._adj = defaultdict(set)
        self._edges = []

    def addEdge(self, e):
        """

        Args:
            e (Edge):

        Returns:
            None
        """
        v = e.either()
        w = e.other(v)
        self._adj[v].add(e)
        self._adj[w].add(e)
        self._e += 1
        self._edges.append(e)

    def adj(self, v):
        """

        Args:
            v (int):

        Returns:
            (list)
        """
        return self._adj[v]

    def edges(self):
        return self._edges

    @property
    def V(self):
        return self._v

    @property
    def E(self):
        return self._e


class MST(object):
    """
    implementation of Minimum Spanning Tree
    """
    def __init__(self, G):
        """

        Args:
            G (EdgeWeightedGraph):
        """
        import heapq
        self._mst = []
        self.uf = UnionFind(G.V)
        edges = G.edges()
        heapq.heapify(edges)
        for e in edges:
            v = e.either()
            w = e.other(v)
            if not self.uf.is_connected(v, w):
                self.uf.union(v, w)
                self._mst.append(e)

    @property
    def edges(self):
        return self._mst

    def weight(self):
        return sum([e.weight for e in self.edges])


class PrimMST(object):
    """
    Implementation of MST with Prim algoritm
    """
    def __init__(self, G):
        """

        Args:
            G (EdgeWeightedGraph):
        """
        import heapq
        self._mst = []
        edges = []
        heapq.heapify(edges)
        visited = set()
        v = 0
        while len(self._mst) < G.V-1:
            for e in G.adj(v):
                v1 = e.either()
                v2 = e.other(v1)
                if v1 not in visited and v2 not in visited:
                    heapq.heappush(edges, e)
            visited.add(v)
            while len(edges) > 0:
                e = heapq.heappop(edges)
                v1 = e.either()
                v2 = e.other(v1)
                if v1 not in visited or v2 not in visited:
                    self._mst.append(e)
                    v = v1 if v1 not in visited else v2
                    break

    @property
    def edges(self):
        return self._mst

    def weight(self):
        return sum([e.weight for e in self.edges])
