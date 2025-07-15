import subprocess, time, signal, os

url = "https://www.twitch.tv/luciid_tw"

# download streams with yt-dlp
# preexec_fn=os.setsid is used to kill the whole process group
proc = subprocess.Popen(["yt-dlp", "--cookies", "cookies.txt", "--wait-for-video", "600", "-S", f'vcodec:h265,acodec:aac', "--no-part", url], preexec_fn=os.setsid)

time.sleep(20)

os.killpg(proc.pid, signal.SIGINT)    # graceful Ctrl‑C to the whole group

# Then there's the matter of killing everything at once... If 
