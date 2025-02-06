import os; import utils.utils as utils; from itertools import pairwise; import subprocess; import cliptu.clip as clip; import cliptu.ffprobe as ffprobe; import sys; import time; import logging; logging.getLogger("ppocr").disabled = True; import uuid

def download_twitch_streams(streamers, output_path):
    """
    Open a subprocess for each twitch streamer, async. Subprocesses will exit when parent exits

    Does not upload, need separate code.
    """
    print("Starting Twitch stream downloads"); downloaded_streams = []
    output_path = utils.path(output_path)

    for streamer in streamers:
        # init folders
        #utils.mkdir(output_path); streamer_output_path = os.path.join(output_path, streamer); os.makedirs(streamer_output_path, exist_ok=True); print(f"Waiting for and downloading {streamer}'s stream to {streamer_output_path}...")
        utils.mkdir(output_path); streamer_output_path = output_path / streamer; utils.mkdir(streamer_output_path); print(f"Waiting for and downloading {streamer}'s stream to {streamer_output_path}...")
        subprocess.Popen(['yt-dlp', '--wait-for-video', '600', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}', '-o', f'{streamer_output_path}/{uuid.uuid4().hex}.%(ext)s'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # processes_have_not_run = False
    return downloaded_streams

if __name__ == "__main__":

  streamers = ['Luciid_TW', 'itzthelastshot', 'SpartanTheDogg', 'SnakeBite', 'aPG', 'Bound']
  download_twitch_streams(streamers, 'twitch_streams')
  #s3.upload_folder('test_upload_folder', 'twitch')
  #s3.download_folder('s3://cliptu/twitch', 'test_download_folder')
