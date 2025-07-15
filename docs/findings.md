# Output of faulty concat
[fc#0 @ 0x137632de0] Stream specifier ':v:0' in filtergraph description [0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa] matches no streams.
Error binding filtergraph inputs/outputs: Invalid argument
Traceback (most recent call last):
  File "/Users/azakaria/Code/twitch_detections/twitch_detections/pipeline.py", line 38, in <module>
    clip.concat(paths)
  File "/Users/azakaria/Code/cliptu/backend/cliptu/cliptu/clip.py", line 42, in concat
    subprocess.run(ffmpeg_cmd, check=True)
  File "/Users/azakaria/.pyenv/versions/3.12.2/lib/python3.12/subprocess.py", line 571, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['ffmpeg', '-y', '-hide_banner', '-i', '135.9994963895575.mp4', '-i', '137.9994889835216.mp4', '-filter_complex', '[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa]', '-map', '[outv]', '-map', '[outa]', 'output.mp4']' returned non-zero exit status 234.


ffmpeg -y -hide_banner -i 135.9994963895575.mp4 -i 137.9994889835216.mp4 -filter_complex [0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa] -map [outv] -map [outa] output.mp4

ffmpeg -y -hide_banner -i 10.0.mp4 -i 30.0.mp4 -i 50.0.mp4 -filter_complex [0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa] -map [outv] -map [outa] output.mp4

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