import os; import uuid; import subprocess; import happy_utils as utils; import sys

"""
There's the acodec, vcodec, and container.
"""

# streamer = 'TchiKK'
# output = f'streams/{uuid.uuid4().hex}.%(ext)s'
# yt_dlp_cmd = [
#   'yt-dlp', '--cookies', 'cookies.txt', '--wait-for-video', '600',
#   '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}',
#   '-o', output
# ]
# subprocess.run(yt_dlp_cmd)  # safer and supports list-form

# Run an ffmpeg command to check the properties of the stream
"""
for f in utils.ls('streams'):
  ffmpeg_cmd = [
    'ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', f'{f}'
  ]
  print(ffmpeg_cmd)
  #breakpoint()
  subprocess.run(ffmpeg_cmd)  # safer and supports list-form
"""