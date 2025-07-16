import twitch_detections.models.twitch_stream as twitch_stream
import threading
import schedule
import os
import signal
import subprocess
import time

procs = []
for streamer in ['mean3st', 'Trunks', 'HuNteR_Jjx']:
  proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", "--wait-for-video", "600", "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}"], preexec_fn=os.setsid)
  procs.append(proc)

# schedule killing and restarting of processes
for proc in procs:
    # kill proc
    schedule.every().day.at("13:59").do(
        os.killpg,        # function reference
        proc.pid,         # first arg
        signal.SIGINT     # second arg
    )

    # restart proc
    schedule.every().day.at("14:00").do(
        proc.start()
    )

while True:
  schedule.run_pending()
  time.sleep(1)