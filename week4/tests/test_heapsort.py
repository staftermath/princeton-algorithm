import pytest




@pytest.fixture()
def max_pq():
    from week4.pq import MaxPQ
    keys = [3.0, 5.5, 1.0, 9.5, 0]
    pq = MaxPQ(10)
    for key in keys:
        pq.insert(key)
    return pq


def test_heaqsort(max_pq):
    from week4.heapsort import HeapSort
    heap_sort = HeapSort(max_pq)
    assert heap_sort.top() == 9.5
    assert heap_sort.topk(4) == [9.5, 5.5, 3.0, 1.0]
