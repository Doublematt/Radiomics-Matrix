
import numpy as np


def get_gray_level_diff(position_x, position_y, matrix):
    voxel_value = matrix[position_x, position_y]
    matrix_shape = np.shape(matrix)
    new_same_value = np.array([0, 0])

    # getting position around voxel
    zone = get_zone(position_x, position_y, matrix_shape[0] - 1, matrix_shape[1] - 1)

    # checking if any voxel has the same gray level
    for i in range(np.shape(zone)[0]):

        if matrix[zone[i, 0], zone[i, 1]] == voxel_value:
            new_same_value = np.vstack([new_same_value, zone[i]])
            continue

    new_same_value = np.delete(new_same_value, 0, 0)
    border = get_positions(position_x, position_y, matrix_shape[0] - 1, matrix_shape[1] - 1)

    new_border = border
    for j in range(np.shape(border)[0]):
        if check_array(border[j], new_same_value):
            new_border = np.delete(border, j, 0)
    border = new_border
    scanned = np.array([position_x, position_y])

    if np.any(new_same_value):
        if new_same_value.ndim == 1:
            scanned, border = scann_further(new_same_value, border, scanned, matrix_shape, matrix)

        elif new_same_value.ndim == 2:
            for i in range(np.shape(new_same_value)[0]):
                scanned, border = scann_further(new_same_value[i], border, scanned, matrix_shape, matrix)

    counter = 0
    new_border = border
    for i in range(np.shape(border)[0]):
        if check_array(border[i], scanned):
            new_border = np.delete(new_border, i - counter, 0)
            counter += 1

    return scanned, np.unique(new_border, axis=0)


def get_positions(position_x, position_y, max_x, max_y):
    range_x = np.array([])
    range_y = np.array([])

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

    positions = np.array([0, 0])

    for i in range_x:
        for j in range_y:
            if np.array_equal([i, j], [position_x, position_y]):
                continue
            positions = np.vstack([positions, [i, j]])
    positions = np.delete(positions, 0, 0)

    return positions


def get_zone(position_x, position_y, max_x, max_y):
    x_range = np.array([])
    y_range = np.array([])

    if position_x != 0 and position_x != max_x:
        x_range = np.array([[position_x - 1, position_y], [position_x + 1, position_y]])
    elif position_x == 0:
        x_range = np.array([[position_x + 1, position_y]])
    elif position_x == max_x:
        x_range = np.array([[position_x - 1, position_y]])

    if position_y != 0 and position_y != max_y:
        y_range = np.array([[position_x, position_y - 1], [position_x, position_y + 1]])
    elif position_y == 0:
        y_range = np.array([[position_x, position_y + 1]])
    elif position_y == max_y:
        y_range = np.array([[position_x, position_y - 1]])

    positions = np.vstack([x_range, y_range])

    return positions


def scann_further(position, border, scanned, matrix_shape, matrix):

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
    for position in range(np.shape(given)[0]):
        if np.array_equal(looking, given[position]):
            return True
    return False


def delete_from_array(array, element):
    index = find_index(array, element)
    if index != -1:
        array = np.delete(array, index, 0)
    return array


def find_index(array, element):
    for i in range(np.shape(array)[0]):
        if np.array_equal(element, array[i]):
            return i
    return -1


def GLDZM_matrix(matrix, gray_level, max_zone):

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

    while np.any(every_coordinates):
        scanned, border = get_gray_level_diff(every_coordinates[0, 0], every_coordinates[0, 1], matrix)

        if scanned.ndim == 1:
            voxel_value = matrix[scanned[0], scanned[1]]
        elif scanned.ndim == 2:
            voxel_value = matrix[scanned[0, 0], scanned[0, 1]]

        smallest_voxel_diff = get_smalest_difference(voxel_value, border, matrix)
        output[voxel_value, smallest_voxel_diff] += 1

        if scanned.ndim == 2:
            for i in range(np.shape(scanned)[0]):
                every_coordinates = delete_from_array(every_coordinates, scanned[i])
        if scanned.ndim == 1:
            every_coordinates = delete_from_array(every_coordinates, scanned)

    return aftercut(output)


def find_zeros(matrix, some_array):

    zeros_coordinates = np.array([0, 0])
    for i in range(np.shape(some_array)[0]):
        if matrix[some_array[i][0], some_array[i][1]] == 0:
            zeros_coordinates = np.vstack([zeros_coordinates, some_array[i]])

    zeros_coordinates = np.delete(zeros_coordinates, 0, 0)

    return zeros_coordinates


def aftercut(matrix):

    matrix_shape = np.shape(matrix)
    new_matrix = np.zeros([matrix_shape[0] - 1, matrix_shape[1] - 1])

    for i in range(1, np.shape(matrix)[0]):
        for j in range(1, np.shape(matrix)[1]):
            new_matrix[i - 1, j - 1] = matrix[i, j]

    return new_matrix


def get_smalest_difference(value, positions, matrix):

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

    new_matrix = matrix
    minimal = 0
    for i in range(np.shape(matrix)[1] - 1, 0, -1):
        if np.any(matrix[:, i]):
            minimal = i
            break

    if minimal != -1:
        new_matrix = np.zeros([np.shape(matrix)[0], minimal + 1])

        for i in range(np.shape(matrix)[0]):
            for j in range(minimal + 1):
                new_matrix[i, j] = matrix[i, j]

    return new_matrix


def get_voxels_number(matrix):
    shape = np.shape(matrix)
    number = 0

    if matrix.ndim == 2:
        number = shape[0] * shape[1]
    if matrix.ndim == 3:
        number = shape[0] * shape[1] * shape[2]

    return number


