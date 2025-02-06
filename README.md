# Install local dependencies
pip install -e ~/Code/utils
pip install -e ~/Code/cliptu/backend/cliptu/

# Run
`python main.py < detect | filter | concat >'`

# Unintegrated code
* test/upload.py has twitch_streams upload code.
* branch batch_reframe:main_tesseract.py has pipeline code, meaning, in main.py it includes partially implemented download stream and timing code.

# Get Test video
## (clip)(zsh escaped) 'Lucid - Greatest Hits / Best Clips | Halo Infinite LAN':
yt-dlp -S vcodec:h265,acodec:aac "https://www.youtube.com/watch?v=Kl5QHzEwbLQ" --download-sections "*00:25-00:26"

# Current

2/5/25 630PM, signing off
* Run debug_pipeline.py
Understand why the output/{ts} folder is created but not detect, probably something with Path
> /home/ubuntu/Code/twitch_detection/test/debug_pipeline.py(91)detect_timestamps()
     90     breakpoint()
---> 91     utils.w(timestamps_lines, utils.opj(output_folder, 'dk_detections.txt'))
     92     utils.jd(detections_log, utils.opj(output_folder, 'text_detections.json'))

ipdb> output_folder
PosixPath('output/02_05_2025_23_29_32/detect')


Traceback (most recent call last):
  File "/home/ubuntu/Code/twitch_detection/test/debug_pipeline.py", line 112, in <module>
    roi = (529, 441, 266, 131)  # (x, y, width, height)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/Code/twitch_detection/test/debug_pipeline.py", line 91, in detect_timestamps
    #print(f'output_folder: {output_folder}')
  File "/home/ubuntu/Code/utils/utils/utils.py", line 332, in w
    with open(fp, 'w') as f:
         ^^^^^^^^^^^^^

okay so detect is not getting made...


Earlier:
* Get a pro twitch stream that definitely has double kills. Though...Bound's stream definitely had a double kill. So let's investigate why that one didn't work? That'd be on GPU. Maybe GPU has unmerged code.
* Processing every 20th frame could be an issue

* Part of what we're wondering is are we capturing all of the information that we need to capture to do post morterm? I'm tempted to capture the results objects and write them - worst case we can work from the results to a more distilled representation.

Looking at confidence scores and bounding boxes is another option.

Yeah im trying to decide if I want to split these into simpler functions or have a single one... if it is provided no timestamps, and no frame rate...welll....cv2 can automatically pull the fps...but I kind of like just getting the frames and not expecting to get the fps as well. It's 

I just really don't want a tangle of code, so I'm investing early. It's slower moving now but we don't know what's going to happen. And it could make development faster eventually.

with get_frames, there are times where we just want the frames, we don't need the timestamps, maybe we can have simple=True (just return frames)

if timestamps=True
return timestamps

I guess we could do this ad nauseum, more flags to return more info.

get_frames

I'm lost. Yeah...capturing our highest level and most direct context are pretty important...maintaining context, that basically is the task. And no matter what it's complex. It can be avoided. But having alternate representations and making sane decisions along the way and having friends etc is how to manage it.
