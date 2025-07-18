import schedule
import os
import signal
import subprocess
import time
import happy_utils as utils
import pipeline
import path
import glob

"""
Instead of start and killing processes, just process videos which are after the time and remove the ones before. Or some other kind of file maintenance. Not sure this is really possible, because new streams would still need to be created...
"""
"""
Currently:

* Exploring cases:
  * A streamer is not streaming - if retry is configured, os.killpg does not work. But it does not need to work - the point of killing a download is so that the stream can be processed and redownloaded with another filename. 
  * Restart works for a streamer streaming
  * If there are two streamers streaming and one is live and one is not, it SEEMs like the WAIT of the not live will block the live processing. It's possible it's just the term that's blocked, and it's surprising because I'd think these are independent processes. Should have process write to files to confirm this is indeed getting blocked.

  Weirdly though, the other streamers download is still working...

  Yes confirmed, log.txt never gets written to.
  * 
 
Logging would be nice.
"""



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
  print('kill_download_procs()')
  for proc in procs:
    os.killpg(proc.pid, signal.SIGINT)
    # os.killpg(proc.pid, signal.SIGKILL)
    proc.wait() # Best practice to fully cleanup subprocess

def process_streams():
  # start processing once the streams are killed.
  for stream_path in glob.glob(f'output/**/stream/*.mp4'):
    pipeline.process(stream_path)

# Start downloads now
streamers = ['Gunplexion'] 
procs = []
start_download_procs(streamers, procs)

# generate times for testing
from datetime import datetime, timedelta
now = datetime.now()
kill_time = (now + timedelta(minutes=1)).strftime("%H:%M")
process_time = (now + timedelta(minutes=2)).strftime("%H:%M")
restart_download_time = (now + timedelta(minutes=6)).strftime("%H:%M")

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

while True:
  schedule.run_pending()
  time.sleep(1)