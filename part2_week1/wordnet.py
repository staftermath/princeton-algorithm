"""
Implement WordNet
"""
from collections import defaultdict
from part2_week1.graph import Digraph
import csv


class SAP(object):
    """Implement an data type SAP (Shortest Ancestral Path)"""
    def __init__(self, G):
        """

        Args:
            G (Digraph):
        """
        self._G = G

    def length(self, v, w):
        """
        Find distance between v and w.
        Distance is defined as sum of steps to shortest common ancestor.
        If no such ancestor exists, return -1
        Args:
            v (int):
            w (int):

        Returns:
            (int)
        """
        min_distance = -1
        visited_from_a = defaultdict(int)
        visited_from_b = defaultdict(int)
        self.min_distance_to_id(v, self._G, visited_from_a)
        self.min_distance_to_id(w, self._G, visited_from_b)
        for idx, d in visited_from_a.items():
            if idx in visited_from_b:
                min_distance = min(min_distance, d+visited_from_b[idx]) if min_distance != -1 else d+visited_from_b[idx]

        return min_distance

    def ancestor(self, v, w):
        """
        Find shortest common ancestor for v and w.
        If no such value exists, return -1
        Args:
            v (int):
            w (int):

        Returns:
            (int)
        """
        min_distance = self._G.V*2
        visited_from_a = defaultdict(int)
        visited_from_b = defaultdict(int)
        self.min_distance_to_id(v, self._G, visited_from_a)
        self.min_distance_to_id(w, self._G, visited_from_b)
        min_distance = -1
        ancestor = -1
        for idx, d in visited_from_a.items():
            if idx in visited_from_b:
                if min_distance == -1:
                    min_distance = d+visited_from_b[idx]
                    ancestor = idx
                elif d+visited_from_b[idx] < min_distance:
                    min_distance = min(min_distance, d+visited_from_b[idx])
                    ancestor = idx

        return ancestor

    def length_s(self, v, w):
        """
        find distance to set v and w. Distance is defined as
        sum of length shortest common ancestor for set v and w.
        If no such ancestor exists, return -1
        Args:
            v (Iterable):
            w: (Iterable)

        Returns:
            (int)
        """
        visited_from_v = self._distance_to_set(v)
        visited_from_w = self._distance_to_set(w)
        min_distance = -1
        for idx, d in visited_from_v.items():
            if idx in visited_from_w:
                min_distance = min(min_distance, d+visited_from_w[idx]) if min_distance != -1 else d+visited_from_w[idx]

        return min_distance

    def ancestor_s(self, v, w):
        """
        find shortest common ancestor for set v and w.
        If no such ancestor exists, return -1
        Args:
            v (Iterable):
            w: (Iterable)

        Returns:
            (int)
        """
        visited_from_v = self._distance_to_set(v)
        visited_from_w = self._distance_to_set(w)
        min_distance = -1
        ancestor = -1
        for idx, d in visited_from_v.items():
            if idx in visited_from_w:
                if min_distance == -1:
                    min_distance = d+visited_from_w[idx]
                    ancestor = idx
                elif d+visited_from_w[idx] < min_distance:
                    min_distance = min(min_distance, d+visited_from_w[idx])
                    ancestor = idx

        return ancestor

    def _distance_to_set(self, v):
        """
        Find shortest distance from any member in v to any node in graph
        Args:
            v (Iterable):

        Returns:
            (defaultdict)
        """
        visited_from_v = defaultdict(int)
        for va in v:
            self.min_distance_to_id(va, self._G, visited_from_v)
        return visited_from_v

    @staticmethod
    def min_distance_to_id(idx, graph, distance):
        """
        Find distance of all node on path from idx.
        time: O(N)
        space: O(N)
        Args:
            idx (ind):
            graph (Graph):
            distance (None or defaultdict)

        Returns:
            None
        """
        from week2.dequeue import Deque
        min_paths = []
        visited = dict()
        for id in graph.adj(idx):
            queue = Deque()
            queue.add_last(id)
            min_paths.append(queue)
            visited[id] = 1
        ended = False
        while not ended:
            ended = True
            for path in min_paths:
                last = path.last()
                for id in graph.adj(last):
                    if id not in visited:
                        # at least one id has not been visited
                        ended = False
                        path.add_last(id)
                        visited[id] = visited[last]+1
        for i, v in visited.items():
            if i in distance:
                distance[i] = min(visited[i], distance[i])
            else:
                distance[i] = visited[i]


