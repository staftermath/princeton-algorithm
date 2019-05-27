import pytest


@pytest.fixture()
def dfs_bfs_graph():
    from part2_week1.graph import Graph
    graph = Graph(11)
    for v, w in [(0, 1), (0, 2), (0, 6), (0, 5), (5, 3), (3, 4), (4, 6), (4, 5), (7, 8), (9, 10)]:
        graph.addEdge(v, w)
    return graph


test_data = [(1, True), (2, True), (3, True), (4, True), (5, True), (6, True),
             (7, False), (8, False), (9, False), (10, False)]


@pytest.mark.parametrize("test_input, expected", test_data)
def test_dfs(dfs_bfs_graph, test_input, expected):
    from part2_week1.path import DepthFirstPaths
    dfs = DepthFirstPaths(dfs_bfs_graph, 0)
    assert dfs.hasPathTo(test_input) == expected


@pytest.mark.parametrize("test_input, expected", test_data)
def test_bfs(dfs_bfs_graph, test_input, expected):
    from part2_week1.path import BreadthFirstPaths
    bfs = BreadthFirstPaths(dfs_bfs_graph, 0)
    assert bfs.hasPathTo(test_input) == expected


@pytest.fixture()
def cc_graph():
    from part2_week1.graph import Graph
    graph = Graph(13)
    for v, w in [(0, 1), (0, 2), (0, 6), (0, 5), (5, 3), (3, 4), (4, 6),
                 (4, 5), (7, 8), (9, 10), (9, 11), (11, 12), (9, 12)]:
        graph.addEdge(v, w)
    return graph


cc_test_data_connected = [
    ((0, 4), True),
    ((1, 5), True),
    ((0, 7), False),
    ((11, 10), True),
    ((7, 12), False),
]

cc_test_data_ids = [
    (4, 0),
    (7, 1),
    (10, 2),
    (12, 2),
    (0, 0)
]


@pytest.mark.parametrize("test_input_connected, expected_connected", cc_test_data_connected)
@pytest.mark.parametrize("test_input_id, expected_id", cc_test_data_connected)
def test_cc(cc_graph, test_input_connected, expected_connected, test_input_id, expected_id):
    from part2_week1.path import CC
    cc = CC(cc_graph)
    assert cc.connected(*test_input_connected) == expected_connected
    assert cc.connected(*test_input_id) == expected_id


@pytest.fixture()
def dfs_bfs_digraph():
    from part2_week1.graph import Digraph
    graph = Digraph(13)
    for v, w in [(0, 1), (0, 5), (2, 0), (6, 0), (3, 5), (3, 2), (2, 3), (4, 2), (5, 4),
                 (4, 3), (6, 4), (11, 4), (6, 9), (7, 6), (6, 8), (8, 6), (7, 9), (9, 10),
                 (10, 12), (12, 9), (9, 11), (11, 12)]:
        graph.addEdge(v, w)
    return graph


test_digrah_data = [(1, True), (6, False), (2, True), (9, False)]


@pytest.mark.parametrize("test_input, expected", test_digrah_data)
def test_digraph_dfs(dfs_bfs_digraph, test_input, expected):
    from part2_week1.path import DepthFirstPaths
    dfs = DepthFirstPaths(dfs_bfs_digraph, 0)
    assert dfs.hasPathTo(test_input) == expected


@pytest.mark.parametrize("test_input, expected", test_digrah_data)
def test_digraph_bfs(dfs_bfs_digraph, test_input, expected):
    from part2_week1.path import BreadthFirstPaths
    bfs = BreadthFirstPaths(dfs_bfs_digraph, 0)
    assert bfs.hasPathTo(test_input) == expected
