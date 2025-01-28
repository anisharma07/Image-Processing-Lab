#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <cmath>

#pragma pack(push, 1)
struct BMPHeader {
    uint16_t bfType;       // File type
    uint32_t bfSize;       // File size in bytes
    uint16_t bfReserved1;  // Reserved
    uint16_t bfReserved2;  // Reserved
    uint32_t bfOffBits;    // Offset to image data
};

struct BMPInfoHeader {
    uint32_t biSize;          // Size of this header
    int32_t biWidth;          // Width of the image
    int32_t biHeight;         // Height of the image
    uint16_t biPlanes;        // Number of color planes
    uint16_t biBitCount;      // Bits per pixel
    uint32_t biCompression;   // Compression type
    uint32_t biSizeImage;     // Image size in bytes
    int32_t biXPelsPerMeter;  // Pixels per meter in X
    int32_t biYPelsPerMeter;  // Pixels per meter in Y
    uint32_t biClrUsed;       // Number of colors used
    uint32_t biClrImportant;  // Important colors
};
#pragma pack(pop)

struct Pixel {
    uint8_t blue;
    uint8_t green;
    uint8_t red;
};

void readBMP(const std::string& filename, BMPHeader& header, BMPInfoHeader& infoHeader, std::vector<std::vector<Pixel>>& pixels) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "Error opening file!" << std::endl;
        exit(1);
    }

    // Read headers
    file.read(reinterpret_cast<char*>(&header), sizeof(header));
    file.read(reinterpret_cast<char*>(&infoHeader), sizeof(infoHeader));

    // Check if it's a 24-bit BMP file
    if (header.bfType != 0x4D42 || infoHeader.biBitCount != 24) {
        std::cerr << "Unsupported file format or bit depth!" << std::endl;
        exit(1);
    }

    // Move to the pixel data
    file.seekg(header.bfOffBits, std::ios::beg);

    // Read pixel data
    int rowPadding = (4 - (infoHeader.biWidth * 3) % 4) % 4;
    pixels.resize(infoHeader.biHeight, std::vector<Pixel>(infoHeader.biWidth));

    for (int i = 0; i < infoHeader.biHeight; ++i) {
        for (int j = 0; j < infoHeader.biWidth; ++j) {
            file.read(reinterpret_cast<char*>(&pixels[i][j]), sizeof(Pixel));
        }
        file.ignore(rowPadding); // Skip padding
    }
}

void writeBMP(const std::string& filename, const BMPHeader& header, const BMPInfoHeader& infoHeader, const std::vector<std::vector<Pixel>>& pixels) {
    std::ofstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "Error creating file!" << std::endl;
        exit(1);
    }

    // Write headers
    file.write(reinterpret_cast<const char*>(&header), sizeof(header));
    file.write(reinterpret_cast<const char*>(&infoHeader), sizeof(infoHeader));

    // Write pixel data
    int rowPadding = (4 - (infoHeader.biWidth * 3) % 4) % 4;
    uint8_t padding[3] = {0};

    for (const auto& row : pixels) {
        for (const auto& pixel : row) {
            file.write(reinterpret_cast<const char*>(&pixel), sizeof(Pixel));
        }
        file.write(reinterpret_cast<const char*>(padding), rowPadding); // Add padding
    }
}

void intensityAveraging(std::vector<std::vector<Pixel>>& pixels) {
    for (auto& row : pixels) {
        for (auto& pixel : row) {
            uint8_t average = (pixel.red + pixel.green + pixel.blue) / 3;
            pixel.red = pixel.green = pixel.blue = average;
        }
    }
}

void inversion(std::vector<std::vector<Pixel>>& pixels) {
    for (auto& row : pixels) {
        for (auto& pixel : row) {
            pixel.red = 255 - pixel.red;
            pixel.green = 255 - pixel.green;
            pixel.blue = 255 - pixel.blue;
        }
    }
}

void subSampling(std::vector<std::vector<Pixel>>& pixels, int factor) {
    int newHeight = pixels.size() / factor;
    int newWidth = pixels[0].size() / factor;

    std::vector<std::vector<Pixel>> newPixels(newHeight, std::vector<Pixel>(newWidth));

    for (int i = 0; i < newHeight; ++i) {
        for (int j = 0; j < newWidth; ++j) {
            newPixels[i][j] = pixels[i * factor][j * factor];
        }
    }

    pixels = std::move(newPixels);
}

int main() {
    BMPHeader header;
    BMPInfoHeader infoHeader;
    std::vector<std::vector<Pixel>> pixels;

    std::string inputFile = "../assets/ass1/boats.bmp";
    std::string outputAverage = "output_average.bmp";
    std::string outputInversion = "output_inversion.bmp";
    std::string outputSubSampled = "output_subsampled.bmp";

    // Read BMP file
    readBMP(inputFile, header, infoHeader, pixels);

    // Intensity Averaging
    auto averagePixels = pixels;
    intensityAveraging(averagePixels);
    writeBMP(outputAverage, header, infoHeader, averagePixels);

    // Inversion
    auto invertedPixels = pixels;
    inversion(invertedPixels);
    writeBMP(outputInversion, header, infoHeader, invertedPixels);

    // Sub-sampling
    auto subSampledPixels = pixels;
    subSampling(subSampledPixels, 2); // Sub-sample by a factor of 2
    infoHeader.biWidth /= 2;
    infoHeader.biHeight /= 2;
    writeBMP(outputSubSampled, header, infoHeader, subSampledPixels);

    std::cout << "Processing completed. Check the output files!" << std::endl;
    return 0;
}
