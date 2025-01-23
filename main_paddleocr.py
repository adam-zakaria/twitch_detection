from paddleocr import PaddleOCR, draw_ocr; from PIL import Image; import os; import cv2; import utils.utils as utils; from itertools import pairwise; import subprocess; import cliptu.clip as clip

# Initialize the PaddleOCR model; uses English language and angle classification
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False, use_gpu=True)  # Load OCR model once during initialization


# Function to process a video and extract OCR text from each frame
def detect(video_path, output_dir):
  os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists or create it

  # Open the output file to write detection times
  detections_file = os.path.join(output_dir, 'dk_detections.txt')
  with open(detections_file, 'w') as f:

    # Iterate through frames using the get_frames generator
    for frame_index, (frame, fps) in enumerate(utils.get_frames(video_path), start=1):

      # Validate cropping dimensions
      # For some reason this is not working on M2, but I'm PRETTY sure it wasn't an issue on GPU, so ignore for now. I just need the detections file to do the rest of the pipeline.
      crop_x, crop_y, crop_w, crop_h = 529, 441, 266, 131  # Define crop dimensions
      frame_h, frame_w = frame.shape[:2]  # Get frame dimensions
      if crop_x + crop_w > frame_w or crop_y + crop_h > frame_h:
        print(f"Skipping frame {frame_index}: Crop dimensions out of bounds")
        continue
      else:
        print(f"Frame dimensions: {crop_x, crop_y, crop_w, crop_h}")
      # Crop the frame
      frame = frame[crop_y:crop_y + crop_h, crop_x:crop_x + crop_w]  # Perform cropping

      # Perform OCR on the saved frame image
      result = ocr.ocr(frame, cls=True)  # Extract text and bounding boxes from the frame
      result = result[0]

      # Print OCR results for the current frame
      print(f"Frame {frame_index}")
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
          utils.wa(f"{detection_time:.2f}\n", detections_file)  # Write the detection time to the file

# Function to process a video and extract OCR text from each frame
def detect_paddleocr(video_path, output_dir):
  os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists or create it

  # Iterate through frames using the get_frames generator
  for frame_index, (frame, fps) in enumerate(utils.get_frames(video_path), start=1):

    # get ROI
    frame = frame[441:441+131, 529:529+266]

    # Save the current frame to the output directory
    frame_path = f"{output_dir}/frame_{frame_index}.jpg"
    cv2.imwrite(frame_path, frame)  # Write the frame as an image file

    # Perform OCR on the saved frame image
    # result = ocr.ocr(frame, cls=True)  # Extract text and bounding boxes from the frame
    result = ocr.ocr(frame_path, cls=True)  # Extract text and bounding boxes from the frame
    result=result[0]

    # OCR result explanation:
    # - result is a list of lines, where each line contains bounding box info and text details.
    # - line[1][0] contains the recognized text.
    # - line[1][1] contains the confidence score for the recognized text.

    # Print OCR results for the current frame
    print(f"Frame {frame_index}")
    #print(result)
    for line in result:
      #breakpoint()
      text = line[1][0]  # Extract the recognized text
      confidence = line[1][1]  # Extract the confidence score

      #print(f"Text: {text}, Confidence: {confidence}")

      # Check for the presence of the word 'Dou' in the recognized text
      if 'Dou' in text:
        print(f'****************************')
        print(f"Match found: {text}")
        print(f'****************************')

def filter(detections_path):
    """
    Extracts video clips based on detection times.
    """
    print("Filtering")
    # Filter the list of floats to ensure no adjacent float is within 3.0 of each other
    filtered_floats = []
    for i, value in enumerate(map(float, utils.rl(detections_path))):  # Convert values to floats
      if i == 0 or (value - filtered_floats[-1] > 3.0):
        filtered_floats.append(value)
    mk_ss = filtered_floats


    if not mk_ss:
        print("No detections found.")
        return None
    else:
       return mk_ss
    
def extract(input_video_path, output_video_folder, detections: float):
    """
    Extracts video clips based on detection times.
    """
    utils.rm_mkdir(output_video_folder)

    for detection in detections:
        print(f"Extracting clip around {detection}s...")
        clip.extract_clip(input_video_path, f'{output_video_folder}/{detection}.mp4', detection-8, detection+1)

    print(f"Clips saved in {output_video_folder}.")

def concat(input_clips_path, output_folder):
    """
    Concatenates multiple video clips into a single video.
    """
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


# Main entry point of the script
if __name__ == "__main__":
  # Process a sample video and save results to the specified output directory
  detect_paddleocr('test/videos/1s_dk.mp4', 'detect')
  detections = filter('/Users/azakaria/Code/twitch_detections/paddleocr_output/dk_detections_original.txt')
  print(detections)
  extract('/Users/azakaria/Code/twitch_detections/test/videos/4m_dk.mp4','extract', detections)
  concat('extract', 'concat')
