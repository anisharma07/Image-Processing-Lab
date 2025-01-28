#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>

// Function to create a height map from the grayscale image
std::vector<std::vector<float>> createHeightMap(const cv::Mat& grayImage) {
    std::vector<std::vector<float>> heightMap(grayImage.rows, std::vector<float>(grayImage.cols, 0));
    for (int i = 0; i < grayImage.rows; i++) {
        for (int j = 0; j < grayImage.cols; j++) {
            heightMap[i][j] = static_cast<float>(grayImage.at<uchar>(i, j));
        }
    }
    return heightMap;
}

int main() {
    // Load the image
    cv::Mat image = cv::imread("image3.jpg", cv::IMREAD_COLOR);
    if (image.empty()) {
        std::cerr << "Error: Unable to load image." << std::endl;
        return -1;
    }

    // Convert to grayscale
    cv::Mat grayImage;
    cv::cvtColor(image, grayImage, cv::COLOR_BGR2GRAY);

    // Generate height map
    auto heightMap = createHeightMap(grayImage);

    // Print the height map
    for (const auto& row : heightMap) {
        for (const auto& value : row) {
            std::cout << value << " ";
        }
        std::cout << std::endl;
        std::cout << std::endl;
    }

    std::cout << "Height map generated. Use OpenGL for visualization." << std::endl;

    return 0;
}