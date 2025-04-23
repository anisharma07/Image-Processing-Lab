import os
from PIL import Image
import numpy as np

# Image and folder paths
file_path = "../assets/ass1/shoulderCR.pgm"
output_folder = "./assets/p1/abc"


def intensity_averaging(image):
    np_img = np.array(image)
    avg_intensity = np.mean(np_img)
    return Image.fromarray(np.full_like(np_img, avg_intensity), mode='L')


def invert_image(image):
    np_img = np.array(image)
    inverted = 255 - np_img
    return Image.fromarray(inverted, mode='L')


def sub_sampling(image, factor):
    np_img = np.array(image)
    sub_sampled = np_img[::factor, ::factor]
    return Image.fromarray(sub_sampled, mode='L')


def contrast_stretching(image_array):
    """
    Applies contrast stretching to the image.
    Formula: new_pixel = 255 * (pixel - min_pixel) / (max_pixel - min_pixel)
    """
    min_pixel = np.min(image_array)
    max_pixel = np.max(image_array)
    stretched = 255 * (image_array - min_pixel) / (max_pixel - min_pixel)
    return stretched.astype(np.uint8)


def process_bmp(file_path, output_folder, sub_sample_factor=2):

    image = Image.open(file_path)

    # Step 1: Intensity Averaging
    avg_intensity = intensity_averaging(image)
    avg_intensity.save(f"{output_folder}/intensity_averaging.bmp")

    # Step 2: Inversion
    inverted_image = invert_image(image)
    inverted_image.save(f"{output_folder}/inverted.bmp")

    # Step 3: Sub-sampling
    sub_sampled_image = sub_sampling(image, sub_sample_factor)
    sub_sampled_image.save(f"{output_folder}/sub_sampled.bmp")

    print("Processing complete. Check the output folder for results.")


# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

process_bmp(file_path, output_folder, sub_sample_factor=4)
