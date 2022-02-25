from ImageHash import *

DIFF_THRESHOLD = 0.4

def main():
    directory_name = input("Введите название папки: ")
    import os
    image_names = os.listdir(directory_name)
    filtered_dir_name = directory_name + " filtered"
    filtered_images = list()
    for image_name1 in image_names:
        image1 = Image.open(f"{directory_name}\\{image_name1}")
        for image_name2 in filtered_images:
            image2 = Image.open(f"{directory_name}\\{image_name2}")
            if GetDifferenceCoef(image1,image2) < DIFF_THRESHOLD:
                break
        else:
            filtered_images.append(image_name1)

    os.mkdir(filtered_dir_name)
    for image_name in filtered_images:
        Image.open(f"{directory_name}\\{image_name}").save(f"{filtered_dir_name}\\{image_name}")

if __name__ == "__main__":
    main()
