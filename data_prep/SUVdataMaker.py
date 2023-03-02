
import numpy as np

def dataPreparation(data):
    """
    Function prepares data loaded from data frame.
    It was created for SUV type of data.
    It creates 3D numpy array of SUV values from data frame.

    Return 3D numpy.array('float') of SUV values

    Parameters
    ------------
    data : data frame
        data frame containing 4 columns 'x', 'y', 'z' 'SUV'

    """
    # setting array boounds
    x_range = np.max(data['x']) - np.min(data['x'])
    y_range = np.max(data['y']) - np.min(data['y'])
    z_range = np.max(data['z']) - np.min(data['z'])

    # creating an array for data
    SUVdata = np.zeros([x_range + 1, y_range + 1, z_range + 1])

    # placing values in array
    for i in range(data.__len__()):
        SUVdata[(data['x'].iloc[i] - np.min(data['x'])),
                (data['y'].iloc[i] - np.min(data['y'])),
                (data['z'].iloc[i] - np.min(data['z']))] = data['SUV'].iloc[i]

    # returning 3D array
    return SUVdata