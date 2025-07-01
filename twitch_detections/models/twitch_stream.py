import uuid
import subprocess
import os
from yt_dlp import YoutubeDL

class TwitchStream:
  def __init__(self, vcodec='h265', acodec='aac', stream_output_path = 'streams', streamer=''):
    self.detections = []
    self.acodec = acodec
    self.vcodec = vcodec
    self.streamer = streamer

  def __str__(self):
    return f"{self.title} - {self.url} - {self.start_time} - {self.end_time}"


  def download_stream(self, output_folder='streams'):
    ydl_opts = {
      'cookiefile': '/Users/azakaria/Code/twitch_detections/cookies.txt',
      'quiet': True,            # suppress all output except errors
      'wait_for_video': (600, 600), # min and max wait time for video to be available
      'format_sort': ['vcodec:h264', 'acodec:aac'],
      'outtmpl': f'{output_folder}/{self.streamer}.%(ext)s'
    }
    with YoutubeDL(ydl_opts) as ydl:
      ydl.download([f'https://www.twitch.tv/{self.streamer}'])

  def run_detection(self):
    pass