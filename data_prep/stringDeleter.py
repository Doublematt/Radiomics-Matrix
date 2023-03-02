
import os

directory_path = "From what dir"
for filename in os.listdir(directory_path):
    current_file = os.path.join(directory_path, filename)
    if os.path.isfile(current_file):
        with open(current_file, "r") as f:
            lines = f.readlines()

            path = "to what dir" + filename
            with open(path, "w") as newf:
                newf.write("x y z SUV \n")
                for line in lines:
                    if line.startswith("#"):
                        continue

                    newf.write(line)





