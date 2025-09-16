import happy_utils as utils
# Streamers to track

"""
streamers = [
    'minib3rzerker', 'hunter_jjx', 'trunks', 'wryce', 'snakebite','bound', 'lqgendd', 'formal', 'barcode_ak', 'Luciid_tw',
    'spartanthedogg', 'Tripppey', 'envor3', 'wutum',
    'pzzznguin', 'manny_hcs', 'druk84', 'lastshot', 'royal2', 'frosty', 'cykul', 'scoobmeister', 'stresss', 'slg_']
"""
streamers = [
    'fluff0132', 'luciid_tw', 'hunter_jjx'
]

# Time offsets (in minutes)
kill_time = 660 # 11 hours (1PM - 12AM
process_time = 662
restart_download_time = 900 # Restart download is currently commented out

log_dir = 'log'
utils.mkdir(log_dir)
log_file_path = utils.opj(log_dir, f'log_{utils.ts()}.txt')