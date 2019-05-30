"""
This file implements classes needed for maxflow mincut algorithms
"""
from collections import defaultdict
import numpy as np


class FlowEdge(object):
    """
    Edge class contain flow and needed methods
    """
    def __init__(self, v, w, capacity):
        self._v = v
        self._w = w
        self._capacity = capacity
        self._flow = 0

    @property
    def origin(self):
        return self._v

    @property
    def to(self):
        return self._w

    def other(self, v):
        """

        Args:
            v (int):

        Returns:
            int
        """
        if self._v == v:
            return self._w
        elif self._w == v:
            return self._v
        else:
            raise RuntimeError("Illegal Endpoint")

    @property
    def capacity(self):
        return self._capacity

    @property
    def flow(self):
        return self._flow

    def residualCapacityTo(self, v):
        """

        Args:
            v (int):

        Returns:

        """
        if v == self.origin:
            return self.flow
        elif v == self.to:
            return self.capacity - self.flow
        else:
            raise RuntimeError("Illegal Endpoint")

    def addResidualFlowTo(self, v, delta):
        if v == self.origin:
            if self._flow < delta:
                raise RuntimeError("Insufficient flow")
            else:
                self._flow -= delta
        elif v == self.to:
            self._flow += delta
        else:
            raise RuntimeError("Illegal Endpoint")

    def __str__(self):
        return "{} --({}/{})--> {}".format(self.origin, self.flow, self.capacity, self.to)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, FlowEdge):
            return (
                    self.origin == other.origin
                    and self.to == other.to
                    and self.capacity == other.capacity
                    and self.flow == other.flow
            )

        raise NotImplementedError("Cannot compare {} with {}.".format(type(self), type(FlowEdge)))


class FlowNetwork(object):
    """"""
    def __init__(self, V):
        self._v = V
        self._adj = defaultdict(set)
        self._e = 0
        self._edges = []

    def addEdge(self, e):
        """

        Args:
            e (FlowEdge):

        Returns:
            None
        """
        if e not in self._adj[e.origin]:
            self._e += 1
            self._adj[e.origin].add(e)
            self._adj[e.to].add(e)
            self._edges.append(e)

    def adj(self, v):
        return self._adj[v]

    def edges(self):
        return self._edges

    def V(self):
        return self._v

    def E(self):
        return self._e


class FordFulkerson(object):
    """Implement FordFulkerson with BFS for augmenting path
    TODO:
    1. implement min_cut
    2. implement other method to find augumenting path
        - fattest path
    """
    def __init__(self, G, s, t):
        """

        Args:
            G (FlowNetwork): a flow network
            s (int): source
            t (int): sink
        """
        self._value = 0
        self._marked = [False]*G.V()
        self._edgesTo = [None]*G.V()
        while self.hasAugmentingPath(G, s, t):
            bottle = np.inf
            v = t
            while v != s:
                bottle = min(bottle, self._edgesTo[v].residualCapacityTo(v))
                v = self._edgesTo[v].other(v)
            v = t
            while v != s:
                self._edgesTo[v].addResidualFlowTo(v, bottle)
                v = self._edgesTo[v].other(v)

            self._value += bottle

    def hasAugmentingPath(self, G, s, t):
        """

        Args:
            G (FlowNetwork):
            s (int):
            t (int):

        Returns:
            (bool)
        """
        from week2.dequeue import Deque
        self._edgesTo = [None]*G.V()
        self._marked = [False]*G.V()
        queue = Deque()
        self._marked[s] = True
        queue.add_first(s)
        while not queue.is_empty():
            v = queue.remove_first()
            for e in G.adj(v):
                w = e.other(v)
                if e.residualCapacityTo(w) > 0 and not self._marked[w]:
                    self._marked[w] = True
                    self._edgesTo[w] = e
                    queue.add_last(w)

        return self._marked[t]

    def value(self):
        return self._value

    def inCut(self, v):
        return self._marked[v]
