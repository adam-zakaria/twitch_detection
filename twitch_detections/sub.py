import subprocess, signal, time, os
import twitch_detections.models.twitch_stream as twitch_stream
import threading
import schedule
from multiprocessing import Process

def main():
  processes = []
  for streamer in ['Pzzznguin', 'spartanthedogg']:
    stream = twitch_stream.TwitchStream(streamer=streamer)
    p = Process(target=stream.download_stream, args=('streams',))
    processes.append(p)
    p.start()

  time.sleep(10)

  for p in processes:
    p.terminate()

if __name__ == "__main__":
  main()