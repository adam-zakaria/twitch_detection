"""
We are trying to figure out when exactly yt-dlp transitions .mp4.part to .mp4

It seems that it can handle signals and exit / transition gracefully.
"""

# translate python to bash, execute, observe .mp4.part transition

# python 
# https://www.twitch.tv/formal
# subprocess.Popen(['yt-dlp', '--wait-for-video', '600', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}', '-o', f'{streamer_output_path}/{uuid.uuid4().hex}.%(ext)s'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# bash
yt-dlp --wait-for-video 600 -S vcodec:h265,acodec:aac https://www.twitch.tv/formal -o "formal.%(ext)s"

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

# So maybe the stream didn't complete because we ran out of storage? I'm actually sure why we exited. So let's see if the process exits gracefully with a pkill -9 and popen?

