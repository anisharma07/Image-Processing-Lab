import cv2
import numpy as np
import matplotlib.pyplot as plt


def otsu_thresholding(image):
    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    total_pixels = image.size

    current_max, threshold = 0, 0
    probability = hist / total_pixels
    mean_global = np.sum(np.arange(256) * probability)
    sum_all = np.dot(np.arange(256), hist)
    sumT = 0
    prob1 = 0

    between_class_variance_matrix = np.zeros(256)

    for i in range(256):
        prob1 += hist[i] / total_pixels
        if prob1 == 0:
            continue
        prob2 = 1 - prob1
        if prob2 == 0:
            break

        sumT += i * hist[i]

        meanA = sumT / (prob1 * total_pixels)
        meanB = (sum_all - sumT) / (prob2 * total_pixels)

        between_class_variance = prob1 * prob2 * (meanA - meanB) ** 2

        between_class_variance_matrix[i] = between_class_variance

        if between_class_variance > current_max:
            current_max = between_class_variance
            threshold = i
    
    global_variance = np.sum(((np.arange(256) - mean_global) ** 2) * probability)
    efficiency = current_max / global_variance
    print(f"Efficiency: {efficiency}")
    binary_image = (image > threshold).astype(np.uint8) * 255

    return threshold, binary_image, hist, current_max, between_class_variance_matrix, efficiency


def process_image(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    color_planes = ['Red', 'Green', 'Blue']
    channels = cv2.split(image_rgb)

    fig, axs = plt.subplots(3, 6, figsize=(20, 10))

    for i, (channel, color) in enumerate(zip(channels, color_planes)):
        threshold, binary_image, hist, var_between, between_class_variance_matrix, efficiency = otsu_thresholding(
            channel)

        axs[i, 0].imshow(channel, cmap='gray')
        axs[i, 0].set_title(f'Original {color} Plane')
        axs[i, 0].axis('off')

        axs[i, 1].hist(channel.ravel(), bins=256, range=[
                       0, 256], color=color.lower())
        axs[i, 1].axvline(threshold, color=color.lower(), linestyle='dashed')
        axs[i, 1].set_title(f'Histogram of {color} Plane')

        axs[i, 2].imshow(binary_image, cmap='gray')
        axs[i, 2].set_title(f'Otsu Thresholded {color} Plane (T={threshold})')
        axs[i, 2].axis('off')

        axs[i, 3].hist(binary_image.ravel(), bins=256,
                       range=[0, 256], color=color.lower())
        axs[i, 3].set_title(f'Pixel Intensity Distribution of {color} Plane')

        axs[i, 4].plot(range(256), between_class_variance_matrix,
                       color=color.lower())
        axs[i, 4].set_title(f'Between-Class Variance ({color} Plane)')
        axs[i, 4].set_xlabel('Threshold')
        axs[i, 4].set_ylabel('Variance')
        axs[i, 4].axvline(threshold, color=color.lower(),
                          linestyle='dashed', label=f'k* = {threshold}')
        axs[i, 4].legend()

        axs[i, 5].axis('off')
        axs[i, 5].text(0.5, 0.5,
                    f'{color} Plane:\n'
                    f'k* = {threshold}\n'
                    f'σB² = {var_between:.6f}\n'
                    f'Efficiency = {efficiency:.6f}\n',
                    ha='center', va='center', fontsize=10, wrap=True)

    plt.tight_layout()
    plt.show()


process_image('./Assignment5/snow.jpeg')
