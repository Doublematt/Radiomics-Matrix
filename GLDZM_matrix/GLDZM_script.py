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
    file.write("small distance emphasis \t")
    file.write("large distance emphasis \t")
    file.write("low gray level zone emphasis \t")
    file.write("high gray level zone emphasis \t")
    file.write("small distance low gray level emphasis \t")
    file.write("small distance high gray level emphasis \t")
    file.write("large distance low gray level emphasis \t")
    file.write("large distance high gray level emphasis \t")
    file.write("gray level non uniformity \t")
    file.write("normalised gray level non uniformity \t")
    file.write("zone size non uniformity \t")
    file.write("normalised zone size non uniformity \t")
    file.write("zone percentage \t")
    file.write("gray level variance \t")
    file.write("zone distance variance \t")
    file.write("zone distance entropy \t")


import os

path_of_the_directory = 'Path to dir'
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
        from GLDZM import GLDZM_matrix
        import GLDZM_features
        from GLDZM import delete_unused_columns

        # reading the data
        data = pd.read_csv(current_file, delimiter=" ")

        # preparing array
        myArray = sdm.dataPreparation(data)

        # converting SUV values to gray levels
        grayLevelArray = glc.get_gray_lvl_matrix(myArray, 8)

        # GLDZM creation

        gldzm_matrix = GLDZM_matrix(grayLevelArray[0], 9, 20)
        for i in range(1, np.shape(grayLevelArray)[0]):
            gldzm_matrix = gldzm_matrix + GLDZM_matrix(grayLevelArray[i], 9, 20)

        gldzm_matrix = delete_unused_columns(gldzm_matrix)

        with open("sample.txt", "a") as file:
            file.write("\n" + filename + "\t")
            file.write(str(GLDZM_features.small_distance_emphasis(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.large_distance_emphasis(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.low_grey_level_zone_emphasis(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.high_grey_level_zone_emphasis(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.small_distance_low_gray_level_emphasis(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.small_distance_high_gray_level_emphasis(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.large_distance_low_gray_level_emphasis(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.large_distance_high_gray_level_emphasis(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.gray_level_non_uniformity(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.normalised_gray_level_non_uniformity(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.zone_distance_non_uniformity(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.normalised_zone_distance_non_uniformity(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.zone_percentage(grayLevelArray, gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.gray_level_variance(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.zone_distance_variance(gldzm_matrix)) + "\t")
            file.write(str(GLDZM_features.zone_distance_entropy(gldzm_matrix)) + "\t")






