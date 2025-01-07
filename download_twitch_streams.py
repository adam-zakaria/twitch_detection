import subprocess; import utils.utils as utils

# If streamer is live, download stream --------------------
#for streamer in ['Luciid_TW', 'ItsTheLastShot', 'SpartanTheDogg', 'SnakeBite', 'aPG']:
for streamer in ['LuciidTW']:
  output_dir = f'twitch_streams/{streamer}';
  # Is streamer live?
  if "The channel is not currently live" in subprocess.run(['yt-dlp', '--get-url', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}','-o', f'{output_dir}/stream.%(ext)s'], text=True, capture_output=True).stderr: # text = true converts the stdout and stderr streams to Python str objects (text).
  #if "The channel is not currently live" in subprocess.run(['yt-dlp', '--get-url', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}','-o', f'{output_dir}/stream.%(ext)s'], text=True).stderr: # text = true converts the stdout and stderr streams to Python str objects (text).
    print(f"{streamer} is not currently live.")
  else:
    # if live, download stream
    utils.rm_mkdir(output_dir)
    print(f"Downloading stream for {streamer}...")
    subprocess.run(['yt-dlp', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}','-o', f'{output_dir}/stream.%(ext)s'])

  # output twitch stream to twitch_streams/{user}/stream.(%ext)
  # capture stdout: if the message includes "The channel is not currently live", the n
  # ERROR: [twitch:stream] luciid_t: The channel is not currently live
  # Run the command and capture the output


"""
# the message we get if we don't use any special flag and the user if not streaming. we can either check this output or use the flag and see if there's no output?
[twitch:stream] Extracting URL: https://www.twitch.tv/LuciidTW
[twitch:stream] luciidtw: Downloading stream GraphQL
ERROR: [twitch:stream] luciidtw: The channel is not currently live
"""
