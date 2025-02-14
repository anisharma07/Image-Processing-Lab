import matplotlib.pyplot as plt
from PIL import Image

def compute_histogram(channel):
    histogram = [0] * 256
    for row in channel:
        for pixel in row:
            histogram[pixel] += 1
    return histogram

def compute_cdf(histogram, total_pixels):
    cdf = [0] * 256
    cumulative_sum = 0
    for i in range(256):
        cumulative_sum += histogram[i]
        cdf[i] = round((cumulative_sum / total_pixels) * 255)
    return cdf

def apply_histogram_equalization(channel, cdf):
    equalized_channel = [[cdf[pixel] for pixel in row] for row in channel]
    return equalized_channel

def process_image(image_path):
    image = Image.open(image_path).convert('RGB')
    width, height = image.size
    pixels = list(image.getdata())
    
    r_channel = [[pixels[i * width + j][0] for j in range(width)] for i in range(height)]
    g_channel = [[pixels[i * width + j][1] for j in range(width)] for i in range(height)]
    b_channel = [[pixels[i * width + j][2] for j in range(width)] for i in range(height)]
    
    r_histogram = compute_histogram(r_channel)
    g_histogram = compute_histogram(g_channel)
    b_histogram = compute_histogram(b_channel)
    
    total_pixels = width * height
    r_cdf = compute_cdf(r_histogram, total_pixels)
    g_cdf = compute_cdf(g_histogram, total_pixels)
    b_cdf = compute_cdf(b_histogram, total_pixels)
    
    r_eq = apply_histogram_equalization(r_channel, r_cdf)
    g_eq = apply_histogram_equalization(g_channel, g_cdf)
    b_eq = apply_histogram_equalization(b_channel, b_cdf)
    
    equalized_pixels = [(r_eq[i][j], g_eq[i][j], b_eq[i][j]) for i in range(height) for j in range(width)]
    equalized_image = Image.new('RGB', (width, height))
    equalized_image.putdata(equalized_pixels)
    
    return image, equalized_image

image_path = '../assets/ass2/class.jpeg'  # Change path accordingly
original, equalized = process_image(image_path)

equalized.save('./Assignment2/class_equalized.png')
original.save('./Assignment2/class.png')


# plt.figure(figsize=(10, 5))
# plt.subplot(1, 2, 1)
# plt.imshow(original)
# plt.title('Original Image')
# plt.axis('off')

# plt.subplot(1, 2, 2)
# plt.imshow(equalized)
# plt.title('Equalized Image')
# plt.axis('off')

# plt.show()
