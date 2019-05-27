import pytest
import random
from week2.dequeue import Deque, RandomDeque


def test_deque_init():
    deque = Deque()
    assert deque.size == 0
    assert deque.is_empty()
    assert deque._begin == 1
    assert deque._end == 1
    assert len(deque._array) == 4

    deque = Deque([100, 200, 300, 400])
    assert deque.size == 4
    assert deque.remove_first() == 100
    assert deque.remove_last() == 400


def test_deque_first_and_add_first():
    deque = Deque()
    deque.add_first(100)
    
    assert deque.first() == 100
    assert deque.size == 1
    assert len(deque._array) == 4

    first_batch = [200, 300, 400]
    for val in first_batch:
        deque.add_first(val)
    
    assert deque.first() == 400
    
    deque = Deque()
    deque.add_last(100)
    assert deque._begin == 1
    assert deque._end == 2
    assert deque.first() == 100
    assert deque.size == 1
    assert len(deque._array) == 4

    first_batch = [200, 300, 400]
    for val in first_batch:
        deque.add_last(val)
    
    assert len(deque._array) == 8
    assert deque.last() == 400
    assert deque.first() == 100


def test_deque_remove_first():
    deque = Deque()
    deque.add_first(100)
    deque.add_first(200)
    result = deque.remove_first()
    assert result == 200
    result = deque.remove_first()
    assert result == 100
    assert deque.is_empty()


def test_deque_remove_last():
    deque = Deque()
    deque.add_first(100)
    deque.add_first(200)
    deque.add_last(300)
    result = deque.remove_last()
    assert result == 300
    assert deque.size == 2
    result = deque.remove_last()
    assert result == 100
    assert deque.size == 1
    result = deque.remove_last()
    assert result == 200
    assert deque.is_empty()


def test_deque_iterator():
    deque = Deque([100, 200, 300, 400])

    result = []
    for x in deque:
        result.append(x)

    assert result == [100, 200, 300, 400]


def test_randome_dequesample():
    random.seed(123)
    random_deque = RandomDeque(list(range(100)))
    result = random_deque.sample()
    assert result == 6
    result = random_deque.sample()
    assert result == 34
