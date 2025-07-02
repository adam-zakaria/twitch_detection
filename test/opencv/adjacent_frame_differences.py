# distinct_frame_selector_with_debug.py

import cv2
import numpy as np
import os
from statistics import median

# === Configuration ===
input_path       = '/Users/azakaria/Code/twitch_detections/test/videos/dks_only.mov'
output_dir       = 'distinct_frames'
threshold_factor = 1.5  # multiplier on median diff to decide “distinct”

# ensure output folder exists
os.makedirs(output_dir, exist_ok=True)

# --- First pass: compute frame-to-frame differences ---
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video: {input_path}")

# read the very first frame
ret, prev_frame = cap.read()
if not ret:
    raise IOError("Failed to read first frame.")
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

diffs = []
frame_indices = []
frame_idx = 1

print("FrameIdx\tDiffScore")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # compute mean absolute difference
    diff_value = np.mean(cv2.absdiff(gray, prev_gray))
    print(f"{frame_idx}\t{diff_value:.2f}")
    diffs.append(diff_value)
    frame_indices.append(frame_idx)
    prev_gray = gray
    frame_idx += 1

cap.release()

# --- Determine threshold from median difference ---
med_diff = median(diffs)
threshold = med_diff * threshold_factor
print(f"\nMedian diff: {med_diff:.2f}")
print(f"Threshold (median × {threshold_factor}): {threshold:.2f}")

# --- Select frames whose diff > threshold ---
selected_frames = [idx for idx, d in zip(frame_indices, diffs) if d > threshold]
print(f"\nSelected {len(selected_frames)} frames for export: {selected_frames}\n")

# --- Second pass: save those selected frames ---
cap = cv2.VideoCapture(input_path)
for idx in selected_frames:
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    if ret:
        out_fname = os.path.join(output_dir, f'frame_{idx:06d}.png')
        cv2.imwrite(out_fname, frame)
cap.release()

print(f"Done. Saved frames into '{output_dir}/'")
