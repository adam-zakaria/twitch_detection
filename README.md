# Install local dependencies
pip install -e /Users/azakaria/Code/utils
pip install -e ~/Code/cliptu/backend/cliptu/

# Get Test video
## (clip)(zsh escaped) 'Lucid - Greatest Hits / Best Clips | Halo Infinite LAN':
yt-dlp -S vcodec:h265,acodec:aac "https://www.youtube.com/watch?v=Kl5QHzEwbLQ" --download-sections "*00:25-00:26"

# Current