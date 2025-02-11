#output/*/*/concat/output.mp4
import glob; import debug_pipeline_all; import utils.utils as utils; import os; import subprocess;

def concat_all(input_file_paths, output_file_path):
  # Non-recursive glob (assuming exactly two subdirectories)
  print(input_file_paths)
  print("Starting clip concatenation.")
  clip_paths = ''
  for clip_path in input_file_paths:
    # clip_path = os.path.basename(clip_path)
    print(f"Adding {clip_path} to concatenation list.")
    clip_paths += f"file '{clip_path}'\n"
    #utils.wa(f"file '{clip_path}'\n", f'output_file_path')  # path to clip must be relative to path of output_file_path
  utils.w(clip_paths, output_file_path)

    # Works, with slight freeze on clip transition
  cmd = [
      "ffmpeg", "-y", "-hide_banner", "-f", "concat", 
      "-safe", "0", "-i", output_file_path, 
      f"output.mp4"
  ]
  subprocess.run(
    cmd,
    check=True  # Raises an error if the command fails
  )
  print(' '.join(cmd))
  print(f"Concatenated video saved in output.mp4.")


if __name__ == "__main__":
  concat_all(glob.glob('output/*/*/concat/output.mp4'), 'concat_files.txt')