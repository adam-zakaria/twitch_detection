import cv2

# CONTROLS
# Use 'a'/'d' to navigate frames.
# Press 's' to select ROI.
# Space or enter to accept.
# Press 'q' to quit.

# MODIFY THESE
INPUT_PATH = '/Users/azakaria/Code/twitch_detections/test/videos/double kills/aqua.mp4'
OUTPUT_PATH = '/Users/azakaria/Code/twitch_detections/test/videos/output.mp4'
# /END

# Path to your input video
input_path = INPUT_PATH

# Open the video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video: {input_path}")

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_idx    = 0

# Function to grab and return a specific frame
def get_frame(idx):
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    if not ret:
        raise IOError(f"Failed to read frame at index {idx}")
    return frame

# ------------------ Slider (Trackbar) Setup ------------------
# Callback for the trackbar that simply updates the global frame_idx
def on_trackbar(pos):
    global frame_idx
    frame_idx = pos

# Create the window first so the trackbar can be attached to it
cv2.namedWindow('Frame Browser', cv2.WINDOW_NORMAL)
# Create the trackbar ranging from 0 to total_frames-1
cv2.createTrackbar('Frame', 'Frame Browser', 0, max(total_frames-1, 0), on_trackbar)

print("Keys: 'd' = next, 'a' = prev, 's' = select ROI, 'q' = quit")
while True:
    # Grab and display the current frame
    frame = get_frame(frame_idx)
    display = frame.copy()
    cv2.putText(display, f'Frame {frame_idx+1}/{total_frames}', (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow('Frame Browser', display)

    # Keep the trackbar in sync with the current frame
    cv2.setTrackbarPos('Frame', 'Frame Browser', frame_idx)

    key = cv2.waitKey(30) & 0xFF  # small delay to allow GUI + slider interaction

    if key in (ord('d'), 83):  # 'd' or right arrow
        frame_idx = min(frame_idx + 1, total_frames - 1)
    elif key in (ord('a'), 81):  # 'a' or left arrow
        frame_idx = max(frame_idx - 1, 0)
    elif key == ord('s'):  # select ROI
        x, y, w, h = cv2.selectROI('Select ROI', frame, showCrosshair=True, fromCenter=False)
        cv2.destroyWindow('Select ROI')
        print(f"Selected ROI - x: {x}, y: {y}, width: {w}, height: {h}")
        break
    elif key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        raise SystemExit("ROI selection cancelled by user")

# Close the browsing window before starting the crop-write loop
cv2.destroyWindow('Frame Browser')

# Prepare video writer with the ROI size
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (w, h))

# Process each frame: crop and write
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
while True:
    ret, frm = cap.read()
    if not ret:
        break
    crop = frm[int(y):int(y+h), int(x):int(x+w)]
    out.write(crop)

cap.release()
out.release()
print("Cropped video saved as output.mp4")
