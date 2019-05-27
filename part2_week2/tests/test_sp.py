import pytest


@pytest.fixture()
def directed_edge():
    from part2_week2.shortest_path.sp import DirectedEdge
    de = DirectedEdge(1, 2, 0.5)
    return de


def test_directed_weighted_edge_attributes(directed_edge):
    assert 1 == directed_edge.origin
    assert 2 == directed_edge.to
    assert 0.5 == directed_edge.weight