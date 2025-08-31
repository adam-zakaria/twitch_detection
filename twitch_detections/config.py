import happy_utils as utils
# Streamers to track

"""
streamers = [
    'minib3rzerker', 'hunter_jjx', 'trunks', 'wryce', 'snakebite','bound', 'lqgendd', 'formal', 'barcode_ak', 'Luciid_tw',
    'spartanthedogg', 'Tripppey', 'envor3', 'wutum',
    'pzzznguin', 'manny_hcs', 'druk84', 'lastshot', 'royal2', 'frosty', 'cykul', 'scoobmeister', 'stresss', 'slg_']
"""
streamers = [
    'fluff0132', 'luciid_tw'
]

# Time offsets (in minutes)
kill_time = 1
process_time = 2
restart_download_time = 900

log_dir = 'log'
utils.mkdir(log_dir)
log_file_path = utils.opj(log_dir, f'log_{utils.ts()}.txt')