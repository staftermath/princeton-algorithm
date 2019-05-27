"""
This file implement a pattern recoginition algorithm to 
discover every (maximal) line segment that connects a subset of 4 or more points
in a given set of points

Implement an algorithm based on
1. Sorting of slope:
    a. time: O(N^2) slope calculation + O(N*log(N)) sorting
2. Hash slope:
    a. time: O(N^2)
    b. space: O(N)
"""
import sys
from math import gcd


class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def slope_to(self, p):
        if isinstance(p, Point):
            return Slope(self, p)
        else:
            raise TypeError("p is not Point")
    
    def __eq__(self, value):
        if not isinstance(value, Point):
            raise TypeError("value is not a Point")
        else:
            return value.x == self.x and value.y == self.y

    def __hash__(self):
        return hash(str(self))


class Slope(object):
    def __init__(self, a, b):
        """

        Args:
            a (Point):
            b (Point):
        """
        self._a = a
        self._b = b
        self._slope = None
        self._reduce()
    
    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def dx(self):
        return self._slope[0]

    @property
    def dy(self):
        return self._slope[1]

    def _reduce(self):
        dx = self.a.x-self.b.x
        dy = self.a.y-self.b.y
        slope_gcd = gcd(dx, dy)
        if slope_gcd != 0:
            dx /= slope_gcd
            dy /= slope_gcd
        if dx < 0:
            dx = -dx
            dy = -dy
        self._slope = (dx, dy)

    def __eq__(self, other):
        if isinstance(other, Slope):
            # TODO: fix integer overflow 
            return self.dx == other.dx and self.dy == other.dy
        else:
            raise TypeError("value is not Slope")

    def __lt__(self, other):
        if isinstance(other, Slope):
            if self.dy == 0 or other.dy == 0:
                return self.dy < other.dy
            else:
                return self.dx/self.dy < other.dx/other.dy
        else:
            raise TypeError("value is not Slope")


class LineSegment(object):
    def __init__(self):
        self._points = []

    @property
    def points(self):
        return self._points
    
    def add_point(self, p):
        if isinstance(p, Point):
            self._points.append(p)
        else:
            raise TypeError("p is not a Point")

    def __str__(self):
        return " -> ".join([str(p) for p in self._points])


class FastCollinearPoints(object):

    def __init__(self, points):
        self._numberOfSegments = 0
        self._lineSegments = []
        self._segments(points)

    def _segments(self, points):
        """The method segments() should include each maximal line segment containing 4 (or more) points exactly once.
        For example, if 5 points appear on a line segment in the order p→q→r→s→t,
        then do not include the subsegments p→s or q→t.
        Args:
            points (list): list of points

        """
        from itertools import chain
        for i in range(len(points)-3):
            slopes = [Slope(points[i], points[p]) for p in range(i, len(points))]
            sorted(slopes)
            num_slopes = len(slopes)
            for i in range(num_slopes-2):
                if slopes[i] == slopes[i+2]:
                    line_segment = LineSegment()
                    points_in_line = set(chain.from_iterable([[s.a, s.b] for s in slopes[i:(i+3)]]))
                    for p in points_in_line:
                        line_segment.add_point(p)
                    self._lineSegments.append(line_segment)
                    self._numberOfSegments += 1


def load_file(input_file):
    with open(input_file, 'r') as f:
        line = int(next(f))
        points = [None]*line
        i = 0
        for line in f:
            x = int(line[:5])
            y = int(line[7:])
            points[i] = Point(x, y)
            i += 1
    return points


if __name__ == "__main__":
    input_file = sys.argv[1]
    points = load_file(input_file)
