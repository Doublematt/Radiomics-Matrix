
import numpy as np


def get_coordinates(matrix):
    shape = np.shape(matrix)

    coordinates = np.array([0, 0])

    for i in range(1, shape[0] - 1):
        for j in range(1, shape[1] - 1):
            coordinates = np.vstack([coordinates, [i, j]])

    coordinates = np.delete(coordinates, 0, 0)

    return coordinates


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


def count_gray_levels(matrix, certain_level, coordinates):

    counter = 0
    coordinates_copy = coordinates

    for i in range(np.shape(coordinates)[0]):
        x, y = coordinates[i]

        if matrix[x, y] == certain_level:
            coordinates_copy = delete_from_array(coordinates_copy, [x, y])
            counter += 1

    return coordinates_copy, counter


def get_neighbourhood(x, y):

    x_range = np.array([x - 1, x, x + 1])
    y_range = np.array([y - 1, y, y + 1])
    positions = np.array([0, 0])

    for i in x_range:
        for j in y_range:

            if i == x and j == y:
                continue
            positions = np.vstack([positions, [i, j]])

    positions = np.delete(positions, 0, 0)
    return positions


def check_neighbourhood(neighbourhood, matrix):

    for voxel in neighbourhood:
        x = voxel[0]
        y = voxel[1]

        if matrix[x, y] != 0:
            return False

    return True


def calculate_average(values):

    how_many = 0
    counter = 0
    for value in values:
        counter += value
        how_many += 1

    return counter/how_many


def calculate_neighbourhood_value(matrix, x, y):

    neighbourhood = get_neighbourhood(x, y)

    if check_neighbourhood(neighbourhood, matrix):
        return 0

    neighbourhood_values = np.array([])

    for voxel in neighbourhood:
        neighbourhood_values = np.append(neighbourhood_values, matrix[voxel[0], voxel[1]])

    average = calculate_average(neighbourhood_values)

    return abs(matrix[x, y] - average)


def delete_zeros(matrix, coordinates):

    if np.array_equal(coordinates, [0]):
        return coordinates

    if coordinates.ndim == 1:
        if matrix[coordinates[0, 0], coordinates[0, 1]] == 0:
            coordinates = np.array([])

    if coordinates.ndim == 2:
        for coordinate in coordinates:
            if matrix[coordinate[0], coordinate[1]] == 0:
                coordinates = delete_from_array(coordinates, coordinate)

    return coordinates


def get_voxels_amount(matrix, coordinates):

    counter = 0
    for coordinate in coordinates:
        neighbourhood = get_neighbourhood(coordinate[0], coordinate[1])

        if not check_neighbourhood(neighbourhood, matrix):
            counter += 1

    return counter


def create_ngtdm_matrix(ni, pi, si):

    matrix = np.array([0, 0, 0])

    for i in range(np.size(pi)):
        matrix = np.vstack([matrix, [ni[i], pi[i], si[i]]])

    matrix = np.delete(matrix, 0, 0)

    return matrix


def ngtdm_matrix(matrix, gray_level):

    coordinates = get_coordinates(matrix)
    coordinates = delete_zeros(matrix, coordinates)

    if np.array_equal(coordinates, [0]):
        return [0]

    n_coordinates = coordinates
    si_coordinates = coordinates
    number_of_certain_levels = np.array([], dtype="int32")
    neighbourhood_si_values = np.zeros([gray_level])

    # ni
    for i in range(1, gray_level + 1):

        n_coordinates, counter = count_gray_levels(matrix, i, n_coordinates)
        number_of_certain_levels = np.append(number_of_certain_levels, counter)

    # si
    for coordinate in si_coordinates:

        voxel_value = matrix[coordinate[0], coordinate[1]]
        si_value = calculate_neighbourhood_value(matrix, coordinate[0], coordinate[1])
        neighbourhood_si_values[voxel_value - 1] += si_value

    # pi
    all_voxels = get_voxels_amount(matrix, coordinates)

    if all_voxels != 0:
        pi_values = number_of_certain_levels / all_voxels
    if all_voxels == 0:
        pi_values = np.zeros_like(neighbourhood_si_values)

    return create_ngtdm_matrix(number_of_certain_levels, pi_values, neighbourhood_si_values)



