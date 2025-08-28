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