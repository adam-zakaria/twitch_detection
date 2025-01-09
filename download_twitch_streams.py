import subprocess; import utils.utils as utils

# If streamer is live, download stream --------------------

for streamer in ['aPG', 'Gunplexion']:
  output_dir = f'twitch_streams/{streamer}';
  # Is streamer live?
  if "The channel is not currently live" in subprocess.run(['yt-dlp', '--get-url', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}','-o', f'{output_dir}/stream.%(ext)s'], text=True, capture_output=True).stderr: # text = true converts the stdout and stderr streams to Python str objects (text).
    print(f"{streamer} is not currently live.")
  else:
    # if live, download stream
    utils.mkdir(output_dir)
    print(f"Downloading stream for {streamer}...")
    import uuid
    subprocess.Popen(['yt-dlp', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}','-o', f'{output_dir}/{uuid.uuid4().hex}.%(ext)s'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Set a new process group)

while(True):
  pass

"""
# Notes ####################
# Problems . . .
One problem right now is if the streams start and stop, which is common. The existing will file be deleted. Also, when we restart the script, new download streams start. At least, ps | grep python shows the yt-dlps.

If we close the download_twitch_streams.py it stops running part if we're doing watchman...

Maybe this actually isn't a problem, just watchman quirks

Maybe just give the file names uuids? and remove the folders once the detections are run.

# Streamer list
['Luciid_TW', 'ItsTheLastShot', 'SpartanTheDogg', 'SnakeBite', 'aPG']:
"""
