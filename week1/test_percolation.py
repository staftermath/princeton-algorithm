import unittest
from week1.percolation import UnionFind, Percolation, MonteCarlo

class TestUnionFind(unittest.TestCase):
    def test_init(self):
        union_find = UnionFind(5)
        self.assertListEqual(union_find.index, 
                             [0, 1, 2, 3, 4])

    def test_union(self):
        union_find = UnionFind(6)
        union_find.union(3, 4)
        self.assertEqual(union_find.index[3], 4)
    
    def test_root(self):
        union_find = UnionFind(6)
        self.assertEqual(union_find.root(3), 3)
        union_find.union(4, 5)
        self.assertEqual(union_find.root(4), 5)
        union_find.union(3, 4)
        self.assertEqual(union_find.root(3), 5)

    def test_is_connected(self):
        union_find = UnionFind(6)
        self.assertFalse(union_find.is_connected(3, 4))
        union_find.union(3, 4)
        self.assertTrue(union_find.is_connected(3, 4))
        union_find.union(1, 2)
        self.assertFalse(union_find.is_connected(1, 3))
        union_find.union(2, 3)
        self.assertTrue(union_find.is_connected(1, 4))

        
class TestPercolation(unittest.TestCase):
    def test_init(self):
        height = 3
        width = 4
        percolation = Percolation(height, width)
        self.assertEqual(len(percolation.palett.index), height*width+2)
        self.assertEqual(percolation.top, 0)
        self.assertEqual(percolation.bottom, height*width+1)
        self.assertFalse(percolation._filled[3])
        self.assertTrue(percolation._filled[0])
        self.assertTrue(percolation._filled[height*width+1])
        self.assertEqual(percolation.get_index(2, 3), 12)
    
    def test_fill_and_connect(self):
        height = 3
        width = 4
        percolation = Percolation(height, width)
        point = (1, 2)
        idx = percolation.get_index(*point)
        self.assertFalse(percolation.is_filled(idx))
        percolation.fill(*point)
        self.assertTrue(percolation.is_filled(idx))
        points = [(1, 3),(2, 2),(0, 1)]
        indices = [percolation.get_index(*p) for p in points]
        for p in points:
            percolation.fill(*p)
        self.assertTrue(percolation.palett.is_connected(indices[1], idx))
        self.assertFalse(percolation.is_percolated())
        last_point = (0, 2)
        percolation.fill(*last_point)
        self.assertTrue(percolation.is_percolated())


class TestMonteCarlo(unittest.TestCase):
    def test_sample(self):
        monte_carlo = MonteCarlo(height=2, width=2, seed=111)
        self.assertListEqual(monte_carlo._list, [(0,0), (0,1), (1,0), (1,1)])
        result = monte_carlo.sample()
        expected_result = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.assertListEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()