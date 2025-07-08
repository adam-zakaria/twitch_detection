# yt-dlp -S 'vcodec:h265,acodec:aac' --download-sections '*0-2:00' https://www.youtube.com/watch?v=Kl5QHzEwbLQ -o videos/lucid_2m.mp4

# roi

from twitch_detections import frame
import happy_utils as utils
import cv2
import os

# download streams from twitch

# input_path = 'videos/lucid_1s.webm'
# roi_frames_dir = 'frames/lucid_1s'
# utils.mkdir(roi_frames_dir)
# 
# #x,y,w,h = 710, 479, 62, 52
# x,y,w,h = 710, 479, 200, 200
# frame.reframe_video(input_path=input_path, output_dir=roi_frames_dir, x=x, y=y, w=w, h=h)
# 
# SOURCE_FOLDER_PATH = roi_frames_dir
# OUTPUT_FOLDER_PATH = 'test/frames/template_matching/lucid_1s'
# #TEMPLATE_IMAGE_PATH = '/Users/azakaria/Code/twitch_detections/twitch_detections/test/frames/template_matching/double_kill.png'
# TEMPLATE_IMAGE_PATH = '/Users/azakaria/Code/twitch_detections/twitch_detections/test/frame/double_kill_tighter.png'
# LOG_FILE_PATH = '/Users/azakaria/Code/twitch_detections/twitch_detections/test/frames/template_matching/output/log.txt'
# 
# frame.template_match_folder(source_folder_path=SOURCE_FOLDER_PATH, output_folder_path=OUTPUT_FOLDER_PATH, template_image_path=TEMPLATE_IMAGE_PATH, log_file_path=LOG_FILE_PATH)
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 