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
            return Slope(p.x-self.x, p.y-self.y)
        else:
            raise TypeError("p is not Point")
    
    def __eq__(self, value):
        if not isinstance(value, Point):
            raise TypeError("value is not a Point")
        else:
            return value.x == self.x and value.y == self.y


class Slope(object):
    def __init__(self, a, b):
        self._a = a
        self._b = b
        self._reduce()
    
    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    def _reduce(self):
        slope_gcd = gcd(self.a, self.b)
        if slope_gcd != 0:
            self._a /= slope_gcd
            self._b /= slope_gcd
        
        if self._a < 0:
            self._a = -self._a
            self._b = -self._b

    def __eq__(self, value):
        if isinstance(value, Slope):
            # TODO: fix integer overflow 
            return (0 == self.a == self.b == value.a == value.b) or (self.a*value.b == self.b*value.a)
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
    