import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def createPdfMap(intMap):
    freqMap = [0] * 256
    total_pixels = intMap.shape[0] * intMap.shape[1]  # Total number of pixels
    
    for row in intMap:
        for val in row:
            freqMap[val] += 1
    
    freqMap = [freq / total_pixels for freq in freqMap]
    return freqMap

def createFreqMap(intMap):
    freqMap = [0]*256
    for row in intMap:
        for val in row:
            freqMap[val] += 1
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


image_path = './Assignment4/assets/input/head.jpg'
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

red_channel = image_rgb[:, :, 0]  # Red channel
green_channel = image_rgb[:, :, 1]  # Green channel
blue_channel = image_rgb[:, :, 2]  # Blue channel

r_pdf = createPdfMap(red_channel)
g_pdf = createPdfMap(green_channel)
b_pdf = createPdfMap(blue_channel)