import cv2 as cv

img = cv.imread("your_image.jpg")
cv.imshow("Image", img)  # Display the image
roi = cv.selectROI("Image", img) # Select the ROI
cv.destroyAllWindows()

x, y, w, h = roi  # Extract coordinates and dimensions
print(f"ROI: x={x}, y={y}, width={w}, height={h}")

roi_cropped = img[y:y+h, x:x+w]
cv.imshow("Cropped ROI",roi_cropped)
cv.waitKey(0)
cv.destroyAllWindows()