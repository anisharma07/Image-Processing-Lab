from PIL import Image
import numpy as np

# Image and folder paths
file_path = "../assets/ass1/boats.bmp"
output_folder = "abc"


def invert_image(image):
    """
    Inverts the grayscale image by applying 255 - pixel_value.
    """
    np_img = np.array(image)
    inverted = 255 - np_img
    return Image.fromarray(inverted, mode='L')

def sub_sampling(image, factor):
    """
    Reduces the size of the image by selecting every nth pixel.
    """
    np_img = np.array(image)
    sub_sampled = np_img[::factor, ::factor]
    return Image.fromarray(sub_sampled, mode='L')

def process_bmp(file_path, output_folder, sub_sample_factor=2):
    """
    Processes the BMP file for intensity averaging, inversion, and sub-sampling.
    """
    # Load the BMP image
    image = Image.open(file_path)
    
    # Step 2: Inversion
    inverted_image = invert_image(image)
    inverted_image.save(f"{output_folder}/inverted.bmp")
    
    # Step 3: Sub-sampling
    sub_sampled_image = sub_sampling(image, sub_sample_factor)
    sub_sampled_image.save(f"{output_folder}/sub_sampled.bmp")
    
    print("Processing complete. Check the output folder for results.")


# Create the output folder if it doesn't exist
import os
os.makedirs(output_folder, exist_ok=True)

process_bmp(file_path, output_folder, sub_sample_factor=4)
