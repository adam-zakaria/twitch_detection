# A useful command to get a sample with a double kill
yt-dlp -S vcodec:h265,acodec:aac "https://www.youtube.com/watch?v=Kl5QHzEwbLQ" --download-sections "*00:25-00:26"

# Annoyances
that it's hard to know the file extension before the download, i.e. the 
streams/486ce962309b4764af98739657be33e1.%(ext)s