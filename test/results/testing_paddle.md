input_video_path = 'test/videos/1m_dk.mp4'
use_angle_cls=True
Time to run: 29.627334594726562

use_angle_cls=False
Time to run: 26.225985288619995

import logging
logging.getLogger("ppocr").disabled = True
Time to run: 25.797281742095947

removing prints
Time to run: 26.05010986328125
Not sure why it's a second slower...

grayscaling
Time to run: 24.8878436088562

downscaling the resolution hurt the detctions so we can't...so we're really not improving much. We could try skipping more frames...

actually no the gray scale actually does seem to miss detections too...


Surprisingly even mod 20 works great...

file '../extract/24_53.mp4'
file '../extract/32_67.mp4'
file '../extract/42_27.mp4'
file '../extract/50_13.mp4'

file '../extract/24_67.mp4'
file '../extract/32_67.mp4'
file '../extract/42_33.mp4'
file '../extract/50_33.mp4'

so it is twice as fast...
Time to run: 16.406522750854492
So we'll use this for now :)

ffmpeg -y -loglevel error -ss 222.33 -i test/videos/4m_dk.mp4 -to 9.0 -c copy output/extract/230_33.mp4
----------------------------------
Clips saved in output/extract.
Time to run: 61.61014413833618

1m processing time for 4m
So 100 hours would be...25 hours. Which is expensive.
$13
i have 2k?
which would be 158 days.

spot can be a lot cheaper...
20% would be....2.60. Which is not much at all...But 100 hours is a lot anyways. We could just try not much to start.

Reframe takes as much time as OCR...crazy.
Reframe time 2.847243070602417
OCR time 2.857661008834839
