import pytest


@pytest.fixture()
def flow_edge():
    from part2_week3.maxflow import FlowEdge
    return FlowEdge(3, 4, 10)


def test_flow_edge_properties(flow_edge):
    assert flow_edge.origin == 3
    assert flow_edge.to == 4
    assert flow_edge.capacity == 10
    assert flow_edge.flow == 0
    assert flow_edge.residualCapacityTo(3) == 0
    assert flow_edge.residualCapacityTo(4) == 10


def test_flow_edge_addResidualFlowTo(flow_edge):
    flow_edge.addResidualFlowTo(4, 3)
    assert flow_edge.flow == 3

    flow_edge.addResidualFlowTo(3, 2)
    assert flow_edge.flow == 1


def test_flow_edge_addResidualFlowTo_insufficient(flow_edge):
    with pytest.raises(RuntimeError):
        flow_edge.addResidualFlowTo(3, 4)


def test_flow_edge_equal(flow_edge):
    assert flow_edge == flow_edge


def test_flow_edge_equal_raise_exception(flow_edge):
    with pytest.raises(NotImplementedError):
        assert flow_edge != 1


edges = [(0, 1, 10), (0, 2, 5), (2, 1, 4), (1, 3, 9), (1, 4, 4), (2, 4, 8), (3, 4, 15), (3, 5, 10), (4, 5, 10)]


@pytest.fixture()
def flow_network():
    from part2_week3.maxflow import FlowEdge, FlowNetwork
    flow_network = FlowNetwork(6)
    for edge in edges:
        flow_network.addEdge(FlowEdge(*edge))
    return flow_network


def test_flow_network(flow_network):
    from part2_week3.maxflow import FlowEdge
    assert flow_network.adj(4) == {FlowEdge(1, 4, 4), FlowEdge(2, 4, 8), FlowEdge(3, 4, 15), FlowEdge(4, 5, 10)}


def test_ford_fulkerson_bfs(flow_network):
    from part2_week3.maxflow import FordFulkerson
    ford_fulkerson = FordFulkerson(flow_network, 0, 5)
    assert ford_fulkerson.value() == 15


bigger_edges = [(0, 1, 10), (0, 2, 5), (0, 3, 15),
                (1, 2, 4), (1, 4, 9), (1, 5, 15),
                (2, 5, 8), (2, 3, 4),
                (3, 6, 16),
                (4, 5, 15), (4, 7, 10),
                (5, 7, 10), (5, 6, 15),
                (6, 2, 6), (6, 7, 10)
                ]


@pytest.fixture()
def big_flow_network():
    from part2_week3.maxflow import FlowEdge, FlowNetwork
    big_flow_network = FlowNetwork(8)
    for edge in bigger_edges:
        big_flow_network.addEdge(FlowEdge(*edge))
    return big_flow_network


def test_ford_fulkerson_min_cut(big_flow_network):
    from part2_week3.maxflow import FordFulkerson
    ford_fulkerson = FordFulkerson(big_flow_network, 0, 7)
    assert sorted(ford_fulkerson.min_cut()) == [0, 2, 3, 6]
