import twitch_detections.models.twitch_stream as twitch_stream
import threading
import schedule

"""
twitch_stream = twitch_stream.TwitchStream()
twitch_stream.download_stream(streamer='formal')
"""
streams = []
for streamer in ['KingJay', 'HuNteR_Jjx', 'formal']:
  stream = twitch_stream.TwitchStream(streamer=streamer)
  threading.Thread(target=stream.download_stream, args=('streams',)).start()
  streams.append(stream)

# at 4AM, kill the threads
for stream in streams:
  schedule.every().day.at("04:00").do(stream.kill_threads)

# maybe we don't need to kill the threads...

# get all the streams
# restart the threads

# Run detection (template matching)

# Run filter

# Run concat