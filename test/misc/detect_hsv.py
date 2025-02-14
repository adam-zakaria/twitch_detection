"""
Outputs attemped_detections/*.jpg

It's not working well: the template image is large than the medal in the input image, and the bounding boxes are about half the size of the medal in the input image.

I really think rgb is a better approach.
"""

import cv2 as cv
import numpy as np
import os


def detect_medal(frame, roi_x, roi_y, roi_width, roi_height, frame_count):
    # Create output directory if it doesn't exist
    output_dir = "attempted_detections_hsv"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load template and calculate histograms (Do this ONCE)
    template = cv.imread("double_kill_medal.png")
    # Convert template from BGR to HSV color space for more robust color matching
    template_hsv = cv.cvtColor(template, cv.COLOR_BGR2HSV)

    # Calculate histograms for each HSV channel separately
    # histogram used to get information about the overall distribution of colors in the image
    # Hue: 180 bins (OpenCV uses 0-180 range for Hue)
    h_hist_template = cv.calcHist([template_hsv], [0], None, [180], [0, 180])
    # Saturation: 256 bins (0-255 range)
    s_hist_template = cv.calcHist([template_hsv], [1], None, [256], [0, 256])
    # Value: 256 bins (0-255 range)
    v_hist_template = cv.calcHist([template_hsv], [2], None, [256], [0, 256])

    # Extract the ROI 
    roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    if roi.size == 0:
        return False

    # Create an even wider visualization image to fit all the text (add 300 pixels width)
    roi_viz = np.zeros((roi.shape[0], roi.shape[1] + 300, 3), dtype=np.uint8)
    roi_viz[:, :roi.shape[1]] = roi  # Copy ROI to the left side

    # show the roi
    cv.imshow("ROI",roi)

    # template.shape returns a tuple (height, width, channels)
    # just return the first two
    template_height, template_width = template.shape[:2]

    # Get dimensions of both images
    template_h, template_w = template.shape[:2]
    roi_h, roi_w = roi_viz.shape[:2]

    # Calculate the width of each section
    column_width = template_width  # Width of the middle section (where BBs go)
    text_section_width = roi_w - template_width  # Width of the remaining text section

    # Create visualization with exact width needed
    total_width = template_w + column_width + text_section_width
    max_height = max(template_h, roi_h)
    combined_viz = np.zeros((max_height, total_width, 3), dtype=np.uint8)

    # Draw the template on the far left
    combined_viz[0:template_h, 0:template_w] = template

    # Draw the ROI column in the middle (right after template)
    middle_start = template_w
    combined_viz[0:roi_h, middle_start:middle_start + column_width] = roi_viz[:, :column_width]

    # Draw the text portion on the far right
    text_start = middle_start + column_width
    combined_viz[0:roi_h, text_start:text_start + text_section_width] = roi_viz[:, column_width:]

    # Scan down the ROI, moving by 25% of the bounding box height
    scan_step = template_height // 4  # Integer division (approximately 13)

    # Moves down the ROI, moving by 25% of the bounding box height (ROI has already been extracted from input image)
    for y in range(0, roi.shape[0] - template_height + 1, scan_step):
        # Get the region we're checking
        check_region = roi[y:y + template_height, 0:template_width]
        
        # Convert region to HSV
        hsv_region = cv.cvtColor(check_region, cv.COLOR_BGR2HSV)
        
        # Calculate mean HSV values for region
        mean_h_region = np.mean(hsv_region[:,:,0])
        mean_s_region = np.mean(hsv_region[:,:,1])
        mean_v_region = np.mean(hsv_region[:,:,2])

        # Get template HSV means (assuming template_hsv is already calculated)
        mean_h_template = np.mean(template_hsv[:,:,0])
        mean_s_template = np.mean(template_hsv[:,:,1])
        mean_v_template = np.mean(template_hsv[:,:,2])

        # Calculate histograms for the region
        h_hist_bb = cv.calcHist([hsv_region], [0], None, [180], [0, 180])
        s_hist_bb = cv.calcHist([hsv_region], [1], None, [256], [0, 256])
        v_hist_bb = cv.calcHist([hsv_region], [2], None, [256], [0, 256])

        # Compare histograms using correlation
        h_correlation = cv.compareHist(h_hist_template, h_hist_bb, cv.HISTCMP_CORREL)
        s_correlation = cv.compareHist(s_hist_template, s_hist_bb, cv.HISTCMP_CORREL)
        v_correlation = cv.compareHist(v_hist_template, v_hist_bb, cv.HISTCMP_CORREL)

        # Combine the correlations (average them)
        overall_correlation = (h_correlation + s_correlation + v_correlation) / 3

        # Calculate the offset where the column starts
        column_start_x = template_w + (roi_w - template_width)  # This aligns with the original column position

        # Draw bounding boxes in the middle section
        cv.rectangle(combined_viz, 
                    (middle_start, y),
                    (middle_start + template_width, y + template_height), 
                    (255, 0, 0), 
                    1)
        
        # Define column positions
        col1_x = roi.shape[1] + 5          # Correlation
        col2_x = roi.shape[1] + 100        # H values
        col3_x = roi.shape[1] + 180        # S values
        col4_x = roi.shape[1] + 260        # V values
        
        # Calculate vertical position (centered with box)
        text_y = y + template_height//2

        # Write each value in its own column
        cv.putText(combined_viz, f"Corr: {overall_correlation:.2f}", 
                  (col1_x, text_y), 
                  cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        cv.putText(combined_viz, f"H: {mean_h_region:.0f}/{mean_h_template:.0f}", 
                  (col2_x, text_y), 
                  cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        cv.putText(combined_viz, f"S: {mean_s_region:.0f}/{mean_s_template:.0f}", 
                  (col3_x, text_y), 
                  cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        cv.putText(combined_viz, f"V: {mean_v_region:.0f}/{mean_v_template:.0f}", 
                  (col4_x, text_y), 
                  cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        if overall_correlation > 0.8:
            # Draw matching box in green
            cv.rectangle(combined_viz, (template_w, y), (template_w + template_width, y + template_height), (0, 255, 0), 2)
            # Save the visualization
            cv.imwrite(f"{output_dir}/frame_{frame_count}_detection.jpg", combined_viz)
            return True
    
    # Save attempt even if no detection
    cv.imwrite(f"{output_dir}/frame_{frame_count}_attempts.jpg", combined_viz)
    return False

if __name__ == "__main__":
  # Define the ROI (adjust these values)
  roi_x = 748
  roi_y = 453
  roi_width = 42  # Template width
  roi_height = 184 # Template height

  cap = cv.VideoCapture("combined_frames.mp4")
  frame_count = 0
  while cap.isOpened():
      ret, frame = cap.read()
      if not ret:
          break
      if detect_medal(frame, roi_x, roi_y, roi_width, roi_height, frame_count):
          print(f"Medal Detected in frame {frame_count}!")
      frame_count += 1
      cv.rectangle(frame,(roi_x,roi_y),(roi_x+roi_width,roi_y+roi_height),(0,255,0),2)
      cv.imshow("Frame",frame)
      if cv.waitKey(1) & 0xFF == ord('q'):
          break
  cap.release()
  cv.destroyAllWindows()