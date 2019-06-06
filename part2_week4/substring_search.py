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


class BM(object):
    """Implement Boyer-Moore Algorithm"""
    def __init__(self, pattern, radix=256, ord_from=0):
        self._pattern = pattern
        self._R = radix
        self._dfa = np.zeros(shape=(self._R, len(pattern)), dtype="int")
        self._M = len(self._pattern)
        self._ord_from = ord_from
        self._right = np.repeat(-1, self._R)
        for i in range(self._M):
            self._right[ord(pattern[i])-self._ord_from] = i

    @property
    def length(self):
        return self._M

    def search(self, s):
        i = 0
        while i <= len(s)-self._M:
            skip = 0
            for j in range(self._M-1, -1, -1):
                if self._pattern[j] != s[i+j]:
                    skip = max(1, j-self._right[ord(s[i+j])-self._ord_from])
            if skip == 0:
                return i
            i += skip
        return -1


class RabinKarp(object):
    """Implement Rabin Karp algorithm"""
    def __init__(self, pattern, radix=256, ord_from=0):
        self._pattern = pattern
        self._R = radix
        self._Q = self._longRandomPrime()
        self._M = len(self._pattern)
        self._ord_from = ord_from
        self._pathash = self.hash(self._pattern)
        self._RM = self._R**(self._M-1) % self._Q

    def _longRandomPrime(self):
        return 997

    def hash(self, s):
        """
        calculate the hash of string s
        Args:
            s (str):

        Returns:
            (int)
        """
        hash = 0
        for c in s:
            hash = (hash*self._R+ord(c)-self._ord_from) % self._Q
        return hash

    def search(self, s):
        """
        Find subpattern in s. if found, return the index of first char, otherwise return -1
        Args:
            s (str):

        Returns:
            (int)
        """
        if len(s) < self._M:
            return -1
        hash = self.hash(s[:self._M])
        if hash == self._pathash:
            return 0

        for i in range(self._M, len(s)):
            hash = (hash + self._Q - (((ord(s[i-self._M])-self._ord_from)*self._RM) % self._Q) % self._Q)
            hash = (hash*self._R + ord(s[i]) - self._ord_from) % self._Q
            if hash == self._pathash:
                return i-self._M+1
        return -1
