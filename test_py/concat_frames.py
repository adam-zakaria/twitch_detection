import subprocess
from pathlib import Path

# Define input directories
true_frames_dir = Path('/Users/azakaria/Code/twitch_highlights/input_frames/true')
false_frames_dir = Path('/Users/azakaria/Code/twitch_highlights/input_frames/false')

def create_video_from_frames(input_dir, output_path, fps=30):
    # Ensure input directory exists
    if not input_dir.exists():
        print(f"Directory {input_dir} does not exist")
        return
    
    # FFmpeg command to create video from frames
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output file if it exists
        '-framerate', str(fps),
        '-pattern_type', 'glob',
        '-i', str(input_dir / '*.png'),  # Input pattern
        '-c:v', 'libx264',  # Use H.264 codec
        '-pix_fmt', 'yuv420p',  # Pixel format for better compatibility
        '-preset', 'fast',  # Encoding preset (fast encoding)
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Video saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating video: {e.stderr.decode()}")

# Create videos for both true and false frames
create_video_from_frames(true_frames_dir, 'true_frames.mp4')
create_video_from_frames(false_frames_dir, 'false_frames.mp4')

# Concatenate true and false videos
def concatenate_videos(video_files, output_path):
    # Create a text file listing the videos to concatenate
    with open('concat_list.txt', 'w') as f:
        for video in video_files:
            f.write(f"file '{video}'\n")
    
    # FFmpeg command to concatenate videos
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output file if it exists
        '-f', 'concat',
        '-safe', '0',
        '-i', 'concat_list.txt',
        '-c', 'copy',  # Copy streams without re-encoding
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"Concatenated video saved to {output_path}")
        # Clean up the temporary file
        Path('concat_list.txt').unlink()
    except subprocess.CalledProcessError as e:
        print(f"Error concatenating videos: {e.stderr.decode()}")

# Concatenate the videos
video_files = ['true_frames.mp4', 'false_frames.mp4']
concatenate_videos(video_files, 'combined_frames.mp4')




