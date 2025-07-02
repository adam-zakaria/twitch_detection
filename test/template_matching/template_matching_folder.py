#!/usr/bin/env python3
"""template_matching.py

Perform template matching on an image using OpenCV.

This script loads a source image and a template image, then finds the best match
location of the template within the source image. It draws a rectangle around
the detected area and displays the result.

"""

import cv2
import sys
from pathlib import Path
import happy_utils as utils

# ---------------------------------------------------------------------------
# Hardcoded parameters
# ---------------------------------------------------------------------------



def main():
    # Define a threshold for determining if the template is present
    threshold = 0.8  # Adjust this value based on your needs
    print(f"Threshold: {threshold}")
    TEMPLATE_IMAGE_PATH = '/Users/azakaria/Code/twitch_detections/test/frames/template_matching/double_kill.png'

    for i,img_path in enumerate(utils.ls('/Users/azakaria/Code/twitch_detections/test/frames/data/train/no_double_kill')):
        SOURCE_IMAGE_PATH  = img_path
        OUTPUT_IMAGE_PATH  = f'/Users/azakaria/Code/twitch_detections/test/frames/template_matching/matched_result_{i}.png'
        # Load the source and template images
        source_image_path = Path(SOURCE_IMAGE_PATH)
        template_image_path = Path(TEMPLATE_IMAGE_PATH)

        if not source_image_path.exists() or not template_image_path.exists():
            sys.exit("Source or template image not found.")

        source_image = cv2.imread(str(source_image_path))
        template_image = cv2.imread(str(template_image_path))

        if source_image is None or template_image is None:
            sys.exit("Failed to load source or template image.")

        # Perform template matching
        result = cv2.matchTemplate(source_image, template_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Print the confidence score
        print(f"Confidence score: {max_val:.4f}")

        # Determine if the template is present
        # if max_val >= threshold:
        #     print("Template is present in the image.")
        # else:
        #     print("Template is not present in the image.")

        # Draw a rectangle around the matched region
        h, w = template_image.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(source_image, top_left, bottom_right, (0, 255, 0), 2)

        # Save and display the result
        # cv2.imwrite(OUTPUT_IMAGE_PATH, source_image)
        # cv2.imshow('Matched Result', source_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # print(f"Matched result saved to {OUTPUT_IMAGE_PATH}")


if __name__ == '__main__':
    main() 