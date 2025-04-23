import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to create a normalized histogram (probability distribution)


def createMap(intMap, total_pixels):
    freqMap = [0] * 256

    for row in intMap:
        for val in row:
            freqMap[val] += 1

    # Normalize frequencies (convert to probability)
    freqMap = [freq / total_pixels for freq in freqMap]
    return freqMap


# Step 1: Read the image
image_path = './assets/p0/rgb.png'

image = cv2.imread(image_path)
m, n = image.shape[:2]
total_pixels = m * n
# Convert the image from BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
red_channel = image_rgb[:, :, 0]  # Red channel
green_channel = image_rgb[:, :, 1]  # Green channel
blue_channel = image_rgb[:, :, 2]  # Blue channel

# Generate normalized histograms
r_hist = createMap(red_channel, total_pixels)
g_hist = createMap(green_channel, total_pixels)
b_hist = createMap(blue_channel, total_pixels)

# Plot the probability histograms
plt.figure(figsize=(10, 6))
plt.title("RGB Histogram (Normalized)")
plt.xlabel("Pixel Intensity")
plt.ylabel("Probability")
plt.plot(r_hist, color='red', label='Red Channel')
plt.plot(g_hist, color='green', label='Green Channel')
plt.plot(b_hist, color='blue', label='Blue Channel')
plt.legend()
plt.grid()
plt.show()
