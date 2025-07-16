import subprocess, time, signal, os

# download streams with yt-dlp
# preexec_fn=os.setsid puts each process and its children its own process group which means yt-dlp and ffmpeg will be killed together (ffmpeg will not hang)
procs = []
for streamer in ['mean3st', 'Trunks', 'HuNteR_Jjx']:
  proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", "--wait-for-video", "600", "-S", f'vcodec:h265,acodec:aac', "--no-part", f"https://www.twitch.tv/{streamer}"], preexec_fn=os.setsid)
  procs.append(proc)

# wait for 2 minutes
time.sleep(120)

# kill all processes
for proc in procs:
  os.killpg(proc.pid, signal.SIGINT)    # graceful Ctrl‑C to the whole group