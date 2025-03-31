import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image in color
image = cv2.imread('./Assignment4/assets/input/head.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Split into R, G, B planes
r, g, b = cv2.split(image_rgb)


# Gaussian smoothing function
def apply_gaussian_smoothing(image):
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
    smoothed = cv2.filter2D(image, -1, gaussian_filter)
    return smoothed


# Non-Maximum Suppression
def non_maximum_suppression(magnitude, angle):
    M, N = magnitude.shape
    nms = np.zeros((M, N), dtype=np.float32)
    angle = angle % 180

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            q, r = 255, 255

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
            else:
                nms[i, j] = 0

    return nms


# Double Thresholding
def double_threshold(img, low_thresh, high_thresh):
    strong = 255
    weak = 75

    strong_edges = (img >= high_thresh)
    weak_edges = (img >= low_thresh) & (img < high_thresh)

    result = np.zeros_like(img)
    result[strong_edges] = strong
    result[weak_edges] = weak

    return result, strong, weak


# Hysteresis for connectivity analysis
def hysteresis(img, weak, strong):
    M, N = img.shape
    for i in range(1, M - 1):
        for j in range(1, N - 1):
            if img[i, j] == weak:
                if ((img[i + 1, j] == strong) or (img[i - 1, j] == strong) or
                    (img[i, j + 1] == strong) or (img[i, j - 1] == strong) or
                    (img[i + 1, j + 1] == strong) or (img[i - 1, j - 1] == strong) or
                        (img[i + 1, j - 1] == strong) or (img[i - 1, j + 1] == strong)):
                    img[i, j] = strong
                else:
                    img[i, j] = 0
    return img


# Function to apply Canny Edge Detection on each plane
def process_channel(channel):
    smoothed = apply_gaussian_smoothing(channel)

    gx = cv2.Sobel(smoothed, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(smoothed, cv2.CV_64F, 0, 1, ksize=3)

    gradient_magnitude = np.sqrt(gx**2 + gy**2)
    gradient_angle = np.arctan2(gy, gx) * (180 / np.pi)

    nms = non_maximum_suppression(gradient_magnitude, gradient_angle)

    low_threshold = 30
    high_threshold = 100

    thresholded, strong, weak = double_threshold(
        nms, low_threshold, high_threshold)

    final_edges = hysteresis(thresholded.copy(), weak, strong)

    return final_edges


# Apply Canny Edge Detection to R, G, B planes
r_edges = process_channel(r)
g_edges = process_channel(g)
b_edges = process_channel(b)

# Merge the edge-detected planes
final_output = cv2.merge([r_edges, g_edges, b_edges])


# Display the results
fig, axes = plt.subplots(3, 4, figsize=(20, 15))

# Original image
axes[0][0].imshow(image_rgb)
axes[0][0].set_title('Original Image')
axes[0][0].axis('off')

# R-plane result
axes[0][1].imshow(r, cmap='gray')
axes[0][1].set_title('R-plane')
axes[0][1].axis('off')
axes[1][1].imshow(r_edges, cmap='gray')
axes[1][1].set_title('R-plane Edges')
axes[1][1].axis('off')

# G-plane result
axes[0][2].imshow(g, cmap='gray')
axes[0][2].set_title('G-plane')
axes[0][2].axis('off')
axes[1][2].imshow(g_edges, cmap='gray')
axes[1][2].set_title('G-plane Edges')
axes[1][2].axis('off')

# B-plane result
axes[0][3].imshow(b, cmap='gray')
axes[0][3].set_title('B-plane')
axes[0][3].axis('off')
axes[1][3].imshow(b_edges, cmap='gray')
axes[1][3].set_title('B-plane Edges')
axes[1][3].axis('off')

# Final merged output
axes[2][1].imshow(final_output)
axes[2][1].set_title('Final Merged Output (RGB Edges)')
axes[2][1].axis('off')

plt.tight_layout()
plt.show()
