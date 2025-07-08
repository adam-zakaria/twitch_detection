import subprocess
import os

def concat_videos(file1, file2, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Create the file list required by the concat demuxer
    concat_list_path = os.path.join(output_folder, "concat_files.txt")
    with open(concat_list_path, "w") as f:
        # Each line must be: file 'path/to/file'
        f.write(f"file '{file1}'\n")
        f.write(f"file '{file2}'\n")
    
    # Build the ffmpeg command using the concat demuxer
    cmd = [
        "ffmpeg", "-y", "-hide_banner",
        "-f", "concat",    # Force concat demuxer
        "-safe", "0",      # Allow unsafe file paths (absolute paths, etc.)
        "-i", concat_list_path,
        #"-loglevel", "error",
        "-threads", "0",
        os.path.join(output_folder, "output.mp4")
    ]
    
    # Execute the command
    subprocess.run(cmd, check=True)
    
    # Print the command and confirmation message
    print(' '.join(cmd))
    print(f"Concatenated video saved in {os.path.join(output_folder, 'output.mp4')}.")

# Example usage:
file1 = "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/Tripppey/02_11_2025_18_59_03/extract/79_73333333333333.mp4"
file2 = "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/formal/02_11_2025_19_23_23/extract/238_56666666666666.mp4"
#output_folder = "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/Concatenated"
output_folder = "."

concat_videos(file1, file2, output_folder)
