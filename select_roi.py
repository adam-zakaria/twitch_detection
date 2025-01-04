import cv2 as cv
import sys
import argparse

# Set up CLI argument parsing
parser = argparse.ArgumentParser(description='Select and crop ROI from an image.')
parser.add_argument('filename', type=str, help='Path to the image file')
args = parser.parse_args()

# Read the image from the provided filename
img = cv.imread(args.filename)

# Check if the image was loaded successfully
if img is None:
    print(f"Error: Unable to load image {args.filename}")
    sys.exit()

cv.imshow("Image", img)  # Display the image
roi = cv.selectROI("Image", img)  # Select the ROI
cv.destroyWindow("Image")  # Close the specific window

x, y, w, h = roi  # Extract coordinates and dimensions
print(f"ROI: x={x}, y={y}, width={w}, height={h}")

# Crop the ROI from the image
roi_cropped = img[y:y+h, x:x+w]
cv.imshow("Cropped ROI", roi_cropped)
cv.waitKey(0)
cv.destroyAllWindows()  # Close all windows
sys.exit()
