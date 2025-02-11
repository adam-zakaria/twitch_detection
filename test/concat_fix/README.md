# Concat works
Concat works with this cmd:
  cmd = [
      "ffmpeg", "-y", "-hide_banner", "-f", "concat", 
      "-safe", "0", "-i", f"{output_folder}/concat_files.txt", 
      f"{output_folder}/output.mp4"
  ]
But weirdly, it works with 4.4.2, but not 7.1. It does have that weird freeze between clips but not a big deal.

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
