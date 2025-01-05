"""
get frames 3s_dk.mp4 + use_roi
for frame, get tesseract output (called {frame_i}.txt)
read in all files, print any that are not empty

yt-dlp -S vcodec:h265,acodec:aac "https://www.youtube.com/watch?v=Kl5QHzEwbLQ" --download-sections "*00:24-00:27"

yt-dlp -S vcodec:h265,acodec:aac "https://www.youtube.com/watch?v=Kl5QHzEwbLQ" --download-sections "*00:00-04:00"
"""

# import libs
import utils.utils as utils; import cv2; import subprocess; import os 

# reset output files
utils.rm('tesseract_frames');utils.mkdir('tesseract_frames');utils.rm('tesseract_output');utils.mkdir('tesseract_output'); utils.rm('dk_detections.txt')

# Go through frames, run detection on ROI
for i,(frame,frame_rate) in enumerate(utils.get_frames('4m_dk.mp4')):
  frame=frame[441:441+131, 529:529+266]; cv2.imwrite(f'tesseract_frames/{i}.png', frame) 
  subprocess.run(['tesseract', f'/Users/azakaria/Code/halo_dk_detection/tesseract_frames/{i}.png', f'tesseract_output/{i}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  print(f'frame: {i}'); time_in_seconds = i / frame_rate; file = f'tesseract_output/{i}.txt'
  # if 'Dou' is detected, print and write the time of detection
  if 'Dou' in utils.r(file): # case sensitive
    print('******************'); print(f'detection at: {time_in_seconds}'); print('******************')
    utils.wa(str(f'{time_in_seconds}\n'), 'dk_detections.txt')

"""
:25
:33
:42
:50
1:24
2;03
2;47
254
310
"""
"""
for file in utils.ls('tesseract_output'):
  frame_num = int(utils.get_file_basename(file))
  time_in_seconds = frame_num / frame_rate
  print(frame_num)
  if 'dou' in utils.r(file):
    print(utils.r(file))
    print(time_in_seconds)
    print('******************')
    utils.wa(time_in_seconds, 'dk_detections.txt')
"""

