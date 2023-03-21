"""
This file contain GLDZM matrix implementation.

 Describe the way the matrix is created

Methods from this file are for ether creating GLDZM or adjust the created matrix

"""

import numpy as np


def get_gray_level_diff(position_x, position_y, matrix):
    """
    Method used to obtain smallest gray level difference between given voxel and it's neighbourhood

    Parameters
    ----------------
    :param position_x: voxel's x-axis position
    :param position_y: voxel's y-axis position
    :param matrix: voxel's matrix
    :return: scanned - voxel's wth certain given value coonected together, border - voxel's neighbourhood
    """
    # init basic values
    voxel_value = matrix[position_x, position_y]
    matrix_shape = np.shape(matrix)
    new_same_value = np.array([0, 0])

    # getting position around voxel
    zone = get_zone(position_x, position_y, matrix_shape[0] - 1, matrix_shape[1] - 1)

    # checking if any voxel has the same gray level
    for i in range(np.shape(zone)[0]):

        if matrix[zone[i, 0], zone[i, 1]] == voxel_value:
            # stacking voxels with the same gray level
            new_same_value = np.vstack([new_same_value, zone[i]])

    # deleting trash value
    new_same_value = np.delete(new_same_value, 0, 0)
    # shaping the border
    border = get_positions(position_x, position_y, matrix_shape[0] - 1, matrix_shape[1] - 1)

    # copied border
    new_border = border

    # deleting voxel's with the same gray level value from border
    for j in range(np.shape(border)[0]):
        if check_array(border[j], new_same_value):
            new_border = np.delete(border, j, 0)

    # border update
    border = new_border
    # init variable for voxel's already checked
    scanned = np.array([position_x, position_y])

    # if there are any same value voxel's go reccurence
    if np.any(new_same_value):

        # only one
        if new_same_value.ndim == 1:
            scanned, border = scann_further(new_same_value, border, scanned, matrix_shape, matrix)

        # many
        elif new_same_value.ndim == 2:
            for i in range(np.shape(new_same_value)[0]):
                scanned, border = scann_further(new_same_value[i], border, scanned, matrix_shape, matrix)

    # border update
    counter = 0
    new_border = border
    for i in range(np.shape(border)[0]):
        if check_array(border[i], scanned):
            new_border = np.delete(new_border, i - counter, 0)
            counter += 1

    return scanned, np.unique(new_border, axis=0)


def get_positions(position_x, position_y, max_x, max_y):
    """
    Method used to obtain voxel's neighbourhood.

    Paramters:
    ---------------------
    :param position_x: voxel's x-axis position
    :param position_y: voxel's y-axis position
    :param max_x: max x-axis range in given matrix
    :param max_y: max y-axis range in given matrix
    :return: set of coordinates of neighbourhood voxels
    """
    # init empty array
    range_x = np.array([])
    range_y = np.array([])

    # getting the neighbourhood range
    if position_x != max_x and position_x != 0:
        range_x = np.array([position_x - 1, position_x, position_x + 1])
    elif position_x == 0:
        range_x = np.array([position_x, position_x + 1])
    elif position_x == max_x:
        range_x = np.array([position_x - 1, position_x])

    if position_y != max_y and position_y != 0:
        range_y = np.array([position_y - 1, position_y, position_y + 1])
    elif position_y == 0:
        range_y = np.array([position_y, position_y + 1])
    elif position_y == max_y:
        range_y = np.array([position_y - 1, position_y])

    # init positions
    positions = np.array([0, 0])

    # 2D loop creating set of coordinates
    for i in range_x:
        for j in range_y:
            if np.array_equal([i, j], [position_x, position_y]):
                continue
            positions = np.vstack([positions, [i, j]])

    # trash value delete
    positions = np.delete(positions, 0, 0)

    return positions


