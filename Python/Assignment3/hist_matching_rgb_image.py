import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def createMap(intMap):
    freqMap = [0] * 256
    total_pixels = intMap.shape[0] * intMap.shape[1]  # Total number of pixels
    
    for row in intMap:
        for val in row:
            freqMap[val] += 1
    
    freqMap = [freq / total_pixels for freq in freqMap]
    return freqMap

def compute_cdf(pdf):
    """Computes the cumulative distribution function (CDF) from the PDF."""
    cdf = np.cumsum(pdf)
    cdf = cdf / cdf[-1]  # Normalize to range [0,1]
    return cdf

def match_histogram(original_pdf, specified_pdf):
    """Finds the mapping function to match original PDF to specified PDF."""
    original_cdf = compute_cdf(original_pdf)
    specified_cdf = compute_cdf(specified_pdf)

    # Create mapping using interpolation
    mapping = np.interp(original_cdf, specified_cdf, np.arange(256))
    return mapping.astype(np.uint8)

def apply_histogram_specification(original_image, mappings):
    """Applies histogram specification using precomputed mapping functions."""
    channels = cv2.split(original_image)
    matched_channels = [cv2.LUT(channels[i], mappings[i]) for i in range(3)]
    return cv2.merge(matched_channels)


image_path = './Assignment3/Moon.jpg'
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

image_path_spec = './Assignment3/nasa-sun.jpg'
image_spec = cv2.imread(image_path_spec)
image_rgb_spec = cv2.cvtColor(image_spec, cv2.COLOR_BGR2RGB)

red_channel = image_rgb[:, :, 0]  # Red channel
green_channel = image_rgb[:, :, 1]  # Green channel
blue_channel = image_rgb[:, :, 2]  # Blue channel

red_channel_spec = image_rgb_spec[:, :, 0]  # Red channel
green_channel_spec = image_rgb_spec[:, :, 1]  # Green channel
blue_channel_spec = image_rgb_spec[:, :, 2]  # Blue channel


r_pdf = createMap(red_channel)
g_pdf = createMap(green_channel)
b_pdf = createMap(blue_channel)

red_spec = createMap(red_channel_spec)
green_spec = createMap(green_channel_spec)
blue_spec = createMap(blue_channel_spec)

if len(r_pdf) != 256:
    raise ValueError("original must have exactly 256 values!")

if len(red_spec) != 256:
    raise ValueError("excel must have exactly 256 values!")

# Compute mapping functions for R, G, B
r_map = match_histogram(r_pdf, red_spec)
g_map = match_histogram(g_pdf, green_spec)
b_map = match_histogram(b_pdf, blue_spec)

original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Apply histogram specification
specified_image = apply_histogram_specification(original_image, [r_map, g_map, b_map])

specified_image_bgr = cv2.cvtColor(specified_image, cv2.COLOR_RGB2BGR)
cv2.imwrite('./Assignment3/Histogram_Specified_Moon_Nasa_Sun.jpg', specified_image_bgr)
