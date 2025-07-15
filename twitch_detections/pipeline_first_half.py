import cliptu.utils as cliptu
import cv2
import os
import sys
from pathlib import Path
import happy_utils as utils

roi_frames_dir = './output'
template_path = './template.png'
stream_path = 'Luciid_TW (live) 2025-07-08 18_04 [323997590012].mp4'
# x,y,w,h = 710, 479, 200, 200
#cliptu.reframe_video(input_path=stream_path, output_dir='./output', x=710, y=479, w=200, h=200)

roi_frames = cliptu.reframe_video_mem(input_path=stream_path, output_dir='./output', x=710, y=479, w=200, h=200, every_nth_frame=60)

# template_match_dir = './template_match'
# cliptu.template_match_folder_mem(source_folder_path=frames, output_folder_path=template_match_dir, template_image_path=template_path, log_file_path='./log.txt', threshold=.8)

template_match_dir = './template_match'
cliptu.template_match_folder_mem(input_frames=roi_frames, output_folder_path=template_match_dir, template_image_path=template_path, log_file_path='./log.txt', threshold=.8)