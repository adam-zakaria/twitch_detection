import utils.utils as utils

for streamer_path in utils.ls('twitch_streams'):
    streamer = streamer_path.split('/')[1]
    input_video_paths = [p for p in utils.ls(streamer_path) if p.count('.') == 1]  # filter .mp4s, avoiding .temp.mp4 and .mp4.part
    # Even with sigint the mp4 gets consolidated, but a .temp.mp4 may be left still
  
    print(input_video_paths)