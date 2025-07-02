#!/usr/bin/env python3
"""
Fixed-parameter video cropper.
Just edit the constants below and run the script:  python reframe_video_fixed.py
"""

import cv2
from pathlib import Path
import sys

# ------------------------------------------------------------------
# EDIT THESE VALUES
INPUT_PATH = '/Users/azakaria/Code/twitch_detections/test/videos/aqua_no_dks.mov'
OUTPUT_PATH = '/Users/azakaria/Code/twitch_detections/test/videos/aqua_no_dks_reframe.mp4'

# ROI (Region of Interest): x, y, width, height
ROI = (710, 479, 62, 52)                    # ← replace with your own numbers
# ------------------------------------------------------------------

def main() -> None:
    x, y, w, h = ROI

    if not Path(INPUT_PATH).exists():
        sys.exit(f"Input file not found: {INPUT_PATH}")

    cap = cv2.VideoCapture(INPUT_PATH)
    if not cap.isOpened():
        sys.exit(f"Cannot open video: {INPUT_PATH}")

    fps   = cap.get(cv2.CAP_PROP_FPS)
    fourc = cv2.VideoWriter_fourcc(*"mp4v")     # change codec if desired
    out   = cv2.VideoWriter(OUTPUT_PATH, fourc, fps, (w, h))

    frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Processing {frame_cnt} frames…")
    print(f"ROI = (x={x}, y={y}, w={w}, h={h})")

    for idx in range(frame_cnt):
        ret, frame = cap.read()
        if not ret:
            print(f"Finished early at frame {idx}")   # in case of truncated files
            break
        crop = frame[y:y+h, x:x+w]
        out.write(crop)

        if idx % 100 == 0:
            print(f"…{idx}/{frame_cnt}")

    cap.release()
    out.release()
    print(f"Saved cropped video to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()