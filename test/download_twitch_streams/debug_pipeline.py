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

#input_video_path = '/home/ubuntu/Code/twitch_detection/twitch_streams/Bound/329ca4963e5a4bccbe1fae83f83d5549.mp4'
#roi = (529, 441, 266, 131)

logging.getLogger("ppocr").disabled = True

# Initialize the PaddleOCR model once for detection.
ocr = PaddleOCR(use_angle_cls=False, lang='en', show_log=False, use_gpu=True)

def detect_timestamps(input_video_path, roi, output_folder, timestamps=None):
    """
    Processes a video and runs OCR detection on frames at specific timestamps.
    
    Parameters:
      input_video_path (str): Path to the video file.
      roi (tuple): A tuple (x, y, width, height) defining the region-of-interest.
      timestamps (list of float): List of timestamps (in seconds) at which to run detection.
      output_detections_path (str): Path to a file where detection timestamps (and optionally details) will be written.
    
    Returns:
      list: A list of dictionaries with detected timestamp and text.
    """
    print('Detect timestamps executing')
    # Ensure the output directory exists.
    #utils.rm_mkdir(os.path.dirname(output_folder))
    # utils.mkdir(os.path.dirname(output_folder))
    utils.mkdir(output_folder)

    detections_log = []
    timestamps_lines = []
    results = []

    for t, frame in utils.get_frames(input_video_path, timestamps=timestamps, yield_timestamps=True):
        # Retrieve the frame at the given timestamp.
        if frame is None:
            print(f"Could not retrieve frame at {t} seconds.")
            continue
        
        # Extract the region of interest from the frame.
        frame_roi = utils.reframe(frame, *roi)
        
        # Run OCR on the ROI.
        ocr_result = ocr.ocr(frame_roi, cls=True)
        if not ocr_result:
            continue
        
        # Assuming ocr_result is a list where the first element is a list of detected lines.
        result = ocr_result[0]
        results.append(result)
        if result is None: 
            # print(f'No text detected at {t}')
            continue
        else: 
            """
            result schema (code): https://paddlepaddle.github.io/PaddleOCR/main/en/quick_start.html#use-by-code

            We're guessing that detections happen at 'line granularity' meaning each line is a detection (we initially thought maybe locality mattered more, i.e. a paragraph would be single detection, we're guessing it's several)
            
            A timestamp is one frame and may include several detections, i.e. output like the following is normal:
            
            Text detected at 5777.71
            Text detected at 5777.71
            """
            for detection in result: # detection = line
                text = detection[1][0]  # Extract recognized text.
                # print(f'Text detected at {t}')
                # save all detections for transparency
                detections_log.append({'timestamp': t, 'text': text})
                if 'Dou' in text:
                    print(f"Match found at {t:.2f}s: {text}")
                    # Write the timestamp to the output file.
                    timestamps_lines.append(t)
        
        # Write the frame and bounding box for debugging
        utils.draw_rect(frame, *roi, save_path=f'output/detect/{t}.jpg')
    
    #result = "\n".join(str(f) for f in floats)
    timestamps_lines = "\n".join(str(t) for t in timestamps_lines)
    print(f'output_folder: {output_folder}')
    #print(f'output_folder: {output_folder}')
    utils.w(timestamps_lines, utils.opj(output_folder, 'dk_detections.txt'))
    utils.jd(detections_log, utils.opj(output_folder, 'text_detections.json'))
    utils.jd(results, utils.opj(output_folder, 'paddle_results_all.json'))
    return detections_log


def add_filtered_detections_json(filtered_detections_path, all_detections_path, ts):
    """
    filtered_detections_path:
        twitch_detection/test/output/02_06_2025_19_53_02/filter/dk_detections.txt
        33.69
        1369.96
        ...
    all_detections_path:
        twitch_detection/test/output/02_06_2025_19_53_02/detect/text_detections.json
        [{
            "timestamp": 5.016666666666667,
            "text": "ITz So Frasty"
        },...]
    """
    found = []
    for detection in utils.rl(filtered_detections_path):
        for obj in utils.jl(all_detections_path):
            # compare floats to 5th place
            if round(obj['timestamp'], 5) == round(float(detection), 5):
                found.append(obj)
    #utils.jd(found, f'output/{ts}/filter/filtered.json')
    utils.jd(found, f'output/{ts}/filter/filtered.json')


def extract(input_video_path, filter_folder, output_video_folder):
  utils.rm_mkdir(output_video_folder)  # Ensure the output directory exists
  detections = [float(line.strip()) for line in utils.rl(filter_folder / 'dk_detections.txt')]

  for detection in detections:
    print(f"Extracting clip around {detection}s...")
    clip.extract_clip(input_video_path, f'{output_video_folder}/{str(detection).replace(".", "_")}.mp4', detection-8, detection+1)
  print(f"Clips saved in {output_video_folder}.")

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


# Example usage:
if __name__ == "__main__":
    # input_video = '/home/ubuntu/Code/twitch_detection/twitch_streams/Bound/329ca4963e5a4bccbe1fae83f83d5549.mp4'
    # roi = (529, 441, 266, 131)  # (x, y, width, height)
    # timestamps_to_check = [ 33.69, 1369.96, 1391.64, 3128.19, 5110.91, 5777.71, 7849.49 ]
    # output_folder = f"output/{utils.ts()}/detect/"
    # detections = detect_timestamps(input_video, roi,  output_folder, timestamps=timestamps_to_check)
    #input_video_path = '/home/ubuntu/Code/twitch_detection/test/videos/1m_dk.mp4'

    # init ##########
    #input_video_path = '/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/twitch_streams/Bound/52a1dac2e5b941fe99ce392239d833a1.mp4'
    input_video_path = '/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/twitch_streams/royal2/7a5027362731493a928a306fa054f3ed.mp4'
    ts = utils.ts()
    #ts = '02_09_2025_03_10_25'
    output_folder = utils.path(f"output/{ts}")
    detect_folder = output_folder / 'detect'
    filter_folder = output_folder / 'filter'
    extract_folder = output_folder / 'extract'
    concat_folder = output_folder / 'concat'
    roi = (529, 441, 266, 131)  # (x, y, width, height)

    # run pipeline ##########
    detections = detect_timestamps(input_video_path, roi, detect_folder)
    main.filter(detect_folder / 'dk_detections.txt', filter_folder / 'dk_detections.txt')

    main.write_filtered_frames(input_video_path, roi, filter_folder / 'dk_detections.txt', output_folder=filter_folder / 'images')
    add_filtered_detections_json(filter_folder /'dk_detections.txt', detect_folder / 'text_detections.json', ts)

    extract(input_video_path, filter_folder, extract_folder)
    concat(extract_folder, concat_folder)


