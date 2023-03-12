import numpy as np
"""
This file contain GLSZM matrix implementation.

TODO: Describe the way the matrix is created

Methods from this file are for ether creating GLSZM or adjust the created matrix

"""


def find_positions(my_matrix, x_position, y_position):
    """


    Parameters:
    -------------

    :param my_matrix: voxel's matrix
    :param x_position: voxel's x-xis position
    :param y_position: voxel's y-axis position
    :return: counter - number of voxels, excluded - voxel's that was already searched
    """

    # init essential values
    shape = np.shape(my_matrix)
    excluded = np.array([x_position, y_position])
    value = my_matrix[x_position, y_position]

    """
    This part determinate the range on which the Neighborhood voxels can be found
    x and y range are defined separately.
    Exception included - voxel is in the corner or on the side of matrix
    Maybe should consider separate this part into function
    """

    # X range
    if 0 < x_position < (shape[0] - 1):
        rows = np.array([x_position - 1, x_position, x_position + 1])
    elif 0 == x_position:
        rows = np.array([x_position, x_position + 1])
    elif x_position == (shape[0] - 1):
        rows = np.array([x_position - 1, x_position])

    # Y range
    if 0 < y_position < (shape[1] - 1):
        columns = np.array([y_position - 1, y_position, y_position + 1])
    elif 0 == y_position:
        columns = np.array([y_position, y_position + 1])
    elif y_position == (shape[1] - 1):
        columns = np.array([y_position - 1, y_position])

    # init the array with some value to be able to vstack later
    same_value_position = np.array([0, 0])

    counter = 1
    # loop in voxel's Neighborhood
    for i in rows:
        for j in columns:
            # skipping the voxel
            if np.array_equal([i, j], [x_position, y_position]):
                continue

            # finding voxel's with the same gray level value
            if my_matrix[i, j] == value:
                same_value_position = np.vstack([same_value_position, [i, j]])
                counter = counter + 1

    # if no same voxel with the same value was found
    if same_value_position.ndim == 1:
        same_value_position = np.array([])

    # if 1 or more was found
    if same_value_position.ndim == 2:
        # delete junk value
        same_value_position = np.delete(same_value_position, 0, 0)

        # looping every voxel
        for k in range(np.shape(same_value_position)[0]):
            # calling recurrence function
            counter, excluded = recurrence_search(my_matrix, counter, excluded, same_value_position[k, 0],
                                                  same_value_position[k, 1])
    # delete not unique value from excluded voxels
    if excluded.ndim == 2:
        new_excluded = np.unique(excluded, axis=0)
        difference = np.shape(excluded)[0] - np.shape(new_excluded)[0]
        counter = counter - difference
    else:
        new_excluded = excluded

    return counter, new_excluded


def recurrence_search(my_matrix, counter, excluded, x_position, y_position):
    """

    Function used for recurrence searched for voxels with the same value as given.

    Parameters:
    ------------------

    :param my_matrix: voxel's matrix
    :param counter: number of voxels found with the same value
    :param excluded: voxel's with the same value, that was already searched
    :param x_position: voxel's x-axis position
    :param y_position: voxel's y-axis position
    :return: number of voxels witch the same value, voxels already searched
    """

    # init initial parameters

    # copy counter value
    given_counter = counter
    # get the value of given voxel
    value = my_matrix[x_position, y_position]
    # update excluded
    excluded = np.vstack([excluded, [x_position, y_position]])

    shape = np.shape(my_matrix)

    # same as in find_positions method

    if 0 < x_position < (shape[0] - 1):
        rows = np.array([x_position - 1, x_position, x_position + 1])
    elif 0 == x_position:
        rows = np.array([x_position, x_position + 1])
    elif x_position == (shape[0] - 1):
        rows = np.array([x_position - 1, x_position])

    if 0 < y_position < (shape[1] - 1):
        columns = np.array([y_position - 1, y_position, y_position + 1])
    elif 0 == y_position:
        columns = np.array([y_position, y_position + 1])
    elif y_position == (shape[1] - 1):
        columns = np.array([y_position - 1, y_position])

    # init with some value to fit
    same_value_position = np.array([0, 0])

    # finding the same within voxel's range
    for i in rows:
        for j in columns:

            if np.array_equal([x_position, y_position], [i, j]):
                continue

            if check_array(np.array([i, j]), excluded):
                continue

            if my_matrix[i, j] == value:
                same_value_position = np.vstack([same_value_position, [i, j]])
                counter = counter + 1

    # deleting trash value
    same_value_position = np.delete(same_value_position, 0, 0)

    # checking if any new value was found
    if given_counter != counter:
        # loop and recursion
        for k in range(np.shape(same_value_position)[0]):
            counter, excluded = recurrence_search(my_matrix, counter, excluded, same_value_position[k, 0],
                                                  same_value_position[k, 1])

    return counter, excluded


