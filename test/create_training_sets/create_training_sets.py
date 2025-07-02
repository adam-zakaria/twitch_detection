import os
import math
import happy_utils as utils

# UPDATE THESE
CLASS = 'double_kill'
INPUT_FRAMES_PATH = '/Users/azakaria/Code/twitch_detections/test/opencv/extracted_frames_all'
BASE_DEST_PATH = '/Users/azakaria/Code/twitch_detections/test/opencv/data'

# 1. Gather all frame paths
frame_paths = utils.ls(INPUT_FRAMES_PATH)
num_frames  = len(frame_paths)

# 2. Compute split indices
train_end = int(math.floor(num_frames * 0.8))
val_end   = int(math.floor(num_frames * 0.9))

train_src = frame_paths[:train_end]
val_src   = frame_paths[train_end:val_end]
test_src  = frame_paths[val_end:]

# 3. Define destination folders
base_dest = BASE_DEST_PATH
train_dest = os.path.join(base_dest, 'train', CLASS)
val_dest   = os.path.join(base_dest, 'val', CLASS)
test_dest  = os.path.join(base_dest, 'test', CLASS)

# Ensure folders exist
for d in (train_dest, val_dest, test_dest):
    os.makedirs(d, exist_ok=True)

# 4. Copy files
for src in train_src:
    dst = os.path.join(train_dest, os.path.basename(src))
    utils.cp(src, dst)  # or shutil.copy(src, dst)

for src in val_src:
    dst = os.path.join(val_dest, os.path.basename(src))
    utils.cp(src, dst)

for src in test_src:
    dst = os.path.join(test_dest, os.path.basename(src))
    utils.cp(src, dst)

print(f"Splits: train={len(train_src)}, val={len(val_src)}, test={len(test_src)}")
