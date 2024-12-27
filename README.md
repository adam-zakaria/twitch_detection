# test video
https://www.youtube.com/watch?v=Kl5QHzEwbLQ&t=4s

# Parts

# Ingest twitch
* for each twitch streamer, if online, yt-dlp the stream and save to /videos

# detect multikills
* at 10pm, run detection script on each video in /videos
* output to /multikills/<streamer_name>/<number>.mp4
* rm videos/*
* concat all multikills into a single video
* save to /final_output/multikills.mp4

# detection scripts
* on each video run template matching to detect multikills
* for now, just start with double kills, but in the future, we'd want to mark the first instance of each medal, 
* for double kills

# upload to youtube
* k




# Notes
## Check if twitch stream is live
➜  github_page git:(main) yt-dlp --get-title https://➜  github_page git:(main) yt-dlp --get-title https://SpartanTheDogg (live) 2024-12-23 19:07
➜  github_page git:(dev) ✗ yt-dlp --get-title https:/➜  github_page git:(dev) ✗ yt-dlp --get-title https:/ERROR: [twitch:stream] broward: The channel is not cuERROR: [twitch:stream] broward: The channel is not cu

# What to do
* We discussed what the convolution operation actually is. 
There is a template image that is slid of an image -> an input image which is processed by a convolution operation and which produces a result image. This is done because a convolution is more resistant to 'noise' (lighting, orientation, etc).
* So, what's the issue. We discussed creating simpler test images, I think this is a really good idea.
* I do wonder if the fact that this is a flat image actually creates more issues for a convolution.

* I'm using opencv's template matching to detect some frames in a video game gameplay. Specifically, I'm trying to detect a double kill in Halo. When a double kill happens a 'medal' is put onto the screen - it is a 2-d circle, where most of the rest of the screen is a 3d environment. I worry that the convolution operation actually hurts the detection of the medal - the medal is just a blue circle with gray stars within it - the defining features are the shape and colors, and a circle is such a popular shape