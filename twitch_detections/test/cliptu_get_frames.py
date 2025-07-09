import cliptu.utils as cliptu

for ts,frame in cliptu.get_frames('/Users/azakaria/Code/twitch_detections/twitch_detections/videos/aqua_no_dks.mov', yield_timestamps=True):
  print(ts)