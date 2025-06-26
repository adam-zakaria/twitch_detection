from yt_dlp import YoutubeDL
import threading


def download_stream(streamer='', output_folder='streams'):
  ydl_opts = {
    'cookiefile': '/Users/azakaria/Code/twitch_detections/cookies.txt',
    'quiet': True,            # suppress all output except errors
    'wait_for_video': (600, 600), # min and max wait time for video to be available
    'format_sort': ['vcodec:h265', 'acodec:aac'],
    'outtmpl': f'{output_folder}/{streamer}.%(ext)s'
  }
  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([f'https://www.twitch.tv/{streamer}'])


if __name__ == '__main__':
  #streamers = ['frosty', 'renegade', 'formal', 'Luciid_TW', 'itzthelastshot', 'SpartanTheDogg', 'SnakeBite', 'aPG', 'Bound', 'kuhlect', 'druk84', 'pzzznguin', 'cykul', 'Tripppey', 'royal2', 'bubudubu', 'mikwen', 'Ogre2', 'HuNteR_Jjx', 'Alleesi', 'Cruvu', 'gunplexion','tashi', 'TchiKK', 'Preecisionn', 'ItzTheLastShot', 'TriPPPeY']
  streamers = ['KingJay', 'HuNteR_Jjx', 'formal']

  for streamer in streamers:
    threading.Thread(target=download_stream, args=(streamer, 'streams')).start()