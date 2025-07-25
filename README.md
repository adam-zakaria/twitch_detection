# Build
From project root
`poetry build`
creates:
dist/twitch_detections-0.1.0-py3-none-any.whl
dist/twitch_detections-0.1.0.tar.gz
# Install
`poetry install` (initiates a venv and installs the package)
or
`pip install -e .` (works from anywhere)

# Run
`poetry shell`
`pm2 start 'python -u main.py' --name 'twitch'`

# Add packages to project
poetry add <packages>

# Additional commands
`pm2 flush`

# Thoughts / Improvements
## New log proposal
-----------------------
{streamer}
Found 3 matches
Extracting clips to {}
Outputting compilation to {}

## Concat issue
Not sure why but it got a sigkill, maybe from main.py? Not sure...

Concatenating clips
Running command: ffmpeg -y -hide_banner -loglevel error -nostats -i output/Tripppey/clips/161.00008944692908.mp4 -i output/Tripppey/clips/162.0000900025001.mp4 -i output/Tripppey/clips/210.0001166699075.mp4 -i output/Tripppey/clips/297.0001650045835.mp4 -i output/Tripppey/clips/298.00016556015447.mp4 -i output/Tripppey/clips/305.0001694491514.mp4 -i output/Tripppey/clips/306.00017000472235.mp4 -i output/Tripppey/clips/329.0001827828551.mp4 -i output/Tripppey/clips/330.0001833384261.mp4 -i output/Tripppey/clips/331.0001838939971.mp4 -i output/Tripppey/clips/347.0001927831329.mp4 -i output/Tripppey/clips/348.00019333870387.mp4 -i output/Tripppey/clips/359.00019944998473.mp4 -i output/Tripppey/clips/394.00021889496935.mp4 -i output/Tripppey/clips/395.0002194505403.mp4 -i output/Tripppey/clips/396.0002200061113.mp4 -i output/Tripppey/clips/444.00024667351875.mp4 -i output/Tripppey/clips/445.0002472290897.mp4 -i output/Tripppey/clips/454.00025222922864.mp4 -i output/Tripppey/clips/455.0002527847996.mp4 -i output/Tripppey/clips/456.0002533403706.mp4 -i output/Tripppey/clips/467.00025945165146.mp4 -i output/Tripppey/clips/468.00026000722244.mp4 -i output/Tripppey/clips/494.00027445206814.mp4 -i output/Tripppey/clips/495.0002750076391.mp4 -i output/Tripppey/clips/496.0002755632101.mp4 -i output/Tripppey/clips/504.00028000777803.mp4 -i output/Tripppey/clips/505.000280563349.mp4 -i output/Tripppey/clips/515.0002861190588.mp4 -i output/Tripppey/clips/516.0002866746299.mp4 -i output/Tripppey/clips/517.0002872302009.mp4 -i output/Tripppey/clips/540.0003000083336.mp4 -i output/Tripppey/clips/541.0003005639046.mp4 -i output/Tripppey/clips/577.0003205644601.mp4 -i output/Tripppey/clips/578.0003211200311.mp4 -i output/Tripppey/clips/583.0003238978861.mp4 -i output/Tripppey/clips/584.0003244534571.mp4 -filter_complex [0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0][3:v:0][3:a:0][4:v:0][4:a:0][5:v:0][5:a:0][6:v:0][6:a:0][7:v:0][7:a:0][8:v:0][8:a:0][9:v:0][9:a:0][10:v:0][10:a:0][11:v:0][11:a:0][12:v:0][12:a:0][13:v:0][13:a:0][14:v:0][14:a:0][15:v:0][15:a:0][16:v:0][16:a:0][17:v:0][17:a:0][18:v:0][18:a:0][19:v:0][19:a:0][20:v:0][20:a:0][21:v:0][21:a:0][22:v:0][22:a:0][23:v:0][23:a:0][24:v:0][24:a:0][25:v:0][25:a:0][26:v:0][26:a:0][27:v:0][27:a:0][28:v:0][28:a:0][29:v:0][29:a:0][30:v:0][30:a:0][31:v:0][31:a:0][32:v:0][32:a:0][33:v:0][33:a:0][34:v:0][34:a:0][35:v:0][35:a:0][36:v:0][36:a:0]concat=n=37:v=1:a=1[outv][outa] -map [outv] -map [outa] output/Tripppey/compilation/07_24_2025_16_24_13.mp4
Error during concatenation: Command '['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-nostats', '-i', 'output/Tripppey/clips/161.00008944692908.mp4', '-i', 'output/Tripppey/clips/162.0000900025001.mp4', '-i', 'output/Tripppey/clips/210.0001166699075.mp4', '-i', 'output/Tripppey/clips/297.0001650045835.mp4', '-i', 'output/Tripppey/clips/298.00016556015447.mp4', '-i', 'output/Tripppey/clips/305.0001694491514.mp4', '-i', 'output/Tripppey/clips/306.00017000472235.mp4', '-i', 'output/Tripppey/clips/329.0001827828551.mp4', '-i', 'output/Tripppey/clips/330.0001833384261.mp4', '-i', 'output/Tripppey/clips/331.0001838939971.mp4', '-i', 'output/Tripppey/clips/347.0001927831329.mp4', '-i', 'output/Tripppey/clips/348.00019333870387.mp4', '-i', 'output/Tripppey/clips/359.00019944998473.mp4', '-i', 'output/Tripppey/clips/394.00021889496935.mp4', '-i', 'output/Tripppey/clips/395.0002194505403.mp4', '-i', 'output/Tripppey/clips/396.0002200061113.mp4', '-i', 'output/Tripppey/clips/444.00024667351875.mp4', '-i', 'output/Tripppey/clips/445.0002472290897.mp4', '-i', 'output/Tripppey/clips/454.00025222922864.mp4', '-i', 'output/Tripppey/clips/455.0002527847996.mp4', '-i', 'output/Tripppey/clips/456.0002533403706.mp4', '-i', 'output/Tripppey/clips/467.00025945165146.mp4', '-i', 'output/Tripppey/clips/468.00026000722244.mp4', '-i', 'output/Tripppey/clips/494.00027445206814.mp4', '-i', 'output/Tripppey/clips/495.0002750076391.mp4', '-i', 'output/Tripppey/clips/496.0002755632101.mp4', '-i', 'output/Tripppey/clips/504.00028000777803.mp4', '-i', 'output/Tripppey/clips/505.000280563349.mp4', '-i', 'output/Tripppey/clips/515.0002861190588.mp4', '-i', 'output/Tripppey/clips/516.0002866746299.mp4', '-i', 'output/Tripppey/clips/517.0002872302009.mp4', '-i', 'output/Tripppey/clips/540.0003000083336.mp4', '-i', 'output/Tripppey/clips/541.0003005639046.mp4', '-i', 'output/Tripppey/clips/577.0003205644601.mp4', '-i', 'output/Tripppey/clips/578.0003211200311.mp4', '-i', 'output/Tripppey/clips/583.0003238978861.mp4', '-i', 'output/Tripppey/clips/584.0003244534571.mp4', '-filter_complex', '[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0][3:v:0][3:a:0][4:v:0][4:a:0][5:v:0][5:a:0][6:v:0][6:a:0][7:v:0][7:a:0][8:v:0][8:a:0][9:v:0][9:a:0][10:v:0][10:a:0][11:v:0][11:a:0][12:v:0][12:a:0][13:v:0][13:a:0][14:v:0][14:a:0][15:v:0][15:a:0][16:v:0][16:a:0][17:v:0][17:a:0][18:v:0][18:a:0][19:v:0][19:a:0][20:v:0][20:a:0][21:v:0][21:a:0][22:v:0][22:a:0][23:v:0][23:a:0][24:v:0][24:a:0][25:v:0][25:a:0][26:v:0][26:a:0][27:v:0][27:a:0][28:v:0][28:a:0][29:v:0][29:a:0][30:v:0][30:a:0][31:v:0][31:a:0][32:v:0][32:a:0][33:v:0][33:a:0][34:v:0][34:a:0][35:v:0][35:a:0][36:v:0][36:a:0]concat=n=37:v=1:a=1[outv][outa]', '-map', '[outv]', '-map', '[outa]', 'output/Tripppey/compilation/07_24_2025_16_24_13.mp4']' died with <Signals.SIGKILL: 9>.