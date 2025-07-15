# Speed
Reframing is slow.

(twitch-detections-py3.12) ➜  twitch_detections git:(rewrite) ✗ py pipeline.py
Reframing video to an ROI
Reframing video to an ROI took 23.942778825759888 seconds
Template matching each frame
Successfully removed the folder: ./template_match
Threshold: 0.8
Template match found at 135.9994963895575 with confidence 0.8849
Template match found at 136.99949268653953 with confidence 0.8875
Template match found at 137.9994889835216 with confidence 0.90

# What is .mp4.part
Not sure, but VLC can play it and ffprobe can introspect it. So the wrinkle it introduces into the program is probably just how the filename is read.

ffprobe -v error -print_format json -show_format -show_streams TchiKK.mp4.part

This shows information that can be used to check that the streams are correct.

# Medals
It seems like 3-4 medals is the max that can be displayed at once. This could be tested by killing a lot of bots with rockets.

It's displayed on a vertical column.