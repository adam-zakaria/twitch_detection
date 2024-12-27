import cv2
import os

def detect_and_save_one_second(video_path, template_path, output_dir, start_time):
    # Load the template image
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print("Error: Template image not found.")
        return
    template_height, template_width = template.shape[:2]

    # Open the video file
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Error: Cannot open video file.")
        return

    # Prepare the output directory
    os.makedirs(output_dir, exist_ok=True)

    # Get video properties
    fps = int(video.get(cv2.CAP_PROP_FPS))
    start_frame = int(start_time * fps)
    end_frame = start_frame + fps
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Process each frame
    frame_number = start_frame
    while frame_number < end_frame:
        ret, frame = video.read()
        if not ret:
            print("Error: Cannot read frame.")
            break

        # Perform template matching
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Debugging: Print the max_val to see the similarity score
        print(f"Frame {frame_number}: max_val = {max_val}")

        # Always draw the bounding box and annotate with the similarity score
        top_left = max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(frame, f'Score: {max_val:.2f}', (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Calculate the timestamp for the current frame
        timestamp = frame_number / fps
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = int(timestamp % 60)

        # Save the frame as an image
        output_filename = f"{output_dir}/frame_{hours:02}_{minutes:02}_{seconds:02}_{frame_number}.png"
        cv2.imwrite(output_filename, frame)
        print(f"Frame saved: {output_filename}")

        frame_number += 1
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    video.release()
    cv2.destroyAllWindows()
    print("Processing complete. Frames saved in the output directory.")

# Example usage
detect_and_save_one_second('video.mkv', 'image.png', 'detections', 23)
