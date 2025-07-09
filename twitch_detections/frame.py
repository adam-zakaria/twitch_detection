#!/usr/bin/env python3
"""
Fixed-parameter video cropper.
Just edit the constants below and run the script:  python reframe_video_fixed.py
"""

import cv2
from pathlib import Path
import sys
import os
import happy_utils as utils

def extract_all(input_path, output_path):
    # Create output directory if missing
    os.makedirs(output_path, exist_ok=True)

    # Open the video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {input_path}")

    frame_idx = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Read and save frames until the video ends
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        timestamp = frame_idx / fps
        timestamp_str = f"{int(timestamp // 3600):02}:{int((timestamp % 3600) // 60):02}:{int(timestamp % 60):02}.{int((timestamp * 1000) % 1000):03}"
        filename = f"frame_{timestamp_str}.png"
        cv2.imwrite(os.path.join(output_path, filename), frame)
        frame_idx += 1

    cap.release()
    print(f"Extracted {frame_idx} frames into '{output_path}/'")

def reframe_video(input_path='', output_dir='', x=0, y=0, w=0, h=0):
    """
    Crop a video to a fixed ROI.
    input_path: path to the input video
    output_path: path to the output video
    x: x coordinate of the top-left corner of the ROI
    y: y coordinate of the top-left corner of the ROI
    w: width of the ROI
    h: height of the ROI
    """
    utils.mkdir(output_dir)

    if not Path(input_path).exists():
        sys.exit(f"Input file not found: {input_path}")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        sys.exit(f"Cannot open video: {input_path}")

    frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Processing {frame_cnt} frames…")
    print(f"ROI = (x={x}, y={y}, w={w}, h={h})")

    for idx in range(frame_cnt):
        ret, frame = cap.read()
        if not ret:
            print(f"Finished early at frame {idx}")   # in case of truncated files
            break
        crop = frame[y:y+h, x:x+w]
        # Save each cropped frame as an image
        frame_output_path = os.path.join(output_dir, f'frame_{idx:06d}.png')
        #breakpoint()
        cv2.imwrite(frame_output_path, crop)

        if idx % 100 == 0:
            print(f"…{idx}/{frame_cnt}")

    cap.release()

def template_match_folder(source_folder_path='', output_folder_path='', template_image_path='', log_file_path='', threshold=.8):

    utils.mkdir(output_folder_path)
    # Define a threshold for determining if the template is present
    print(f"Threshold: {threshold}")

    log_strs = ''
    log_path = log_file_path
    for i,img_path in enumerate(sorted(utils.ls(source_folder_path))):
        SOURCE_IMAGE_PATH  = img_path
        # a
        OUTPUT_IMAGE_PATH  = f'{output_folder_path}/{utils.basename(SOURCE_IMAGE_PATH)}.png'
        # Load the source and template images
        source_image_path = Path(SOURCE_IMAGE_PATH)
        template_image_path = Path(template_image_path)

        if not source_image_path.exists() or not template_image_path.exists():
            sys.exit("Source or template image not found.")

        source_image = cv2.imread(str(source_image_path))
        template_image = cv2.imread(str(template_image_path))

        if source_image is None or template_image is None:
            sys.exit("Failed to load source or template image.")

        # Perform template matching
        result = cv2.matchTemplate(source_image, template_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        log_str = f"Output Image path: {OUTPUT_IMAGE_PATH}\n"
        log_str += f"Confidence score: {max_val:.4f}\n"
        log_str += f"--------------------------------\n"
        log_strs += log_str

        # Print the confidence score
        if max_val >= threshold:
            pass
        print(log_str)

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
        print(f"Saving result to {OUTPUT_IMAGE_PATH}")
        cv2.imwrite(OUTPUT_IMAGE_PATH, source_image)
        # cv2.imshow('Matched Result', source_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # print(f"Matched result saved to {OUTPUT_IMAGE_PATH}")
    utils.w(log_strs, log_path)


if __name__ == "__main__":
    pass


    # input_path = '/Users/azakaria/Code/twitch_detections/test/videos/aqua_only_dks_reframe.mp4'  # update this path
    # output_path = '/Users/azakaria/Code/twitch_detections/test/frames/extracted_frames_all_dks'
    # extract_all(input_path=input_path, output_path=output_path)