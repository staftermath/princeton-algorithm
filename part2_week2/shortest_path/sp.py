"""
This file implement class and APIs for shortest path algorithms
"""
from collections import defaultdict
import numpy as np
import heapq


class DirectedEdge(object):

    def __init__(self, v, w, weight):
        self._v = v
        self._w = w
        self._weight = weight

    @property
    def origin(self):
        return self._v

    @property
    def to(self):
        return self._w

    @property
    def weight(self):
        return self._weight

    def __str__(self):
        return "{} -> {} ({})".format(self.origin, self.to, self.weight)

    def __hash__(self):
        return hash(str(self))


class EdgeWeightedDigraph(object):

    def __init__(self, v):
        self._v = v
        self._e = 0
        self._adj = defaultdict(set)

    def addEdge(self, e):
        """

        Args:
            e (DirectedEdge):

        Returns:

        """
        self._adj[e.origin].add(e)
        self._e += 1

    def adj(self, v):
        """

        Args:
            v (int):

        Returns:

        """
        return self._adj[v]

    def V(self):
        return self._v

    def E(self):
        return self._e

    def edges(self):
        pass


class SP(object):
    """ Shortest Path API"""
    def __init__(self, G, s):
        """

        Args:
            G (EdgeWeightedDigraph):
            s (int):
        """
        pass

    def distTo(self, v):
        raise NotImplementedError("Not implemented for type({})".format(self))

    def pathTo(self, v):
        raise NotImplementedError("Not implemented for type({})".format(self))


class DijkstraSP(SP):
    """Dijkstra Algorithm"""
    def __init__(self, G, s):
        super(DijkstraSP, self).__init__(G, s)
        self._v = G.V()
        self._edgesTo = [None]*len(self._v)
        self._distTo = np.repeat(np.inf, self._v)
        self._distTo[s] = 0.0
        self._pq = [(s, self._distTo[s])]
        self._visited = np.repeat(False, G.V())
        heapq.heapify(self._pq)
        while len(self._pq) > 0:
            v, d = heapq.heappop(self._pq)
            for e in G.adj(v):
                self._relax(e)

    @property
    def distTo(self, v):
        return self._distTo[v]

    def _relax(self, e):
        """

        Args:
            e (DirectedEdge):

        Returns:

        """
        origin = e.origin
        to = e.to
        new_dist = self._distTo[origin] + e.weight
        if new_dist < self._distTo[to]:
            self._distTo[to] = new_dist
            heapq.heappush(self._pq, (to, new_dist))
            self._edgesTo[to] = e
