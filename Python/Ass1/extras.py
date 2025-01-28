
# def intensity_averaging(image):
#     """
#     Converts an image to grayscale by averaging the R, G, and B values.
#     If the image is already grayscale, it is returned as is.
#     """
#     np_img = np.array(image)
    
#     # Check if the image has 3 channels (RGB)
#     if len(np_img.shape) == 3 and np_img.shape[2] == 3:
#         grayscale = np.mean(np_img, axis=2).astype(np.uint8)  # Average intensity
#         return Image.fromarray(grayscale, mode='L')
#     elif len(np_img.shape) == 2:  # Already grayscale
#         return image
#     else:
#         raise ValueError("Unsupported image format")



#     # Step 1: Intensity Averaging
#     avg_image = intensity_averaging(image)
#     avg_image.save(f"{output_folder}/intensity_averaged.bmp")
    

# def contrast_stretching(image_array):
#     """
#     Applies contrast stretching to the image.
#     Formula: new_pixel = 255 * (pixel - min_pixel) / (max_pixel - min_pixel)
#     """
#     min_pixel = np.min(image_array)
#     max_pixel = np.max(image_array)
#     stretched = 255 * (image_array - min_pixel) / (max_pixel - min_pixel)
#     return stretched.astype(np.uint8)

    # Apply contrast stretching
    # contrast_image = contrast_stretching(image_array)
    # save_image(contrast_image, os.path.join(output_folder, "contrast_stretched.bmp"))
    