"""
This script implement union-find to simulate and calculate percolation threshold.
"""
import random
import sys
from itertools import product


class UnionFind(object):
    def __init__(self, n):
        self._index = list(range(n))
    
    @property
    def index(self):
        return self._index

    def union(self, x, y):
        if self.index[x] != self.index[y]:
            x = self.root(x)
            y = self.root(y)
            self.index[x] = y

    def root(self, x):
        while x != self.index[x]:
            self.index[x] = self.index[self.index[x]]
            x = self.index[x]
        return x
    
    def is_connected(self, x, y):
        return self.root(x) == self.root(y)


class Percolation(object):
    def __init__(self, x, y):
        """Initiate board with height x and width y.
        It comes with dummy top node (idx = 0) and dummy bottom node (idx=x*y+1)
        index is assigned as:
            (i, j) -> y*i+j+1
        Args:
            x (int): height
            y (int): width
        """
        self.top = 0
        self.bottom = x*y+1
        self.height = x
        self.width = y
        # Union Find class
        self._palette = UnionFind(self.bottom+1)
        # is the block filled
        self._filled = [False]*(self.bottom+1)
        self._filled[self.top] = self._filled[self.bottom] = True
        # connect first row with top dummy node
        for i in range(1, y+1):
            self.palett.union(i, self.top)
        
        # connect bottom row with bottom dummy node
        for i in range(x*y+1, self.bottom):
            self.palett.union(i, self.bottom)

    @property
    def palett(self):
        return self._palette

    def get_index(self, x, y):
        return x*self.width+y+1

    def is_filled(self, idx):
        """Check if row x column y is filled
        
        Args:
            idx (int): index number
        
        Returns:
            bool: if the block is filled
        """
        return self._filled[idx]

    def _connect(self, idx1, idx2):
        if idx2 <= self.top:
            # connect to top node
            self.palett.union(idx1, 0)
        elif idx2 >= self.bottom:
            # connect to bottom node
            self.palett.union(idx1, self.bottom)
        elif self.is_filled(idx2):
            # only connect when target is filled
            self.palett.union(idx1, idx2)

    def fill(self, x, y):
        idx = self.get_index(x, y)
        self._filled[idx] = True
        for target in (idx-self.width, idx+self.width):
            self._connect(idx, target)
        
        if (idx-1)%self.width != 0:
            # not on the left boundary
            self._connect(idx, idx-1)
        
        if idx%self.width != 0:
            # not on the right boundary
            self._connect(idx, idx+1)

    def is_percolated(self):
        return self.palett.is_connected(self.top, self.bottom)
        

class MonteCarlo(object):
    def __init__(self, height, width, seed=123):
        self._height = height
        self._width = width
        self._seed = seed
        random.seed(seed)
        self.height_idx = range(height)
        self.width_idx = range(width)
        self._list = list(product(self.height_idx, self.width_idx))
    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def sample(self):
        random.shuffle(self._list)
        return self._list
    
if __name__ == "__main__":
    height = int(sys.argv[1])
    width = int(sys.argv[2])
    simulation_rounds = int(sys.argv[3])

    monte_carlo = MonteCarlo(height=height, width=width)
    area = height*width
    total = 0.0
    for i in range(simulation_rounds):
        percolation = Percolation(height, width)
        for j, point in enumerate(monte_carlo.sample()):
            percolation.fill(*point)
            if percolation.is_percolated():
                total += j/area
                break
    print("Threshhold is {}".format(total/simulation_rounds))
