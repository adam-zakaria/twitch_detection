import cv2
import os

# === Configuration ===
input_path = '/Users/azakaria/Code/twitch_detections/test/videos/aqua_no_dks_reframe.mp4'  # update this path
output_dir = 'extracted_frames_all_no_dks'

# Create output directory if missing
os.makedirs(output_dir, exist_ok=True)

# Open the video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video: {input_path}")

frame_idx = 0
# Read and save frames until the video ends
while True:
    ret, frame = cap.read()
    if not ret:
        break
    filename = f"frame_{frame_idx:06d}.png"
    cv2.imwrite(os.path.join(output_dir, filename), frame)
    frame_idx += 1

cap.release()
print(f"Extracted {frame_idx} frames into '{output_dir}/'")
