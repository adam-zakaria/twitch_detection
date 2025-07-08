import subprocess, signal, time, os
import twitch_detections.models.twitch_stream as twitch_stream
import threading
import schedule
from multiprocessing import Process

streamers = ['mean3st', 'Walmahrt', 'ubernick' ]
def main():
  processes = []
  for streamer in streamers:
    stream = twitch_stream.TwitchStream(streamer=streamer)
    p = stream.download_stream('streams')
    processes.append(p)

  # time.sleep(10)

  # for p in processes:
  #   p.terminate()
  #   p.join()

if __name__ == "__main__":
  main()