import cv2
import subprocess
from pathlib import Path
import sys
import os
import happy_utils as utils
import shlex

def save_image(img, path):
    cv2.imwrite(path, img) # correctly formats depending on ext provided

def get_frame(video_path, timestamp: float, save_path=None):
    """
    Retrieves a single frame from a video at the specified timestamp.

    Parameters:
      video_path (str): Path to the video file.
      timestamp (float): Timestamp in seconds at which to extract the frame.

    Returns:
      numpy.ndarray or None: The frame at the specified timestamp, or None if the frame cannot be read.
    """
    cap = cv2.VideoCapture(video_path)  # Open the video file
    # Set the position in the video (in milliseconds)
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
    ret, frame = cap.read()  # Read the frame at the given timestamp
    if save_path:
      save_image(frame, save_path)
    cap.release()  # Release the video capture object
    return frame if ret else None

def reframe(frame, x, y, width, height):
    """
    Extracts a region of interest from an image.

    Parameters:
      frame: The input image (numpy array).
      x, y: The top-left corner coordinates of the region.
      width, height: The width and height of the region.

    Returns:
      The ROI as: img[y:y+height, x:x+width]
    """
    return frame[y:y+height, x:x+width]

def draw_rect(img, x1, y1, width, height, color=(0, 255, 0), thickness=2, save_path=None):
    """
    Draws a rectangle on the image 'img' using the top-left corner (x1, y1)
    and the given width and height.

    Parameters:
      img: The image (numpy array).
      x1, y1: Coordinates of the top-left corner of the rectangle.
      width: The width of the rectangle.
      height: The height of the rectangle.
      color: The rectangle color in BGR (default green).
      thickness: The thickness of the rectangle border.

    Returns:
      The image with the rectangle drawn.
    """
    # Calculate bottom-right corner
    x2 = x1 + width
    y2 = y1 + height
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    if save_path:
       cv2.imwrite(save_path ,img)
    return img

def get_fps(video_path):
  """
  Get the frames per second (FPS) of a video.

  Args:
      video_path (str): Path to the video file.

  Returns:
      float: FPS of the video.
  """
  cap = cv2.VideoCapture(video_path)  # Open video capture
  fps = cap.get(cv2.CAP_PROP_FPS)  # Retrieve the FPS
  cap.release()  # Release the video capture object
  return fps

def get_frames(video_path, timestamps=None, yield_timestamps=False, every_nth_frame=None):
    """
    Generator to yield frames from a video.
    
    Args:
        video_path (str): Path to the video file.
        timestamps (list of float, optional): Do not go over the whole video, just get the frames for the timestamps (in seconds).
            If provided, yields a tuple (timestamp, numpy.ndarray) for each timestamp.
            Otherwise, yields all frames sequentially.
        yield_timestamps (bool, optional): If True and timestamps is None,
            calculates and yields the timestamp (using FPS and frame index) along with the frame.
    
    Yields:
        If timestamps is provided or yield_timestamps is True:
            (timestamp, numpy.ndarray) tuples.
        Otherwise:
            numpy.ndarray frames.

    Example:
        import cliptu.utils as cliptu

        for ts,frame in cliptu.get_frames('/Users/azakaria/Code/twitch_detections/twitch_detections/videos/aqua_no_dks.mov', yield_timestamps=True):
            print(ts)
    """
    # open video
    cap = cv2.VideoCapture(video_path)

    # Check if the video was opened successfully
    if not cap.isOpened():
        raise ValueError(f"Error: Cannot open video at path '{video_path}'")
    
    # if no timestamps are provided, go through the whole video
    if timestamps is None:
        if yield_timestamps:
            # yield timestamps and frames, below
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_index = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if every_nth_frame and frame_index % every_nth_frame == 0:
                    timestamp = frame_index / fps  # Calculate timestamp from frame index and fps
                    # yield timestamps and frames
                    yield timestamp, frame
                frame_index += 1
        else:
            # do not yield timestamps (simpler interface)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                yield frame
    # if timestamps are provided, go through the provided timestamps, and yield the frames at the provided timestamps and frames
    else:
        for t in sorted(timestamps):
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ret, frame = cap.read()
            if ret:
                yield t, frame
            else:
                print(f"Warning: Could not retrieve frame at {t} seconds.")
    
    cap.release()

