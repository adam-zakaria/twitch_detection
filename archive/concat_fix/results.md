# Results
file1 = "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/Tripppey/02_11_2025_18_59_03/extract/79_73333333333333.mp4"
file2 = "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/output/formal/02_11_2025_19_23_23/extract/238_56666666666666.mp4"
  ```
  cmd = [
      "ffmpeg", "-y", "-hide_banner",
      "-f", "concat",    # Force concat demuxer
      "-safe", "0",      # Allow unsafe file paths (absolute paths, etc.)
      "-i", concat_list_path,
      #"-loglevel", "error",
      "-threads", "0",
      os.path.join(output_folder, "output.mp4")
  ]
  ```
Result: Formal clip audio is mangled.
