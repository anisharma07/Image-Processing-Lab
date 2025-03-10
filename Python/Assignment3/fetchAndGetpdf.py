import cv2
import numpy as np

# Function to create a normalized histogram (probability distribution)
def createMap(intMap):
    freqMap = [0] * 256
    total_pixels = intMap.shape[0] * intMap.shape[1]  # Total number of pixels
    
    for row in intMap:
        for val in row:
            freqMap[val] += 1
    
    # Normalize frequencies (convert to probability)
    freqMap = [freq / total_pixels for freq in freqMap]
    return freqMap

# Step 1: Read the image
image_path = './Assignment3/Moon.jpg'  # Update with your image path
image = cv2.imread(image_path)

# Convert the image from BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
red_channel = image_rgb[:, :, 0]  # Red channel
green_channel = image_rgb[:, :, 1]  # Green channel
blue_channel = image_rgb[:, :, 2]  # Blue channel

# Generate normalized histograms
r_hist = createMap(red_channel)
g_hist = createMap(green_channel)
b_hist = createMap(blue_channel)
# Example usage:
print(r_hist)
print(g_hist)
print(b_hist)