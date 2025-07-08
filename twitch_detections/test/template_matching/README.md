Running template_matching_folder.py on train/double_kill, there is no where that 5 adjacent frames do not have at least a .8 - that is, each clip with a double kill has at least one frame that is correctly identified.

But the false positives are an issue :)
0.8239 for a frame which is not even a medal (just background)...
Image path: /Users/azakaria/Code/twitch_detections/test/frames/data/train/no_double_kill/frame_000540.png
Confidence score: 0.8239

# Investigate templateMatch implementation
It is not straightforward to understand.
https://github.com/search?q=repo%3Aopencv%2Fopencv+matchTemplate&type=code