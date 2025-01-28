#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <GL/glut.h>
#include<bits/stdc++.h>

using namespace std;

// Function to create a height map from a single channel image
vector<int> createHeightMap(const cv::Mat& channelImage) {
    vector<int> heightMap(256, 0);
    for (int i = 0; i < channelImage.rows; i++) {
        for (int j = 0; j < channelImage.cols; j++) {
            heightMap[(int)channelImage.at<uchar>(i, j)]+=1 ;
        }
    }
    return heightMap;
}

// Function to compute the histogram for a single channel image
std::vector<int> computeHistogram(const cv::Mat& channelImage) {
    std::vector<int> histogram(256, 0);
    for (int i = 0; i < channelImage.rows; i++) {
        for (int j = 0; j < channelImage.cols; j++) {
            int intensity = channelImage.at<uchar>(i, j);
            histogram[intensity]++;
        }
    }
    return histogram;
}

// Function to render the histogram using OpenGL


void renderHistogram(const std::vector<int>& histogram, const std::string& color, int maxFreq) {
    if (!glfwInit()) {
        std::cerr << "Failed to initialize GLFW" << std::endl;
        return;
    }

    int argc = 1;
    char* argv[1] = {(char*)"Something"};
    glutInit(&argc, argv); // Initialize GLUT

    GLFWwindow* window = glfwCreateWindow(1200, 900, "Histogram Visualization", NULL, NULL);
    if (!window) {
        std::cerr << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return;
    }

    glfwMakeContextCurrent(window);
    glewExperimental = GL_TRUE;
    if (glewInit() != GLEW_OK) {
        std::cerr << "Failed to initialize GLEW" << std::endl;
        return;
    }

    // Scaling factor and margin
    float scaleFactor = 0.8f;
    float margin = maxFreq * 0.1f; // 10% of maxFreq as margin

    while (!glfwWindowShouldClose(window)) {
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        // Set up the orthographic projection with a bottom margin
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glOrtho(0.0, histogram.size(), -margin, maxFreq, -1.0, 1.0); // Add margin at the bottom
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();

        // Draw the histogram
        glBegin(GL_LINES);
        for (size_t i = 0; i < histogram.size(); i++) {
            float intensity = static_cast<float>(i);
            float frequency = static_cast<float>(histogram[i]) * scaleFactor;

            if (color == "red") {
                glColor3f(1.0f, 0.0f, 0.0f);
            } else if (color == "green") {
                glColor3f(0.0f, 1.0f, 0.0f);
            } else if (color == "blue") {
                glColor3f(0.0f, 0.0f, 1.0f);
            }

            glVertex2f(intensity, 0.0f);
            glVertex2f(intensity, frequency);
        }
        glEnd();

        // Draw axis lines
        glColor3f(1.0f, 1.0f, 1.0f);
        glBegin(GL_LINES);
        glVertex2f(0.0f, 0.0f);  // X-axis
        glVertex2f(histogram.size(), 0.0f);
        glVertex2f(0.0f, 0.0f);  // Y-axis
        glVertex2f(0.0f, maxFreq);
        glEnd();

        // Add frequency markings on the Y-axis
        int numMarks = 10; // Number of marks (e.g., 10% intervals)
        for (int i = 0; i <= numMarks; i++) {
            float freq = (maxFreq / numMarks) * i;
            glRasterPos2f(-3.0f, freq); // Adjust position
            std::string freqLabel = std::to_string(static_cast<int>(freq));
            for (const char& c : freqLabel) {
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, c);
            }
        }

        // Add "Frequency" label on Y-axis
        glRasterPos2f(-10.0f, maxFreq / 2.0f); // Position it in the middle of the Y-axis
        const char* ylabel = "Frequency";
        for (const char* c = ylabel; *c != '\0'; c++) {
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, *c);
        }

        // Add max frequency label at the top
        glRasterPos2f(histogram.size() - 20.0f, maxFreq - 10.0f);
        std::string maxFreqLabel = "Max: " + std::to_string(maxFreq);
        for (const char& c : maxFreqLabel) {
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, c);
        }

        // Add X-axis labels (0 to 255)
        for (int i = 0; i <= 255; i += 20) { // Label every 20 units
            glRasterPos2f(i, -margin * 0.3f); // Slightly below the X-axis
            std::string xLabel = std::to_string(i);
            for (const char& c : xLabel) {
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, c); // Small font
            }
        }

        // Add X-axis label
        glRasterPos2f(histogram.size() / 2.0f, -margin * 0.7f); // Use margin for spacing
        const char* xlabel = "Intensity";
        for (const char* c = xlabel; *c != '\0'; c++) {
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, *c);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glfwDestroyWindow(window);
    glfwTerminate();
}




int main() {
    // Load the image
    cv::Mat image = cv::imread("../assets/Images/Exp1/nuts.png", cv::IMREAD_COLOR);
    if (image.empty()) {
        std::cerr << "Error: Unable to load image." << std::endl;
        return -1;
    }

    // Split the image into R, G, B channels
    std::vector<cv::Mat> channels(3);
    cv::split(image, channels);
    cv::Mat redChannel = channels[2];   // Red channel
    cv::Mat greenChannel = channels[1]; // Green channel
    cv::Mat blueChannel = channels[0];  // Blue channel

    // Compute histograms for each channel
    auto redHistogram = computeHistogram(redChannel);
    auto greenHistogram = computeHistogram(greenChannel);
    auto blueHistogram = computeHistogram(blueChannel);
    int mfGreen = 0, mfRed =0, mfBlue =0;

   for (int i = 0; i < 256; i++) {
   if(greenHistogram[i]) cout<<greenHistogram[i] << " "<< i <<endl;
    mfGreen = max(mfGreen, greenHistogram[i]);
    mfRed = max(mfRed, redHistogram[i]);
    mfBlue = max(mfBlue, blueHistogram[i]);
    }

    // Render histograms using OpenGL
    // renderHistogram(redHistogram, "red", mfRed);
    renderHistogram(greenHistogram, "green", mfGreen);
    // renderHistogram(blueHistogram, "blue", mfBlue);

    return 0;
}