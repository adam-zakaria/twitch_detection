# Build
From project root
`poetry build`
creates:
dist/twitch_detections-0.1.0-py3-none-any.whl
dist/twitch_detections-0.1.0.tar.gz
# Install
`poetry install` (initiates a venv and installs the package)
or
`pip install -e .` (works from anywhere)

# Run
`source /Users/azakaria/Library/Caches/pypoetry/virtualenvs/twitch-detections-UsLtH0Yo-py3.13/bin/activate`
`pm2 start 'python -u schedule_events.py' --name 'twitch'`

# Add packages to project
poetry add <packages>

# venv
## Create venv
ubuntu@ip-172-31-46-149:~/Code/twitch_detections/twitch_detections$ `poetry env activate`
Creating virtualenv twitch-detections-0p2BiuAg-py3.13 in /home/ubuntu/.cache/pypoetry/virtualenvs
source /home/ubuntu/.cache/pypoetry/virtualenvs/twitch-detections-0p2BiuAg-py3.13/bin/activate
# activate it
ubuntu@ip-172-31-46-149:~/Code/twitch_detections/twitch_detections$ `source /home/ubuntu/.cache/pypoetry/virtualenvs/twitch-detections-0p2BiuAg-py3.13/bin/activate`

# Additional commands
`pm2 flush`
`tail -n 100000 /home/ubuntu/.pm2/logs/twitch-out.log`
3.13.2 is not installed and happy-utils is not installed.
Why?
Also the pm2 logs 0 --lines 100000 behavior is weird. It's not less, so I can't gg to the top, I also can't scroll to the top. And there's just those tons of 'The channel is not currently live'.

So obviously the python version needs to be resolved, but wasn't this already working with the fluff0132 test?

A lot of streams got downloaded. Do we want to just delete the streams?


# Current issue 8/27/25

Okay, so the typical logs not getting output to /home/ubuntu/.pm2/logs/twitch-out.log also it seems a package 

pm2 start 'python pipeline_pieces.py' --name 'twitch_process'

Okay, so something deleted the streams. Keeping the streams around isn't expensive, so maybe we can do that for a bit and manually delete them? 

And what about shorter runs? And also what about this just going a lot faster? 1080p is nothing to scoff at though, But maybe there's a way to do this.

# Current issue:
* ffprobe failed: [mov,mp4,m4a,3gp,3g2,mj2 @ 0xb63cb32e5a40] moov atom not found
output/spartanthedogg/stream/spartanthedogg_08_20_2025_14_43_55.temp.mp4: Invalid data found when processing input


# Current
* Add timestamp to top of log
* Investigate .temp.mp4? 
* Do math on a long run - i.e. if
  The stream is 3601.016667 seconds long
  Template matching each frame
          took 1691.42 seconds
  Will this work for a long run.

* The logging on pm2 is not great - it's not easy to tell separate the current run from previous ones. Cannot get specifically stdout and stderr for specific processes. 

# Output results
* Snakebite compilation did not work, clips did
* manny_hcs, royal2, sparty, clips, compilation, deleted stream
* envor3, barcode all folders created, nothing in them
* tripppey, trunks, hunter_jjx, miniberzerker, stream/<stream>.mp4, nothing else

## Logs Reflections
So for all of the streamers mentioned above the streams were downloaded, so something must have prevented their processing.
Envore - hour long stream nothing detected.

Error during sparty concatenation

barcode 4 hour stream with no matches. 
Envore almost 3 hour with no matches.
Fishy but not much to do...

Concatenating clips snakebite is the last thing that got logged, so it's possible the program froze or something during this concatenation. Could skip concatenation step for now because there isn't enough memory for lots of clips with the current method. Then I'd guess for tripppey, trunks, hunter_jjx, miniberzerker they just didn't get run because of program crash or something.

Okay so what am I think then...Don't do concatentation? Add multi kill support? Put these on s3? 

Yes. Disable concatenation. Remove log ahead of time for easier parsing. Do tee another time. For next run confirm all streams get evaluated - they probably will given concatenation is disabled.


## Logs
Starting downloads at 08_14_2025_16_33_28

output/spartanthedogg/stream/spartanthedogg_08_14_2025_16_33_29.temp.mp4: Invalid data found when processing input

Starting process_streams() on ['output/manny_hcs/stream/manny_hcs_08_14_2025_22_38_30.mp4', 'output/royal2/stream/royal2_0
8_14_2025_22_38_30.mp4', 'output/envor3/stream/envor3_08_14_2025_22_38_30.mp4', 'output/spartanthedogg/stream/spartanthedo
gg_08_14_2025_22_38_30.mp4', 'output/barcode_ak/stream/barcode_ak_08_14_2025_22_38_30.mp4', 'output/snakebite/stream/snake
bite_08_14_2025_22_38_29.mp4', 'output/minib3rzerker/stream/minib3rzerker_08_14_2025_22_38_29.mp4', 'output/Tripppey/strea
m/Tripppey_08_14_2025_22_38_30.mp4']

# To do
* add triple kill, overkill, etc support. would that make it a lot longer...I think? Which would technically be fine...? And also could only check multi kills once a double kill shows up.
* tempted to delete logs from last run - it's hard to parse the logs otherwise - though can look at date. Well....teeing logs to a timestamped file would probably be ideal.

