import twitch_detections.models.twitch_stream as twitch_stream
import threading


"""
twitch_stream = twitch_stream.TwitchStream()
twitch_stream.download_stream(streamer='formal')
"""
for streamer in ['KingJay', 'HuNteR_Jjx', 'formal']:
  ts = twitch_stream.TwitchStream(streamer=streamer)
  threading.Thread(target=ts.download_stream, args=('streams',)).start()


# Run detection

# Run filter

# Run concat