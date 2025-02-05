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
* Get a pro twitch stream that definitely has double kills. Though...Bound's stream definitely had a double kill. So let's investigate why that one didn't work? That'd be on GPU. Maybe GPU has unmerged code.
* Processing every 20th frame could be an issue

* Part of what we're wondering is are we capturing all of the information that we need to capture to do post morterm? I'm tempted to capture the results objects and write them - worst case we can work from the results to a more distilled representation.

But actually results don't even include timestamps...Which makes sense - it's just given frames.
