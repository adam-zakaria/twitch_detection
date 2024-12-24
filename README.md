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