def ffprobe(video_file, output_file=""):
  ffprobe_command = [
      'ffprobe', '-v', 'error', '-show_streams', '-show_format', video_file
  ]
  result = subprocess.run(ffprobe_command, capture_output=True, text=True)

  # Prepare to filter ffprobe output
  filtered_lines = []
  for line in result.stdout.split('\n'):
      if 'codec_name=' in line or 'width=' in line or 'height=' in line:
          filtered_lines.append(line)
  filtered_lines = '\n'.join(filtered_lines)
  if output_file:
     w(filtered_lines, output_file)
  print(filtered_lines)

def extract_all(input_path, output_path):
    # Create output directory if missing
    os.makedirs(output_path, exist_ok=True)

    # Open the video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {input_path}")

    frame_idx = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Read and save frames until the video ends
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        timestamp = frame_idx / fps
        timestamp_str = f"{int(timestamp // 3600):02}:{int((timestamp % 3600) // 60):02}:{int(timestamp % 60):02}.{int((timestamp * 1000) % 1000):03}"
        filename = f"frame_{timestamp_str}.png"
        cv2.imwrite(os.path.join(output_path, filename), frame)
        frame_idx += 1

    cap.release()
    print(f"Extracted {frame_idx} frames into '{output_path}/'")

def reframe_video(input_path='', output_dir='', x=0, y=0, w=0, h=0):
    """
    Crop a video to a fixed ROI.
    input_path: path to the input video
    output_path: path to the output video
    x: x coordinate of the top-left corner of the ROI
    y: y coordinate of the top-left corner of the ROI
    w: width of the ROI
    h: height of the ROI
    """
    utils.mkdir(output_dir)

    if not Path(input_path).exists():
        sys.exit(f"Input file not found: {input_path}")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        sys.exit(f"Cannot open video: {input_path}")

    frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Processing {frame_cnt} frames…")
    print(f"ROI = (x={x}, y={y}, w={w}, h={h})")

    for idx, (ts,frame) in enumerate(get_frames(input_path, yield_timestamps=True)):
        crop = frame[y:y+h, x:x+w]
        # Save each cropped frame as an image
        frame_output_path = os.path.join(output_dir, f'frame_{ts:.3f}.png')
        cv2.imwrite(frame_output_path, crop)

        if idx % 100 == 0:
            print(f"…{idx}/{frame_cnt}")

    cap.release()

def filter_timestamps(timestamps):
  """
  Inputs: list of floats
  Outputs: list of floats separated by at least 1 second
  """
  filtered_timestamps = []
  for i, value in enumerate(timestamps):  # Convert values to floats
    if i == 0 or (value - filtered_timestamps[-1] >= 1.0):
      filtered_timestamps.append(value)
  return filtered_timestamps

def reframe_video_mem(input_path='', x=0, y=0, w=0, h=0, every_nth_frame=None):
    """
    Crop a video to a fixed ROI.
    input_path: path to the input video
    output_path: path to the output video
    x: x coordinate of the top-left corner of the ROI
    y: y coordinate of the top-left corner of the ROI
    w: width of the ROI
    h: height of the ROI
    """
    # get frames from input_path and crop
    timestamps_crops = []
    for idx, (ts,frame) in enumerate(get_frames(input_path, yield_timestamps=True, every_nth_frame=every_nth_frame)):
        crop = frame[y:y+h, x:x+w]
        timestamps_crops.append((ts, crop))

    # return timestamps and crops
    return timestamps_crops

