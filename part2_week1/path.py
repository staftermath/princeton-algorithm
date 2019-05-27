from queue import Queue


class Paths(object):
    def __init__(self, G, s):
        self._marked = [False]*G.V
        self._edgeTo = [-1]*G.V
        self._s = s

    @property
    def s(self):
        return self._s

    @property
    def edgeTo(self):
        return self._edgeTo

    def pathTo(self, v):
        path = [v]
        while self.edgeTo[v] != -1:
            v = self.edgeTo[v]
            path.append(v)

        if v == -1:
            return None
        else:
            return path

    def hasPathTo(self, v):
        while self.edgeTo[v] != -1:
            v = self.edgeTo[v]
        return v == self.s


class DepthFirstPaths(Paths):
    def __init__(self, G, s):
        """

        Args:
            G (Graph):
            s (int):
        """
        super().__init__(G, s)
        self.dfs(G, s)

    def dfs(self, G, v):
        """

        Args:
            G (Graph):
            v (int):

        Returns:
            None
        """
        self._marked[v] = True
        for s in G.adj(v):
            if not self._marked[s]:
                self.dfs(G, s)
                self._edgeTo[s] = v


class BreadthFirstPaths(Paths):
    def __init__(self, G, s):
        """

        Args:
            G (Graph):
            s (int):
        """
        super().__init__(G, s)
        self.bfs(G, s)

    def bfs(self, G, v):
        """

        Args:
            G (Graph):
            v (int):

        Returns:
            None
        """
        self._marked[v] = True
        queue = Queue(G.V)
        queue.put(v)
        while not queue.empty():
            t = queue.get()
            for s in G.adj(t):
                if not self._marked[s]:
                    self._marked[s] = True
                    self._edgeTo[s] = t
                    queue.put(s)


class CC(object):

    def __init__(self, G):
        """

        Args:
            G (Graph):
        """
        self._marked = [False]*G.V
        self._id = list(range(G.V))
        self._count = 0
        for v in range(G.V):
            if not self._marked[v]:
                self.dfs(G, v)
                self._count += 1

    def dfs(self, G, v):
        """
        running depth-first search to find the components of each vertices.

        Args:
            G (Graph):
            v (v):

        Returns:

        """
        self._marked[v] = True
        self._id[v] = self._count
        for s in G.adj(v):
            if not self._marked[s]:
                self.dfs(G, s)

    def connected(self, v, w):
        """
        return if vertices v and w are connect by a path between them
        Args:
            v (int):
            w (int):

        Returns:
            (bool)
        """
        return self._id[v] == self._id[w]

    @property
    def count(self):
        """
        return number of connected components
        Returns:
            (int)
        """
        return self._count

    def id(self, v):
        """
        return the identifier of connected component to which vertex v belongs.
        Args:
            v (int):

        Returns:
            (int)

        """
        return self._id[v]