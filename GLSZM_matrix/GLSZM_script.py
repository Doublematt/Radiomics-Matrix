with open("sample.txt", "w") as file:
    file.write("File Name \t")
    file.write("small zone emphasis \t")
    file.write("large zone emphasis \t")
    file.write("low gray level zone emphasis \t")
    file.write("high gray level zone emphasis \t")
    file.write("small zone low gray level emphasis \t")
    file.write("small zone high gray level emphasis \t")
    file.write("large zone low gray level emphasis \t")
    file.write("large zone high gray level emphasis \t")
    file.write("gray level non uniformity \t")
    file.write("normalised gray level non uniformity \t")
    file.write("zone size non uniformity \t")
    file.write("normalised zone size non uniformity \t")
    file.write("zone percentage \t")
    file.write("gray level variance \t")
    file.write("zone size variance \t")
    file.write("zone size entropy \t")
    file.write("zone size energy \t")

import os

path_of_the_directory = '..\LungNodules'
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
        from GLSZM import GLSZM_matrix
        import features
        from GLSZM import delete_unused_columns

        # reading the data
        data = pd.read_csv(current_file, delimiter=" ")

        # preparing array
        myArray = sdm.dataPreparation(data)

        # converting SUV values to gray levels
        grayLevelArray = glc.get_gray_lvl_matrix(myArray, 8)

        # GLSZM creation

        glszm_matrix = GLSZM_matrix(grayLevelArray[0], 9)
        for i in range(1, np.shape(grayLevelArray)[0]):
            glszm_matrix = glszm_matrix + GLSZM_matrix(grayLevelArray[i], 9)

        glszm_matrix = delete_unused_columns(glszm_matrix)

        with open("sample.txt", "a") as file:
            file.write("\n" + filename + "\t")
            file.write(str(features.small_zone_emphasis(glszm_matrix)) + "\t")
            file.write(str(features.large_zone_emphasis(glszm_matrix)) + "\t")
            file.write(str(features.low_gray_level_zone_emphasis(glszm_matrix)) + "\t")
            file.write(str(features.high_gray_level_zone_emphasis(glszm_matrix)) + "\t")
            file.write(str(features.small_zone_low_gray_level_emphasis(glszm_matrix)) + "\t")
            file.write(str(features.small_zone_high_gray_level_emphasis(glszm_matrix)) + "\t")
            file.write(str(features.large_zone_low_gray_level_emphasis(glszm_matrix)) + "\t")
            file.write(str(features.large_zone_high_gray_level_emphasis(glszm_matrix)) + "\t")
            file.write(str(features.gray_level_non_uniformity(glszm_matrix)) + "\t")
            file.write(str(features.normalised_gray_level_non_uniformity(glszm_matrix)) + "\t")
            file.write(str(features.zone_size_non_uniformity(glszm_matrix)) + "\t")
            file.write(str(features.normalised_zone_size_non_uniformity(glszm_matrix)) + "\t")
            file.write(str(features.zone_percentage(grayLevelArray, glszm_matrix)) + "\t")
            file.write(str(features.gray_level_variance(glszm_matrix)) + "\t")
            file.write(str(features.zone_size_variance(glszm_matrix)) + "\t")
            file.write(str(features.zone_size_entropy(glszm_matrix)) + "\t")
            file.write(str(features.dependence_count_energy(glszm_matrix)) + "\t")




