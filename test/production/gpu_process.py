import os
import sys
import time
import glob
import subprocess
import logging
import cv2

import utils.utils as utils
import cliptu.s3 as s3
import cliptu.clip as clip
from paddleocr import PaddleOCR

# Disable unwanted logging
logging.getLogger("ppocr").disabled = True

# Ensure proper path for local modules
sys.path.insert(0, '/home/ubuntu/Code/twitch_detection')

# Define a decorator to log function entry, exit, and exceptions.
def log_calls(func):
    def wrapper(*args, **kwargs):
        utils.log(f"Starting {func.__name__}...")
        try:
            result = func(*args, **kwargs)
            utils.log(f"{func.__name__} finished successfully.")
            return result
        except Exception as e:
            utils.log(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

@log_calls
def detect_timestamps(input_video_path, roi, output_folder, timestamps=None):
    """
    Processes a video and runs OCR detection on frames at specific timestamps.
    
    Parameters:
      input_video_path (str): Path to the video file.
      roi (tuple): A tuple (x, y, width, height) defining the region-of-interest.
      timestamps (list of float): List of timestamps (in seconds) at which to run detection.
    
    Returns:
      list: A list of dictionaries with detected timestamp and text.
    """
    utils.mkdir(output_folder)
    detections_log = []
    timestamps_lines = []
    results = []

    for t, frame in utils.get_frames(input_video_path, timestamps=timestamps, yield_timestamps=True):
        try:
            if frame is None:
                utils.log(f"Could not retrieve frame at {t} seconds.")
                continue
            
            # Extract the region of interest from the frame.
            frame_roi = utils.reframe(frame, *roi)
            
            try:
                ocr_result = ocr.ocr(frame_roi, cls=True)
            except Exception as ocr_err:
                utils.log(f"OCR failed at {t}s: {ocr_err}")
                continue

            if not ocr_result:
                continue

            result = ocr_result[0]
            results.append(result)
            if result is None:
                continue
            else:
                for detection in result:
                    text = detection[1][0]
                    detections_log.append({'timestamp': t, 'text': text})
                    if 'Dou' in text:
                        utils.log(f"Match found at {t:.2f}s: {text}")
                        timestamps_lines.append(t)
            
            # Write the frame with drawn ROI for debugging.
            utils.draw_rect(frame, *roi, save_path=f'output/detect/{t}.jpg')
        except Exception as inner_err:
            utils.log(f"Error processing frame at {t}: {inner_err}")

    timestamps_lines_str = "\n".join(str(t) for t in timestamps_lines)
    utils.log(f'Output folder: {output_folder}')
    if not timestamps_lines_str:
      return None
    utils.w(timestamps_lines_str, utils.opj(output_folder, 'dk_detections.txt'))
    utils.jd(detections_log, utils.opj(output_folder, 'text_detections.json'))
    utils.jd(results, utils.opj(output_folder, 'paddle_results_all.json'))
    return detections_log

@log_calls
def add_filtered_detections_json(filtered_detections_path, all_detections_path, filtered_json_path):
    """
    Compares filtered detection timestamps with all detections and writes the matched detections to a JSON file.
    """
    found = []
    for detection in utils.rl(filtered_detections_path):
        for obj in utils.jl(all_detections_path):
            if round(obj['timestamp'], 5) == round(float(detection), 5):
                found.append(obj)
    utils.jd(found, filtered_json_path)

@log_calls
def extract(input_video_path, filter_folder, output_video_folder):
    """
    Extracts clips from the input video around each detection timestamp.
    """
    utils.rm_mkdir(output_video_folder)
    detections = [float(line.strip()) for line in utils.rl(filter_folder / 'dk_detections.txt')]

    for detection in detections:
        utils.log(f"Extracting clip around {detection}s...")
        clip.extract_clip(
            input_video_path, 
            f'{output_video_folder}/{str(detection).replace(".", "_")}.mp4', 
            detection - 8, 
            detection + 1
        )
    utils.log(f"Clips saved in {output_video_folder}.")

# Process a video and extract OCR text from each frame
@log_calls
def filter(input_detections_path, output_filtered_path):
  breakpoint
  print("Filtering")
  utils.rm_mkdir(os.path.dirname(output_filtered_path))  # Ensure the output directory exists

  filtered_timestamps = [] # floats
  for i, value in enumerate(map(float, utils.rl(input_detections_path))):  # Convert values to floats
    if i == 0 or (value - filtered_timestamps[-1] > 3.0):
      filtered_timestamps.append(value)

  if not filtered_timestamps:
    print("No detections found.")
    utils.w('None', output_filtered_path)
    return None
  else:
    for filtered_timestamp in filtered_timestamps:
      utils.wa(f'{filtered_timestamp}\n', output_filtered_path) # float
    return filtered_timestamps

@log_calls
def write_filtered_frames(input_video_path, roi, filtered_detections_path, output_folder=utils.path('filter/images/')):
  utils.mkdir(output_folder)  
  print('write_filtered_frames()')
  for i, detection in enumerate(map(float, utils.rl(filtered_detections_path))):  # Convert strings to floats
  # write frame + detection ROI for debugging
    img = utils.draw_rect(utils.get_frame(input_video_path, detection), *roi)
    # cv2.imwrite(utils.opj(output_folder, f'{detection}.jpg'), img) # correctly formats depending on ext provided
    print(f'Writing {output_folder / f"{detection}.jpg"}')
    cv2.imwrite(output_folder / f'{detection}.jpg', img) # correctly formats depending on ext provided


@log_calls
def concat(input_clips_path, output_folder):
    """
    Concatenates video clips from the given directory.
    """
    utils.rm_mkdir(output_folder)
    utils.log("Starting clip concatenation.")
    
    # Build concat_files.txt
    for clip_path in sorted(utils.ls(input_clips_path)):
        base_clip = os.path.basename(clip_path)
        utils.log(f"Adding {base_clip} to concatenation list.")
        utils.wa(f"file '../extract/{base_clip}'\n", f'{output_folder}/concat_files.txt')
    
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-f", "concat", 
        "-safe", "0", "-i", f"{output_folder}/concat_files.txt", 
        f"{output_folder}/output.mp4"
    ]
    subprocess.run(cmd, check=True)
    utils.log(f"Concatenated video saved in {output_folder}/output.mp4.")
    return output_folder

