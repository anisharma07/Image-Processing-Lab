import cv2
import numpy as np
import os

def log_transform(image_path, output_folder, c=1.0):
    """
    Apply log transformation to an image and save the result in the specified folder.

    Parameters:
    - image_path (str): Path to the input image.
    - output_folder (str): Path to the folder where the transformed image will be saved.
    - c (float): Scaling constant for the log transformation (default is 1.0).
    
    Returns:
    - output_path (str): Path to the saved log-transformed image.
    """
    # Step 1: Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    
    # Step 2: Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Step 3: Normalize the pixel values to [0, 1]
    normalized_image = gray_image / 255.0
    
    # Step 4: Apply the log transform
    log_transformed = c * np.log(1 + normalized_image)
    
    # Step 5: Scale back to [0, 255]
    log_transformed = np.uint8(255 * log_transformed)
    
    # Step 6: Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Step 7: Save the transformed image
    output_path = os.path.join(output_folder, 'log_transformed.jpg')
    cv2.imwrite(output_path, log_transformed)
    
    print(f"Log-transformed image saved at: {output_path}")
    return output_path


def gamma_transform(image_path, output_folder, gamma=1.0, c=1.0):
    """
    Apply gamma transformation to an image and save the result in the specified folder.

    Parameters:
    - image_path (str): Path to the input image.
    - output_folder (str): Path to the folder where the transformed image will be saved.
    - gamma (float): Gamma value for the transformation (default is 1.0).
    - c (float): Scaling constant for the gamma transformation (default is 1.0).

    Returns:
    - output_path (str): Path to the saved gamma-transformed image.
    """
    # Step 1: Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    
    # Step 2: Convert to grayscale (optional, gamma can be applied to color images as well)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Step 3: Normalize the pixel values to [0, 1]
    normalized_image = gray_image / 255.0
    
    # Step 4: Apply the gamma transform
    gamma_transformed = c * np.power(normalized_image, gamma)
    
    # Step 5: Scale back to [0, 255]
    gamma_transformed = np.uint8(255 * gamma_transformed)
    
    # Step 6: Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Step 7: Save the transformed image
    output_path = os.path.join(output_folder, f'gamma_transformed_gamma_{gamma}.jpg')
    cv2.imwrite(output_path, gamma_transformed)
    
    print(f"Gamma-transformed image saved at: {output_path}")
    return output_path

# Example Usage
input_image_path = '../assets/ass1/boats.bmp'
output_directory = 'log_transform'

# Call the function
log_transform(input_image_path, output_directory, c=1)


# Apply gamma transform with gamma = 2.2 (brightens the image)
gamma_transform(input_image_path, output_directory, gamma=0.1)

# Apply gamma transform with gamma = 0.5 (darkens the image)
# gamma_transform(input_image_path, output_directory, 1)

# gamma_transform(input_image_path, output_directory, 2.2)


