import schedule
import os
import signal
import subprocess
import time
import happy_utils as utils
import pipeline
import glob
import atexit
import signal
import subprocess
import sys


def start_download_procs(streamers, procs):
  # Start downloads
  # clear out any old entries from process list
  procs.clear()
  for streamer in streamers:
    # Create output folder
    output_folder = f'output/{streamer}/stream/'
    utils.mkdir(output_folder)
    print(f'Starting download for {streamer}')
    # download and output to output/{streamer}/stream/{streamer.mp4}
    proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", '-q', "--wait-for-video", "600", "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}", '-o',
    #proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}", '-o',
    f'{output_folder}/{streamer}-{utils.ts()}.mp4'], preexec_fn=os.setsid)
    procs.append(proc)

def kill_download_procs(procs):
  # Kill processes
  print('Killing all downloads')
  for proc in procs:
    os.killpg(proc.pid, signal.SIGINT)
    # os.killpg(proc.pid, signal.SIGKILL)
    # proc.wait() # Best practice to fully cleanup subprocess

def process_streams():
  # start processing once the streams are killed
  print('process_streams()')
  # process
  for stream_path in glob.glob(f'output/**/stream/*.mp4'):
    pipeline.process(stream_path)
  # remove processed streams
  for stream_path in glob.glob(f'output/**/stream/*.mp4'):
      utils.rm(stream_path)

# Start downloads now
#streamers = ['hunter_jjx', 'vsweetheart', 'perkushon', 'formal'] 
streamers = ['vincesega', 'Pandas_POV', 'Aldonaitorr', 'luciid_tw'] 
procs = []
start_download_procs(streamers, procs)

# generate times for testing
from datetime import datetime, timedelta
now = datetime.now()
kill_time = (now + timedelta(seconds=60)).strftime("%H:%M:%S")
process_time = (now + timedelta(seconds=90)).strftime("%H:%M:%S") # kill_time + 1
restart_download_time = (now + timedelta(seconds=120)).strftime("%H:%M:%S") # process_time + 1

schedule.every().day.at(kill_time).do(
  kill_download_procs,
  procs
)

# Process streams
schedule.every().day.at(process_time).do(
  process_streams
)

# Redownload streams
schedule.every().day.at(restart_download_time).do(
  start_download_procs,
  streamers,
  procs
)

def cleanup():
    print('[CLEANUP] Killing twitch.tv downloads...')
    subprocess.run("ps aux | grep '[t]witch.tv' | awk '{print $2}' | xargs kill -9", shell=True)

# Register cleanup on normal exit
atexit.register(cleanup)

# Catch signals like Ctrl+C and kill
signal.signal(signal.SIGINT, lambda s, f: sys.exit(1))   # Ctrl+C
signal.signal(signal.SIGTERM, lambda s, f: sys.exit(1))  # kill or shutdown

while True:
  schedule.run_pending()
  time.sleep(1)