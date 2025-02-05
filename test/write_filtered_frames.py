import sys
sys.path.insert(0, '/home/ubuntu/Code/twitch_detection')

from main import write_filtered_frames

input_video_path = '/home/ubuntu/Code/twitch_detection/twitch_streams/Bound/329ca4963e5a4bccbe1fae83f83d5549.mp4'
roi = (529, 441, 266, 131)

write_filtered_frames(input_video_path, roi, '/home/ubuntu/Code/twitch_detection/output/filter/dk_detections.txt')
