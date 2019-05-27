"""
Write a program to solve the 8-puzzle problem (and its natural generalizations) using the A* search algorithm.

The problem. The 8-puzzle problem is a puzzle invented and popularized by Noyes Palmer Chapman in the 1870s.
It is played on a 3-by-3 grid with 8 square blocks labeled 1 through 8 and a blank square.
Your goal is to rearrange the blocks so that they are in order, using as few moves as possible.
You are permitted to slide blocks horizontally or vertically into the blank square.
"""
from collections import defaultdict
import numpy as np
from math import factorial


class Position(object):
    """Position with distance to final location"""
    def __init__(self, pos, distance):
        """

        Args:
            pos (numpy.ndarray):
            distance:
        """
        self._pos = pos.copy()
        self._distance = distance

    @property
    def pos(self):
        return self._pos

    @property
    def distance(self):
        return self._distance

    def __lt__(self, other):
        """

        Args:
            other (Position):

        Returns:

        """
        return self._distance < other._distance


class DistanceHash(object):
    """Precalculate all distance"""
    def __init__(self, height, width):
        from week4.pq import MinPQ
        if height <= 1 or width <= 1:
            raise ValueError("Both height and width must be no less than 2")
        self._h = height
        self._w = width
        self._total = height*width
        self._distance = np.zeros([self._total]*self._total)
        self._pq = MinPQ(capacity=factorial(self._total))
        self._populate_distance()
        self._visited = np.zeros([self._total]*self._total)

    def get_distance(self, pos):
        """

        Args:
            pos (numpy.ndarray):

        Returns:
            int
        """
        return self._distance.item(*(pos-1))

    def visited(self, pos):
        """

        Args:
            pos (numpy.ndarray):

        Returns:
            bool
        """
        return self._visited.item(*(pos-1))

    @property
    def height(self):
        return self._h

    @property
    def width(self):
        return self._w

    def _populate_distance(self):
        raise NotImplementedError()

    def solve(self, pos):
        self._pq.insert(Position(pos, self.get_distance(pos)))
        while not self._pq.isEmpty():
            top = self._pq.delTop()
            if top.distance == 0:
                return True

            self._visited[set(top.pos-1)] = 1
            idx_blank = np.where(top.pos == self._total)[0][0]
            if idx_blank >= self.width:
                # from up:
                top.pos[idx_blank], top.pos[idx_blank-self.width] = top.pos[idx_blank-self.width], top.pos[idx_blank]
                if self._visited.item(*(top.pos-1)) == 0:
                    self._pq.insert(Position(top.pos, self.get_distance(top.pos)))
                top.pos[idx_blank-self.width], top.pos[idx_blank] = top.pos[idx_blank], top.pos[idx_blank-self.width]

            if self._total - idx_blank > self.width:
                # from bottom
                top.pos[idx_blank], top.pos[idx_blank+self.width] = top.pos[idx_blank+self.width], top.pos[idx_blank]
                if self._visited.item(*(top.pos-1)) == 0:
                    self._pq.insert(Position(top.pos, self.get_distance(top.pos)))
                top.pos[idx_blank+self.width], top.pos[idx_blank] = top.pos[idx_blank], top.pos[idx_blank+self.width]

            if idx_blank % self.width != 0:
                # from left
                top.pos[idx_blank], top.pos[idx_blank-1] = top.pos[idx_blank-1], top.pos[idx_blank]
                if self._visited.item(*(top.pos-1)) == 0:
                    self._pq.insert(Position(top.pos, self.get_distance(top.pos)))
                top.pos[idx_blank-1], top.pos[idx_blank] = top.pos[idx_blank], top.pos[idx_blank-1]

            if (idx_blank+1) % self.width != 0:
                # from right
                top.pos[idx_blank], top.pos[idx_blank+1] = top.pos[idx_blank+1], top.pos[idx_blank]
                if self._visited.item(*(top.pos-1)) == 0:
                    self._pq.insert(Position(top.pos, self.get_distance(top.pos)))
                top.pos[idx_blank+1], top.pos[idx_blank] = top.pos[idx_blank], top.pos[idx_blank+1]

        return False


class HammingDistanceHash(DistanceHash):
    """Implement Hamming Distance"""
    def __init__(self, height, width):
        super(HammingDistanceHash, self).__init__(height, width)

    def _populate_distance(self):
        from itertools import permutations
        correct_position = np.array(range(self._total))
        for pos in permutations(correct_position):
            self._distance.itemset(tuple(pos), self._total - np.sum(np.array(pos) == correct_position))
