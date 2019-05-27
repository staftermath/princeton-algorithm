"""
Implement heapsort
"""


class HeapSort(object):
    """Heapsort"""
    def __init__(self, h):
        """

        Args:
            h (week4.pq.MaxPQ):
        """
        self._values = [None]*h.N
        for i in range(len(self)):
            self._values[i] = h.delTop()

    def topk(self, k):
        return self._values[:k]

    def top(self):
        return self._values[0]

    def __iter__(self):
        return iter(self._values)

    @property
    def values(self):
        return self._values

    def __len__(self):
        return len(self.values)
