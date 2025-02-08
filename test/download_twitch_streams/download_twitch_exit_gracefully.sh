"""
We are trying to figure out when exactly yt-dlp transitions .mp4.part to .mp4

It seems that it can handle signals and exit / transition gracefully.
"""

# Manually get pgid
# ps -o pid,pgid,comm -p 7157 # replace 7157 with PID
# -> 2172 # gid
# kill -2 -2172 # kill

# translate python to bash, execute, observe .mp4.part transition

# python 
# https://www.twitch.tv/formal
# subprocess.Popen(['yt-dlp', '--wait-for-video', '600', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}', '-o', f'{streamer_output_path}/{uuid.uuid4().hex}.%(ext)s'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# bash
yt-dlp --wait-for-video 600 -S vcodec:h265,acodec:aac https://www.twitch.tv/renegade -o "renegade.%(ext)s"

# If this receives a ctrl-c it will takes the .mp4.part and make it into .mp4
# See below "[FixupM3u8] Fixing MPEG-TS in MP4 container of formal.mp4"

"""
frame= 1078 fps= 72 q=-1.0 Lsize=   14061kB time=00:00:17.97 bitrate=6406.4kbits/s speed= 1.2x    
video:13170kB audio:383kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 3.743312%
Exiting normally, received signal 2.
[ffmpeg] Interrupted by user
[download] 100% of   13.73MiB in 00:00:16 at 853.39KiB/s
[FixupM3u8] Fixing MPEG-TS in MP4 container of "formal.mp4"
"""
# If it gets a kill -2 it consolidates and exits

# So maybe the stream didn't complete because we ran out of storage? I'm actually sure why we exited. So let's see if the process exits gracefully with a pkill -9 and popen?

# Okay so we're pretty sure the subprocess does not exit on kill -2 like the cli execution does. 
# Let's confirm one more time, then we can do a -2 to consolidate and -9 to shutdown, assuming the gid is the same.

# OKAY, so it seems killing the group id printed actually DOES allow the children to clean up, i.e.
# python /home/ubuntu/Code/twitch_detection/test/download_twitch_streams/download_upload_twitch_streams.py
# kill -2 -17144
# and /home/ubuntu/Code/twitch_detection/test/download_twitch_streams/twitch_streams/renegade/48286e3cbe7a46229516320b80f64ebc.mp4 gets consolidated within... a minute? maybe longer.
# To confirm no longer running:
# ps -aux | grep yt-dlp 

# So NEXT, let's try with ALL the streams (at least, more than 1)
# It worked

# okay so what now...
# download the streams? an issue is that I think...well...Maybe Ill start it tomorrow? We said we'd download during the time range? Maybe that'll work?


# hmmmm it seems like the -2 does not work with waiting streams (i.e. the streamer is offline). I guess that's fine because we want them waiting. And we can still kill them with -9

"""
Next, let's write out a big diagram with the plan.

Immediately, we still need to test double kill detection on twitch streams. So maybe get a few hours? 

Okay and actually...don't do this on the GPU...
"""