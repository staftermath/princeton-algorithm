"""This file tests the implementation of Graph class
"""
import pytest


@pytest.fixture()
def edges():
    return [(0, 1), (0, 2), (1, 2), (3, 4), (2, 4)]


@pytest.fixture()
def graph(edges):
    from part2_week1.graph import Graph
    graph = Graph(5)
    for v, w in edges:
        graph.addEdge(v, w)
    return graph


def test_initiation():
    from part2_week1.graph import Graph
    graph = Graph(3)
    with pytest.raises(TypeError):
        Graph(3.5)

    with pytest.raises(ValueError):
        Graph(-3)

    with pytest.raises(ValueError):
        Graph(0)


def test_add_edges():
    from part2_week1.graph import Graph
    graph = Graph(3)
    assert graph.V == 3

    graph.addEdge(0, 1)
    assert graph.E == 1

    graph.addEdge(0, 2)
    assert graph.E == 2

    graph.addEdge(1, 2)
    assert graph.E == 3

    # add existing edge should not increase any count
    graph.addEdge(1, 2)
    assert graph.E == 3
    assert graph.V == 3


def test_adj(graph):
    assert sorted(graph.adj(0)) == [1, 2]
    assert sorted(graph.adj(4)) == [2, 3]
    assert sorted(graph.adj(2)) == [0, 1, 4]

    with pytest.raises(ValueError):
        graph.adj(5)


def test_degree(graph):
    from part2_week1.graph import Graph
    assert Graph.degree(graph, 0) == 2
    assert Graph.degree(graph, 2) == 3
    with pytest.raises(ValueError):
        Graph.degree(graph, 5)


def test_maxDegree(graph):
    from part2_week1.graph import Graph
    assert Graph.maxDegree(graph) == 3


def test_averageDegree(graph):
    from part2_week1.graph import Graph
    assert Graph.averageDegree(graph) == 2


def test_numberOfSelfLoops(graph):
    from part2_week1.graph import Graph
    assert Graph.numberOfSelfLoops(graph) == 0
    graph.addEdge(0, 0)
    assert Graph.numberOfSelfLoops(graph) == 1
    graph.addEdge(4, 4)
    assert Graph.numberOfSelfLoops(graph) == 2


@pytest.fixture()
def digraph_edges():
    return [(0, 1), (0, 2), (1, 2), (3, 4), (2, 4), (4, 1)]


@pytest.fixture()
def digraph(digraph_edges):
    from part2_week1.graph import Digraph
    graph = Digraph(5)
    for v, w in digraph_edges:
        graph.addEdge(v, w)
    return graph


def test_digraph_add_edges(digraph):
    assert digraph.V == 5
    assert digraph.E == 6


def test_digraph_adj(digraph):
    assert sorted(digraph.adj(0)) == [1, 2]
    assert sorted(digraph.adj(4)) == [1]
    assert sorted(digraph.adj(2)) == [4]

    with pytest.raises(ValueError):
        digraph.adj(5)
