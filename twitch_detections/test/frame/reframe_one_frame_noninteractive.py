#!/usr/bin/env python3
"""reframe_one_frame_noninteractive.py

Accept ROI coordinates and save the cropped region from a single image.

Usage
-----
Provide the ROI coordinates (x, y, w, h) as input to the script.

"""
from __future__ import annotations
import sys
from pathlib import Path
import cv2

IMAGE_PATH = '/Users/azakaria/Code/twitch_detections/test/frames/extracted_frames_all_dks/frame_000113.png'
OUTPUT_PATH = '/Users/azakaria/Code/twitch_detections/test/frames/template_matching/double_kill.png'

# Example ROI coordinates
ROI_COORDS = (12, 6, 40, 40)

def main() -> None:
    ipath = Path(IMAGE_PATH)

    if not ipath.exists():
        sys.exit(f"Image not found: {ipath}")

    image = cv2.imread(str(ipath))
    if image is None:
        sys.exit(f"Cannot open image: {ipath}")

    x, y, w, h = ROI_COORDS
    crop = image[y:y+h, x:x+w]

    out_path = Path(OUTPUT_PATH)
    cv2.imwrite(str(out_path), crop)
    print(f"Saved ROI to {out_path}")
    print(f"ROI coordinates (x, y, w, h): {ROI_COORDS}")


if __name__ == '__main__':
    main()
