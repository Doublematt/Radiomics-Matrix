"""
NOTE!!!!
if you want to run this script follow these steps:
    1. Create new folder.
    2. Copy all the files from this folder to folder you just created.
    3. Create file 'sample.txt'.
    4. Copy files from data_prep folder: GraylevelConverter.py , SUVdataMaker.py .
    5. Add the directory with data files to your new folder and change the variable 'path_of_the_directory' to your directory name.
    6. Now you should be good to run this script.

    if something is not working contact me on mateusz.matusewicz16@gmail.com

"""



with open("sample.txt", "w") as file:
    file.write("File Name \t")
    file.write("low dependence emphasis \t")
    file.write("high dependence emphasis \t")
    file.write("low gray level count emphasis \t")
    file.write("high gray level count emphasis \t")
    file.write("low dependence low gray level emphasis \t")
    file.write("low dependence high gray level emphasis \t")
    file.write("high dependence low gray level emphasis \t")
    file.write("high dependence high gray level emphasis \t")
    file.write("gray level non uniformity \t")
    file.write("normalised gray level non uniformity \t")
    file.write("dependence count non uniformity \t")
    file.write("normalised gray level non uniformity \t")
    file.write("gray level variance \t")
    file.write("dependence count variance \t")
    file.write("dependence count entropy \t")
    file.write("dependence count energy \t")

import os

path_of_the_directory = 'some dir'
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
        import NGLDM
        import NGLDM_features

        # reading the data
        data = pd.read_csv(current_file, delimiter=" ")

        # preparing array
        myArray = sdm.dataPreparation(data)

        # converting SUV values to gray levels
        grayLevelArray = glc.get_gray_lvl_matrix(myArray, 8)

        # NGLDM creation

        matrix = NGLDM.NGLDM(grayLevelArray[0])
        matrix.NGLDM_matrix(9)
        ngldm_matrix = np.zeros_like(matrix.get_NGLDM_matrix())

        for i in range(len(grayLevelArray)):
            tmp_matrix = NGLDM.NGLDM(grayLevelArray[i])
            tmp_matrix.NGLDM_matrix(9)
            ngldm_matrix += tmp_matrix.get_NGLDM_matrix()


        with open("sample.txt", "a") as file:
            file.write("\n" + filename + "\t")
            file.write(str(NGLDM_features.low_dependence_emphasis(ngldm_matrix)) + "\t")
            file.write(str(NGLDM_features.high_dependence_emphasis(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.low_gray_level_count_emphasis(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.high_gray_level_count_emphasis(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.low_dependence_low_gray_level_emphasis(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.low_dependence_high_gray_level_emphasis(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.high_dependence_low_gray_level_emphasis(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.high_dependence_high_gray_level_emphasis(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.gray_level_non_uniformity(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.normalised_gray_level_non_uniformity(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.dependence_count_non_uniformity(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.normalised_gray_level_non_uniformity(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.gray_level_variance(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.dependence_count_variance(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.dependence_count_entropy(ngldm_matrix)) + " \t")
            file.write(str(NGLDM_features.dependence_count_energy(ngldm_matrix)) + " \t")



