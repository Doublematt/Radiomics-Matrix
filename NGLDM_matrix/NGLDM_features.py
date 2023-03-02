import numpy as np


def low_gray_level_count_emphasis(matrix):
    import numpy as np

    # variable for matrix size and shape
    size = np.size(matrix)
    shape = np.shape(matrix)

    # sum is a sum of ever row (sj) divided by row's dependence squared
    sum = 0

    # loop for every row
    for i in range(shape[0]):

        # init sj value with 0
        row = 0

        # getting every element in a specific row
        for j in range(shape[1]):
            # adding every value from a row
            row += matrix[i, j]

        # dividing sj by squared dependence
        row = row / ((i + 1) * (i + 1))

        # adding row value to sum
        sum += row

    # dividing value by the number of values in matrix
    return sum / size


def high_gray_level_count_emphasis(matrix):
    import numpy as np

    # variable for matrix size and shape
    size = np.size(matrix)
    shape = np.shape(matrix)

    # sum is a sum of ever row (sj) multiplied by row's dependence squared
    sum = 0

    # loop for every row
    for i in range(shape[0]):

        # init sj value with 0
        row = 0

        # getting every element in a specific row
        for j in range(shape[1]):
            # adding every value from a row
            row += matrix[i, j]

        # multiplying si by squared dependence
        row = row * ((i + 1) * (i + 1))

        # adding row value to sum
        sum += row

    # dividing value by the number of values in matrix
    return sum / size


def low_dependence_emphasis(matrix):
    # sum of values with discrete gray level
    size = np.size(matrix)
    shape = np.shape(matrix)
    sum_col = 0

    for i in range(1, shape[1]):
        column = 0

        for j in range(shape[0]):
            column += matrix[j, i]

        column = column / (i * i)
        sum_col += column

    return sum_col / size


def high_dependence_emphasis(matrix):
    # sum of values with discrete gray level
    size = np.size(matrix)
    shape = np.shape(matrix)
    sum_col = 0

    for i in range(1, shape[1]):
        column = 0

        for j in range(shape[0]):
            column += matrix[j, i]

        column = column * (i * i)
        sum_col += column

    return sum_col / size


def low_dependence_low_gray_level_emphasis(matrix):
    size = np.size(matrix)
    shape = np.shape(matrix)
    all_values = 0

    for i in range(shape[0]):
        for j in range(1, shape[1]):
            all_values += (matrix[i, j] /
                           (pow(i + 1, 2) * pow(j, 2)))

    return all_values / size


def low_dependence_high_gray_level_emphasis(matrix):
    size = np.size(matrix)
    shape = np.shape(matrix)
    all_values = 0

    for i in range(shape[0]):
        for j in range(1, shape[1]):
            all_values += ((matrix[i, j] * pow(i + 1, 2)) /
                            pow(j, 2))

    return all_values / size



def high_dependence_low_gray_level_emphasis(matrix):
    size = np.size(matrix)
    shape = np.shape(matrix)
    all_values = 0

    for i in range(shape[0]):
        for j in range(1, shape[1]):
            all_values += (
                    (matrix[i, j] * pow(j, 2)) /
                    pow(i + 1, 2))

    return all_values / size


def high_dependence_high_gray_level_emphasis(matrix):
    size = np.size(matrix)
    shape = np.shape(matrix)
    all_values = 0

    for i in range(shape[0]):
        for j in range(1, shape[1]):
            all_values += (
                    matrix[i, j] * pow(j, 2) * pow(i + 1, 2))

    return all_values / size


def gray_level_non_uniformity(matrix):
    import numpy as np

    # variable for matrix size and shape
    size = np.size(matrix)
    shape = np.shape(matrix)

    # sum is a sum of ever row (sj) multiplied by row's dependence squared
    rows_sum = 0

    # loop for every row
    for i in range(shape[0]):

        # init sj value with 0
        row = 0

        # getting every element in a specific row
        for j in range(shape[1]):
            # adding every value from a row
            row += matrix[i, j]

        row = pow(row, 2)

        # adding row value to sum
        rows_sum += row

    # dividing value by the number of values in matrix
    return rows_sum / size


def normalised_gray_level_non_uniformity(matrix):
    import numpy as np

    # variable for matrix size and shape
    size = np.size(matrix)
    size = pow(size, 2)
    shape = np.shape(matrix)

    # sum is a sum of ever row (sj) multiplied by row's dependence squared
    rows_sum = 0

    # loop for every row
    for i in range(shape[0]):

        # init sj value with 0
        row = 0

        # getting every element in a specific row
        for j in range(shape[1]):
            # adding every value from a row
            row += matrix[i, j]

        row = pow(row, 2)

        # adding row value to sum
        rows_sum += row

    # dividing value by the number of values in matrix
    return rows_sum / size


def dependence_count_non_uniformity(matrix):
    # sum of values with discrete gray level
    size = np.size(matrix)
    shape = np.shape(matrix)
    sum_col = 0

    for i in range(1, shape[1]):
        column = 0

        for j in range(shape[0]):
            column += matrix[j, i]

        sum_col += pow(column, 2)

    return sum_col / size


def normalised_dependence_count_non_uniformity(matrix):
    # sum of values with discrete gray level
    size = np.size(matrix)
    shape = np.shape(matrix)
    size = pow(size, 2)
    sum_col = 0

    for i in range(1, shape[1]):
        column = 0

        for j in range(shape[0]):
            column += matrix[j, i]

        sum_col += pow(column, 2)

    return sum_col / size


# parameters!!

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


def dependence_count_variance(matrix):
    shape = np.shape(matrix)
    size = np.size(matrix)
    variance_value = 0

    for i in range(shape[0]):
        for j in range(shape[1]):
            variance_value += (pow((j - mi_parameter(matrix)), 2)
                               * pij_parameter(matrix[i, j], size))

    return variance_value


def get_logaritm(value):
    from math import log

    return log(value, 2)


def dependence_count_entropy(matrix):
    shape = np.shape(matrix)
    size = np.size(matrix)
    entropy_value = 0

    for i in range(shape[0]):
        for j in range(shape[1]):

            pij_value = pij_parameter(matrix[i, j], size)
            if pij_value != 0:
                entropy_value += (pij_value * get_logaritm(pij_value))

    return (-1) * entropy_value


def dependence_count_energy(matrix):
    shape = np.shape(matrix)
    size = np.size(matrix)
    energy_value = 0

    for i in range(shape[0]):
        for j in range(shape[1]):
            pji_value = pij_parameter(matrix[i, j], size)

            energy_value += pow(pji_value, 2)

    return energy_value
