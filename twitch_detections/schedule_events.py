"""
Imports
"""

import schedule
import os
import signal
import subprocess
import time
import happy_utils as utils
import process
import glob
import atexit
import signal
import subprocess
import sys
import config
import download
from datetime import datetime, timedelta

def hms(seconds):
  # Convert seconds to HH:MM:SS format
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60
  return f"{hours}:{minutes}:{seconds}"

def cleanup_on_exit():
  print('[CLEANUP] Killing twitch.tv downloads...')
  subprocess.run("ps aux | grep '[t]witch.tv' | awk '{print $2}' | xargs kill -9", shell=True)
  subprocess.run("ps aux | grep '[f]fmpeg' | awk '{print $2}' | xargs kill -9", shell=True)
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

  # Clear log files
  utils.rm('/home/ubuntu/.pm2/logs/twitch-out.log')

  # Start downloads now
  processes = []
  print(f'Starting downloads at {utils.ts()}')
  print(f'Going to run process in {config.process_time} minutes')
  download.start_downloads(streamers, processes)

  # Schedule events to happen later
  # Kill downloads
  schedule.every().day.at(kill_time).do(
    download.kill_downloads,
    processes
  )
  # Process downloads
  schedule.every().day.at(process_time).do(
    process.process_streams
  )
  # Start downloads again
  # schedule.every().day.at(restart_download_time).do(
  #   download.start_downloads,
  #   streamers,
  #   processes
  # )
  # Infinite loop so schedule can fire events 
  while True:
    schedule.run_pending()
    time.sleep(1)