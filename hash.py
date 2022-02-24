from PIL import Image
import numpy as np

def GetImageHash(image):
    resized = image.resize((8,8))
    gray = resized.convert("L")
    arr = np.array(gray)
    treshold = np.mean(arr)
    hash = [1 if i >= treshold else 0 for i in arr.flatten()]
    return hash

def main():
    image = Image.open('test images\\akudama drive.png')
    image1 = Image.open('test images\\akudama drive wo logo.png')
    hash = GetImageHash(image)
    hash1 = GetImageHash(image1)
    sim = np.count_nonzero(hash!=hash1)/len(hash)
    print(hash)
    print(hash1)
    print(sim)

if __name__ == "__main__":
    main()
