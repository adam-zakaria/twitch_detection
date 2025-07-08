"""
"""
import cv2 as cv
import numpy as np
import os

# Create output directory if it doesn't exist
output_dir = "attempted_detections_rgb"
os.makedirs(output_dir, exist_ok=True)

# Define the ROI (adjust these values)
roi_x = 748
roi_y = 453
roi_width = 42  # Template width
roi_height = 184 # Template height

# Load and get template dimensions
template = cv.imread("double_kill_medal.png")
template_height, template_width = template.shape[:2]

# Calculate step size (1/4 of template height)
step_size = template_height // 4

# Process video frames
cap = cv.VideoCapture("combined_frames.mp4")
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    # Extract ROI from this frame
    roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    roi_viz = roi.copy()
    
    print(f"\nFrame {frame_count}")
    # Scan vertically down the column
    for y in range(0, roi_height - template_height + 1, step_size):
        # Get the region we're checking
        bb_region = roi[y:y + template_height, 0:template_width]
        
        # Calculate mean RGB values for the region
        mean_rgb = cv.mean(bb_region)[:3]  # Get only RGB values (ignore alpha)
        print(f"BB at y={y}")
        print(f"Mean RGB: R={r}, G={g}, B={b} {color_block}")
        
        # Draw bounding boxes
        cv.rectangle(roi_viz, 
                    (0, y),
                    (template_width, y + template_height), 
                    (255, 0, 0), 
                    1)
    
    # Save ROI visualization
    cv.imwrite(f"{output_dir}/frame_{frame_count}.jpg", roi_viz)
    
    frame_count += 1
    
    # Display (optional)
    cv.imshow("ROI", roi_viz)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()


