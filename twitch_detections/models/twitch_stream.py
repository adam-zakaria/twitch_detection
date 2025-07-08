import uuid
import subprocess
import os
from yt_dlp import YoutubeDL, utils as ytdlp_utils

import threading

class TwitchStream:
  def __init__(self, vcodec='h265', acodec='aac', stream_output_path = 'streams', streamer=''):
    self.detections = []
    self.acodec = acodec
    self.vcodec = vcodec
    self.streamer = streamer

  def __str__(self):
    return f"{self.title} - {self.url} - {self.start_time} - {self.end_time}"

  def download_stream(self, output_folder='streams'):
    cmd = [
        'yt-dlp', '--cookies', 'cookies.txt', '--wait-for-video', '600', '-S', f'vcodec:h265,acodec:aac', '--no-part',
        f'https://www.twitch.tv/{self.streamer}']
    p = subprocess.Popen(cmd, preexec_fn=lambda: os.setpgid(0, 0), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # p = subprocess.Popen(cmd)

  def run_detection(self):
    pass