def get_zone(position_x, position_y, max_x, max_y):
    """
    Method used to obtain voxel's zone

    Paramters:
    ---------------------
    :param position_x: voxel's x-axis position
    :param position_y: voxel's y-axis position
    :param max_x: max x-axis range in given matrix
    :param max_y: max y-axis range in given matrix
    :return: set of coordinates of zone voxels
    """
    # init empty range arrays
    x_zone = np.array([])
    y_zone = np.array([])

    # getting the zone
    if position_x != 0 and position_x != max_x:
        x_zone = np.array([[position_x - 1, position_y], [position_x + 1, position_y]])
    elif position_x == 0:
        x_zone = np.array([[position_x + 1, position_y]])
    elif position_x == max_x:
        x_zone = np.array([[position_x - 1, position_y]])

    if position_y != 0 and position_y != max_y:
        y_zone = np.array([[position_x, position_y - 1], [position_x, position_y + 1]])
    elif position_y == 0:
        y_zone = np.array([[position_x, position_y + 1]])
    elif position_y == max_y:
        y_zone = np.array([[position_x, position_y - 1]])

    positions = np.vstack([x_zone, y_zone])

    return positions


def scann_further(position, border, scanned, matrix_shape, matrix):
    """
    Recurrence method used to obtain further same value voxel's and update neighoburhood

    Parameters:
    ----------------
    :param position: voxel's x and y position
    :param border: voxel or voxels neighbourhood
    :param scanned: already checked voxels
    :param matrix_shape: you should know it
    :param matrix: voxel's matrix
    :return: updated scanned and border
    """

    # init parameters and update
    scanned = np.vstack([scanned, position])
    value = matrix[position[0], position[1]]
    zone = get_zone(position[0], position[1], matrix_shape[0] - 1, matrix_shape[1] - 1)
    new_same_value = np.array([1000, 1000])

    # look for same gray lavel in the zone
    for i in range(np.shape(zone)[0]):
        # checking if voxel has the same gray level
        if matrix[zone[i, 0], zone[i, 1]] == value:
            new_same_value = np.vstack([new_same_value, zone[i]])

    # delete trash value
    new_same_value = np.delete(new_same_value, 0, 0)

    # init the border of current voxel
    current_border = get_positions(position[0], position[1], matrix_shape[0] - 1, matrix_shape[1] - 1)

    # updating the border

    for j in range(np.shape(current_border)[0]):
        if not check_array(current_border[j], border):
            border = np.vstack([border, current_border])

    # checking if there is any more same value voxels

    for i in range(np.shape(new_same_value)[0]):
        if not check_array(new_same_value[i], scanned):
            scanned, border = scann_further(new_same_value[i], border, scanned, matrix_shape, matrix)

    # out of recursion statement
    return scanned, border


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


def GLDZM_matrix(matrix, gray_level, max_zone):
    """
    Main method for this file. Used to create gldzm matrix.

    Parameters:
    --------------------
    :param matrix: gray level matrix
    :param gray_level: number of gray levels
    :param max_zone: max zone value
    :return: gldzm matrix
    """

    # init variables
    output = np.zeros([gray_level, max_zone])
    x_shape, y_shape = np.shape(matrix)
    every_coordinates = np.array([1000, 1000])

    # get every_coordinates of every voxel in given matrix
    for i in range(x_shape):
        for j in range(y_shape):
            every_coordinates = np.vstack([every_coordinates, [i, j]])

    # delete trash value
    every_coordinates = np.delete(every_coordinates, 0, 0)

    # finding zeros in given matrix
    zeros_coordinates = find_zeros(matrix, every_coordinates)

    # deleting zeros from coordinates
    if zeros_coordinates.ndim == 2:
        for i in range(np.shape(zeros_coordinates)[0]):
            every_coordinates = delete_from_array(every_coordinates, zeros_coordinates[i])
    elif zeros_coordinates.ndim == 1:
        every_coordinates = delete_from_array(every_coordinates, zeros_coordinates)

    # while every coordinate wasn't checked
    while np.any(every_coordinates):

        scanned, border = get_gray_level_diff(every_coordinates[0, 0], every_coordinates[0, 1], matrix)

        # getting the voxel value based on scanned length
        if scanned.ndim == 1:
            voxel_value = matrix[scanned[0], scanned[1]]
        elif scanned.ndim == 2:
            voxel_value = matrix[scanned[0, 0], scanned[0, 1]]

        # calculating smallest difference
        smallest_voxel_diff = get_smalest_difference(voxel_value, border, matrix)
        # gldzm matrix update
        output[voxel_value, smallest_voxel_diff] += 1

        # updating the coordinates set
        if scanned.ndim == 2:
            for i in range(np.shape(scanned)[0]):
                every_coordinates = delete_from_array(every_coordinates, scanned[i])
        if scanned.ndim == 1:
            every_coordinates = delete_from_array(every_coordinates, scanned)

    return delete_0_column_row(output)


