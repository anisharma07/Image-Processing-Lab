import cv2
import numpy as np
import matplotlib.pyplot as plt

def otsu_thresholding(image_channel):
    hist, bins = np.histogram(image_channel.flatten(), 256, [0,256])
    total_pixels = image_channel.size
    
    probability = hist / total_pixels
    mean_global = np.sum(np.arange(256) * probability)
    
    best_threshold = 0
    max_between_class_variance = 0
    
    weight_background = 0
    sum_background = 0
    
    for t in range(256):
        weight_background += probability[t]
        weight_foreground = 1 - weight_background
        
        if weight_background == 0 or weight_foreground == 0:
            continue
        
        sum_background += t * probability[t]
        mean_background = sum_background / weight_background
        mean_foreground = (mean_global - sum_background) / weight_foreground
        
        between_class_variance = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
        
        if between_class_variance > max_between_class_variance:
            max_between_class_variance = between_class_variance
            best_threshold = t
    
    global_variance = np.sum(((np.arange(256) - mean_global) ** 2) * probability)
    efficiency = max_between_class_variance / global_variance
    
    return best_threshold, max_between_class_variance, efficiency

def process_image(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    channels = cv2.split(image_rgb)
    
    processed_images = []
    histograms = []
    
    for channel in channels:
        threshold, between_class_variance, efficiency = otsu_thresholding(channel)
        binary_image = (channel > threshold).astype(np.uint8) * 255
        processed_images.append(binary_image)
        
        hist, bins = np.histogram(channel.flatten(), 256, [0,256])
        histograms.append(hist)
        
        print(f"Optimal Threshold: {threshold}")
        print(f"Between-Class Variance: {between_class_variance}")
        print(f"Efficiency Metric: {efficiency}")
    
    fig, axes = plt.subplots(2, 4, figsize=(15, 8))
    axes[0, 0].imshow(image_rgb)
    axes[0, 0].set_title("Original Image")
    
    color_labels = ["Red", "Green", "Blue"]
    
    for i in range(3):
        axes[0, i+1].imshow(processed_images[i], cmap='gray')
        axes[0, i+1].set_title(f"{color_labels[i]} Binary Image")
        
        axes[1, i+1].plot(histograms[i], color=color_labels[i].lower())
        axes[1, i+1].set_title(f"{color_labels[i]} Histogram")
    
    plt.show()

# Run the process
process_image('./Assignment5/snow.jpeg')