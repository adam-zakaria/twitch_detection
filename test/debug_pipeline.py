from paddleocr import PaddleOCR
import os
import cv2
import utils.utils as utils
import time
import logging
import sys
sys.path.insert(0, '/home/ubuntu/Code/twitch_detection')
# from main import write_filtered_frames, filter
import main as main

#input_video_path = '/home/ubuntu/Code/twitch_detection/twitch_streams/Bound/329ca4963e5a4bccbe1fae83f83d5549.mp4'
#roi = (529, 441, 266, 131)




logging.getLogger("ppocr").disabled = True

# Initialize the PaddleOCR model once for detection.
ocr = PaddleOCR(use_angle_cls=False, lang='en', show_log=False, use_gpu=True)

def detect_timestamps(input_video_path, roi, output_folder, timestamps=None, yield_timestamps=False):
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

    for t, frame in utils.get_frames(input_video_path, timestamps=timestamps, yield_timestamps=yield_timestamps):
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


# Example usage:
if __name__ == "__main__":
    # input_video = '/home/ubuntu/Code/twitch_detection/twitch_streams/Bound/329ca4963e5a4bccbe1fae83f83d5549.mp4'
    # roi = (529, 441, 266, 131)  # (x, y, width, height)
    # timestamps_to_check = [ 33.69, 1369.96, 1391.64, 3128.19, 5110.91, 5777.71, 7849.49 ]
    # output_folder = f"output/{utils.ts()}/detect/"
    # detections = detect_timestamps(input_video, roi,  output_folder, timestamps=timestamps_to_check)

    input_video_path = '/home/ubuntu/Code/twitch_detection/test/videos/4m _dk.mp4'
    output_folder = utils.path(f"output/{utils.ts()}")
    detect_folder = output_folder / 'detect'
    filter_folder = output_folder / 'filter'

    roi = (529, 441, 266, 131)  # (x, y, width, height)

    detections = detect_timestamps(input_video_path, roi, detect_folder, yield_timestamps=True)

    #filter('output/detect/dk_detections.txt', 'output/filter/dk_detections.txt')
    main.filter(detect_folder / 'dk_detections.txt', filter_folder / 'dk_detections.txt')

    #write_filtered_frames(input_video_path, roi, 'output/filter/dk_detections.txt')

    main.write_filtered_frames(input_video_path, roi, filter_folder / 'dk_detections.txt', output_folder=filter_folder / 'images')