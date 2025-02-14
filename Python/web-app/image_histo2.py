from flask import Flask, render_template, request
from PIL import Image, ImageOps
import numpy as np
import io
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import cv2

app = Flask(__name__)

def log_transform(image, c):
    img_array = np.array(image, dtype=np.float32)
    img_array = c * np.log(1 + img_array)
    img_array = np.uint8(img_array / np.max(img_array) * 255)
    img_transformed = Image.fromarray(img_array)
    return img_transformed

def contrast_stretching(image):
    img_array = np.array(image, dtype=np.float32)
    min_val = np.min(img_array)
    max_val = np.max(img_array)
    stretched = (img_array - min_val) * (255.0 / (max_val - min_val))
    stretched = np.clip(stretched, 0, 255).astype(np.uint8)
    stretched_image = Image.fromarray(stretched)
    return stretched_image

def power_transform(image, gamma, c=1):
    image_array = np.array(image) / 255.0
    power_image = c * np.power(image_array, gamma)
    power_image = np.clip(power_image, 0, 1) * 255
    return Image.fromarray(power_image.astype(np.uint8))

def image_to_base64(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"

def createMap(intMap):
    freqMap = [0]*256
    for row in intMap:
        for val in row:
            freqMap[val] += 1
    return freqMap

def histogram_to_base64(image):
    """
    Generate and return the base64-encoded histogram image of the input image.
    """
    image_rgb = np.array(image.convert('RGB'))
    red_channel = image_rgb[:, :, 0]
    green_channel = image_rgb[:, :, 1]
    blue_channel = image_rgb[:, :, 2]

    # Calculate histograms for each channel
    r_hist = createMap(red_channel)
    g_hist = createMap(green_channel)
    b_hist = createMap(blue_channel)

    # Get the total number of pixels
    total_pixels = image_rgb.shape[0] * image_rgb.shape[1]

    # Convert histograms to probability distributions
    r_prob = [count / total_pixels for count in r_hist]
    g_prob = [count / total_pixels for count in g_hist]
    b_prob = [count / total_pixels for count in b_hist]

    # Average the probabilities to get a mean probability distribution
    mean_prob = [(r_prob[i] + g_prob[i] + b_prob[i]) / 3 for i in range(256)]

    # Plot the histogram
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(256), mean_prob, color='blue', alpha=0.6)
    ax.set_title("Image Histogram")
    ax.set_xlabel("Pixel Intensity")
    ax.set_ylabel("Probablity")
    ax.grid()

    # Save the histogram plot to a BytesIO buffer and convert to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"

@app.route('/')
def index():
    return render_template('assignment2.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if not file:
        return "No file uploaded", 400

    image = Image.open(file).convert('L')  # Convert to grayscale
    c = float(request.form.get('c', 1.0))
    gamma = float(request.form.get('gamma', 1.0))

    log_image = log_transform(image, c)
    power_image = power_transform(image, gamma, c)
    contrast_image = contrast_stretching(image)


    original_base64 = image_to_base64(image)
    log_base64 = image_to_base64(log_image)
    power_base64 = image_to_base64(power_image)
    contrast_base64 = image_to_base64(contrast_image)

    original_hist_base64 = histogram_to_base64(image)
    log_hist_base64 = histogram_to_base64(log_image)
    power_hist_base64 = histogram_to_base64(power_image)
    contrast_hist_base64 = histogram_to_base64(contrast_image)


    return {
        'original': original_base64,
        'log': log_base64,
        'contrast': contrast_base64,
        'power': power_base64,
        'original_hist': original_hist_base64,
        'log_hist': log_hist_base64,
        'contrast_hist': contrast_hist_base64,
        'power_hist': power_hist_base64
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

