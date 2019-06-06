import pytest
import numpy as np
from numpy.testing import assert_array_equal

pattern = "ABABAC"
ord_from = ord('A')


@pytest.fixture()
def kmp():
    from part2_week4.substring_search import KMP
    kmp = KMP(pattern, radix=3, ord_from=ord_from)
    return kmp


dfa = np.array([[1, 1, 3, 1, 5, 1],
                [0, 2, 0, 4, 0, 4],
                [0, 0, 0, 0, 0, 6]], dtype="int")


def test_kmp_dfa(kmp):
    assert_array_equal(kmp._dfa, dfa)


string_and_indices = [
    ("ABABAC", 0),
    ("BABABABA", -1),
    ("CCCABABABABACCC", 7),
    ("CCCABAAAABABABACCC", 10)
]


@pytest.mark.parametrize(("test_string", "expected"),
                         string_and_indices)
def test_kmp_search(kmp, test_string, expected):
    assert kmp.search(test_string) == expected


@pytest.mark.parametrize(("bad_string", "expected_error"),
                         [
                             ("bad", IndexError),
                             ("中文", IndexError)
                         ])
def test_kmp_search_error(kmp, bad_string, expected_error):
    with pytest.raises(expected_error):
        kmp.search(bad_string)


full_pattern = "an_awesome_string"


@pytest.fixture()
def full_kmp():
    from part2_week4.substring_search import KMP
    full_kmp = KMP(full_pattern)
    return full_kmp


@pytest.mark.parametrize(("test_string", "expected"),
                         [
                             ("an_awesome_string_is_here", 0),
                             ("BABABABA", -1),
                             ("@_#an_awesome_string@@", 3)
                         ])
def test_full_kmp_search(full_kmp, test_string, expected):
    assert full_kmp.search(test_string) == expected


@pytest.fixture()
def bm():
    from part2_week4.substring_search import BM
    bm = BM(pattern, radix=3, ord_from=ord_from)
    return bm


@pytest.mark.parametrize(("test_string", "expected"),
                         string_and_indices)
def test_bm_search(bm, test_string, expected):
    assert bm.search(test_string) == expected


@pytest.fixture()
def rk():
    from part2_week4.substring_search import RabinKarp
    rk = RabinKarp(pattern)
    return rk


@pytest.mark.parametrize(("test_string", "expected"),
                         string_and_indices)
def test_bm_search(rk, test_string, expected):
    assert rk.search(test_string) == expected
