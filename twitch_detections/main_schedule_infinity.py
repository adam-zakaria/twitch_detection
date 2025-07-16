import twitch_detections.models.twitch_stream as twitch_stream
import threading
import schedule
import os
import signal
import subprocess
import time

def start_procs(streamers, procs):
  for streamer in streamers:
    procs.append(subprocess.Popen('yt-dlp'), os.setsid())

def kill_procs(procs):
  for proc in procs:
    os.killpg(proc)

procs = []

start_procs(procs)

schedule.start('4', kill_procs, procs)
schedule.start('401', start_procs, streamers, procs)

while True:
  schedule.run_pending()
  sleep(1)
