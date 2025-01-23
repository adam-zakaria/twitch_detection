from paddleocr import PaddleOCR, draw_ocr; from PIL import Image; import os; import cv2; import utils.utils as utils; from itertools import pairwise;  # Importing the generator for video frames

# Initialize the PaddleOCR model; uses English language and angle classification
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False, use_gpu=True)  # Load OCR model once during initialization

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
    
import cliptu.clip as clip
def extract(input_video_path, output_video_folder, detections: float):
    """
    Extracts video clips based on detection times.
    """
    utils.rm_mkdir(output_video_folder)

    for detection in detections:
        print(f"Extracting clip around {detection}s...")
        clip.extract_clip(input_video_path, f'{output_video_folder}/{detection}.mp4', detection-8, detection+1)

    print(f"Clips saved in {output_video_folder}.")

# Main entry point of the script
if __name__ == "__main__":
  # Process a sample video and save results to the specified output directory
  #detect_paddleocr('test/videos/1s_dk.mp4', 'test/ocr_results')
  detections = filter('/Users/azakaria/Code/twitch_detections/paddleocr_output/dk_detections_original.txt')
  print(detections)
  extract('/Users/azakaria/Code/twitch_detections/test/videos/4m_dk.mp4','extract', detections)
