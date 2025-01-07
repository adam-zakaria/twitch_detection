
 # watch_and_run.py

import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script_to_run):
        self.script_to_run = script_to_run

    def on_modified(self, event):
        if event.src_path.endswith(self.script_to_run):
            print(f"Change detected in {self.script_to_run}. Running script...")
            subprocess.run([sys.executable, self.script_to_run])

def watch_file(script_to_run):
    event_handler = ChangeHandler(script_to_run)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print('usage: watchman.py <file_to_watch>')
  watch_file(sys.argv[1])

