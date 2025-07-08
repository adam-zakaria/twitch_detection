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
from twitch_detections.frame import template_match_folder


if __name__ == '__main__':
    SOURCE_FOLDER_PATH = '/Users/azakaria/Code/twitch_detections/twitch_detections/test/frames/extracted_frames_all_no_dks'
    OUTPUT_FOLDER_PATH = '/Users/azakaria/Code/twitch_detections/twitch_detections/test/frames/template_matching/output/all_no_dks'
    TEMPLATE_IMAGE_PATH = '/Users/azakaria/Code/twitch_detections/twitch_detections/test/frames/template_matching/double_kill.png'
    LOG_FILE_PATH = '/Users/azakaria/Code/twitch_detections/twitch_detections/test/frames/template_matching/output/log.txt'

    template_match_folder(source_folder_path=SOURCE_FOLDER_PATH, output_folder_path=OUTPUT_FOLDER_PATH, template_image_path=TEMPLATE_IMAGE_PATH, log_file_path=LOG_FILE_PATH)