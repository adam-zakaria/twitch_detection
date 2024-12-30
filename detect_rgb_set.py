import cv2
def detect_rgb_set(template_image, input_image):
  print(f"template_image: {template_image}")
  print(f"input_image: {input_image}")
  # read in double_kill_medal.png (template image)
  # bgr
  template_image = cv2.imread(template_image)
  # create rgb set
  template_bgr_set = set()
  for row in template_image:
      for pixel in row:
          template_bgr_set.add(tuple(map(int, pixel)))  # Convert numpy values to regular integers before creating tuple

  input_image = cv2.imread(input_image)
  input_bgr_set = set()
  for row in input_image:
      for pixel in row:
          input_bgr_set.add(tuple(map(int, pixel)))  # Convert numpy values to regular integers before creating tuple

  # Calculate overlap
  # this would make sense if there are a lot more colors contained in the non-medal portion despite being a smaller area
  intersection = template_bgr_set.intersection(input_bgr_set)
  percentage_covered = (len(intersection) / len(template_bgr_set)) * 100
  print("len(intersection): ", len(intersection))
  print("len(template_bgr_set): ", len(template_bgr_set))
  print("len(input_bgr_set): ", len(input_bgr_set))
  print(f"percentage_covered: {percentage_covered:.2f}%")
  print("--------------------------------")

detect_rgb_set("double_kill_medal.png", "double_kill_medal.png") # 42%
detect_rgb_set("double_kill_medal.png", "double_kill_medal_with_bg.png") # 42%
detect_rgb_set("double_kill_medal.png", "blue_map_piece.png") # 0%
detect_rgb_set("double_kill_medal.png", "medal_large_column.png") # 0%