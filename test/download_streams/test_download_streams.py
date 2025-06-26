import logging
import sys
import utils.utils as utils
from datetime import datetime, timedelta
logging.getLogger("ppocr").disabled = True
sys.path.insert(0, '/Users/azakaria/Code/twitch_detections/test/production')
from main import download_twitch_streams

if __name__ == "__main__":
    utils.log(f'Starting job at {utils.ts()} ################################')
    utils.log(f'Removing twitch_streams from front')
    utils.rm('twitch_streams')
    streamers = ['frosty', 'renegade', 'formal', 'Luciid_TW', 'itzthelastshot', 'SpartanTheDogg', 'SnakeBite', 'aPG', 'Bound', 'kuhlect', 'druk84', 'pzzznguin', 'cykul', 'Tripppey', 'royal2', 'bubudubu', 'mikwen', 'Ogre2', 'HuNteR_Jjx', 'Alleesi', 'Cruvu', 'gunplexion','tashi' ]
    download_twitch_streams(streamers, 'twitch_streams')
