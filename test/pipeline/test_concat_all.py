#!/usr/bin/env python3
import subprocess
import json

# List of video file paths to analyze.
clip_paths = [
    "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/Tripppey/02_11_2025_18_59_03/extract/79_73333333333333.mp4",
    "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/royal2/02_11_2025_19_44_43/extract/155_78333333333333.mp4",
    "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/formal/02_11_2025_19_23_23/extract/238_56666666666666.mp4",
    "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/Bound/02_11_2025_20_06_30/extract/42_1.mp4"
]

# Dictionary to store the ffprobe output for each clip.
results = {}

# Loop over each clip path and run ffprobe.
for clip in clip_paths:
    # Define the ffprobe command. The command queries:
    #   - codec_name: The video codec used.
    #   - width & height: Resolution of the video.
    #   - avg_frame_rate: Average frame rate.
    #   - duration: Duration of the stream.
    command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=codec_name,width,height,avg_frame_rate,duration",
        "-of", "json",
        clip
    ]
    
    try:
        # Run the command and capture the output.
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        # Parse the JSON output from ffprobe.
        data = json.loads(process.stdout)
        results[clip] = data
    except subprocess.CalledProcessError as e:
        print(f"Error processing file: {clip}\nError: {e.stderr}")
        results[clip] = {"error": e.stderr}
    except json.JSONDecodeError as je:
        print(f"Error decoding JSON for file: {clip}\nRaw output: {process.stdout}")
        results[clip] = {"error": "JSON decode error", "raw_output": process.stdout}

# Write all the results to a single JSON file.
output_file = "ffprobe_output.json"
with open(output_file, "w") as outfile:
    json.dump(results, outfile, indent=4)

print(f"Analysis complete. Results written to {output_file}")
