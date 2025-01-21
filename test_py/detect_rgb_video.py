from detect_rgb_set import detect_rgb_set
import cv2
template_image = "double_kill_medal.png"
input_video = "combined_frames.mp4"

# read in combined_frames.mp4
input_video = cv2.VideoCapture(input_video)

# for each frame in the video, detect the rgb set
while True:
    ret, frame = input_video.read()
    if not ret:
        break
    detect_rgb_set(template_image, frame, video=True)
