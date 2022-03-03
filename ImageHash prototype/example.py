from ImageHash import *

DIFF_THRESHOLD = 0.2

directory_name = input("Введите название папки: ")
import os
image_names = os.listdir(directory_name)
filtered_dir_name = directory_name + " filtered"
filtered_image_names = list()
for image_name1 in image_names:
    image1 = Image.open(f"{directory_name}\\{image_name1}")
    for image_name2 in filtered_image_names:
        image2 = Image.open(f"{directory_name}\\{image_name2}")
        diff = GetDifferenceCoef(image1,image2)
        print(image_name1,image_name2, diff)
        if diff < DIFF_THRESHOLD:
            break
    else:
        filtered_image_names.append(image_name1)

os.mkdir(filtered_dir_name)
for image_name in filtered_image_names:
    Image.open(f"{directory_name}\\{image_name}").save(f"{filtered_dir_name}\\{image_name}")
