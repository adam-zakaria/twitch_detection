import cv2

# Path to your input video
input_path = '/Users/azakaria/Code/twitch_detections/test/videos/dk_compilation_az.mov'

# Open the video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video: {input_path}")

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_idx = 0

# Function to grab and return a specific frame
def get_frame(idx):
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    if not ret:
        raise IOError(f"Failed to read frame at index {idx}")
    return frame

# Interactive frame browsing
print("Use 'a'/'d' to navigate frames. Press 's' to select ROI. Press 'q' to quit.")
while True:
    frame = get_frame(frame_idx)
    display = frame.copy()
    cv2.putText(display, f'Frame {frame_idx+1}/{total_frames}', (10,30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow('Frame Browser', display)
    key = cv2.waitKey(0) & 0xFF

    if key in (ord('d'), 83):  # 'd' or right arrow (right not working)
        frame_idx = min(frame_idx + 1, total_frames - 1)
    elif key in (ord('a'), 81):  # 'a' or left arrow (left not working)
        frame_idx = max(frame_idx - 1, 0)
    elif key == ord('s'):  # select ROI
        x, y, w, h = cv2.selectROI('Select ROI', frame, showCrosshair=True, fromCenter=False)
        cv2.destroyWindow('Select ROI')
        break
    elif key == ord('q'):  # quit without selecting
        cap.release()
        cv2.destroyAllWindows()
        raise SystemExit("ROI selection cancelled by user")

cv2.destroyWindow('Frame Browser')

# Prepare video writer with the ROI size
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/Users/azakaria/Code/twitch_detections/test/videos/output.mp4', fourcc, fps, (w, h))

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
