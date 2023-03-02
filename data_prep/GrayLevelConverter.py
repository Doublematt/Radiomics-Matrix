import numpy as np

"""
    A collection of functions to convert SUV data to gray level matrix's
    
    Attributes
    ---------------
        It has no attributes
        
    Methods
    --------------
        get_min(matrix)
            returns smallest value from 3D matrix
        
        set_division_range(division_number, max_SUV_value, min_SUV_value)
            creates an array of numbers equally divided between two numbers
            
        group_number(value_SUV, division_number_set)
            used to group SUV values in gray level scale
            
        get_gray_lvl_matrix(matrix, gray_lvl_number=8)
            returns a new gray level matrix created based on given one
            
        get_gray_lvl_value(value_SUV, matrix, gray_lvl_number)
            implementation of an equasion - Suv value to gray level transformation
               
        
        

"""


def get_min(matrix):
    """
    Function created to calculated minimal value from given 3D array.
    It ignores 0 values, does not count them

    Parameters
    ------------

    matrix : 3D numpy.array()
        array in which minimal value is being found


    """

    # getting the input array shape
    x, y, z = np.shape(matrix)
    # setting min value to max
    min_value = np.max(matrix)

    # scanning array for smaller number
    for i in range(x):
        for j in range(y):
            for k in range(z):
                # ignores 0
                if matrix[i, j, k] == 0.0:
                    continue

                # if value is less than current min_value change it
                if matrix[i, j, k] < min_value:
                    min_value = matrix[i, j, k]

    # returns smallest value from array
    return min_value


def set_division_range(division_number, max_SUV_value, min_SUV_value):
    """
    Divide a range from min value to max value to equal number of parts.
    The number of parts is called division_number

    Parameters
    -----------
        division_number : int
            number to which the range of values should be divided to

        max_SUV_value : float
            max number in given range

        min_SUV_value : float
            min number in given range

    returns numpy.array() of divided numbers

    """
    # between is a step (value) between to values in return array
    between = (max_SUV_value - min_SUV_value) / division_number

    # initializing array with first value - minimal
    division_number_set = np.array([min_SUV_value])

    # setting up the starting value
    value = division_number_set[0]

    # creating a set
    while value < max_SUV_value:
        # increasing the value by step
        value += between
        # adding value to set
        division_number_set = np.append(division_number_set, value)

    # returns set
    return division_number_set


def group_number(value_SUV, division_number_set):
    """
        This function groups numbers in a given set and returns value which refers to position in the set
        Set is a gray level range

        Parameters
        -------------
            value_SUV : float
                SUV value to group

            division_number_set
                set of values to classify

        retuns a int value - gray level of SUV value

    """
    # setting starting index (gray level) to 0
    index = 0

    # finding the right index based on SUV value
    while value_SUV >= division_number_set[index]:
        index += 1

        # handling exception - given value is max value
        if value_SUV >= division_number_set[-1]:
            index = len(division_number_set) - 1
            break

    # returns gray level value
    return index


def get_gray_lvl_matrix(matrix, gray_lvl_number=8):
    """
    Function to calculate matrix's of gray level value from SUV data.
    It transforms the SUV data do gray level's

    gray_lvl_number is by default set to 8

    Does not use equation method!

    Parameters
    -------------

        matrix : 3D numpy.array()
            input SUV data 3D matrix

        gray_lvl_number : int
            a number of gray levels


    returns gray level 3D array

    """

    # setting max and min value
    max_value = np.max(matrix)
    min_value = get_min(matrix)

    # getting a range
    division_range = set_division_range(gray_lvl_number, max_value, min_value)

    # setting up the gray level matrix
    gray_level_matrix = np.zeros_like(matrix)

    # getting the shape of input 3D matrix
    x, y, z = np.shape(matrix)

    # loop to fill the gray level matrix
    for i in range(x):
        for j in range(y):
            for k in range(z):
                # ignoring 0
                if matrix[i, j, k] == 0:
                    continue

                gray_level_matrix[i, j, k] = group_number(matrix[i, j, k], division_range)

    # setting a type to int
    gray_level_matrix = gray_level_matrix.astype(dtype='int32')

    # lowering max value from n + 1 to n
    gray_level_matrix = gray_level_max_value_handler(gray_level_matrix, gray_lvl_number)

    # returns 3D gray level matrix
    return gray_level_matrix


def get_gray_lvl_value(value_SUV, matrix, gray_lvl_number):
    """
        Function calculates a gray level value of SUV value based on equation.

        Parameters
        ------------

            value_SUV : float
                SUV value from matrix

            matrix : numpy.array()
                matrix of SUV value

            gray_lvl_number : int
                amount of gray levels


        returns gray level value
    """
    from math import floor

    # getting min and max value from the matrix
    max_value = np.max(matrix)
    min_value = get_min(matrix)

    # equation implementation
    gray_lvl_value = floor(gray_lvl_number * ((value_SUV - min_value) / (max_value - min_value))) + 1

    # value on gray scale
    return gray_lvl_value


def get_gray_lvl_matrix_equasion(matrix, gray_lvl_number=8):
    """
        Function calculates and creates a gray level matrix based on given equation.

        gray_lvl_number is by default set to 8

        Parameters
        -----------
            matrix : numpy.array()
                SUV data matrix

            gray_lvl_number : int
                a number of gray levels


    returns gray level 3D array

    """
    # setting up the gray level matrix
    gray_level_matrix = np.zeros_like(matrix)
    # getting the input matrix shape
    x, y, z = np.shape(matrix)

    # loop to fill gray level matrix
    for i in range(x):
        for j in range(y):
            for k in range(z):
                # ignores 0
                if matrix[i, j, k] == 0:
                    continue

                gray_level_matrix[i, j, k] = get_gray_lvl_value(matrix[i, j, k], matrix, gray_lvl_number)

    # converting matrix to int type
    gray_level_matrix = gray_level_matrix.astype(dtype='int32')

    # exception max value
    gray_level_max_value_handler(gray_level_matrix, gray_lvl_number)
    # returns matrix of gray levels
    return gray_level_matrix


def gray_level_max_value_handler(arr, gray_levels):
    shape = np.shape(arr)
    max_number = gray_levels + 1

    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                if arr[i, j, k] == max_number:
                    arr[i, j, k] = gray_levels

    return arr