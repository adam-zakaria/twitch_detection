import subprocess; import utils.utils as utils; import uuid

def download_twitch_streams():
  processes = [] 
  # If streamer is live, download stream --------------------
  #for streamer in ['aPG']:
  for streamer in ['Gunplexion']:
    output_dir = f'twitch_streams/{streamer}';
    # Is streamer live?
    if "The channel is not currently live" in subprocess.run(['yt-dlp', '--get-url', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}','-o', f'{output_dir}/stream.%(ext)s'], text=True, capture_output=True).stderr: # text = true converts the stdout and stderr streams to Python str objects (text).
      print(f"{streamer} is not currently live.")
    else:
      # if live, download stream
      utils.mkdir(output_dir)
      print(f"Downloading stream for {streamer}...")
      process = subprocess.Popen(['yt-dlp', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}','-o', f'{output_dir}/{uuid.uuid4().hex}.%(ext)s'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); processes.append(process)

  for process in processes:
    process.wait()

"""
# Notes 
## Streamer list
['Luciid_TW', 'itzthelastshot', 'SpartanTheDogg', 'SnakeBite', 'aPG']:
"""
if __name__ == "__main__":
  download_twitch_streams()
