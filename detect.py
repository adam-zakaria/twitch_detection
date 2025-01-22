import subprocess; import sys; import os; import glob; import cv2
from paddleocr import PaddleOCR; import utils.utils as utils

# Function to perform text detection on videos using the specified OCR model
def detect(model, input_dir, output_dir):
  # Log the selected OCR model
  print(f"Starting detection with model: {model}")
  
  # Define paths for extracted frames, OCR outputs, and detections file
  frames_dir, ocr_output_dir, detections_file = utils.opj(output_dir, "frames"), utils.opj(output_dir, "ocr_output"), utils.opj(output_dir, "detections.txt")
  
  # Clean up any previous data in the output directories and create fresh ones
  [utils.rm(d) for d in [frames_dir, ocr_output_dir, detections_file]]; [utils.mkdir(d) for d in [frames_dir, ocr_output_dir]]
  
  # Initialize the OCR model based on the provided model name
  ocr_model = PaddleOCR(use_gpu=True) if model == "paddleocr" else None

  # Iterate over all .mp4 video files in the input directory (recursively)
  for video_path in glob.glob(f"{input_dir}/**/*.mp4", recursive=True):
    print(f"Processing video: {video_path}")

    # Extract frames from the video and process them
    for i, (frame, frame_rate) in enumerate(utils.get_frames(video_path)):
      # Save the cropped frame to the frames directory
      frame_path = utils.opj(frames_dir, f"{i}.png")
      frame = frame[441:441+131, 529:529+266]  # Crop the frame
      cv2.imwrite(frame_path, frame)
      
      # Perform OCR using the specified model
      if model == "tesseract":
        # Run Tesseract on the frame and read the output text
        subprocess.run(['tesseract', frame_path, utils.opj(ocr_output_dir, str(i))], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(utils.opj(ocr_output_dir, f"{i}.txt"), "r") as f: text = f.read()
      elif model == "paddleocr":
        # Run PaddleOCR and extract text from the frame
        text = " ".join([line[-1][0] for line in ocr_model.ocr(frame_path)[0]])
      else:
        # Raise an error if an unsupported model is specified
        raise ValueError(f"Unsupported model: {model}")

      # Check if the text contains the keyword "Dou"
      if "Dou" in text:
        # Log the detection time in seconds and save it to the detections file
        time_in_seconds = i / frame_rate
        print(f"Detection at time {time_in_seconds}s in video {video_path}")
        utils.wa(f"{video_path}: {time_in_seconds}\n", detections_file)

  # Indicate completion of the detection process
  print(f"Detection process completed. Results saved in {detections_file}.")

# Entry point for the script
if __name__ == "__main__":
  # Validate the command-line arguments
  if len(sys.argv) != 4:
    print("Usage: python detect.py  <model_name> <input_dir> <output_dir>")
    sys.exit(1)
  
  # Parse arguments
  model_name, input_dir, output_dir = sys.argv[1:]
  
  # Validate the specified model name
  if model_name not in ["tesseract", "paddleocr"]:
    print("Error: Model must be 'tesseract' or 'paddleocr'")
    sys.exit(1)
  
  # Call the detect function with the provided arguments
  detect(model_name, input_dir, output_dir)
