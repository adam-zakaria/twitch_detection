output_folder: output/Tripppey/02_11_2025_01_14_55/detect
Filtering
The path does not exist: output/Tripppey/02_11_2025_01_14_55/filter
write_filtered_frames()
[h264 @ 0x58a9988df1c0] mmco: unref short failure
[h264 @ 0x58a99eccf2c0] co located POCs unavailable
Writing output/Tripppey/02_11_2025_01_14_55/filter/images/79.73333333333333.jpg
[h264 @ 0x58a99eccf2c0] reference picture missing during reorder
[h264 @ 0x58a99eccf2c0] Missing reference picture, default is 2
[h264 @ 0x58a9988de4c0] mmco: unref short failure
[h264 @ 0x58a99eccf2c0] co located POCs unavailable
[h264 @ 0x58a99ecce540] mmco: unref short failure
[h264 @ 0x58a99ecce540] co located POCs unavailable
[h264 @ 0x58a99eccf2c0] co located POCs unavailable
[h264 @ 0x58a99ecce540] mmco: unref short failure
[h264 @ 0x58a99ecce540] co located POCs unavailable
[h264 @ 0x58a99eccf2c0] co located POCs unavailable
[h264 @ 0x58a99ecce540] mmco: unref short failure
[h264 @ 0x58a99ecce540] co located POCs unavailable
[h264 @ 0x58a99eccf2c0] co located POCs unavailable
[h264 @ 0x58a99ecce540] mmco: unref short failure
[h264 @ 0x58a99ecce540] co located POCs unavailable
Writing output/Tripppey/02_11_2025_01_14_55/filter/images/137.58333333333334.jpg
[h264 @ 0x58a99e6bb540] co located POCs unavailable
[h264 @ 0x58a99ecce540] co located POCs unavailable
Writing output/Tripppey/02_11_2025_01_14_55/filter/images/317.6333333333333.jpg
Writing output/Tripppey/02_11_2025_01_14_55/filter/images/558.8666666666667.jpg
[h264 @ 0x58a99ecce540] co located POCs unavailable
Writing output/Tripppey/02_11_2025_01_14_55/filter/images/605.3.jpg
Writing output/Tripppey/02_11_2025_01_14_55/filter/images/704.1833333333333.jpg
[h264 @ 0x58a998910bc0] co located POCs unavailable
[h264 @ 0x58a99eccf2c0] mmco: unref short failure
[h264 @ 0x58a99eccf2c0] co located POCs unavailable
Writing output/Tripppey/02_11_2025_01_14_55/filter/images/1118.1333333333334.jpg
[h264 @ 0x58a998910bc0] co located POCs unavailable
[h264 @ 0x58a99eccf2c0] mmco: unref short failure
[h264 @ 0x58a99eccf2c0] co located POCs unavailable
Writing output/Tripppey/02_11_2025_01_14_55/filter/images/1174.8.jpg
Traceback (most recent call last):
  File "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/debug_pipeline_all.py", line 180, in <module>
    add_filtered_detections_json(filter_folder /'dk_detections.txt', detect_folder / 'text_detections.json', ts)
    │                            │                                   │                                       └ '02_11_2025_01_14_55'
    │                            │                                   └ PosixPath('output/Tripppey/02_11_2025_01_14_55/detect')
    │                            └ PosixPath('output/Tripppey/02_11_2025_01_14_55/filter')
    └ <function add_filtered_detections_json at 0x7f906a361a80>
  File "/home/ubuntu/Code/twitch_detection/test/download_twitch_streams/debug_pipeline_all.py", line 120, in add_filtered_detections_json
    utils.jd(found, f'output/{ts}/filter/filtered.json')
    │        │                └ '02_11_2025_01_14_55'
    │        └ [{'timestamp': 79.73333333333333, 'text': '100'}, {'timestamp': 79.73333333333333, 'text': 'Double kil'}, {'timestamp': 79.73333...
    └ <module 'utils.utils' from '/home/ubuntu/Code/utils/utils/utils.py'>
  File "/home/ubuntu/Code/utils/utils/utils.py", line 369, in jd
    with open(fp, 'w') as f:
FileNotFoundError: [Errno 2] No such file or directory: 'output/02_11_2025_01_14_55/filter/filtered.json'
ubuntu@ip-172-31-75-23:~/Code/twitch_detection/test/d
ownload_twitch_streams$ 