def check_array(looking, given):
    """
    Helper method used to determinate if array is a part of different 2D array for example:
    if [2, 1] is in [[2, 2], [2, 1], [2, 0]] --> True
                             -----

     if [2, 1] is in [[2, 2], [1, 1], [2, 0]] --> False
           ^                ^
        looking             given

    Parameters:
    ----------------

    :param looking: 1 Dimension array
    :param given:  2 Dimnesion array
    :return: True if looking is in the 2D array and false otherwise
    """
    # loop through every position in given
    for position in range(np.shape(given)[0]):
        if np.array_equal(looking, given[position]):
            return True

    # if value wasn't found return false
    return False


def delete_from_array(array, element):
    """
    Helper method that finds first occurrence of given element and deletes it from array.

    Parameters:
    -------------

    :param array: group of elements
    :param element: element to be deleted
    :return: array without given element
    """

    # finding first position of given element
    index = find_index(array, element)
    # deleting it from array
    array = np.delete(array, index, 0)
    return array


def find_index(array, element):
    """
    Helper method that finds index of given element in given array
    If element is not found returns -1

    Parameters:
    ----------------

    :param array: group of elements
    :param element: element to which index is being found
    :return: index of element or -1
    """
    # linear search for element
    for i in range(np.shape(array)[0]):
        if np.array_equal(element, array[i]):
            return i
    # occurs if element is not found
    return -1


def create_coordinates(shape):
    coor_array = np.array([0, 0])

    for i in range(shape[0]):
        for j in range(shape[1]):
            coor_array = np.vstack([coor_array, [i, j]])

    coor_array = np.delete(coor_array, 0, 0)

    return coor_array


def aftercut(matrix):

    matrix_shape = np.shape(matrix)
    new_matrix = np.zeros([matrix_shape[0] - 1, matrix_shape[1] - 1])

    for i in range(1, np.shape(matrix)[0]):
        for j in range(1, np.shape(matrix)[1]):
            new_matrix[i - 1, j - 1] = matrix[i, j]

    return new_matrix


def GLSZM_matrix(matrix, gray_level=8):
    max_zone_size = 600
    matrix_shape = np.shape(matrix)
    output_matrix = np.zeros([gray_level, max_zone_size])
    every_coordinates = create_coordinates(matrix_shape)
    zeros_cooridnates = find_zeros(matrix, every_coordinates)

    if zeros_cooridnates.ndim == 2:
        for i in range(np.shape(zeros_cooridnates)[0]):
            every_coordinates = delete_from_array(every_coordinates, zeros_cooridnates[i])
    elif zeros_cooridnates.ndim == 1:
        every_coordinates = delete_from_array(every_coordinates, zeros_cooridnates)

    while np.any(every_coordinates):
        zone_size, excluded = find_positions(matrix, every_coordinates[0][0], every_coordinates[0][1])
        output_matrix[matrix[every_coordinates[0][0], every_coordinates[0][1]], zone_size] = output_matrix[matrix[
            every_coordinates[0][0], every_coordinates[0][1]], zone_size] + 1

        if excluded.ndim == 2:
            for i in range(np.shape(excluded)[0]):
                every_coordinates = delete_from_array(every_coordinates, excluded[i])

        elif excluded.ndim == 1:
            every_coordinates = delete_from_array(every_coordinates, excluded)

    return aftercut(output_matrix)


def find_zeros(matrix, some_array):

    zeros_coordinates = np.array([0, 0])
    for i in range(np.shape(some_array)[0]):
        if matrix[some_array[i][0], some_array[i][1]] == 0:
            zeros_coordinates = np.vstack([zeros_coordinates, some_array[i]])

    zeros_coordinates = np.delete(zeros_coordinates, 0, 0)

    return zeros_coordinates


def get_voxels_number(matrix):
    shape = np.shape(matrix)
    number = 0

    if matrix.ndim == 2:
        number = shape[0] * shape[1]
    if matrix.ndim == 3:
        number = shape[0] * shape[1] * shape[2]

    return number


def delete_unused_columns(matrix):
    minimal = 0
    for i in range(np.shape(matrix)[1] - 1, 0, -1):
        if np.any(matrix[:, i]):
            minimal = i
            break

    if minimal != 0:
        new_matrix = np.zeros([np.shape(matrix)[0], minimal + 1])

        for i in range(np.shape(matrix)[0]):
            for j in range(minimal + 1):
                new_matrix[i, j] = matrix[i, j]

    return new_matrix
