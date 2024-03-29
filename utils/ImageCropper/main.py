import ntpath
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
from time import time

def crop_black_letter(image, margin, threshold):
    # Invert the image (black on white to white on black)
    inverted = cv2.bitwise_not(image)

    # Convert the image to grayscale
    gray = cv2.cvtColor(inverted, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get a binary mask
    _, thresholded = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    cv2.imwrite("C:/Users/Pingwin/Desktop/tmp.png", thresholded)

    # Find the non-zero pixels in the thresholded image
    points = cv2.findNonZero(thresholded)

    # Create a rectangular bounding box around the contour
    x, y, w, h = cv2.boundingRect(points)

    # Calculate the maximum side length for the square
    max_side = max(w, h)

    # Calculate the center coordinates of the square
    cx = x + w // 2
    cy = y + h // 2

    # Calculate half the side length of the square
    half_side = max_side // 2

    # Calculate the new bounding box coordinates for the square
    x = cx - half_side
    y = cy - half_side
    w = h = max_side

    # Add margin to the bounding rectangle
    x -= margin
    y -= margin
    w += 2 * margin
    h += 2 * margin

    # Fix overflows
    if x + w > image.shape[0] or y + h > image.shape[1] or x < 0 or y < 0:
        # Create new image with the letter in its center
        newImage = np.zeros((w, h, 3), dtype=np.uint8)
        for i in range(0, w):
            for j in range(0, h):
                if 0 < x + i < image.shape[0] and 0 < y + j < image.shape[1]:
                    newImage[j][i] = image[y+j][x+i]
                else:
                    newImage[j][i] = 255
        cropped = newImage
    else:
        # Crop the image using the bounding box coordinates
        cropped = image[y:y + h, x:x + w]

    if cropped.shape[0] != cropped.shape[1]:
        # if this executes I suck
        print(cropped.shape)
        print(w, h)
        imgplot = plt.imshow(cropped)
        plt.show()

    return cropped

def crop_black_letters_file(address,file,margin,threshold,destination,location):
    image = cv2.imread(os.path.join(address, file))
    cropped_image = crop_black_letter(image, margin, threshold)
    cv2.imwrite(os.path.join(destination + address.replace(location, ''), file), cropped_image)


def crop_black_letters_catalog(location, destination, margin=0, threshold=100):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for address, dirs, files in os.walk(location):
        for directory in dirs:
            subdirectory = address.replace(location, "")
            temp = destination + subdirectory
            if not os.path.exists(os.path.join(temp, directory)):
                os.makedirs(os.path.join(temp, directory))

        pool = mp.Pool()
        pool.starmap_async(crop_black_letters_file,[(address,x,margin,threshold,destination,location) for x in files])
        pool.close()
        pool.join()

    print(f"Cropping finished for catalog {location}")


def main():
    margin = 50
    start = time()

    #TODO: Add cropped directory

    # TEST RUN
    # input_image = cv2.imread("../../resources/uploaded-images/z.png")
    # cv2.imwrite("../../resources/uploaded-images/z-cropped.png", img=crop_black_letter(input_image, margin, threshold=10))
    # crop_black_letters_catalog("../../resources/uploaded-images", "../../resources/preprocessed-images", margin, threshold=100)

    crop_black_letters_catalog("../../resources/datasets/unpacked/dataset-multi-person",
                              f"../../resources/datasets/unpacked/dataset-multi-person-cropped-{margin}", margin, threshold=100)
    crop_black_letters_catalog("../../resources/datasets/unpacked/dataset-single-person",
                              f"../../resources/datasets/unpacked/dataset-single-person-cropped-{margin}", margin, threshold=100)

    end = time()
    print(f"Finished in {end-start}")

if __name__ == '__main__':
    main()
