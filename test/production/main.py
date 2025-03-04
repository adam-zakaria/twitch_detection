import os
import subprocess
import uuid
import time
import logging
import requests  # new import for making HTTP requests
import utils.utils as utils
import cliptu.s3 as s3
import time
from datetime import datetime, timedelta
logging.getLogger("ppocr").disabled = True

"""
Manually kill processes without PID

ps -aux | grep twitch | awk '{print $2}'
# take first output from above and add to below
kill -9 -

"""

def log(message):
    """
    Prints the message locally and POSTs it to the log endpoint.
    """
    # Print the message to the console
    print(message)
    try:
        # URL for your logging endpoint; adjust port/hostname as needed
        url = "http://localhost:1337/logs"
        # Build the payload JSON
        payload = {"logs": message}
        # POST the message as JSON to the log endpoint
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print("Error posting log:", response.text)
    except Exception as e:
        print("Failed to post log:", e)

def download_twitch_streams(streamers, output_path):
    """
    Open a subprocess for each Twitch streamer, all in a separate process group.

    The behavior of yt-dlp sigint and sigkill handling:
    * on sigint, it will consolidate mp4.part to .mp4 and it will continue to run, 
      but it will not continue to download.
    * sigkill kills the process.
    """
    log("Starting Twitch stream downloads")
    output_path = utils.path(output_path)
    utils.mkdir(output_path)

    group_leader_pid = None
    processes = []

    for streamer in streamers:
        # Setup folder for streamer
        streamer_output_path = output_path / streamer
        utils.mkdir(streamer_output_path)
        log(f"Downloading {streamer}'s stream to {streamer_output_path}...")

        # yt-dlp --wait-for-video 600 -S, 'vcodec:h265,acodec:aac' https://www.twitch.tv/alleesi -o
        
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

    log(f"Subprocesses are in group with leader PID: {group_leader_pid}")
    utils.w(str(group_leader_pid), 'gid.txt')

    log("To kill all download subprocesses (without killing the parent), run:")
    log(f"kill -2 -{group_leader_pid}; sleep 2; kill -9 -{group_leader_pid}")
    return group_leader_pid

import schedule
import time

if __name__ == "__main__":
    log(f'Starting job at {utils.ts()} ################################')
    log(f'Removing twitch_streams from front')
    utils.rm('twitch_streams')
    streamers = [
        'frosty', 'renegade', 'formal', 'Luciid_TW', 'itzthelastshot', 'SpartanTheDogg',
        'SnakeBite', 'aPG', 'Bound', 'kuhlect', 'druk84', 'pzzznguin',
        'cykul', 'Tripppey', 'royal2', 'bubudubu', 'mikwen', 'Ogre2', 'HuNteR_Jjx', 'Alleesi', 'Cruvu', 'gunplexion'
    ]
    download_twitch_streams(streamers, 'twitch_streams')

    def daily_stream_task():
        # At scheduled time, stop the download subprocesses, upload streams, and restart downloaders.
        group_leader_pid = utils.r('gid.txt')
        log(f'Daily task at {utils.ts()} ################################')
        log('* Sleeping *')
        s3.rm('s3://cliptu/twitch_streams')
        log('Removing s3://cliptu/twitch_streams')
        os.system(f'kill -2 -{group_leader_pid}')
        time.sleep(8)
        log('* Waking *')
        os.system(f'kill -9 -{group_leader_pid}')
        input_folder = 'twitch_streams'
        output_folder = 'twitch_streams'
        log(f'Uploading {input_folder} to {output_folder}')
        s3.upload_folder(input_folder, output_folder)
        log(f'Starting gpu')
        os.system('./g4dn_xlarge_stop.sh')
        utils.rm('twitch_streams')
        log('Removed twitch_streams folder.')
        download_twitch_streams(streamers, 'twitch_streams')
        return group_leader_pid

    # Schedule the daily_stream_task to run at specified times.
    #future_time = datetime.now() + timedelta(seconds=1800)
    future_time = datetime.now() + timedelta(seconds=30)
    time_str = future_time.strftime("%H:%M:%S")
    schedule.every().day.at(time_str).do(daily_stream_task)

    # Continuously check for pending scheduled tasks.
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every second for better precision.
