import os
import subprocess

def template_match():
  # stub 
  return [2.3, 2.33, 2.34, 2.35, 5.0, 5.02, 5.04]

def filter(timestamps, min_gap=3.0):
  """
  Inputs: list of floats
  Outputs: list of floats separated by at least 1 second
  """
  filtered_timestamps = []
  for i, value in enumerate(timestamps):  # Convert values to floats
    if i == 0 or (value - filtered_timestamps[-1] >= min_gap):
      filtered_timestamps.append(value)
  return filtered_timestamps

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
  ffmpeg_cmd = ["ffmpeg", "-y", "-hide_banner"]
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
  print("*"*100)
  print(ffmpeg_cmd)
  print("*"*100)
  subprocess.run(ffmpeg_cmd, check=True)

if __name__ == "__main__":
  import cliptu.clip as clip
  paths = []
  for timestamp in [10.0, 30.0, 50.0]:
    paths.append(clip.extract_clip(f'lastshot.mp4', f'{timestamp}.mp4', timestamp, timestamp + 3))
  
  concat(paths)
