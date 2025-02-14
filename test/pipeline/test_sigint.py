import subprocess
import os
import utils.utils as utils

streamer = 'renegade'
proc = subprocess.Popen(
    [
        'yt-dlp',
        '--wait-for-video', '600',
        '-S', 'vcodec:h265,acodec:aac',
        f'https://www.twitch.tv/{streamer}',
        '-o', f'{streamer}.%(ext)s'
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

pgid = os.getpgid(os.getpid())
print(f"kill -2 -{pgid}")
print(f'ps -aux | grep yt-dlp')