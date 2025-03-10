import cv2
import numpy as np
import matplotlib.pyplot as plt

#  create a 0 to 255 freqMap, where index = intensity level & freq[index] = freq of pixels
def createMap(intMap):
    freqMap = [0]*256
    for row in intMap:
        for val in row:
            freqMap[val]+=1
    return freqMap


# Step 1: Read the image
# image_path = '../assets/Images/Exp1/scene.jpg'  # Replace with the path to your image
image_path = './Assignment3/Histogram_Specified_Moon.jpg'


image = cv2.imread(image_path)
print(image.shape);

# Convert the image from BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
red_channel = image_rgb[:, :, 0]  # Red channel (0 for Red in RGB image)
green_channel = image_rgb[:, :, 1]  # Green channel (1 for Green in RGB image)
blue_channel = image_rgb[:, :, 2]  # Blue channel (2 for Blue in RGB image)

r_hist = createMap(red_channel)
g_hist  = createMap(green_channel)
b_hist = createMap(blue_channel)

print(r_hist)

# Step 4: Plot the histograms
plt.figure(figsize=(10, 6))
plt.title("RGB Histogram")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")

# Plot each histogram
plt.plot(r_hist, color='red', label='Red Channel')
plt.plot(g_hist, color='green', label='Green Channel')
plt.plot(b_hist, color='blue', label='Blue Channel')

plt.legend()
plt.grid()
plt.show()


# Step 2: Split the image into R, G, B channels
# r, g, b = cv2.split(image_rgb)
# Step 3: Compute histograms for each channel
# hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])
# hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
# hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])

# print(hist_b)