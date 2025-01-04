"""
get frames 3s_dk.mp4 + use_roi
for frame, get tesseract output (called {frame_i}.txt)
read in all files, print any that are not empty

yt-dlp -S vcodec:h265,acodec:aac "https://www.youtube.com/watch?v=Kl5QHzEwbLQ" --download-sections "*00:24-00:27"
"""

import utils.utils as utils; import cv2; import subprocess
utils.rm('tesseract_frames');utils.mkdir('tesseract_frames');utils.rm('tesseract_output');utils.mkdir('tesseract_output')

for i,frame in enumerate(utils.get_frames('3s_dk.mp4')):
  frame=frame[441:441+131, 529:529+266]; cv2.imwrite(f'tesseract_frames/{i}.png', frame) 
  #cv2.imwrite(f'tesseract_frames/{i}.png', frame) 
  subprocess.run(['tesseract', f'/Users/azakaria/Code/halo_dk_detection/tesseract_frames/{i}.png', f'tesseract_output/{i}'])
for file in utils.ls('tesseract_output'):
  if utils.r(file):
    print(utils.r(file))

