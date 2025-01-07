"""
# discard all detections that are within 3s of each other,
i.e 
for line, set multi_kill start
if next line - multi kill start (abs) > 3, multi_kill_starts.append

# get clip 2s before and 6s after (and it'll look better for twitch because no jumps to new map)
for i,start in enumerate multi
  ffmpeg extract start-2,  start+6, output=dk_detections/{i}.ext

for line in detections.txt

