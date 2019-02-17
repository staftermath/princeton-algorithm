import unittest
from week2.dequeue import Deque


class TestDeque(unittest.TestCase):
    def test_init(self):
        deque = Deque()
        self.assertEqual(deque.size, 0)
        self.assertTrue(deque.is_empty())
        self.assertEqual(deque._begin, 1)
        self.assertEqual(deque._end, 1)
        self.assertEqual(len(deque._array), 4)

        deque = Deque([100, 200, 300, 400])
        self.assertEqual(deque.size, 4)
        self.assertEqual(deque.remove_first(), 100)
        self.assertEqual(deque.remove_last(), 400)

    def test_add_first(self):
        deque = Deque()
        deque.add_first(100)
        
        self.assertEqual(deque._array[deque._begin], 100)
        self.assertEqual(deque.size, 1)
        self.assertEqual(len(deque._array), 4)

        first_batch = [200, 300, 400]
        for val in first_batch:
            deque.add_first(val)
        
        self.assertEqual(deque._array[deque._begin], 400)
        self.assertEqual(deque._array[deque._end-1], 100)
        self.assertEqual(len(deque._array), 8)

    def test_add_last(self):
        deque = Deque()
        deque.add_last(100)
        self.assertEqual(deque._begin, 1)
        self.assertEqual(deque._end, 2)
        self.assertEqual(deque._array[deque._begin], 100)
        self.assertEqual(deque.size, 1)
        self.assertEqual(len(deque._array), 4)

        first_batch = [200, 300, 400]
        for val in first_batch:
            deque.add_last(val)
        
        self.assertEqual(len(deque._array), 8)
        self.assertEqual(deque._array[deque._end-1], 400)
        self.assertEqual(deque._array[deque._begin], 100)

    def test_remove_first(self):
        deque = Deque()
        deque.add_first(100)
        deque.add_first(200)
        result = deque.remove_first()
        self.assertEqual(result, 200)
        result = deque.remove_first()
        self.assertEqual(result, 100)
        self.assertTrue(deque.is_empty())

    def test_remove_last(self):
        deque = Deque()
        deque.add_first(100)
        deque.add_first(200)
        deque.add_last(300)
        result = deque.remove_last()
        self.assertEqual(result, 300)
        self.assertEqual(deque.size, 2)
        result = deque.remove_last()
        self.assertEqual(result, 100)
        self.assertEqual(deque.size, 1)
        result = deque.remove_last()
        self.assertEqual(result, 200)
        self.assertTrue(deque.is_empty())

    def test_iterator(self):
        deque = Deque([100, 200, 300, 400])

        result = []
        for x in deque:
            result.append(x)

        self.assertListEqual(result, [100, 200, 300, 400])