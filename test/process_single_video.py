"detect,extract"

# paddleocr detect
# extract

"""
okay for tesseract it would output a file {frame_i}.txt for each frame and detection attempt, and we look through each frame file for 'dou' and append them all to a single file. so instead of reading each file...for detection we go through all the frames,

paddle just outputs to memory, so we just read from memory and write to a dk_detections.txt, the float detection time 
"""
from paddleocr import PaddleOCR, draw_ocr; from PIL import Image; import os; import cv2; import utils.utils as utils  # Importing the generator for video frames

# Initialize the PaddleOCR model; uses English language and angle classification
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)  # Load OCR model once during initialization

# Generator to yield frames from the video
def get_frames(video_path):
  cap = cv2.VideoCapture(video_path)  # Open video capture
  frame_num = 0
  fps = cap.get(cv2.CAP_PROP_FPS)  # Retrieve FPS once at the start
  while True:
    ret, frame = cap.read()  # Read a frame
    if not ret:  # If no more frames, break the loop
      break
    yield frame, fps  # Yield the frame and the FPS
    frame_num += 1
  cap.release()  # Release the video capture object

# Function to process a video and extract OCR text from each frame
def process_video(video_path, output_dir):
  os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists or create it

  # Open the output file to write detection times
  detections_file = os.path.join(output_dir, 'dk_detections.txt')
  with open(detections_file, 'w') as f:

    # Iterate through frames using the get_frames generator
    for frame_index, (frame, fps) in enumerate(utils.get_frames(video_path), start=1):

      # start at frame 29 for quick dk detection
      if frame_index < 29:
        continue

      # Validate cropping dimensions
      # For some reason this is not working on M2, but I'm PRETTY sure it wasn't an issue on GPU, so ignore for now. I just need the detections file to do the rest of the pipeline.
      """
      crop_x, crop_y, crop_w, crop_h = 529, 441, 266, 131  # Define crop dimensions
      frame_h, frame_w = frame.shape[:2]  # Get frame dimensions
      if crop_x + crop_w > frame_w or crop_y + crop_h > frame_h:
        print(f"Skipping frame {frame_index}: Crop dimensions out of bounds")
        continue
      else:
        print(f"Frame dimensions: {crop_x, crop_y, crop_w, crop_h}")
      # Crop the frame
      frame = frame[crop_y:crop_y + crop_h, crop_x:crop_x + crop_w]  # Perform cropping
      """

      # Perform OCR on the saved frame image
      result = ocr.ocr(frame, cls=True)  # Extract text and bounding boxes from the frame
      result = result[0]

      # Print OCR results for the current frame
      print(f"Frame {frame_index}")
      for line in result:
        text = line[1][0]  # Extract the recognized text

        #confidence = line[1][1]  # Extract the confidence score
        #print(f"Text: {text}, Confidence: {confidence}")

        breakpoint()
        # Check for the presence of the word 'Dou' in the recognized text
        if 'Dou' in text:
          print(f'****************************')
          print(f"Match found: {text}")
          print(f'****************************')
          
          # Calculate the timestamp for the detection
          detection_time = frame_index / fps  # Frame index divided by FPS gives the time in seconds
          utils.wa(f"{detection_time:.2f}\n", detections_file)  # Write the detection time to the file

# Main entry point of the script
if __name__ == "__main__":
  # Process a sample video and save results to the specified output directory
  process_video('test/videos/3s_dk.mp4', 'paddleocr_output')

