import pytest
from part2_week2.mst.mst import Edge


@pytest.mark.parametrize("test_edges, cmp_edges",
                         ((Edge(3, 4, 0.3) > Edge(1, 2, 0.2), True),
                          (Edge(3, 4, 0.1) > Edge(1, 2, 0.2), False),
                          (Edge(3, 4, 0.3) == Edge(1, 2, 0.3), True),
                          (Edge(3, 4, 0.3) >= Edge(1, 2, 0.2), True),
                          (Edge(3, 4, 0.3) >= Edge(1, 2, 0.3), True),
                          (Edge(3, 4, 0.1) < Edge(1, 2, 0.3), True),
                          (Edge(3, 4, 0.3) <= Edge(1, 2, 0.3), True),
                          (Edge(3, 4, 0.4) < Edge(1, 2, 0.3), False),
                          )
                         )
def test_edge_cmp(test_edges, cmp_edges):
    assert test_edges == cmp_edges


def test_edge_method():
    sample_edge = Edge(1, 2, 0.1)
    with pytest.raises(NotImplementedError):
        sample_edge > 2

    with pytest.raises(NotImplementedError):
        2 < sample_edge
    assert str(sample_edge) == "1 -> 2 (0.1)"
    assert sample_edge.weight == 0.1
    assert sample_edge.either() in {1, 2}
    assert sample_edge.other(2) == 1
    assert sample_edge.other(1) == 2

    with pytest.raises(ValueError):
        sample_edge.other(3)


edges = [Edge(0, 7, 0.16),
         Edge(2, 3, 0.17),
         Edge(1, 7, 0.19),
         Edge(0, 2, 0.26),
         Edge(5, 7, 0.28),
         Edge(1, 3, 0.29),
         Edge(1, 5, 0.32),
         Edge(2, 7, 0.34),
         Edge(4, 5, 0.35),
         Edge(1, 2, 0.36),
         Edge(4, 7, 0.37),
         Edge(0, 4, 0.38),
         Edge(6, 2, 0.40),
         Edge(3, 6, 0.52),
         Edge(6, 0, 0.58),
         Edge(6, 4, 0.93)]
n_v = 8


@pytest.fixture()
def ewg():
    from part2_week2.mst.mst import EdgeWeightedGraph, MST
    ewg = EdgeWeightedGraph(n_v)
    for e in edges:
        ewg.addEdge(e)
    return ewg


def test_edge_weighted_graph(ewg):
    assert ewg.V() == n_v
    assert ewg.E() == 16
    assert len(ewg.adj(0)) == 4


def test_mst(ewg):
    from part2_week2.mst.mst import MST
    mst = MST(ewg)

    assert len(mst.edges) == 7
    assert mst.weight() == (0.16+0.17+0.19+0.26+0.28+0.35+0.40)


def test_prim_mst(ewg):
    from part2_week2.mst.mst import PrimMST
    prim_mst = PrimMST(ewg)
    assert len(prim_mst.edges) == 7
    assert prim_mst.weight() == (0.16+0.17+0.19+0.26+0.28+0.35+0.40)
