Twitch stream downloads have broken historically because of ads - yt-dlp does not correctly handle twitch streams with ads - it can't be remember what the ads mess with, but basically corrupts the file - might desync video and audio, etc.

The solution that had been working is to use twitch turbo which removes ads. So --cookies gets passed with the twitch turbo account cookies. However, upon code inspection it seems like --cookies wasn't even getting passed. 

So now we want to run tests to download streams and see if they contain ads. However, if they do contain ads with --cookies it's unclear what direction to go in.

Okay so, download streams and ideally from the thumbnails it will be clear if ads are included - the ads often appear at the beginnning. 

So how to do this...import 