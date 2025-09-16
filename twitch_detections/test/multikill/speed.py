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

def grab_frames(video_path, timestamps=None, yield_timestamps=False, every_nth_frame=None):
    """
    Generator to yield frames from a video.

    - When `timestamps` is None:
        * Uses cap.grab() to skip frames cheaply.
        * Uses cap.retrieve() only for frames you keep (every Nth).
        * If `yield_timestamps=True`, yields (ts, frame) where ts = frame_index / FPS.
          (Note: this timestamp is derived from FPS, not container timecodes.)
    - When `timestamps` is provided:
        * Seeks and decodes those frames (random access path; grab/retrieve is not applicable).

    Yields:
        If timestamps provided or yield_timestamps=True -> (timestamp, frame)
        else -> frame
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Error: Cannot open video at path '{video_path}'")

    try:
        if timestamps is None:
            # sequential scan
            step = max(1, int(every_nth_frame) if every_nth_frame else 1)
            fps = cap.get(cv2.CAP_PROP_FPS) if yield_timestamps else None

            frame_index = 0
            while True:
                # Skip step-1 frames with grab() (no full decode)
                for _ in range(step - 1):
                    ok = cap.grab()
                    if not ok:
                        return  # end of stream
                    frame_index += 1

                # Grab the kept frame and then retrieve (decode once)
                ok = cap.grab()
                if not ok:
                    return
                ok, frame = cap.retrieve()
                if not ok:
                    return

                if yield_timestamps:
                    if fps is None or fps <= 0:
                        fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
                    ts = (frame_index) / fps if fps > 0 else 0.0
                    yield ts, frame
                else:
                    yield frame

                frame_index += 1

        else:
            # random access by timestamps (seek -> decode)
            for t in sorted(timestamps):
                # Set position by milliseconds; decoder may need to decode from prior keyframe.
                cap.set(cv2.CAP_PROP_POS_MSEC, float(t) * 1000.0)
                ok, frame = cap.read()
                if ok:
                    yield t, frame if yield_timestamps else (t, frame)  # keep (t, frame) API
                else:
                    print(f"Warning: Could not retrieve frame at {t} seconds.")
    finally:
        cap.release()

def get_frames(video_path, timestamps=None, yield_timestamps=False, every_nth_frame=None):
    """
    Generator to yield frames from a video.
    
    Args:
        video_path (str): Path to the video file.
        timestamps (list of float, optional): Do not go over the whole video, just get the frames for the timestamps (in seconds).
            If provided, yields a tuple (timestamp, numpy.ndarray) for each timestamp.
            Otherwise, yields all frames sequentially.
        yield_timestamps (bool, optional): If True and timestamps is None,
            calculates and yields the timestamp (using FPS and frame index) along with the frame.
    
    Yields:
        If timestamps is provided or yield_timestamps is True:
            (timestamp, numpy.ndarray) tuples.
        Otherwise:
            numpy.ndarray frames.

    Example:
        import cliptu.utils as cliptu

        for ts,frame in cliptu.get_frames('/Users/azakaria/Code/twitch_detections/twitch_detections/videos/aqua_no_dks.mov', yield_timestamps=True):
            print(ts)
    """
    # open video
    cap = cv2.VideoCapture(video_path)

    # Check if the video was opened successfully
    if not cap.isOpened():
        raise ValueError(f"Error: Cannot open video at path '{video_path}'")
    
    # if no timestamps are provided, go through the whole video
    if timestamps is None:
        if yield_timestamps:
            # yield timestamps and frames, below
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_index = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if every_nth_frame and frame_index % every_nth_frame == 0:
                    timestamp = frame_index / fps  # Calculate timestamp from frame index and fps
                    # yield timestamps and frames
                    yield timestamp, frame
                frame_index += 1
        else:
            # do not yield timestamps (simpler interface)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                yield frame
    # if timestamps are provided, go through the provided timestamps, and yield the frames at the provided timestamps and frames
    else:
        for t in sorted(timestamps):
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ret, frame = cap.read()
            if ret:
                yield t, frame
            else:
                print(f"Warning: Could not retrieve frame at {t} seconds.")
    
    cap.release()

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

def template_match_folder(output_folder_path='', template_image_path='', log_file_path='', threshold=.8, verbose=False):
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

def benchmark_process(stream_path):
  template_path = '/home/ubuntu/Code/twitch_detections/twitch_detections/test/frame/double_kill_tighter.png'

  # Template match (and create frame generator)
  print(f'Running benchmark_process() on {stream_path}')
  print(f'The stream is {hms(cliptu.get_video_length(stream_path))}')
  try:
      start_time = time.time()
      timestamps_and_frames_generator = crop(
          input_path=stream_path, x=710, y=479, w=75, h=50, every_nth_frame=60
      )
      end_time = time.time()
      print(f'\tCrop took {hms(end_time - start_time)}')
      start_time = time.time()
      match_timestamps = template_match_folder(
          timestamps_and_frames=timestamps_and_frames_generator,
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
  benchmark_process(stream_path)