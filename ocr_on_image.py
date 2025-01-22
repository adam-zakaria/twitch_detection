import subprocess; import sys; import os; import glob; import cv2
from paddleocr import PaddleOCR; import utils.utils as utils

def detect(model, input_dir, output_dir):
  print(f"Starting OCR with model: {model}")
  
  # Output directory for OCR text files
  ocr_output_dir = utils.opj(output_dir, "ocr_output")
  utils.rm(ocr_output_dir); utils.mkdir(ocr_output_dir)

  # Initialize OCR model
  if model == "paddleocr": ocr_model = PaddleOCR(use_gpu=False)
  elif model == "tesseract": ocr_model = None
  else: raise ValueError(f"Unsupported model: {model}")

  # Decide whether input_dir is really a directory or a single file
  if os.path.isfile(input_dir):
    # If single image, just handle that file
    image_paths = [input_dir]
  else:
    # Build a list of image paths from the directory
    img_extensions = ["*.png", "*.jpg", "*.jpeg"]
    image_paths = []
    for ext in img_extensions:
      image_paths.extend(glob.glob(os.path.join(input_dir, "**", ext), recursive=True))

  # Process each image
  for idx, image_path in enumerate(image_paths):
    print(f"Processing image: {image_path}")
    image = cv2.imread(image_path)
    if image is None: 
      print(f"Warning: Could not read {image_path}. Skipping.")
      continue

    # Run OCR
    if model == "tesseract":
      # Tesseract requires an output text file prefix
      base_name = os.path.splitext(os.path.basename(image_path))[0]
      txt_output_prefix = utils.opj(ocr_output_dir, base_name)
      subprocess.run(['tesseract', image_path, txt_output_prefix], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      txt_file = txt_output_prefix + ".txt"
      with open(txt_file, "r", encoding="utf-8") as f: 
        text = f.read()
    else:
      # PaddleOCR (in-memory)
      ocr_result = ocr_model.ocr(image_path)
      text = " ".join([line[-1][0] for line in ocr_result[0]])
      # Optionally write to a text file
      base_name = os.path.splitext(os.path.basename(image_path))[0]
      txt_file = utils.opj(ocr_output_dir, f"{base_name}.txt")
      utils.wa(text, txt_file)

    # Print the recognized text
    print(f"OCR result for {image_path}:\n{text}")

  print("OCR process completed.")

if __name__ == "__main__":
  if len(sys.argv) != 4:
    print("Usage: python detect.py <model_name> <input_dir_or_file> <output_dir>")
    sys.exit(1)
  
  model_name, input_dir, output_dir = sys.argv[1:]
  if model_name not in ["tesseract", "paddleocr"]:
    print("Error: Model must be 'tesseract' or 'paddleocr'")
    sys.exit(1)
  
  detect(model_name, input_dir, output_dir)
