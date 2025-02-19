from paddleocr import PaddleOCR, draw_ocr; from PIL import Image; import os; import cv2; import utils.utils as utils; from itertools import pairwise; import subprocess; import cliptu.clip as clip; import cliptu.ffprobe as ffprobe; import sys; import time; import logging; logging.getLogger("ppocr").disabled = True; import uuid; import time

# Initialize the PaddleOCR model
ocr = PaddleOCR(use_angle_cls=False, lang='en', show_log=False, use_gpu=True) 

def download_twitch_streams(streamers, output_path):
    """
    Open a subprocess for each twitch streamer, async. Subprocesses will exit when parent exits

    Does not upload, need separate code.
    """
    print("Starting Twitch stream downloads"); downloaded_streams = []
    output_path = utils.path(output_path)

    for streamer in streamers:
        # init folders
        #utils.mkdir(output_path); streamer_output_path = os.path.join(output_path, streamer); os.makedirs(streamer_output_path, exist_ok=True); print(f"Waiting for and downloading {streamer}'s stream to {streamer_output_path}...")
        utils.mkdir(output_path); streamer_output_path = output_path / streamer; utils.mkdir(streamer_output_path); print(f"Waiting for and downloading {streamer}'s stream to {streamer_output_path}...")
        subprocess.Popen(['yt-dlp', '--wait-for-video', '600', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}', '-o', f'{streamer_output_path}/{uuid.uuid4().hex}.%(ext)s'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # processes_have_not_run = False
    return downloaded_streams

# Process a video and extract OCR text from each frame
def detect(input_video_path, roi, output_detections_path):
  fps = utils.get_fps(input_video_path)
  utils.rm_mkdir(os.path.dirname(output_detections_path))  # Ensure the output directory exists
  ffprobe.get_video_length(input_video_path)
  ffprobe.get_resolution(input_video_path)
  print('We process every 20 frames, and the detect is completing videos at about 1/4 their time.')
  print('Detect running')
  log = []
  with open(output_detections_path, 'w') as f:
    for frame_index, frame in enumerate(utils.get_frames(input_video_path), start=1):
      if frame_index % 20 != 0: continue # process every 20th frame
      # frame = frame[441:441+131, 529:529+266]  # get ROI
      frame = utils.reframe(frame, *roi)
      result = ocr.ocr(frame, cls=True)  # Extract text and bounding boxes from the frame
      result = result[0]
      #print(f"Frame {frame_index}")
      #if result is None: print('None result'); continue
      if result is None: continue
      for line in result:
        text = line[1][0]  # Extract the recognized text
        if 'Dou' in text:
          print(f'****************************')
          print(f"Match found: {text}")
          print(f'****************************')
          detection_time = frame_index / fps  # Frame index divided by FPS gives the time in seconds
          utils.wa(f"{detection_time:.2f}\n", output_detections_path)  # Write the detection time to the file
          log.append({'timestamp': detection_time, 'text': text})
  utils.w(log, output_detections_path)

# Process a video and extract OCR text from each frame
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

def extract(input_video_path, output_video_dir):
  utils.rm_mkdir(output_video_dir)  # Ensure the output directory exists
  detections = [float(line.strip()) for line in utils.rl('output/filter/dk_detections.txt')]

  for detection in detections:
    print(f"Extracting clip around {detection}s...")
    clip.extract_clip(input_video_path, f'{output_video_dir}/{str(detection).replace(".", "_")}.mp4', detection-8, detection+1)
  print(f"Clips saved in {output_video_dir}.")

def concat(input_clips_path, output_folder):
  utils.rm_mkdir(output_folder)  # Ensure the output directory exists

  print("Starting clip concatenation.")
  for clip_path in sorted(utils.ls(input_clips_path)):
    clip_path = os.path.basename(clip_path)
    print(f"Adding {clip_path} to concatenation list.")
    utils.wa(f"file '../extract/{clip_path}'\n", f'{output_folder}/concat_files.txt')  # path to clip must be relative to path of concat_files.txt

  concat_command = f"ffmpeg -y -hide_banner -loglevel error -f f'{output_folder}/concat_files.txt' concat -safe 0 -i  -c copy f'{output_folder}/output.mp4'"
  subprocess.run(
    [
      "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", 
      "-safe", "0", "-i", f"{output_folder}/concat_files.txt", 
      "-c", "copy", f"{output_folder}/output.mp4"
    ],
    check=True  # Raises an error if the command fails
  )

  print(f"Concatenated video saved in {output_folder}/output.mp4.")
  return output_folder

def write_filtered_frames(input_video_path, roi, filtered_detections_path, output_folder=utils.path('filter/images/')):
  utils.mkdir(output_folder)  
  print('write_filtered_frames()')
  for i, detection in enumerate(map(float, utils.rl(filtered_detections_path))):  # Convert strings to floats
  # write frame + detection ROI for debugging
    img = utils.draw_rect(utils.get_frame(input_video_path, detection), *roi)
    # cv2.imwrite(utils.opj(output_folder, f'{detection}.jpg'), img) # correctly formats depending on ext provided
    print(f'Writing {output_folder / f"{detection}.jpg"}')
    cv2.imwrite(output_folder / f'{detection}.jpg', img) # correctly formats depending on ext provided

if __name__ == "__main__":
  # INTRO ##########
  # All output files are saved in folders named after their function, i.e. detect, filter, etc.
  # /INTRO ##########

  # INIT ##########
  #input_video_path = 'test/videos/1m_dk.mp4'
  input_video_path = '/home/ubuntu/Code/twitch_detection/twitch_streams/Bound/329ca4963e5a4bccbe1fae83f83d5549.mp4'
  roi = (529, 441, 266, 131)
  start_time = time.time()  # Record start time
  # /INIT ##########

  # PIPELINE ##########
  detect(input_video_path, roi, 'output/detect/dk_detections.txt')
  filter('output/detect/dk_detections.txt', 'output/filter/dk_detections.txt')
  # /PIPELINE ##########

  # LOGGING ##########
  write_filtered_frames(input_video_path, roi, 'output/filter/dk_detections.txt')
  # /LOGGING ##########

  # PIPELINE ##########
  extract(input_video_path, 'output/extract')
  concat('output/extract', 'output/concat')
  # /PIPELINE ##########

  # FINISH BENCHMARKING ############
  elapsed_time = time.time() - start_time  # Calculate elapsed time
  print(f'Time to run: {elapsed_time}')
  # /FINISH BENCHMARKING ############