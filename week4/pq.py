"""
Implements priority queue. the 'max()' and 'delMax()' methods are renamed as
'top()' and 'delTop()' to prevent confusion between MaxPQ and MinPQ
"""


class PQ(object):
    """abstract class of PQ"""
    def __init__(self, capacity):
        pass

    @property
    def N(self):
        raise NotImplementedError()

    def isEmpty(self):
        return self.N == 0

    def insert(self, x):
        raise NotImplementedError()

    def top(self):
        raise NotImplementedError()

    def delTop(self):
        raise NotImplementedError()

    def _less(self, i, j):
        raise NotImplementedError()

    def _exch(self, i, j):
        raise NotImplementedError()


class UnorderedMaxPQ(PQ):
    """unordered array implementation
    insert: 1
    delTop: N
    top: N
    """
    def __init__(self, capacity):
        super(UnorderedMaxPQ, self).__init__(capacity)
        self._pq = [None]*(capacity+1)
        self._n = 0

    @property
    def N(self):
        return self._n

    def isEmpty(self):
        return self.N == 0

    def insert(self, x):
        self._n += 1
        self._pq[self.N] = x

    def delTop(self):
        if self.isEmpty():
            raise RuntimeError("PQ is empty")

        top = 1
        for i in range(1, self.N+1):
            if self._less(top, i):
                top = i
        self._exch(top, self.N)
        top_val = self._pq[self.N]
        self._n -= 1
        self._pq[self.N+1] = None
        return top_val

    def top(self):
        if self.isEmpty():
            raise RuntimeError("PQ is empty")

        top = 1
        for i in range(1, self.N+1):
            if self._less(top, i):
                top = i
        return self._pq[top]

    def _less(self, i, j):
        """

        Args:
            i:
            j:

        Returns:
            (bool)
        """
        return self._pq[i] < self._pq[j]

    def _exch(self, i, j):
        self._pq[i], self._pq[j] = self._pq[j], self._pq[i]


class MaxPQ(PQ):
    """heap priority queue
    insert: logN
    delTop: logN
    top: 1
    """
    def __init__(self, capacity):
        super(MaxPQ, self).__init__(capacity)
        self._pq = [None]*(capacity+1)
        self._n = 0

    @property
    def N(self):
        return self._n

    def insert(self, key):
        self._n += 1
        self._pq[self.N] = key
        self._swim(self.N)

    def delTop(self):
        if self.isEmpty():
            raise RuntimeError("PQ is empty")

        top_val = self._pq[1]
        self._exch(1, self.N)
        self._n -= 1
        self._sink(1)
        self._pq[self.N+1] = None
        return top_val

    def top(self):
        return self._pq[1]

    def _less(self, i, j):
        """

        Args:
            i:
            j:

        Returns:
            (bool)
        """
        return self._pq[i] < self._pq[j]

    def _swim(self, k):
        while k > 1 and self._less(k//2, k):
            self._exch(k, k//2)
            k = k//2

    def _sink(self, k):
        """
        exchange key in parent with key in larger child
        repeat until heap order restored
        Args:
            k (int):

        Returns:

        """
        while 2*k <= self.N:
            j = 2*k
            if j < self.N and self._less(j, j+1):
                j += 1
            if not self._less(k, j):
                break
            self._exch(j, k)
            k = j

    def _exch(self, i, j):
        self._pq[i], self._pq[j] = self._pq[j], self._pq[i]


class MinPQ(MaxPQ):
    """Priority Queue to have smallest value on top"""
    def __init__(self, capacity):
        super(MinPQ, self).__init__(capacity)

    def _less(self, i, j):
        return not super(MinPQ, self)._less(i, j)
