"""This file implement generic Graph class and method.
The method naming convention follows princeton algorithm course (java) rather than PEP8.
"""
from collections import defaultdict


class Graph(object):
    def __init__(self, v):
        if not isinstance(v, int):
            raise TypeError("v must be int.")

        if v <= 0:
            raise ValueError("v must be positive.")

        self._v = v
        self._e = 0
        self._adj = defaultdict(set)

    def addEdge(self, v, w):
        for x in {v, w}:
            if x >= self._v:
                raise ValueError("Vertice {} is not in the Graph.".format(x))

        if w not in self._adj[v]:
            self._e += 1
        self._adj[v].add(w)
        self._adj[w].add(v)

    def adj(self, v):
        if v >= self.V:
            raise ValueError("vertice not in Graph")

        return list(self._adj[v])

    @property
    def V(self):
        return self._v

    @property
    def E(self):
        return self._e

    def __str__(self):
        for _, e in self._adj.items():
            print(str(e))

    @staticmethod
    def degree(G, v):
        """
            return the degree of vertex
        Args:
            G (Graph):
            v (int):

        Returns:
            (int)
        """
        return len(G.adj(v))

    @staticmethod
    def maxDegree(G):
        return max(Graph.degree(G, v) for v in range(G.V))

    @staticmethod
    def averageDegree(G):
        from statistics import mean
        return mean(Graph.degree(G, v) for v in range(G.V))

    @staticmethod
    def numberOfSelfLoops(G):
        count = 0
        for v in range(G.V):
            if v in G.adj(v):
                count += 1
        return count


class Digraph(Graph):
    """Directed Graph API"""
    def __init__(self, v):
        super(Digraph, self).__init__(v)

    def addEdge(self, v, w):
        for x in {v, w}:
            if x >= self._v:
                raise ValueError("Vertice {} is not in the Graph.".format(x))

        if w not in self._adj[v]:
            self._e += 1
            self._adj[v].add(w)


class DepthFirstOrder(object):
    """Impletment Depth-first order (Topological Sorting)"""
    def __init__(self, G):
        """

        Args:
            G (Digraph):
        """
        from week2.dequeue import Deque
        import numpy as np
        self._reversePost = Deque()
        self._visited = np.repeat(False, G.V)
        for i in range(G.V):
            if not self._visited[i]:
                self.dfs(G, i)

    def dfs(self, G, v):
        """

        Args:
            G (Digraph):
            v (int):

        Returns:
            None
        """
        self._visited[v] = True
        for w in G.adj(v):
            if not self._visited[w]:
                self.dfs(G, w)
        self._reversePost.add_last(v)

    def reversePost(self):
        return self._reversePost
