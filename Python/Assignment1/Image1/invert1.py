import cv2
import numpy as np
import matplotlib.pyplot as plt

# Create a 0 to 255 freqMap, where index = intensity level & freq[index] = freq of pixels
def createMap(intMap):
    freqMap = [0]*256
    for row in intMap:
        for val in row:
         freqMap[val] += 1
    return freqMap

image_path = './Ass1/Image1/abc1/inverse.bmp'

image = cv2.imread(image_path)
print(image.shape)

# Convert the image from BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
red_channel = image_rgb[:, :, 0]  # Red channel (0 for Red in RGB image)
green_channel = image_rgb[:, :, 1]  # Green channel (1 for Green in RGB image)
blue_channel = image_rgb[:, :, 2]  # Blue channel (2 for Blue in RGB image)

r_hist = createMap(red_channel)
g_hist = createMap(green_channel)
b_hist = createMap(blue_channel)

# Create a figure with subplots
fig, axs = plt.subplots(2, 4, figsize=(19, 10))
# fig.suptitle("Inverted Image and Histograms", fontsize=16)
fig.canvas.manager.set_window_title("Inverted Boat Image")


# Display the RGB image
axs[0, 0].imshow(image_rgb)
axs[0, 0].set_title("Inverted Image")
axs[0, 0].axis('off')

# Histogram
axs[1,0].plot(r_hist, color='red', label='Red Channel')
axs[1,0].plot(g_hist, color='green', label='Green Channel')
axs[1,0].plot(b_hist, color='blue', label='Blue Channel')
axs[1, 0].set_xlabel("Pixel Intensity")
axs[1, 0].set_ylabel("Frequency")
axs[1, 0].legend()
axs[1, 0].grid()


# Plot the histograms as bars
axs[1,1].bar(range(256), r_hist, color='red', alpha=0.6, label='Red Channel')
axs[1, 2].bar(range(256), g_hist, color='green', alpha=0.6, label='Green Channel')
axs[1, 3].bar(range(256), b_hist, color='blue', alpha=0.6, label='Blue Channel')

# red channel
axs[1, 1].set_xlabel("Pixel Intensity")
axs[1,1].set_ylabel("Frequency")
axs[1,1].legend()
axs[1,1].grid()

# green channel
axs[1,2].set_xlabel("Pixel Intensity")
axs[1,2].set_ylabel("Frequency")
axs[1,2].legend()
axs[1,2].grid()

# green channel
axs[1,3].set_xlabel("Pixel Intensity")
axs[1,3].set_ylabel("Frequency")
axs[1,3].legend()
axs[1,3].grid()

# Display the Red channel
axs[0,1].imshow(red_channel, cmap='Reds')
axs[0,1].set_title("Red Channel")
axs[0,1].axis('off')

# Display the Green channel
axs[0,2].imshow(green_channel, cmap='Greens')
axs[0,2].set_title("Green Channel")
axs[0,2].axis('off')

# Display the Blue channel
axs[0,3].imshow(blue_channel, cmap='Blues')
axs[0,3].set_title("Blue Channel")
axs[0,3].axis('off')

plt.tight_layout()
plt.show()