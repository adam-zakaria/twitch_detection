#!/usr/bin/env python3
"""reframe_one_frame_interactive.py

Interactively select an ROI on a single image and save the cropped region.

Controls
--------
• 's'                : select ROI on the image
• 'q'                : quit

After you press 's' and draw the rectangle, press Space or Enter to accept
(OpenCV's default behaviour).  The script then saves the crop and prints the
(x, y, w, h) coordinates so you can reuse them elsewhere.

"""
from __future__ import annotations
import sys
from pathlib import Path
import cv2

IMAGE_PATH = '/Users/azakaria/Code/twitch_detections/twitch_detections/test/template_matching/double_kill.png'
#OUTPUT_PATH = '/Users/azakaria/Code/twitch_detections/test/frames/template_matching/double_kill_tighter.png'
OUTPUT_PATH = 'double_kill_tighter.png'

def main() -> None:
    ipath = Path(IMAGE_PATH)

    if not ipath.exists():
        sys.exit(f"Image not found: {ipath}")

    image = cv2.imread(str(ipath))
    if image is None:
        sys.exit(f"Cannot open image: {ipath}")

    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Image', image)

    print("Controls: 's' select ROI | 'q' quit")

    roi_coords: tuple[int, int, int, int] | None = None

    while True:
        key = cv2.waitKey(0) & 0xFF
        if key == ord('s'):
            # ROI selection dialog
            x, y, w, h = cv2.selectROI('Select ROI', image, showCrosshair=True, fromCenter=False)
            cv2.destroyWindow('Select ROI')
            if w == 0 or h == 0:
                print("Empty ROI—try again")
                continue
            roi_coords = (int(x), int(y), int(w), int(h))
            break
        elif key == ord('q'):
            print("Quit without selecting ROI")
            cv2.destroyAllWindows()
            return
        # else: loop continues

    cv2.destroyWindow('Image')

    if roi_coords is None:
        print("No ROI selected; exiting.")
        return

    x, y, w, h = roi_coords
    crop = image[y:y+h, x:x+w]

    out_path = Path(OUTPUT_PATH)
    cv2.imwrite(str(out_path), crop)
    print(f"Saved ROI to {out_path}")
    print(f"ROI coordinates (x, y, w, h): {roi_coords}")


if __name__ == '__main__':
    main()
