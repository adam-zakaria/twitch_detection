import os
import subprocess
import uuid
import signal
import utils.utils as utils

"""
# process management
We do this semi-automatically: the script prints the group id of the parent and it's subprocesses (the same by default). From there, we can kill the group manually. Honestly I'm not sure the best way to do this because we're going to start the script then leave. So we could write it to a file, and we have another script called kill group which will kill the process group, reading the file. 

Yeah so longer term we'll figure something out. For now, we just 

# Additional information about managing the processes.

By default subprocess.popen will spawn them under the same group id as the parent.
So you can find one pid, get the group id, then kill the group

$ ps -o pid,pgid,comm -p 3275
    PID    PGID COMMAND
   3275    3139 ffmpeg
$ kill -9 -3139
"""

def download_twitch_streams(streamers, output_path):
    """
    Open a subprocess for each Twitch streamer asynchronously. 
    The subprocesses will exit when the parent exits because they share the parent's process group.
    """
    print("Starting Twitch stream downloads")
    downloaded_streams = []
    procs = []  # to store process objects
    output_path = utils.path(output_path)

    for streamer in streamers:
        # Create output directories
        utils.mkdir(output_path)
        streamer_output_path = output_path / streamer
        utils.mkdir(streamer_output_path)
        print(f"Waiting for and downloading {streamer}'s stream to {streamer_output_path}...")

        # No preexec_fn here so the child inherits the parent's process group.
        proc = subprocess.Popen(
            [
                'yt-dlp',
                '--wait-for-video', '600',
                '-S', 'vcodec:h265,acodec:aac',
                f'https://www.twitch.tv/{streamer}',
                '-o', f'{streamer_output_path}/{uuid.uuid4().hex}.%(ext)s'
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        procs.append(proc)

    return procs, downloaded_streams

if __name__ == "__main__":
    # Define the streamers and output folder
    streamers = ['Luciid_TW', 'itzthelastshot', 'SpartanTheDogg', 'SnakeBite',
                 'aPG', 'Bound', 'kuhlect', 'druk84', 'pzzznguin']
    download_twitch_streams(streamers, 'twitch_streams')

    # Get and print the parent's process group id.
    pgid = os.getpgid(os.getpid())
    print(f"Parent process PGID: {pgid}")

    # Provide the CLI command to kill the entire process group.
    print(f"To kill the entire process group from the CLI, run:")
    print(f"kill -9 -{pgid}")