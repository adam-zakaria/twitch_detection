import schedule
import os
import signal
import subprocess
import time

def start_procs(streamers, procs):
  # Start downloads
  # clear out any old entries from process list
  procs.clear()
  for streamer in streamers:
    proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", "--wait-for-video", "600", "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}"], preexec_fn=os.setsid)
    procs.append(proc)

def kill_procs(procs):
  # Kill processes
  for proc in procs:
    os.killpg(proc.pid, signal.SIGINT)
    proc.wait() # Best practice to fully cleanup subprocess

# Start downloads now
streamers = ['Luciid_TW', 'Formal', 'frosty']
procs = []
start_procs(streamers, procs)

# Kill downloads at 2PM everyday
schedule.every().day.at("15:08").do(
  kill_procs,
  procs
)

# Start downloads at 201PM everyday
schedule.every().day.at("15:10").do(
  start_procs,
  streamers,
  procs
)

while True:
  schedule.run_pending()
  time.sleep(1)