import uuid
import subprocess
import os
from yt_dlp import YoutubeDL, utils as ytdlp_utils

import threading
from multiprocessing import Process

class TwitchStream:
  def __init__(self, vcodec='h265', acodec='aac', stream_output_path = 'streams', streamer=''):
    self.detections = []
    self.acodec = acodec
    self.vcodec = vcodec
    self.streamer = streamer

  def __str__(self):
    return f"{self.title} - {self.url} - {self.start_time} - {self.end_time}"

  def download_stream(self, output_folder='streams'):
    p = Process(target=self._download_stream_process, args=(output_folder,))
    p.start()
    return p

  def _download_stream_process(self, output_folder):
    cmd = [
        'yt-dlp', '--cookies', 'cookies.txt', '--wait-for-video', '600', '-S', f'vcodec:h265,acodec:aac', '--no-part',
        f'https://www.twitch.tv/{self.streamer}']
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

  def run_detection(self):
    pass