import pytest
from part2_week2.sp import DirectedEdge


# @pytest.fixture()
# def directed_edge():
#     from part2_week2.sp import DirectedEdge
#     de = DirectedEdge(1, 2, 0.5)
#     return de


def test_directed_weighted_edge_attributes():
    directed_edge = DirectedEdge(1, 2, 0.5)
    assert 1 == directed_edge.origin
    assert 2 == directed_edge.to
    assert 0.5 == directed_edge.weight


directed_edge = [DirectedEdge(0, 1, 5),
                 DirectedEdge(0, 7, 8),
                 DirectedEdge(0, 4, 9),
                 DirectedEdge(1, 3, 15),
                 DirectedEdge(1, 2, 12),
                 DirectedEdge(1, 7, 4),
                 DirectedEdge(7, 2, 7),
                 DirectedEdge(7, 5, 6),
                 DirectedEdge(4, 7, 5),
                 DirectedEdge(4, 5, 4),
                 DirectedEdge(4, 6, 20),
                 DirectedEdge(3, 6, 9),
                 DirectedEdge(2, 3, 3),
                 DirectedEdge(2, 6, 11),
                 DirectedEdge(5, 2, 1),
                 DirectedEdge(5, 6, 13)
                 ]
n_v = 8


@pytest.fixture()
def dewg():
    from part2_week2.sp import EdgeWeightedDigraph
    dewg = EdgeWeightedDigraph(n_v)
    for e in directed_edge:
        dewg.addEdge(e)
    return dewg


@pytest.fixture()
def dijkstra(dewg):
    from part2_week2.sp import DijkstraSP
    return DijkstraSP(dewg, 0)


distance = [(7, 8),
      (6, 25),
      (2, 14),
      (3, 17),
      (5, 13)]


@pytest.mark.parametrize(("target", "expected_sp"),
                         distance)
def test_dijkstra_dist_to(dijkstra, target, expected_sp):
    assert expected_sp == dijkstra.distTo(target)


sp = [
    (7, [0, 7]),
    (6, [0, 4, 5, 2, 6]),
    (2, [0, 4, 5, 2]),
    (3, [0, 4, 5, 2, 3]),
    (5, [0, 4, 5])
]


@pytest.mark.parametrize(("target", "path"),
                         sp)
def test_dijkstra_path_to(dijkstra, target, path):
    assert path == dijkstra.pathTo(target)


@pytest.fixture()
def acyclic_sp(dewg):
    from part2_week2.sp import AcyclicSP
    acyclic_sp = AcyclicSP(dewg, 0)
    return acyclic_sp


@pytest.mark.parametrize(("target", "expected_sp"),
                         distance)
def test_acyclic_distance(acyclic_sp, target, expected_sp):
    assert expected_sp == acyclic_sp.distTo(target)


@pytest.mark.parametrize(("target", "path"),
                         sp)
def test_acyclic_sp(acyclic_sp, target, path):
    assert path == acyclic_sp.pathTo(target)