class WordNet(object):

    def __init__(self, synsets, hypernyms):
        """
        root is not listed in either synsets or hypernyms
        Args:
            synsets (string): path to synsets file
            hypernyms (string): path to hypernyms file
        """
        self._nouns = defaultdict(set)
        self._ids = defaultdict(str)
        with open(synsets, 'r') as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                synset_id = int(line[0])
                for noun in line[1].split(" "):
                    self._nouns[noun].add(synset_id)
                    self._ids[synset_id] = noun
        with open(synsets, 'r') as f:
            last_line = f.readlines()[-1]
            V = int(last_line.strip().split(",")[0])+1
        self._root_id = -1
        dag = Digraph(V)
        with open(hypernyms, 'r') as f:
            for line in f:
                edges = line.strip().split(",")
                if len(edges) == 1:
                    self._root_id = int(edges[0])
                else:
                    synset_id = int(edges[0])
                    for _id in edges[1:]:
                        dag.addEdge(synset_id, int(_id))
        self._sap = SAP(dag)

    def id(self, noun):
        if self.isNoun(noun):
            return self._nouns[noun]
        else:
            raise RuntimeError("{} is not valid noun".format(noun))

    def _noun(self, id):
        if id in self._ids:
            return self._ids[id]
        else:
            raise RuntimeError("{} is not valid synset".format(id))

    def nouns(self):
        return self._nouns.keys()

    def isNoun(self, word):
        return word in self._nouns

    def distance(self, nounA, nounB):
        # get a lower bound for maximum path from nounA to root

        if not self.isNoun(nounA) or not self.isNoun(nounB):
            raise RuntimeError("{} or {} are not valid nouns".format(nounA, nounB))

        id_a = self._nouns[nounA]
        id_b = self._nouns[nounB]

        return self._sap.length_s(id_a, id_b)

    def sap(self, nounA, nounB):
        """

        Args:
            nounA (string):
            nounB (string):

        Returns:

        """
        if not self.isNoun(nounA) or not self.isNoun(nounB):
            raise RuntimeError("{} or {} are not valid nouns".format(nounA, nounB))

        id_a = self._nouns[nounA]
        id_b = self._nouns[nounB]
        return self._noun(self._sap.ancestor_s(id_a, id_b))

    @staticmethod
    def min_distance_to_id(idx, graph):
        """
        Find distance of all node on path from idx.
        time: O(N)
        space: O(N)
        Args:
            idx (ind):
            graph (Graph):

        Returns:
            (dict)
        """
        from week2.dequeue import Deque
        visited = {idx: 0}
        min_paths = []
        for id in graph.adj(idx):
            queue = Deque()
            queue.add_last(id)
            min_paths.append(queue)
            visited[id] = 1
        ended = False
        while not ended:
            ended = True
            for path in min_paths:
                last = path.last()
                for id in graph.adj(last):
                    if id not in visited:
                        ended = False
                        path.add_last(id)
                        visited[id] = visited[last]+1
        return visited


class Outcast(object):
    """Given a list of WordNet nouns x1, x2, ..., xn, which noun is the least related to the others"""
    def __init__(self, wordnet):
        """

        Args:
            wordnet (WordNet):
        """
        self._wordnet = wordnet

    def outcast(self, nouns):
        """
        given an array of WordNet nouns, return an outcast
        Args:
            nouns ([string]):

        Returns:
            (string)
        """
        import numpy as np
        d = np.zeros((len(nouns), len(nouns)))
        for i in range(len(nouns)-1):
            for j in range(i+1, len(nouns)):
                d[i][j] = self._wordnet.distance(nouns[i], nouns[j])
                d[j][i] = d[i][j]
        total_d = d.sum(axis=1)
        outcast = np.argmax(total_d)
        return nouns[outcast]
