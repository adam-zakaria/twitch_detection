# Summary of findings
## varying n frames
every_nth_frame=1
vs
every_nth_frame=60
is about 2x faster not 60x, and that's because most of the cost in decoding is frame traversal not the decode, I think? Regardless, the frame traversal must happen no matter the n.

(twitch-detections-py3.13) ubuntu@ip-172-31-46-149:~/Code/twitch_detections/twitch_detections/test/speed_investigation$ py speed.py 
Running benchmark_process() on /home/ubuntu/Code/twitch_detections/twitch_detections/test/speed_investigation/output_trimmed.mp4
The stream is 30.03 seconds
Grabbing every 1 frame
        Crop took 0.00 seconds
frame.shape[:2]=(200, 200)
template_image.shape[:2]=(18, 23)
        Template match took 18.89 seconds
        no matches found, exiting process()
(twitch-detections-py3.13) ubuntu@ip-172-31-46-149:~/Code/twitch_detections/twitch_detections/test/speed_investigation$ py speed.py 
Running benchmark_process() on /home/ubuntu/Code/twitch_detections/twitch_detections/test/speed_investigation/output_trimmed.mp4
The stream is 30.03 seconds
Grabbing every 60 frame
        Crop took 0.00 seconds
frame.shape[:2]=(200, 200)
template_image.shape[:2]=(18, 23)
        Template match took 8.45 seconds
        no matches found, exiting process()

# gray scale
I don't think gray scale made much of a difference.

# roi
Smaller ROI *DOES* make sense difference, and it's more obvious with higher numbers of frames.

Running benchmark_process() on /home/ubuntu/Code/twitch_detections/twitch_detections/test/speed_investigation/output_trimmed.mp4
The stream is 30.03 seconds
Grabbing every 1 frame
        Crop took 0.00 seconds
frame.shape[:2]=(200, 200)
template_image.shape[:2]=(18, 23)
        Template match took 18.47 seconds
        no matches found, exiting process()
(twitch-detections-py3.13) ubuntu@ip-172-31-46-149:~/Code/twitch_detections/twitch_detections/test/speed_investigation$ py speed.py 
Running benchmark_process() on /home/ubuntu/Code/twitch_detections/twitch_detections/test/speed_investigation/output_trimmed.mp4
The stream is 30.03 seconds
Grabbing every 1 frame
        Crop took 0.00 seconds
frame.shape[:2]=(50, 75)
template_image.shape[:2]=(18, 23)
        Template match took 14.69 seconds
        no matches found, exiting process()

----------------
----------------
----------------
Having such a big ROI is probably unnecessary - could do a check with all the clips that we've already compiled - draw a box around and confirm that they are around the dk. The detection is linear with the ROI so that'd saved a lot of time.

The stream is 30 seconds
        Crop took 0 seconds
frame.shape[:2]=(200, 200)
template_image.shape[:2]=(18, 23)

# grab() improvement
Okay almost 50% improvement
From:
The stream is 30 seconds
        Crop took 0 seconds
        Template match took 14 seconds
To:
The stream is 30 seconds
        Crop took 0 seconds
        Template match took 8 seconds
        no matches found, exiting process()