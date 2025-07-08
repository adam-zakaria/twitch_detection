# Intro
This folder is being used to create ML set for double kills.

# Scratch
ls -1 selected_frames_double_kills | wc -l 
      73

➜  ~ ffprobe -v error \
  -select_streams v:0 \
  -show_entries stream=nb_frames \
  -of default=noprint_wrappers=1:nokey=1 \
  /Users/azakaria/Downloads/dks_only.mov

1162
80, 10, 10 split





# Current
So maybe chop this up more and random sample? Should be enough. Even though it's a pain.