"""
Pipeline:

detect_dk.py
filter_dk_times.py
extract.py
concat (this file)
"""
"""
get videos ............
get top twitch streamers, or at least choose a few known streamers
on ec2, check if the streams are running every ten minutes; if running, download to halo/streamer/input-video/====

at 8pm, run detections....
run a script which checks time every minute; if greater than 8pm, set running to true (set running to false when done_
twitch
halo/streamer/detection-clips
halo/streamer/concatenated_clips.mp4
overlay in bottom left with streamers name
post to youtube .....

concat ....
get_roi's
"""

# imports
import utils.utils as utils; import subprocess
import cliptu.clip as clip

clip.concat('extracted_dks', "concatenated_files.mp4") # need to redo detection clips to replace non ending .
