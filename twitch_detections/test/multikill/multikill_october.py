import time
import cv2
import sys
# Add the folder containing cliptu.py to sys.path
sys.path.append("/Users/azakaria/Code/twitch_detections/twitch_detections")
import cliptu


def detect(frame, template_image):
  pass

def detect_video(stream_path):
  templates = [None, None, 'dk.png','tk.png','ok.png']
  start_time = time.time()
  in_multi_kill = False
  template_index = 2 # start with double kill
  detections = []

  for ts, frame in cliptu.crop(input_path = stream_path, x = 710, y = 479, w = 200, h = 200, every_nth_frame = 60):
    # If we're in a multikill
    print(f'in_multi_kill: {in_multi_kill} {templates[template_index]}')
    if in_multi_kill and (time.time() - start_time <= 5):
      #result = detect(frame, templates[template_index])
      result = cv2.matchTemplate(frame, cv2.imread(templates[template_index]), cv2.TM_CCOEFF_NORMED)
      min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
      if max_val >= .8:
        detections.append(result)
        template_index += 1
    # If we're not in a multikill
    else:
      # Reset vars in case we are coming out of a multikill
      template_index = 2 
      in_multi_kill = False
      start_time = time.time()

      #result = detect(frame, templates[template_index])
      result = cv2.matchTemplate(frame, cv2.imread(templates[template_index]), cv2.TM_CCOEFF_NORMED)
      min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
      if max_val >= .8:
        detections.append(result)
        template_index += 1
        in_multi_kill = True

  return detections

if __name__ == '__main__':
  # test cases
  detect_video('/Users/azakaria/Code/twitch_detections/twitch_detections/test/multikill/lucid_killtrocity.webm') # only single kills