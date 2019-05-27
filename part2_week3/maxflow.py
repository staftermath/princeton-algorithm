"""
This file implements classes needed for maxflow mincut algorithms
"""


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

    def residualCapacityTo(self, vertex):
        """

        Args:
            vertex (int):

        Returns:

        """
        if vertex == self.origin:
            return self.flow
        elif vertex == self.to:
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
