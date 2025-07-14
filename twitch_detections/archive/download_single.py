import subprocess
import os
import uuid

# 7/8/2025
streamers = ['mean3st', 'Walmahrt', 'ubernick' ]

if __name__ == "__main__":
  for streamer in streamers:
    cmd = [
        'yt-dlp', '--cookies', 'cookies.txt', '--wait-for-video', '600', '-S', f'vcodec:h265,acodec:aac',
        f'https://www.twitch.tv/{streamer}']

    p = subprocess.Popen(cmd, preexec_fn=lambda: os.setpgid(0, 0),
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Download all the streams