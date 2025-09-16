"""
match template with not just dk, tk, ok, etc.

so:
maybe - if dk, template match tk for next 5 seconds, if tk, then okay for the next x seconds
So it's not tk every second
"""

import sys
sys.path.append("/home/ubuntu/Code/twitch_detections/twitch_detections")
import cv2
import time
import cliptu
import happy_utils as utils
from pathlib import Path

def hms(seconds):
    parts = []
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours: parts.append(f"{hours} hours")
    if minutes: parts.append(f"{minutes} minutes")
    if secs or not parts: parts.append(f"{secs} seconds")

    return " ".join(parts)

def crop(input_path='', x=0, y=0, w=0, h=0, every_nth_frame=None):
    """
    Crop a video to a fixed ROI.
    input_path: path to the input video
    output_path: path to the output video
    x: x coordinate of the top-left corner of the ROI
    y: y coordinate of the top-left corner of the ROI
    w: width of the ROI
    h: height of the ROI
    """
    # get frames from input_path and crop
    timestamps_crops = []
    for idx, (ts,frame) in enumerate(grab_frames(input_path, yield_timestamps=True, every_nth_frame=every_nth_frame)):
        crop = frame[y:y+h, x:x+w]
        yield(ts,crop)
        #timestamps_crops.append((ts, crop))

def match_template(stream_path = '', output_folder_path='', template_image_path='', log_file_path='', threshold=.8, verbose=False):
    """
    Template match each frame in the folder
    timestamps_and_frames: list of tuples (timestamp, frame)
    output_folder_path: path to the output folder
    template_image_path: path to the template image
    log_file_path: path to the log file
    threshold: threshold for determining if the template is present

    Returns:
    - list of tuples (timestamp, frame) with the template match applied
    """

    # create output folder
    utils.rm(output_folder_path)
    utils.mkdir(output_folder_path)

    # create log string and file
    log_strs = ''
    log_path = log_file_path

    # go through each frame looking for a double kill (template match each frame)
    match_timestamps = []

    # initialize tempate image path and load template image
    template_image_path = Path(template_image_path)
    template_image = cv2.imread(str(template_image_path))

    # initialize log_str
    log_str = ''

    # iterate through frames and perform template matching
    for i, (ts, frame) in enumerate(crop(input_path=stream_path, x=710, y=479, w=75, h=50, every_nth_frame=60)):
        # print the current frame - This trick only works for an interactive terminal 
        # print(f"\rProcessing frame {i}", end="")
        
        # initialize output image path
        OUTPUT_IMAGE_PATH  = f'{output_folder_path}/{ts}.png'

        #print(f'{frame.shape[:2]=}')
        #print(f'{template_image.shape[:2]=}')
        # Perform template matching
        result = cv2.matchTemplate(frame, template_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # log the output image path and confidence score
        if verbose:
            log_str += f"Output Image path: {OUTPUT_IMAGE_PATH}\n"
            log_str += f"Confidence score: {max_val:.4f}\n"
            log_str += f"--------------------------------\n"
            log_strs += log_str

        # Draw a rectangle around the matched region
        h, w = template_image.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        # Save and display the result
        if max_val >= threshold:
            log_strs += f"Template match found at {ts} with confidence {max_val:.4f}\n"
            cv2.imwrite(OUTPUT_IMAGE_PATH, frame)
            match_timestamps.append(ts)

    # write log and return match timestamps
    utils.wa(log_strs, log_path)
    return match_timestamps

def match_template_multi(stream_path = '', output_folder_path='', template_image_paths=[], log_file_path='', threshold=.8, verbose=False):

    # create output folder
    utils.rm(output_folder_path)
    utils.mkdir(output_folder_path)

    # create log string and file
    log_strs = ''
    log_path = log_file_path

    # go through each frame looking for a double kill (template match each frame)
    match_timestamps = []

    # initialize tempate image path and load template image
    template_image_path = Path(template_image_path)
    template_image = cv2.imread(str(template_image_path))

    # initialize log_str
    log_str = ''

    # iterate through frames and perform template matching
    for i, (ts, frame) in enumerate(crop(input_path=stream_path, x=710, y=479, w=75, h=50, every_nth_frame=60)):
        # print the current frame - This trick only works for an interactive terminal 
        # print(f"\rProcessing frame {i}", end="")
        
        # initialize output image path
        OUTPUT_IMAGE_PATH  = f'{output_folder_path}/{ts}.png'

        #print(f'{frame.shape[:2]=}')
        #print(f'{template_image.shape[:2]=}')
        # Perform template matching
        result = cv2.matchTemplate(frame, template_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # log the output image path and confidence score
        if verbose:
            log_str += f"Output Image path: {OUTPUT_IMAGE_PATH}\n"
            log_str += f"Confidence score: {max_val:.4f}\n"
            log_str += f"--------------------------------\n"
            log_strs += log_str

        # Draw a rectangle around the matched region
        h, w = template_image.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        # Save and display the result
        if max_val >= threshold:
            log_strs += f"Template match found at {ts} with confidence {max_val:.4f}\n"
            cv2.imwrite(OUTPUT_IMAGE_PATH, frame)
            match_timestamps.append(ts)

    # write log and return match timestamps
    utils.wa(log_strs, log_path)
    return match_timestamps


def benchmark_template_match(stream_path):
  template_path = '/home/ubuntu/Code/twitch_detections/twitch_detections/test/frame/double_kill_tighter.png'

  # Template match (and create frame generator)
  print(f'Running benchmark_process() on {stream_path}')
  print(f'The stream is {hms(cliptu.get_video_length(stream_path))}')
  try:
      start_time = time.time()
      match_timestamps = match_template(
          output_folder_path='./template_match',
          template_image_path=template_path,
          log_file_path='./log.txt',
          threshold=0.8
      )
      end_time = time.time()
      print(f'\tTemplate match took {hms(end_time - start_time)}')
      # Check for detections
      if match_timestamps == []:
        print('\tno matches found, exiting process()')
        return
  except Exception as e:
      # utils.wa('Error during template matching', config.log_file_path)
      print(f'Error during template matching: {e}')
      print(f'Returning from process()')
      return

if __name__ == "__main__":
  stream_path = '/home/ubuntu/Code/twitch_detections/twitch_detections/test/speed_investigation/output_trimmed.mp4'
  benchmark_template_match(stream_path)