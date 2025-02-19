from PIL import Image; import os; import cv2; import utils.utils as utils; from itertools import pairwise; import subprocess; import cliptu.clip as clip; import cliptu.ffprobe as ffprobe; import sys; import time; import logging; logging.getLogger("ppocr").disabled = True; import uuid; import cliptu.s3 as s3

def download_twitch_streams(streamers, output_path):
    """
    Open a subprocess for each twitch streamer, async. Subprocesses will exit when parent exits

    Does not upload, need separate code.
    """
    print("Starting Twitch stream downloads"); downloaded_streams = []
    output_path = utils.path(output_path)

    for streamer in streamers:
        # init folders
        utils.mkdir(output_path); streamer_output_path = output_path / streamer; utils.mkdir(streamer_output_path); print(f"Waiting for and downloading {streamer}'s stream to {streamer_output_path}...")
        subprocess.Popen(['yt-dlp', '--wait-for-video', '600', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}', '-o', f'{streamer_output_path}/{uuid.uuid4().hex}.%(ext)s'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # processes_have_not_run = False

    pgid = os.getpgid(os.getpid())
    print(f"Parent process PGID: {pgid}")
    utils.w(str(pgid), 'gid.txt')

    print(f"To kill the entire process group from the CLI, run:")
    # # ctrl+c (SIGINT)
    print(f"kill -2 -{pgid}; kill -9 -{pgid}")
    return pgid

"""
Production twitch downlader and double kill compiler.

Ensure no downloaders are already running (check with ps -aux)
"""

if __name__ == "__main__":
  while True:
    # 4AM in prod; kill the downloaders, upload streams, start downloaders
    ran=False
    if utils.between(utils.now(), utils.now(4)) and (not ran):
      print('between')
    else:
      print('not between')
    time.sleep(60)
    print('Sleeping for 60s')


