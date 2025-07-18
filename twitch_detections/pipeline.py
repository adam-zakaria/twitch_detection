import cliptu.utils as cliptu_utils
import cliptu.clip as clip
import cv2
import os
import sys
from pathlib import Path
import happy_utils as utils
import time
import glob

def process(stream_path=''):
    """
    * Reframe
    * Template match
    * Extract clips
    * Concatenate clips
    """
    try:
        utils.w('---- Starting process() ----', 'log.txt')
        print('---- Starting process() ----')

        # Initialize paths
        roi_frames_dir = './output'
        template_path = 'test/frame/double_kill_tighter.png'

        # Reframe
        print('Reframing video to an ROI')
        try:
            start_time = time.time()
            timestamps_and_frames = cliptu_utils.reframe_video_mem(
                input_path=stream_path, x=710, y=479, w=200, h=200, every_nth_frame=60
            )
            end_time = time.time()
            print(f'\ttook {end_time - start_time:.2f} seconds')
        except Exception as e:
            utils.wa('Error during reframing', 'log.txt')
            print(f'Error during reframing: {e}')

        # Template match
        print('Template matching each frame')
        try:
            start_time = time.time()
            match_timestamps = cliptu_utils.template_match_folder(
                timestamps_and_frames=timestamps_and_frames,
                output_folder_path='./template_match',
                template_image_path=template_path,
                log_file_path='./template_match_log.txt',
                threshold=0.8
            )
            end_time = time.time()
            print(f'\ttook {end_time - start_time:.2f} seconds')
            breakpoint()
            # Check for detections
            if match_timestamps is []:
              print('\tNo matches found, exiting process()')
              return

        except Exception as e:
            utils.wa('Error during template matching', 'log.txt')
            print(f'Error during template matching: {e}')

        # Filter timestamps
        print('Filtering timestamps')
        try:
            filtered_timestamps = cliptu_utils.filter_timestamps(match_timestamps)
        except Exception as e:
            utils.wa('Error filtering timestamps', 'log.txt')
            print(f'Error filtering timestamps: {e}')

        # Extract clips
        print('Extracting clips')
        paths = []
        output_dir = './clips'
        utils.mkdir(output_dir)
        print('Created output dir')
        try:
            for timestamp in filtered_timestamps:
                path = clip.extract_clip(
                    stream_path, f'{output_dir}/{timestamp}.mp4',
                    timestamp - 6, timestamp + 3
                )
                paths.append(path)
        except Exception as e:
            utils.wa('Error during clip extraction', 'log.txt')
            print(f'Error during clip extraction: {e}')

        # Concatenate
        print('Concatenating clips')
        try:
            clip.concat(paths)
            print(f'Concatenated {len(paths)} clips to {output_dir}')
        except Exception as e:
            utils.wa('Error during concatenation', 'log.txt')
            print(f'Error during concatenation: {e}')

        # Cleanup
        print('Removing processed streams')
        try:
            for stream_path in glob.glob(f'output/**/stream/*.mp4'):
                utils.rm(stream_path)
        except Exception as e:
            utils.wa('Error removing processed streams', 'log.txt')
            print(f'Error removing processed streams: {e}')

    except Exception as e:
        utils.wa('Exception in process', 'log.txt')
        print(f'Exception {e} in process')

    finally:
        print('---- Finishing process() ----')


if __name__ == "__main__":
  stream_path = 'lucid_3m.mp4' # dk at ~2:16
  process(stream_path)