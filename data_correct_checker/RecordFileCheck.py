import os

file1 = "file1.txt"
file2 = "file2.txt"

file1_lines = []
file2_lines = []

if os.path.isfile(file1 and file2):
    with open(file1, "r") as f1:
        lines = f1.readlines()

        for line in lines:
            file1_lines.append(line)

    with open(file2, "r") as f2:
        lines2 = f2.readlines()

        for line in lines2:
            file2_lines.append(line)

f1.close()
f2.close()

print("records in file 1, but not in file 2")
for i in range(len(file1_lines)):
    if file1_lines[i] not in file2_lines:
        print(file1_lines[i])
print("----------------------------------------")


print("records in file 2, but not in file 1")
for i in range(len(file2_lines)):
    if file2_lines[i] not in file1_lines:
        print(file2_lines[i])
print("----------------------------------------")


print("duplicates from file 1")
for i in range(0, len(file1_lines) - 1):
    if file1_lines[i] == file1_lines[i + 1]:
        print(file1_lines[i])
print("----------------------------------------")


print("duplicates from file 2")
for i in range(0, len(file2_lines) - 1):
    if file2_lines[i] == file2_lines[i + 1]:
        print(file2_lines[i])
print("----------------------------------------")
