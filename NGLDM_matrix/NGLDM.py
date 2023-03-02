class NGLDM:
    """
    This class calculates NGLDM NGLDM_matrix based on given algorytm:

    !!! TODO: DESCRIBE THE ALGORYTM

    Attributes
    ----------

    matrix : numpy.array('int')
        2D array of voxel's values in a given gray scale

    NGLDM_omatrix : numpy.array()
        output NGLDM NGLDM_matrix, NGLDM_matrix based on NGLDM NGLDM_matrix algorytm


    Methods
    --------

    get_matrix()
        returns a NGLDM_matrix given in constructor

    set_matrix(new_matrix)
        sets new NGLDM_matrix

    get_NGLDM_omatrix()
        returns 2D array - output NGLDM NGLDM_matrix

    get_Ng (position_x, position_y)
        Function used to obtain Ng value nessesery to create NGLDM NGLDM_matrix

    NGLDM_matrix (grey_levels, d)
        Function used to set the NGLDM_omatrix value.
        Returns NGLDM NGLDM_matrix.



    """

    def __init__(self, matrix):
        """
        Constructor method setting up a NGLDM_matrix on which the NGLDM NGLDM_matrix will be prepared on.

        Parameters
        ------------

        matrix : numpy.array()
            voxel's values on gray scale

        """

        import numpy as np

        self.matrix = matrix
        self.NGLDM_omatrix = np.array([])

    def get_matrix(self):
        """
        Returns an array of voxel's values on gray scale (one given in a constructor)
        """
        return self.matrix

    def set_matrix(self, new_matrix):
        """
        Allows to change the voxel's gray scale NGLDM_matrix

        Parameters
        ------------

        new_matrix : numpy.array()
            new array of voxel's values on gray scale

        """
        self.matrix = new_matrix

    def get_NGLDM_matrix(self):
        """
        Returns 2D numpy.array() NGLDM_matrix

        if NGLDM_matrix wasn't calculated, it returns empty array

        """

        return self.NGLDM_omatrix

    def get_Ng(self, position_x, position_y, d=1):
        """
        Returns Ng value nessesery to create NGLDM NGLDM_matrix.

        Calculates Ng value for given position.

        Parameters
        ------------

        position_x : int
            x position (in data set) of value to which Ng will be calculated to

        position_y : int
            y position (in data set) of value to which Ng will be calculated to

        d : int in range {1, 2, 3}
            d value describes search range for the same values as given number
            read also NGLDM_matrix

        """
        import numpy as np

        # getting a value at given coordinates
        central_value = self.matrix[position_x, position_y]

        # calculating range for loops
        range_x = np.array([], dtype="int")
        range_y = np.array([], dtype="int")

        for i in range(position_x - d, position_x + d + 1):
            range_x = np.append(range_x, i)

        for j in range(position_y - d, position_y + d + 1):
            range_y = np.append(range_y, j)

        # number of the same values as given
        counter = 0

        # finding the same values
        for i in range_x:
            for j in range_y:

                # checking if value is the same as given one
                if self.matrix[i, j] == central_value:
                    counter += 1

        # given value is calculated too so - 1 is nessesery
        return (counter - 1)

    def NGLDM_matrix(self, grey_levels, d=1):
        """
        Function returns NGLDM NGLDM_matrix.

        It follows the algorithm to get Ng, Nn values and increase value at this location.
        [x, y] -> [Ng, Nn]
        Then process repeats until no value can be calculated and the NGLDM NGLDM_matrix is returned

        If d is different from 1,2,3 then It will return empty NGLDM_matrix (filled with 0)
        If d is not defined then it's value is set to 1

        Parameters
        -----------

        grey_levels : int
            number of possible gray levels and number of rows in NGLDM NGLDM_matrix

        d : int in {1, 2, 3}
            range in which algorytm looks for same values 1 -> 3x3, 2 -> 5x5, 3 -> 7x7

        """
        import numpy as np

        # array of possible d values
        d_range = np.array([1, 2, 3])

        # range for loops
        matrix_range = np.shape(self.matrix)

        # preparing NGLDM NGLDM_matrix filled with zeros
        output_matrix = np.zeros([grey_levels, 9])

        # checking if d values is right
        # if it is, returns blank NGLDM_matrix filed with zeros
        if d not in d_range:
            return output_matrix

        # looping for every value in 3D NGLDM_matrix
        for i in range(d, matrix_range[0] - d):
            for j in range(d, matrix_range[1] - d):
                # getting Ng value
                Ng = self.get_Ng(i, j, d)
                # getting Nn value
                Nn = self.matrix[i, j]

                # changing specific value in NGLDM NGLDM_matrix
                output_matrix[Nn, Ng] += 1

        #deleting 0's'
        output_matrix = modifyMatrix(output_matrix)

        # setting the attribute value
        self.NGLDM_omatrix = output_matrix

        # NGLDM NGLDM_matrix
        return output_matrix.astype(dtype='int32')

def modifyMatrix(matrix):
    import numpy as np

    shape = np.shape(matrix)
    modifiedMatrix = matrix[1:shape[0]]

    return modifiedMatrix

