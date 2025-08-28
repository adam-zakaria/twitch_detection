import subprocess, signal, time, os
import twitch_detections.models.twitch_stream as twitch_stream
import threading
import schedule
from multiprocessing import Process

streamer = 'formal'
output_file_path = './output.mp4'
proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", '-q', "--wait-for-video", "600", "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}", '-o', output_file_path ], preexec_fn=os.setsid)