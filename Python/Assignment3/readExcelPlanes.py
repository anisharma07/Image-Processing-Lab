import pandas as pd

# Read the Excel file
df = pd.read_excel('./Assignment3/HistogramSpecificationData.xlsx', header=None)

# Check the shape of the DataFrame
print("DataFrame shape:", df.shape)

# Extract the PDFs for each channel
red_pdf = df.iloc[:, 0].tolist()
blue_pdf = df.iloc[:, 1].tolist()
green_pdf = df.iloc[:, 2].tolist()

# Check the lengths of the extracted lists
print("Length of red_pdf:", len(red_pdf))
print("Length of blue_pdf:", len(blue_pdf))
print("Length of green_pdf:", len(green_pdf))

# Print the last few values to verify
print("Last few values of red_pdf:", red_pdf[-5:])
print("Last few values of blue_pdf:", blue_pdf[-5:])
print("Last few values of green_pdf:", green_pdf[-5:])