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


class Distance(object):
    """Implement helper class for Dijkstra Algorithm"""
    def __init__(self, s, d):
        self._s = s
        self._d = d

    @property
    def to(self):
        return self._s

    @property
    def distance(self):
        return self._d

    @distance.setter
    def distance(self, d):
        self._d = d

    def __lt__(self, other):
        if isinstance(other, Distance):
            return self.distance < other.distance

        raise NotImplementedError("Cannot compare {} with {}".format(type(self), type(other)))


class DijkstraSP(SP):
    """Dijkstra Algorithm Using MinPQ (binary heap implementation)
    time: O(Elog(V))
    space: O(V)
    """
    def __init__(self, G, s):
        from week4.pq import MinPQ
        super(DijkstraSP, self).__init__(G, s)
        self._from = s
        self._v = G.V()
        self._edgesTo = [None]*self._v
        self._distTo = np.repeat(np.inf, self._v)
        self._distTo[s] = 0
        self._pq = MinPQ(G.V())
        self._pq.insert(Distance(s, self._distTo[s]))
        self._visited = np.repeat(False, G.V())
        while not self._pq.isEmpty():
            closest = self._pq.delTop()
            for e in G.adj(closest.to):
                self._relax(e)

    @property
    def origin(self):
        return self._from

    def distTo(self, v):
        return self._distTo[v]

    def pathTo(self, v):
        path = [v]
        while v != self.origin:
            e = self._edgesTo[v]
            path.append(e.origin)
            v = e.origin
        return path[::-1]

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
            self._pq.insert(Distance(to, new_dist))
            self._edgesTo[to] = e
