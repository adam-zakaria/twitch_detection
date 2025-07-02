import cv2
import os

# Path to the input video and output directory
input_path = '/Users/azakaria/Code/twitch_detections/test/videos/dks_only.mov'
output_dir = 'selected_frames'
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video: {input_path}")

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_idx    = 0

# callback for trackbar: update frame_idx
def on_trackbar(pos):
    global frame_idx
    frame_idx = pos

# create window and slider
cv2.namedWindow('Frame Selector', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Frame', 'Frame Selector', 0, total_frames-1, on_trackbar)

print("Keys: 'd' = next, 'a' = prev, 's' = save, 'q' = quit")

while True:
    # grab the desired frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if not ret:
        print(f"Failed to read frame {frame_idx}")
        break

    cv2.imshow('Frame Selector', frame)
    # sync slider position
    cv2.setTrackbarPos('Frame', 'Frame Selector', frame_idx)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('d'):
        frame_idx = min(frame_idx + 1, total_frames - 1)
    elif key == ord('a'):
        frame_idx = max(frame_idx - 1, 0)
    elif key == ord('s'):
        fname = os.path.join(output_dir, f'frame_{frame_idx+1:06d}.png')
        cv2.imwrite(fname, frame)
        print(f"Saved {fname}")
    elif key == ord('q'):
        print("Exiting.")
        break
    # any other key or trackbar movement will just refresh the frame

cap.release()
cv2.destroyAllWindows()
