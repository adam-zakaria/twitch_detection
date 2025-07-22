import subprocess
import os
import signal
import happy_utils as utils
import time

# streamer
streamer = 'luciid_tw'
output_folder = 'output'

# No --wait-for-video
#proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", '-q', "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}", '-o'])

# --wait-for-video
proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", '-q', "--wait-for-video", "600", "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}", '-o', f'{output_folder}/{streamer}-{utils.ts()}.mp4'], preexec_fn=os.setsid)

time.sleep(5)
#os.killpg(proc.pid, signal.SIGINT)

"""
Results:
* If popen and program naturally exits AND *terminal is left running*, yt-dlp keeps running. Surprising.
* If popen and program naturally exits AND *terminal is killed*, yt-dlp keeps running. Surprising.
"""