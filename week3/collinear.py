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
            return (p.x-self.x, p.y-self.y)
        else:
            raise TypeError("p is not Point")
    
    def __eq__(self, value):
        if not isinstance(value, Point):
            raise TypeError("value is not a Point")
        else:
            return value.x == self.x and value.y == self.y


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
        return " -> ".join(self._points)
