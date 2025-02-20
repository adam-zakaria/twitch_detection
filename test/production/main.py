import os
import subprocess
import uuid
import time
import logging
import utils.utils as utils
import cliptu.s3 as s3

logging.getLogger("ppocr").disabled = True

def download_twitch_streams(streamers, output_path):
    """
    Open a subprocess for each Twitch streamer, all in a separate process group.

    The behavior of yt-dlp sigint and sigkill handling:
    * on sigint, it will consolidate mp4.part to .mp4 and it will continue to run, but it will not continue to download (it seems to do nothing).
    * sigkill kills the process
    """
    print("Starting Twitch stream downloads")
    output_path = utils.path(output_path)
    utils.mkdir(output_path)

    group_leader_pid = None
    processes = []

    for streamer in streamers:
        # Setup folder for streamer
        streamer_output_path = output_path / streamer
        utils.mkdir(streamer_output_path)
        print(f"Downloading {streamer}'s stream to {streamer_output_path}...")

        cmd = [
            'yt-dlp', '--wait-for-video', '600', '-S', 'vcodec:h265,acodec:aac',
            f'https://www.twitch.tv/{streamer}', '-o',
            f'{streamer_output_path}/{uuid.uuid4().hex}.%(ext)s'
        ]

        if group_leader_pid is None:
          # For the first subprocess, create a new process group.
          p = subprocess.Popen(cmd, preexec_fn=lambda: os.setpgid(0, 0),
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
          group_leader_pid = p.pid
        else:
            # For subsequent processes, assign them to the existing process group.
            def set_group():
                os.setpgid(0, group_leader_pid)
            p = subprocess.Popen(cmd, preexec_fn=set_group,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        processes.append(p)

    print(f"Subprocesses are in group with leader PID: {group_leader_pid}")
    utils.w(str(group_leader_pid), 'gid.txt')

    print("To kill all download subprocesses (without killing the parent), run:")
    print(f"kill -2 -{group_leader_pid}; sleep 2; kill -9 -{group_leader_pid}")
    return group_leader_pid

import schedule
import time
import os
# Import your utility modules and functions as needed
# from your_module import utils, download_twitch_streams, s3

if __name__ == "__main__":
    streamers = ['renegade', 'formal', 'Luciid_TW', 'itzthelastshot', 'SpartanTheDogg',
                 'SnakeBite', 'aPG', 'Bound', 'kuhlect', 'druk84', 'pzzznguin',
                 'cykul', 'Tripppey', 'royal2', 'bubudubu', 'mikwen', 'Ogre2']
    download_twitch_streams(streamers, 'twitch_streams')

    def daily_stream_task():
        # At 4AM, signal the subprocesses to stop, upload streams, and restart downloaders.
        group_leader_pid = utils.r('gid.txt')
        utils.pr('yellow', 'daily task!')
        print('* Sleeping *')
        os.system(f'kill -2 -{group_leader_pid}')
        time.sleep(4)
        print('* Waking *')
        os.system(f'kill -9 -{group_leader_pid}')
        s3.upload_folder('twitch_streams', 'twitch_streams')
        os.system('rm -rf twitch_streams')
        print('Removed twitch_streams folder.')
        download_twitch_streams(streamers, 'twitch_streams')
        return group_leader_pid

    # Schedule the daily_task to run at 4:00 AM every day.
    schedule.every().day.at("00:19").do(daily_stream_task)
    schedule.every().day.at("00:22").do(daily_stream_task)
    schedule.every().day.at("00:25").do(daily_stream_task)

    # Continuously check for pending scheduled tasks.
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every second for better precision.
