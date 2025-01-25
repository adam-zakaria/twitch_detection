import cliptu.s3 as s3; import utils.utils as utils;

#s3.upload_folder('/home/ubuntu/Code/twitch_detection/twitch_streams_time_range', 'twitch')
#s3.upload_folder('test_upload_folder', 'twitch')
print('upload.py', flush=True)
#s3.upload_folder('twitch_streams_time_range', 'twitch_streams')

s3.download_folder('s3://cliptu/twitch_streams', 'twitch_streams')