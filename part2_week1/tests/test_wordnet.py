import pytest
import os
from part2_week1.wordnet import WordNet


TEST_NAME = "princeton_algorithm_unittest_part2_week1"


@pytest.fixture()
def tmp_folder(tmpdir):
    if not tmpdir.join(TEST_NAME).exists():
        tmpdir.mkdir(TEST_NAME)
    return tmpdir.join(TEST_NAME)


@pytest.fixture()
def resources():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")


@pytest.fixture()
def test_synsets(resources):
    return os.path.join(resources, "test_synsets.txt")


@pytest.fixture()
def test_hypernyms(resources):
    return os.path.join(resources, "test_hypernyms.txt")


@pytest.fixture()
def synsets(tmp_folder):
    import urllib.request
    url = "http://coursera.cs.princeton.edu/algs4/testing/wordnet/synsets.txt"
    path = tmp_folder.join("synsets.txt")
    urllib.request.urlretrieve(url, str(path))
    return str(path)


@pytest.fixture()
def hypernyms(tmp_folder):
    import urllib.request
    url = "http://coursera.cs.princeton.edu/algs4/testing/wordnet/hypernyms.txt"
    path = tmp_folder.join("hypernyms.txt")
    urllib.request.urlretrieve(url, str(path))
    return str(path)


@pytest.fixture()
def wordnet(test_synsets, test_hypernyms):
    return WordNet(test_synsets, test_hypernyms)


@pytest.fixture()
def nouns():
    return {"noun0", "noun1", "noun1_dup1",
     "noun2", "noun3", "noun3_dup1",
     "noun3_dup2", "noun3_dup3", "noun4", "noun5", "entity", "noun6"}


@pytest.mark.parametrize(("nouns", "expected"),
                         [
                             ("noun3", True),
                             ("badnoun", False),
                             ("root", False)
                         ])
def test_wordnet_isNoun(wordnet, nouns, expected):
    assert wordnet.isNoun(nouns) == expected


def test_wordnet_nouns(wordnet, nouns):
    assert set(wordnet.nouns()) == nouns


@pytest.mark.parametrize(("noun", "expected_id"),
                         [
                             ("noun0", {0}),
                             ("entity", {7}),
                             ("noun3_dup2", {3})
                         ])
def test_wordnet_id(wordnet, noun, expected_id):
    assert expected_id == wordnet.id(noun)


def test_wordnet_id_not_valid_noun(wordnet):
    with pytest.raises(RuntimeError):
        wordnet.id("dummy")


@pytest.mark.parametrize(("test_nouns", "expected_distance"),
                         [
                             (["noun0", "noun3"], 3),
                             (["noun1", "noun3"], 2),
                             (["noun1", "noun2"], 4)
                         ])
def test_wordnet_distance(wordnet, test_nouns, expected_distance):
    assert wordnet.distance(test_nouns[0], test_nouns[1]) == expected_distance


@pytest.mark.parametrize(("test_nouns", "expected_sap"),
                         [
                             (["noun0", "noun3"], "noun4"),
                             (["noun1", "noun3"], "noun4"),
                             (["noun1", "noun2"], "entity")
                         ])
def test_wordnet_sap(wordnet, test_nouns, expected_sap):
    assert expected_sap == wordnet.sap(test_nouns[0], test_nouns[1])


@pytest.mark.skip
def test_raw_wordnet(synsets, hypernyms):
    wordnet = WordNet(synsets, hypernyms)
    assert wordnet.distance("quadrangle", "mountain_devil") == 11


@pytest.fixture()
def digraph(resources):
    from part2_week1.graph import Digraph
    digraph_path = os.path.join(resources, "test_digraph.txt")
    with open(digraph_path, 'r') as f:
        v = int(f.readline())
        digraph = Digraph(v)
        e = int(f.readline())
        for l in f:
            origin = int(l[:2])
            target = int(l[2:])
            digraph.addEdge(int(origin), int(target))
    return digraph


@pytest.mark.parametrize(("test_idx", "expected_distance", "expected_ancestor"),
                         [
                             ([3, 11], 4, 1),
                             ([9, 12], 3, 5),
                             ([7, 2], 4, 0),
                             ([1, 6], -1, -1),
                         ])
def test_sap(digraph, test_idx, expected_distance, expected_ancestor):
    from part2_week1.wordnet import SAP
    sap = SAP(digraph)
    assert sap.length(*test_idx) == expected_distance
    assert sap.ancestor(*test_idx) == expected_ancestor


def test_outcast(digraph, wordnet):
    from part2_week1.wordnet import Outcast
    outcast = Outcast(wordnet)
    result = outcast.outcast(["noun3", "noun5", "noun6"])
    assert result == "noun5"


@pytest.fixture()
def full_wordnet(synsets, hypernyms):
    return WordNet(synsets, hypernyms)


@pytest.fixture()
def full_outcast(full_wordnet):
    from part2_week1.wordnet import Outcast
    outcast = Outcast(full_wordnet)
    return outcast


@pytest.mark.skip
@pytest.mark.parametrize(("test_nouns_file", "expected_outcast"),
                         [
                             ("outcast5.txt", "table"),
                             ("outcast8.txt", "bed"),
                             ("outcast11.txt", "potato")
                         ])
def test_full_outcast(full_outcast, resources, test_nouns_file, expected_outcast):
    with open(os.path.join(resources, test_nouns_file), 'r') as f:
        nouns = []
        for l in f:
            nouns.append(l.strip())
    assert expected_outcast == full_outcast.outcast(nouns)
