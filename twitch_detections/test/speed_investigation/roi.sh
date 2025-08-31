# Trim
mkdir -p "/Users/azakaria/twitch_videos/compilations_trimmed"

for f in "/Users/azakaria/twitch_videos/compilations/"*.mp4; do
  base="$(basename "$f")"
  ffmpeg -y -i "$f" -t 10 -c copy "/Users/azakaria/twitch_videos/compilations_trimmed/$base"
done

# ROI
mkdir -p "/Users/azakaria/twitch_videos/compilations_roi"

for f in "/Users/azakaria/twitch_videos/compilations/"*.mp4; do
  base="$(basename "$f")"
  ffmpeg -y -i "$f" -t 10 \
    -vf "drawbox=x=710:y=479:w=75:h=50:color=green@1.0:t=2" \
    -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 128k \
    "/Users/azakaria/twitch_videos/compilations_roi/$base"
done
