"""
Imports
"""

import schedule
import os
import signal
import subprocess
import time
import happy_utils as utils
import process_stream
import glob
import atexit
import signal
import subprocess
import sys
import config
from datetime import datetime, timedelta

"""
Function which enable cliptu to download halo twitch streams 24/7 and create double kill compilations
"""

def start_downloads(streamers, processes):
  # Start downloads
  # clear out any old entries from process list
  processes.clear()
  for streamer in streamers:
    # Create output folder
    output_folder = f'output/{streamer}/stream/'
    utils.mkdir(output_folder)
    print(f'Starting download for {streamer}')
    # download and output to output/{streamer}/stream/{streamer.mp4}
    proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", '-q', "--wait-for-video", "600", "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}", '-o',
    #proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}", '-o',
    f'{output_folder}/{streamer}-{utils.ts()}.mp4'], preexec_fn=os.setsid)
    processes.append(proc)

def kill_downloads(processes):
  # Kill processes
  print('Killing all downloads')
  for proc in processes:
    os.killpg(proc.pid, signal.SIGINT)
    # os.killpg(proc.pid, signal.SIGKILL)
    # proc.wait() # Best practice to fully cleanup subprocess

def process_streams():
  # start processing once the streams are killed
  print('process_streams()')
  # process
  for stream_path in glob.glob(f'output/**/stream/*.mp4'):
    process_stream.process_stream(stream_path)
  # remove processed streams
  try:
    for stream_path in glob.glob(f'output/**/stream/*.mp4'):
        utils.rm(stream_path)
  except:
    pass

def cleanup_on_exit():
  print('[CLEANUP] Killing twitch.tv downloads...')
  subprocess.run("ps aux | grep '[t]witch.tv' | awk '{print $2}' | xargs kill -9", shell=True)
  for stream_path in glob.glob(f'output/**/stream/*.mp4'):
      utils.rm(stream_path)

if __name__ == "__main__":
  """
  * Init config data
  * Register cleanup on exit
  * Start downloads
  * Kill downloads
  * Process downloads
  * Start downloads again
  """

  # Init config data
  streamers = config.streamers
  now = datetime.now()
  kill_time = (now + timedelta(minutes=config.kill_time)).strftime("%H:%M:%S")
  process_time = (now + timedelta(minutes=config.process_time)).strftime("%H:%M:%S")
  restart_download_time = (now + timedelta(minutes=config.restart_download_time)).strftime("%H:%M:%S")

  # Register cleanup on normal exit, and catch signals like Ctrl+C and kill
  atexit.register(cleanup_on_exit)
  signal.signal(signal.SIGINT, lambda s, f: sys.exit(1))   # Ctrl+C
  signal.signal(signal.SIGTERM, lambda s, f: sys.exit(1))  # kill or shutdown

  # Start downloads now
  processes = []
  start_downloads(streamers, processes)

  # Schedule events to happen later
  # Kill downloads
  schedule.every().day.at(kill_time).do(
    kill_downloads,
    processes
  )
  # Process downloads
  schedule.every().day.at(process_time).do(
    process_streams
  )
  # Start downloads again
  schedule.every().day.at(restart_download_time).do(
    start_downloads,
    streamers,
    processes
  )
  # Infinite loop so schedule can fire events 
  while True:
    schedule.run_pending()
    time.sleep(1)