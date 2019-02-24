import unittest
from week3.collinear import *

class TestPoint(unittest.TestCase):
    def test_init(self):
        point = Point(3, 5)
        self.assertEqual(point.x, 3)
        self.assertEqual(point.y, 5)
    
    def test_slope_to(self):
        point = Point(3, 5)
        point2 = Point(6, 9)
        self.assertEqual(point2.slope_to(point), (-3,-4))

        with self.assertRaises(TypeError):
            point2.slope_to((3, 4))

    def test_str(self):
        point = Point(3, 5)
        result_str = "(3,5)"
        self.assertEqual(str(point), result_str)

    def test_equal(self):
        point1 = Point(3, 5)
        point2 = Point(4, 5)
        not_a_point = (3, 5)
        self.assertEqual(point1, point1)
        self.assertNotEqual(point1, point2)
        with self.assertRaises(TypeError):
            self.assertEqual(point1, not_a_point)


class TestLineSegment(unittest.TestCase):
    def test_init(self):
        line_segment = LineSegment()
        self.assertEqual(len(line_segment.points), 0)
    
    def test_add_point(self):
        line_segment = LineSegment()
        point = Point(3, 4)
        line_segment.add_point(point)
        self.assertEqual(len(line_segment.points), 1)
        self.assertEqual(line_segment.points[0], point)

        with self.assertRaises(TypeError):
            line_segment.add_point((3, 4))
        
    def test_str(self):
        line_segment = LineSegment()
        line_segment.add_point(Point(3,4))
        line_segment.add_point(Point(1,2))
        result_str = "(3,4) -> (1,2)"
        self.assertEqual(str(line_segment), result_str)