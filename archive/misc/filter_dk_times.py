"""
###########
extract clips from multikill_detection_times.txt
###########

# discard all detections that are within 3s of each other,
i.e 
for line, set multi_kill start
if next line - multi kill start (abs) > 3, multi_kill_starts.append

# get clip 2s before and 6s after (and it'll look better for twitch because no jumps to new map)
for i,start in enumerate multi
  ffmpeg extract start-2,  start+6, output=dk_detections/{i}.ext
"""
import utils.utils as utils; from itertools import pairwise

# get all multikill detections separated by 3+ seconds 
mk_ss = [a for a,b in pairwise(map(float, utils.rl('dk_detections.txt'))) if (b - a) > 3]
# print(mk_ss)

import cliptu.clip as clip
utils.rm_mkdir('extracted_dks')
for s in mk_ss:
  clip.extract_clip('4m_dk.mp4', f'extracted_dks/{s}.mp4', s-8,s+1)


