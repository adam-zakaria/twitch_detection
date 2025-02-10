from paddleocr import PaddleOCR
import os
import cv2
import utils.utils as utils
import time
import logging
import sys
sys.path.insert(0, '/home/ubuntu/Code/twitch_detection')
# from main import write_filtered_frames, filter
import cliptu.clip as clip
import main as main
import subprocess

def concat(input_clips_path, output_folder):
  utils.rm_mkdir(output_folder)  # Ensure the output directory exists

  print("Starting clip concatenation.")
  for clip_path in sorted(utils.ls(input_clips_path)):
    clip_path = os.path.basename(clip_path)
    print(f"Adding {clip_path} to concatenation list.")
    utils.wa(f"file '../extract/{clip_path}'\n", f'{output_folder}/concat_files.txt')  # path to clip must be relative to path of concat_files.txt

  # broken
  # -safe 0 needed to allow relative paths in concat_files.txt
  """
  cmd = [
      "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", 
      "-safe", "0", "-i", f"{output_folder}/concat_files.txt", 
      "-c", "copy", f"{output_folder}/output.mp4"
  ]
  """

  """
  cmd = [
      "ffmpeg", "-y", "-hide_banner", "-f", "concat", 
      "-safe", "0", "-i", f"{output_folder}/concat_files.txt", 
      f"{output_folder}/output.mp4"
  ]
  """
  # Goes wayyyy faster with gpu accel, like 10x faster, more
  # There is some weird pause between each clip, it's not ideal, but it's tolerable
  """
  cmd = [
      "ffmpeg", "-y", "-hide_banner",
      "-hwaccel", "cuda",            # Optional: for hardware-accelerated decoding
      "-f", "concat",
      "-safe", "0",
      "-i", f"{output_folder}/concat_files.txt",
      "-c:v", "h264_nvenc",          # Use NVIDIA’s GPU-accelerated encoder
      f"{output_folder}/output.mp4"
  ]
  """
  """
  # error excerpt:
  # [h264_nvenc @ 0x5c6609c3d940] Driver does not support the required nvenc API version. Required: 13.0 Found: 12.1
  # t4 only supports up to 12.1, supposedly.
  See README for more
  cmd = [
      "ffmpeg",
      "-y",
      "-hide_banner",
      "-hwaccel", "cuda",          # Optional: for hardware-accelerated decoding
      "-f", "concat",
      "-safe", "0",
      "-i", f"{output_folder}/concat_files.txt",
      "-c:v", "h264_nvenc",        # NVIDIA’s GPU-accelerated H.264 encoder
      "-preset", "slow",           # Slower preset = higher quality
      "-rc", "vbr_hq",             # High-quality variable bitrate mode
      "-cq", "22",                 # Constant quality (lower = better quality, bigger file)
      "-b:v", "0",                 # No hard bitrate limit; focus on quality
      f"{output_folder}/output.mp4"
  ]
  """
  cmd = [
      "ffmpeg",
      "-y",
      "-hide_banner",
      "-hwaccel", "cuda",
      "-f", "concat",
      "-safe", "0",
      "-i", f"{output_folder}/concat_files.txt",
      "-c:v", "h264_nvenc",
      "-preset", "medium",   # or "slow" if supported
      "-rc", "vbr",          # simpler rate-control than "vbr_hq"
      "-b:v", "5M",          # target bitrate
      "-maxrate", "8M",      # maximum allowed bitrate
      "-bufsize", "16M",     # VBV buffer size
      "-c:a", "aac",
      "-b:a", "192k",
      f"{output_folder}/output.mp4"
  ]

  subprocess.run(
    cmd,
    check=True  # Raises an error if the command fails
  )

  print(' '.join(cmd))

  print(f"Concatenated video saved in {output_folder}/output.mp4.")
  return output_folder

if __name__ == "__main__":
  input_video_path = '/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/twitch_streams/royal2/7a5027362731493a928a306fa054f3ed.mp4'
  #ts = utils.ts()
  #ts = '02_09_2025_03_10_25'
  ts = '02_09_2025_04_07_29'
  output_folder = utils.path(f"output/{ts}")
  detect_folder = output_folder / 'detect'
  filter_folder = output_folder / 'filter'
  extract_folder = output_folder / 'extract'
  concat_folder = output_folder / 'concat'
  roi = (529, 441, 266, 131)  # (x, y, width, height)
  concat(extract_folder, concat_folder)