# Looking at compilations
## General thoughts
Watching the penguin dks with no comms makes me think dks are often not enough dope (with no comms, limited outplay). Might want to do triples and up and then extended highlights (thought it's not clear how many triples there'd be. But even a couple minutes could be good. Some of these dk's are 5 minutes each, all streamers compilation would be too long.

there are some people who have clips/, compilation/, streams/ empty which suggests processing unveiled no dks and then the stream got deleted on cleanup. let's review logs and confirm.

Improve logging - be able to view all the commands run. Add clock times? Make it easier to tell what exactly is happening right now (what's running for which stream?). Learn what's taking so long. Learn why there is a .temp.mp4 and what it contains.

bound_double_kills_7_24_25.mp4 there are instances of the initial or final frame freezing for a second. One repeat clip. The clips are mostly maybe 1 second too long. The individuals clips in clips/ have slightly desynced tracks, though chat can explain it.

formal_07_24_2025_22_42_28.mp4 (local) there are a few consecutive clips where the clip starts at the end of the dk, not clear why.

# Killing processes waiting for offline downloads
## Investigating the underlying wait in ytdlp
Given the following output from ytdlp
WARNING: [twitch:stream] gamesager: The channel is not currently live
[wait] Waiting for 00:10:00 - Press Ctrl+C to try now

In yt-dlp codebase I did cmd+f for "Waiting for"

And found the wait is a sleep()
line 1709                time.sleep(1)
/Users/azakaria/Library/Caches/pypoetry/virtualenvs/twitch-detections-UsLtH0Yo-py3.12/lib/python3.12/site-packages/yt_dlp/YoutubeDL.py

## Killing
Just doing 

def kill_downloads(proc):
    os.killpg(proc.pid, signal.SIGKILL)
Was not working, but 
schedule.every(20).seconds.do(kill_downloads, procs)
Was working. And so I tried adding a lot kill calls:
def kill_downloads(proc):
    os.killpg(proc.pid, signal.SIGKILL)
    os.killpg(proc.pid, signal.SIGKILL)
    os.killpg(proc.pid, signal.SIGKILL)
but that did not work.
But the following works, and yeah an exception gets called but that's fine and no zombies to speak of, at least visibly, and LLMs -1 for their advice on this one. This seems like a great solution for my use case.
def kill_downloads(procs):
  # Kill processes
  print('Kill processes')
  for proc in procs:
    while proc.poll() is None:
        os.killpg(proc.pid, signal.SIGKILL)



# Sub
Running multiple processes in python is way less ergonomic than I'd expect, tt might partially be because this is a complex use case. 

Doing:
```
proc = subprocess('ytdlp)
proc.kill()
```
Actually doesn't work - it terminates to the terminal but then the download just takes the terminal back over, possibly because
yt-dlp calls ffmpeg (subprocesses calling subprocesses). 

The threading and multiprocess and pool options are surprisingly complex for something so seemingly simple. Maybe LLMs just aren't great at this yet, but I'd advise reading the docs and example code (invest time to understand it deeply given how useful it is).

Also, there is already a way to download multiple videos at once: Just pass the urls in :) Though it is single core.
https://github.com/yt-dlp/yt-dlp/issues/1918

And there is a wrapper that uses multiprocessing to download multiple at once.
https://github.com/targetdisk/squid-dl

# Speed
Reframing is slow.

(twitch-detections-py3.12) ➜  twitch_detections git:(rewrite) ✗ py pipeline.py
Reframing video to an ROI
Reframing video to an ROI took 23.942778825759888 seconds
Template matching each frame
Successfully removed the folder: ./template_match
Threshold: 0.8
Template match found at 135.9994963895575 with confidence 0.8849
Template match found at 136.99949268653953 with confidence 0.8875
Template match found at 137.9994889835216 with confidence 0.90

# What is .mp4.part
Not sure, but VLC can play it and ffprobe can introspect it. So the wrinkle it introduces into the program is probably just how the filename is read.

ffprobe -v error -print_format json -show_format -show_streams TchiKK.mp4.part

This shows information that can be used to check that the streams are correct.

# Medals
It seems like 3-4 medals is the max that can be displayed at once. This could be tested by killing a lot of bots with rockets.

It's displayed on a vertical column.