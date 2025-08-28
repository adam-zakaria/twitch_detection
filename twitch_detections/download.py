import os
import signal
import subprocess
import happy_utils as utils
import signal
import subprocess

def start_downloads(streamers, processes):
  """
  Enable cliptu to download halo twitch streams 24/7 and create double kill compilations
  """
  # Start downloads
  # clear out any old entries from process list
  processes.clear()
  for streamer in streamers:
    # Create output folder
    output_folder = f'output/{streamer}/stream/'
    utils.mkdir(output_folder)
    output_file_path = utils.opj(output_folder, f'{streamer}_{utils.ts()}.mp4')
    print(f'Starting download for {streamer}')
    # download and output to output/{streamer}/stream/{streamer.mp4}
    proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", '-q', "--wait-for-video", "600", "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}", '-o', output_file_path ], preexec_fn=os.setsid)
    processes.append(proc)

def kill_downloads(processes):
  # Kill processes
  print('Killing all downloads')
  for proc in processes:
    os.killpg(proc.pid, signal.SIGINT)
    # os.killpg(proc.pid, signal.SIGKILL)
    # proc.wait() # Best practice to fully cleanup subprocess
