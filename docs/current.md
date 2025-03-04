# Current
* We are testing the filter .mp4 fix.
* Okay, so our .mp4 filter was not working, so we've updated it and added logging:
    gpu_process.py
        input_video_paths = [p for p in utils.ls('twitch_streams') if p.endswith(".mp4") and not p.endswith(".temp.mp4")] # filter .mp4s, avoiding .temp.mp4
        utils.log(f'input_video_paths: {input_video_paths}')

Next, run main.py for 30min (current setting) and see the logs. Expect detection.

# More
* There's the question of: Should we change:
        os.system('./g4dn_xlarge_stop.sh')
        to popen?
        Right now, closing the parent terminal kills the child process..Which SEEMS to kill the GPU, but it's not clear how. In yt-dlp, a sigint handler wraps things up, here there is no such thing. main.py will run in pm2...
        The next command after:
        ssh "$INSTANCE_NAME" "rm -rf /home/ubuntu/Code/twitch_detection && git clone git@github.com:adam-zakaria/twitch_detection.git /home/ubuntu/Code/twitch_detection && cd /home/ubuntu/Code/twitch_detection/test/production && python gpu_process.py"

        is shutdown, so if gpu_process.py gets interrupted shutdown will execute next likely. 
