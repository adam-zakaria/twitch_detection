import cv2 as cv
import numpy as np
import os

# Create output directory if it doesn't exist
output_dir = "rgb"
os.makedirs(output_dir, exist_ok=True)

# Define bounding box dimensions
bb_width = 100
bb_height = 50

# Load input image
image = cv.imread("rgb.png")
height, width = image.shape[:2]

# Create visualization image
viz = image.copy()

# Scan down the image
for y in range(0, height - bb_height + 1, 25):
    # Get the region we're checking
    bb_region = image[y:y + bb_height, 0:bb_width]
    
    # Calculate mean RGB values for the region
    mean_rgb = cv.mean(bb_region)[:3]  # Get only RGB values (ignore alpha)
    r, g, b = int(mean_rgb[2]), int(mean_rgb[1]), int(mean_rgb[0])
    
    # Create colored block using ANSI escape codes
    color_block = f"\x1b[48;2;{r};{g};{b}m    \x1b[0m"
    
    # Print RGB values with color block
    print(f"BB at y={y}")
    print(f"Mean RGB: R={r}, G={g}, B={b} {color_block}")

    
    
    # Create a copy for this iteration
    current_viz = image.copy()
    
    # Draw bounding box
    cv.rectangle(current_viz, 
                (0, y),
                (bb_width, y + bb_height), 
                (255, 0, 0), 
                1)
    
    # Save each iteration
    cv.imwrite(f"{output_dir}/rgb_scan_{y:04d}.jpg", current_viz)

# Save final visualization
cv.imwrite(f"{output_dir}/rgb_viz.jpg", viz)

# Display (optional)
cv.imshow("Visualization", viz)
cv.waitKey(0)
cv.destroyAllWindows()