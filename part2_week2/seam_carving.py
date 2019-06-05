"""
Implement Seam Carver class API
"""
from PIL import Image
import numpy as np

from part2_week2.sp import DirectedEdge, EdgeWeightedDigraph, AcyclicSP


class RGB(object):
    """color of pixel represented by RGB"""
    def __init__(self, r, g, b):
        if 0 <= r <= 255:
            self._r = r
        else:
            raise ValueError("R must be between 0 and 255")

        if 0 <= g <= 255:
            self._g = g
        else:
            raise ValueError("G must be between 0 and 255")

        if 0 <= b <= 255:
            self._b = b
        else:
            raise ValueError("B must be between 0 and 255")

    @property
    def R(self):
        return self._r

    @property
    def G(self):
        return self._g

    @property
    def B(self):
        return self._b

    def __str__(self):
        return "R: {}, G: {}, B: {}".format(self.R, self.G, self.B)

    def __eq__(self, other):
        if isinstance(other, RGB):
            return self.R == other.R and self.G == other.G and self.B == other.B

        raise NotImplementedError("Cannot compare with non RGB type")


class Picture(object):
    """picture class that stores information of picture"""
    def __init__(self, file):
        self._im2arr = np.array(Image.open(file)).astype("int")

    def getRGB(self, col, row):
        return self._im2arr[row, col]

    def height(self):
        return self._im2arr.shape[1]

    def width(self):
        return self._im2arr.shape[0]

    def setRGB(self, col, row, rgb):
        """

        Args:
            col (int):
            row (int):
            rgb (numpy.array):

        Returns:
            None
        """
        self._im2arr[row, col] = rgb

    @property
    def im2arr(self):
        return self._im2arr


class SeamCarver(object):
    """Seam Carver main class"""
    def __init__(self, picture):
        """

        Args:
            picture (Picture):
        """
        self._picture = picture.im2arr
        self._width, self._height, _ = self._picture.shape
        self._energy = None
        self._calculate_energy()

    def _calculate_energy(self):
        self._energy = np.ones((self.width, self.height))*1000
        x_gradient = np.sum(np.square(np.roll(self._picture, 1, axis=0) - np.roll(self._picture, -1, axis=0)), axis=2)
        y_gradient = np.sum(np.square(np.roll(self._picture, 1, axis=1) - np.roll(self._picture, -1, axis=1)), axis=2)
        central = np.sqrt(x_gradient + y_gradient)
        self._energy[1:(self.width-1), 1:(self.height-1)] = central[1:(self.width-1), 1:(self.height-1)]

    def picture(self):
        return self._picture

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def energy(self, x, y):
        return self._energy[x, y]

    def findHorizontalSeam(self):
        """

        Returns: Indices of horizontal seam
            (list)
        """
        return self._construct_sp_from_matrix(self._energy)

    def findVerticalSeam(self):
        """

        Returns: Indices of vertical seam
            (list)
        """
        return self._construct_sp_from_matrix(self._energy.transpose())

    def removeHorizontalSeam(self, seam):
        horizontal_seam = self.findHorizontalSeam()
        # picture is transposed in array
        for i, v in enumerate(horizontal_seam):
            self._picture[i, v:(self._height-1)] = self._picture[i, (v+1):self._height]
        self._picture = self._removeLastCol(self._picture)
        self._height -= 1
        self._calculate_energy()

    def removeVerticalSeam(self, seam):
        vertical_seam = self.findVerticalSeam()
        # picture is transposed in array
        for i, v in enumerate(vertical_seam):
            self._picture[v:(self._width-1), i] = self._picture[(v+1):self._width, i]
        self._picture = self._removeLastRow(self._picture)
        self._width -= 1
        self._calculate_energy()

    def save_picture(self, file):
        im = Image.fromarray(self._picture.astype("uint8"))
        im.save(file)

    @staticmethod
    def _removeLastCol(arr):
        """
        remove last column of an array
        Args:
            arr (numpy.ndarray): a 3 dimensional numpy array

        Returns:
            (numpy.ndarray)
        """
        height, width, _ = arr.shape
        return arr[:, :(width-1), :]

    @staticmethod
    def _removeLastRow(arr):
        """
        remove last row of an array
        Args:
            arr (numpy.ndarray): a 3 dimensional numpy array

        Returns:
            (numpy.ndarray)
        """
        height, width, _ = arr.shape
        return arr[:(height-1), :, :]

    def _construct_vertical_dag(self):
        total_nodes = self.height*self.width+2
        energy = self._energy.transpose()
        shape = energy.shape

        ewg = EdgeWeightedDigraph(v=total_nodes)
        # first row
        for j in range(1, self.width-1):
            from_node = 0
            ewg.addEdge(DirectedEdge(from_node,
                                     j+self.width,
                                     energy[np.unravel_index(j+self.width, shape)]))
        # intermediate rows
        for i in range(1, self.height-2):
            for j in range(1, self.width-1):
                from_node = i*self.width+j
                for to_node in (from_node+self.width-1, from_node+self.width, from_node+self.width+1):
                    ewg.addEdge(DirectedEdge(from_node,
                                             to_node,
                                             energy[np.unravel_index(to_node, shape)]))

        # last row
        for j in range(1, self.width-1):
            from_node = (self.height-2)*self.width+j
            ewg.addEdge(DirectedEdge(from_node,
                                     total_nodes-1,
                                     0))

        return ewg

    @staticmethod
    def _construct_sp_from_matrix(matrix):
        shape = matrix.shape
        height, width = shape
        total_nodes = height*width+2

        ewg = EdgeWeightedDigraph(v=total_nodes)
        # first row
        for j in range(1, width-1):
            from_node = 0
            ewg.addEdge(DirectedEdge(from_node,
                                     j + width,
                                     matrix[np.unravel_index(j + width, shape)]))
        # intermediate rows
        for i in range(1, height-2):
            for j in range(1, width-1):
                from_node = i*width+j
                for to_node in (from_node+width-1, from_node+width, from_node+width+1):
                    ewg.addEdge(DirectedEdge(from_node,
                                             to_node,
                                             matrix[np.unravel_index(to_node, shape)]))

        # last row
        for j in range(1, width-1):
            from_node = (height-2)*width+j
            ewg.addEdge(DirectedEdge(from_node,
                                     total_nodes-1,
                                     0))

        acyclic_sp = AcyclicSP(ewg, 0)
        edges = acyclic_sp.pathTo(height*width+1)
        result = [np.unravel_index(x, shape)[1] for x in edges[1:-1]]
        return [result[0]]+result+[result[-1]]
