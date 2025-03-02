# Concat does not work
Concat works with this cmd:
  cmd = [
      "ffmpeg", "-y", "-hide_banner", "-f", "concat", 
      "-safe", "0", "-i", f"{output_folder}/concat_files.txt", 
      f"{output_folder}/output.mp4"
  ]
But weirdly, it works with 4.4.2, but not 7.1. It does have that weird freeze between clips but not a big deal.

Hmmmm maybe it doesn't work...but it seems like clip extraction is not working correctly...

ffmpeg -y -loglevel error -ss 230.56666666666666 -i /home/ubuntu/Code/twitch_detection/test/download_twitch_streams/twitch_streams/formal/20cd578ba8fd43d4bd09e6c539c80c55.mp4 -to 9.0 -c copy output/formal/02_11_2025_19_23_23/extract/238_56666666666666.mp4

# Trying clip.concatenate_clips
This is all with streams concat clips (not just individual clips)

I thought this was promising initially because it seemed like out of Royal2, Bound, Formal, and Trippey, Formal's clips were the problematic ones. It almost seems like the last clip is typically the problematic one. Which makes me wonder if I only do 3 instead of 4, will the 3rd become problematic. Regardless, this method does not result in a pristine concat. I need to reorganize the tests. Let's try 3 clips to see.

Okay so bound, formal, royal2 works. i'm trying to understand at what point this breaks. Let's try different combos.

Bound, trippey - Trippy is broken.

trippy_concat.mp4 alone works, so it seems like there's some kind of compatibility issue with Trippy, which is weird because it was formal at first.

Trippy, formall

# Extract clip
Extract clip breaks because of the seek times are not on key frames. Reencoding makes this much better, though the video still freezes for 1s

## Addressing the video freezing
The issue is likely that fast seeking (using -ss before -i) jumps to the nearest keyframe, which may occur before your exact start time. When you re-encode, the decoder starts with an incomplete GOP (Group of Pictures), so the first few frames may not decode properly—resulting in a frozen video until the full GOP is available.

Since you can’t afford to decode from the beginning of a 3‑hour video, here are some workarounds:

Two-Step Process:

Step 1: Quickly extract a slightly longer segment using -ss before -i (fast seeking) so that you get close to your desired start time.
Step 2: Then, on the much shorter extracted clip (say 10–15 seconds), perform a frame-accurate trim by placing -ss after -i (which decodes only a few seconds).
This lets you get the correct cut without processing the entire 3‑hour file accurately.

Accept a Minor Glitch:
If the freeze is only about one second and acceptable for your use case, you might choose to live with it. However, if that’s not acceptable, the two-step approach is recommended.

Additional Filtering:
Another option is to use filters (like the trim filter) on the short segment, but again, this generally works best on a shorter clip rather than re-encoding a 3‑hour file frame-accurately.

In summary, the freeze is due to the boundaries imposed by keyframes when using fast seeking. A two-step process—fast extraction followed by a precise trim on the shorter clip—can often be a good compromise when dealing with long videos.

# Sometimes -c copy works for extract clip, sometimes it doesn't
That's correct, and it all comes down to how the extraction boundaries align with the underlying media data. When you use -c copy, ffmpeg doesn't re-encode; it simply copies the existing encoded packets. This means:

Keyframe Boundaries:
The copy method works best if your start time lands on a keyframe (for video) and on proper packet boundaries (for audio). If the extraction point cuts in the middle of a Group of Pictures (GOP) or in the middle of an audio packet, you can end up with corrupted or missing data.

Container and Timestamp Issues:
Some files have more robust indexing or metadata that allows a clean cut, while others may not. If the timestamps or indexing information aren't perfectly aligned, -c copy might sometimes yield a clean cut and sometimes not.

Inconsistent Behavior:
Since the behavior of -c copy depends on the structure of the source file and the precise extraction time, you might see inconsistent results from file to file or even within the same file if the cut points are not ideal.

In short, -c copy works reliably only when the extraction points coincide with valid boundaries in the media streams. If they don't, you might experience issues like frozen video, audio dropouts, or other artifacts. If you need consistent results regardless of boundary alignment, re-encoding (with properly chosen codecs and parameters) is usually the safer option, even though it's more time-consuming.







