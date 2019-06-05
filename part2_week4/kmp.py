"""Implement Knuth-Morris-Pratt algorithm"""
import numpy as np


class KMP(object):
    """main KMP algorithm class"""
    def __init__(self, pattern, radix=256, ord_from=0):
        self._pattern = pattern
        self._R = radix
        self._dfa = np.zeros(shape=(self._R, len(pattern)), dtype="int")
        self._M = len(self._pattern)
        self._ord_from = ord_from
        lps = np.zeros(self._R, dtype="int")
        X = 0
        self._dfa[ord(self._pattern[0])-ord_from][0] = 1
        for i in range(1, self._M):
            ordinal = ord(self._pattern[i])-self._ord_from
            for j in range(self._R):
                self._dfa[j][i] = self._dfa[j][X]
            self._dfa[ordinal][i] = i+1
            X = self._dfa[ordinal][X]

    @property
    def length(self):
        return self._M

    def search(self, s):
        j = 0
        for i in range(len(s)):
            j = self._dfa[ord(s[i])-self._ord_from][j]
            if j == self._M:
                return i - j + 1
        return -1
