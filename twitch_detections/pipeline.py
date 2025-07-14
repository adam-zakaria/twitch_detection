import cliptu.utils as cliptu
import cv2
import os
import sys
from pathlib import Path
import happy_utils as utils

"""
def reframe_video(input_path='', output_dir='', x=0, y=0, w=0, h=0):
    # Crop a video to a fixed ROI.
    # input_path: path to the input video
    # output_path: path to the output video
    # x: x coordinate of the top-left corner of the ROI
    # y: y coordinate of the top-left corner of the ROI
    # w: width of the ROI
    # h: height of the ROI

    utils.mkdir(output_dir)

    if not Path(input_path).exists():
        sys.exit(f"Input file not found: {input_path}")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        sys.exit(f"Cannot open video: {input_path}")

    frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Processing {frame_cnt} frames…")
    print(f"ROI = (x={x}, y={y}, w={w}, h={h})")

    for idx, (ts,frame) in enumerate(cliptu.get_frames(input_path, yield_timestamps=True)):
        crop = frame[y:y+h, x:x+w]
        # Save each cropped frame as an image
        frame_output_path = os.path.join(output_dir, f'frame_{ts:.3f}.png')
        cv2.imwrite(frame_output_path, crop)

        if idx % 100 == 0:
            print(f"…{idx}/{frame_cnt}")

    cap.release()
"""

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