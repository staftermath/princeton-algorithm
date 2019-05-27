import pytest


@pytest.fixture()
def unordered_pq():
    from week4.pq import UnorderedMaxPQ
    pq = UnorderedMaxPQ(10)
    return pq


@pytest.fixture()
def raw_keys():
    return [3.0, 5.5, 1.0, 9.5, 0]


def test_unordered_max_pq(unordered_pq, raw_keys):
    with pytest.raises(RuntimeError):
        unordered_pq.delTop()

    assert unordered_pq.isEmpty()

    for key in raw_keys:
        unordered_pq.insert(key)

    assert unordered_pq.N == 5
    assert unordered_pq.delTop() == 9.5
    assert unordered_pq.N == 4
    assert unordered_pq.delTop() == 5.5
    assert unordered_pq.N == 3
    assert unordered_pq.top() == 3.0


@pytest.fixture()
def max_pq():
    from week4.pq import MaxPQ
    pq = MaxPQ(10)
    return pq


def test_max_pq(max_pq, raw_keys):
    with pytest.raises(RuntimeError):
        max_pq.delTop()

    assert max_pq.isEmpty()

    for key in raw_keys:
        max_pq.insert(key)

    assert max_pq.N == 5
    assert max_pq.delTop() == 9.5
    assert max_pq.N == 4
    assert max_pq.delTop() == 5.5
    assert max_pq.N == 3
    assert max_pq.top() == 3.0


def test_max_pq_with_custom_class(max_pq, raw_keys):
    class CustomObject(object):
        def __init__(self, v):
            self._v = v

        def __lt__(self, other):
            """

            Args:
                other (CustomObject):

            Returns:

            """
            return self._v < other._v

    for i in raw_keys:
        max_pq.insert(CustomObject(i))

    assert max_pq.N == 5
    assert max_pq.delTop()._v == 9.5
    assert max_pq.N == 4
    assert max_pq.delTop()._v == 5.5
    assert max_pq.N == 3
    assert max_pq.top()._v == 3.0


@pytest.fixture()
def min_pq():
    from week4.pq import MinPQ
    pq = MinPQ(10)
    return pq


def test_min_pq(min_pq, raw_keys):
    with pytest.raises(RuntimeError):
        min_pq.delTop()

    assert min_pq.isEmpty()

    for key in raw_keys:
        min_pq.insert(key)

    assert min_pq.N == 5
    assert min_pq.delTop() == 0
    assert min_pq.N == 4
    assert min_pq.delTop() == 1.0
    assert min_pq.N == 3
    assert min_pq.top() == 3.0
