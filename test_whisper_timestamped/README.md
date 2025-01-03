# Conclusion
'double kill' can detected on a 'clean gameplay', i.e. the 13s clip. In practice, streamers seem to mix their voice to be louder than the game audio which is still louder than 'double kill' (very soft). HCS gameplay is even worse. This plus additional complications make visual detection seem like a better candidate.

# Install
pi whisper_timestamped

# Download audio
## 13s clip
yt-dlp https://www.youtube.com/watch\?v\=hESiNIHGgE8 --extract-audio -o 'test_audio/short.%(ext)s'

## best of lucid compilation
yt-dlp <url>l  --extract-audio -o 'test_audio/short.%(ext)s' 

# Run
whisper_timestamped test_audio/short.opus --model medium --output_dir test_transcriptions/short/medium/short.opus.words.json

# View Results

# Results
* medium is the smallest model that does a detection on small.mp3
* preprocessing the audio might help performance. splitting into smaller segments might help to, or tuning the hyper parameters. It's odd that it detects double kill as part of 'there at charlie' when it was a few seconds after - it's as if the model is optimized for conversation, not disjointed speech'. It might be considering it noise / background, so changing the levels could be good.

