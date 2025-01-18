import subprocess; import uuid; import sys; import cv2; import os; import glob; import utils.utils as utils; from itertools import pairwise; from datetime import datetime, timedelta; import time

def download_twitch_streams_time_range(start_time, end_time, streamers, output_path):
    """
    Checks Twitch streamers' live status within a time range and downloads their streams if they are live.
    """
    print("Starting Twitch stream download within time range.")

    now = datetime.now()
    start_dt = datetime.combine(now.date(), datetime.strptime(start_time, "%H:%M").time())
    end_dt = datetime.combine(now.date(), datetime.strptime(end_time, "%H:%M").time())

    if end_dt <= start_dt:
        end_dt += timedelta(days=1)

    downloaded_streams = []

    while datetime.now() < end_dt:
        current_time = datetime.now()
        if current_time >= start_dt:
            print(f"In the time range ({current_time.strftime('%H:%M:%S')} EST). Checking streams...")
            processes = []
            for streamer in streamers:
                result = subprocess.run(['yt-dlp', '--get-url', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}', '-o', f'{output_path}/stream.%(ext)s'], text=True, capture_output=True)
                if "The channel is not currently live" in result.stderr:
                    print(f"{streamer} is not currently live.")
                else:
                    utils.mkdir(output_path)
                    print(f"Downloading {streamer} to {output_path}...")
                    process = subprocess.Popen(['yt-dlp', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}', '-o', f'{output_path}/{streamer}/{uuid.uuid4().hex}.%(ext)s'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    processes.append(process)

            for process in processes:
                process.wait()

            downloaded_streams.extend(glob.glob(f'{output_path}/**/*.mp4'))
            print("Checked streams. Next check in 10 minutes.")
        else:
            print(f"Out of time range ({current_time.strftime('%H:%M:%S')} EST). Sleeping...")

        time.sleep(10 * 60)

    print(f"Time range ended. Downloads completed. Streams saved in {output_path}.")
    return downloaded_streams

def download_twitch_streams(streamers, output_path):
    """
    Downloads live Twitch streams from a list of streamers to the specified output path.
    """
    print("Starting Twitch stream download.")
    processes = []
    for streamer in streamers:
        if "The channel is not currently live" in subprocess.run(
            ['yt-dlp', '--get-url', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}', '-o', f'{output_path}/stream.%(ext)s'],
            text=True, capture_output=True
        ).stderr:
            print(f"{streamer} is not currently live.")
        else:
            utils.mkdir(output_path)
            print(f"Downloading {streamer} to {output_path}...")
            process = subprocess.Popen(
                ['yt-dlp', '-S', 'vcodec:h265,acodec:aac', f'https://www.twitch.tv/{streamer}', '-o', f'{output_path}/{streamer}/{uuid.uuid4().hex}.%(ext)s'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            processes.append(process)

    for process in processes:
        process.wait()

    print(f"All downloads completed. Streams saved in {output_path}.")
    return glob.glob(f'{output_path}/**/*.mp4')

def detect(streams):
    """
    Detects specific patterns (e.g., 'Dou') in the frames of video streams and logs detection times.
    """
    print("Starting detection process.")
    utils.rm('tesseract_frames'); utils.mkdir('tesseract_frames'); utils.rm('tesseract_output'); utils.mkdir('tesseract_output'); utils.rm('dk_detections.txt')

    for stream in streams:
        print(f"Processing stream: {stream}")
        for i, (frame, frame_rate) in enumerate(utils.get_frames(stream)):
            frame = frame[441:441+131, 529:529+266]
            cv2.imwrite(f'tesseract_frames/{i}.png', frame)
            print(f'Detection on frame {i}')
            subprocess.run(['tesseract', f'tesseract_frames/{i}.png', f'tesseract_output/{i}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time_in_seconds = i / frame_rate
            if 'Dou' in utils.r(f'tesseract_output/{i}.txt'):
                print(f"Detection at time: {time_in_seconds}s in stream {stream}")
                utils.wa(f'{time_in_seconds}\n', 'dk_detections.txt')

    print("Detection process completed. Results saved in 'dk_detections.txt'.")

def extract(detections_path, clips_output_path):
    """
    Extracts video clips based on detection times.
    """
    print("Starting clip extraction.")
    mk_ss = [a for a, b in pairwise(map(float, utils.rl('dk_detections.txt'))) if (b - a) > 3]

    if not mk_ss:
        print("No detections found. Skipping clip extraction.")
        return

    import cliptu.clip as clip
    utils.rm_mkdir(clips_output_path)

    for s in mk_ss:
        print(f"Extracting clip around {s}s...")
        clip.extract_clip(stream_path, f'{clips_output_path}/{s}.mp4', s-8, s+1)

    print(f"Clips saved in {clips_output_path}.")

def concat(clips_path):
    """
    Concatenates multiple video clips into a single video.
    """
    print("Starting clip concatenation.")
    for clip_path in utils.ls(clips_path):
        print(f"Adding {clip_path} to concatenation list.")
        utils.wa(f"file '{clip_path}'", 'concat/concat_files.txt')

    output_folder = 'concat'
    utils.rm_mkdir(output_folder)
    subprocess.run(
        ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'concat/concat_files.txt', '-c', 'copy', f'{output_folder}/output.mp4'],
        check=True
    )
    print(f"Concatenated video saved in {output_folder}/output.mp4.")
    return output_folder

if __name__ == "__main__":
    if (len(sys.argv) > 2):
        print('Usage: python main.py <download_twitch_streams | detect | filter | concat>')
        sys.exit()

    streamers = ['Luciid_TW', 'itzthelastshot', 'SpartanTheDogg', 'SnakeBite', 'aPG']
    streams_output_path = 'twitch_streams'

    if len(sys.argv) == 1:
        download_twitch_streams_time_range("00:00", "23:00", streamers, "./twitch_streams_time_range")
        detect(glob.glob(f'{streams_output_path}/**/*.mp4'))
        extract('detections', 'clips')
        concat('clips')
    else:
        if sys.argv[1] == 'download_twitch_streams':
            download_twitch_streams(streamers, streams_output_path)
        elif sys.argv[1] == 'detect':
            video_files = glob.glob(f'{streams_output_path}/**/*.mp4')
            detect(video_files)
        elif sys.argv[1] == 'extract':
            extract('detections', 'clips')
        elif sys.argv[1] == 'concat':
            concat('clips')
        elif sys.argv[1] == 'download_twitch_streams_time_range':
            download_twitch_streams_time_range("00:00", "23:00", streamers, "./twitch_streams_time_range")
        else:
            print('Invalid command. Use one of: download_twitch_streams, detect, extract, concat.')
            sys.exit()
