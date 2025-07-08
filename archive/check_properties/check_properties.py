import os; import uuid; import subprocess; import happy_utils as utils; import sys; import threading

def process_yt_dlp_output(proc, output_path, video_codec, audio_codec):
  for line in proc.stdout:
    print(line.strip())
    if '[download]' in line:
      print(f'Download has started (PID {proc.pid})')
      check_properties(file=output_path, video_codec=video_codec, audio_codec=audio_codec, pid=proc.pid)
      break

def download_stream(streamer, output_folder='streams'):
  output_path = f'{output_folder}/{uuid.uuid4().hex}.mp4'
  #output_template = f'{output_folder}/%(title)s.%(ext)s'

  cmd = [
    'yt-dlp', '--cookies', 'cookies.txt', '--wait-for-video', '600',
    '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}',
    '-o', output_path
  ]
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
  # start thread
  thread = threading.Thread(target=process_yt_dlp_output, args=(proc, output_path, video_codec, audio_codec))
  thread.start()


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
  for streamer in ['ItzTheLastShot', 'TchiKK', 'Preecisionn']:
    pid = download_stream(streamer=streamer, output_folder='streams')
  
  """
  Okay, having a tough time staying focused. This is being done so that there is something to show off.
  Something to keep me busy and motivated while applying to jobs. Demonstrate my programming skills so I don't need to work for some shitty company.


  """