import cliptu.utils as cliptu_utils
import cliptu.clip as clip
import cv2
import os
import sys
from pathlib import Path
import happy_utils as utils
import time
import glob

def process(stream_path=''):
  """
  * Reframe
  * Template match
  * Extract clips
  * Concatenate clips
  """
  try:
    utils.w('Starting process()','log.txt')

    # Initialize paths
    roi_frames_dir = './output'
    template_path = 'test/frame/double_kill_tighter.png'

    # Reframe video to an ROI, only take every 60th frame. This is very slow. There are options for speeding up, with ffmpeg maybe being 10x faster? https://chatgpt.com/share/6875d629-1a94-8013-9af4-001b34edfea4 Could be a pain. Leave it unless it's an issue :)
    print('Reframing video to an ROI')
    start_time = time.time()
    timestamps_and_frames = cliptu_utils.reframe_video_mem(input_path=stream_path, x=710, y=479, w=200, h=200, every_nth_frame=60)
    end_time = time.time()
    print(f'Reframing video to an ROI took {end_time - start_time} seconds')

    # Template match each frame
    template_match_dir = './template_match'
    print('Template matching each frame')
    start_time = time.time()
    match_timestamps = cliptu_utils.template_match_folder(timestamps_and_frames=timestamps_and_frames, output_folder_path=template_match_dir, template_image_path=template_path, log_file_path='./template_match_log.txt', threshold=.8)
    end_time = time.time()
    print(f'Template matching each frame took {end_time - start_time} seconds')

    # Expecting template matches in template_match_dir
    filtered_timestamps = cliptu_utils.filter_timestamps(match_timestamps)

    # Extract clips
    paths = []
    output_dir = './clips'
    utils.mkdir(output_dir)
    for timestamp in filtered_timestamps:
      paths.append(clip.extract_clip(stream_path, f'{output_dir}/{timestamp}.mp4', timestamp-6, timestamp + 3))
    clip.concat(paths)

    # remove processed streams
    for stream_path in glob.glob(f'output/**/stream/*.mp4'):
      utils.rm(stream_path)
  except:
    utils.wa('Exception in process', 'log.txt')
    print('Exception in process')


if __name__ == "__main__":
  stream_path = 'lucid_3m.mp4' # dk at ~2:16
  process(stream_path)