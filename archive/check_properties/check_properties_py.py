import os; import uuid; import subprocess; import happy_utils as utils; import sys

from yt_dlp import YoutubeDL

def hook(d):
  print('hoook', flush=True)
  if d['status'] == 'downloading':
    print('Download started:', d['_filename'])  # Your custom hook here

def download_stream(streamer='TchiKK', output_folder='streams'):
  ydl_opts = {
    'cookiefile': 'cookies.txt',
    'quiet': True,            # suppress all output except errors
    'wait_for_video': 600,
    'progress_hooks': [hook],
    'format_sort': ['vcodec:h265', 'acodec:aac'],
    'outtmpl': f'{output_folder}/{uuid.uuid4().hex}.%(ext)s'
  }
  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([f'https://www.twitch.tv/{streamer}'])


def check_properties(file='', video_codec='', audio_codec='', pid=''):
  """
  Checks the properties of the stream.
  """
  # Ensure stream is downloading (check if file exists)
  if not os.path.exists(file):
    print(f"{file} does not exist")
    subprocess.Popen(['kill', pid])
    return

  # Run an ffmpeg command to check the properties of the stream
  ffmpeg_cmd = [
    'ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', f'{file}'
  ]
  result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
  stdout = result.stdout
  stderr = result.stderr
  streams = utils.jls(stdout)['streams']
  if streams[0]['codec_name'] != video_codec:
    print(f"{streams[0]['codec_name']} != {video_codec}")
    subprocess.Popen(['kill', pid])
  elif streams[1]['codec_name'] != audio_codec:
    print(f"{streams[1]['codec_name']} != {audio_codec}")
    subprocess.Popen(['kill', pid])
  else:
    print(f"{file} passed all checks")

if __name__ == '__main__':
  video_codec = 'h265'
  audio_codec = 'aac'
  #for streamer in ['ItzTheLastShot', 'TchiKK', 'Preecisionn']:
  for streamer in ['TriPPPeY']:
    pid = download_stream(streamer=streamer, output_folder='streams')