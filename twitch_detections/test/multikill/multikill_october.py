import time

def detect(frame, template_image):
  pass

def detect_video():
  frames = []
  templates = ['/path/to/dk','/path/to/tk','/path/to/ok']
  start_time = time.time()
  in_multi_kill = False
  template_index = 2 # start with double kill

  for frame in frames:
    # If we're in a multikill
    if in_multi_kill and (time.now() - start_time <= 5):
      result = detect(frame, templates[template_index])
      if result:
        template_index += 1
    # If we're not in a multikill
    else:
      # Reset vars in case we are coming out of a multikill
      template_index = 2 
      in_multi_kill = False
      start_time = time.now()

      result = detect(frame, templates[template_index])
      if result:
        template_index += 1
        in_multi_kill = True

if __name__ == '__main__':
  # test cases
  detect_video() # only single kills
  #

  detect_video() # double kill

  detect_video() # triple kill
  pass
