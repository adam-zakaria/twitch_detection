import cv2

# Load the template image
# template = cv2.imread('image.png', cv2.IMREAD_COLOR)
template = cv2.imread('medal_bg_removed.png', cv2.IMREAD_COLOR)
template_height, template_width = template.shape[:2]

# Open the video file
video = cv2.VideoCapture('video.mkv')

# Check if video opened successfully
if not video.isOpened():
    print("Error: Cannot open video file.")
    exit()

# Prepare the output video writer
fps = int(video.get(cv2.CAP_PROP_FPS))
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
output = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

# Process each frame
# Start processing from 23 seconds
start_time = 23  # seconds
start_frame = int(start_time * fps)
frame_number = start_frame
while True:
    ret, frame = video.read()
    if not ret:
        break  # End of video
    
    # Calculate the timestamp for the current frame
    timestamp = frame_number / fps
    hours = int(timestamp // 3600)
    minutes = int((timestamp % 3600) // 60)
    seconds = int(timestamp % 60)
    
    # Perform template matching
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Define a threshold for detection
    threshold = 0.55  # Adjust this value as needed
    
    # Check if the best match exceeds the threshold
    if max_val >= threshold:
        # Get the top-left corner of the best match
        top_left = max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        
        # Draw a rectangle around the matched region
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        
        # Output the detection time
        print(f"Detection at {hours:02}:{minutes:02}:{seconds:02}")
    
    # Write the frame to the output video
    output.write(frame)
    
    # Optional: Display the frame with the rectangle
    cv2.imshow('Template Matching', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Skip the next frame
    frame_number += 2
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

# Release resources
video.release()
output.release()
cv2.destroyAllWindows()
print("Processing complete. Output saved as 'output.mp4'.")