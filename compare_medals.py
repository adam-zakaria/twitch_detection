"""
Save every 10th frame (just the ROI) as a PNG
I manually inspect if dk medals remain constant across frames

Results: The medal seems to have slight transparency! :)

Get video with:
yt-dlp -S vcodec:h265,acodec:aac https://www.youtube.com/watch?v=Kl5QHzEwbLQ --download-sections "*00:25-00:26"
"""
import cv2; import utils.utils as utils; import os

utils.rm('compare_medals/frames_roi'); utils.mkdir('compare_medals/frames_roi');utils.rm('compare_medals/frames_full'); utils.mkdir('compare_medals/frames_full'); utils.rm('compare_medals/frames_text'); utils.mkdir('compare_medals/frames_text');

for i,frame in enumerate(utils.get_frames('1s_dk.mp4')): 
  print(i)
  if i % 10 == 0: 
    # write different kinds of frames, frame[y0:y1,x0:x1]
    cv2.imwrite(f'compare_medals/frames_roi/{i}.png', frame[485:485 + 38, 745:745 + 44]); cv2.imwrite(f'compare_medals/frames_full/{i}.png', frame); cv2.imwrite(f'compare_medals/frames_text/{i}.png', frame[441:441+131, 529:529+266])