@log_calls
def concat_all(input_file_paths, output_file="output.mp4"):
  if not input_file_paths:
    raise ValueError("No input files provided.")

  num_files = len(input_file_paths)

  # Build the ffmpeg command starting with the input files.
  ffmpeg_cmd = ["ffmpeg", "-y", "-hide_banner"]
  for f in input_file_paths:
    ffmpeg_cmd.extend(["-i", f])  # Add each file as an input

  # Build the stream mapping string.
  stream_mapping = "".join(f"[{i}:v:0][{i}:a:0]" for i in range(num_files))

  # Append the concat filter
  filter_complex = f"{stream_mapping}concat=n={num_files}:v=1:a=1[outv][outa]"

  # Complete the ffmpeg command
  ffmpeg_cmd.extend([
    "-filter_complex", filter_complex,
    "-map", "[outv]", "-map", "[outa]",
    output_file
  ])

  # Print the command for debugging
  print("Running command:", " ".join(ffmpeg_cmd))

  # Execute the command
  subprocess.run(ffmpeg_cmd, check=True)


if __name__ == "__main__":
    utils.log(f'Downloading twitch_streams')
    # Download twitch streams from S3.
    s3.download_folder('s3://cliptu/twitch_streams', 'twitch_streams')

    # Initialize OCR and pipeline parameters.
    ocr = PaddleOCR(use_angle_cls=False, lang='en', show_log=False, use_gpu=True)
    roi = (529, 441, 266, 131)  # (x, y, width, height)

    for streamer_path in utils.ls('twitch_streams'):
        streamer = streamer_path.split('/')[1]
        input_video_paths = [p for p in utils.ls('twitch_streams') if p.endswith(".mp4") and not p.endswith(".temp.mp4")] # filter .mp4s, avoiding .temp.mp4
        utils.log(f'input_video_paths: {input_video_paths}')
        for input_video_path in input_video_paths:
            ts = utils.ts()
            output_folder = utils.path(f"output/{streamer}/{ts}")
            detect_folder = output_folder / 'detect'
            filter_folder = output_folder / 'filter'
            extract_folder = output_folder / 'extract'
            concat_folder = output_folder / 'concat'

            # Run the pipeline.
            detections = detect_timestamps(input_video_path, roi, detect_folder)
            if not detections:
              utils.log(f'In detect() no double kills detected for {input_video_path}, moving onto next video')
              continue
            filter(detect_folder / 'dk_detections.txt', filter_folder / 'dk_detections.txt')
            write_filtered_frames(
                input_video_path, 
                roi, 
                filter_folder / 'dk_detections.txt', 
                output_folder=filter_folder / 'images'
            )
            add_filtered_detections_json(
                filter_folder / 'dk_detections.txt', 
                detect_folder / 'text_detections.json', 
                filter_folder / 'filtered.json'
            )
            extract(input_video_path, filter_folder, extract_folder)
            concat(extract_folder, concat_folder)
    
    compilation_paths = glob.glob('output/*/*/concat/output.mp4')
    if compilation_paths:
      concat_all(compilation_paths, 'output.mp4')
    else:
      utils.log('No files in concat_files.txt (none of the streamers have double kills), skipping concat_all()')
