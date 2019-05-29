import pytest
import os
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal


TEST_NAME = "princeton_algoritm_part2_week2_seam_carving"


@pytest.fixture()
def tmp_folder(tmpdir):
    if not tmpdir.join(TEST_NAME).exists():
        tmpdir.mkdir(TEST_NAME)
    return tmpdir.join(TEST_NAME)


@pytest.fixture()
def resources():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")


@pytest.fixture()
def energy_4x6():
    return np.array([[1000.00,  1000.00, 1000.00, 1000.00],
                     [1000.00,   275.66,  173.21, 1000.00],
                     [1000.00,   173.21,  321.01, 1000.00],
                     [1000.00,   171.80,  195.63, 1000.00],
                     [1000.00,   270.93,  188.15, 1000.00],
                     [1000.00,  1000.00, 1000.00, 1000.00]])


@pytest.fixture()
def picture_4x6(resources):
    from part2_week2.seam_carving import Picture
    path_png_4x6 = os.path.join(resources, "4x6.png")
    return Picture(path_png_4x6)


def test_seam_carving_energy(picture_4x6, energy_4x6):
    from part2_week2.seam_carving import SeamCarver
    seam_carver = SeamCarver(picture_4x6)
    assert_array_almost_equal(energy_4x6, seam_carver._energy, decimal=2)


@pytest.fixture()
def seam_carver_4x6(picture_4x6):
    from part2_week2.seam_carving import SeamCarver
    seam_carver = SeamCarver(picture_4x6)
    return seam_carver


vertical_seam = [2, 2, 1, 1]
horizontal_seam = [2, 2, 1, 1, 2, 2]


def test_seam_carver_find_vertical_seam(seam_carver_4x6):
    result = seam_carver_4x6.findVerticalSeam()
    assert vertical_seam == result


def test_seam_carver_find_horizontal_seam(seam_carver_4x6):
    result = seam_carver_4x6.findHorizontalSeam()
    assert horizontal_seam == result


@pytest.fixture()
def raw_picture():
    return np.array([[[186,  40,  23], [123, 181, 202], [190, 148,  10], [ 20,   7, 162]],
                     [[ 35, 169, 100], [203,  13, 166], [245, 171, 124], [209,  68, 160]],
                     [[129, 137,  60], [220,  71, 103], [206, 219, 157], [ 26, 233,  41]],
                     [[ 93,  71,  65], [119,  41, 176], [118,  83, 231], [208,  33,  14]],
                     [[101, 108, 129], [207,  60, 133], [220, 161, 179], [215, 141, 196]],
                     [[143, 126,  53], [220, 245, 222], [178, 156, 105], [108, 113,   5]]])


def test_seam_carver_remove_vertical_seam(seam_carver_4x6):
    expected = np.array([[[186,  40,  23], [123, 181, 202], [190, 148,  10], [ 20,   7, 162]],
                         [[ 35, 169, 100], [203,  13, 166], [206, 219, 157], [ 26, 233,  41]],
                         [[ 93,  71,  65], [119,  41, 176], [118,  83, 231], [208,  33,  14]],
                         [[101, 108, 129], [207,  60, 133], [220, 161, 179], [215, 141, 196]],
                         [[143, 126,  53], [220, 245, 222], [178, 156, 105], [108, 113,   5]]])
    seam_carver_4x6.removeVerticalSeam(vertical_seam)
    assert_array_equal(expected, seam_carver_4x6._picture)
    assert seam_carver_4x6.height == 4
    assert seam_carver_4x6.width == 5


def test_seam_carver_remove_horizontal_seam(seam_carver_4x6):
    # [2, 2, 1, 1, 2, 2]
    expected = np.array([[[186,  40,  23], [123, 181, 202], [ 20,   7, 162]],
                         [[ 35, 169, 100], [203,  13, 166], [209,  68, 160]],
                         [[129, 137,  60], [206, 219, 157], [ 26, 233,  41]],
                         [[ 93,  71,  65], [118,  83, 231], [208,  33,  14]],
                         [[101, 108, 129], [207,  60, 133], [215, 141, 196]],
                         [[143, 126,  53], [220, 245, 222], [108, 113,   5]]])
    seam_carver_4x6.removeHorizontalSeam(horizontal_seam)
    assert_array_equal(expected, seam_carver_4x6._picture)
    assert seam_carver_4x6.height == 3
    assert seam_carver_4x6.width == 6


@pytest.fixture()
def surfing_png(tmp_folder):
    import urllib.request
    url = "http://coursera.cs.princeton.edu/algs4/assignments/HJoceanSmall.png"
    path = tmp_folder.join("raw.png")
    urllib.request.urlretrieve(url, str(path))
    return str(path)


@pytest.mark.skip
def test_remove_horizontal_seam_many_times_and_save(tmp_folder, surfing_png):
    from part2_week2.seam_carving import SeamCarver, Picture
    path = tmp_folder.join("output_file.png")
    seam_carver = SeamCarver(Picture(surfing_png))
    for i in range(100):
        print("Iteration: {}".format(i))
        seam_carver.removeHorizontalSeam(seam_carver.findHorizontalSeam())
    print(str(path))
    seam_carver.save_picture(str(path))
