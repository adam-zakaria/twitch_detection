# Run
pm2 start 'python debug_pipeline_all.py' --name 'pipeline' --no-autorestart
pm2 start 'python concat_all.py' --name 'pipeline' --no-autorestart

# Current
We are troubleshooting concatenating all of the videos, with 
twitch_detection/test/download_twitch_streams/concat_all.py
