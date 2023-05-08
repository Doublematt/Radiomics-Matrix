import numpy as np


def coarsennes(matrix):

    sum = 0
    for i in range(np.shape(matrix)[0]):

        tmp = matrix[i, 1] * matrix[i, 2]
        sum += tmp

    return 1 / sum


def calculate_ngp(matrix):

    counter = 0
    for i in range(np.shape(matrix)[0]):

        tmp = matrix[i, 1]
        if tmp != 0:
            counter += 1

    return counter


def calculate_nvc(matrix):
    nvc = 0
    for i in range(np.shape(matrix)[0]):

        tmp = matrix[i, 0]
        nvc += tmp

    return nvc


def contrast(matrix):
    from math import pow

    ngp = calculate_ngp(matrix)
    nvc = calculate_nvc(matrix)
    loop_range = np.shape(matrix)[0]

    first_part = 1 / (ngp * (ngp - 1))

    second_part = 0
    for i in range(loop_range):
        i_var = i + 1

        for j in range(loop_range):
            j_var = j + 1
            tmp = pow(i_var * j_var, 2) * matrix[i, 1] * matrix[j, 1]

            second_part += tmp

    third_part = 0
    for i in range(loop_range):
        tmp = matrix[i, 2]
        third_part += tmp

    third_part = (1 / nvc) * third_part

    return first_part * second_part * third_part


def busyness(matrix):

    loop_range = np.shape(matrix)[0]
    upper_part = 0

    for i in range(loop_range):
        pi = matrix[i, 1]
        si = matrix[i, 2]
        upper_part += (pi * si)

    lower_part = 0
    for j in range(loop_range):
        j_var = j + 1
        for k in range(loop_range):
            k_var = k + 1
            tmp = (j_var * matrix[j, 1]) - (k_var * matrix[k, 1])
            tmp = abs(tmp)
            lower_part += tmp

    return upper_part / lower_part

def check_complexity(matrix):

    for i in range(np.shape(matrix)[0]):
        if matrix[i, 1] != 0:
            return False

    return True


def complexity(matrix):

    if check_complexity(matrix):
        return 0

    loop_range = np.shape(matrix)[0]
    second_part = 0

    first_part = 1 / calculate_nvc(matrix)

    for i in range(loop_range):
        i_var = i + 1
        for j in range(loop_range):
            j_var = j + 1
            tmp = (matrix[i, 1] * matrix[i, 2] + matrix[j, 1] * matrix[j, 2]) / (matrix[i, 1] + matrix[j, 1])
            tmp = tmp * abs(i_var - j_var)
            second_part += tmp

    return first_part * second_part


def strenght(matrix):

    from math import pow

    loop_range = np.shape(matrix)[0]
    top_part = 0
    bottom_part = 0

    for i in range(loop_range):
        i_var = i + 1
        for j in range(loop_range):
            j_var = j + 1
            tmp = matrix[i, 1] + matrix[j, 1]
            tmp2 = pow(i_var - j_var, 2)
            tmp = tmp * tmp2
            top_part += tmp

    for k in range(loop_range):
        bottom_part += matrix[k, 2]

    return top_part / bottom_part



