# Check length
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 your_video_file.mp4

38 minutes
ubuntu@ip-172-31-46-149:~/Code/twitch_detection/twitch_detections$ ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 'Luciid_TW (live) 2025-07-08 18_04 [323997590012].mp4'

2287.279410
~ 38 minutes


ubuntu@ip-172-31-46-149:~/Code/twitch_detection/twitch_detections$ ffprobe -v error -show_entries fo
rmat=duration -of default=noprint_wrappers=1:nokey
=1 'UberNick (live) 2025-07-08 18_04 [322863740921].mp4' 
7373.136009

~2 hours


ubuntu@ip-172-31-46-149:~/Code/twitch_detection/twitch_detections$ ^C
ubuntu@ip-172-31-46-149:~/Code/twitch_detection/twitch_detections$ ffprobe -v error -show_entries fo
rmat=duration -of default=noprint_wrappers=1:nokey
=1 'Walmahrt (live) 2025-07-08 18_04 [328382344317].mp4' 
5187.160604

~1 hour 26 min