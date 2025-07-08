import twitch_detections.models.twitch_stream as twitch_stream
import threading
import schedule

"""
twitch_stream = twitch_stream.TwitchStream()
twitch_stream.download_stream(streamer='formal')
"""
for streamer in ['KingJay', 'HuNteR_Jjx', 'formal']:
  ts = twitch_stream.TwitchStream(streamer=streamer)
  threading.Thread(target=ts.download_stream, args=('streams',)).start()

# at 4AM, kill the threads
schedule.every().day.at("04:00").do(ts.kill_threads)

# get all the streams
# restart the threads

# Run detection (template matching)

# Run filter

# Run concat