def template_match_folder(timestamps_and_frames=[], output_folder_path='', template_image_path='', log_file_path='', threshold=.8):
    """
    Template match each frame in the folder
    timestamps_and_frames: list of tuples (timestamp, frame)
    output_folder_path: path to the output folder
    template_image_path: path to the template image
    log_file_path: path to the log file
    threshold: threshold for determining if the template is present

    Returns:
    - list of tuples (timestamp, frame) with the template match applied
    """

    # create output folder
    utils.rm(output_folder_path)
    utils.mkdir(output_folder_path)

    # create log string and file
    log_strs = ''
    log_path = log_file_path

    # go through each frame looking for a double kill (template match each frame)
    match_timestamps = []
    for i, (ts, frame) in enumerate(timestamps_and_frames):
        
        # initialize image paths and load template image
        OUTPUT_IMAGE_PATH  = f'{output_folder_path}/{ts}.png'
        template_image_path = Path(template_image_path)
        template_image = cv2.imread(str(template_image_path))

        # Perform template matching
        result = cv2.matchTemplate(frame, template_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # log the output image path and confidence score
        log_str = f"Output Image path: {OUTPUT_IMAGE_PATH}\n"
        log_str += f"Confidence score: {max_val:.4f}\n"
        log_str += f"--------------------------------\n"
        log_strs += log_str

        # Draw a rectangle around the matched region
        h, w = template_image.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        # Save and display the result
        if max_val >= threshold:
            print(f"Template match found at {ts} with confidence {max_val:.4f}")
            cv2.imwrite(OUTPUT_IMAGE_PATH, frame)
            match_timestamps.append(ts)

    # write log and return match timestamps
    utils.w(log_strs, log_path)
    return match_timestamps

def every_nth_frame(input_path, nth_frame):
    """
    Get every nth frame of a video.
    
    Parameters:
    - input_path: str, path to the input video.
    - nth_frame: int, the interval of frames to capture (e.g., every 10th frame).
    
    Returns:
    - List of frames captured at every nth interval.
    """
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {input_path}")
    
    frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    
    for i in range(0, frame_cnt, nth_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    
    cap.release()
    return frames

def extract(timestamps, video_path):
  """
  For each timestamp, create a 3 second clip
  """
  for ts in timestamps:
    os.system(f"ffmpeg -i {video_path} -ss {ts} -t 3 -c copy {ts}.mp4")

def concat(input_file_paths, output_file="output.mp4"):
  if not input_file_paths:
    raise ValueError("No input files provided.")

  num_files = len(input_file_paths)

  # Build the ffmpeg command starting with the input files.
  ffmpeg_cmd = ["ffmpeg", "-y"]
  
  # Make the command quiet
  ffmpeg_cmd.extend(['-hide_banner', '-loglevel', 'error', '-nostats']) 

  for f in input_file_paths:
    ffmpeg_cmd.extend(["-i", f])  # Add each file as an input

  # Build the stream mapping string.
  stream_mapping = "".join(f"[{i}:v:0][{i}:a:0]" for i in range(num_files))

  # Append the concat filter
  filter_complex = f"{stream_mapping}concat=n={num_files}:v=1:a=1[outv][outa]"

  # Complete the ffmpeg command
  ffmpeg_cmd.extend([
    "-filter_complex", filter_complex,
    "-map", "[outv]", "-map", "[outa]",
    output_file
  ])

  # Print the command for debugging
  print("Running command:", " ".join(ffmpeg_cmd))

  # Execute the command
  subprocess.run(ffmpeg_cmd, check=True)

  return output_file

def extract_clip(input_path, output_path, start_time=None, end_time=None, gpu=False):
    """
    Extracts a clip from a video using ffmpeg with optional start and end times.

    For more notes see backend/test/extract_clip/README.md

    We really don't like building the string like this, it's not clear what's being executed.
    """
    # Quote paths for safety
    input_path = shlex.quote(input_path)
    output_path = shlex.quote(output_path)
    
    # Start building the base ffmpeg command
    if gpu:
        cmd = f"ffmpeg -y -loglevel error -hwaccel cuda"
    else:
        cmd = f"ffmpeg -y -loglevel error"
    
    # Add the start time if provided
    if start_time:
        cmd += f" -ss {start_time}"
    
    # Add the input file
    cmd += f" -i {input_path}"
    
    # Add the end time if provided
    # omitting end_time might be broken after adding end_time - start_time
    if end_time:
        cmd += f" -to {end_time - start_time}"
    
    # Complete the command with the copy and output options
    cmd += f" -c copy {output_path}"
    
    # Print the command and execute it
    print('----------------------------------')
    print(cmd)
    print('----------------------------------')

    # execute the command
    os.system(cmd)

    # return the output path
    return output_path

def extract_clips_global_timestamps_segment(segmentation, input_video, output_folder):
    """
    so this should write to clips and without clip_
    """
    """
    return / write: 
    - Extracts clips from an input video based on diarization results and writes them to a common folder.

    - writes a JSON file mapping each clip to its global timestamp and speaker.
    
    Parameters:
    - diarization.pkl: A pyannote.core.annotation.Annotation object containing diarization results.
    - input_video: Path to the input video file.
    - output_folder: Path to the folder where extracted clips and mapping file will be saved.
    """
    clips_folder = os.path.join(output_folder, 'clips')
    os.makedirs(clips_folder, exist_ok=True)
    
    clips_mapping = []
    for i, seg in enumerate(segmentation.get_timeline()):
        output_clip_path = os.path.join(clips_folder, f'{i}.mp4')
        extract_clip(input_video, output_clip_path, start_time=seg.start, end_time=(seg.end - seg.start))
        clips_mapping.append({
            'clip_path': output_clip_path,
            'start': seg.start,
            'end': seg.end,
        })
    
    mapping_file_path = os.path.join(output_folder, 'clips_mapping.json')
    with open(mapping_file_path, 'w') as f:
        json.dump(clips_mapping, f, indent=2)

    return clips_folder

def extract_clips_global_timestamps(diarization, input_video, output_folder):
    """
    so this should write to clips and without clip_
    """
    """
    return / write: 
    - Extracts clips from an input video based on diarization results and writes them to a common folder.

    - writes a JSON file mapping each clip to its global timestamp and speaker.
    
    Parameters:
    - diarization.pkl: A pyannote.core.annotation.Annotation object containing diarization results.
    - input_video: Path to the input video file.
    - output_folder: Path to the folder where extracted clips and mapping file will be saved.
    """
    clips_folder = os.path.join(output_folder, 'clips')
    os.makedirs(clips_folder, exist_ok=True)
    
    clips_mapping = []
    for i, (seg, track, label) in enumerate(diarization.itertracks(yield_label=True)):
        output_clip_path = os.path.join(clips_folder, f'{i}.mp4')
        extract_clip(input_video, seg.start, seg.end, output_clip_path)
        clips_mapping.append({
            'clip_path': output_clip_path,
            'start': seg.start,
            'end': seg.end,
            'speaker': label
        })
    
    mapping_file_path = os.path.join(output_folder, 'clips_mapping.json')
    with open(mapping_file_path, 'w') as f:
        json.dump(clips_mapping, f, indent=2)

    return clips_folder

def preprocess_clip(clip_path, output_dir):
    """
    Currently used in /concatenate_clips
    Takes clips sent from front_end and stored in temp
    and 'preprocesses' them and outputs them to preprocessed

    really, specifies audio and video codecs, bitrate, resolution, etc.

    reminder: codecs are within a container where mp4 is a container.
    """
    output_file_name = os.path.basename(clip_path)
    output_path = os.path.join(output_dir, output_file_name)
    clip_path_shlex = shlex.quote(clip_path)
    output_path_shlex = shlex.quote(output_path)
    print('preprocess_clip')
    #ffmpeg_command = f"ffmpeg -y -hide_banner -loglevel error -hwaccel cuda -i {clip_path_shlex} -c:v libx264 -preset superfast -c:a aac -strict experimental -b:a 192k -r 30 -s 1280x720 {output_path_shlex}"

    ffmpeg_command = f"ffmpeg -y -hide_banner -loglevel error -hwaccel cuda -i {clip_path_shlex} -c:v libx264 -c:a aac -strict experimental -b:a 192k -r 30 -s 1920x1080 {output_path_shlex}"
    os.system(ffmpeg_command)
    return output_path

def concatenate_clips(clip_folder, file_name, sort=True, rm=True):
    """
    Concatenates local clips (Cliptu specific function)

    This is coupled to the cliptu clip naming scheme, i.e.
    Nevada Rally with Vice President Kamala Harris and Governor Tim Walz-fDcXZp4Vi4Y/clips/120.mp4
    hmmmmm actually maybe it's the cloudfront urls...because there's no underscore in this url
    let's add a switch for sort so we can use it outside pipeline
    """
    clip_paths = ld(clip_folder)

    # Sorting by video name and then by the numeric suffix in the filename
    if sort:
        clip_paths.sort(key=lambda x: (
            x.rsplit('_', 1)[0],  # This gives everything before the last '_'
            int(x.rsplit('_', 1)[1].split('.')[0])  # This extracts the number between the last '_' and '.'
        ))

    # Directory to store preprocessed clips
    preprocessed_dir = 'preprocessed_clips'
    os.makedirs(preprocessed_dir, exist_ok=True)

    # Preprocess clips and create the file list for concatenation
    list_file_path = 'concat_list.txt'
    with open(list_file_path, 'w') as list_file:
        print('Preprocessing clips')
        for i,clip_path in enumerate(clip_paths):
            print(f'preprocessing clip {i}/{len(clip_paths)}')
            preprocessed_path = preprocess_clip(opj(clip_folder,clip_path), preprocessed_dir)
            preprocessed_path_replaced = preprocessed_path.replace("'", "'\\''")
            #preprocessed_path_escaped = shlex.quote(preprocessed_path)
            list_file.write(f"file '{preprocessed_path_replaced}'\n")
    # Concatenate using ffmpeg
    list_file_path_escaped=shlex.quote(list_file_path)
    file_name_escaped=shlex.quote(file_name)
    print('concatenate_clips')
    concat_command = f"ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i {list_file_path_escaped} -c copy {file_name_escaped}"
    os.system(concat_command)
    # not sure why concat_list.txt doesn't exist at this point.. get's deleted somewhere?
    if rm:
        rm(list_file_path)
        rm(clip_folder)
    return file_name

def extract_clips_speaker(speaker, diarization, input_video, output_folder):
    """
    Extracts clips for a specific speaker from an input video based on diarization results.
    
    Parameters:
    - speaker: The target speaker identifier (e.g., "speaker_xx").
    - diarization: A pyannote.core.annotation.Annotation object containing diarization results.
    - input_video: Path to the input video file.
    - output_folder: Path to the folder where extracted clips will be saved.
    
    Returns:
    - The path to the output folder where clips are saved.
    """
    mkdir(output_folder)
    for i, (seg, track, label) in enumerate(diarization.itertracks(yield_label=True)):
        if label == speaker:
            output_clip_path = f'{output_folder}/{i}.mp4'
            extract_clip(input_video, seg.start, seg.end, output_clip_path)
    return output_folder

def extract_clips_all_speakers(diarization, input_video, output_folder):
    """
    Extracts clips for a specific speaker from an input video based on diarization results.
    
    Parameters:
    - diarization: A pyannote.core.annotation.Annotation object containing diarization results.
    - input_video: Path to the input video file.
    - output_folder: Path to the folder where extracted clips will be saved.
    
    Returns:
    - The path to the output folder where clips are saved. Clips are stored in a folder for each speaker.
    """

    speakers = set()
    for i, (seg, track, label) in enumerate(diarization.itertracks(yield_label=True)):
      speakers.add(label)
    
    output_folder = opj(output_folder,'clips')

    for speaker in speakers:
      mkdir(opj(output_folder,speaker))

    clip_paths =[]
    for i, (seg, track, label) in enumerate(diarization.itertracks(yield_label=True)):
        output_clip_path = f'{output_folder}/{label}/{i}.mp4'
        extract_clip(input_video, seg.start, seg.end, output_clip_path)
        clip_paths.append(d(output_clip_path))
    return clip_paths

def extract_clips(diarization,input_video, output_folder):
  for i, (seg, track, label) in enumerate(diarization.itertracks(yield_label=True)):
    output_clip_path = f'{output_folder}/{i}.mp4'
    extract_clip(input_video, seg['start'], seg['end'], output_clip_path)
  return output_folder
