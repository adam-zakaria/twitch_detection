from paddleocr import PaddleOCR, draw_ocr; from PIL import Image; import os; import cv2; import utils.utils as utils  # Importing the generator for video frames

# Initialize the PaddleOCR model; uses English language and angle classification
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)  # Load OCR model once during initialization

# Function to process a video and extract OCR text from each frame
def process_video(video_path, output_dir):
  os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists or create it

  # Iterate through frames using the get_frames generator
  for frame_index, (frame, fps) in enumerate(utils.get_frames(video_path), start=1):

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
    print(result)
    for line in result:
      #breakpoint()
      text = line[1][0]  # Extract the recognized text
      confidence = line[1][1]  # Extract the confidence score

      print(f"Text: {text}, Confidence: {confidence}")

      # Check for the presence of the word 'Dou' in the recognized text
      if 'Dou' in text:
        print(f'****************************')
        print(f"Match found: {text}")
        print(f'****************************')
        breakpoint()

# Main entry point of the script
if __name__ == "__main__":
  # Process a sample video and save results to the specified output directory
  process_video('test/videos/3s_dk.mp4', 'test/ocr_results')
