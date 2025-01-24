from paddleocr import PaddleOCR, draw_ocr; from PIL import Image; import os; import cv2; import utils.utils as utils; from itertools import pairwise; import subprocess; import cliptu.clip as clip

#[concat @ 0x60926e399700] Impossible to open 'output/concat/../extract/output/extract/0_02.mp4' output/concat/concat_files.txt: No such file or directory

# Initialize the PaddleOCR model; uses English language and angle classification
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False, use_gpu=True)  # Load OCR model once during initialization

# Function to process a video and extract OCR text from each frame
def detect(input_video_path, output_detections_path):
  utils.rm_mkdir(os.path.dirname(output_detections_path))  # Ensure the output directory exists

  with open(output_detections_path, 'w') as f:
    for frame_index, (frame, fps) in enumerate(utils.get_frames(input_video_path), start=1):
      frame = frame[441:441+131, 529:529+266]  # get ROI
      result = ocr.ocr(frame, cls=True)  # Extract text and bounding boxes from the frame
      result = result[0]
      print(f"Frame {frame_index}")
      if result is None: print('None result'); continue
      for line in result:
        text = line[1][0]  # Extract the recognized text
        if 'Dou' in text:
          print(f'****************************')
          print(f"Match found: {text}")
          print(f'****************************')
          detection_time = frame_index / fps  # Frame index divided by FPS gives the time in seconds
          utils.wa(f"{detection_time:.2f}\n", output_detections_path)  # Write the detection time to the file

# Function to process a video and extract OCR text from each frame
def filter(input_detections_path, output_filtered_path):
  print("Filtering")
  utils.rm_mkdir(os.path.dirname(output_filtered_path))  # Ensure the output directory exists

  filtered_floats = []
  for i, value in enumerate(map(float, utils.rl(input_detections_path))):  # Convert values to floats
    if i == 0 or (value - filtered_floats[-1] > 3.0):
      filtered_floats.append(value)

  if not filtered_floats:
    print("No detections found.")
    utils.w('None', output_filtered_path)
    return None
  else:
    for _float in filtered_floats:  # floating point detection
      utils.wa(f'{_float}\n', output_filtered_path)
    return filtered_floats

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
  for clip_path in utils.ls(input_clips_path):
    clip_path = os.path.basename(clip_path)
    print(f"Adding {clip_path} to concatenation list.")
    utils.wa(f"file '../extract/{clip_path}'\n", f'{output_folder}/concat_files.txt')  # path to clip must be relative to path of concat_files.txt

  subprocess.run(
    ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', f'{output_folder}/concat_files.txt', '-c', 'copy', f'{output_folder}/output.mp4'],
    check=True
  )
  print(f"Concatenated video saved in {output_folder}/output.mp4.")
  return output_folder

if __name__ == "__main__":
  # All output files are saved in folders named after their function, i.e. detect, filter, etc.
  input_video_path = 'test/videos/1s_dk.mp4'
  detect(input_video_path, 'output/detect/dk_detections.txt')
  filter('output/detect/dk_detections.txt', 'output/filter/dk_detections.txt')
  extract(input_video_path, 'output/extract')
  concat('output/extract', 'output/concat')
