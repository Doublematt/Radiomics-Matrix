with open("sample.txt", "w") as file:
    file.write("File Name \t")
    file.write("coarseness \t")
    file.write("contrast \t")
    file.write("busyness \t")
    file.write("complexity \t")
    file.write("strength \t")


import os

path_of_the_directory = '../badanie2_pet'
print("Files and directories in a specified path:")
for filename in os.listdir(path_of_the_directory):
    current_file = os.path.join(path_of_the_directory, filename)
    if os.path.isfile(current_file):
        print(current_file)

        # official library
        import pandas as pd
        import numpy as np

        # my files
        import SUVdataMaker as sdm
        import GrayLevelConverter as glc
        import NGTDM


        # reading the data
        data = pd.read_csv(current_file, delimiter=" ")

        # preparing array
        myArray = sdm.dataPreparation(data)

        # converting SUV values to gray levels
        grayLevelArray = glc.get_gray_lvl_matrix(myArray, 64)

        # NGTDM creation
        ngtdm_list = []
        for i in range(np.shape(grayLevelArray)[0]):
            ngtdm_matrix = NGTDM.ngtdm_matrix(grayLevelArray[i], 64)
            if np.array_equal(ngtdm_matrix, [0]):
                continue
            ngtdm_list.append(ngtdm_matrix)


        final_ngtdm = np.zeros([64, 3])
        counter = 0
        for ngtdm in ngtdm_list:
            final_ngtdm[:, 0] += ngtdm[:, 0]
            final_ngtdm[:, 1] += ngtdm[:, 1]
            final_ngtdm[:, 2] += ngtdm[:, 2]
            counter += 1

        final_ngtdm[:, 1:3] = final_ngtdm[:, 1:3] / counter

        import features

        with open("sample.txt", "a") as file:
            file.write("\n" + filename + "\t")
            file.write(str(features.coarsennes(final_ngtdm)) + "\t")
            file.write(str(features.contrast(final_ngtdm)) + "\t")
            file.write(str(features.busyness(final_ngtdm)) + "\t")
            file.write(str(features.complexity(final_ngtdm)) + "\t")
            file.write(str(features.strenght(final_ngtdm)) + "\t")