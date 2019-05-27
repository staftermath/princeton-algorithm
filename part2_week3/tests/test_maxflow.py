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
