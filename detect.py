import subprocess; import sys; import os; import glob; import cv2
from paddleocr import PaddleOCR; import utils.utils as utils

def detect(model, input_dir, output_dir):
  print(f"Starting detection with model: {model}")
  frames_dir, ocr_output_dir, detections_file = utils.opj(output_dir, "frames"), utils.opj(output_dir, "ocr_output"), utils.opj(output_dir, "detections.txt")
  [utils.rm(d) for d in [frames_dir, ocr_output_dir, detections_file]]; [utils.mkdir(d) for d in [frames_dir, ocr_output_dir]]
  ocr_model = PaddleOCR(use_gpu=True) if model == "paddleocr" else None

  for video_path in glob.glob(f"{input_dir}/**/*.mp4", recursive=True):
    print(f"Processing video: {video_path}")
    for i, (frame, frame_rate) in enumerate(utils.get_frames(video_path)):
      frame_path = utils.opj(frames_dir, f"{i}.png"); frame = frame[441:441+131, 529:529+266]; cv2.imwrite(frame_path, frame)
      if model == "tesseract":
        subprocess.run(['tesseract', frame_path, utils.opj(ocr_output_dir, str(i))], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(utils.opj(ocr_output_dir, f"{i}.txt"), "r") as f: text = f.read()
      elif model == "paddleocr":
        text = " ".join([line[-1][0] for line in ocr_model.ocr(frame_path)[0]])
      else: raise ValueError(f"Unsupported model: {model}")
      if "Dou" in text:
        time_in_seconds = i / frame_rate; print(f"Detection at time {time_in_seconds}s in video {video_path}")
        utils.wa(f"{video_path}: {time_in_seconds}\n", detections_file)

  print(f"Detection process completed. Results saved in {detections_file}.")

if __name__ == "__main__":
  if len(sys.argv) != 5: print("Usage: python main.py detect <model_name> <input_dir> <output_dir>"); sys.exit(1)
  command, model_name, input_dir, output_dir = sys.argv[1:]
  if command == "detect":
    if model_name not in ["tesseract", "paddleocr"]: print("Error: Model must be 'tesseract' or 'paddleocr'"); sys.exit(1)
    detect(model_name, input_dir, output_dir)
  else: print(f"Unsupported command: {command}"); sys.exit(1)
