import uuid
import subprocess
import os

class TwitchStream:
  def __init__(self, streamer, vcodec='h265', acodec='aac', stream_output_path = 'streams'):
    self.detections = []
    self.acodec = acodec
    self.vcodec = vcodec

  def __str__(self):
    return f"{self.title} - {self.url} - {self.start_time} - {self.end_time}"
  
  def download_stream(self):
    # --cookies : so yt-dlp uses twitch creds, they should last for a while

    # --wait-for-video : so yt-dlp waits for the stream to start
    cmd = [
        'yt-dlp', '--cookies', 'cookies.txt', '--wait-for-video', '600', '-S', f'vcodec:{self.vcodec},acodec:{self.acodec}',
        f'https://www.twitch.tv/{self.streamer}', '-o',
        f'{self.stream_output_path}/{uuid.uuid4().hex}.%(ext)s'
    ]

    p = subprocess.Popen(cmd, preexec_fn=lambda: os.setpgid(0, 0),
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

  def run_detection(self):
    pass