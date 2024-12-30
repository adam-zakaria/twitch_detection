import cv2 as cv
import sys

img = cv.imread("double_kill_full_image.png")
cv.imshow("Image", img)  # Display the image
roi = cv.selectROI("Image", img) # Select the ROI
cv.destroyWindow("Image")  # Close the specific window

x, y, w, h = roi  # Extract coordinates and dimensions
print(f"ROI: x={x}, y={y}, width={w}, height={h}")

roi_cropped = img[y:y+h, x:x+w]
cv.imshow("Cropped ROI", roi_cropped)
cv.waitKey(0)
sys.exit()
#cv.destroyAllWindows()  # Close all windows

# a more narrow column selection
# ROI: x=748, y=453, width=42, height=184
# if scanning left to right (which is actually saying were moving down the column), trying to understand the risk of missing the medal entirely.
# My intuition is that if we're scanning the size of the medal we can't miss it my more than half.
"""
Well, it is an issue if the top of medal gets compared to the bottom of the medal...

But we're asking, in the worst case, does this bounding box compare at least say 25% of the medal? So we could split the medal into 4 sections and compare each section to each of the bounding box.
"""
