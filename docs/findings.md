# What is .mp4.part
Not sure, but VLC can play it and ffprobe can introspect it. So the wrinkle it introduces into the program is probably just how the filename is read.

ffprobe -v error -print_format json -show_format -show_streams TchiKK.mp4.part

This shows information that can be used to check that the streams are correct.

# Medals
It seems like 3-4 medals is the max that can be displayed at once. This could be tested by killing a lot of bots with rockets.

It's displayed on a vertical column.