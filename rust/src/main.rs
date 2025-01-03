/*
1) Confirm 'double kill can be detected' 
2) For list of twitch accounts, check if online, if online download streams
3) Run detection (transcribe)
4) Get all 'double' timestamps and extract the clips 10 seconds before and 10 seconds after
*/

fn main() {
    // download streams if users online
    // not sure what yt-dlp returns if users online...
    // yt-dlp --skip-download --print "%(is_live)s" https://twitch.tv/spartanthedogg
    // will output the string True is live
    map(['LucidTWW', 'spartanthedogg'], if os.system(f'yt-dlp --skip-download --print "%(is_live)s" https://twitch.tv/{ele}')  == 'True') 
    for stream in os.ls(streams) os.system('transcribe.py stream')
    for transcription in os.ls('transcriptions') get the timestamp each time 'double' occurs

}
    
