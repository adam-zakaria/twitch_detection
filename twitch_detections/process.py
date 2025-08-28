"""
Imports
"""
import traceback
import cliptu
import cv2
import os
import sys
from pathlib import Path
import happy_utils as utils
import time
import glob
import subprocess
import config

def hms(seconds):
    parts = []
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours: parts.append(f"{hours} hours")
    if minutes: parts.append(f"{minutes} minutes")
    if secs or not parts: parts.append(f"{secs} seconds")

    return " ".join(parts)

def process_stream(stream_path=''):
    """
    Given a path to a stream:
    * Template match to detect double kills
    * Extract detected clips
    * Concatenate the clips
    """
    try:
        # start benchmark for process_stream()
        process_stream_start_time = time.time()

        # welcome print
        print(f'Starting process() at {utils.ts()} on {stream_path}')
        print(f'The stream is {hms(cliptu.get_video_length(stream_path))}')

        # Initialize paths
        # Might want to convert this to use Paths instead of opj and splits
        output_base_folder = stream_path.split('/')[0]
        streamer = stream_path.split('/')[1]
        clips_dir = utils.opj(output_base_folder, streamer, 'clips')
        compilation_dir = utils.opj(output_base_folder, streamer, 'compilation')
        template_path = 'test/frame/double_kill_tighter.png'
        compilation_path = utils.opj(compilation_dir, f'{utils.ts()}.mp4')
        utils.mkdir(compilation_dir)
        utils.mkdir(clips_dir)

        # Template match (and create frame generator)
        print('Template matching each frame')
        try:
            start_time = time.time()
            timestamps_and_frames_generator = cliptu.crop(
                input_path=stream_path, x=710, y=479, w=200, h=200, every_nth_frame=60
            )
            match_timestamps = cliptu.template_match_folder(
                timestamps_and_frames=timestamps_and_frames_generator,
                output_folder_path='./template_match',
                template_image_path=template_path,
                log_file_path=config.log_file_path,
                threshold=0.8
            )
            end_time = time.time()
            print(f'\ttook {hms(end_time - start_time)}')
            # Check for detections
            if match_timestamps == []:
              print('\tno matches found, exiting process()')
              return
        except Exception as e:
            utils.wa('Error during template matching', config.log_file_path)
            print(f'Error during template matching: {e}')
            print(f'Returning from process()')
            return

        # Filter timestamps
        print('Filtering timestamps')
        try:
            filtered_timestamps = cliptu.filter_timestamps(match_timestamps)
        except Exception as e:
            utils.wa('Error filtering timestamps', config.log_file_path)
            print(f'Error filtering timestamps: {e}')
            print(f'Returning from process()')
            return

        # Extract clips
        print('Extracting clips')
        paths = []
        try:
            for timestamp in filtered_timestamps:
                path = cliptu.extract_clip(stream_path, utils.opj(clips_dir, f'{timestamp}.mp4'), timestamp - 8, timestamp + 3, log_file_path = config.log_file_path)
                paths.append(path)
        except Exception as e:
            utils.wa('Error during clip extraction', config.log_file_path)
            print(f'Error during clip extraction: {e}')
            print(f'Returning from process()')
            return

        # ***** SKIP CONCATENATION FOR NOW BECAUSE OF CRASHES *****
        # Concatenate clips (for single streamer, need to do an additional concat for all streamers)
        # print('Concatenating clips')
        # try:
        #     cliptu.concat(paths, output_file_path=compilation_path, log_file_path=config.log_file_path)
        #     print(f'Concatenated {len(paths)} clips to {compilation_path}')
        # except Exception as e:
        #     utils.wa('Error during concatenation', config.log_file_path)
        #     print(f'Error during concatenation: {e}')
        #     print(f'Returning from process()')
        #     return

    except Exception as e:
        utils.wa('Exception in process', config.log_file_path)
        print(f'Exception {e} in process')

    finally:
        # Cleanup
        print(f'Removing {stream_path}')
        try:
            utils.rm(stream_path)
        except Exception as e:
            print(f'Error removing processed streams: {e}')
        process_stream_end_time = time.time()
        print(f'process() took {hms(process_stream_end_time - process_stream_start_time)}')
        return

def process_streams():
  # start processing once the streams are killed
  
  # remove all temp streams (not sure why they're still created)
  temp_stream_paths = glob.glob(f'output/**/stream/*.temp.mp4', recursive = True) # ** matches ONE directory, otherwise recursive = True is needed
  for temp_stream_path in temp_stream_paths:
    print(f'Removing {temp_stream_path} ({hms(cliptu.get_video_length(temp_stream_path))})')
    utils.rm(temp_stream_path)

  # get all downloaded stream paths (mp4s)
  stream_paths = glob.glob(f'output/**/stream/*.mp4', recursive = True)
  # process all streams
  print(f'Starting process_streams() on {stream_paths}')
  for stream_path in stream_paths:
    process_stream(stream_path)