def find_zeros(matrix, my_coordinates_array):
    """
    Method to find zero values within a matrix

    Parameters:
    --------------

    :param matrix: initial matrix with gray level values
    :param my_coordinates_array: array of coordinates
    :return: array of zeros coordinates
    """
    # init variable
    zeros_coordinates = np.array([0, 0])

    # look for 0 and add their coordinates to array
    for i in range(np.shape(my_coordinates_array)[0]):
        if matrix[my_coordinates_array[i][0], my_coordinates_array[i][1]] == 0:
            zeros_coordinates = np.vstack([zeros_coordinates, my_coordinates_array[i]])

    zeros_coordinates = np.delete(zeros_coordinates, 0, 0)

    return zeros_coordinates


def delete_0_column_row(matrix):
    """
    Method used to delete first column and first row.
    This needs to be done, because the output matrix has to match GLSZM matrix which starts with 1 not 0

    Parameters:
    --------------

    :param matrix: matrix to be cut
    :return: matrix starting with 1
    """
    # get the matrix shape
    matrix_shape = np.shape(matrix)
    # make an empty array for values from matrix
    new_matrix = np.zeros([matrix_shape[0] - 1, matrix_shape[1] - 1])

    # rewrite values from given matrix to the new one
    # starting with position 1
    for i in range(1, np.shape(matrix)[0]):
        for j in range(1, np.shape(matrix)[1]):
            new_matrix[i - 1, j - 1] = matrix[i, j]

    return new_matrix


def get_smalest_difference(value, positions, matrix):
    """
    Method used to obtain smallest difference between voxel and it's neighbourhood

    Parameters:
    ------------------
    :param value: voxel's gray level value
    :param positions: voxel's neighbourhood
    :param matrix: voxel's matrix
    :return: smallest gray level difference
    """

    # load the first value
    minimum = abs(value - matrix[positions[0,0], positions[0, 1]])

    # look in every other position
    for i in range(1, np.shape(positions)[0]):

        # rule of the matrix, prevents dividing by 0
        if minimum == 0:
            minimum = 1

        if minimum == 1:
            break

        tmp = abs(value - matrix[positions[i, 0], positions[i, 1]])
        if tmp < minimum:
            minimum = tmp

    # return minimal difference between voxels
    return minimum


def delete_unused_columns(matrix):
    """
        Deletes columns filed with 0.
        Nessesery because the max zone size is hardcoded

        Parameters:
        --------------

        :param matrix: GLSZM matrix
        :return: GLSZM matrix without 0-filled columns
    """

    new_matrix = matrix
    minimal = 0
    # looping backwards from last column to first
    for i in range(np.shape(matrix)[1] - 1, 0, -1):
        # if column has no-zero value it stops and breaks loop
        if np.any(matrix[:, i]):
            minimal = i
            break

    # if matrix has any no-zero columns
    # create new matrix of given size
    if minimal != -1:
        new_matrix = np.zeros([np.shape(matrix)[0], minimal + 1])

        # rewrite the matrix
        for i in range(np.shape(matrix)[0]):
            for j in range(minimal + 1):
                new_matrix[i, j] = matrix[i, j]

    return new_matrix


def get_voxels_number(matrix):
    """
    Method used for feature - zone_percentage

    Parameters:
    -----------

    :param matrix: gray level array
    :return: volume of gray level array
    """
    # init
    shape = np.shape(matrix)
    volume = 0

    # if array is 2 Dimensional
    if matrix.ndim == 2:
        volume = shape[0] * shape[1]

    # if array is 3 Dimensional
    if matrix.ndim == 3:
        volume = shape[0] * shape[1] * shape[2]

    return volume

