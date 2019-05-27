import pytest
from week4.puzzle import HammingDistanceHash
import numpy as np


@pytest.mark.parametrize(("test_tuple", "expected_distance", "expected_visited"),
                         [(np.array([1, 2, 3, 4, 5, 6]), 0, False),
                          (np.array([1, 2, 3, 4, 6, 5]), 2, False),
                          (np.array([1, 2, 3, 6, 4, 5]), 3, False)])
def test_hamming_distance_hash(test_tuple, expected_distance,expected_visited):
    hamming = HammingDistanceHash(2, 3)
    assert expected_distance == hamming.get_distance(test_tuple)
    assert expected_visited == hamming.visited(test_tuple)


# @pytest.mark.parametrize(("test_tuple", "expected_moves"),
#                          [(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), [np.array([1, 2, 3, 4, 5, 9, 7, 8, 6]), None,
#                                                          (1, 2, 3, 4, 5, 6, 7, 9, 8), None]),
#                           (np.array([9, 1, 2, 3, 4, 5, 6, 7, 8]), [None, np.array([3, 1, 2, 9, 4, 5, 6, 7, 8]),
#                                                          None, np.array([1, 9, 2, 3, 4, 5, 6, 7, 8])]),
#                           (np.array([1, 9, 2, 3, 4, 5, 6, 7, 8]), [None, np.array([1, 4, 2, 3, 9, 5, 6, 7, 8]),
#                                                                    np.array([9, 1, 2, 3, 4, 5, 6, 7, 8]), np.array([1, 2, 9, 3, 4, 5, 6, 7, 8])]),
#                           ((1, 2, 9, 3, 4, 5, 6, 7, 8), [None, (1, 2, 5, 3, 4, 9, 6, 7, 8),
#                                                          (1, 9, 2, 3, 4, 5, 6, 7, 8), None]),
#                           ((1, 2, 3, 9, 4, 5, 6, 7, 8), [(9, 2, 3, 1, 4, 5, 6, 7, 8), (1, 2, 3, 6, 4, 5, 9, 7, 8),
#                                                          None, (1, 2, 3, 4, 9, 5, 6, 7, 8)]),
#                           ((1, 2, 3, 4, 9, 5, 6, 7, 8), [(1, 9, 3, 4, 2, 5, 6, 7, 8), (1, 2, 3, 4, 7, 5, 6, 9, 8),
#                                                          (1, 2, 3, 9, 4, 5, 6, 7, 8), (1, 2, 3, 4, 5, 9, 6, 7, 8)]),
#                           ])
# def test_hamming_distance_possible_move(test_tuple, expected_moves):
#     hamming = HammingDistanceHash(3, 3)
#     assert hamming.possible_move(test_tuple) == expected_moves


@pytest.mark.parametrize(("test_tuple", "solvable"), [
    (np.array([1, 2, 3, 4, 5, 6, 7, 9, 8]), True),
    (np.array([1, 2, 3, 4, 5, 6, 9, 7, 8]), True),
    (np.array([1, 2, 3, 9, 5, 6, 4, 7, 8]), True),
    (np.array([2, 1, 4, 3, 5, 6, 7, 8, 9]), False)
])
def test_hamming_distance_solvable(test_tuple, solvable):
    hamming = HammingDistanceHash(3, 3)
    assert solvable == hamming.solve(test_tuple)
