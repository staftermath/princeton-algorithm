import pytest
import os
from week3.collinear import *


def test_point_init():
    point = Point(3, 5)
    assert (3, 5) == (point.x, point.y)


def test_piont_slope_to():
    point = Point(3, 5)
    point2 = Point(6, 9)
    assert Slope(Point(3, 5), Point(6, 9)) == point2.slope_to(point)
    point3 = Point(4, 8)
    assert Slope(Point(3, 5), Point(4, 8)) == point.slope_to(point3)

    with pytest.raises(TypeError):
        point2.slope_to((3, 4))


def test_point_str():
    point = Point(3, 5)
    result_str = "(3,5)"
    assert result_str == str(point)


def test_point_equal():
    point1 = Point(3, 5)
    point2 = Point(4, 5)
    not_a_point = (3, 5)
    assert point1 == point1
    assert point1 != point2
    with pytest.raises(TypeError):
        assert point1 != not_a_point


@pytest.mark.parametrize(("test_slope", "expected"),
                         [
                             (Slope(Point(6, 10), Point(2, 2)), (1, 2)),
                             (Slope(Point(6, 10), Point(6, 10)), (0, 0)),
                             (Slope(Point(6, 10), Point(6, 5)), (0, 1)),
                             (Slope(Point(6, 10), Point(8, 10)), (1, 0)),
                             (Slope(Point(6, 10), Point(10, 2)), (1, -2)),
                             (Slope(Point(6, 10), Point(10, 18)), (1, 2))
                         ]
                         )
def test_slope_init(test_slope, expected):
    assert expected == (test_slope.dx, test_slope.dy)


def test_equal():
    slope1 = Slope(Point(6, 10), Point(10, 2))
    slope2 = Slope(Point(6, 10), Point(0, 22))
    assert slope1 == slope2
    assert slope1 == Slope(Point(3, 4), Point(2, 6))
    assert Slope(Point(0, 3), Point(0, -2)) != Slope(Point(-1, 3), Point(-1, 6))
    assert Slope(Point(3, 3), Point(3, 3)) == Slope(Point(4, 4), Point(4, 4))

    with pytest.raises(TypeError):
        assert Slope(Point(3, 3), Point(3, 3)) == (0, 1)


def test_init():
    line_segment = LineSegment()
    assert 0 == len(line_segment.points)


def test_add_point():
    line_segment = LineSegment()
    point = Point(3, 4)
    line_segment.add_point(point)
    assert 1 == len(line_segment.points)
    assert point == line_segment.points[0]

    with pytest.raises(TypeError):
        line_segment.add_point((3, 4))


def test_str():
    line_segment = LineSegment()
    line_segment.add_point(Point(3,4))
    line_segment.add_point(Point(1,2))
    result_str = "(3,4) -> (1,2)"
    assert result_str == str(line_segment)


@pytest.fixture()
def resource_path():
    resource_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")
    return resource_path


@pytest.fixture()
def grid5x5(resource_path):
    from week3.collinear import load_file
    points = load_file(os.path.join(resource_path, "grid5x5.txt"))
    return points


def test_FastCollinearPoints_segments(grid5x5):
    from week3.collinear import FastCollinearPoints
    # require validation
    fast_collinear_points = FastCollinearPoints(grid5x5)
    assert fast_collinear_points == 36
