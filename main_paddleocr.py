"""
Compile double kills from a Halo Infinite gameplay.
"""

from paddleocr import PaddleOCR, draw_ocr; from PIL import Image; import os; import cv2; import utils.utils as utils; from itertools import pairwise; import subprocess; import cliptu.clip as clip

# Initialize the PaddleOCR model; uses English language and angle classification
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False, use_gpu=True)  # Load OCR model once during initialization
# Function to process a video and extract OCR text from each frame
def detect(input_video_path, output_detections_path):
  os.makedirs('detect', exist_ok=True)  # Ensure the output directory exists or create it
  # Open the output file to write detection times

  with open(output_detections_path, 'w') as f:
    # Iterate through frames using the get_frames generator
    for frame_index, (frame, fps) in enumerate(utils.get_frames(input_video_path), start=1):
      # get ROI
      frame = frame[441:441+131, 529:529+266]
      # Perform OCR on the saved frame image
      result = ocr.ocr(frame, cls=True)  # Extract text and bounding boxes from the frame
      result = result[0]
      # Print OCR results for the current frame
      print(f"Frame {frame_index}")
      if result is None: print('None result'); continue
      for line in result:
        text = line[1][0]  # Extract the recognized text
        #confidence = line[1][1]  # Extract the confidence score
        #print(f"Text: {text}, Confidence: {confidence}")
        # Check for the presence of the word 'Dou' in the recognized text
        if 'Dou' in text:
          print(f'****************************')
          print(f"Match found: {text}")
          print(f'****************************')
          # Calculate the timestamp for the detection
          detection_time = frame_index / fps  # Frame index divided by FPS gives the time in seconds
          utils.wa(f"{detection_time:.2f}\n", output_detections_path)  # Write the detection time to the file

# Function to process a video and extract OCR text from each frame
def filter(input_path, output_path):
    """
    Extracts video clips based on detection times.
    """
    print("Filtering")
    # Filter the list of floats to ensure no adjacent float is within 3.0 of each other
    filtered_floats = []
    for i, value in enumerate(map(float, utils.rl('detect/dk_detections.txt'))):  # Convert values to floats
      if i == 0 or (value - filtered_floats[-1] > 3.0):
        filtered_floats.append(value)
    mk_ss = filtered_floats

    utils.rm_mkdir('filter')
    if not mk_ss:
        print("No detections found.")
        utils.w('None', 'filter/dk_detections.txt')
        return None
    else:
        utils.w(mk_ss, 'filter/dk_detections.txt')
        return mk_ss

def extract(input_video_path):
    """
    Extracts video clips based on detection times.
    """
    output_video_dir = 'extract'
    utils.rm_mkdir(output_video_dir)
    detections = [float(line.strip()) for line in utils.rl('filter/dk_detections.txt')]
    
    for detection in detections:
        print(f"Extracting clip around {detection}s...")
        clip.extract_clip(input_video_path, f'{output_video_dir}/{detection.replace('.','_')}.mp4', detection-8, detection+1)
    print(f"Clips saved in {output_video_dir}.")

def concat():
    """
    Concatenates multiple video clips into a single video.
    """
    input_clips_path = 'extract'
    output_folder 

    utils.rm_mkdir(output_folder)

    print("Starting clip concatenation.")
    for clip_path in utils.ls(input_clips_path):
        print(f"Adding {clip_path} to concatenation list.")
        utils.wa(f"file '../{clip_path}'\n", 'concat/concat_files.txt') # path to clip must be relative to path of concat_files.txt

    output_folder = 'concat'
    subprocess.run(
        ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'concat/concat_files.txt', '-c', 'copy', f'{output_folder}/output.mp4'],
        check=True
    )
    print(f"Concatenated video saved in {output_folder}/output.mp4.")
    return output_folder

if __name__ == "__main__":
  # All output files are saved in folders named after their function, i.e. detect, filter, etc.
  detect('test/videos/4m_dk.mp4', 'detect/dk_detections.txt')
  filter('detect/dk_detections.txt', 'filter/dk_detections.txt')
  extract('test/videos/4m_dk.mp4', 'extract')
  concat('extract', 'concat')
