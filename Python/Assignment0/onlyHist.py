import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def createMap(intMap):
    freqMap = [0]*256
    for row in intMap:
        for val in row:
            freqMap[val] += 1
    return freqMap
# Gamma transformation function
def gamma_transform(image, gamma):
    image_array = np.array(image) / 255.0
    gamma_image = np.power(image_array, gamma)
    gamma_image = np.clip(gamma_image, 0, 1) * 255
    return Image.fromarray(gamma_image.astype(np.uint8))

# Filepath
image_path = '../assets/ass1/boats.bmp'

# Read and transform the image
image = Image.open(image_path)
gamma = 2.2  # Example gamma value
gamma_image = gamma_transform(image, gamma)

# Convert the gamma-corrected image to RGB and then to numpy array
gamma_image_rgb = np.array(image.convert('RGB'))
red_channel = gamma_image_rgb[:, :, 0]
green_channel = gamma_image_rgb[:, :, 1]
blue_channel = gamma_image_rgb[:, :, 2]

r_hist = createMap(red_channel)
g_hist = createMap(green_channel)
b_hist = createMap(blue_channel)
mean_hist = [0]*256
for i in range(256):
    mean_hist[i] = (r_hist[i] + g_hist[i] + b_hist[i]) / 3

# Create a figure with subplots
fig, axs = plt.subplots(1, 1, figsize=(10, 6))  # Create a single subplot
fig.suptitle("Image Histogram", fontsize=16)
fig.canvas.manager.set_window_title("Histogram")

# Plot the histograms as bars
axs.bar(range(256), mean_hist, color='gray', alpha=0.6, label='Red Channel')

# Set titles and labels
axs.set_title("Image Histogram")
axs.set_xlabel("Pixel Intensity")
axs.set_ylabel("Frequency")
axs.legend()
axs.grid()

plt.tight_layout()
plt.show()