import subprocess
import os
import uuid

if __name__ == "__main__":
  for streamer in ['TchiKK', 'YNOT_B_CASTING']:
    cmd = [
        'yt-dlp', '--cookies', 'cookies.txt', '--wait-for-video', '600', '-S', f'vcodec:h265,acodec:aac',
        f'https://www.twitch.tv/{streamer}']

    p = subprocess.Popen(cmd, preexec_fn=lambda: os.setpgid(0, 0),
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
