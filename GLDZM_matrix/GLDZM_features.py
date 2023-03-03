
import numpy as np


def small_distance_emphasis(matrix):
    size = np.size(matrix)
    total = 0
    for j in range(np.shape(matrix)[1]):

        column = 0
        for i in range(np.shape(matrix)[0]):
            column += matrix[i, j]

        column = column / (pow((j + 1), 2))
        total += column

    return total/size


def large_distance_emphasis(matrix):
    size = np.size(matrix)
    total = 0
    for j in range(np.shape(matrix)[1]):

        column = 0
        for i in range(np.shape(matrix)[0]):
            column += matrix[i, j]

        column = column * (pow((j + 1), 2))
        total += column

    return total / size


def low_grey_level_zone_emphasis(matrix):
    size = np.size(matrix)
    total = 0

    for i in range(np.shape(matrix)[0]):
        row = 0
        for j in range(np.shape(matrix)[1]):
            row += matrix[i, j]

        row = row / pow((i + 1), 2)
        total += row

    return total / size


def high_grey_level_zone_emphasis(matrix):
    size = np.size(matrix)
    total = 0

    for i in range(np.shape(matrix)[0]):
        row = 0
        for j in range(np.shape(matrix)[1]):
            row += matrix[i, j]

        row = row * pow((i + 1), 2)
        total += row

    return total / size


def small_distance_low_gray_level_emphasis(matrix):

    size = np.size(matrix)
    total = 0

    for i in range(np.shape(matrix)[0]):
        for j in range(np.shape(matrix)[1]):
            value = matrix[i, j]
            value = value / (pow((i + 1), 2) * pow((j + 1), 2))
            total += value

    return total / size


def small_distance_high_gray_level_emphasis(matrix):
    size = np.size(matrix)
    total = 0

    for i in range(np.shape(matrix)[0]):
        for j in range(np.shape(matrix)[1]):
            value = matrix[i, j]
            value = (pow((i + 1), 2) * value) / pow((j + 1), 2)
            total += value

    return total / size


def large_distance_low_gray_level_emphasis(matrix):

    size = np.size(matrix)
    total = 0

    for i in range(np.shape(matrix)[0]):
        for j in range(np.shape(matrix)[1]):
            value = matrix[i, j]
            value = (pow((j + 1), 2) * value) / pow((i + 1), 2)
            total += value

    return total / size


def large_distance_high_gray_level_emphasis(matrix):

    size = np.size(matrix)
    total = 0

    for i in range(np.shape(matrix)[0]):
        for j in range(np.shape(matrix)[1]):
            value = matrix[i, j]
            value = pow((j + 1), 2) * value * pow((i + 1), 2)
            total += value

    return total / size


def gray_level_non_uniformity(matrix):

    size = np.size(matrix)
    total = 0

    for i in range(np.shape(matrix)[0]):
        row = 0
        for j in range(np.shape(matrix)[1]):
            row += matrix[i, j]
        row = pow(row, 2)

        total += row

    return total / size


def normalised_gray_level_non_uniformity(matrix):
    size = np.size(matrix)
    total = 0

    for i in range(np.shape(matrix)[0]):
        row = 0
        for j in range(np.shape(matrix)[1]):
            row += matrix[i, j]
        row = pow(row, 2)

        total += row

    size = pow(size, 2)

    return total / size


def zone_distance_non_uniformity(matrix):
    size = np.size(matrix)
    total = 0

    for j in range(np.shape(matrix)[1]):
        column = 0
        for i in range(np.shape(matrix)[0]):
            column += matrix[i, j]

        column = column * column

        total += column

    return total / size


def normalised_zone_distance_non_uniformity(matrix):
    size = np.size(matrix)
    total = 0

    for j in range(np.shape(matrix)[1]):
        column = 0
        for i in range(np.shape(matrix)[0]):
            column += matrix[i, j]
        column = column * column

        total += column

    size = pow(size, 2)
    return total / size


def zone_percentage(matrix1, matrix2):
    from GLDZM import get_voxels_number
    volume = get_voxels_number(matrix1)
    size = np.size(matrix2)

    return size/volume


def pij_parameter(sij_value, Ns_value):
    return sij_value / Ns_value


def mi_parameter(matrix):
    shape = np.shape(matrix)
    mi_value = 0
    size = np.size(matrix)

    for i in range(shape[0]):
        for j in range(shape[1]):
            mi_value += ((i + 1) * pij_parameter(matrix[i, j], size))

    return mi_value


def gray_level_variance(matrix):
    shape = np.shape(matrix)
    size = np.size(matrix)
    variance_value = 0

    for i in range(shape[0]):
        for j in range(shape[1]):
            local_i = i + 1
            variance_value += (pow((local_i - mi_parameter(matrix)), 2)
                               * pij_parameter(matrix[i, j], size))

    return variance_value


def zone_distance_variance(matrix):
    shape = np.shape(matrix)
    size = np.size(matrix)
    variance_value = 0

    for i in range(shape[0]):
        for j in range(shape[1]):
            variance_value += (pow(((j + 1) - mi_parameter(matrix)), 2)
                               * pij_parameter(matrix[i, j], size))

    return variance_value


def get_logaritm(value):
    from math import log

    return log(value, 2)


def zone_distance_entropy(matrix):
    shape = np.shape(matrix)
    size = np.size(matrix)
    entropy_value = 0

    for i in range(shape[0]):
        for j in range(shape[1]):

            pij_value = pij_parameter(matrix[i, j], size)
            if pij_value != 0:
                entropy_value += (pij_value * get_logaritm(pij_value))

    return (-1) * entropy_value









