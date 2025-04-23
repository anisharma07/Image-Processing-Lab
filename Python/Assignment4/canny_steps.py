import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('./assets/p4/house.jpg',
                   cv2.IMREAD_GRAYSCALE)

gaussian_filter = np.array([
    [0, 0, 0.01, 0.01, 0.01, 0, 0],
    [0, 0.02, 0.08, 0.14, 0.08, 0.02, 0],
    [0.01, 0.08, 0.37, 0.61, 0.37, 0.08, 0.01],
    [0.01, 0.14, 0.61, 1.0, 0.61, 0.14, 0.01],
    [0.01, 0.08, 0.37, 0.61, 0.37, 0.08, 0.01],
    [0, 0.02, 0.08, 0.14, 0.08, 0.02, 0],
    [0, 0, 0.01, 0.01, 0.01, 0, 0]
])
gaussian_filter /= np.sum(gaussian_filter)

smoothed_image = cv2.filter2D(image, -1, gaussian_filter)

gx = cv2.Sobel(smoothed_image, cv2.CV_64F, 1, 0, ksize=3)
gy = cv2.Sobel(smoothed_image, cv2.CV_64F, 0, 1, ksize=3)


gradient_magnitude = np.sqrt(gx**2 + gy**2)
gradient_angle = np.arctan2(gy, gx) * (180 / np.pi)


def non_maximum_suppression(magnitude, angle):
    M, N = magnitude.shape
    nms = np.zeros((M, N), dtype=np.float32)
    angle = angle % 180
    q, r = 0, 0

    for i in range(1, M - 1):
        for j in range(1, N - 1):

            if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                q = magnitude[i, j + 1]
                r = magnitude[i, j - 1]
            elif 22.5 <= angle[i, j] < 67.5:
                q = magnitude[i + 1, j - 1]
                r = magnitude[i - 1, j + 1]
            elif 67.5 <= angle[i, j] < 112.5:
                q = magnitude[i + 1, j]
                r = magnitude[i - 1, j]
            elif 112.5 <= angle[i, j] < 157.5:
                q = magnitude[i - 1, j - 1]
                r = magnitude[i + 1, j + 1]

            if magnitude[i, j] >= q and magnitude[i, j] >= r:
                nms[i, j] = magnitude[i, j]

    return nms


nms_image = non_maximum_suppression(gradient_magnitude, gradient_angle)


strong = 255
weak = 75


def double_threshold(img, low_thresh, high_thresh):
    """Apply double thresholding."""

    strong_edges = (img >= high_thresh)
    weak_edges = (img >= low_thresh) & (img < high_thresh)

    result = np.zeros_like(img)
    result[strong_edges] = strong
    result[weak_edges] = weak
    return result


low_threshold = 20
high_threshold = 100


thresholded = double_threshold(
    nms_image, low_threshold, high_threshold)


def hysteresis(thrCopy):
    M, N = thrCopy.shape
    directions = [
        [1, 0],   # right
        [0, 1],   # down
        [-1, 0],  # left
        [0, -1],  # up
        [1, 1],   # down-right
        [-1, 1],  # down-left
        [1, -1],  # up-right
        [-1, -1]  # up-left
    ]
    for i in range(1, M - 1):
        for j in range(1, N - 1):
            booly = False

            if thrCopy[i, j] == weak:
                for x, y in directions:
                    nx, ny = x+i, y+j
                    if thrCopy[nx, ny] == strong:
                        booly = True
                        break
                if booly:
                    thrCopy[i, j] = strong
                else:
                    thrCopy[i, j] = 0

    return thrCopy


final_edges = hysteresis(thresholded.copy())

fig, axes = plt.subplots(2, 4, figsize=(18, 10))


# Original image
axes[0][0].imshow(image, cmap='gray')
axes[0][0].set_title('Original Image')
axes[0][0].axis('off')
axes[1][0].hist(image.ravel(), bins=256, color='black')
axes[1][0].set_title('Histogram')

# Smoothed image
axes[0][1].imshow(smoothed_image, cmap='gray')
axes[0][1].set_title('Smoothed Image')
axes[0][1].axis('off')
axes[1][1].hist(smoothed_image.ravel(), bins=256, color='black')
axes[1][1].set_title('Histogram')

# NMS image
axes[0][2].imshow(nms_image, cmap='gray')
axes[0][2].set_title('Non-Maximum Suppression')
axes[0][2].axis('off')
axes[1][2].hist(nms_image.ravel(), bins=256, color='black')
axes[1][2].set_title('Histogram')

# Final edges (Double Thresholding)
axes[0][3].imshow(final_edges, cmap='gray')
axes[0][3].set_title('Final Edges (Double Thresholding)')
axes[0][3].axis('off')
axes[1][3].hist(final_edges.ravel(), bins=256, color='black')
axes[1][3].set_title('Histogram')

plt.tight_layout()
plt.show()