# ffmpeg versions
We were on ffmpeg 4.4.2 (Ubuntu) but the latest is 7.1 so we want to update.

The issue is im on an older Ubuntu

Looking at the packages I see the latest ffmpeg on ubuntu is actually the latest ffmpeg publishes
7:7.1-3ubuntu3

but for my OS (I think ubuntu 22) we are only only 4.4.2
7:4.4.2-0ubuntu0.22.04.1	

source docs: https://launchpad.net/ubuntu/+source/ffmpeg

We were able to build 7.1 from source. Unfortunately, GPU support turned out to be a pain - see below.

# GPU support
This is a little complicated.

For GPU accelerated reencoding, ffmpeg using NVENC - NVIDIA Encoding (library). NVENC versions are tied to GPUs. Tesla T4 supports up to NVENC 12.1, but the latest FFMPEG (7.1) expects 13. We tried to reinstall an ffmpeg version that expects 12.1, but it's being a pain in the ass. 

Furthermore, it's not even definite that GPU acceleration will really help us. By default, it encodes a lot faster with much lower quality. This aligns with its intent to be used for real time encoding. Chatgpt says it can be tuned to have near indistinguishable quality, but still fast, but given how much a pita this has been, we're going to put it away for now and revisit if we need the speed.

# Tested cmds
  """
  # broken
  # -safe 0 needed to allow relative paths in concat_files.txt
  cmd = [
      "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", 
      "-safe", "0", "-i", f"{output_folder}/concat_files.txt", 
      "-c", "copy", f"{output_folder}/output.mp4"
  ]
  """
  """
  # reencode, works, a lot slower but fine.
  # It's surprising we need to reencode but who 
  cmd = [
      "ffmpeg", "-y", "-hide_banner", "-f", "concat", 
      "-safe", "0", "-i", f"{output_folder}/concat_files.txt", 
      f"{output_folder}/output.mp4"
  ]
  """
  """
  # Goes wayyyy faster with gpu accel, like 10x faster, more
  # There is some weird pause between each clip, it's not ideal, but it's tolerable.
  # Okay but the quality is a lot worse LOL
  cmd = [
      "ffmpeg", "-y", "-hide_banner",
      "-hwaccel", "cuda",            # Optional: for hardware-accelerated decoding
      "-f", "concat",
      "-safe", "0",
      "-i", f"{output_folder}/concat_files.txt",
      "-c:v", "h264_nvenc",          # Use NVIDIA’s GPU-accelerated encoder
      f"{output_folder}/output.mp4"
  ]
  """
  """
  # error excerpt:
  # [h264_nvenc @ 0x5c6609c3d940] Driver does not support the required nvenc API version. Required: 13.0 Found: 12.1
  # t4 only supports up to 12.1, supposedly.
  See README for more
  cmd = [
      "ffmpeg",
      "-y",
      "-hide_banner",
      "-hwaccel", "cuda",          # Optional: for hardware-accelerated decoding
      "-f", "concat",
      "-safe", "0",
      "-i", f"{output_folder}/concat_files.txt",
      "-c:v", "h264_nvenc",        # NVIDIA’s GPU-accelerated H.264 encoder
      "-preset", "slow",           # Slower preset = higher quality
      "-rc", "vbr_hq",             # High-quality variable bitrate mode
      "-cq", "22",                 # Constant quality (lower = better quality, bigger file)
      "-b:v", "0",                 # No hard bitrate limit; focus on quality
      f"{output_folder}/output.mp4"
  ]
  """
  """
  This doesn't work because of nvenc version problems
  cmd = [
      "ffmpeg",
      "-y",
      "-hide_banner",
      "-hwaccel", "cuda",
      "-f", "concat",
      "-safe", "0",
      "-i", f"{output_folder}/concat_files.txt",
      "-c:v", "h264_nvenc",
      "-preset", "medium",   # or "slow" if supported
      "-rc", "vbr",          # simpler rate-control than "vbr_hq"
      "-b:v", "5M",          # target bitrate
      "-maxrate", "8M",      # maximum allowed bitrate
      "-bufsize", "16M",     # VBV buffer size
      "-c:a", "aac",
      "-b:a", "192k",
      f"{output_folder}/output.mp4"
  ]
  """
