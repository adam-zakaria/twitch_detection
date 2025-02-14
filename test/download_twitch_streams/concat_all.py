#!/usr/bin/env python3
import glob
import os
import subprocess
import debug_pipeline_all  # Assuming this is needed elsewhere in your pipeline
import utils.utils as utils  # Assuming utils.w is your file-writing function
import cliptu.clip as clip

def concat_all(input_file_paths, concat_list_path):
    print("Input file paths:")
    print(input_file_paths)
    print("Starting clip concatenation.")

    # Build the concat file content
    concat_file_content = ""
    for clip_path in input_file_paths:
        print(f"Adding {clip_path} to concatenation list.")
        # Each line must be in the form: file 'relative_or_absolute_path'
        concat_file_content += f"file '{clip_path}'\n"

    # Write the list to the provided concat file path
    utils.w(concat_file_content, concat_list_path)

    # Build the ffmpeg command
    # This command uses the concat demuxer to read the file list,
    # then forces the output to 60 fps (with a filter) and re-encodes using libx264.
    """
    # Not working, even with correctly extracted clips
    cmd = [
        "ffmpeg",
        "-y",                # Overwrite output file without asking
        "-hide_banner",      # Hide non-critical output
        "-f", "concat",      # Use the concat demuxer
        "-safe", "0",        # Allow unsafe file paths in the list
        "-i", concat_list_path,
        "output.mp4"         # Output file name
    ]
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-vf", "fps=60,format=yuv420p",
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-af", "aresample=async=1",
        "-movflags", "+faststart",
        "output.mp4"
    ]

    print("Running ffmpeg command:")
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)  # Raises an error if the command fails

    print("Concatenated video saved as output.mp4.")

if __name__ == "__main__":
    # Find all the input clips matching the pattern.
    input_files = glob.glob('output/*/*/concat/output.mp4')
    #input_files = ['/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/Bound/02_11_2025_20_06_30/extract/42_1.mp4', '/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/formal/02_11_2025_19_23_23/extract/238_56666666666666.mp4', '/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/royal2/02_11_2025_19_44_43/extract/155_78333333333333.mp4', '/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/Tripppey/02_11_2025_18_59_03/extract/79_73333333333333.mp4']
    # Specify a temporary file that will list the input clips.
    #concat_list_file = "concat_files.txt"
    #concat_all(input_files, concat_list_file)
    clip.concatenate_clips('concat_clips', 'concatenate_clips_3.mp4', sort=False, rm=False)
