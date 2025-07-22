import atexit
import signal
import sys
import os

# Global process list
procs = []

def cleanup():
  print('[CLEANUP] Killing all yt-dlp subprocesses...')
  for proc in procs:
    try:
      os.killpg(proc.pid, signal.SIGINT)
    except ProcessLookupError:
      pass  # Already dead

def handle_exit(signum, frame):
  cleanup()
  sys.exit(0)

# Register exit + signal cleanup
atexit.register(cleanup)
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
